---
name: sample-label-mapping
description: Use when you have a raw peak table (CSV format, from any of 12 supported
  LC-MS software tools or standardized format) and a separate label file that assigns
  each sample to an experimental class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - devtools
  - Biobase
  - readr
  - R base (read.csv, data.frame manipulation)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- '![installed with devtools](https://img.shields.io/badge/installed%20with-devtools-blueviolet.svg)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-label-mapping

## Summary

Create a mapping between peak table samples and their experimental class labels (time-course or multi-class assignments) to enable downstream NOREVA assessment functions to correctly stratify metabolomic data by study design. This step ensures that intensity profiles are paired with their corresponding phenotypic or temporal metadata before preprocessing evaluation.

## When to use

You have a raw peak table (CSV format, from any of 12 supported LC-MS software tools or standardized format) and a separate label file that assigns each sample to an experimental class (e.g., control vs. treatment, or time points in a time-series), and you are preparing data for NOREVA preprocessing assessment or biomarker discovery.

## When NOT to use

- Peak table and labels are already integrated into a single ExpressionSet or SummarizedExperiment object.
- Study design is single-class (no experimental stratification), making label assignment irrelevant.
- Label file structure does not match sample identifiers in the peak table (missing or misaligned samples).

## Inputs

- Peak table (CSV) in format code 1 (standardized NOREVA format) or format code 2 (from 12 LC-MS software tools)
- Label file (CSV) assigning sample identifiers to experimental class or time-course labels

## Outputs

- ExpressionSet object with intensity data in expression matrix, sample-level class/time labels in phenoData, and feature metadata in featureData

## How to apply

Load the peak table and label file using R base functions or readr::read_csv(). Validate that the row count of the label file matches the column count (or sample count) of the peak table. For each sample identifier in the peak table, verify a corresponding label assignment exists. Construct a Biobase ExpressionSet object, placing sample identifiers and their class/time-series labels into the phenoData slot so that downstream NOREVA functions (normulticlassqcall, nortimecourseqcall, etc.) can access the experimental design. This pairing is essential because NOREVA's five assessment criteria depend on knowing which samples belong to which study condition or time point.

## Related tools

- **Biobase** (Construct ExpressionSet object to link peak intensities with sample phenotype (class/time labels) and feature metadata) — https://bioconductor.org/packages/release/bioc/html/Biobase.html
- **readr** (Load CSV peak table and label file with type inference and validation)
- **R base (read.csv, data.frame manipulation)** (Alternative file I/O and label-to-sample mapping) — https://www.r-project.org/

## Examples

```
PrepareInuputFiles(dataformat=1, rawdata='peak_table.csv', label='sample_labels.csv')
```

## Evaluation signals

- Row count of label file equals the number of samples (columns) in peak table intensity matrix.
- All sample identifiers in peak table have a corresponding entry in label file with no NA or missing values.
- ExpressionSet object successfully constructs with no errors; phenoData slot contains class/time-series labels; expression matrix and phenoData have matching column/row counts.
- Downstream NOREVA functions (e.g., normulticlassqcall) accept the ExpressionSet without validation errors and correctly stratify samples by class.
- Feature metadata (m/z, retention time, or software-specific columns) is preserved in featureData slot.

## Limitations

- Requires exact one-to-one correspondence between sample identifiers in peak table and label file; misaligned or duplicate sample names will cause ExpressionSet construction to fail.
- Label file must be manually created or exported from study metadata; no automated label inference from raw data is provided.
- NOREVA's five assessment criteria assume labels correctly represent the true experimental design; mislabeled samples will bias preprocessing evaluation and downstream biomarker ranking.
- Format code 2 (12 software tool formats) requires careful parsing; column headers and sample ID positions vary by tool, and incorrect format specification will lead to structural validation failures.

## Evidence

- [other] PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for time-course/multi-class studies: "PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for"
- [other] Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels: "Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels"
- [other] Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to featureData: "Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to"
- [readme] label – This variable allows the user to indicate the NAME of their input label file for time-course/multi-class: "label – This variable allows the user to indicate the NAME of their input label file for time-course/multi-class"
- [readme] five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion"
