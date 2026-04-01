## Summary
This PR provides draft JSON-LD templates for:
- the Tanzania 1984 Copernicus temperature dataset, and
- the PM2.5 dataset (1998–2016),

and prepares them for review as candidate reusable metadata templates.

## Main changes
- cleaned up the Dataset-level structure
- refined `variableMeasured` to focus more clearly on the variable itself
- moved spatial and grid-related metadata to `spatialCoverage` to improve conceptual clarity and template reusability across raster, sensor, and tabular datasets
- structured `license`, `identifier`, `provider`, and `distribution` more consistently
- aligned the templates more closely with Science-on-Schema.org guidance
- improved QUDT usage ???

## Review requested on
- whether `variableMeasured` is now appropriately scoped, or whether some elements should still be linked to `geocr` (GeoCroissant) attributes
- whether `spatialCoverage` and `distribution` are modeled clearly and at the correct metadata level
- whether any important information from the earlier version has been lost
- whether this structure is suitable as a reusable template for raster, tabular, and future sensor datasets

## Notes
The goal of these revisions is not only to improve the current Copernicus and PM2.5 records, but also to move toward a standardized and reusable JSON-LD template that can be applied consistently across multiple dataset modalities.
