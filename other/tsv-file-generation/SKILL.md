---
name: tsv-file-generation
description: Use when after completing a BiG-SLiCE v2 clustering analysis on an input
  folder of BGCs, when you need to retrieve the computed BGC and GCF cluster membership
  tables in a portable, widely-compatible tabular format rather than querying the
  SQLite database directly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
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

# Export Pre-calculated BGC and GCF Tables to TSV Format

## Summary

Export BiG-SLiCE v2 pre-calculated Biosynthetic Gene Cluster (BGC) and Gene Cluster Family (GCF) tables from a completed clustering run into tab-separated values (TSV) files for downstream tabular analysis and integration with external tools.

## When to use

After completing a BiG-SLiCE v2 clustering analysis on an input folder of BGCs, when you need to retrieve the computed BGC and GCF cluster membership tables in a portable, widely-compatible tabular format rather than querying the SQLite database directly.

## When NOT to use

- Input clustering analysis is still running or incomplete — --export-csv requires a finalized result directory
- You need programmatic access to structured cluster data with complex query requirements — use direct SQLite3 queries instead for more flexible filtering and joining
- Output must remain in a database format for subsequent BiG-SLiCE operations like --query mode

## Inputs

- BiG-SLiCE v2 output directory (completed clustering run)
- SQLite3 database file containing pre-calculated BGC and GCF clustering results

## Outputs

- TSV file(s) containing BGC cluster assignments and metadata
- TSV file(s) containing GCF (Gene Cluster Family) cluster definitions and metadata

## How to apply

Invoke the BiG-SLiCE command-line tool with the --export-csv parameter, pointing it to a completed run directory where clustering results have already been calculated and stored. The parameter triggers export of pre-calculated BGC and GCF tables from the output database into TSV files. The exported files are written to the same output directory and can be read by any downstream tabular analysis tool (spreadsheet software, R, pandas, etc.). Verify export success by checking for the presence of TSV files in the output directory with expected structure and row counts matching the clustering summary.

## Related tools

- **BiG-SLiCE** (Primary clustering engine and command-line interface for invoking --export-csv export functionality) — https://github.com/medema-group/bigslice
- **pyHMMER** (Underlying HMM profile search library used by BiG-SLiCE v2 to generate the pre-calculated cluster assignments being exported) — https://github.com/althonos/pyhmmer

## Examples

```
bigslice --export-csv <output_folder>
```

## Evaluation signals

- TSV files are present in the output directory with non-zero file size and readable structure
- TSV header row matches expected BGC/GCF table schema (presence of cluster ID, BGC ID/name, domain architecture, and similarity columns)
- Number of data rows in TSV files matches the BGC/GCF counts reported by BiG-SLiCE's console output or version summary
- TSV files are tab-delimited (verifiable by parsing with standard CSV/TSV readers) with consistent column count across all rows
- Re-import of TSV into R/pandas does not raise schema, encoding, or parsing errors

## Limitations

- TSV export requires the clustering analysis to be fully completed — no partial exports available during an ongoing run
- Export format may differ between BiG-SLiCE major versions; v2.0.0 schema may not be backward-compatible with earlier versions
- Large clustering results (>1M BGCs) may produce very large TSV files; consider disk space and memory constraints when loading into tabular software
- No built-in filtering or column selection at export time — all pre-calculated tables are exported; post-processing is required for subsetting

## Evidence

- [readme] Ability to export pre-calculated BGCs and GCFs table into TSVs: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
- [other] Workflow for invoking export: "Invoke BiG-SLiCE with the --export-csv parameter on a completed run directory to export the pre-calculated BGC and GCF cluster tables."
- [other] Output location and format: "Retrieve the exported TSV files from the output directory."
