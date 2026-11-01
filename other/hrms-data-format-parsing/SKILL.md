---
name: hrms-data-format-parsing
description: Use when you have raw or processed HRMS/MS data from Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, or SCIEX Q-TOF instruments in formats such as mzML, CSV peaklists, or vendor-specific formats, and you need to extract experimental fragment m/z values and their intensities for comparison against.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Q-Exactive orbitrap
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data
- Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# hrms-data-format-parsing

## Summary

Parse and load experimental high-resolution tandem mass spectrometry (HRMS/MS) data from instrument-specific file formats (mzML, CSV peaklists, vendor formats) into a standardized in-memory representation suitable for fragment m/z matching and lipid identification workflows. This skill bridges raw instrument output to downstream lipidomics analysis.

## When to use

You have raw or processed HRMS/MS data from Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, or SCIEX Q-TOF instruments in formats such as mzML, CSV peaklists, or vendor-specific formats, and you need to extract experimental fragment m/z values and their intensities for comparison against in-silico lipid fragmentation libraries.

## When NOT to use

- Input is already a vendor-independent, harmonized peaklist or feature table from peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer); use that output directly.
- Data is from Waters UHPLC-HRMS/MS instruments; LipidMatch does not currently support Waters files.
- Raw m/z values have already been matched to library fragments; this skill applies only to raw or minimally processed experimental data.

## Inputs

- mzML files from Q-Exactive or Q-TOF UHPLC-HRMS/MS
- CSV peaklist files (Q-Exactive or Q-TOF format) with m/z and intensity columns
- Vendor-specific raw files or vendor-converted CSV exports

## Outputs

- Structured peaklist table (m/z, intensity, optional: retention time, charge state)
- In-memory array of experimental fragment m/z values
- Validated peaklist ready for downstream m/z matching and lipid identification

## How to apply

Load experimental peaklist files in CSV or mzML-derived table format containing m/z and intensity pairs from your HRMS/MS instrument (Q-Exactive orbitrap or Q-TOF platforms). Parse the file headers and data columns to extract fragment m/z values and associated metadata. Ensure mass values are in the same mass tolerance units (typically ppm or Da) that will be used in the downstream m/z matching step. Validate that the parsed m/z range and intensity distribution are consistent with the acquisition method (targeted, data-dependent MS/MS top-N, or all-ion fragmentation). Output a structured table or in-memory array of m/z–intensity pairs ready for matching against the LipidMatch in-silico library.

## Related tools

- **MZmine** (Peak picking and peaklist generation from raw HRMS/MS data; produces CSV or other formats compatible with LipidMatch input)
- **XCMS** (Centroiding and peak detection from mzML or netCDF; exports peaklist for m/z matching workflows)
- **MS-DIAL** (Peak picking and spectral deconvolution for HRMS/MS data; generates peaklists for downstream matching)
- **Compound Discoverer** (Commercial peak picking and annotation software compatible with LipidMatch input format)
- **Q-Exactive orbitrap** (Thermo HRMS/MS instrument producing mzML and vendor-format files containing experimental fragment m/z data)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Agilent TOF instrument generating peaklists and raw files with fragment m/z values)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Bruker TOF instrument producing raw and converted peaklist formats for fragment matching)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (SCIEX TOF instrument generating peaklists compatible with LipidMatch input specifications)

## Evaluation signals

- Parsed peaklist contains m/z values in expected range (typically 100–1200 m/z for lipidomics), with no missing or corrupted entries.
- Intensity values are positive and span a reasonable dynamic range (e.g., 1e4 to 1e8 for orbitrap data); no negative or zero intensities in valid peaks.
- Header row and column mapping are correctly identified; optional metadata (retention time, charge state) are present and non-null where expected.
- Parsed data structure matches the input format specification (e.g., CSV with columns [m/z, intensity, ...] or mzML scan-level m/z–intensity arrays).
- Data integrity check: file size, row count, and column count are consistent; no truncated or corrupted records detected.

## Limitations

- Waters UHPLC-HRMS/MS files are not currently supported by downstream LipidMatch matching; data from Waters instruments cannot proceed in this workflow.
- mzML parsing requires correct mzML format compliance; malformed or non-standard mzML variants may fail to parse correctly.
- CSV peaklist parsing is format-dependent; inconsistent column headers, delimiters, or decimal formats across vendor implementations may cause parsing errors.
- Mass calibration errors in raw data are not corrected during parsing; ensure instrument mass calibration is adequate before file acquisition.

## Evidence

- [other] Load experimental fragment m/z values from a peaklist file (Q-Exactive or Q-TOF format, e.g., CSV or mzML-derived table): "Load experimental fragment m/z values from a peaklist file (Q-Exactive or Q-TOF format, e.g., CSV or mzML-derived table)"
- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries"
- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches, as well as Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer): "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
