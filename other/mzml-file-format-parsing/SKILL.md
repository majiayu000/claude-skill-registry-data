---
name: mzml-file-format-parsing
description: Use when you have mass spectrometry raw data in mzML format and need
  to execute MassQL queries, perform batch analysis across a directory of spectra
  files, or programmatically access MS1 and MS2 scan data with retention time, m/z,
  and intensity metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassQLab
  - MassQL
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lcmsworld_cq
    doi: 10.1021/acs.jproteome.0c00618
    title: lcmsWorld
  - build: coll_massqlab_cq
    doi: 10.1002/rcm.10132
    title: MassQLab
  dedup_kept_from: coll_massqlab_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.10132
  all_source_dois:
  - 10.1002/rcm.10132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML File Format Parsing

## Summary

Parse and load mass spectrometry data stored in mzML format into structured dataframes (MS1 and MS2 scans) for downstream query and analysis. This skill is essential for enabling domain-specific query languages and batch analysis workflows to operate on standardized mass spectrometry data.

## When to use

When you have mass spectrometry raw data in mzML format and need to execute MassQL queries, perform batch analysis across a directory of spectra files, or programmatically access MS1 and MS2 scan data with retention time, m/z, and intensity metadata. Specifically useful when you are building a reproducible workflow that must handle multiple mzML files uniformly.

## When NOT to use

- Input is already in a non-mzML format (e.g. raw Waters, Thermo, or Bruker files) without prior conversion — convert to mzML using external tool (ProteoWizard msconvert) first.
- Data is already loaded in memory as a pandas DataFrame or other table format and does not need file I/O.
- mzML files are corrupted or do not conform to mzML schema — parsing will fail or produce incomplete dataframes.

## Inputs

- mzML mass spectrometry data files (single file or directory of files)
- File path or directory path to mzML files

## Outputs

- Parsed MS1 dataframe (scan info, retention time, m/z values, intensities)
- Parsed MS2 dataframe (scan info, precursor m/z, product ion m/z, intensities)
- Optional: Feather-format cached intermediate file for faster re-access

## How to apply

Use the MassQL file-loading API to discover and parse all mzML files in an input directory, extracting MS1 and MS2 dataframes with scan metadata (scan ID, retention time, m/z, intensity, precursor m/z for MS2). The parsed dataframes can then be passed directly to the MassQL query engine, or cached as Feather format for faster re-querying on subsequent runs. Key decision: if re-querying the same directory frequently, enable caching; if converting from raw format, pre-convert to mzML using ProteoWizard msconvert rather than relying on MassQLab's experimental raw-to-mzML conversion.

## Related tools

- **MassQL** (Domain-specific query language that accepts parsed MS1/MS2 dataframes from mzML parsing and executes mass spectrometry queries (e.g., m/z tolerance filters, retention time ranges, precursor/product ion matching)) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (Batch workflow orchestrator that internally uses mzML file parsing to load all files from a directory, then applies a set of MassQL queries to each parsed file and tabulates results) — https://github.com/JohnsonDylan/MassQLab
- **ProteoWizard msconvert** (External tool for converting raw mass spectrometry formats (Waters, Thermo, Bruker) to mzML before parsing)

## Examples

```
from massql import msql_fileloading
ms1_df, ms2_df = msql_fileloading.load_data('path/to/file.mzML')
```

## Evaluation signals

- Both MS1 and MS2 dataframes are successfully returned with non-empty rows if mzML file contains both scan types.
- Parsed scan metadata (scan ID, retention time, m/z, intensity columns) match the structure expected by MassQL query engine without additional transformation.
- Parsed dataframes can be passed directly to `msql_engine.process_query()` without type errors or missing columns.
- If caching is enabled, Feather file is written to disk and subsequent re-parsing loads from cache in sub-second time (vs. full parse time).
- All mzML files in a directory are discovered and parsed; no files are silently skipped due to naming or location mismatches.

## Limitations

- MassQLab's experimental raw-to-mzML conversion feature is not recommended for production use; pre-convert raw files using ProteoWizard msconvert instead.
- Currently processes all files in the specified directory without filtering by name or extension; must pre-organize input folder to avoid non-mzML files.
- Performance scales linearly with the number and size of mzML files; very large batch jobs (thousands of files or multi-GB files) may require memory optimization or chunking.
- Corrupted or malformed mzML files will cause parsing to fail or return incomplete/null dataframes; no robust error recovery or partial-file resumption is documented.

## Evidence

- [readme] Loading Data
ms1_df, ms2_df = msql_fileloading.load_data(input_filename): "ms1_df, ms2_df = msql_fileloading.load_data(input_filename)"
- [readme] MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format.: "directory containing mass spectrometry data in mzML format"
- [other] Load all mzML files from the input directory using MassQLab's file-discovery mechanism.: "Load all mzML files from the input directory using MassQLab's file-discovery mechanism"
- [readme] If `cache_setting` is `true`, saves an intermediate Feather file to disk and uses it for faster re-querying.: "saves an intermediate Feather file to disk and uses it for faster re-querying"
- [readme] This feature is experimental. It is recommended to convert files using ProteoWizard msconvert before using MassQLab.: "recommended to convert files using ProteoWizard msconvert before using MassQLab"
