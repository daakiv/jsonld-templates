#!/usr/bin/env bash
# End-to-end: transform -> split -> QC, from a committed raw file + reviewed mapping.
# The Kobo pull is intentionally NOT here (it needs a token + network and is the
# optional, non-reproducible step). Run pull_all_kobo_records.py separately first
# if you need fresh data.
#
# Usage (from mappings/scripts/):
#   ./run_pipeline.sh [MAPPING_TSV] [RAW_JSON]
# Defaults shown below.
set -euo pipefail

MAPPING="${1:-../sssom/kobo_form.sssom.tsv}"
RAW="${2:-../../records/raw/all_records_raw.json}"
OUT_DIR="../../records/outputs"
VAL_DIR="../../records/validation"

echo ">> mapping : $MAPPING"
echo ">> input   : $RAW"
[ -f "$MAPPING" ] || { echo "ERROR: mapping not found: $MAPPING"; exit 1; }
[ -f "$RAW" ]     || { echo "ERROR: raw input not found: $RAW"; exit 1; }

echo ">> [1/3] combined JSON-LD"
python3 sssom_to_jsonld.py --sssom "$MAPPING" --input "$RAW" --output "$OUT_DIR/all_records.jsonld"

echo ">> [2/3] per-record JSON-LD"
python3 split_records_to_jsonld.py --sssom "$MAPPING" --input "$RAW" --outdir "$OUT_DIR/per_record"

echo ">> [3/3] QC + stored validation report"
python3 qc_report.py --input "$RAW" --sssom "$MAPPING" --out "$VAL_DIR/qc_issues.tsv"

echo ">> done. outputs -> $OUT_DIR   validation -> $VAL_DIR"
