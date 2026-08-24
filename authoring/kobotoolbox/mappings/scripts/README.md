# KoboToolbox Scripts

Python scripts for the **KoboToolbox → SSSOM → JSON-LD** workflow.

The pipeline authors one reusable SSSOM mapping for the form, then applies it to
every record — you do not write a mapping per record.

```text
1. Pull ALL Kobo records            -> pull_all_kobo_records.py
2. Author / update the SSSOM mapping -> AI prompt + human review
3. Transform records to JSON-LD      -> sssom_to_jsonld.py   (combined @graph)
                                        split_records_to_jsonld.py (one file per record)
4. (optional) Inspect the mapping    -> vanilla_sssom.py
```

Run all commands from this folder:

```bash
cd authoring/kobotoolbox/mappings/scripts
```

---

## Script flow

| Step | Script | Purpose | Main output |
| ---- | ------ | ------- | ----------- |
| 1 | `pull_all_kobo_records.py` | Pull **all** submissions for the form; emit the wrapped record file, a prompt-sized sample, and a field inventory. | `records/raw/all_records_raw.json` (+ `sample_records_raw.json`, `field_inventory.md`) |
| 2 | AI prompt + manual review | Author or update the reusable SSSOM crosswalk (Kobo JSON → Schema.org JSON-LD). | `sssom/kobo_form.sssom.tsv` |
| 3a | `sssom_to_jsonld.py` | Transform records into a **single combined** JSON-LD (`@graph`). | `records/outputs/all_records.jsonld` |
| 3b | `split_records_to_jsonld.py` | Transform into **one JSON-LD file per record**. | `records/outputs/per_record/record_<id>_<table>.jsonld` |
| — | `vanilla_sssom.py` | Optional: inspect/validate the mapping's structure (does not read records or produce JSON-LD). | summary / turtle / validation report |

> A previous version of this repo pulled one record at a time
> (`01_pull_kobo_raw_json_records.py`, still present for reference). The current
> flow pulls the whole form in one call with `pull_all_kobo_records.py`.

---

## Step 1 — Pull all Kobo records

```bash
unset KOBO_API_TOKEN
python3 pull_all_kobo_records.py --form-name gaia_metadata_authoring_form_v2
```
You should then see:
```bash
Paste Kobo API token:
```
Writes into `records/raw/`:

```text
all_records_raw.json      # every record, wrapped as {"datasets": [ ... ]}  -> for the transformer
sample_records_raw.json   # a few records per dataset type                 -> for the prompt
field_inventory.md        # union of all fields (+ repeat groups, vector/raster) -> for the prompt
all_records_keys.txt      # flat list of every field key
```

Useful flags: `--asset-uid <uid>` (skip the form-name lookup),
`--record-id <id>` (also write a single `record_<id>_raw.json`),
`--out-dir <path>` (override the output location).

To pull just one record by ID (spot-checks / debugging):

```bash
python3 pull_single_kobo_record.py --record-id 217
```

---

## Step 2 — Author or update the SSSOM mapping

The SSSOM TSV defines, per row: source JSONPath (Kobo), target JSON-LD path,
mapping predicate, confidence, transform rule, and a comment.

Attach **`field_inventory.md`** and **`sample_records_raw.json`** to the
generation prompt:

```text
../prompts/kobo_reusable_sssom_generation_prompt.md
```

AI-generated mappings **must be reviewed by a human** before use. The production
mapping lives at:

```text
../sssom/kobo_form.sssom.tsv
```

---

## Step 3a — Transform to a single combined JSON-LD

```bash
python3 sssom_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --output ../../records/outputs/all_records.jsonld
```

Produces one file with all records in a single `@graph`.

> **Do NOT add `--wrap-key datasets` here.** `all_records_raw.json` is already
> `{"datasets": [ ... ]}`. Adding the flag wraps it a second time into
> `{"datasets": [{"datasets": [ ... ]}]}`, so `$.datasets[*]` matches only the
> inner object and **just one record is produced**. `--wrap-key datasets` is
> only for a single *bare* record (one unwrapped object) — see below.

---

## Step 3b — Transform to one file per record

This is the desired output for catalogue ingestion (one JSON-LD per dataset).

```bash
python3 split_records_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --outdir ../../records/outputs/per_record
```

Writes `record_<id>_<table_name>.jsonld` — one per record — into `per_record/`.

**How it works:** the splitter reads `all_records_raw.json`, separates it into
single records, and calls `sssom_to_jsonld.py` once per record. Each single
record *is* a bare object, so the splitter applies `--wrap-key datasets`
internally. The core transformer is unchanged — the splitter simply orchestrates
it. You run **either** 3a **or** 3b; they both read the same raw file and are not
a sequence.

**Duplicate records:** if the pull contains duplicate `control_group/id` values,
the splitter still writes every file, suffixing collisions `__2` / `__3`. Those
files share the same `@id`, so they would collide in a catalogue keyed on `@id`.
De-duplicate at the source, then regenerate.

---

## `--wrap-key` in one line

| Input | Command |
| ----- | ------- |
| `all_records_raw.json` (already `{"datasets": [...]}`) | **omit** `--wrap-key` |
| a single bare record (one unwrapped object) | add `--wrap-key datasets` |

---

## Optional — Inspect the mapping (`vanilla_sssom.py`)

A mapping **inspector**, not part of JSON-LD production. It parses the SSSOM,
prints a summary, can export the alignments (json / tsv / turtle), and can
validate with `sssom-py`. Useful as a pre-flight check that the mapping is
well-formed before a big run.

```bash
python3 vanilla_sssom.py --sssom ../sssom/kobo_form.sssom.tsv --validate
```

---

## Conventions

- Don't edit scripts to change records — use the CLI flags.
- Raw Kobo files → `records/raw/`
- Generated JSON-LD → `records/outputs/` (combined) and `records/outputs/per_record/` (per record)
- Mapping files → `sssom/`
- Validation / comparison outputs → `records/validation/`
