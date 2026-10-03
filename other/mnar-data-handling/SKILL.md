---
name: mnar-data-handling
description: Use when you have metabolomics data (targeted LC/MS or untargeted GC/MS)
  with left-censored missing values below the limit of quantification (LOQ) or limit
  of detection (LOD), and you need to impute these values while preserving the underlying
  distributional structure and avoiding bias from.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2269
  tools:
  - R
  - GSimp.R
  - Impute_wrapper.R
  - imputeLCMD (R package)
  - Trunc_KNN
  - glmnet (R package)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: noncommercial
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-SA-4.0
    url: WandeRum/GSimp
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
evidence_spans:
- '**GSimp.R** contains the core functions for GSimp'
- GSimp.R contains the core functions for GSimp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gsimp_cq
    doi: 10.1371/journal.pcbi.1005973
    title: GSimp
  dedup_kept_from: coll_gsimp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1005973
  all_source_dois:
  - 10.1371/journal.pcbi.1005973
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MNAR Data Handling

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

A multi-step preprocessing and imputation pipeline for left-censored metabolomics data where missingness is not random (MNAR), combining log-transformation, quantile-regression initialization, scaling, Gibbs sampling imputation, and recovery transformations to produce complete datasets suitable for downstream analysis.

## When to use

You have metabolomics data (targeted LC/MS or untargeted GC/MS) with left-censored missing values below the limit of quantification (LOQ) or limit of detection (LOD), and you need to impute these values while preserving the underlying distributional structure and avoiding bias from non-random missingness mechanisms.

## When NOT to use

- Data contains missing values that are missing completely at random (MCAR) or missing at random (MAR) — use non-informative bounds (lo=-Inf, hi=Inf) or alternative methods instead of the default left-censored configuration.
- Input is right-censored (detection limit at upper tail) — requires symmetric initialization ('rsym') or different bounds configuration, not the default 'lsym' or 'qrilc' setup.
- Missing values have already been retrieved or manually curated — preprocessing and QRILC initialization may introduce bias on already-detected values.

## Inputs

- R data.frame or matrix with metabolite abundances (rows=samples, columns=metabolites)
- Missing values encoded as NA in the input matrix
- Numeric vector or scalar for lower bound (lo) and upper bound (hi) parameters defining censoring thresholds

## Outputs

- Complete R data.frame with imputed abundance values (no remaining NAs)
- 3D array (data_imp, gibbs_res) recording imputation trajectories across MCMC iterations for specified missing positions
- CSV or R data object of imputed matrix indexed by method name

## How to apply

Apply the pre_processing_GS_wrapper function in sequence: (1) Log-transform raw abundance data to stabilize variance; (2) Initialize missing values using QRILC (quantile regression imputation of left-censored data) to seed the imputation with plausible truncated estimates; (3) Centralize and scale the initialized data to unit variance for elastic-net prediction stability; (4) Reintroduce NA markers at original missing positions, then feed the scaled-initialized matrix into GS_impute with bounds set to lo=-Inf and hi='min' (the minimum of non-missing values per variable, or quantiles like the 10th percentile if minimum is too strict); (5) Run GSimp's Gibbs sampler with recommended iterations (iters_all=10–20, iters_each=50–100) and elastic-net prediction model (imp_model='glmnet_pred'); (6) Recover scaling by reversing centering/scaling parameters, then apply exponential transformation to return to original abundance scale. The pipeline preserves the distributional assumptions of MNAR data by constraining imputed values to fall below the detection threshold.

## Related tools

- **GSimp.R** (Core Gibbs sampler imputation engine; contains GS_impute function that performs MCMC-based left-censored missing value estimation with user-defined bounds and prediction model) — https://github.com/WandeRum/GSimp
- **Impute_wrapper.R** (Dispatcher and wrapper suite; contains pre_processing_GS_wrapper and method-specific wrappers (sim_QRILC_wrapper, sim_trKNN_wrapper, sim_HM_wrapper) for routing data to different imputation backends) — https://github.com/WandeRum/GSimp
- **imputeLCMD (R package)** (Provides impute.QRILC function for quantile-regression-based initialization of left-censored values)
- **Trunc_KNN** (Truncation k-nearest neighbors imputation as alternative MNAR method for comparison; uses Newton-Raphson optimization and Pearson correlation on standardized data) — https://github.com/WandeRum/GSimp
- **glmnet (R package)** (Elastic-net prediction model used within GS_impute (imp_model='glmnet_pred') to predict missing values based on observed metabolite correlations)

## Examples

```
source('GSimp.R'); source('Impute_wrapper.R'); data <- read.csv('untargeted_data.csv', row.names=1); imputed_data <- pre_processing_GS_wrapper(data)
```

## Evaluation signals

- No remaining NA values in output data.frame; all original missing positions have been assigned numeric imputations within the defined bounds.
- Imputed values fall below the specified upper bound (hi='min' or quantile threshold); verify via min(imputed_subset) <= hi for each variable.
- Gibbs sampler convergence: trace plots of gibbs_res show stable posterior means across iterations without drift or divergence; compare early vs. late iterations.
- Distributional recovery: quantile-quantile plots or Kolmogorov-Smirnov tests show that imputed data obey the same truncated distribution as the observed left tail.
- Method comparison: imputation accuracy assessed against held-out synthetic MNAR data (LOQ/LOD retrieval rate, bias in summary statistics) shows GSimp outperforms or matches QRILC and kNN-TN on metabolomics benchmarks.

## Limitations

- Convergence and accuracy depend on iteration counts (iters_all, iters_each); smaller values (iters_all=10, iters_each=50) trade computational speed for potential bias in MCMC chains.
- Method assumes left-censoring (MNAR below detection limit); right-censored data or MCAR/MAR mechanisms require different bounds or initialization strategies.
- Performance is sensitive to initialization quality; QRILC depends on accurate quantile regression estimation, which may fail if missing-data proportion exceeds ~50% per variable.
- Computational cost scales with sample size and missingness; parallel computing (n_cores parameter) mitigates but large untargeted datasets (>1000 metabolites) may require memory optimization.
- Imputed values are plausible synthetic draws, not ground truth; their use in downstream statistical tests may underestimate variance if multiple imputation or Bayesian uncertainty quantification is not performed.

## Evidence

- [intro] GSimp is a gibbs sampler based left-censored missing value imputation approach for metabolomics studies: "GSimp is a gibbs sampler based left-censored missing value imputation approach for metabolomics studies."
- [readme] wrapper functions for different imputation methods (GSimp, QRILC, and kNN-TN): "wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods"
- [readme] pre_processing_GS_wrapper wraps all preprocessing and imputation steps: "All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation. The function will give the final imputed dataset."
- [readme] Log transformation, initialization, scaling, imputation, recovery sequence: "Log-transformation (for non-normal data), Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction), Imputation using GSimp, Scaling recovery,"
- [readme] GS_impute bounds define left-censoring detection limits: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] Iteration counts balance convergence and speed: "Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely"
- [readme] QRILC initialization for left-censored data: "QRILC (Quantile Regression Imputation of Left-Censored data) imputes missing elements randomly drawing from a truncated distribution estimated by a quantile regression"
