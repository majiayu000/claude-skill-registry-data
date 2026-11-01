---
name: tabular-data-tag-parsing
description: 'Use when you have raw tabular experimental data (CSV or Excel) with column headers annotated using MESSES tag syntax (#<table_name>.id for record identifiers, #.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES
  - jsonschema
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes
schema_version: 0.2.0
---

# tabular-data-tag-parsing

## Summary

Parse tagged tabular files (Excel or CSV) into nested JSON by interpreting export tags (prefixed with # or #.) in column headers to map table names, record identifiers, and field names. This extraction step converts raw experimental metadata spreadsheets into a standardized, interoperable JSON representation suitable for downstream validation and format conversion.

## When to use

You have raw tabular experimental data (CSV or Excel) with column headers annotated using MESSES tag syntax (#<table_name>.id for record identifiers, #.<field_name> for field values), and you need to transform it into a nested JSON structure that conforms to the Experiment Description Specification for validation and repository submission.

## When NOT to use

- Input tabular data has no tagging layer or uses a different tagging convention incompatible with MESSES syntax
- Data is already in valid JSON format and only needs validation or conversion, not extraction
- Tabular data structure does not follow a record-based model (e.g., purely columnar, matrix-like experimental data without identifiable records or tables)

## Inputs

- tagged tabular file (CSV or Excel format)
- column headers with MESSES export tags (#<table_name>.id, #.<field_name>)
- tabular rows with experimental metadata and measurements

## Outputs

- nested JSON structure with table names as top-level keys
- records indexed by identifier within each table
- field key-value pairs within each record
- intermediate JSON representation conforming to Experiment Description Specification

## How to apply

Read the tagged tabular file row-by-row and parse each column header to extract tag syntax: identify # or #. prefixes, then extract the table name and field name (or record identifier marker) from the tag string. Build a hierarchical JSON dictionary by iterating through rows: for each row, create or append records keyed by table name and record identifier (from columns marked #<table_name>.id), populating field key-value pairs from columns marked #.<field_name>. Validate that all tagged columns conform to expected syntax (either #<table_name>.id or #.<field_name>) and that no duplicate record identifiers exist within a single table before outputting the nested JSON. The MESSES extract command automates this process and produces intermediate JSON ready for downstream validation and conversion steps.

## Related tools

- **MESSES** (Python package that automates tagged tabular extraction via the 'extract' command, handling tag parsing, JSON serialization, and validation against Experiment Description Specification) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Programming language for implementing tag parsing logic, JSON object construction, and row-by-row file iteration)
- **jsonschema** (Post-extraction validation tool for verifying the produced nested JSON against the Experiment Description Specification and Protocol Dependent Schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes extract your_data.csv --output your_data.json
```

## Evaluation signals

- All tagged columns in the input are successfully parsed and no tag syntax errors or unrecognized prefixes remain in the output
- The output nested JSON structure has correct hierarchy: table names at top level, records keyed by identifier within each table, field key-value pairs within records
- No duplicate record identifiers exist within a single table (validate uniqueness of #<table_name>.id values per table)
- The output JSON validates successfully against the Experiment Description Specification using jsonschema
- All rows from the input tabular file are represented in the output JSON with no data loss

## Limitations

- Tag parsing assumes strict adherence to MESSES tag syntax (#<table_name>.id and #.<field_name>); malformed, missing, or non-standard tags will cause parsing errors or data loss
- The skill requires prior manual or automated tagging of the raw tabular data; untagged spreadsheets cannot be processed without first applying the tagging layer
- Duplicate record identifiers within a table will be flagged as an error; the user must resolve identifier conflicts in the source data before extraction succeeds
- The approach is specific to record-oriented (relational) data models; purely columnar or matrix-based experimental data (e.g., omics feature tables) may not map cleanly to the nested table-record-field structure

## Evidence

- [other] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: "Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing"
- [other] Extract tabular data into JSON using tags. This is done by adding a layer of tags on top of the data.: "The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data."
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats."
- [readme] MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a"
- [readme] The expected workflow is to use the "extract" command to transform your tabular data into JSON: "The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON based on your specific project schema"
