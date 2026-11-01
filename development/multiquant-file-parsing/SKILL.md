---
name: multiquant-file-parsing
description: Use when you have Sciex Multiquant text export files from one or more metabolomics or lipidomics analytical sequences and need to identify and locate QCpool (pooled quality control) samples that should have been injected at regular intervals, or when you must validate that the study design's.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Sciex Multiquant (> v3.0.3)
  - ricoderks/QComics
  - Sciex Multiquant
  - QComics
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format
- codecov.io/gh/ricoderks/QComics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics
schema_version: 0.2.0
---

# multiquant-file-parsing

## Summary

Parse Sciex Multiquant text export files to extract sample metadata, injection sequence information, and quality control pool (QCpool) sample positions for metabolomics and lipidomics quality assessment workflows. This skill enables systematic identification and validation of QCpool samples injected at regular intervals across analytical sequences.

## When to use

You have Sciex Multiquant text export files from one or more metabolomics or lipidomics analytical sequences and need to identify and locate QCpool (pooled quality control) samples that should have been injected at regular intervals, or when you must validate that the study design's expected QCpool injection frequency was actually observed in the exported sequence data.

## When NOT to use

- The input is not a Sciex Multiquant text export but another instrument or software's format (e.g., raw .raw files, mzML, or non-Sciex vendor exports).
- You do not have QCpool samples in your study design or experimental sequence.
- The analytical sequence data is already preprocessed into a feature table or peak intensity matrix (use this skill only on raw sequence metadata).

## Inputs

- Sciex Multiquant text export file (txt format)
- Study design specification (expected QCpool injection interval)

## Outputs

- Structured table of detected QCpool samples (columns: sample name, injection index, sequence ID, interval position)
- QCpool interval validation results (detected vs. expected intervals)

## How to apply

Load the Sciex Multiquant text export file and extract the sample metadata and injection sequence information in order. Scan through the injection sequence to identify samples marked or annotated as QCpool or quality control pool samples, recording the injection index (position in sequence), sample name, and any sequence identifier for each detected QCpool. Validate that QCpool samples occur at the regular intervals expected from your study design by computing the differences between consecutive QCpool injection indices. Compile results into a structured table with columns for sample name, injection index, sequence ID, and interval position, which serves as input for downstream quality assessment in tools like QComics.

## Related tools

- **Sciex Multiquant** (Source instrument software that generates the text export file; must be version > 3.0.3 to ensure compatibility with QComics workflow)
- **QComics** (Downstream R/Bioconductor package that consumes parsed QCpool sample tables and sequence metadata to generate quality overview plots and metrics for metabolomics/lipidomics studies) — https://github.com/ricoderks/QComics

## Evaluation signals

- All QCpool samples in the export file are correctly identified and no non-QCpool samples are misclassified as QCpool.
- Injection indices are monotonically increasing and correspond to actual positions in the source text export.
- Interval differences between consecutive QCpool samples match the study design specification (e.g., every 10th injection, every 15th injection); any deviation is flagged.
- The output table has no missing values in required columns (sample name, injection index, sequence ID) and can be successfully loaded by QComics without schema errors.
- Cross-validation: re-reading the output table and spot-checking sample names and indices against the original Multiquant export confirms faithful parsing.

## Limitations

- Parsing assumes QCpool samples are explicitly marked or annotated in the Multiquant export; if naming conventions differ or samples are not labeled, detection may fail or require custom annotation logic.
- The skill detects *actual* QCpool injection positions but does not infer or impute missing QCpool samples if the analytical run deviated from study design; validation will reveal such deviations but cannot correct them.
- No changelog or versioning details for Sciex Multiquant text export schema are available; breaking changes in the Multiquant software format (> v3.0.3) could affect parsing without notice.

## Evidence

- [intro] Sciex Multiquant version requirement and export format: "analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] QCpool injection regularity requirement: "a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences"
- [intro] Purpose and scope of QComics package: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [discussion] Downstream workflow integration: "Source: github:ricoderks__QComics"
