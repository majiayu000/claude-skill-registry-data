---
name: matlab-package-execution
description: Use when you have two separate LC-MS untargeted metabolomic feature datasets (each with retention time and m/z values) and need to establish feature-to-feature correspondence between them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Matlab
  - M2S
derived_from:
- doi: 10.1021/acs.analchem.1c03592
  title: m2s
evidence_spans:
- Matlab package to match untargeted metabolomic features
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  dedup_kept_from: coll_m2s
schema_version: 0.2.0
---

# matlab-package-execution

## Summary

Execute a Matlab package to algorithmically match untargeted metabolomic features across two LC-MS datasets based on retention time and mass-to-charge ratio similarity. This skill is essential when you have two independent LC-MS feature tables and need to identify corresponding features to enable cross-dataset metabolomic analysis.

## When to use

You have two separate LC-MS untargeted metabolomic feature datasets (each with retention time and m/z values) and need to establish feature-to-feature correspondence between them. This is necessary before performing comparative metabolomics, quality control checks, or data fusion across multiple acquisition runs or instruments.

## When NOT to use

- Input data is already aligned or pre-matched; M2S is designed for de novo feature matching only
- Feature tables do not contain retention time and m/z values; M2S requires both metrics for matching
- You need targeted metabolomic feature matching; M2S is specifically designed for untargeted metabolomic features

## Inputs

- LC-MS untargeted metabolomic feature table 1 (retention time and m/z columns)
- LC-MS untargeted metabolomic feature table 2 (retention time and m/z columns)

## Outputs

- Matched feature table with feature correspondences and matching scores

## How to apply

Load both LC-MS untargeted metabolomic feature datasets into Matlab as feature tables containing retention time and m/z values. Initialize the M2S package by passing both feature tables as input arguments. The package executes a matching algorithm that compares features across the two datasets using retention time and m/z similarity metrics to identify corresponding features. The algorithm produces a matched feature table with feature correspondences and their associated matching scores. Export the resulting matched feature table for downstream analysis, ensuring that the matching scores meet your confidence threshold for the intended application.

## Related tools

- **M2S** (Matlab package that executes the feature matching algorithm using retention time and m/z similarity) — https://github.com/rjdossan/M2S

## Evaluation signals

- Matched feature table is generated with no errors or warnings from the M2S algorithm
- All entries in the matched feature table contain valid feature pairs (one from each input dataset) with non-null matching scores
- Matching scores are within expected range (0–1 or equivalent confidence metric defined by the package)
- Retention time and m/z differences between matched feature pairs are within expected tolerance windows for LC-MS reproducibility
- The number of matched features is consistent with biological expectations (e.g., >80% of features matched for technical replicates, lower overlap for different samples)

## Limitations

- M2S relies solely on retention time and m/z similarity; it does not incorporate intensity, spectral, or chemical identity information for matching
- Matching accuracy depends on the quality and consistency of retention time calibration across the two datasets
- The package is designed for two datasets only; matching multiple datasets requires pairwise application or post-hoc consensus strategies
- No information provided regarding sensitivity to parameter tuning or tolerance thresholds for matching

## Evidence

- [other] M2S is a Matlab package designed to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] The workflow accepts two feature datasets as input and produces matched features as output: "accepting two feature datasets as input and producing matched features as output"
- [other] M2S uses retention time and m/z ratio similarity for feature matching: "identify and link corresponding features across the two datasets based on retention time and mass-to-charge ratio similarity"
- [other] The output includes matching scores for each feature correspondence: "matched feature table containing feature correspondences and matching scores"
