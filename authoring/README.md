# Authoring

Metadata **authoring** workflows for the [Gaia Catalog](https://github.com/OHDSI/gaiaCatalog)
and OHDSI GIS metadata pipeline — how structured metadata is captured and turned
into machine-readable, FAIR-aligned JSON-LD.

This directory contains both the current KoboToolbox-based workflow and the
legacy spreadsheet-based authoring approach retained for reference and transition support.

| Folder | Purpose |
| ------ | ------- |
| [`kobotoolbox/`](kobotoolbox/) | Current KoboToolbox / XLSForm authoring workflow: capture metadata in Kobo, map it with a reusable SSSOM crosswalk, and transform it into Schema.org / Science-on-Schema.org JSON-LD. |
| [`legacy-box-spreadsheet/`](legacy-box-spreadsheet/) | Earlier spreadsheet-based authoring workflow retained for reference and transition support. |

## Current workflow

For the active implementation, start with:

- [`kobotoolbox/README.md`](kobotoolbox/README.md) — workflow overview
- [`kobotoolbox/REPRODUCIBILITY.md`](kobotoolbox/REPRODUCIBILITY.md) — local setup and replication
- [`kobotoolbox/requirements.txt`](kobotoolbox/requirements.txt) — Python dependencies

Each subfolder contains its own `README.md` with more detailed setup and usage notes.
