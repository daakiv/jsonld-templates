# SSSOM Mappings

SSSOM-style TSV files that define how Kobo JSON fields map to Schema.org /
Science-on-Schema.org JSON-LD. Each row records a source JSONPath, a target
JSON-LD path, a mapping predicate, a confidence score, a transform rule, and a
comment.

## Production mapping

| File | Purpose |
| ---- | ------- |
| `kobo_form.sssom.tsv` | **The current, form-level reusable mapping.** Covers every field in the form and is applied to all records. This is the one the scripts use. |

## Earlier / reference mappings

Kept for provenance and comparison. Not used in the current workflow.

| File | Purpose |
| ---- | ------- |
| `kobo_testing_merged.sssom.tsv` | An earlier merged mapping used while consolidating rules; superseded by `kobo_form.sssom.tsv`. |
| `gaia_metadata_authoring_form_v2_to_schemaorg.sssom.tsv` | Early full-form mapping draft. |
| `gaia_record026_mdc_fire_stations.sssom.tsv` | Per-record mapping (record 26), from before the single reusable file. |
| `gaia_record217_tanzania_temp.sssom.tsv` | Per-record mapping (record 217), from before the single reusable file. |

> The per-record `gaia_record0XX_*` files predate the reusable approach — the
> project has since moved to **one mapping for the whole form** (see
> `kobo_form.sssom.tsv`). They are retained for reference.

## Column reference (13 confirmed + 1 proposed)

`subject_id · predicate_id · object_id · mapping_justification · confidence ·
subject_label · object_label · subject_category · object_category ·
source_jsonpath · target_jsonpath · transform_rule · comment`
(proposed extension: `property_decision_rationale`)

Two rules worth remembering:

- **Every field row must use `subject_category = owl:ObjectProperty`.** Rows with
  any other category are silently skipped by the transformer.
- **One row per target path.** Two rows writing to the same target stack into a
  list; pick one canonical source and send the rest to `additionalProperty`.
