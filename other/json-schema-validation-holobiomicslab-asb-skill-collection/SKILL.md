---
name: json-schema-validation
description: Use when after extracting tabular data into intermediate JSON representation (via tagging), or after manual JSON editing, and before converting to a target format (e.g., mwTab for Metabolomics Workbench).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - jsonschema
  - MESSES
  - npm
  - ajv
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
- doi: 10.1038/s41589-020-00724-z
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_messes
schema_version: 0.2.0
---

# JSON Schema Validation

## Summary

Validate extracted or intermediate JSON data against formal JSON Schema specifications and custom protocol-dependent schemas to detect structural, type, and domain-specific errors before format conversion or deposition. This skill catches inconsistencies early in the data pipeline, reducing downstream failures during conversion to repository-preferred formats.

## When to use

After extracting tabular data into intermediate JSON representation (via tagging), or after manual JSON editing, and before converting to a target format (e.g., mwTab for Metabolomics Workbench). Use this skill when you need confidence that your JSON conforms to the Experiment Description Specification, adheres to protocol-dependent constraints, or satisfies format-specific schema requirements. Particularly important when multiple contributors have tagged or edited JSON, or when the extraction rules are new or complex.

## When NOT to use

- Input JSON is already known to conform to the target schema and has been previously validated in the same workflow.
- You are performing a quick data preview or exploratory analysis where schema conformance is not a hard requirement.
- The JSON comes from a trusted, automated source with its own internal validation already in place (though re-validation is still recommended for critical pipelines).

## Inputs

- Intermediate JSON file extracted from tabular data
- JSON Schema file (Experiment Description Specification)
- Protocol Dependent Schema (PDS) JSON file (optional, project-specific)
- Format-specific JSON Schema (e.g., mwTab schema)

## Outputs

- Validation report (errors and warnings list)
- Pass/fail status per schema
- Corrected intermediate JSON file (after fixing reported issues)

## How to apply

Load your intermediate JSON file and one or more JSON Schema files: the built-in Experiment Description Specification schema, any Protocol Dependent Schema (PDS) you have created for your project, and the format-specific schema (e.g., mwTab schema). Use jsonschema to validate the JSON against each schema in sequence. Document all validation errors and warnings, then feed them back to the data source (raw tabular file or JSON editor) to fix structural issues, missing required fields, or type mismatches. Repeat extraction → validation → correction cycles until no errors remain. This iterative approach, combined with the ability to view record lineages, helps trace validation failures back to their source in the original data.

## Related tools

- **jsonschema** (Python library for validating JSON documents against JSON Schema specifications; used to check intermediate JSON against Experiment Description Specification, Protocol Dependent Schema, and format-specific schemas) — https://pypi.org/project/jsonschema/
- **MESSES** (Command-line tool and Python package that integrates JSON schema validation as the 'validate' command; orchestrates validation workflows and integrates results with extraction and conversion steps) — https://github.com/MoseleyBioinformaticsLab/MESSES

## Examples

```
messes validate json your_data.json --pds your_schema.json --format desired_format
```

## Evaluation signals

- JSON document passes validation against Experiment Description Specification without errors.
- JSON document passes validation against Protocol Dependent Schema (if provided) with zero errors.
- JSON document passes validation against format-specific schema (e.g., mwTab) with zero errors.
- All required fields are present and populated with appropriate data types (string, number, array, object).
- Record lineage can be traced back to source tabular data without gaps or missing references.

## Limitations

- Validation reports only flag schema violations; they do not verify semantic correctness or domain-specific logic (e.g., whether mass values are physically plausible). Custom validation rules beyond JSON Schema syntax must be implemented separately.
- The initial schema design and Protocol Dependent Schema creation require significant effort and domain expertise; poorly designed schemas will produce false negatives or fail to catch real errors.
- Validation does not fix errors automatically; all corrections must be made in the source data (tabular file) or intermediate JSON, and extraction/validation must be re-run.

## Evidence

- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the `Experiment Description Specification`, the `Protocol Dependent Schema`, any additional JSON schema you wish to provide,"
- [other] The validate command of MESSES supports validating JSON data using JSON Schema and custom schemas.: "The validate command of MESSES supports validating JSON data. This is done largely through utilizing `JSON Schema`"
- [readme] Original data entry, manual tagging of tabular data, and even automated tagging facilities can be messy, generating errors in the extracted JSONized representation. So MESSES includes a validate command to help make sure your data is in line with your project parameters and data schema.: "original data entry, manual tagging of tabular data, and even automated tagging facilities can be messy, generating errors in the extracted JSONized representation. So MESSES includes a validate"
- [readme] The expected workflow includes using the validate command to validate JSON based on your specific project schema, fixing errors and warnings in the original data, and repeating until there are no more errors.: "then use the "validate" command to validate the JSON based on your specific project schema, fix errors and warnings in the original data, repeat steps 1-3 until there are no more errors"
