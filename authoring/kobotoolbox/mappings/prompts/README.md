# SSSOM Prompt Template — README

**File:** `prompts/transform_prompt_template.md`  


---

## What This Is

These prompts support the KoboToolbox → SSSOM → JSON-LD workflow for the GDSC Gaia Catalog.
The main prompt instructs an AI model (Claude Sonnet or Opus) to generate a `.sssom.tsv`
mapping file that the pipeline script `02_sssom_to_jsonld.py` reads to produce Schema.org JSON-LD.

Prompts are **drafting and review aids** — not final authority. Every AI output must be
validated against the Post-Generation Checklist before saving.

---

## AI Model Used

The SSSOM prompt templates in this folder were developed and tested primarily using
**Anthropic Claude Opus 4.8** through a paid Claude account.

- **Provider:** Anthropic
- **Model:** Claude Opus 4.8
- **Access type:** Closed / hosted model
- **Role in the workflow:** AI-assisted generation and refinement of draft SSSOM mappings
- **Human review:** Required before a generated mapping is accepted for use

The AI model is used only to assist with drafting and reviewing semantic mappings.
Once a reusable SSSOM mapping has been reviewed and approved, the downstream
SSSOM-to-JSON-LD transformation runs deterministically in Python and does not require
the AI model.

Because model outputs may vary across runs or model versions, the prompt templates
and reviewed SSSOM mappings are version-controlled in GitHub and should be treated
as the reproducible project artifacts.

---

## Quick-Start

```
1. Open  prompts/transform_prompt_template.md
2. Paste your record_NNN_raw.json into Step 1
3. Paste the prompt into Claude
4. Download the .sssom.tsv output
5. Run the checklist before saving
```

| Scenario | Step 2 | Step 3 |
|---|---|---|
| First record — no prior SSSOM | Write `NONE — generating from scratch` | Option A |
| Adding fields to existing SSSOM | Paste the existing `.sssom.tsv` | Option B |

---

## What the Prompt Produces

| Output section | Contents |
|---|---|
| YAML header block | Curie map, extension definitions, mapping set metadata |
| Column header row | 13 fixed columns in required order |
| Mapping rows | One TSV row per mappable Kobo field |
| UNMAPPED FIELDS table | Every skipped field with reason and suggested action |
| VALIDATION NOTES block | Counts, confidence breakdown, flags for human review |

---

## The 13 Required Columns (in order)

```
subject_id | predicate_id | object_id | mapping_justification | confidence |
subject_label | object_label | subject_category | object_category |
source_jsonpath | target_jsonpath | transform_rule | comment
```

The `comment` column is required on every row. It is never optional.

---

### What Is Already Built Into the Prompt

The prompt (`transform_prompt_template.md`) contains two quality-control mechanisms
that run as part of every generation. You do not need separate files for these.

#### Validation (Step 7 — Validation Notes)

After generating all mapping rows, the AI produces a `## VALIDATION NOTES` block that:

- counts total Kobo fields found, rows mapped, and fields not mapped
- breaks down mappings by confidence level (exactMatch / closeMatch / relatedMatch)
- lists any new transform rules introduced that are not in the known rules table
- flags every field where human review is required
- reports whether `kobo:temporalCoverage` is present or absent and why
- reports whether `iso_group/extent` needs CRS reprojection before pipeline use

This is the primary mechanism for comparing the AI output against what the record
actually contains and catching structural gaps before running `02_sssom_to_jsonld.py`.

#### Hallucination guard (built into Your Role + Step 4)

The prompt contains 10 non-negotiable hallucination guard rules enforced at generation time:

1. Only JSONPaths verified against the raw JSON are allowed
2. Only Schema.org properties documented at schema.org are allowed
3. ROR identifiers must come from the raw JSON — all others flagged
4. GeoNames IDs must come from `coverage_identifier` in the raw JSON only
5. Fields with value `"TBD"` or `"--"` go to the UNMAPPED table — never a mapping row
6. Uncertain predicates must use `skos:relatedMatch` at confidence ≤ 0.75 with explanation
7. The `comment` column is required on every row
8. Transform rule parameters are required wherever the rules table marks them Required
9. Every `source_jsonpath` must start with `$.datasets[*]`
10. Array groups map as one row per group — sub-field detail goes in the comment

These rules are stated at the top of the prompt (Your Role section) and repeated in the
`## Hallucination guard` section at the end of the prompt so the AI sees them twice.

---

