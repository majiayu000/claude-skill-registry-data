---
name: mzml-file-import-xcms
description: Use when you have raw mzML files from a mass spectrometry instrument
  and need to begin a preprocessing workflow in xcms. This is the essential first
  step before any peak detection (centWave, MSWParam) or feature grouping can occur.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - MsDataHub
  - MassSpecWavelet
  - MSnbase
  - Spectra
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as
  well as GC-MS and LC-MS/MS) data.
- 'Package: xcms'
- library(MsDataHub)
- '`r Biocpkg("xcms")` uses functionality from the *MassSpecWavelet* package to identify
  such peaks'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-file-import-xcms

## Summary

Load raw mass spectrometry data in mzML format into xcms as an XCMSnExp object with on-disk mode to enable downstream peak detection and feature grouping workflows. This is the foundational step that prepares LC-MS, GC-MS, or LC-MS/MS data for chromatographic peak detection and feature extraction.

## When to use

You have raw mzML files from a mass spectrometry instrument and need to begin a preprocessing workflow in xcms. This is the essential first step before any peak detection (centWave, MSWParam) or feature grouping can occur. Use this skill when starting fresh with instrument output files, not when data is already loaded or peak-detected.

## When NOT to use

- Data is already in NetCDF format — use xcms's NetCDF import functions instead.
- Spectra have already been peak-detected and you have a feature table — skip to feature grouping.
- You are working with already-preprocessed data from another tool (e.g., vendor software); import the results directly if they are in a supported format.

## Inputs

- vector of mzML file paths
- AnnotatedDataFrame with sample metadata (phenotype information)
- mzML files from LC-MS, GC-MS, or LC-MS/MS instrument

## Outputs

- XCMSnExp object (on-disk mode)
- spectral data index with m/z and retention time ranges
- linked sample metadata and file references

## How to apply

Call readMSData() with the vector of mzML file paths, pass an AnnotatedDataFrame containing sample metadata (phenotype information), and set mode='onDisk' to avoid loading all spectra into memory at once. The on-disk mode defers spectrum loading until needed, enabling efficient processing of large experiments. The function returns an XCMSnExp object that retains file paths and metadata while providing access to raw spectra data on demand. Validate that the resulting object contains the expected number of samples and that mz/retention time ranges are present in the spectra index.

## Related tools

- **xcms** (Primary tool providing readMSData() function and XCMSnExp object class for on-disk mzML import and spectrum indexing) — https://github.com/sneumann/xcms
- **MSnbase** (Provides AnnotatedDataFrame class for sample metadata and underlying spectrum data structures used by xcms)
- **MsDataHub** (Optional data source for retrieving example mzML files used in workflows)
- **Spectra** (Alternative modern backend for spectrum representation in xcms version 4+)

## Examples

```
library(xcms); pd <- data.frame(sample_name=c('HAM004','HAM005'), file=c('HAM004.mzML','HAM005.mzML')); xmse <- readMSData(files=pd$file, pdata=AnnotatedDataFrame(pd), mode='onDisk')
```

## Evaluation signals

- Resulting XCMSnExp object has length equal to the number of input mzML files and contains sample names from metadata
- Object is in on-disk mode (no full spectra loaded into memory) — verify via object class and memory footprint
- Spectrum index contains valid m/z ranges and retention time ranges for each sample
- Calling spectra() or mz() on the object successfully retrieves data without error
- Sample metadata from AnnotatedDataFrame is accessible via phenoData() with no missing values for key experimental descriptors

## Limitations

- On-disk mode requires mzML files to remain at their original file paths; moving files after import breaks spectrum access.
- mzML import assumes well-formed XML structure; corrupted or non-compliant mzML files will fail parsing.
- Very large mzML files (>10 GB) may experience slow index creation; consider splitting by sample or time range.
- Metadata in the input AnnotatedDataFrame must match the number and order of mzML files; mismatches will cause incorrect sample assignment.

## Evidence

- [intro] readMSData() function with on-disk mode documentation: "readMSData(files = mzML_files, pdata = AnnotatedDataFrame(pd), mode = "onDisk")"
- [readme] xcms package purpose statement: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [other] Task-level workflow confirming XCMSnExp creation from mzML: "Load the HAM004 and HAM005 mzML files from MsDataHub using readMSData() in xcms with on-disk mode to create an XCMSnExp object."
- [readme] Version 4 support for modern data containers: "Version 4 adds native support for the Spectra package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects"
