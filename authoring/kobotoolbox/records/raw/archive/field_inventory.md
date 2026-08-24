# Kobo form field inventory

Built from **88 records**. Dataset types: {'vector': 59, 'raster': 28, 'raster_tiles': 1}.

Treat this as the form schema: the union of every field across all records. `exclusive to` marks fields seen only under one dataset type — map those as conditional rows (VECTOR ONLY / RASTER ONLY) so one file serves every record.

> **Caveat:** `exclusive to` is evidence from the records pulled, not a guarantee about the form. A field can look type-exclusive simply because the records of the other type happened to leave it blank (a DOI, for example). Confirm against the form definition before treating a row as conditional.

## Form fields (66)

| field (exact Kobo key) | present | kind | exclusive to | sub-fields | example |
|---|---|---|---|---|---|
| `cartography_group/attributes_group` | 88/88 | repeat_group | — | `attribute_concept_id`, `attribute_description`, `attribute_end_date`, `attribute_external_id`, `attribute_max_value`, `attribute_min_value`, `attribute_name`, `attribute_source`, `attribute_start_date`, `attribute_type`, `attribute_unit`, `attribute_unit_concept_id` | `{"cartography_group/attributes_group/attribute_description": "Code of ` |
| `cartography_group/color_ramp` | 32/88 | scalar | — | — | `"33 127 39 4 255\n  31.20 166 54 3 255\n  29.04 217 72 1 255\n  26.70 ` |
| `cartography_group/label` | 39/88 | scalar | **vector** | — | `"name"` |
| `cartography_group/legend` | 25/88 | scalar | **raster** | — | `"TBD"` |
| `cartography_group/no_data_group` | 9/88 | repeat_group | — | `no_data_type`, `no_data_value` | `{"cartography_group/no_data_group/no_data_type": "int4", "cartography_` |
| `cartography_group/tile_url_group` | 26/88 | repeat_group | — | `tile_base_url` | `{"cartography_group/tile_url_group/tile_base_url": "https://gdsc.idsc.` |
| `cartography_group/tile_zoom_group` | 28/88 | repeat_group | — | `tile_min_zoom` | `{"cartography_group/tile_zoom_group/tile_min_zoom": "14"}` |
| `cartography_group/values_group` | 43/88 | repeat_group | **vector** | `values_group`, `value_field` | `{"cartography_group/values_group/value_field": "area_sqmi"}` |
| `collection_group/analytic_epsg` | 87/88 | scalar | — | — | `"3857"` |
| `collection_group/analytic_function` | 57/88 | scalar | — | — | `"gdsc_get_attributes"` |
| `collection_group/collections` | 88/88 | scalar | — | — | `"mdc-health-outcomes ohdsi-gaia"` |
| `collection_group/derivative_url` | 88/88 | scalar | — | — | `"TBD"` |
| `collection_group/derivatives` | 53/88 | scalar | — | — | `"sql shp"` |
| `collection_group/disclaimer` | 27/88 | scalar | — | — | `"The Database is licensed by the Licensor “as is” and without any warr` |
| `collection_group/rights_statement` | 2/88 | scalar | **raster** | — | `"This data is open to the public and browse images are freely availabl` |
| `collection_group/service_definition` | 53/88 | scalar | — | — | `"API\|arcgis\|query"` |
| `collection_group/sponsor_group` | 72/88 | repeat_group | — | `sponsor_name`, `sponsor_url` | `{"collection_group/sponsor_group/sponsor_name": "TuftsCTSI", "collecti` |
| `collection_group/status` | 46/88 | scalar | — | — | `"draft"` |
| `collection_group/thumbnail` | 5/88 | scalar | — | — | `"published"` |
| `control_group/external_id_group` | 3/88 | repeat_group | **vector** | `external_id_type`, `external_id_value` | `{"control_group/external_id_group/external_id_type": "ohdsi", "control` |
| `control_group/id` | 88/88 | scalar | — | — | `"136"` |
| `dublin_core_group/coverage_group` | 88/88 | repeat_group | — | `coverage_identifier`, `coverage_identifier_schema`, `coverage_identifier_schema_uri`, `coverage_name` | `{"dublin_core_group/coverage_group/coverage_identifier": "6295630", "d` |
| `dublin_core_group/creator_group` | 88/88 | repeat_group | — | `creator_affiliation`, `creator_affiliation_identifier`, `creator_affiliation_schema`, `creator_affiliation_schema_uri`, `creator_first_name`, `creator_identifier`, `creator_identifier_schema`, `creator_identifier_schema_uri`, `creator_last_name`, `creator_name`, `creator_type` | `{"dublin_core_group/creator_group/creator_name": "CIESIN - Center for ` |
| `dublin_core_group/description` | 88/88 | scalar | — | — | `"The Annual PM2.5 Concentrations for Countries and Urban Areas, 1998-2` |
| `dublin_core_group/doi` | 20/88 | scalar | — | — | `"https://doi.org/10.7910/DVN/RHIFKL"` |
| `dublin_core_group/language` | 78/88 | scalar | — | — | `"en"` |
| `dublin_core_group/license` | 18/88 | scalar | — | — | `"odbl"` |
| `dublin_core_group/license_text` | 36/88 | scalar | — | — | `"OpenStreetMap® is open data, licensed under the [Open Data Commons Op` |
| `dublin_core_group/provenance` | 70/88 | scalar | — | — | `"Direct from source"` |
| `dublin_core_group/publication_date` | 78/88 | scalar | — | — | `"2021-04-06"` |
| `dublin_core_group/publisher_group` | 88/88 | repeat_group | — | `publisher_name` | `{"dublin_core_group/publisher_group/publisher_name": "University of Mi` |
| `dublin_core_group/relation_group` | 13/88 | repeat_group | — | `relation_title` | `{"dublin_core_group/relation_group/relation_title": "tl_2018_25_tract"` |
| `dublin_core_group/resource_type` | 88/88 | scalar | — | — | `"vector_dataset"` |
| `dublin_core_group/restrictions` | 25/88 | scalar | — | — | `"You are free to copy, distribute, transmit and adapt our data, as lon` |
| `dublin_core_group/rights` | 88/88 | scalar | — | — | `"public_domain"` |
| `dublin_core_group/subject_group` | 88/88 | repeat_group | — | `subject_term` | `{"dublin_core_group/subject_group/subject_term": "Global"}` |
| `dublin_core_group/time_period_start/__/dublin_core_group/time_period_end` | 3/88 | scalar | — | — | `"1984-01-01\|1984-12-31"` |
| `dublin_core_group/title` | 88/88 | scalar | — | — | `"Annual PM2.5 Concentrations for Countries and Urban Areas, v1 (1998 –` |
| `dublin_core_group/url` | 86/88 | scalar | — | — | `"https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/` |
| `etl_group/checksum` | 88/88 | scalar | — | — | `"TBD"` |
| `etl_group/custom_etl` | 30/88 | scalar | — | — | `"srtm_merge_and_crop"` |
| `etl_group/custom_parameters` | 30/88 | scalar | — | — | `"S10W077.SRTMGL1\|S10W078.SRTMGL1\|S11W077.SRTMGL1\|S11W078.SRTMGL1\|b` |
| `etl_group/dependency_group` | 28/88 | repeat_group | — | `dependency_table_name` | `{"etl_group/dependency_group/dependency_table_name": "fl_2018_svi_trac` |
| `etl_group/download` | 57/88 | scalar | — | — | `"wget"` |
| `etl_group/etl_parameters` | 29/88 | scalar | — | — | `"-k"` |
| `etl_group/extension` | 73/88 | scalar | — | — | `"zip"` |
| `etl_group/file_name_group` | 88/88 | repeat_group | — | `file_inside_archive`, `file_name_value` | `{"etl_group/file_name_group/file_inside_archive": "sdei-annual-pm2-5-c` |
| `etl_group/format` | 88/88 | scalar | — | — | `"shp"` |
| `etl_group/last_updated` | 81/88 | scalar | — | — | `"2021-04-06"` |
| `etl_group/podid` | 88/88 | scalar | — | — | `"TBD"` |
| `etl_group/source` | 88/88 | scalar | — | — | `"https://sedac.ciesin.columbia.edu/downloads/data/sdei/sdei-annual-pm2` |
| `etl_group/table_name` | 88/88 | scalar | — | — | `"global_pm25_concentration_1998_2016"` |
| `etl_group/up` | 88/88 | scalar | — | — | `"tbd"` |
| `etl_group/update_frequency` | 88/88 | scalar | — | — | `"as_needed"` |
| `iso_group/band_group` | 28/88 | repeat_group | **raster** | `band_name` | `{"iso_group/band_group/band_name": "Single Band Elevation"}` |
| `iso_group/data_level` | 72/88 | scalar | — | — | `"derived"` |
| `iso_group/dimension_units` | 28/88 | scalar | **raster** | — | `"meters"` |
| `iso_group/epsg` | 88/88 | scalar | — | — | `"4326"` |
| `iso_group/extent` | 37/88 | scalar | — | — | `"-77.33\|-10.7\|-76.55\|-9.8"` |
| `iso_group/geometry` | 59/88 | scalar | **vector** | — | `"polygon"` |
| `iso_group/lineage` | 88/88 | scalar | — | — | `"TBD"` |
| `iso_group/pixel_dimension` | 28/88 | scalar | **raster** | — | `"30.0"` |
| `iso_group/point_of_contact_group` | 78/88 | repeat_group | — | `contact_name` | `{"iso_group/point_of_contact_group/contact_name": "TBD"}` |
| `iso_group/process_step` | 88/88 | scalar | — | — | `"TBD"` |
| `iso_group/processor` | 88/88 | scalar | — | — | `"TBD"` |
| `iso_group/structure` | 88/88 | scalar | — | — | `"vector"` |

## Kobo envelope / system fields (11)

Document these as intentional non-mappings (one representative `skos:noMatch` row), with the deliberate exceptions noted in the prompt.

`_attachments`, `_geolocation`, `_id`, `_status`, `_submission_time`, `_submitted_by`, `_uuid`, `_validation_status`, `_xform_id_string`, `meta/instanceID`, `meta/rootUuid`
