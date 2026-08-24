# Kobo form field inventory

Built from **5 records**. Dataset types: {'vector': 3, 'raster': 1, 'table': 1}.

Treat this as the form schema: the union of every field across all records. `exclusive to` marks fields seen only under one dataset type — map those as conditional rows (VECTOR ONLY / RASTER ONLY) so one file serves every record.

> **Caveat:** `exclusive to` is evidence from the records pulled, not a guarantee about the form. A field can look type-exclusive simply because the records of the other type happened to leave it blank (a DOI, for example). Confirm against the form definition before treating a row as conditional.

## Form fields (66)

| field (exact Kobo key) | present | kind | exclusive to | sub-fields | example |
|---|---|---|---|---|---|
| `cartography_group/attributes_group` | 5/5 | repeat_group | — | `attribute_concept_id`, `attribute_description`, `attribute_end_date`, `attribute_external_id`, `attribute_min_value`, `attribute_name`, `attribute_source`, `attribute_start_date`, `attribute_type`, `attribute_unit`, `attribute_unit_concept_id` | `{"cartography_group/attributes_group/attribute_name": "holc_grade", "c` |
| `cartography_group/label` | 5/5 | scalar | — | — | `"holc_grade"` |
| `cartography_group/no_data_group` | 1/5 | repeat_group | **vector** | `no_data_type`, `no_data_value` | `{"cartography_group/no_data_group/no_data_type": "int", "cartography_g` |
| `cartography_group/values_group` | 2/5 | repeat_group | **vector** | `value_field` | `{"cartography_group/values_group/value_field": "holc"}` |
| `collection_group/analytic_epsg` | 5/5 | scalar | — | — | `"2236"` |
| `collection_group/analytic_function` | 5/5 | scalar | — | — | `"gdsc_nearest_neighbor gdsc_get_attributes"` |
| `collection_group/collections` | 5/5 | scalar | — | — | `"displacement-vulnerability-mitigation-tool displacement vulnerability` |
| `collection_group/derivatives` | 4/5 | scalar | — | — | `"sql"` |
| `collection_group/disclaimer` | 5/5 | scalar | — | — | `"no Disclaimer"` |
| `collection_group/service_definition` | 2/5 | scalar | **vector** | — | `"mdc_holc_redlining.sd"` |
| `collection_group/sponsor_group` | 4/5 | repeat_group | — | `sponsor_name`, `sponsor_url` | `{"collection_group/sponsor_group/sponsor_name": "IDSC", "collection_gr` |
| `collection_group/status` | 2/5 | scalar | — | — | `"draft"` |
| `collection_group/thumbnail` | 2/5 | scalar | **vector** | — | `"published"` |
| `control_group/external_id_group` | 3/5 | repeat_group | — | `external_id_type` | `{"control_group/external_id_group/external_id_type": "1"}` |
| `control_group/id` | 5/5 | scalar | — | — | `"1"` |
| `dublin_core_group/coverage_group` | 5/5 | repeat_group | — | `coverage_identifier`, `coverage_identifier_schema`, `coverage_identifier_schema_uri`, `coverage_name` | `{"dublin_core_group/coverage_group/coverage_name": "Miami-Dade County"` |
| `dublin_core_group/creator_group` | 5/5 | repeat_group | — | `creator_affiliation`, `creator_affiliation_identifier`, `creator_affiliation_schema`, `creator_affiliation_schema_uri`, `creator_identifier`, `creator_identifier_schema`, `creator_identifier_schema_uri`, `creator_name`, `creator_type` | `{"dublin_core_group/creator_group/creator_name": "University of Richmo` |
| `dublin_core_group/description` | 5/5 | scalar | — | — | `"The historical redlining grade from 143 cities across the United Stat` |
| `dublin_core_group/doi` | 1/5 | scalar | **vector** | — | `"10.7910/DVN/RHIFKL"` |
| `dublin_core_group/language` | 5/5 | scalar | — | — | `"en"` |
| `dublin_core_group/license` | 5/5 | scalar | — | — | `"public_domain"` |
| `dublin_core_group/license_text` | 3/5 | scalar | — | — | `"Miami-Dade County provides this data for use \"as is\". The areas dep` |
| `dublin_core_group/provenance` | 4/5 | scalar | — | — | `"direct from source as subset"` |
| `dublin_core_group/publication_date` | 5/5 | scalar | — | — | `"2020-06-24"` |
| `dublin_core_group/publisher_group` | 5/5 | repeat_group | — | `publisher_name` | `{"dublin_core_group/publisher_group/publisher_name": "University of Ri` |
| `dublin_core_group/relation_group` | 5/5 | repeat_group | — | `relation_title` | `{"dublin_core_group/relation_group/relation_title": "--"}` |
| `dublin_core_group/resource_type` | 5/5 | scalar | — | — | `"vector_dataset"` |
| `dublin_core_group/restrictions` | 5/5 | scalar | — | — | `"Use items owned by Esri in ArcGIS Online in conjunction with Esri sof` |
| `dublin_core_group/rights` | 5/5 | scalar | — | — | `"Public Domain"` |
| `dublin_core_group/subject_group` | 5/5 | repeat_group | — | `subject_term` | `{"dublin_core_group/subject_group/subject_term": "Florida\|Miami-Dade ` |
| `dublin_core_group/time_period_end` | 2/5 | scalar | — | — | `"1984-12-31"` |
| `dublin_core_group/time_period_start` | 2/5 | scalar | — | — | `"1984-01-01"` |
| `dublin_core_group/title` | 5/5 | scalar | — | — | `"Miami-Dade Home Owner's Loan Corporation (HOLC) Neighborhood Redlinin` |
| `dublin_core_group/url` | 5/5 | scalar | — | — | `"https://services.arcgis.com/jIL9msH9OI208GCb/arcgis/rest/services/HOL` |
| `etl_group/bash_etl` | 1/5 | scalar | **vector** | — | `"TBD"` |
| `etl_group/checksum` | 1/5 | scalar | **raster** | — | `"TBD"` |
| `etl_group/columns_group` | 1/5 | repeat_group | **vector** | `column_name` | `{"etl_group/columns_group/column_name": "OBJECTID"}` |
| `etl_group/custom_etl` | 1/5 | scalar | **vector** | — | `"not_applicable"` |
| `etl_group/custom_parameters` | 1/5 | scalar | **raster** | — | `"python \| copernicus_aggregate.py \| json;table;extension;extent;attr` |
| `etl_group/download` | 5/5 | scalar | — | — | `"esri_recursive_ogr"` |
| `etl_group/extension` | 5/5 | scalar | — | — | `"geojson"` |
| `etl_group/file_name_group` | 5/5 | repeat_group | — | `file_inside_archive`, `file_name_value` | `{"etl_group/file_name_group/file_name_value": "mdc_holc_redlining"}` |
| `etl_group/format` | 5/5 | scalar | — | — | `"geojson"` |
| `etl_group/index_fields_group` | 1/5 | repeat_group | **raster** | `index_field` | `{"etl_group/index_fields_group/index_field": "TBD"}` |
| `etl_group/last_updated` | 5/5 | scalar | — | — | `"2026-04-29"` |
| `etl_group/parameters` | 5/5 | scalar | — | — | `"city = 'Miami'\|f=json\|outSR=4326"` |
| `etl_group/podid` | 1/5 | scalar | **raster** | — | `"TBD"` |
| `etl_group/service` | 5/5 | scalar | — | — | `"api arcgis query"` |
| `etl_group/source` | 5/5 | scalar | — | — | `"https://services.arcgis.com/jIL9msH9OI208GCb/ArcGIS/rest/services/HOL` |
| `etl_group/sql_transform` | 1/5 | scalar | **vector** | — | `"TBD"` |
| `etl_group/table_name` | 5/5 | scalar | — | — | `"mdc_holc_redlining"` |
| `etl_group/up` | 1/5 | scalar | **raster** | — | `"unknown"` |
| `etl_group/update_frequency` | 5/5 | scalar | — | — | `"not_applicable"` |
| `iso_group/band_group` | 1/5 | repeat_group | **raster** | `band_name` | `{"iso_group/band_group/band_name": "t2m"}` |
| `iso_group/data_level` | 3/5 | scalar | **vector** | — | `"derived"` |
| `iso_group/dimension_units` | 1/5 | scalar | **raster** | — | `"degrees"` |
| `iso_group/epsg` | 5/5 | scalar | — | — | `"4326"` |
| `iso_group/extent` | 3/5 | scalar | — | — | `"-122.767506653\|25.705373207\|-70.949200532\|47.722514045"` |
| `iso_group/geometry` | 3/5 | scalar | **vector** | — | `"polygon"` |
| `iso_group/lineage` | 2/5 | scalar | **vector** | — | `"TBD"` |
| `iso_group/pixel_dimension` | 1/5 | scalar | **raster** | — | `"0.25"` |
| `iso_group/point_of_contact_group` | 1/5 | repeat_group | **vector** | `contact_name` | `{"iso_group/point_of_contact_group/contact_name": "TBD"}` |
| `iso_group/process_step` | 2/5 | scalar | **vector** | — | `"TBD"` |
| `iso_group/processor` | 2/5 | scalar | **vector** | — | `"TBD"` |
| `iso_group/structure` | 5/5 | scalar | — | — | `"vector"` |
| `iso_group/temporal_resolution` | 1/5 | scalar | **vector** | — | `"not_applicable"` |

## Kobo envelope / system fields (13)

Document these as intentional non-mappings (one representative `skos:noMatch` row), with the deliberate exceptions noted in the prompt.

`__version__`, `_attachments`, `_geolocation`, `_id`, `_status`, `_submission_time`, `_submitted_by`, `_uuid`, `_validation_status`, `_xform_id_string`, `formhub/uuid`, `meta/instanceID`, `meta/rootUuid`
