## Summary
This PR provides draft JSON-LD template  for the Tanzania 1984 Copernicus temperature dataset and PM2.5 from 1998 to 2016 and prepares it for review.

## Main changes
- cleaned up the Dataset-level structure
- refined `variableMeasured` to focus on the variable itself
- moved spatial/grid metadata to `spatialCoverage` for better template reusability across sensor and tabular datasets.
- structured `license`, `identifier`, `provider`, and `distribution`
- aligned the template more closely with Science-on-Schema.org guidance
- QUDT Optimization 

## Review requested on
- whether `variableMeasured` is now appropriately scoped or should we intergrate with `geocr `(GeoCroissant) attributes
- whether `spatialCoverage` and `distribution` are modeled clearly 
- whether any important information from the original version has been lost
- whether this structure is suitable as a reusable template for raster, tabular, and future sensor datasets


