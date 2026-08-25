# Kobo form field inventory

Built from **128 records**. Dataset types: {'vector': 95, 'raster': 25, 'table': 7, 'raster_tiles': 1}.

Treat this as the form schema: the union of every field across all records. `exclusive to` marks fields seen only under one dataset type — map those as conditional rows (VECTOR ONLY / RASTER ONLY) so one file serves every record.

> **Caveat:** `exclusive to` is evidence from the records pulled, not a guarantee about the form. A field can look type-exclusive simply because the records of the other type happened to leave it blank (a DOI, for example). Confirm against the form definition before treating a row as conditional.

## Form fields (69)

| field (exact Kobo key) | present | kind | exclusive to | sub-fields | example |
|---|---|---|---|---|---|
| `cartography_group/attributes_group` | 128/128 | repeat_group | — | `attribute_concept_id`, `attribute_description`, `attribute_end_date`, `attribute_external_id`, `attribute_max_value`, `attribute_min_value`, `attribute_name`, `attribute_source`, `attribute_start_date`, `attribute_type`, `attribute_unit`, `attribute_unit_concept_id` | `{"cartography_group/attributes_group/attribute_description": "HOLC alp` |
| `cartography_group/color_ramp` | 22/128 | scalar | — | — | `"nv 0 0 0 0\n  178 0 68 27 255\n  160.2 0 109 44 255\n  142.4 29 134 6` |
| `cartography_group/label` | 75/128 | scalar | — | — | `"holc_grade"` |
| `cartography_group/legend` | 18/128 | scalar | **raster** | — | `"TBD"` |
| `cartography_group/no_data_group` | 13/128 | repeat_group | — | `no_data_type`, `no_data_value` | `{"cartography_group/no_data_group/no_data_type": "int4", "cartography_` |
| `cartography_group/tile_url_group` | 18/128 | repeat_group | — | `tile_base_url` | `{"cartography_group/tile_url_group/tile_base_url": "https://gdsc.idsc.` |
| `cartography_group/tile_zoom_group` | 22/128 | repeat_group | — | `tile_min_zoom` | `{"cartography_group/tile_zoom_group/tile_min_zoom": "8"}` |
| `cartography_group/values_group` | 61/128 | repeat_group | — | `values_group`, `value_field` | `{"cartography_group/values_group/value_field": "holc"}` |
| `collection_group/analytic_epsg` | 120/128 | scalar | — | — | `"2236"` |
| `collection_group/analytic_function` | 89/128 | scalar | — | — | `"gdsc_get_attributes gdsc_nearest_neighbor"` |
| `collection_group/collections` | 128/128 | scalar | — | — | `"displacement-vulnerability-mitigation-tool displacement vulnerability` |
| `collection_group/derivative_url` | 128/128 | scalar | — | — | `"/data/mdc_holc_redlining/"` |
| `collection_group/derivatives` | 83/128 | scalar | — | — | `"sql"` |
| `collection_group/disclaimer` | 56/128 | scalar | — | — | `"The Software is provided to the User and those who may take by, throu` |
| `collection_group/rights_statement` | 3/128 | scalar | **raster** | — | `"This data is open to the public and browse images are freely availabl` |
| `collection_group/service_definition` | 85/128 | scalar | — | — | `"API\|arcgis\|query"` |
| `collection_group/sponsor_group` | 105/128 | repeat_group | — | `sponsor_name`, `sponsor_url` | `{"collection_group/sponsor_group/sponsor_name": "IDSC", "collection_gr` |
| `collection_group/status` | 65/128 | scalar | — | — | `"published"` |
| `collection_group/thumbnail` | 23/128 | scalar | — | — | `"published"` |
| `control_group/external_id_group` | 7/128 | repeat_group | **vector** | `external_id_type`, `external_id_value` | `{"control_group/external_id_group/external_id_type": "ohdsi", "control` |
| `control_group/id` | 128/128 | scalar | — | — | `"1"` |
| `dublin_core_group/coverage_group` | 128/128 | repeat_group | — | `coverage_identifier`, `coverage_identifier_schema`, `coverage_identifier_schema_uri`, `coverage_name` | `{"dublin_core_group/coverage_group/coverage_identifier": "4164238", "d` |
| `dublin_core_group/creator_group` | 128/128 | repeat_group | — | `creator_affiliation`, `creator_affiliation_identifier`, `creator_affiliation_schema`, `creator_affiliation_schema_uri`, `creator_first_name`, `creator_identifier`, `creator_identifier_schema`, `creator_identifier_schema_uri`, `creator_last_name`, `creator_name`, `creator_type` | `{"dublin_core_group/creator_group/creator_identifier": "https://ror.or` |
| `dublin_core_group/description` | 128/128 | scalar | — | — | `"The historical redlining grade from 143 cities across the United Stat` |
| `dublin_core_group/doi` | 20/128 | scalar | — | — | `"https://doi.org/10.17604/p318-6n41"` |
| `dublin_core_group/language` | 108/128 | scalar | — | — | `"en"` |
| `dublin_core_group/license` | 28/128 | scalar | — | — | `"odc_by"` |
| `dublin_core_group/license_text` | 48/128 | scalar | — | — | `"This Software was created by U.S. Government employees and therefore ` |
| `dublin_core_group/provenance` | 120/128 | scalar | — | — | `"direct from source as subset"` |
| `dublin_core_group/publication_date` | 116/128 | scalar | — | — | `"2020-06-24"` |
| `dublin_core_group/publisher_group` | 128/128 | repeat_group | — | `publisher_name` | `{"dublin_core_group/publisher_group/publisher_name": "University of Ri` |
| `dublin_core_group/relation_group` | 14/128 | repeat_group | — | `relation_title` | `{"dublin_core_group/relation_group/relation_title": "tl_2021_12_tract"` |
| `dublin_core_group/resource_type` | 128/128 | scalar | — | — | `"vector_dataset"` |
| `dublin_core_group/restrictions` | 38/128 | scalar | — | — | `"Use items owned by Esri in ArcGIS Online in conjunction with Esri sof` |
| `dublin_core_group/rights` | 128/128 | scalar | — | — | `"public_domain"` |
| `dublin_core_group/size_group` | 128/128 | repeat_group | — | `size_bytes`, `size_human_readable` | `{"dublin_core_group/size_group/size_bytes": "121190", "dublin_core_gro` |
| `dublin_core_group/subject_group` | 128/128 | repeat_group | — | `subject_term` | `{"dublin_core_group/subject_group/subject_term": "Florida"}` |
| `dublin_core_group/time_period_end` | 9/128 | scalar | — | — | `"1984-12-31"` |
| `dublin_core_group/time_period_start` | 9/128 | scalar | — | — | `"1984-01-01"` |
| `dublin_core_group/title` | 128/128 | scalar | — | — | `"Miami-Dade Home Owner's Loan Corporation (HOLC) Neighborhood Redlinin` |
| `dublin_core_group/url` | 126/128 | scalar | — | — | `"https://services.arcgis.com/jIL9msH9OI208GCb/arcgis/rest/services/HOL` |
| `etl_group/checksum` | 126/128 | scalar | — | — | `"TBD"` |
| `etl_group/custom_etl` | 32/128 | scalar | — | — | `"acs_custom_aggregate"` |
| `etl_group/custom_parameters` | 32/128 | scalar | — | — | `"for=tract:*\|in=state:12\|in=county:086"` |
| `etl_group/dependency_group` | 24/128 | repeat_group | — | `dependency_table_name` | `{"etl_group/dependency_group/dependency_table_name": "fl_2021_tl_tract` |
| `etl_group/download` | 97/128 | scalar | — | — | `"esri_recursive_ogr"` |
| `etl_group/etl_parameters` | 34/128 | scalar | — | — | `"-t 48x48"` |
| `etl_group/extension` | 118/128 | scalar | — | — | `"geojson"` |
| `etl_group/file_name_group` | 128/128 | repeat_group | — | `file_inside_archive`, `file_name_value` | `{"etl_group/file_name_group/file_name_value": "mdc_holc_redlining"}` |
| `etl_group/format` | 128/128 | scalar | — | — | `"geojson"` |
| `etl_group/index_fields_group` | 1/128 | repeat_group | **vector** | `index_field` | `{"etl_group/index_fields_group/index_field": "true_mailing_addr1"}` |
| `etl_group/last_updated` | 128/128 | scalar | — | — | `"2023-06-13 23:02:46"` |
| `etl_group/podid` | 128/128 | scalar | — | — | `"gdsc-postgis-node-14tphzahiyxfy9tf"` |
| `etl_group/source` | 128/128 | scalar | — | — | `"https://services.arcgis.com/jIL9msH9OI208GCb/ArcGIS/rest/services/HOL` |
| `etl_group/table_name` | 128/128 | scalar | — | — | `"mdc_holc_redlining"` |
| `etl_group/up` | 128/128 | scalar | — | — | `"false"` |
| `etl_group/update_frequency` | 128/128 | scalar | — | — | `"never"` |
| `iso_group/band_group` | 25/128 | repeat_group | **raster** | `band_name` | `{"iso_group/band_group/band_name": "30-meter Landsat 8 Imagery Band 1"` |
| `iso_group/data_level` | 110/128 | scalar | — | — | `"derived"` |
| `iso_group/dimension_units` | 25/128 | scalar | **raster** | — | `"meters"` |
| `iso_group/epsg` | 120/128 | scalar | — | — | `"4326"` |
| `iso_group/extent` | 88/128 | scalar | — | — | `"POLYGON((-80.297516 25.705373, -80.118841 25.705373, -80.118841 25.91` |
| `iso_group/geometry` | 95/128 | scalar | **vector** | — | `"polygon"` |
| `iso_group/lineage` | 128/128 | scalar | — | — | `"TBD"` |
| `iso_group/pixel_dimension` | 25/128 | scalar | **raster** | — | `"30.0"` |
| `iso_group/point_of_contact_group` | 128/128 | repeat_group | — | `contact_affiliation`, `contact_affiliation_identifier`, `contact_affiliation_schema`, `contact_affiliation_schema_uri`, `contact_email`, `contact_first_name`, `contact_identifier`, `contact_identifier_schema`, `contact_identifier_schema_uri`, `contact_last_name`, `contact_name` | `{"iso_group/point_of_contact_group/contact_affiliation": "University o` |
| `iso_group/process_step` | 128/128 | scalar | — | — | `"#########\n  # GDSC ETL is performed in two steps: shell script to ET` |
| `iso_group/processor` | 128/128 | scalar | — | — | `"GDSC automation (see Process Step)"` |
| `iso_group/structure` | 128/128 | scalar | — | — | `"vector"` |

## Kobo envelope / system fields (11)

Document these as intentional non-mappings (one representative `skos:noMatch` row), with the deliberate exceptions noted in the prompt.

`_attachments`, `_geolocation`, `_id`, `_status`, `_submission_time`, `_submitted_by`, `_uuid`, `_validation_status`, `_xform_id_string`, `meta/instanceID`, `meta/rootUuid`
