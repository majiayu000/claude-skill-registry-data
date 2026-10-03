---
name: json-file-parsing
description: Use when when you have JSON-formatted curation data organized in a directory
  structure (e.g., the MIBiG `data` directory) and need to extract a specific nested
  field (e.g., `cluster.status`) across all entries to build an index, summary table,
  or quality report.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0219
  tools:
  - Python (json module for parsing JSON files)
  - pandas or equivalent tabular data library
  - Python json module
  - pandas
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/nar/gkac1049
  title: MIBiG 3.0
evidence_spans:
- MIBiG curation data in JSON format
- entry status is now tracked via the `cluster.status` field
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_2_0_cq
    doi: 10.1093/nar/gkz882
    title: MIBiG 2.0
  - build: coll_mibig_3_0_cq
    doi: 10.1093/nar/gkac1049
    title: MIBiG 3.0
  dedup_kept_from: coll_mibig_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac1049
  all_source_dois:
  - 10.1093/nar/gkac1049
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-file-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and extract structured fields from JSON files distributed across a directory tree, aggregating results into a tabular format. This skill is essential when source data is curated in JSON format with nested schema (like MIBiG cluster annotations) and you need to index or summarize a particular field across all records.

## When to use

When you have JSON-formatted curation data organized in a directory structure (e.g., the MIBiG `data` directory) and need to extract a specific nested field (e.g., `cluster.status`) across all entries to build an index, summary table, or quality report.

## When NOT to use

- JSON files are already pre-indexed or aggregated into a single database or API endpoint — use direct database/API query instead.
- Target field is deeply nested or conditional on complex schema variants — may require custom schema mapping rather than simple dot-notation extraction.
- File count is extremely large (>1M files) and directory I/O becomes a bottleneck — consider batch processing or stream-based parsing.

## Inputs

- Directory tree containing JSON files (e.g., github.com/mibig-secmet/mibig-json `data` directory)
- Target nested field path as a dot-notation string (e.g., 'cluster.status')

## Outputs

- Tabular data file (CSV) with columns: entry_id, extracted_field_value
- Aggregated summary indexed by entry and field value

## How to apply

Recursively scan the target directory for all JSON files. For each file, parse the JSON structure and navigate to the target nested field using dot notation (e.g., `cluster.status`). Extract the field value along with the entry identifier. Aggregate all extracted records into a structured table (with columns for entry_id and the target field). Export the aggregated table to CSV or other tabular format. Validate the output by spot-checking a sample of entries against the original JSON files to confirm field extraction accuracy and absence of parsing errors.

## Related tools

- **Python json module** (Parse JSON structure and navigate nested fields)
- **pandas** (Aggregate parsed records into tabular data and export to CSV)

## Examples

```
import json, os, pandas as pd; records = []; [records.append({'entry_id': f.split('.')[0], 'cluster_status': json.load(open(os.path.join('data', f))).get('cluster', {}).get('status')}) for f in os.listdir('data') if f.endswith('.json')]; pd.DataFrame(records).to_csv('entry_status_index.csv', index=False)
```

## Evaluation signals

- Output CSV contains no blank rows and row count matches total JSON files scanned
- Spot-check: randomly select 5–10 entries from output and verify extracted field values match the original JSON files
- No parsing errors or exceptions logged during directory traversal and JSON deserialization
- All expected entry identifiers are present in the output; no entries silently dropped
- CSV schema matches specification: entry_id column is unique and non-null; extracted_field_value column contains valid values for the field type (e.g., status is a recognized categorical value)

## Limitations

- Assumes well-formed JSON and consistent nested schema across all files; malformed or schema-variant entries may cause parsing errors or silent omissions.
- Dot-notation field extraction is brittle if schema evolves or if field is conditionally present; requires manual schema validation before applying this skill at scale.
- No changelog or version tracking in the MIBiG repository was found, so field semantics or structure may change without notice between data pulls.

## Evidence

- [readme] The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field.: "The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field."
- [other] MIBiG curation data is maintained in JSON format with entry status tracked through the `cluster.status` field within each annotation record.: "MIBiG curation data is maintained in JSON format with entry status tracked through the `cluster.status` field"
- [other] Recursively scan the `data` directory for all JSON files. Parse each JSON file and extract the `cluster.status` field value for each entry. Aggregate entries into a table grouped by status.: "Recursively scan the `data` directory for all JSON files. 2. Parse each JSON file and extract the `cluster.status` field value for each entry. 3. Aggregate entries into a table"
- [other] Python (json module for parsing JSON files), pandas or equivalent tabular data library: "Python (json module for parsing JSON files), pandas or equivalent tabular data library"
