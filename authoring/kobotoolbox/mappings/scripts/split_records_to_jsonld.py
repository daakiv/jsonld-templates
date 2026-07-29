#!/usr/bin/env python3
"""
Generate ONE JSON-LD file per Kobo record (88 files, not one combined @graph).

Run from: authoring/kobotoolbox/mappings/scripts

    python3 split_records_to_jsonld.py \
        --sssom  ../sssom/kobo_form.sssom.tsv \
        --input  ../../records/raw/all_records_raw.json \
        --outdir ../../records/outputs/per_record

For each record it writes  record_<id>_<table_name>.jsonld  into --outdir.

Why this exists
    sssom_to_jsonld.py always writes a single combined @graph. To get one file per
    record, we split all_records_raw.json into single records and call the transformer
    once per record. A single bare record IS wrapped (--wrap-key datasets); the combined
    all_records_raw.json is already wrapped and must NOT be (that double-wraps and yields
    one record).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def record_id(rec: dict) -> str | None:
    for key in ("control_group/id", "id", "_id"):
        val = rec.get(key)
        if val not in (None, ""):
            return str(val).replace(".0", "")   # 116.0 -> 116 (Excel float artefact)
    return None


def make_slug(rec: dict, rid: str | None, idx: int) -> str:
    table = rec.get("etl_group/table_name") or ""
    table = re.sub(r"[^A-Za-z0-9_-]+", "_", str(table)).strip("_").lower()
    base = f"record_{rid}" if rid else f"record_idx{idx}"
    return f"{base}_{table}" if table else base


def main() -> None:
    here = Path(__file__).parent
    parser = argparse.ArgumentParser(description="Emit one JSON-LD file per Kobo record.")
    parser.add_argument("--sssom", type=Path, default=here / "../sssom/kobo_form.sssom.tsv")
    parser.add_argument("--input", type=Path, default=here / "../../records/raw/all_records_raw.json")
    parser.add_argument("--outdir", type=Path, default=here / "../../records/outputs/per_record")
    parser.add_argument("--transformer", type=Path, default=here / "sssom_to_jsonld.py")
    parser.add_argument("--keep-split", action="store_true",
                        help="Keep the intermediate single-record raw files.")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    records = data["datasets"] if isinstance(data, dict) and "datasets" in data else data
    if not isinstance(records, list):
        sys.exit("Input is not a list of records or a {'datasets': [...]} wrapper.")

    args.outdir.mkdir(parents=True, exist_ok=True)
    split_dir = args.outdir / "_split_raw"
    split_dir.mkdir(exist_ok=True)

    print(f"Records to process: {len(records)}")
    ok = fail = 0
    used: set[str] = set()
    manifest = []
    duplicate_ids: dict[str, int] = {}

    for idx, rec in enumerate(records):
        rid = record_id(rec)
        slug = make_slug(rec, rid, idx)

        # guarantee unique filenames (the data contains duplicate control ids)
        final = slug
        n = 2
        while final in used:
            final = f"{slug}__{n}"
            n += 1
            duplicate_ids[slug] = duplicate_ids.get(slug, 1) + 1
        used.add(final)

        raw_path = split_dir / f"{final}_raw.json"
        raw_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")

        out_path = args.outdir / f"{final}.jsonld"
        proc = subprocess.run(
            [sys.executable, str(args.transformer),
             "--sssom", str(args.sssom),
             "--input", str(raw_path),
             "--output", str(out_path),
             "--wrap-key", "datasets"],   # single bare record -> wrap
            capture_output=True, text=True,
        )
        if proc.returncode == 0 and out_path.exists():
            ok += 1
            manifest.append({
                "file": out_path.name,
                "record_id": rid,
                "table_name": rec.get("etl_group/table_name"),
                "structure": rec.get("iso_group/structure"),
            })
        else:
            fail += 1
            print(f"  FAIL {final}: {proc.stderr.strip()[-200:]}")

    (args.outdir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    if not args.keep_split:
        for f in split_dir.glob("*.json"):
            f.unlink()
        split_dir.rmdir()

    print(f"\nDone: {ok} written, {fail} failed -> {args.outdir}")
    if duplicate_ids:
        print(f"NOTE: {len(duplicate_ids)} record id(s) were duplicated in the source "
              f"(saved with __2/__3 suffixes; they share the same @id and will collide "
              f"in a catalogue keyed on @id).")


if __name__ == "__main__":
    main()
