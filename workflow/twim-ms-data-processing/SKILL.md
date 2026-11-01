---
name: twim-ms-data-processing
description: 'Use when you have TWIM-MS data (arrival time and m/z values) from a multi-omic sample and need to: (1) establish a CCS calibration curve from known standards, (2) assign unidentified features to biomolecular classes (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - HinesLab/MOCCal
  - DEIMoS
  - MOCCal
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- HinesLab/MOCCal
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal
schema_version: 0.2.0
---

# twim-ms-data-processing

## Summary

Apply MOCCal to perform collision cross section (CCS) calibration, biomolecular class assignment, and class-specific CCS calculation on traveling-wave ion mobility mass spectrometry (TWIM-MS) data without requiring prior feature identification. This workflow transforms raw or processed TWIM-MS arrival time and m/z measurements into calibrated, class-labeled CCS values suitable for multi-omic profiling.

## When to use

Apply this skill when you have TWIM-MS data (arrival time and m/z values) from a multi-omic sample and need to: (1) establish a CCS calibration curve from known standards, (2) assign unidentified features to biomolecular classes (e.g., lipids, metabolites, peptides) based on physico-chemical properties alone, and (3) compute class-appropriate CCS values for downstream feature matching or annotation. This is particularly valuable when feature identification is unavailable or unreliable at the time of analysis.

## When NOT to use

- Input is already a fully identified and annotated feature table with known compound identities — use direct CCS lookup or library matching instead
- Arrival time data are actually drift time values from drift tube instruments rather than TWIM detector arrival times — clarify instrument platform first
- You require feature-level CCS uncertainty quantification or confidence intervals — MOCCal outputs point estimates without explicit error propagation

## Inputs

- Processed TWIM-MS feature table (UserDT format) with arrival time and m/z values, or raw TWIM-MS data files requiring DEIMoS preprocessing (RawDT format)
- Feature table indexed by feature identifier with columns for arrival time and mass-to-charge ratio (m/z)
- Calibration standard dataset with known CCS reference values

## Outputs

- Calibrated CCS feature table indexed by feature identifier
- Table with columns: feature ID, assigned biomolecular class label, computed class-specific CCS value
- CCS calibration curve model (class-specific, linear or non-linear)

## How to apply

Load your TWIM-MS dataset in either UserDT (processed calibration) or RawDT (raw calibration) format, containing arrival time and m/z columns indexed by feature identifier. Run MOCCal's CCS calibration module on calibrant standards to establish a class-appropriate calibration curve (linear or non-linear). Execute the biomolecular class-assignment algorithm, which classifies each feature based on its arrival time and m/z physico-chemical signature without requiring identification. Finally, apply class-specific CCS calculation using the class label to select and apply the appropriate calibration parameters, converting arrival time to CCS for each feature. Output a structured feature table indexed by feature ID with columns for class label and computed CCS values. Validate output for completeness and correct schema (all features present, no null CCS values, class labels match expected biomolecular categories).

## Related tools

- **DEIMoS** (Preprocessing dependency for RawDT workflow — converts raw TWIM calibration files to processed format prior to MOCCal execution) — http://github.com/pnnl/deimos
- **MOCCal** (Core Python application performing CCS calibration, biomolecular class assignment, and class-specific CCS calculation) — https://github.com/HinesLab/MOCCal

## Examples

```
python MOCCal_UserDT.py --input_file features.csv --calibration_standards calibrants.csv --output_dir ./Output
```

## Evaluation signals

- All input features are present in output table (no dropped rows); output row count equals input row count
- Every feature has a non-null assigned biomolecular class label and computed CCS value; no missing or placeholder entries
- CCS values are within expected range for the assigned class (e.g., lipids typically 200–500 Å², metabolites 100–300 Å², peptides 300–800 Å²)
- Calibration curve R² or goodness-of-fit metric exceeds threshold (typically ≥0.95 for acceptable linear fit) for each class
- Output table schema matches expected structure: indexed by feature ID, with class label and CCS columns; field names and data types are consistent

## Limitations

- Requires either processed UserDT format or installation of DEIMoS v1.3.2 for RawDT processing; no changelog available to track version-specific compatibility or bug fixes
- Biomolecular class assignment relies on physico-chemical properties and may conflate features with overlapping arrival time and m/z signatures across different compound classes
- TWIM platforms record arrival time (detector reach time) rather than drift time (ion residence in mobility cell); software uses these terms interchangeably for convenience, which may cause confusion if raw data are misidentified
- Class-specific CCS calculations assume that calibration standards are representative of the sample classes being analyzed; poor calibrant coverage for a target class may yield inaccurate CCS values

## Evidence

- [readme] MOCCal is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data analysis. Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision"
- [readme] MOCCal offers class assignment and CCS calculations without needing to identify features first, enabling analysis of unidentified multi-omic features.: "Notably, MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [other] The workflow loads TWIM-MS data, runs CCS calibration, executes biomolecular class assignment, and calculates class-specific CCS values.: "1. Load the multi-omic TWIM-MS dataset from a public repository (e.g., MassIVE, MetaboLights, or PRIDE). 2. Run MOCCal's CCS calibration module on the raw TWIM data to establish the calibration"
- [readme] Arrival time and drift time terminology: TWIM platforms record arrival time (detector reach) rather than drift time (ion residence in mobility cell).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [other] Class-specific CCS calculation applies class-appropriate calibration parameters selected by biomolecular class label to convert arrival time to CCS.: "Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature. 3. Convert arrival time to CCS using the"
- [readme] RawDT workflow requires DEIMoS v1.3.2 installation; UserDT workflow requires only the executable and output folder.: "If you plan to use raw calibration files, you will need to install pnnl's DEIMoS, version 1.3.2 (http://github.com/pnnl/deimos)."
