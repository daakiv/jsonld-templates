# FarajahMH Workflow
<img width="800" height="1000" alt="image" src="https://github.com/user-attachments/assets/2ec03a8e-b086-47be-8fd4-6646197dff27" />

## Overview
The chatbot is the product of a workflow that begins with the INSPIRE data warehouse which hosts and links data from EHR records, population health studies and community conversational records between patients and community health workers. Next steps are taken by a schema.org JSON-LD DataCatalog through which warehouse (meta)data is projected into machine actionable Datasets that have the knowhow an open source AI coding agent uses to move these Datasets into an OMOP CDM instance. Here, using the OHDSI methods library (HADES), cohorts are constructed and features are extracted through which prediction models are discovered that relate "idioms of distress", other observations (like SES and education) and covariates with depression, anxiety and psychosis (DAP) health outcomes over time. These models are stored for downstream use. Downstream the OMOP CDM instance is converted into one or more Croissant datasets by the MIT Croissant-baker. These Croissant datasets are used to fine tune a bespoke LLM with mental health knowledge on the HuggingFace and PyTorch platform. Feature selection during fine tuning is informed by the model(s) that the OHDSI methods library has built.

## INSPIRE Data Warehouse
The warehouse hosts:
* digitized clinical archives in an EHR card format
* multiple waves of HDSS survey data
* community conversational records

The warehouse is structured as follows:

<img width="519" height="352" alt="image" src="https://github.com/user-attachments/assets/13520193-5069-4970-9ad4-9a13d25a02b8" />

<br />
This structure is closely aligned with LOINC (Logical Observation Identifiers Names and Codes). LOINC acts as a common language for identifying and describing health measurements ("labs"), observations NLP makes from clinical notes and patient/provider conversations, panels of measurements, panels of observations (including questionnaires) and reports:
<br /><br />
<img width="494" height="365" alt="image" src="https://github.com/user-attachments/assets/437992c2-e90f-4341-9187-004e5e437274" />
<br />
The alignment goes like this: <br /><br />

* In the data warehouse there are facts that corresponds to LOINC observations and measurements
* Different parts of a fully specified observation or measurement in LOINC like code, component, system, timing, scale and method are captured across the several dimensions of the measurement and observation facts in the data warehouse
* These dimensions include records for concept, person, instrument, method, sample, visit, agent, place and panel

INSPIRE data warehouse development is led by Dorothy Mailosi.

## Mental Health DataCatalog
The Mental Health DataCatalog has several components:
* The catalog itself is a schema.org DataCatalog which is a collection of one or more schema.org Datasets rendered in JSON-LD format
* The catalog has an authoring tool that generates the schema.org JSON-LD datasets that we draw from the data warehouse
* Each dataset in the catalog includes a knowledgebase that an AI coding agent can use to create concepts in a OMOP CDM community vocabulary for the DAP "idioms of distress" under the direction of clinical expertise and lived experience
* Each dataset in the catalog includes a knowledgebase that an AI coding agent can use to create observations, measurements and visit occurrences in an OMOP CDM instance using concepts from this community vocabulary

A catalog with this functionality is not new. Parts of it have been developed already in another project the CODATA team is participating -- the [OHDSI GIS WG](https://github.com/OHDSI/GIS). And the OHDSI GIS WG itself and its initiative called the gaiaCatalog has been guided by work started at the University of Miami. That being said, hosting a knowledgebase for AI agents is experimental and is still very much a work in progress. Success with agentic AI in these early times will take a significant effort.
<br /><br />
David Amadi will lead authoring and catalog entry generation except he will need support from the CODATA team (Doug Fils and Letisha Najjemba) when it comes to the parts of the catalog that an AI coding agent might use first to create concepts iteratively under the direction of clinical expertise and lived experience and then to populate measurements and observations in an OMOP CDM instance using these concepts.


## OMOP CDM Instance

## OHDSI Patient Level Prediction (PLP)
PLP will be conducted in OHDSI. Three PLP outcome cohorts will be created -- one for people who test positive on the GAD-7 anxiety scale, another for people who test positive on the PHQ-9 depression scale and a third for people who test positive on the psychosis screener. The composition of the target cohort(s) is to be determined. Using the ATLAS interface, feature selection in OHDSI PLP usually comes with the choice of prediction methods and their hyperparameters. In our use case, because of the data and for the sake of Responsible AI, our plan is to conduct PLP via scripting instead.

Letisha Najjemba will lead OHDSI PLP.

## Croissant Dataset

<img width="328" height="468" alt="image" src="https://github.com/user-attachments/assets/1f44a0d5-806c-48a8-998d-0a07256e0bb9" />
<br />

Conversion of OMOP CDM instances into Croissant datasets by the MIT Croissant-baker is a work in progress. See 
[here](https://github.com/MIT-LCP/croissant-baker/issues/33) for the latest and greatest.
<br /><br />
Conversion of OMOP CDM instances into Croissant datasets is led by Slava Tykhonov.

## Bespoke LLM Fine Tuning

## FarajaMH



