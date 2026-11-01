---
name: data-summary-statistics
description: Use when you have a curated relational dataset (structure-organism pairs) and need to quantify how structures distribute across a categorical variable (e.g., organism prevalence).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3372
  tools:
  - R
  - Python 3
  - lotus-processor
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]], 280[[3_cleaningAndEnriching/stereocounting.py]]
- R - Python 3 - Java >= 17
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
---

# data-summary-statistics

## Summary

Compute and report frequency distributions and summary counts across categorical bins to characterize the composition and coverage of a large structure-organism dataset. This skill validates data integrity by comparing observed bin membership against reference gold-standard counts.

## When to use

Apply this skill when you have a curated relational dataset (structure-organism pairs) and need to quantify how structures distribute across a categorical variable (e.g., organism prevalence). Use it as a validation checkpoint to detect data loss, miscuration, or processing errors by comparing bin counts against published benchmarks.

## When NOT to use

- Input is a pre-computed summary table or aggregated report (you would be double-summarizing).
- The analysis goal is to identify which specific structures or organisms are anomalous rather than to validate global bin distributions.
- Organism prevalence counts have not been computed or validated upstream; use organism-count binning as a prerequisite first.

## Inputs

- Flat-file table of structure-organism pairs (TSV or TSV.GZ format)
- Column defining unique structure identifier (SMILES or InChI)
- Column defining organism association for each pair
- Reference gold-standard bin counts (from published dataset version)

## Outputs

- Summary table with four rows (one per frequency bin) and columns for bin label, count, and discrepancy flag
- Text or markdown report documenting bin membership and any divergence from reference counts
- Validation flag (pass/fail) indicating whether observed counts match reference within tolerance

## How to apply

Load the flat-file table of structure-organism pairs (e.g., from LOTUS as .tsv.gz). Group all unique 2D structures by their organism count (the number of distinct organisms in which each structure appears). Define four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures (>100 organisms). Count the number of unique structures falling into each bin. Generate a summary report tabulating bin membership counts and compute any numeric discrepancies between observed counts and the gold-standard reference counts reported in the literature or prior dataset releases. Use R or Python (pandas, groupby, value_counts) to aggregate and validate.

## Related tools

- **R** (Execute grouping, binning, and count aggregation; generate summary reports) — https://www.r-project.org/
- **Python 3** (Load TSV/GZ files, perform pandas groupby and value_counts operations to bin and count structures) — https://www.python.org/
- **lotus-processor** (Source repository containing validated LOTUS data tables and example curation/validation workflows) — https://github.com/lotusnprod/lotus-processor

## Examples

```
python3 -c "import pandas as pd; df = pd.read_csv('lotus_pairs.tsv.gz', sep='\t', compression='gzip'); bins = df.groupby(df.groupby('structure_id').size().rename('org_count')).size(); print(f'Singleton: {bins[1]}, Low (2-10): {bins[2:11].sum()}, Medium (11-100): {bins[11:101].sum()}, High (>100): {bins[101:].sum()}')"
```

## Evaluation signals

- Observed bin counts for all four frequency categories (1, 2–10, 11–100, >100 organisms) are non-zero and match published LOTUS gold-standard counts to within ±1–2% (accounting for rounding and incremental updates).
- Total count of unique 2D structures across all bins matches the expected curated structure count (e.g., 153956 unique 2D structures for LOTUS).
- No structure appears in more than one bin; bin membership is mutually exclusive and exhaustive.
- Summary report is human-readable, clearly labeled by bin, and includes numeric discrepancy values flagged when observed ≠ reference.
- All input rows are accounted for in the output; no structures are dropped during grouping or binning.

## Limitations

- Binning thresholds (1, 2–10, 11–100, >100) are fixed and may not suit datasets with very different organism prevalence distributions.
- The skill depends on accurate upstream organism counting; errors in organism deduplication upstream will propagate into bin counts.
- Comparison to gold-standard reference counts assumes the reference is correct and applicable to the current dataset version; dataset growth or curation changes will render older benchmarks obsolete.
- The skill does not identify *which* structures or organisms are anomalous—only whether the global distribution is as expected.

## Evidence

- [other] Group all unique 2D structures by their associated organism count. Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures (>100 organisms).: "Group all unique 2D structures by their associated organism count. Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms),"
- [other] Count the number of structures in each bin and compare against the reported gold-standard counts.: "Count the number of structures in each bin and compare against the reported gold-standard counts."
- [other] LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding of organisms and their chemistry.: "LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding of organisms and their chemistry."
- [other] 231330 | 153956 (3D|2D) unique curated structures: "231330 | 153956 (3D|2D) unique curated structures"
- [other] Load the LOTUS 2D structure-organism pairs table from the published flat file.: "Load the LOTUS 2D structure-organism pairs table from the published flat file."
