---
name: mzml-file-parsing
description: Use when you have raw LC- or GC-HRMS data from vendor instruments (ESI or APCI ionization) that needs to be converted to a vendor-neutral format for non-target screening, or you already have mzML files that require loading into a Python environment for downstream feature detection and MS2 spectral.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
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

# mzml-file-parsing

## Summary

Parse vendor-independent centroided mzML files using pyOpenMS to ingest high-resolution mass spectrometry raw data in a standardized, platform-agnostic format suitable for automated feature detection and PFAS prioritization workflows.

## When to use

You have raw LC- or GC-HRMS data from vendor instruments (ESI or APCI ionization) that needs to be converted to a vendor-neutral format for non-target screening, or you already have mzML files that require loading into a Python environment for downstream feature detection and MS2 spectral analysis.

## When NOT to use

- Input is already a feature table (xlsx, CSV) with pre-extracted m/z, RT, and intensity — use external feature list import instead.
- Raw data is in profile (centroid-like but not centroided) format without explicit centroid annotation — pyOpenMS feature detection expects true centroided spectra; profile data may produce spurious or low-confidence features.
- mzML file lacks MS2 data (MS1-only or survey scan data) and diagnostic fragment matching is required for PFAS prioritization — MS2 spectra are essential for the fragment mass difference and diagnostic fragment filtering steps.

## Inputs

- vendor raw mass spectrometry data file (Thermo .raw, Waters .raw, Bruker .d, or equivalent)
- centroided mzML file (generated via MSConvert or equivalent conversion tool)
- optional: blank/control mzML file for blank correction

## Outputs

- pyOpenMS MSExperiment object (in-memory representation of MS1 and MS2 spectra)
- parsed MS1 spectra with m/z, retention time, and intensity arrays
- parsed MS2 spectra with precursor m/z, product m/z, and intensity information

## How to apply

Use pyOpenMS MSExperiment reader to load centroided mzML files that have been acquired under data-dependent acquisition (ddMS2) with centroided spectra. The mzML format can be generated from vendor raw files using MSConvert (e.g., from Thermo .raw or other proprietary formats). Once loaded, the MSExperiment object exposes both MS1 and MS2 spectra with precursor–product mass pairs, retention times, and intensity values for subsequent feature detection and diagnostic fragment matching. Verify that the file contains centroided (not profile) spectra and that MS2 data is present if MS2-based filtering will be applied; raw data without MS2 information limits downstream PFAS prioritization techniques.

## Related tools

- **pyOpenMS** (Python interface for loading and parsing centroided mzML files into MSExperiment objects for feature detection and spectral manipulation) — https://github.com/OpenMS/OpenMS
- **OpenMS** (C++ library underlying pyOpenMS; provides MSExperiment data structure and I/O for mzML format) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Utility to convert vendor raw mass spectrometry files to vendor-independent mzML format with centroiding options)
- **PFΔScreen** (Complete GUI workflow that wraps pyOpenMS mzML parsing and feature detection for PFAS prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- MSExperiment object successfully loads without I/O or parsing errors; file size and spectrum count match metadata in mzML header.
- Centroid flag is set correctly in spectrum metadata; centroid m/z and intensity arrays are non-empty and finite for all spectra.
- Retention time values are monotonically increasing or properly ordered by scan number; m/z values fall within expected range (50–2000 m/z typical for HRMS).
- MS2 spectra are correctly linked to precursor m/z and precursor scan number; no orphaned MS2 spectra lacking a valid precursor mass.
- Intensity values are numeric, non-negative, and match the dynamic range expected from the mass spectrometer (e.g., no saturation artifacts if data was acquired properly).

## Limitations

- mzML parsing requires that data be acquired and exported in centroided format; profile-mode data or centroiding applied post-hoc during export may lead to poor feature detection.
- MSConvert conversion parameters (centroiding algorithm, mass accuracy, peak-picking threshold) affect downstream feature detection; suboptimal conversion settings propagate through the entire workflow.
- Very large mzML files (>1–2 GB) may require substantial RAM when fully loaded into a single MSExperiment object; batch processing or streaming may be necessary for high-throughput studies.
- mzML standard does not guarantee preservation of vendor-specific metadata (e.g., collision energy per precursor, scan event configuration); loss of this information may limit retrospective analysis.

## Evidence

- [intro] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool).: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
- [other] Load centroided mzML file using pyOpenMS MSExperiment reader.: "Load centroided mzML file using pyOpenMS MSExperiment reader"
- [other] Load centroided MS2 spectra from mzML file using pyOpenMS.: "Load centroided MS2 spectra from mzML file using pyOpenMS"
