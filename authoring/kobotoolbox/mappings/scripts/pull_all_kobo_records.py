#!/usr/bin/env python3
"""
Pull ALL KoboToolbox submissions for a form and write them as one wrapped JSON file,
plus a prompt-sized sample and a field inventory.

Outputs (under authoring/kobotoolbox/records/raw/):
- all_records_raw.json      {"datasets": [ ...every record... ]}  -> feed the transformer
- sample_records_raw.json   {"datasets": [ ...N per dataset type... ]} -> paste into the prompt
- field_inventory.md        union of all fields (+ vector-only / raster-only detection)
- all_records_keys.txt      flat sorted list of every field key seen
- record_<id>_raw.json      single bare record, only when --record-id is given (back-compat)

IMPORTANT
    all_records_raw.json is ALREADY wrapped as {"datasets": [...]}, which is the shape the
    SSSOM source_jsonpath expressions ($.datasets[*][...]) expect. Do NOT pass --wrap-key
    when running the transformer on it, or it will be double-wrapped and produce nothing:

        python 03_sssom_to_jsonld_extra.py \
            --sssom  mappings/sssom/kobo_testing_merged.sssom.tsv \
            --input  records/raw/all_records_raw.json \
            --output records/outputs/all_records.jsonld

    (--wrap-key datasets is only for a single bare record, e.g. record_136_raw.json.)

Environment variables:
- KOBO_API_TOKEN
- KOBO_SERVER_URL   optional, defaults to https://kf.kobotoolbox.org
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from getpass import getpass
from pathlib import Path

import requests

# Kobo envelope/system fields — listed separately in the inventory so the prompt can see
# them without confusing them for real form fields.
SYSTEM_FIELD_PREFIXES = ("_", "formhub/", "meta/", "__")

# Field whose value tells us the dataset type; drives vector/raster conditional detection.
STRUCTURE_FIELD = "iso_group/structure"


# --------------------------------------------------------------------------------------
# repo / http helpers
# --------------------------------------------------------------------------------------

def find_repo_root(start_path: Path | None = None) -> Path:
    """Find the Git repository root by walking upward until .git is found."""
    start_path = Path(start_path or Path.cwd()).resolve()

    for path in [start_path, *start_path.parents]:
        if (path / ".git").exists():
            return path

    raise RuntimeError("Could not find repository root. Run this script from inside the Git repo.")


def get_json(url: str, headers: dict, timeout: int = 60) -> dict:
    """GET a URL and return parsed JSON."""
    response = requests.get(url, headers=headers, timeout=timeout)
    print(f"GET {response.url} -> {response.status_code}")
    response.raise_for_status()
    return response.json()


def fetch_paginated_results(start_url: str, headers: dict) -> list[dict]:
    """Fetch all paginated results from a Kobo v2 API endpoint."""
    results: list[dict] = []
    next_url = start_url

    while next_url:
        payload = get_json(next_url, headers=headers)
        results.extend(payload.get("results", []))
        next_url = payload.get("next")

    return results


def resolve_data_url(server_url: str, headers: dict, form_name: str, asset_uid: str | None) -> str:
    """Return the submissions endpoint for the target form."""
    base = server_url.rstrip("/")

    if asset_uid:
        return f"{base}/api/v2/assets/{asset_uid}/data/"

    print("\nFetching Kobo forms/assets...")
    assets = fetch_paginated_results(f"{base}/api/v2/assets/", headers=headers)

    target = form_name.strip().lower()
    for asset in assets:
        if asset.get("name", "").strip().lower() == target:
            print(f"\nFound form: {asset.get('name')}")
            print(f"UID: {asset.get('uid')}  (tip: pass --asset-uid to skip this lookup)")
            data_url = asset.get("data")
            if not data_url:
                raise ValueError("The target Kobo form does not have a data endpoint.")
            return data_url

    print("\nAvailable form names:")
    for name in sorted(a.get("name", "") for a in assets if a.get("name")):
        print("-", name)
    raise ValueError(f"Could not find a form named '{form_name}'")


# --------------------------------------------------------------------------------------
# record helpers  (pure functions — unit-testable without the API)
# --------------------------------------------------------------------------------------

def get_record_id(record: dict) -> str | None:
    """Return the legacy/control ID from a Kobo record."""
    for key in ("control_group/id", "id", "ID", "dataset_id", "record_id"):
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def sort_key(record: dict) -> tuple[int, str]:
    """Sort records by numeric control ID when possible, so output diffs stay stable."""
    rid = get_record_id(record) or ""
    return (0, f"{int(rid):012d}") if rid.isdigit() else (1, rid)


def is_system_field(key: str) -> bool:
    return key.startswith(SYSTEM_FIELD_PREFIXES)


def structure_of(record: dict) -> str:
    """vector / raster / unknown."""
    return str(record.get(STRUCTURE_FIELD, "") or "unknown").strip().lower() or "unknown"


def summarise_value(value) -> tuple[str, list[str], str]:
    """
    Return (kind, subkeys, example) for a field value.

    kind    : 'repeat_group' when the value is a list of objects, else 'scalar'
    subkeys : sub-field names seen inside a repeat group
    example : short printable example of the value
    """
    if isinstance(value, list) and value and isinstance(value[0], dict):
        subkeys = sorted({k for item in value if isinstance(item, dict) for k in item})
        example = json.dumps(value[0], ensure_ascii=False)[:120]
        return "repeat_group", subkeys, example

    example = json.dumps(value, ensure_ascii=False)
    return "scalar", [], example[:120]


def build_field_inventory(records: list[dict]) -> dict:
    """
    Build the union of all fields across records.

    For each field: how many records carry it, whether it is a repeat group (and its
    sub-fields), an example value, and which dataset types it appears under — which is
    what lets the prompt mark rows VECTOR ONLY / RASTER ONLY.
    """
    total = len(records)
    counts: Counter[str] = Counter()
    kinds: dict[str, str] = {}
    subkeys: dict[str, set[str]] = defaultdict(set)
    examples: dict[str, str] = {}
    types_seen: dict[str, set[str]] = defaultdict(set)

    structure_totals = Counter(structure_of(r) for r in records)

    for record in records:
        struct = structure_of(record)
        for key, value in record.items():
            counts[key] += 1
            types_seen[key].add(struct)
            kind, subs, example = summarise_value(value)
            # a field is a repeat group if it is ever seen as one
            kinds[key] = "repeat_group" if kinds.get(key) == "repeat_group" or kind == "repeat_group" else "scalar"
            subkeys[key].update(subs)
            examples.setdefault(key, example)

    fields = {}
    for key in sorted(counts):
        seen = types_seen[key]
        # "only" == appears exclusively under one dataset type that has >1 record overall
        exclusive = None
        real_types = {t for t in seen if t != "unknown"}
        if len(real_types) == 1:
            only = next(iter(real_types))
            if structure_totals.get(only, 0) > 0 and len(structure_totals) > 1:
                exclusive = only

        fields[key] = {
            "present_in": counts[key],
            "of_total": total,
            "kind": kinds[key],
            "subfields": sorted(subkeys[key]),
            "example": examples[key],
            "dataset_types": sorted(seen),
            "exclusive_to": exclusive,
            "system_field": is_system_field(key),
        }

    return {
        "record_count": total,
        "structure_counts": dict(structure_totals),
        "field_count": len(fields),
        "fields": fields,
    }


def render_field_inventory_md(inventory: dict) -> str:
    """Render the inventory as markdown — this is the file you attach to the prompt."""
    lines: list[str] = []
    lines.append("# Kobo form field inventory")
    lines.append("")
    lines.append(f"Built from **{inventory['record_count']} records**. "
                 f"Dataset types: {inventory['structure_counts']}.")
    lines.append("")
    lines.append("Treat this as the form schema: the union of every field across all records. "
                 "`exclusive to` marks fields seen only under one dataset type — map those as "
                 "conditional rows (VECTOR ONLY / RASTER ONLY) so one file serves every record.")
    lines.append("")
    lines.append("> **Caveat:** `exclusive to` is evidence from the records pulled, not a "
                 "guarantee about the form. A field can look type-exclusive simply because the "
                 "records of the other type happened to leave it blank (a DOI, for example). "
                 "Confirm against the form definition before treating a row as conditional.")
    lines.append("")

    form_fields = {k: v for k, v in inventory["fields"].items() if not v["system_field"]}
    system_fields = [k for k, v in inventory["fields"].items() if v["system_field"]]

    lines.append(f"## Form fields ({len(form_fields)})")
    lines.append("")
    lines.append("| field (exact Kobo key) | present | kind | exclusive to | sub-fields | example |")
    lines.append("|---|---|---|---|---|---|")
    for key, info in form_fields.items():
        subs = ", ".join(f"`{s.split('/')[-1]}`" for s in info["subfields"]) or "—"
        excl = f"**{info['exclusive_to']}**" if info["exclusive_to"] else "—"
        example = info["example"].replace("|", "\\|")[:70]
        lines.append(
            f"| `{key}` | {info['present_in']}/{info['of_total']} | {info['kind']} "
            f"| {excl} | {subs} | `{example}` |"
        )

    lines.append("")
    lines.append(f"## Kobo envelope / system fields ({len(system_fields)})")
    lines.append("")
    lines.append("Document these as intentional non-mappings (one representative `skos:noMatch` row), "
                 "with the deliberate exceptions noted in the prompt.")
    lines.append("")
    lines.append(", ".join(f"`{k}`" for k in system_fields) or "_none_")
    lines.append("")
    return "\n".join(lines)


def select_samples(records: list[dict], per_type: int = 2) -> list[dict]:
    """
    Pick a small, field-rich set of records covering every dataset type.

    Within each type the records with the most populated fields are chosen, so the sample
    exercises as much of the form as possible.
    """
    by_type: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_type[structure_of(record)].append(record)

    chosen: list[dict] = []
    for struct in sorted(by_type):
        ranked = sorted(by_type[struct], key=lambda r: len(r), reverse=True)
        chosen.extend(ranked[:per_type])

    return sorted(chosen, key=sort_key)


def wrap(records: list[dict], key: str = "datasets") -> dict:
    """Wrap records in the shape the SSSOM source paths expect: {"datasets": [...]}"""
    return {key: records}


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pull all KoboToolbox submissions into one wrapped JSON file, "
                    "plus a prompt-sized sample and a field inventory."
    )
    parser.add_argument("--form-name", default="GDSC",    # Change "GDSC" to your actual Kobo form name #
                        help="Kobo form name to search for.")
    parser.add_argument("--asset-uid", default=None,
                        help="Kobo asset UID. Skips the form-name lookup when supplied.")
    parser.add_argument("--server-url", default=os.getenv("KOBO_SERVER_URL", "https://kf.kobotoolbox.org"),
                        help="KoboToolbox server URL.")
    parser.add_argument("--wrap-key", default="datasets",
                        help="Top-level key to wrap records under. Default: datasets")
    parser.add_argument("--samples-per-type", type=int, default=2,
                        help="Records to include per dataset type in the prompt sample. Default: 2")
    parser.add_argument("--record-id", default=None,
                        help="Optional: also write a single bare record_<id>_raw.json (back-compat).")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Override the output directory.")
    args = parser.parse_args()

    if args.out_dir:
        raw_dir = args.out_dir
        repo_root = None
    else:
        repo_root = find_repo_root()
        raw_dir = repo_root / "authoring" / "kobotoolbox" / "records" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    api_token = (os.getenv("KOBO_API_TOKEN") or getpass("Paste Kobo API token: ")).strip()
    if not api_token:
        raise ValueError("No Kobo API token provided.")

    headers = {"Authorization": f"Token {api_token}", "Accept": "application/json"}

    if repo_root:
        print("Repository root:", repo_root)
    print("Output directory:", raw_dir)

    data_url = resolve_data_url(args.server_url, headers, args.form_name, args.asset_uid)

    print("\nFetching submissions...")
    submissions = fetch_paginated_results(data_url, headers=headers)
    print(f"Total submissions retrieved: {len(submissions)}")

    if not submissions:
        raise ValueError("No submissions returned for this form.")

    records = sorted(submissions, key=sort_key)

    # flag duplicate control IDs rather than silently shipping them
    ids = [rid for rid in (get_record_id(r) for r in records) if rid]
    duplicates = [rid for rid, n in Counter(ids).items() if n > 1]
    if duplicates:
        print(f"\nWARNING: duplicate control IDs found: {sorted(duplicates)[:20]}")

    # ---- 1. every record, wrapped -----------------------------------------------------
    all_file = raw_dir / "all_records_raw.json"
    with open(all_file, "w", encoding="utf-8") as fh:
        json.dump(wrap(records, args.wrap_key), fh, indent=2, ensure_ascii=False)

    # ---- 2. prompt-sized sample -------------------------------------------------------
    samples = select_samples(records, per_type=args.samples_per_type)
    sample_file = raw_dir / "sample_records_raw.json"
    with open(sample_file, "w", encoding="utf-8") as fh:
        json.dump(wrap(samples, args.wrap_key), fh, indent=2, ensure_ascii=False)

    # ---- 3. field inventory -----------------------------------------------------------
    inventory = build_field_inventory(records)

    inventory_json = raw_dir / "field_inventory.json"
    with open(inventory_json, "w", encoding="utf-8") as fh:
        json.dump(inventory, fh, indent=2, ensure_ascii=False)

    inventory_md = raw_dir / "field_inventory.md"
    with open(inventory_md, "w", encoding="utf-8") as fh:
        fh.write(render_field_inventory_md(inventory))

    keys_file = raw_dir / "all_records_keys.txt"
    with open(keys_file, "w", encoding="utf-8") as fh:
        for key in sorted(inventory["fields"]):
            fh.write(key + "\n")

    # ---- 4. optional single record (back-compat) --------------------------------------
    if args.record_id:
        match = next((r for r in records if get_record_id(r) == str(args.record_id)), None)
        if match is None:
            print(f"\nWARNING: no record found with ID {args.record_id}; skipping single-record file.")
        else:
            single_file = raw_dir / f"record_{args.record_id}_raw.json"
            with open(single_file, "w", encoding="utf-8") as fh:
                json.dump(match, fh, indent=2, ensure_ascii=False)
            print(f"\nSingle bare record written: {single_file}")

    # ---- summary ----------------------------------------------------------------------
    struct_summary = ", ".join(f"{k}={v}" for k, v in sorted(inventory["structure_counts"].items()))
    sample_ids = [get_record_id(r) for r in samples]

    print("\n" + "=" * 72)
    print(f"Records written : {len(records)}   ({struct_summary})")
    print(f"Fields in form  : {inventory['field_count']} unique keys")
    print("=" * 72)
    print(f"  {all_file.name:<26} all records, wrapped under '{args.wrap_key}'")
    print(f"  {sample_file.name:<26} {len(samples)} records {sample_ids} for the prompt")
    print(f"  {inventory_md.name:<26} field union + vector/raster detection")
    print(f"  {inventory_json.name:<26} same inventory, machine-readable")
    print(f"  {keys_file.name:<26} flat key list")

    print("\nNext steps")
    print("  Generate a mapping : attach field_inventory.md + sample_records_raw.json to the prompt")
    print("  Transform ALL      : python 03_sssom_to_jsonld_extra.py \\")
    print("                         --sssom <mapping>.sssom.tsv \\")
    print(f"                         --input {all_file} \\")
    print("                         --output <out>.jsonld")
    print("                       (no --wrap-key: this file is already wrapped)")


if __name__ == "__main__":
    main()
