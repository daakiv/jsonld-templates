# Reproducing the KoboToolbox -> SSSOM -> JSON-LD Pipeline

This guide applies specifically to the metadata-authoring workflow under
`authoring/kobotoolbox/`.

The repository contains other experimental and research work. The instructions
below reproduce only the KoboToolbox -> SSSOM -> Schema.org / Science-on-Schema.org
JSON-LD workflow.

The pipeline has two distinct parts:

1. **Semantic mapping authoring** — AI-assisted and manually reviewed.
2. **Deterministic transformation** — Python applies the reviewed SSSOM mapping
   to Kobo JSON and produces JSON-LD.

You do **not** need an AI model, an Anthropic account, an API key, or a Kobo
token to reproduce the transformation using the committed data. AI is used only
to assist with authoring or extending the SSSOM mapping.

---

## 1. Prerequisites

- Git
- Python **3.10 or newer**
- Python **3.11+ recommended**
- `pip`
- A shell / terminal

Optional:

- KoboToolbox credentials only if pulling fresh records
- An AI model only if regenerating or extending the SSSOM mapping
- `sssom` / `rdflib` only for optional validation or Turtle export

---

## 2. Clone the repository

```bash
git clone https://github.com/daakiv/ohdsi-gis-metadata-template.git
cd ohdsi-gis-metadata-template/authoring/kobotoolbox
```

---

## 3. Create an isolated Python environment

Using a virtual environment is recommended so the workflow does not depend on
packages already installed elsewhere on the machine.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Confirm the interpreter:

```bash
python --version
```

---

## 4. Install dependencies

From `authoring/kobotoolbox/`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Core runtime dependencies are:

- `jsonpath-ng`
- `PyYAML`
- `ply`

`requests` is needed only when pulling fresh data from KoboToolbox.

Optional validation / export tools:

```bash
python -m pip install sssom rdflib
```

---

## 5. Reproduce the committed transformation

Change to the scripts directory:

```bash
cd mappings/scripts
```

### Option A — One JSON-LD file per dataset

Recommended for catalogue ingestion.

```bash
python3 split_records_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --outdir ../../records/outputs/per_record
```

Expected output:

```text
authoring/kobotoolbox/records/outputs/per_record/
```

### Option B — One combined JSON-LD `@graph`

```bash
python3 sssom_to_jsonld.py \
  --sssom  ../sssom/kobo_form.sssom.tsv \
  --input  ../../records/raw/all_records_raw.json \
  --output ../../records/outputs/all_records.jsonld
```

> **Important:** do **not** add `--wrap-key datasets` when using
> `all_records_raw.json`. That file is already wrapped as:
>
> ```json
> {"datasets": [ ... ]}
> ```
>
> Adding `--wrap-key datasets` would double-wrap the input.

---

## 6. Optional pre-flight mapping check

To inspect the committed SSSOM mapping:

```bash
python3 vanilla_sssom.py \
  --sssom ../sssom/kobo_form.sssom.tsv
```

If the optional `sssom` package is installed:

```bash
python3 vanilla_sssom.py \
  --sssom ../sssom/kobo_form.sssom.tsv \
  --validate
```

This checks the mapping structure. It does not generate JSON-LD.

---

## 7. Optional — Pull fresh KoboToolbox records

This step is **not required** to reproduce the committed transformation.

The Kobo scripts read the API token from the `KOBO_API_TOKEN` environment
variable. If it is not set, the script prompts for the token interactively.

### Option 1 — Environment variable

macOS / Linux:

```bash
export KOBO_API_TOKEN=...
```

Then run:

```bash
python3 pull_all_kobo_records.py \
  --form-name gaia_metadata_authoring_form_v2
```

### Option 2 — Interactive prompt

Run the same command without setting `KOBO_API_TOKEN`. The script will ask for
the token interactively.

The pull writes:

```text
records/raw/all_records_raw.json
records/raw/sample_records_raw.json
records/raw/field_inventory.md
records/raw/field_inventory.json
records/raw/all_records_keys.txt
```

To pull only one record for debugging:

```bash
python3 pull_single_kobo_record.py --record-id 217
```

The existing `.env.example` documents expected environment variables, but the
current Python scripts do **not** automatically load `.env` files.

---

## 8. AI-assisted mapping authoring

AI is **not part of the runtime transformation path**.

If the Kobo form changes and the SSSOM mapping must be regenerated or extended:

1. Use:
   - `records/raw/field_inventory.md`
   - `records/raw/sample_records_raw.json`
2. Follow:
   - `mappings/prompts/kobo_reusable_sssom_generation_prompt.md`
3. Review the generated mapping manually.
4. Save the reviewed mapping as:
   - `mappings/sssom/kobo_form.sssom.tsv`
5. Re-run the deterministic transformation.

The prompts folder README documents the AI model provenance used during prompt
development and testing.

---

## 9. What makes this reproducible

The reproducible artifacts are:

- the **version-controlled SSSOM mapping**
- the **committed raw/test records**
- the **Python transformation scripts**
- the **prompt templates**
- the **documented Python dependencies**
- the **Git commit history**

The reviewed SSSOM mapping — not the AI output from a particular interactive
session — is the artifact of record.

---

## 10. Reproducibility levels

### Level 1 — Reproduce the transformation

Requires only:

- cloned repository
- Python environment
- `requirements.txt`
- committed Kobo JSON records
- reviewed SSSOM mapping

No Kobo credentials and no AI model are required.

### Level 2 — Reproduce the full workflow

Additionally requires:

- KoboToolbox access / API token to pull fresh records
- the documented AI prompt workflow if the SSSOM mapping must be regenerated or extended
- human review of AI-generated mapping changes

---

## 11. Expected workflow

```text
KoboToolbox XLSForm
        ↓
Kobo metadata submission
        ↓
Raw Kobo JSON export
        ↓
AI-assisted + human-reviewed reusable SSSOM mapping
        ↓
Deterministic Python transformation
        ↓
Schema.org / Science-on-Schema.org JSON-LD
        ↓
Gaia Catalog review and ingestion
```

---

