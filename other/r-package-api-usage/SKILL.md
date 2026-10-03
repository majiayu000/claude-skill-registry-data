---
name: r-package-api-usage
description: Use when you have tabular metabolomics data (tab-delimited or Sciex OS format) and need to apply a specialized R package's analysis pipeline—such as mzQuality—that requires sequential function calls (readData → buildExperiment → doAnalysis) to construct, validate, and transform experiment objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  - xcms
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
---

# R Package API Usage

## Summary

Programmatically invoke R package functions in sequence to transform input data through a package's public API, leveraging type-aware objects (e.g., SummarizedExperiment) to chain operations and extract results. This skill is essential when a domain-specific R package provides a documented interface for reproducible, multi-step analysis pipelines.

## When to use

You have tabular metabolomics data (tab-delimited or Sciex OS format) and need to apply a specialized R package's analysis pipeline—such as mzQuality—that requires sequential function calls (readData → buildExperiment → doAnalysis) to construct, validate, and transform experiment objects. Use this skill when the package's public API is the primary means of interaction and the input data structure is known to match the package's documented schema.

## When NOT to use

- Input is already a pre-processed SummarizedExperiment object—skip readData() and buildExperiment() and call doAnalysis() directly.
- You only need to read and inspect the raw data without running quality control metrics or batch correction; use readData() alone.
- The metabolomics data lacks pooled QC samples; batch-correction and RSDQC-based internal standard recommendation will not function meaningfully.

## Inputs

- Tab-delimited text file (TSV) with mandatory columns: compound identifier, sample identifier, internal standard assignment, measurement area
- Sciex OS text export files
- Data frame with validated column structure from readData()

## Outputs

- SummarizedExperiment object with assays (e.g., 'primary', 'ratio', 'ratio_corrected'), rowData (compound-level quality metrics: RSDQC, background %, presence, use flag), and colData (sample-level metadata: batch, sample type, outlier status, use flag)
- Excel export containing all assays, rowData, colData, and categorized compound confidence labels (High Confidence, Caution, Low SNR)

## How to apply

Load the R package library and identify the input file format (tab-delimited text or Sciex OS export). Call readData() to validate mandatory columns (e.g., compound, sample, area columns) and catch format errors early. Pass the resulting data frame to buildExperiment() to construct a SummarizedExperiment object, which internally organizes compounds as rows, samples as columns, and numeric assays (e.g., 'primary', 'ratio'). Call doAnalysis() on the experiment object to apply the full pipeline: compute compound/internal-standard ratios, perform batch correction using pooled QC samples, calculate background signal and matrix effects, and generate quality-control metrics (e.g., RSDQC, presence flags). Extract results from assay(), rowData(), and colData() slots of the returned experiment object. The rationale is that SummarizedExperiment enforces consistent indexing across assays and metadata, preventing silent misalignment of samples or compounds during multi-step transformations.

## Related tools

- **mzQuality** (Primary R package providing readData(), buildExperiment(), doAnalysis(), and plotting functions for metabolomics quality control and batch correction) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor class used internally by mzQuality to store and organize compound assays, row metadata (compounds), and column metadata (samples))
- **mzQualityDashboard** (Shiny application wrapper around mzQuality API for interactive use without R programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **xcms** (R package often used upstream in metabolomics pipelines; mzQuality accepts its output as input)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality")
exp <- buildExperiment(readData(path))
exp <- doAnalysis(exp = exp)
exp <- exp[rowData(exp)$use, exp$use]
head(assays(exp)[["ratio_corrected"]])
```

## Evaluation signals

- readData() completes without errors and returns a data frame with all mandatory columns (compound, sample, internal standard, area); check nrow() and ncol() match expected dimensions.
- buildExperiment() successfully constructs a SummarizedExperiment object with non-empty assays, rowData containing compound identifiers, and colData containing sample identifiers and batch information.
- doAnalysis() adds new assay columns ('ratio', 'ratio_corrected', 'background_percent', 'matrix_effect') and rowData columns ('RSDQC', 'presence', 'use') without throwing errors; verify using names(assays(exp)) and colnames(rowData(exp)).
- ratio assay equals primary assay values when secondaryAssay is not provided (default divisor of 1); element-wise comparison: all.equal(assays(exp)[['ratio']], assays(exp)[['primary']]) should return TRUE.
- Final rowData$use and colData$use flags are logical (TRUE/FALSE); manual override of these flags before createReports() filters compounds and samples as expected in the output HTML and Excel files.

## Limitations

- Only one sample type can be used for calculating absolute concentrations in the current version; if multiple sample types with different calibration lines are required, this limitation will not be addressed until a future version.
- mzQuality requires a strictly formatted input (mandatory columns: compound, sample, internal standard, measurement area); missing or misnamed columns will cause readData() to fail.
- Batch-correction and RSDQC-based internal-standard recommendations depend on the presence of pooled study quality control (SQC) samples; datasets without QC samples will not benefit from these features.
- The Rosner Test for outlier detection in QC samples may yield false positives or negatives if QC sample size is very small or the distribution is non-normal.

## Evidence

- [readme] Input data format requirement: "To use your own data, either a SummarizedExperiment or a tab-delimited text file can be used. See the vignette [Data input]"
- [readme] Core API workflow: "path <- system.file("extdata", "example.tsv", package = "mzQuality")
exp <- buildExperiment(readData(path))"
- [readme] readData() function purpose and validation: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format."
- [readme] SummarizedExperiment as core object: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns. This is the object that mzQuality uses to perform all"
- [readme] doAnalysis() pipeline steps and outputs: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
- [readme] Results stored in experiment slots: "All calculations will be added to the `assay`, `rowData` and `colData` slots of the experiment, or overwrite the values if they are already present."
- [other] Secondary assay default behavior: "When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values."
- [readme] Quality control metric thresholds: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
