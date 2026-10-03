---
name: msp-to-csv-parsing
description: Use when you have a .msp format MS/MS spectrum library (e.g., from MassBank
  or similar public databases) and need to convert it into individual CSV entries
  indexed by positive or negative ionisation mode for use as a custom fragment library
  in MetaboAnnotatoR annotation pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - MetaboAnnotatoR
  - R
  - MassBank
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS
  All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msp-to-csv-parsing

## Summary

Convert MS/MS spectra from .msp library files into individual CSV library entries with ionisation mode suffixes using the mspToLib function. This skill enables organisation of custom MS/MS fragment libraries for use in metabolite annotation workflows.

## When to use

You have a .msp format MS/MS spectrum library (e.g., from MassBank or similar public databases) and need to convert it into individual CSV entries indexed by positive or negative ionisation mode for use as a custom fragment library in MetaboAnnotatoR annotation pipelines.

## When NOT to use

- Your spectra are already in individual CSV format or in a pre-built feature library format compatible with MetaboAnnotatoR
- You need to process raw centroid-mode LC-MS AIF chromatograms directly; use xcms + RamClustR preprocessing first
- Your input is already peak-picked pseudo-MS/MS spectra objects from RAMClustR; proceed directly to annotation

## Inputs

- .msp file containing MS/MS spectra records (e.g., MassBank_example.msp)
- User-specified output directory path for CSV library entries

## Outputs

- Individual CSV library entries (one per spectrum), with filenames tagged with ionisation mode suffix (positive/negative)
- Occurrence scores for peaks above noise and marker peak thresholds

## How to apply

Load the .msp file using the mspToLib function from MetaboAnnotatoR, which reads each spectra record and applies default peak-picking parameters: noise threshold of 0.005, marker peaks score of 0.9, and marker peaks threshold of 0.1. These thresholds filter peaks above noise level and assign occurrence scores to peaks meeting the marker peak criteria. The function generates one CSV file per spectrum record, stored in a user-defined output directory, with each filename annotated with a 'positive' or 'negative' ionisation mode suffix based on the spectrum metadata. Verify that all spectrum records from the input .msp file are represented as individual CSV entries with correctly labeled mode suffixes and complete spectral annotations.

## Related tools

- **MetaboAnnotatoR** (Provides mspToLib function for .msp-to-CSV conversion and subsequent metabolite annotation of LC-MS AIF features) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher) required to execute mspToLib)
- **MassBank** (Public source of MS/MS spectra in .msp format suitable for conversion into custom libraries)

## Examples

```
mspToLib(mspFile='MassBank_example.msp', outDir='./custom_library', noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)
```

## Evaluation signals

- All spectra records from the input .msp file are converted to individual CSV files (verify record count matches output file count)
- Each output CSV filename contains an ionisation mode suffix (positive or negative) corresponding to spectrum metadata
- Peak occurrence scores are assigned only to peaks above the noise threshold (0.005) and marker peak threshold (0.1)
- Output CSV structure and column names match the expected MetaboAnnotatoR library format for downstream annotateRC function use
- Spectral annotations are complete with m/z values and relative intensities preserved in the CSV entries

## Limitations

- Requires input .msp files to contain properly formatted spectra records with ionisation mode metadata; malformed records may be skipped or cause errors
- Default peak-picking parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1) are fixed in the function; custom thresholds require function modification
- No changelog or version history is available for the MetaboAnnotatoR package, limiting traceability of updates to mspToLib behavior
- Output quality depends on completeness of metadata in the source .msp file (e.g., missing ionisation mode designation may result in ambiguous naming)

## Evidence

- [other] The mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file name to facilitate organisation of custom libraries: "mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file name"
- [other] occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1): "occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)"
- [readme] Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format).: "Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format)"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode.: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
