---
name: qcpool-cv-calculation
description: Use when you have Sciex Multiquant txt exports containing signal intensities from QCpool samples injected at regular intervals (e.g., every 10–20 samples) during one or more analytical sequences in a metabolomics or lipidomics study.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3391
  tools:
  - QComics
  - Sciex Multiquant
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study
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

# qcpool-cv-calculation

## Summary

Calculate per-compound coefficient of variation (CV) from pooled quality control (QCpool) sample intensities measured at regular intervals during a metabolomics or lipidomics sequence. CV quantifies technical reproducibility and is a primary metric for assessing data quality before downstream analysis.

## When to use

Apply this skill when you have Sciex Multiquant txt exports containing signal intensities from QCpool samples injected at regular intervals (e.g., every 10–20 samples) during one or more analytical sequences in a metabolomics or lipidomics study. Use it as a prerequisite step to generate a quality overview and to identify compounds with unacceptable technical variability that may compromise study validity.

## When NOT to use

- Input data are not from pooled QC samples (e.g., single-injection or non-replicated samples); CV calculation requires multiple measurements of the same biological or chemical composition.
- Signal intensities have not been corrected for detector saturation, baseline drift, or instrumental calibration artifacts; CV may be inflated by instrumental rather than biological/chemical variation.
- QCpool samples were not injected at regular intervals during the sequence; isolated or clustered QCpool measurements limit trend detection and may yield unrepresentative CV estimates.

## Inputs

- Sciex Multiquant txt export file containing QCpool sample results
- QCpool positional data table (compound identifiers, injection sequence order, signal intensities)

## Outputs

- Per-compound coefficient of variation (CV) values (%)
- Summary table of CV results indexed by compound, with pass/fail quality status
- Optional: visualization (e.g., histogram or dot plot) highlighting compounds with acceptable vs. poor reproducibility

## How to apply

Load the QCpool positional table exported from Sciex Multiquant (version > v3.0.3) in txt format. Parse compound identifiers and extract signal intensity values across all sequential QCpool injections within the sequence. For each compound, calculate the coefficient of variation as CV = (standard deviation of intensities / mean intensity) × 100%. Aggregate CV results by compound and compare against study-specific acceptance thresholds (e.g., typically CV < 20–30% for metabolomics). Flag compounds with CV exceeding the threshold as candidates for exclusion or investigation of instrumental drift during the sequence.

## Related tools

- **Sciex Multiquant** (Acquires and exports QCpool sample signal intensities in txt format; provides the input file required for CV calculation)
- **QComics** (Downstream package that aggregates per-compound CV values and signal-trend metrics into quality overview summaries and visualizations for rapid metabolomics/lipidomics study quality assessment) — https://github.com/ricoderks/QComics

## Evaluation signals

- CV values are positive, finite numbers (0–∞%; typical acceptance range 0–30% for metabolomics), with no NaN, infinite, or negative results.
- Per-compound CV is calculated from ≥2 QCpool intensity measurements; sample size and degree of freedom are documented or traceable.
- CV summary table is indexed consistently by compound identifier and matches the total number of unique compounds in the input file.
- Compounds flagged as 'poor quality' (CV exceeding threshold) are reproducible when CV is recalculated independently; no arithmetic or parsing errors in intensity extraction.
- Temporal trend in CV (e.g., early vs. late in sequence) can be stratified; if CV increases over sequence, it aligns with signal-trend metrics indicating instrumental drift.

## Limitations

- CV is sensitive to low absolute signal intensities; near-limit-of-detection (LOD) compounds may show artificially high CV due to baseline noise, not true biological/chemical variability.
- CV does not directly measure instrumental drift or signal degradation; slope and trend metrics are required in parallel to distinguish between random analytical noise and systematic instrumental drift.
- QCpool composition (single pooled aliquot vs. re-created pools across sequences) affects interpretation; CV from a single prepared pool reflects analytical reproducibility, while CV from independent pool preparations may reflect both analytical and biological/preparatory variation.
- File format dependency: only Sciex Multiquant txt exports (version > v3.0.3) are explicitly supported; other vendor formats or older Multiquant versions require re-export or format conversion before input to this skill.

## Evidence

- [intro] QCpool samples analyzed with Sciex Multiquant and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [other] CV is calculated as a measure of technical reproducibility: "Calculate per-compound coefficient of variation (CV) as a measure of technical reproducibility"
- [intro] QCpool samples injected at regular intervals during sequences: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [other] QComics generates quality overview report from CV and trend results: "Aggregate CV and trend results into a summary table or visualization highlighting compounds with acceptable vs. poor quality metrics"
- [intro] QComics goal is quick overview of study quality: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
