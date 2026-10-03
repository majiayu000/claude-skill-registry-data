---
name: bgc-cluster-export
description: Use when you have completed a BiG-SLiCE v2 clustering analysis and need
  to convert the internal SQLite3 database results into human-readable, tabular TSV
  files for import into spreadsheet applications, statistical tools, or custom analysis
  pipelines that do not support SQLite3 directly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3999
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0218
  tools:
  - BiG-SLiCE
  - pyHMMER
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_slice_cq
    doi: 10.1093/gigascience/giaa154
    title: BiG-SLiCE
  dedup_kept_from: coll_big_slice_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa154
  all_source_dois:
  - 10.1093/gigascience/giaa154
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Export Pre-Calculated BGC and GCF Tables to TSV

## Summary

Export pre-calculated Biosynthetic Gene Cluster (BGC) and Gene Cluster Family (GCF) tables from a completed BiG-SLiCE v2 run into tab-separated values (TSV) format for downstream analysis and data sharing. This enables tabular access to clustering results without requiring programmatic database queries.

## When to use

Use this skill when you have completed a BiG-SLiCE v2 clustering analysis and need to convert the internal SQLite3 database results into human-readable, tabular TSV files for import into spreadsheet applications, statistical tools, or custom analysis pipelines that do not support SQLite3 directly.

## When NOT to use

- The clustering run has not completed successfully or the output directory does not contain a valid SQLite3 database.
- You need real-time query access or programmatic filtering of clustering results (use SQL queries on the database directly instead).
- The output will be consumed downstream by a tool that natively reads SQLite3 (TSV export is redundant).

## Inputs

- BiG-SLiCE v2 output directory (containing completed clustering run with SQLite3 database)

## Outputs

- Tab-separated values (TSV) files containing BGC cluster table
- Tab-separated values (TSV) files containing GCF cluster table

## How to apply

After BiG-SLiCE v2 has completed a clustering run (producing an output folder with an SQLite3 database), invoke the bigslice command with the --export-csv parameter pointing to that output folder. The parameter triggers BiG-SLiCE to reconstruct the pre-calculated BGC and GCF cluster tables from the internal database and serialize them as TSV files. The exported TSVs will be written to the output directory alongside the original database. No intermediate processing or reformatting is required; the export operation handles schema reconstruction automatically.

## Related tools

- **BiG-SLiCE** (Performs BGC/GCF clustering and exports results via --export-csv parameter) — https://github.com/medema-group/bigslice
- **pyHMMER** (Underlying HMMER3 binding library used by BiG-SLiCE for profile HMM search) — https://github.com/althonos/pyhmmer

## Examples

```
bigslice --export-csv <output_folder>
```

## Evaluation signals

- TSV files are present in the output directory after running --export-csv.
- TSV files contain expected column headers corresponding to BGC and GCF metadata (e.g., cluster ID, family ID, gene count, domain composition).
- Row counts in exported TSVs match the number of BGCs and GCFs recorded in the internal database (can be verified by SQLite3 SELECT COUNT queries).
- TSV files are parseable by standard tabular data tools (e.g., `cut`, `awk`, pandas, R `read.delim()`) without format errors.
- No data loss or truncation between database records and TSV output (spot-check representative rows for completeness).

## Limitations

- Export produces read-only snapshots of the database at export time; subsequent database updates are not reflected in already-exported TSVs.
- Large clustering runs (1.2M+ BGCs) may produce very large TSV files that are memory-intensive to load in spreadsheet applications.
- TSV format loses relational schema and integrity constraints present in the SQLite3 database; joining or filtering across tables requires manual logic in downstream tools.

## Evidence

- [intro] Ability to export pre-calculated BGCs and GCFs table into TSVs: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
- [other] TSV file retrieval workflow: "Invoke BiG-SLiCE with the --export-csv parameter on a completed run directory to export the pre-calculated BGC and GCF cluster tables. Retrieve the exported TSV files from the output directory."
- [readme] Internal data storage format: "BiG-SLiCE's output folder contains both the processed input data (in the form of an SQLite3 database file)"
