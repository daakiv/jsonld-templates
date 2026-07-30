# Forms

KoboToolbox / XLSForm authoring templates for the Gaia metadata authoring form.

| Path | Purpose |
| ---- | ------- |
| `kobo/gaia_metadata_authoring_form_v3.xlsx` | **Current live form** Adds structured contact/contributor fields (split names, affiliation and person identifiers with schema + URI, `contributor_type`, `size_human_readable`). |
| `kobo/gaia_metadata_authoring_form_v2.xlsx` | Previous version, retained for reference. |
|  `kobo/gaia_metadata_authoring_form_v1.xlsx` | 1st  version, retained for reference. |

The form defines the fields captured at authoring time. Its structure is the
schema the SSSOM mapping is built against — when the form changes, the field
inventory and mapping are updated to match.

> **Versioning:** the live form is edited in KoboToolbox and downloaded here as a
> new version (v2 → v3) rather than overwritten in place, so the form's evolution
> stays visible and each SSSOM mapping can be traced to the form version it was
> built against.
