# KoboToolbox Scripts

Python scripts for the **KoboToolbox → SSSOM → JSON-LD** workflow.

One reusable SSSOM mapping is authored for the form, then applied to every
record — you do **not** write a mapping per record.

---

## Setup (do this once)

From the repository root:

```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: py -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r authoring/kobotoolbox/requirements.txt
```

Then work from this folder — **every command below assumes you are here**:

```bash
cd authoring/kobotoolbox/mappings/scripts
```

The reviewed mapping the commands use is `../sssom/kobo_form.sssom.tsv`. If your
current mapping has another name (e.g. `kobo_form.regenerated_128.sssom.tsv`),
either rename it to `kobo_form.sssom.tsv` or substitute its name in every
`--sssom` argument below. Keep **one** canonical mapping file.

---

## Quickstart — pick your path

**Path A — Reproduce the committed outputs (no Kobo token needed).**
Everything is already in the repo; this just re-runs the deterministic transform
+ QC on the committed records:

```bash
./run_pipeline.sh
```

**Path B — Run on fresh data from Kobo (needs a token).**
Pull first, then run the pipeline:

```bash
unset KOBO_API_TOKEN
python3 pull_all_kobo_records.py --form-name GDSC   # paste token when prompted
./run_pipeline.sh
```

`run_pipeline.sh` runs steps 3 → 4 below and writes all outputs. To run the
steps by hand instead, follow them in order.

---

## The flow

```text
1. Pull ALL Kobo records       -> pull_all_kobo_records.py         (needs token; Path B only)
2. Author/update SSSOM mapping  -> AI prompt + human review
3. Transform to JSON-LD         -> sssom_to_jsonld.py    (combined @graph)
                                   split_records_to_jsonld.py (one file per record)
4. Quality-check + store report -> qc_report.py
—  Inspect the mapping (optional)-> vanilla_sssom.py
—  Run 3+4 in one command        -> run_pipeline.sh
```

| Step | Script | Output |
| ---- | ------ | ------ |
| 1 | `pull_all_kobo_records.py` | `records/raw/all_records_raw.json` (+ `sample_records_raw.json`, `field_inventory.md`, `all_records_keys.txt`) |
| 2 | AI prompt + manual review | `sssom/kobo_form.sssom.tsv` |
| 3a | `sssom_to_jsonld.py` | `records/outputs/all_records.jsonld` (one `@graph`) |
| 3b | `split_records_to_jsonld.py` | `records/outputs/per_record/record_<id>_<table>.jsonld` |
| 4 | `qc_report.py` | `records/validation/qc_issues.tsv`, `qc_summary.md`, `qc_summary.json` |
| — | `vanilla_sssom.py` | mapping summary (does not read records) |
| — | `run_pipeline.sh` | runs 3a + 3b + 4 |

---

## Step 1 — Pull all Kobo records (Path B only)

```bash
unset KOBO_API_TOKEN
python3 pull_all_kobo_records.py --form-name GDSC
```
**Expected:** a `Paste Kobo API token:` prompt, then a count of records written.
Writes into `records/raw/`:

```text
all_records_raw.json      # every record, wrapped {"datasets":[ ... ]}  -> transformer input
sample_records_raw.json   # a few records per dataset type              -> for the prompt
field_inventory.md        # union of all fields                         -> for the prompt
all_records_keys.txt      # flat list of every field key
```

`--form-name` matches the project name **exactly** (case-insensitive), so `GDSC`
will not match `GDSC_TESTING`/`GDSC_Authoring`. More robust: `--asset-uid <uid>`
(copy the `aXXXX…` id from the project URL). Non-default server:
`--server-url <url>`. Spot-check one record: `python3 pull_single_kobo_record.py
--record-id 217`.

---

## Step 2 — Author or update the mapping

Attach **`field_inventory.md`** and **`sample_records_raw.json`** to the prompt at
`../prompts/kobo_reusable_sssom_generation_prompt.md`. AI output **must be
human-reviewed** before use, then saved as `../sssom/kobo_form.sssom.tsv`.
Skip this step entirely if you are reusing the committed mapping.

---

## Step 3 — Transform to JSON-LD

Run **3a or 3b** (not both in sequence — they read the same raw file).

**3a — one combined file (all datasets in a single `@graph`):**

```bash
python3 sssom_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --output ../../records/outputs/all_records.jsonld
```
**Expected:** `N mapping row(s) loaded` → `N dataset record(s) mapped` → `Output written…`

**3b — one file per record (this is what catalogue ingestion uses):**

```bash
python3 split_records_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --outdir ../../records/outputs/per_record
```
**Expected:** `Done: N written, 0 failed`, plus a NOTE if any `control_group/id`
is duplicated (those files share an `@id` and collide in a catalogue — fix at
source, then regenerate). Step 4 lists and classifies duplicates.

---

## Step 4 — Quality checks + stored validation

```bash
python3 qc_report.py \
  --input ../../records/raw/all_records_raw.json \
  --sssom ../sssom/kobo_form.sssom.tsv \
  --out   ../../records/validation/qc_issues.tsv
```
`--input` is the **records `.json`**; `--sssom` is the **mapping `.sssom.tsv`**.
Swapping them is the most common error.

Checks: duplicate `control_group/id` (classified as *true duplicate submission* vs
*id collision*), float-formatted ids (`116.0`), malformed concatenated key,
missing descriptions, and transform validation (records mapped, empty
PropertyValues, unmapped license codes).

**Writes to `records/validation/`:** `qc_issues.tsv` (per-record table),
`qc_summary.md` (readable report), `qc_summary.json` (machine-readable +
provenance: git commit, python, mapping). Add `--no-report` for the TSV only.

---

## Optional — inspect the mapping

```bash
python3 vanilla_sssom.py --sssom ../sssom/kobo_form.sssom.tsv --validate
```
Prints an alignment summary (not JSON-LD); prints to the terminal unless you add
`--output <path>`. `--validate` needs `pip install sssom` for the deep check.

---

