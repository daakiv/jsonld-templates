#!/usr/bin/env python3
"""Data-quality + transform validation for the Kobo -> SSSOM -> JSON-LD pipeline.

Reproduces the migration-issue checks (duplicate / float / malformed / missing),
classifies duplicates (true duplicate submission vs id collision), runs the
transformer, and STORES the result as reproducible artifacts under the
validation directory:

    qc_issues.tsv     per-record issue table
    qc_summary.md     human-readable report (the numbers + duplicate breakdown)
    qc_summary.json   machine-readable report (same data + provenance)

Usage:
  python3 qc_report.py \
     --input ../../records/raw/all_records_raw.json \
     --sssom ../sssom/kobo_form.regenerated_128.sssom.tsv \
     --out   ../../records/validation/qc_issues.tsv
"""
import argparse, json, re, sys, subprocess, tempfile, datetime
from collections import Counter, defaultdict
from pathlib import Path

def is_float_formatted(v):
    if isinstance(v, float): return True
    return bool(re.fullmatch(r'-?\d+\.\d+', str(v).strip()))

def norm_id(v):
    s = str(v).strip()
    if is_float_formatted(v):
        try: return str(int(float(s)))
        except ValueError: return s
    return s

def git_commit(start: Path):
    try:
        return subprocess.run(["git","-C",str(start),"rev-parse","--short","HEAD"],
                              capture_output=True, text=True).stdout.strip() or None
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--sssom", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None,
                    help="per-record issue table (TSV). Its directory also receives "
                         "qc_summary.md / qc_summary.json unless --no-report is set.")
    ap.add_argument("--no-report", action="store_true",
                    help="skip writing qc_summary.md / qc_summary.json")
    a = ap.parse_args()

    d = json.load(open(a.input))
    recs = d["datasets"] if isinstance(d, dict) and "datasets" in d else d
    n = len(recs)
    ID, DESC, TBL = "control_group/id", "dublin_core_group/description", "etl_group/table_name"

    # ---- checks ----
    id_norm = [norm_id(r.get(ID)) for r in recs]
    counts = Counter(id_norm)
    dup_ids = {k: c for k, c in counts.items() if c > 1 and k not in ("None", "")}

    # classify duplicates: same table_name = true dup; different = id collision
    tables_by_id = defaultdict(list)
    for r in recs:
        tables_by_id[norm_id(r.get(ID))].append(r.get(TBL))
    true_dups, collisions = {}, {}
    for k in dup_ids:
        uniq = sorted(set(tables_by_id[k]))
        (true_dups if len(uniq) == 1 else collisions)[k] = {
            "count": len(tables_by_id[k]), "tables": uniq}

    float_ids = [{"index": i, "id": r.get(ID)} for i, r in enumerate(recs) if is_float_formatted(r.get(ID))]

    def malformed_keys(r):
        out = []
        for k in r.keys():
            if "/__/" in k: out.append(k)
            elif k.count("time_period_start") and k.count("time_period_end"): out.append(k)
        return out
    malformed = [{"index": i, "id": r.get(ID), "keys": malformed_keys(r)}
                 for i, r in enumerate(recs) if malformed_keys(r)]

    def missing_desc(r):
        v = r.get(DESC)
        return v is None or str(v).strip() in ("", "--", "TBD", "tbd", "n/a", "N/A")
    no_desc = [{"index": i, "id": r.get(ID), "table": r.get(TBL)}
               for i, r in enumerate(recs) if missing_desc(r)]

    # ---- transform validation ----
    transform = {"ran": False}
    if a.sssom:
        tj = Path(__file__).resolve().parent / "sssom_to_jsonld.py"
        if tj.exists():
            outp = Path(tempfile.mkdtemp()) / "all.jsonld"
            res = subprocess.run([sys.executable, str(tj), "--sssom", str(a.sssom),
                                  "--input", str(a.input), "--output", str(outp)],
                                 capture_output=True, text=True)
            transform["ran"] = True
            transform["ok"] = (res.returncode == 0)
            if outp.exists():
                g = json.load(open(outp)).get("@graph", [])
                def empties(o):
                    c = 0
                    if isinstance(o, dict):
                        if o.get("@type") == "PropertyValue" and not o.get("name") and not str(o.get("value","")).strip(): c += 1
                        for v in o.values(): c += empties(v)
                    elif isinstance(o, list):
                        for v in o: c += empties(v)
                    return c
                unmapped = Counter()
                for obj in g:
                    lic = obj.get("license")
                    if isinstance(lic, str) and not lic.startswith("http"): unmapped[lic] += 1
                transform.update(datasets=len(g), empty_property_values=sum(empties(o) for o in g),
                                 unmapped_license_codes=dict(unmapped))

    # ---- assemble report ----
    report = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "input_file": a.input.name, "record_count": n,
        "mapping_file": a.sssom.name if a.sssom else None,
        "git_commit": git_commit(a.input.resolve().parent),
        "python": sys.version.split()[0],
        "checks": {
            "duplicate_control_group_id": {
                "ids": len(dup_ids), "records": sum(dup_ids.values()),
                "true_duplicate_submissions": true_dups, "id_collisions": collisions},
            "float_formatted_ids": {"records": len(float_ids), "detail": float_ids},
            "malformed_concatenated_key": {"records": len(malformed), "detail": malformed},
            "missing_descriptions": {"records": len(no_desc), "detail": no_desc},
        },
        "transform": transform,
    }

    # ---- console ----
    print("=" * 64)
    print(f"DATA-QUALITY REPORT  —  {n} records  ({a.input.name})")
    print("=" * 64)
    c = report["checks"]
    print(f"1. Duplicate control_group/id : {c['duplicate_control_group_id']['ids']} ids / "
          f"{c['duplicate_control_group_id']['records']} records "
          f"({len(true_dups)} true dups, {len(collisions)} collisions)")
    for k, v in sorted(collisions.items()):
        print(f"     COLLISION id {k}: {v['tables']}")
    print(f"2. Float-formatted ids        : {len(float_ids)} records")
    print(f"3. Malformed concatenated key : {len(malformed)} records")
    print(f"4. Missing descriptions       : {len(no_desc)} records")
    if transform.get("ran"):
        print("-" * 64)
        print(f"TRANSFORM: {'OK' if transform.get('ok') else 'FAILED'}  "
              f"datasets={transform.get('datasets')}  "
              f"empty_property_values={transform.get('empty_property_values')}  "
              f"unmapped_license_codes={transform.get('unmapped_license_codes') or 'none'}")

    # ---- write artifacts ----
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w") as f:
            f.write("record_index\tcontrol_group_id\ttable_name\tissues\n")
            for i, r in enumerate(recs):
                iss = []
                if norm_id(r.get(ID)) in dup_ids: iss.append("duplicate_id")
                if is_float_formatted(r.get(ID)): iss.append("float_id")
                if malformed_keys(r): iss.append("malformed_date_key")
                if missing_desc(r): iss.append("missing_description")
                if iss: f.write(f"{i}\t{r.get(ID)}\t{r.get(TBL)}\t{';'.join(iss)}\n")
        rdir = a.out.parent
        if not a.no_report:
            (rdir / "qc_summary.json").write_text(json.dumps(report, indent=2))
            (rdir / "qc_summary.md").write_text(render_md(report))
            print(f"\nStored: {a.out.name}, qc_summary.md, qc_summary.json  ->  {rdir}")
        else:
            print(f"\nStored: {a.out.name}  ->  {rdir}")

