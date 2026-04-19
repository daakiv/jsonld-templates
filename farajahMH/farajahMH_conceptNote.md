# FarajahMH Workflow
<img width="800" height="1100" alt="image" src="https://github.com/user-attachments/assets/1d0f9264-bc0a-4772-83ff-818fbd8ef80d" />

## Overview
The chatbot is the product of a workflow that begins with the INSPIRE data warehouse which hosts and links data from EHR records, population health studies and community conversational records between patients and community health workers. Next steps are taken by a schema.org JSON-LD DataCatalog through which warehouse (meta)data is projected into machine actionable Datasets that have and use their knowhow to move these Datasets into an OMOP CDM instance. Using the OHDSI methods library (HADES), here cohorts are constructed and features are extracted through whch prediction models are discovered that relate "idioms of distress", other observations and covariates with depression, anxiety and psychosis (DAP) health outcomes over time. These models are stored for downstream use. Downstream the OMOP CDM instance is converted into a Croissant dataset by the MIT Croissant-baker. Croissant datasets can be used to fine tune a bespoke LLM in our case with mental health knowledge on the HuggingFace and PyTorch platform. Feature selection during this fine tuning is informed by the model(s) that the OHDSI methods library has built.

## INSPIRE Data Warehouse
The warehouse hosts:
* digitized clinical archives in an EHR card format
* multiple waves of HDSS survey data
* community conversational records

The warehouse is structured as follows:

<img width="341" height="299" alt="image" src="https://github.com/user-attachments/assets/6785d5d2-46d3-4219-8989-42d09e6e04f1" />
<br />
This structure is closely aligned with LOINC. LOINC is a common language (set of identifiers, names, and codes) for identifying and describing health measurements, observations, panels of measurements, panels of observations (including questionnaires) and reports:
<br /><br />
<img width="494" height="365" alt="image" src="https://github.com/user-attachments/assets/437992c2-e90f-4341-9187-004e5e437274" />
<br />
INSPIRE data warehouse development is led by Dorothy Mailosi.

## Mental Health Data Catalog

## OMOP CDM Instance

## OHDSI Patient Pevel Prediction (PLP)

## Croissant Dataset

<img width="328" height="468" alt="image" src="https://github.com/user-attachments/assets/1f44a0d5-806c-48a8-998d-0a07256e0bb9" />
<br />

Conversion of an OMOP CDM instance into a Croissant dataset by the MIT Croissant-baker is a work in progress. See 
[here](https://github.com/MIT-LCP/croissant-baker/issues/33) for the latest and greatest.
<br /><br />
Conversion of an OMOP CDM instance into a Croissant dataset is led by Slava Tykhonov.

## Bespoke LLM Fine Tuning

## FarajaMH



