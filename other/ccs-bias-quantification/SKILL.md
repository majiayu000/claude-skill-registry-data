---
name: ccs-bias-quantification
description: Use when you have IM-MS lipidomics data acquired on samples spiked with fully labeled U13C lipid standards (e.g., U13C yeast extract), and you need to assess whether systematic CCS deviation exists between your instrument's measured values and the DT CCS N2 reference library for U13C labeled lipids.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MobiLipid
  - ggplot2
  - data.table
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
---

# ccs-bias-quantification

## Summary

Quantify systematic collision cross section (CCS) bias in ion mobility-mass spectrometry lipidomics data by comparing measured CCS values of U13C-labeled internal standards against a validated DT CCS N2 reference library. This skill enables internal standardization-based quality control without additional external calibration.

## When to use

Apply this skill when you have IM-MS lipidomics data acquired on samples spiked with fully labeled U13C lipid standards (e.g., U13C yeast extract), and you need to assess whether systematic CCS deviation exists between your instrument's measured values and the DT CCS N2 reference library for U13C labeled lipids. Use it as a prerequisite step before CCS correction or when validating CCS quality across lipid classes.

## When NOT to use

- Input lipidomics data lacks U13C-labeled internal standard lipids — the skill requires heavy-labeled reference compounds for bias calculation.
- You are processing non-lipidomics IM-MS data (e.g., metabolomics, proteomics) without a validated CCS reference library for your analyte class.
- Your CCS values are already corrected or normalized by vendor software — bias quantification is meaningful only on raw measured CCS data.

## Inputs

- IM-MS lipidomics data (.csv) with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), measured CCS value
- DT CCS N2 reference library for U13C labeled lipids (.csv) containing lipid species, lipid class, adduct, and theoretical CCS N2 values
- Sample must contain U13C-labeled internal standards (fully labeled lipid extract)

## Outputs

- CCS bias table (.csv) with measured CCS, reference CCS, calculated bias (absolute and/or percentage), by lipid species and class
- Summary statistics (.csv) of mean bias, standard deviation, and range aggregated by lipid class and adduct combination
- Bias visualization report (.html, .pdf) with class-level and adduct-specific bias distributions (box plots, violin plots, scatter plots)
- RData file containing all intermediate results and metrics as an R list object

## How to apply

Load your IM-MS lipidomics data and the DT CCS N2 library for U13C labeled lipids into R. Map detected lipid features to reference library entries by matching lipid species nomenclature, lipid class, and adduct form. For each matched U13C lipid, calculate bias as the absolute or percentage difference between your measured CCS value and the library CCS value. Aggregate bias metrics by lipid class and adduct combination, computing mean bias, standard deviation, and range. Generate summary statistics and visualizations (e.g., box plots, violin plots, heatmaps) to reveal systematic deviation patterns and class-level bias distribution. A minimum of 1–3 U13C lipids per lipid class-adduct combination is sufficient for effective bias estimation, though more lipids improve stability of downstream correction models.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias calculation and optional bias correction for IM-MS lipidomics) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Programming language and environment for loading data, matching to library, computing bias metrics, and generating visualizations)
- **ggplot2** (R package for generating publication-quality bias distribution visualizations)
- **data.table** (R package for efficient aggregation of bias statistics by lipid class and adduct)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_results.html', 'MobiLipid_CCS-bias-calculation_results.pdf'))
```

## Evaluation signals

- Verify that all detected U13C lipids in the input data successfully matched to the DT CCS N2 library by lipid species, class, and adduct; report the number and percentage of matched versus unmatched features.
- Check that CCS bias values fall within expected ranges (typically ±2–3% for well-calibrated instruments) and that mean bias per lipid class is reported with non-zero standard deviation, indicating biological/technical variation rather than missing data.
- Confirm that summary statistics tables include counts of U13C lipids per lipid class-adduct combination; classes with fewer than 1–3 lipids should be flagged as having low statistical power.
- Validate that visualizations (violin plots, heatmaps) clearly show bias distribution shape and identify outlier lipids or classes with systematically large deviations that may warrant instrument maintenance or re-calibration.
- Cross-check that bias calculation formula (e.g., (measured − reference) / reference × 100) is correctly applied and consistently used across all lipid features and output tables.

## Limitations

- CCS bias quantification is restricted to lipid classes and adducts present in the DT CCS N2 library; unmapped lipids cannot be assessed. The supported lipid classes with CCS reference values are: AcCa, Cer, Co, DG, HexCer, LPC, LPE, PA, PC, PE, PG, PI, PS, SPH, TG.
- Bias estimation quality depends on the number and diversity of U13C lipids detected per lipid class-adduct combination; insufficient lipids (< 1) in a class will yield unreliable class-level bias statistics.
- The workflow assumes your IM-MS instrument has been subject to vendor-specific CCS calibration (e.g., Agilent, Waters, Bruker); additional external calibration compounds beyond vendor protocols are not required but may improve bias estimates if available.
- Systematic CCS bias may be driven by instrument drift, ion source conditions, or adduct-specific ion mobility properties; the skill quantifies bias but does not diagnose its root cause.
- Linear regression-based CCS correction (available as a companion skill) requires a minimum of 3 lipids per lipid class-adduct combination, which may not always be achievable, limiting subsequent correction scope.

## Evidence

- [other] MobiLipid performs CCS bias assessment through a R Markdown workflow that integrates a newly established DT CCS N2 library for U13C labeled lipids, enabling internal standardization-based bias calculation: "MobiLipid performs CCS bias assessment through a R Markdown workflow that integrates a newly established DT CCS N2 library for U13C labeled lipids, enabling internal standardization-based bias"
- [other] Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values: "Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values. 4. Aggregate bias metrics by lipid class and generate summary"
- [other] MobiLipid enables effective CCS bias calculation and correction while requiring only a low number of lipids detected per lipid class: "MobiLipid enables effective CCS bias calculation and correction while requiring only a low number of lipids detected per lipid class."
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract): "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract (Neubauer et al. 2012))."
- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization."
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DT CCS N2 library values as y value: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DT CCS N2 library values as y value."
