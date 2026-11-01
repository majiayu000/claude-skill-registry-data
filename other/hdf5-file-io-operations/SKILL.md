---
name: hdf5-file-io-operations
description: Use when you have raw or peak-picked mass spectrometry data in HDF5 format that needs to be loaded into memory for downstream processing (feature alignment, isotope detection, CCS calibration), or when you need to export annotated feature tables with isotopologue metadata back to HDF5 for archival.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
  - HDF5 / h5py
  - pandas
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
---

# HDF5 File I/O Operations

## Summary

Load and save peak-picked mass spectrometry feature tables from/to HDF5 files with multidimensional columns (m/z, drift time, retention time, intensity). This skill enables efficient storage and retrieval of intermediate analysis results in DEIMoS workflows.

## When to use

Use this skill when you have raw or peak-picked mass spectrometry data in HDF5 format that needs to be loaded into memory for downstream processing (feature alignment, isotope detection, CCS calibration), or when you need to export annotated feature tables with isotopologue metadata back to HDF5 for archival or cross-sample comparison.

## When NOT to use

- Input data is already loaded in memory as a DataFrame or NumPy array — load() is unnecessary.
- Data is in mzML or other non-HDF5 formats — use ProteoWizard msconvert or format-specific loaders first.
- You need real-time streaming of very large files that exceed available RAM — HDF5 load() loads the full group into memory.

## Inputs

- HDF5 file with peak-picked features (key/group path specified)
- Column names mapping to m/z, drift_time, retention_time, and intensity

## Outputs

- In-memory pandas DataFrame or similar structure with multidimensional feature columns
- HDF5 file with annotated features and isotopologue metadata columns

## How to apply

Load HDF5 files using deimos.load() with explicit column specification for the multidimensional data (m/z, drift_time, retention_time, intensity). After processing steps such as intensity thresholding or isotope annotation, export results back to HDF5 format with metadata columns preserved. The key rationale is that HDF5 format preserves the N-dimensional structure of the data while enabling efficient access to subsets of columns across large study cohorts. Specify the HDF5 key (group path within the file) and column names explicitly to ensure correct data interpretation and prevent silent misalignment of features across samples.

## Related tools

- **DEIMoS** (Primary Python API providing deimos.load() and deimos.save() functions for HDF5 I/O) — http://github.com/pnnl/deimos
- **HDF5 / h5py** (Underlying binary format and low-level Python interface used by deimos.load())
- **pandas** (DataFrame object structure returned by deimos.load() for in-memory manipulation)

## Examples

```
ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
```

## Evaluation signals

- Loaded DataFrame shape matches expected number of features and columns (m/z, drift_time, retention_time, intensity present).
- Column data types are numeric (float64 for m/z and times; int or float for intensity) and not object/string.
- No NaN or inf values in critical columns unless explicitly expected from the raw data.
- Round-trip test: save annotated features to HDF5, reload, and verify isotopologue metadata columns and feature counts are preserved.
- Feature m/z and retention time ranges fall within expected instrument calibration bounds (e.g., m/z > 0, retention_time >= 0).

## Limitations

- HDF5 files must be structured with recognizable group/key paths; nonstandard or undocumented internal layouts will cause deimos.load() to fail or return empty results.
- Loading entire large HDF5 groups into memory may exhaust RAM if datasets contain millions of features across high-dimensional space.
- Column names and data types are inferred from HDF5 metadata; misnamed or incompatible columns will not raise errors but will silently produce incorrect results in downstream analysis.
- DEIMoS v1.6.2 operates on N-dimensional data agnostic to instrument type, but the HDF5 schema and column semantics must be consistent with DEIMoS conventions (accession metadata for MS1, MS2, CCS, etc.).

## Evidence

- [results] Load operation with column specification: "ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])"
- [results] Export annotated features to HDF5 with metadata: "Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns."
- [intro] Multi-dimensional HDF5 structure for study cohorts: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [results] Load operation from alternate format (mzML with accession metadata): "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
