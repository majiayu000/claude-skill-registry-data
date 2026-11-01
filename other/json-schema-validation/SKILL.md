---
name: json-schema-validation
description: Use when you have loaded an mwTab file into a structured MWTabFile object
  and need to verify it conforms to MS or NMR schema specifications before deposition,
  curation, or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - mwtab
  - npm
  - ajv
  - Github
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
- doi: 10.1038/s41589-020-00724-z
  title: ''
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  - build: coll_pairedomicsdatapla_cq
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  - 10.1038/s41589-020-00724-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JSON Schema Validation

## Summary

Validate mwTab files against JSON schema definitions for MS and NMR experimental data to ensure structural conformance and data quality. This skill applies jsonschema-based validation to assess whether parsed mwTab data adheres to defined schema requirements for metabolomics datasets.

## When to use

Apply this skill when you have loaded an mwTab file into a structured MWTabFile object and need to verify it conforms to MS or NMR schema specifications before deposition, curation, or downstream analysis. Use it when you need to identify schema violations, missing required fields, or invalid metadata column formats in metabolomics experimental data.

## When NOT to use

- Input mwTab file has not been parsed into an MWTabFile object yet—use mwtab.fileio.read_files() first to load and instantiate the file
- You are converting mwTab to JSON format without validation requirements—use the converter module directly without schema checks
- Schema definitions (ms_schema or nmr_schema) for your experiment type are unavailable or not loaded

## Inputs

- mwtab.mwtab.MWTabFile object (parsed from mwTab file)
- JSON schema definition (ms_schema or nmr_schema)
- metadata_column_matching rules (optional, for column name/format validation)

## Outputs

- Validation report (pass/fail status)
- List of schema violation details
- Metadata column validation results
- Recommendations for schema correction

## How to apply

Load the mwTab file using the mwtab.mwtab.MWTabFile parser to extract structured metadata and tabular data sections. Retrieve the appropriate JSON schema definition (ms_schema or nmr_schema) that specifies required structure, metadata fields, and value constraints for the experiment type. Apply jsonschema validation against the parsed MWTabFile object, passing the schema and enabling verbose reporting to capture all violations. Collect and categorize validation errors and warnings, including metadata column validation results against standard column name and format rules (via metadata_column_matching). Generate a structured validation report documenting pass/fail status, violation details, and recommendations for correcting violations.

## Related tools

- **mwtab** (Parses mwTab files into MWTabFile objects and provides the validation interface) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **jsonschema** (Performs schema validation of parsed mwTab data against JSON schema definitions)
- **Python** (Execution environment for invoking validation functions and processing reports)

## Examples

```
import mwtab; import jsonschema; mwfile = mwtab.read_files('1')[0]; errors = list(mwtab.validate(mwfile, schema=mwfile.ms_schema)); print('Validation errors:', errors) if errors else print('File is valid')
```

## Evaluation signals

- Validation report returns pass status with zero schema violations for conformant files
- All required metadata fields and columns are present in the MWTabFile object before validation completes
- Violation details include specific schema path and constraint information enabling targeted corrections
- Metadata column names match standard naming conventions and value formats conform to schema rules
- Verbose validation output identifies both critical errors and non-blocking warnings for curation guidance

## Limitations

- Validation accuracy depends on completeness and correctness of the provided JSON schema definitions (ms_schema or nmr_schema); incomplete schemas may miss violations
- Metadata_column_matching validation is limited to defined standard column names and formats; novel or institution-specific column patterns may not be validated
- No changelog is available for mwtab, so breaking changes in schema or validation behavior may not be documented

## Evidence

- [other] The mwtab library uses jsonschema to validate mwTab files based on JSON schema definitions, enabling schema-based validation of MS and NMR experimental data files.: "The mwtab library uses jsonschema to validate mwTab files based on JSON schema definitions, enabling schema-based validation of MS and NMR experimental data files."
- [other] Apply jsonschema validation to the parsed mwTab data against the appropriate schema based on experiment type, with verbose reporting enabled by default.: "Apply jsonschema validation to the parsed mwTab data against the appropriate schema based on experiment type, with verbose reporting enabled by default."
- [other] Retrieve the MS and NMR JSON schemas (ms_schema and nmr_schema parameters) that define the required structure and content rules for each experiment type.: "Retrieve the MS and NMR JSON schemas (ms_schema and nmr_schema parameters) that define the required structure and content rules for each experiment type."
- [other] Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats).: "Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats)."
- [other] jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema.: "jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema."
