---
name: mzml-mzxml-parsing
description: Use when you have raw LC-MS/MS data in mzML or mzXML format and need
  to isolate specific MS1/MS2 scan pairs for a targeted compound list or for building
  a local spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - meRgeION2
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML/mzXML parsing for MS1/MS2 scan extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse mass spectrometry chromatogram files in mzML or mzXML format (converted from Thermo, Waters, or Bruker instruments) to extract MS1 precursor scans and corresponding MS2 fragment spectra based on user-specified m/z and retention time targets. This skill enables selective recovery of scan pairs for spectral library construction while preserving scan metadata.

## When to use

You have raw LC-MS/MS data in mzML or mzXML format and need to isolate specific MS1/MS2 scan pairs for a targeted compound list or for building a local spectral library. Your input includes user-defined m/z targets (and optionally retention time windows) and you want to avoid processing the entire chromatogram file.

## When NOT to use

- Input data is already in a proprietary binary format (Thermo .raw, Waters .raw, Bruker .d) that has not been converted to mzML/mzXML — use a format conversion tool first.
- You require extraction of all scans in the entire file without user-specified m/z or retention time filtering — use a generic mzML/mzXML reader instead.
- Your goal is real-time streaming analysis of acquisition-in-progress data — mzML/mzXML files are typically complete offline outputs.

## Inputs

- mzML file converted from Thermo, Waters, or Bruker raw data
- mzXML file converted from Thermo, Waters, or Bruker raw data
- User-provided m/z target list (as numeric values)
- User-provided retention time ranges (optional; as numeric min/max pairs)

## Outputs

- Extracted MS1 scans (with m/z, retention time, scan number, intensity metadata)
- Extracted MS2 fragment spectra (with scan number, precursor m/z, fragment m/z and intensity pairs)
- Compiled scan pairs in tabular or structured format ready for downstream library merging

## How to apply

Load the mzML/mzXML file using a mass spectrometry data parser compatible with Thermo, Waters, or Bruker conversion outputs. Parse the user-provided m/z targets (and optional retention time ranges if specified) into a query specification. Scan the chromatogram data to identify MS1 scans matching the target m/z values within a user-defined m/z tolerance window and optional retention time bounds. For each matched precursor, extract the corresponding MS2 fragment spectrum. Compile the extracted MS1 and MS2 scan pairs into a tabular or structured output format that retains scan metadata (m/z, retention time, scan number, and intensity). The parsing must support both Data-Driven Acquisition (DDA) and targeted MS/MS acquisition modes.

## Related tools

- **meRgeION2** (R/Bioconductor package providing mzML/mzXML parsing and MS1/MS2 scan extraction workflow with m/z and retention time matching) — https://github.com/daniellyz/MergeION2
- **GNPS** (Reference format standard (GNPS-style spectral library) that downstream merged scans conform to)

## Examples

```
# R example from MergeION2: Extract MS1/MS2 scans from mzML file with m/z targets and RT bounds; exact invocation not detailed in README, but workflow is: (1) load mzML file, (2) specify m/z targets and optional RT range, (3) call extraction function to produce tabular output of matched scans with metadata.
```

## Evaluation signals

- Extracted MS1 scans have m/z values within user-specified tolerance of the query targets (default tolerance and exact tolerance windows should be logged).
- Extracted MS2 scans are correctly paired to their precursor MS1 scans (verify by precursor m/z match and scan ordering).
- Retention time of matched scans (if filtering was applied) falls within user-specified retention time bounds.
- Scan metadata (scan number, intensity, m/z precision) is preserved and matches the values in the original mzML/mzXML file.
- No scans are duplicated or lost in the extraction process (compare total count to manually validated subset).

## Limitations

- Parser compatibility is limited to mzML/mzXML files converted from Thermo, Waters, or Bruker instruments; other vendor formats or non-standard mzML variants may fail to parse correctly.
- Accuracy of m/z and retention time matching depends on user-specified tolerance windows; overly tight tolerances risk missing true target scans due to calibration drift, while loose tolerances may capture off-target scans.
- Both DDA and targeted MS/MS modes are supported, but the presence of MS2 spectra for a matched precursor is not guaranteed (e.g., in DDA mode if the precursor was not selected for fragmentation).
- The README mentions support for ESI-MS/MS spectra in positive ion mode in the pre-compiled spectral database, suggesting potential limitations for negative ion mode data.
- No changelog is documented in the project, limiting visibility into parser updates or bug fixes.

## Evidence

- [intro] Parse mzML/mzXML files from Thermo, Waters, Bruker; support both DDA and targeted MS/MS: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
- [intro] Match MS1 scans by m/z and retention time; extract corresponding MS2 spectra: "extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users"
- [other] Compilation workflow with scan metadata preservation: "Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds (if specified). Extract corresponding MS2 fragment spectra for matched"
- [other] Support for multiple input files and tolerance windows: "Load mzML/mzXML file(s) using a mass spectrometry data parser compatible with Thermo, Waters, or Bruker formats. Parse user-provided m/z targets (and optional retention time ranges) into a query"
