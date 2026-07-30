# JSON-LD outputs

Generated Schema.org / Science-on-Schema.org JSON-LD. Produced by the scripts in
`mappings/scripts/` from `records/raw/all_records_raw.json` and the mapping
`mappings/sssom/kobo_form.sssom.tsv`.

## Two forms of output

| Path | What it is | Produced by |
| ---- | ---------- | ----------- |
| `all_records.jsonld` | All records in a single `@graph`. | `sssom_to_jsonld.py` |
| `per_record/` | One JSON-LD file per dataset (`record_<id>_<table>.jsonld`). | `split_records_to_jsonld.py` |

**One file per dataset is the desired output for catalogue ingestion.** The
combined `@graph` can be produced when a single-file view is wanted.

## Duplicate records

The current pull contains duplicate `control_group/id` values. In `per_record/`
these appear with `__2` / `__3` suffixes and **share the same `@id`**, so they
would collide in a catalogue keyed on `@id`. See the
[data-quality report](../../docs/quality_issues/Kobo_Data_Quality_Issues.xlsx).
De-duplicate at the source, then regenerate.

## Regenerating

From `mappings/scripts/`:

```bash
# per-record (desired)
python3 split_records_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --outdir ../../records/outputs/per_record

# combined @graph (note: NO --wrap-key on the already-wrapped all-records file)
python3 sssom_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --output ../../records/outputs/all_records.jsonld
```
