---
name: m-z-array-processing
description: Use when when you have imported MSI data (imzML or vendor format) loaded
  into the napari plugin environment and need to organize raw spectral m/z and intensity
  arrays prior to mean intensity calculation, ROI analysis, or database annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3444
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical
  annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-array-processing

## Summary

Extract and aggregate m/z values and their corresponding intensity arrays from mass spectrometry imaging (MSI) spectra loaded in imzML or vendor-specific format. This skill prepares spectral data for downstream quantitative analysis by structuring m/z–intensity pairs into a standardized format.

## When to use

When you have imported MSI data (imzML or vendor format) loaded into the napari plugin environment and need to organize raw spectral m/z and intensity arrays prior to mean intensity calculation, ROI analysis, or database annotation. Apply this skill as the first post-import step to ensure consistent m/z indexing across all pixels/samples in the dataset.

## When NOT to use

- If m/z values and intensities are already pre-processed and aggregated into a mean spectrum table; extract only when raw per-pixel/per-sample data are available.
- If data have already been converted to a feature table (e.g., m/z bins × samples intensity matrix) by another tool; extraction is redundant.
- If you require only visualization of raw spectra without quantitative extraction; skip this step if the goal is exploratory browsing only.

## Inputs

- imzML file (or vendor-specific MSI format)
- Imported MSI spectral dataset within napari plugin environment
- Raw m/z and intensity arrays from mass spectrometry detector

## Outputs

- Structured m/z array (1D vector of unique m/z values)
- Intensity matrix (m/z values × pixel/sample indices)
- CSV or HDF5 table (m/z vs. intensity columns)
- Validated m/z–intensity mapping ready for downstream analysis

## How to apply

After loading imzML data via the MSI-Explorer import interface, extract the m/z axis (common to all spectra) and the intensity arrays for each pixel or sample. Validate that all spectra share the same m/z grid (or perform m/z alignment if data is in profile mode by opting to convert to centroid mode when prompted). Organize extracted m/z values and intensity arrays into a structured table or array object keyed by m/z. This preprocessed m/z–intensity mapping then serves as input to mean intensity aggregation (computing arithmetic mean of intensities at each m/z across all pixels) and enables efficient ROI and annotation queries.

## Related tools

- **napari** (Plugin framework and interactive environment for loading, visualizing, and processing MSI spectral data; hosts the MSI-Explorer plugin interface) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that provides data import, m/z–intensity array extraction, visualization, and downstream analysis workflows for MSI datasets) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Programming language and ecosystem for array manipulation, m/z indexing, and intensity aggregation operations)

## Evaluation signals

- All imported spectra share the same m/z array after extraction (verify by checking m/z grid consistency across pixel indices).
- Intensity matrix dimensions match expected pixel count × m/z bin count; no missing or NaN values in m/z axis.
- Mean intensity calculation on extracted m/z–intensity arrays produces a 1D spectrum with peaks at expected m/z values and no negative intensities.
- Exported CSV/HDF5 file contains m/z and intensity columns with correct data types and numeric ranges; file can be re-imported for ROI or database queries.
- Profile-mode data prompted for centroid conversion; centroid output has higher m/z resolution and lower data size than profile, as expected.

## Limitations

- MSI-Explorer prompts for profile-to-centroid conversion only upon upload; users must explicitly confirm conversion, or data remain in profile mode which may inflate array size and reduce m/z precision.
- m/z arrays extracted from different vendor formats (e.g., Bruker imzML vs. Waters) may differ in precision and binning; alignment or interpolation may be required for cross-platform comparisons.
- If spectra have non-uniform m/z spacing or instrument drift, extracted m/z arrays may contain gaps or duplicate bins; validation and binning strategies are not documented in the README.
- Large MSI datasets (>10,000 pixels) may result in large intensity matrices; memory constraints and file I/O performance are not addressed in the documentation.

## Evidence

- [other] Extract m/z values and intensity arrays for all spectra in the dataset.: "Extract m/z values and intensity arrays for all spectra in the dataset."
- [other] For each unique m/z value across all spectra, calculate the arithmetic mean of intensities at that m/z across all pixels/samples.: "For each unique m/z value across all spectra, calculate the arithmetic mean of intensities at that m/z across all pixels/samples."
- [other] Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows.: "Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows."
- [other] Load imported MSI spectral data (imzML or vendor-specific format) into the napari plugin environment via the MSI-Explorer data import interface.: "Load imported MSI spectral data (imzML or vendor-specific format) into the napari plugin environment via the MSI-Explorer data import interface."
- [readme] Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format.: "Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format."
