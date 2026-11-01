---
name: error-report-generation
description: Use when when a user uploads a JSON project document to the Pairing Omics Data Platform and you need to determine whether it satisfies the platform's data structure requirements, including all mandatory fields, proper data types, and constraint satisfaction for paired omics metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - npm
  - ajv
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
---

# error-report-generation

## Summary

Validate JSON project documents against a formal schema and generate structured error reports enumerating constraint violations and missing required fields. This skill ensures uploaded omics data projects conform to the Pairing Omics Data Platform's structural and semantic requirements before acceptance.

## When to use

When a user uploads a JSON project document to the Pairing Omics Data Platform and you need to determine whether it satisfies the platform's data structure requirements, including all mandatory fields, proper data types, and constraint satisfaction for paired omics metadata (e.g., MS/MS spectra linked with genome, sample preparation, extraction method, and instrumentation method).

## When NOT to use

- Input is not a JSON document (e.g., XML, CSV, or binary omics data file).
- The schema file itself is missing, corrupted, or the validator library is unavailable.
- Validation of non-structural properties (e.g., scientific correctness of genome identifiers, GNPS task IDs, or whether sample preparation methods are appropriate for the analyte) — this skill only checks syntactic and format conformance.

## Inputs

- JSON project document (from user upload)
- JSON schema definition file (app/public/schema.json)

## Outputs

- Validation result (pass/fail boolean)
- Error report (list of constraint violations and missing fields with field names and descriptions)

## How to apply

Load the candidate JSON project file from the upload input and load the JSON Schema definition from app/public/schema.json. Perform schema validation using a JSON Schema validator library (e.g., ajv). If validation fails, enumerate and report each constraint violation or missing required field with sufficient specificity for the user to correct the document. Validation passes only when all required fields are present, all values match their specified types and formats, and all constraints defined in the schema are satisfied.

## Related tools

- **ajv** (JSON Schema validator library used to perform schema validation against the platform's schema.json)
- **npm** (Package manager and test runner for running validation in the development environment (npm run test))

## Evaluation signals

- A valid JSON project document passes validation with no errors reported.
- An invalid document missing required fields produces an error report naming each absent field.
- A document with malformed values (wrong type, invalid format, out-of-range) produces errors identifying the field name and the constraint violated.
- Error messages are specific enough for a user to locate and correct the problem in their JSON without ambiguity.
- Validation result is deterministic — the same document always produces the same result when validated against the same schema version.

## Limitations

- This skill validates only structural and format conformance; it cannot verify the scientific validity or accuracy of the metadata (e.g., whether a genome accession ID actually exists in GenBank, or whether a GNPS task ID is functional).
- The schema may become out of date if the platform adds new required fields or constraints; the schema file itself must be updated and deployed before validation reflects those changes.
- Error messages depend on the quality and clarity of the schema definition and validator library; unclear constraint descriptions in the schema will result in unclear error reports.

## Evidence

- [other] A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform.: "A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform."
- [other] Perform schema validation using a JSON Schema validator (e.g. ajv or similar library). Report validation result (pass or fail) and enumerate any constraint violations or missing required fields.: "Perform schema validation using a JSON Schema validator (e.g. ajv or similar library). Report validation result (pass or fail) and enumerate any constraint violations or missing required fields."
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project."
- [readme] Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
