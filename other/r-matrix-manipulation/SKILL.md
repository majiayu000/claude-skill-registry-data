---
name: r-matrix-manipulation
description: 'Use when when working with three-part metabolomics data structures (featuredata
  matrix, metabolitedata and sampledata dataframes) and you need to: (1) identify
  subsets of metabolites by their annotation (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R matrix manipulation for metabolomics feature data

## Summary

Programmatically load, index, and transform metabolomics feature matrices in R using vectorized operations and conditional subsetting. This skill enables extraction of control metabolite indices, application of normalization workflows, and assembly of multi-component result objects from featuredata, sampledata, and metabolitedata inputs.

## When to use

When working with three-part metabolomics data structures (featuredata matrix, metabolitedata and sampledata dataframes) and you need to: (1) identify subsets of metabolites by their annotation (e.g., negative controls via a Boolean column), (2) apply a normalization function that returns a list object and extract normalized featuredata plus computed components (e.g., unwanted variation matrices), or (3) store the results as a named list object for downstream analysis.

## When NOT to use

- Input data is already in a pre-normalized or processed format and control metabolite identification is not needed
- Metabolite annotations (neg_control or equivalent column) are missing from metabolitedata; the conditional indexing step will fail or return empty indices
- The normalization function has already been applied and the result object is being reprocessed; re-running risks double-normalization

## Inputs

- featuredata (numeric matrix: samples × metabolites)
- metabolitedata (dataframe with metabolite annotations, including control status columns)
- sampledata (dataframe with sample metadata)
- control indices (integer vector from conditional indexing)

## Outputs

- uv_ruvrandclust or similar named list object containing: normalized featuredata, unwanted variation matrix (uvdata), and associated metadata
- Extracted normalized featuredata matrix
- Computed variation components

## How to apply

Load the metabolomics dataset (three components: featuredata as a numeric matrix with samples as rows and metabolites as columns; metabolitedata as a dataframe with metabolite names as row names; sampledata as a dataframe with sample names as row names) into R using the NormalizeMets package or native data I/O. Use vectorized conditional indexing (e.g., `which(metabolitedata$neg_control==1)`) to identify control metabolite column indices based on metadata annotations. Pass the featuredata and control indices to the normalization function (e.g., `NormQcmets()` with parameters: `method='ruvrandclust'`, `k=1`, `qcmets=control_indices`) and capture the returned list object. Extract the normalized featuredata, computed variation components (e.g., `uvdata`), and metadata from the result list and assign to a new named object (e.g., `uv_ruvrandclust <- list(featuredata=..., uvdata=..., metadata=...)`). This approach ensures reproducibility and enables chaining of downstream analyses.

## Related tools

- **NormalizeMets** (Provides NormQcmets() function to apply ruvrandclust normalization on featuredata using control metabolite indices and parameters (method, k, qcmets); returns list object with normalized data and computed components) — github.com/metabolomicstats/NormalizeMets
- **R** (Environment for matrix operations, conditional indexing (which()), list construction, and data structure manipulation)
- **RStudio** (Recommended IDE for interactive R code execution and data exploration during matrix manipulation workflows)

## Examples

```
neg_control_idx <- which(UVdata$metabolitedata$neg_control==1); uv_ruvrandclust <- NormQcmets(UVdata$featuredata, factors=NULL, method='ruvrandclust', k=1, qcmets=neg_control_idx)
```

## Evaluation signals

- Verify the control_indices vector has length > 0 and all values are valid column indices in featuredata (1 ≤ index ≤ ncol(featuredata))
- Check that the returned normalized featuredata has identical dimensions to input featuredata (same number of rows and columns)
- Confirm that uvdata component (unwanted variation matrix) has the same number of rows as featuredata and a number of columns equal to k or the number of principal components extracted
- Validate that no NaN, Inf, or unexpected missing values were introduced by the normalization; use summary() and is.na() checks
- Verify row names (sample identifiers) and column names (metabolite identifiers) are preserved in the normalized featuredata output

## Limitations

- The skill requires that metabolitedata includes a control status column (e.g., neg_control); if annotations are incomplete or inconsistent, indexing will fail or return incomplete subsets.
- The featuredata matrix must be numeric; non-numeric or mixed-type columns will cause errors during normalization and component extraction.
- Parameters such as k (number of components) and the choice of qcmets (control metabolites vs. all metabolites) are user-specified and require domain knowledge; incorrect specification can yield biologically misleading normalization.
- The skill assumes three-part input structure; datasets with alternative formats (e.g., transposed matrices, single merged tables) require reshaping before the workflow can be applied.

## Evidence

- [other] Load the UVdata dataset (featuredata, sampledata, metabolitedata) into R using the NormalizeMets package: "Load the UVdata dataset (featuredata, sampledata, metabolitedata) into R using the NormalizeMets package."
- [other] Identify negative control metabolites from metabolitedata using the neg_control column (which(UVdata$metabolitedata$neg_control==1)): "Identify negative control metabolites from metabolitedata using the neg_control column (which(UVdata$metabolitedata$neg_control==1))."
- [other] Apply NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization: "Apply NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization with clustering on the UVdata featuredata."
- [other] Extract the normalized featuredata, uvdata (removed unwanted-variation component), and metadata from the returned object and store as uv_ruvrandclust: "Extract the normalized featuredata, uvdata (removed unwanted-variation component), and metadata from the returned object and store as uv_ruvrandclust."
- [readme] featuredata is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as column names: "featuredata which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as"
