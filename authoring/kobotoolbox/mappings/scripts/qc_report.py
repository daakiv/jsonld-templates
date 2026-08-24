#!/usr/bin/env python3
"""Data-quality + transform validation for the Kobo -> SSSOM -> JSON-LD pipeline.
Reproduces the checks from David's prior QC report and confirms whether the
BOX->Kobo migration issues Tim resolved are gone.

Usage:
  python3 qc_report.py --input all_records_raw.json --sssom kobo_form.sssom.tsv
"""
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

def is_float_formatted(v):
    if isinstance(v, float):
        return True
    s = str(v).strip()
    return bool(re.fullmatch(r'-?\d+\.\d+', s))  # e.g. 116.0

def norm_id(v):
    s = str(v).strip()
    if is_float_formatted(v):
        try: return str(int(float(s)))
        except ValueError: return s
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--sssom", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None, help="write per-record issue table (TSV)")
    a = ap.parse_args()

    d = json.load(open(a.input))
    recs = d["datasets"] if isinstance(d, dict) and "datasets" in d else d
    n = len(recs)

    ID = "control_group/id"
    DESC = "dublin_core_group/description"

    # --- Check 1: duplicate control_group/id (normalised so 116 and 116.0 collide) ---
    id_norm = [norm_id(r.get(ID)) for r in recs]
    counts = Counter(id_norm)
    dup_ids = {k: c for k, c in counts.items() if c > 1 and k not in ("None", "")}
    dup_records = [(i, r.get(ID), norm_id(r.get(ID))) for i, r in enumerate(recs)
                   if norm_id(r.get(ID)) in dup_ids]

    # --- Check 2: float-formatted identifiers (116.0 instead of 116) ---
    float_ids = [(i, r.get(ID)) for i, r in enumerate(recs) if is_float_formatted(r.get(ID))]

    # --- Check 3: malformed concatenated date key (two field names fused) ---
    def malformed_keys(r):
        bad = []
        for k in r.keys():
            if "/__/" in k or "__" in k.replace("__version__", ""):
                bad.append(k)
            elif k.count("time_period_start") and k.count("time_period_end"):
                bad.append(k)
        return bad
    malformed = [(i, r.get(ID), malformed_keys(r)) for i, r in enumerate(recs) if malformed_keys(r)]

    # --- Check 4: missing descriptions ---
    def missing_desc(r):
        v = r.get(DESC)
        return v is None or str(v).strip() in ("", "--", "TBD", "tbd", "n/a", "N/A")
    no_desc = [(i, r.get(ID), r.get("etl_group/table_name")) for i, r in enumerate(recs) if missing_desc(r)]

    print("=" * 64)
    print(f"DATA-QUALITY REPORT  —  {n} records  ({a.input.name})")
    print("=" * 64)
    print(f"1. Duplicate control_group/id : {len(dup_ids)} id(s) across {len(dup_records)} records")
    for k, c in sorted(dup_ids.items()):
        print(f"     id {k!r} x{c}")
    print(f"2. Float-formatted ids        : {len(float_ids)} records (e.g. 116.0)")
    for i, v in float_ids[:10]:
        print(f"     record[{i}] id={v!r}")
    if len(float_ids) > 10: print(f"     ... (+{len(float_ids)-10} more)")
    print(f"3. Malformed concatenated key : {len(malformed)} records")
    for i, rid, ks in malformed:
        print(f"     record[{i}] id={rid!r}: {ks}")
    print(f"4. Missing descriptions       : {len(no_desc)} records")
    for i, rid, tbl in no_desc:
        print(f"     record[{i}] id={rid!r} table={tbl!r}")

    # --- optional: per-record issue table ---
    if a.out:
        with open(a.out, "w") as f:
            f.write("record_index\tcontrol_group_id\ttable_name\tissues\n")
            for i, r in enumerate(recs):
                iss = []
                if norm_id(r.get(ID)) in dup_ids: iss.append("duplicate_id")
                if is_float_formatted(r.get(ID)): iss.append("float_id")
                if malformed_keys(r): iss.append("malformed_date_key")
                if missing_desc(r): iss.append("missing_description")
                if iss:
                    f.write(f"{i}\t{r.get(ID)}\t{r.get('etl_group/table_name')}\t{';'.join(iss)}\n")
        print(f"\nPer-record issue table -> {a.out}")

    # --- transform validation (only if sssom given and transformer importable) ---
    print("-" * 64)
    if a.sssom:
        import subprocess, tempfile, os
        script_dir = Path(__file__).resolve().parent
        tj = script_dir / "sssom_to_jsonld.py"
        if not tj.exists():
            print("TRANSFORM: sssom_to_jsonld.py not next to this script — skipping run.")
        else:
            outp = Path(tempfile.mkdtemp()) / "all.jsonld"
            res = subprocess.run([sys.executable, str(tj), "--sssom", str(a.sssom),
                                  "--input", str(a.input), "--output", str(outp)],
                                 capture_output=True, text=True)
            tail = (res.stdout + res.stderr).strip().splitlines()[-3:]
            print("TRANSFORM:", "OK" if res.returncode == 0 else "FAILED")
            for l in tail: print("   ", l)
            if outp.exists():
                g = json.load(open(outp)).get("@graph", [])
                # empty PropertyValues + unmapped license codes
                def empties(o):
                    c = 0
                    if isinstance(o, dict):
                        if o.get("@type") == "PropertyValue" and not o.get("name") and not str(o.get("value","")).strip(): c += 1
                        for v in o.values(): c += empties(v)
                    elif isinstance(o, list):
                        for v in o: c += empties(v)
                    return c
                unmapped_lic = Counter()
                for obj in g:
                    lic = obj.get("license")
                    if isinstance(lic, str) and not lic.startswith("http"):
                        unmapped_lic[lic] += 1
                print(f"   datasets in @graph: {len(g)}")
                print(f"   empty PropertyValues: {sum(empties(o) for o in g)}")
                print(f"   unmapped license codes: {dict(unmapped_lic) or 'none'}")
    else:
        print("TRANSFORM: skipped (no --sssom given)")

if __name__ == "__main__":
    main()
