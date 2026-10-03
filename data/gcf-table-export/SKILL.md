---
name: gcf-table-export
description: Use when you have completed a BiG-SLiCE v2 clustering run and need to
  extract the pre-calculated BGC and GCF cluster assignments in TSV format for postprocessing,
  integration with SQL pipelines, or sharing with collaborators who require flat tabular
  output rather than the SQLite database or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3697
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

# Export pre-calculated BGCs and GCFs tables into TSVs

## Summary

Export clustered BGC and GCF tables from a completed BiG-SLiCE v2 run into tab-separated value (TSV) files for downstream analysis and integration with external tools. This skill enables tabular access to pre-computed BGC-to-GCF assignments and GCF metadata.

## When to use

Apply this skill when you have completed a BiG-SLiCE v2 clustering run and need to extract the pre-calculated BGC and GCF cluster assignments in TSV format for postprocessing, integration with SQL pipelines, or sharing with collaborators who require flat tabular output rather than the SQLite database or interactive web interface.

## When NOT to use

- If you need access to BGC feature vectors themselves rather than cluster assignments — use SQL queries on the database or the programmatic API instead.
- If your downstream analysis requires the full hierarchical clustering dendrogram or similarity distances between all BGC pairs — the TSV export provides only cluster membership, not pairwise distances.
- If you have not yet run BiG-SLiCE clustering on your input BGCs — this skill requires a completed run with pre-calculated assignments.

## Inputs

- BiG-SLiCE v2 completed run directory (containing SQLite database and processed BGC data)
- Output folder path where TSV exports should be written

## Outputs

- TSV file with BGC identifiers and GCF cluster assignments
- TSV file with pre-calculated BGCs table
- TSV file with pre-calculated GCFs table

## How to apply

After a BiG-SLiCE v2 clustering run completes successfully, invoke the --export-csv parameter on the output folder directory. BiG-SLiCE will serialize the internally computed BGC feature vectors (already normalized via l2-normalization for cosine-like distance clustering) and their assigned GCF cluster IDs into TSV tables. The exported tables include BGC identifiers, GCF cluster assignments, and associated metadata columns. Retrieve the exported TSV files from the designated output directory. Verify that all BGCs present in the input are represented in the output TSV and that GCF cluster IDs are consistent with the SQLite database.

## Related tools

- **BiG-SLiCE** (Performs BGC clustering via l2-normalized cosine-like distances and provides --export-csv parameter to serialize GCF tables into TSV format) — https://github.com/medema-group/bigslice
- **pyHMMER** (Underlying HMM search engine used by BiG-SLiCE v2 to compute BGC feature vectors from domain annotations) — https://github.com/althonos/pyhmmer

## Examples

```
bigslice --export-csv <output_folder>
```

## Evaluation signals

- TSV files are produced in the output directory with correct tabular structure (tab-delimited, proper header row).
- All BGC identifiers from the input are present in the exported BGC table.
- GCF cluster IDs are positive integers and form a contiguous or sparse set with no orphaned references.
- BGC-to-GCF mapping in the TSV matches the cluster assignments stored in the SQLite database when queried directly.
- TSV export completes without errors or warnings from BiG-SLiCE (exit code 0).

## Limitations

- TSV export provides only cluster membership and metadata; pairwise BGC similarity scores and hierarchical distances are not included and require direct SQL queries.
- Export is read-only and represents a snapshot of the clustering state at export time; re-running clustering will require re-export to capture updated assignments.
- Large clustering results (>100k BGCs) may produce very large TSV files that require streaming or chunked parsing in downstream applications.

## Evidence

- [readme] Ability to export pre-calculated BGCs and GCFs table into TSVs: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
- [readme] Clustering methodology uses l2-normalized cosine distances: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [other] Export workflow retrieves TSV files from output directory: "Retrieve the exported TSV files from the output directory"
- [other] BGC-to-GCF mapping is exported with identifiers and cluster IDs: "Export the BGC-to-GCF mapping as a TSV table with BGC identifier and GCF cluster ID columns"