def render_md(r):
    c = r["checks"]; dup = c["duplicate_control_group_id"]; t = r["transform"]
    L = [f"# QC report — {r['input_file']} ({r['record_count']} records)", "",
         f"- generated: {r['generated_at']}",
         f"- mapping: `{r['mapping_file']}`",
         f"- git commit: `{r['git_commit']}`  |  python: {r['python']}", "",
         "## Migration-issue checks", "",
         "| Check | Records |", "|---|---|",
         f"| Duplicate control_group/id | {dup['records']} across {dup['ids']} ids |",
         f"| Float-formatted ids | {c['float_formatted_ids']['records']} |",
         f"| Malformed concatenated key | {c['malformed_concatenated_key']['records']} |",
         f"| Missing descriptions | {c['missing_descriptions']['records']} |", ""]
    if dup["true_duplicate_submissions"]:
        L += ["### True duplicate submissions (same table_name)", ""]
        for k, v in sorted(dup["true_duplicate_submissions"].items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            L.append(f"- id `{k}` ×{v['count']} — {v['tables'][0]}")
        L.append("")
    if dup["id_collisions"]:
        L += ["### ID collisions (one id, different datasets)", ""]
        for k, v in sorted(dup["id_collisions"].items()):
            L.append(f"- id `{k}` ×{v['count']} — {', '.join(v['tables'])}")
        L.append("")
    if t.get("ran"):
        L += ["## Transform", "",
              f"- status: {'OK' if t.get('ok') else 'FAILED'}",
              f"- datasets: {t.get('datasets')}",
              f"- empty PropertyValues: {t.get('empty_property_values')}",
              f"- unmapped license codes: {t.get('unmapped_license_codes') or 'none'}", ""]
    return "\n".join(L)

if __name__ == "__main__":
    main()
