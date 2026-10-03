---
name: r-package-api-usage
description: Use when when you have metabolomics data (tab-delimited text or SummarizedExperiment
  object) and need to apply batch correction, outlier detection, internal standard
  recommendation, and quality filtering at scale or in non-interactive workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - xcms
  - mzQualityDashboard
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Package API Usage

## Summary

Programmatically invoke R package functions to perform metabolomics quality control analyses and generate standardized reports. This skill encompasses reading data, building experiment objects, executing analysis pipelines, and exporting results through mzQuality's documented API.

## When to use

When you have metabolomics data (tab-delimited text or SummarizedExperiment object) and need to apply batch correction, outlier detection, internal standard recommendation, and quality filtering at scale or in non-interactive workflows. Use this skill when makeSummaryReport and makeCompoundReport flags must be set programmatically to control report output types.

## When NOT to use

- Input data lacks mandatory columns (compound ID, aliquot/sample name, assay area values, sample type) or cannot be coerced to SummarizedExperiment format.
- Analysis requires interactive exploration or real-time parameter tuning; use mzQualityDashboard Shiny application instead.
- No Quality Control (QC) samples are present in the dataset; Rosner outlier test and batch correction rely on pooled QC replicates.

## Inputs

- Tab-delimited text file (Sciex OS export or user-formatted with compound, aliquot, assay, type columns)
- SummarizedExperiment object (from existing R-based pipeline, e.g., xcms)
- Pre-analyzed experiment object (result of doAnalysis)

## Outputs

- SummarizedExperiment object with added assays (ratio, ratio_corrected, background %, matrix effect, RSD_QC, median area, presence)
- rowData slot with use (TRUE/FALSE) column and compound reliability flags (High Confidence, Caution, Low SNR)
- colData slot with use column and sample outlier status
- Project folder containing Plots/ (visualization PNGs/PDFs), Reports/ (HTML summary and compound reports, tab-delimited matrices), and Excel workbook

## How to apply

Load metabolomics data using readData() to validate column structure (mandatory: compound, aliquot, assay, type columns); construct a SummarizedExperiment via buildExperiment(); invoke doAnalysis() with threshold parameters (RSDQC, background signal %, QC presence) to compute batch-corrected ratios, detect outliers via Rosner Test on QC samples, and flag unreliable compounds; subset using rowData(exp)$use and exp$use to retain high-confidence results; call createReports() with makeSummaryReport=TRUE and makeCompoundReport=TRUE to export a Project folder with Plots/ and Reports/ subdirectories containing HTML visualizations, tab-delimited matrices (assays, rowData, colData), and Excel workbook.

## Related tools

- **mzQuality** (Primary R package providing readData(), buildExperiment(), doAnalysis(), and createReports() API functions for quality control analysis) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor class for storing assay data, row metadata (compounds), and column metadata (samples/aliquots) used internally by mzQuality) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **xcms** (R-based metabolomics preprocessing pipeline that outputs SummarizedExperiment objects compatible with mzQuality input)
- **mzQualityDashboard** (Interactive Shiny application wrapper around mzQuality API for users without R programming experience) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- doAnalysis(buildExperiment(readData(path))); exp <- exp[rowData(exp)$use, exp$use]; createReports(exp, makeSummaryReport=TRUE, makeCompoundReport=TRUE, dir="./analysis_output")
```

## Evaluation signals

- SummarizedExperiment object contains new assay matrices (ratio, ratio_corrected, background_percent, matrix_effect, rsd_qc, median_area, presence) matching sample count and compound count
- rowData includes use column with all TRUE or FALSE values; compounds marked FALSE have RSDQC > threshold, background % > threshold, or < presence threshold
- colData includes use column; QC samples marked FALSE are identified as statistical outliers by Rosner Test on compound/IS ratios
- Project folder exists with Plots/ and Reports/ subdirectories; Reports/ contains summary and compound HTML files; tab-delimited files (assays.tsv, rowData.tsv, colData.tsv) are readable and match SummarizedExperiment dimensions
- Excel workbook generated contains sheets for each assay, rowData, and colData with no missing values in key columns (compound ID, sample ID, ratios, flags)

## Limitations

- Requires pooled Quality Control (QC) samples; analysis will not perform outlier detection or reliable batch correction without QC replicates.
- Tab-delimited input must have exact column names and format; readData() validation is strict and will reject malformed files.
- Internal Standard assignment must be pre-specified; mzQuality recommends standards but does not automate selection if multiple candidates exist.
- Batch correction assumes systematic variation; if batch effect is sample-type-dependent or non-linear, results may be suboptimal.
- No changelog provided in repository; API stability and parameter names across versions are not documented.

## Evidence

- [readme] buildExperiment and doAnalysis workflow: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format. Finally, the"
- [readme] doAnalysis steps and outputs: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
- [other] createReports output structure: "createReports generates a Project folder organized into Plots and Reports subdirectories containing analysis results, including summary reports, compound reports, and tab-delimited text files for"
- [readme] SummarizedExperiment selection workflow: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [readme] Outlier detection and sample filtering: "It bases the decision for samples on the outcome of the Rosner Test, which tests for statistical outliers in QC samples."
- [intro] Input data format requirement: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports"
