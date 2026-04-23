# KoboToolbox Metadata Authoring

This folder documents the transition from the legacy Box spreadsheet-based metadata authoring workflow to a structured KoboToolbox/XLSForm workflow for Gaia Catalog ingestion.

## Purpose
The KoboToolbox form serves as the standardized metadata authoring interface for geospatial datasets intended for Gaia Catalog ingestion and downstream machine-readable metadata generation.

## Why this change
The previous workflow relied on a manually maintained spreadsheet. The new workflow improves:
- consistency of metadata capture
- validation during entry
- reuse of controlled vocabularies
- scalability across datasets and contributors
- compatibility with downstream JSON-LD / Schema.org generation

## Main assets
- `gaia_metadata_authoring_form.xlsx` — Kobo/XLSForm template
- `field_mapping.md` — mapping from legacy spreadsheet fields to XLSForm structure
- `docs/workflow.md` — authoring and ingestion process
- `docs/api_notes.md` — Kobo API notes and integration details

## Core workflow
1. Author metadata in KoboToolbox using the XLSForm
2. Export submissions from KoboToolbox
3. Transform exported metadata into Gaia-ready structured records
4. Generate machine-readable metadata (e.g., JSON-LD / Schema.org)
5. Ingest into Gaia Catalog

## Configuration
Project identifiers and server information may be documented here, but secrets must not be committed to the repository.
Use a local `.env` file or GitHub Secrets for tokens.
