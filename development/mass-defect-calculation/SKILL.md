---
name: mass-defect-calculation
description: Use when processing feature lists from LC- or GC-HRMS data (in mzML format or as custom feature tables with m/z and molecular formula columns) and you need to flag potential PFAS candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pyOpenMS
  - PFΔScreen
  - MSConvert
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
---

# mass-defect-calculation

## Summary

Mass defect calculation is a quantitative technique for identifying PFAS-like features in non-target HRMS data by computing the difference between observed m/z values and theoretical exact masses. It serves as a foundational metric for downstream PFAS prioritization filters including MD/C ratio normalization and Kendrick mass defect analysis.

## When to use

Apply this skill when processing feature lists from LC- or GC-HRMS data (in mzML format or as custom feature tables with m/z and molecular formula columns) and you need to flag potential PFAS candidates. Mass defect calculation is the necessary first step before applying MD/C-m/C ratio filtering or Kendrick mass defect (KMD) analysis for PFAS homologue clustering.

## When NOT to use

- Input feature list lacks assigned molecular formulas—mass defect calculation requires formula to compute theoretical exact mass; use formula assignment tools first.
- Data are from targeted MS/MS experiments with pre-selected PFAS compounds—mass defect filtering is designed for non-target screening and adds no value when analytes are already known.
- Input is low-resolution MS data (e.g., unit mass resolution)—mass defect calculations depend on high-resolution m/z accuracy (typical HRMS: <5 ppm); results become unreliable below ~0.005 Da precision.

## Inputs

- Feature list (CSV/TSV or Excel) with required columns: m/z (observed mass-to-charge ratio), molecular formula (e.g., 'C8H5F13O2'), optional: retention time, intensity
- mzML raw data file (centroided spectra from LC-HRMS or GC-HRMS, data-dependent acquisition) corresponding to the feature list

## Outputs

- Annotated feature table (Excel format) with appended columns: exact_mass, mass_defect, MD/C_ratio, PFAS_prioritization_flag
- MD/C-m/C scatter plot (interactive HTML) showing mass defect vs. m/z with color coding by MD/C score
- m/C histogram (interactive HTML) showing distribution of MD/C values across features

## How to apply

For each feature in the input list, retrieve its observed m/z value and assigned molecular formula. Using standard atomic masses (e.g., C=12.0000, H=1.00783, F=18.99840), calculate the exact theoretical mass for that molecular formula. Compute mass defect as (observed m/z − exact mass). If normalizing by carbon count (MD/C approach), divide the mass defect by the number of carbon atoms in the formula to obtain the MD/C ratio, which is more consistent across homologous series. The mass defect calculation leverages the fact that PFAS compounds, enriched in fluorine and carbon with characteristic heteroatom compositions, exhibit elevated and systematic mass defects compared to common organic contaminants. Apply user-specified MD/C thresholds (e.g., to flag features as PFAS-like) and output the annotated feature table with mass defect and MD/C scores for visual inspection (MD/C-m/C scatter plots) and downstream prioritization.

## Related tools

- **pyOpenMS** (Feature detection in MS raw data; provides m/z values and retention times for input to mass defect calculation) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (Host application implementing mass defect calculation as the foundation for MD/C-m/C and KMD prioritization filters; generates annotated feature tables and visualization plots) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Converts vendor-specific MS raw formats (e.g., .raw, .d) to vendor-independent mzML for use in PFΔScreen and mass defect workflows)

## Evaluation signals

- Output mass defect values are within expected range for organic compounds (typically −0.3 to +0.3 Da for small molecules); PFAS features exhibit elevated mass defects (>0.1 Da) due to fluorine enrichment.
- MD/C ratios for homologous PFAS series (differing by CH₂ units) cluster within a narrow band (<0.005 Da per carbon) on scatter plots, confirming consistent normalization by carbon count.
- Comparison of mass defects calculated in-house against PFΔScreen output for a test feature list (sample or external_feature_list.xlsx) yields exact agreement within floating-point tolerance (±1e-6 Da).
- Features flagged as PFAS-like by MD/C threshold (e.g., MD/C > user-specified cutoff) show visual overlap with known PFAS reference compounds when plotted on the MD/C-m/z scatter; blank-corrected features and sample features separate clearly.
- MD/C histogram shows bimodal or multimodal distribution with a distinct high-MD/C peak (PFAS candidates) separated from a main low-MD/C population (background organics), validating threshold selection.

## Limitations

- Mass defect calculation requires accurate molecular formula assignment; incorrect formulas produce misleading mass defects and false PFAS prioritization. Formula assignment errors propagate through downstream MD/C filtering.
- High-resolution mass accuracy is critical; typical HRMS achieves <5 ppm error, but instrumental drift, calibration issues, or low signal-to-noise features can inflate mass defect uncertainties and reduce discriminatory power.
- Elemental composition alone (mass defect) is not PFAS-specific; other halogenated or heavily oxygenated compounds may exhibit elevated mass defects. MD/C filtering is a preliminary screen; confirmation requires MS2 fragment analysis or reference standards.
- MD/C approach assumes uniform fluorine content and carbon backbone across a feature series; atypical PFAS structures (e.g., partially fluorinated, branched, or with unusual heteroatoms) may not follow expected MD/C clustering patterns.
- Custom feature lists with missing or inconsistent molecular formulas will fail or produce incomplete annotation; quality control and formula validation are prerequisites.

## Evidence

- [other] Calculate exact mass for each molecular formula using standard atomic masses: "Calculate exact mass for each molecular formula using standard atomic masses"
- [other] Mass defect is observed m/z minus exact mass: "Compute mass defect (observed m/z minus exact mass) for each feature"
- [other] MD/C normalizes by carbon count: "Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value"
- [other] MD/C-m/C approach is one prioritization technique for PFAS: "The MD/C-m/C approach is one of several prioritization techniques implemented in PFΔScreen for identifying potential PFAS features from non-target HRMS data"
- [readme] pyOpenMS used for feature detection providing m/z input: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] Custom feature lists can be included with required m/z columns: "Optionally, custom feature lists can be included"
- [readme] MD/C histogram output visualization: "several interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot, a m/z vs. RT plot (with and without MS2 raw data), a KMD vs. m/z"
- [readme] mzML format requirement with data-dependent acquisition: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor"
