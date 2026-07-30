# Mappings

Everything that turns raw Kobo metadata into Schema.org / Science-on-Schema.org
JSON-LD lives here.

| Folder | Purpose |
| ------ | ------- |
| `prompts/` | AI prompt templates for authoring and reviewing the SSSOM mapping. |
| `scripts/` | Python scripts to pull records, transform SSSOM → JSON-LD (combined or per-record), and inspect mappings. See its [README](scripts/README.md). |
| `sssom/` | The SSSOM `.tsv` mapping files. `kobo_form.sssom.tsv` is the production, form-level mapping. |

## The idea in one line

Author **one reusable SSSOM mapping for the form**, then run it on every record —
rather than writing a mapping per record.

```text
prompts/  ──►  sssom/kobo_form.sssom.tsv  ──►  scripts/  ──►  JSON-LD
(author)          (the reusable mapping)        (apply)      (output)
```
