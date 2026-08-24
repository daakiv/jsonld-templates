# KoboToolbox Metadata Authoring

This folder documents the KoboToolbox/XLSForm-based metadata authoring workflow being developed for the [Gaia Catalog](https://github.com/OHDSI/gaiaCatalog) and OHDSI GIS metadata pipeline.

The workflow supports the transition from a legacy spreadsheet-based metadata process into a more structured, reusable, and machine-actionable authoring approach. It uses:

- **KoboToolbox** for structured metadata capture and interface management.
- **Raw Kobo JSON exports** as the source records.
- **SSSOM-style mapping files** ([Simple Standard for Sharing Ontological Mappings](https://w3id.org/sssom)) for explicit semantic translation rules.
- **JSON-LD outputs** strictly aligned with [Schema.org](https://schema.org) and [Science-on-Schema.org (SOSO)](https://github.com/ESIPFed/science-on-schema.org/blob/main/guides/Dataset.md#roles-of-people) recommendations.

---

---

## Purpose

The KoboToolbox form serves as a structured metadata authoring interface for geospatial datasets intended for Gaia Catalog ingestion and downstream machine-readable metadata generation.

The goal is to support consistent metadata capture across geospatial use cases — including vector, raster, tabular, and sensor-based datasets — while reducing manual transformation work and improving the reproducibility of metadata outputs.

---

## Why this approach

The previous workflow relied on manually maintained spreadsheet templates. The KoboToolbox-based workflow improves:

| Aspect                      | Benefit                                                                                                                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Consistency**             | Structured form fields reduce free-text variation and improve metadata consistency.                                    |
| **Validation**              | Entry-time checks help catch missing values, type errors, and required-field issues before export.                     |
| **Controlled vocabularies** | Dropdown and select responses support the use of standardized terms and reduce ambiguity.                              |
| **Scalability**             | The workflow supports metadata authoring by multiple contributors across different datasets and use cases.             |
| **Interoperability**        | Raw Kobo metadata can be transformed into JSON-LD aligned with Schema.org and Science-on-Schema.org (`soso`) patterns. |
| **Traceability**            | The workflow provides a clear chain from raw Kobo record → SSSOM mapping → generated JSON-LD output.                   |


---

## Current workflow

```
KoboToolbox XLSForm
        ↓
Kobo metadata submission
        ↓
Raw Kobo JSON export
        ↓
AI-assisted and manually reviewed SSSOM mapping
        ↓
SSSOM-to-JSON-LD transformation
        ↓
Schema.org / Science-on-Schema.org JSON-LD output
   (combined @graph, or one file per dataset)
        ↓
Gaia Catalog review and ingestion
```

---

## Main assets

> [!NOTE]
> Each major subfolder contains its own documentation or supporting files with
> more detailed technical notes, conventions, and usage instructions.

| Folder / file | Purpose |
| --- | --- |
| [`docs/`](docs/) | Workflow notes, architecture documentation, concept notes, and the [data-quality report](docs/quality_issues/Kobo_Data_Quality_Issues.xlsx) for earlier validation work. |
| [`forms/`](forms/) | KoboToolbox/XLSForm authoring templates and related form assets. |
| [`mappings/prompts/`](mappings/prompts/) | AI prompt templates used to support reusable SSSOM mapping generation, validation, human review, and AI model provenance documentation. See the [prompts README](mappings/prompts/README.md). |
| [`mappings/scripts/`](mappings/scripts/) | Python scripts for pulling Kobo records, inspecting and validating source records, transforming SSSOM mappings into JSON-LD, splitting outputs, and checking mapping quality. See the [scripts README](mappings/scripts/README.md). |
| [`mappings/sssom/`](mappings/sssom/) | Version-controlled SSSOM-style TSV mapping files defining how Kobo JSON paths map to Schema.org / JSON-LD properties. |
| [`records/raw/`](records/raw/) | Raw Kobo JSON records, field inventories, samples, and extracted source keys generated from Kobo pulls. |
| [`records/outputs/`](records/outputs/) | Generated Schema.org / Science-on-Schema.org JSON-LD outputs, including combined and per-record representations. |
| [`records/validation/`](records/validation/) | Quality-control and validation outputs generated from source records and SSSOM mappings, including issue-level QC reports. See the [validation README](records/validation/README.md). |
| [`.env.example`](.env.example) | Documents expected environment variables without exposing secrets. The current Python scripts do not automatically load this file. |
| [`requirements.txt`](requirements.txt) | Python dependencies required to reproduce and run the KoboToolbox → SSSOM → JSON-LD pipeline. |
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Step-by-step instructions for setting up a local environment and reproducing the committed workflow. |
| [`README.md`](README.md) | This KoboToolbox metadata-authoring workflow overview. |                                                                                  |


> For Science-on-Schema.org guidance on dataset roles, see the [official Dataset guide](https://github.com/ESIPFed/science-on-schema.org/blob/main/guides/Dataset.md#roles-of-people).
