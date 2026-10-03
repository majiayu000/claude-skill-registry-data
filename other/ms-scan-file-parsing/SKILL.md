---
name: ms-scan-file-parsing
description: Use when you have acquired a Thermo mass spectrometry RAW file (or other
  proprietary instrument format) and need to extract MS1 and/or MS2 scans in an open,
  interoperable format (mzML, MGF, or Raxport-processed FT1/FT2 files) for TIC visualization,
  PSM scoring, or stable isotope labeling analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - ThermoRawFileParser
  - Raxport.net
  - mzR (Bioconductor)
  - MSnbase (Bioconductor)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-scan-file-parsing

## Summary

Parse mass spectrometry raw files and extract MS1/MS2 scan data into structured formats (mzML, MGF, FT1/FT2) suitable for downstream chromatographic visualization and peptide-spectrum matching. This skill bridges proprietary instrument formats (Thermo RAW) and open standards required by proteomics and metabolomics workflows.

## When to use

You have acquired a Thermo mass spectrometry RAW file (or other proprietary instrument format) and need to extract MS1 and/or MS2 scans in an open, interoperable format (mzML, MGF, or Raxport-processed FT1/FT2 files) for TIC visualization, PSM scoring, or stable isotope labeling analysis. This is a mandatory first step before applying getTIC, isotopic envelope calculation, or PSM visualization in Aerith.

## When NOT to use

- Input is already in an open format (mzML, MGF, or Raxport FT1/FT2); proceed directly to getTIC or PSM scoring.
- You need to preserve Thermo-specific metadata (e.g., instrument tuning parameters, detector-level noise data) beyond standard PROXI; use ThermoRawFileParser with `-a` (allDetectors) flag or consider proprietary APIs.
- Your workflow is instrument-agnostic and does not require charge state annotation; other converters (e.g., XCMS, msConvert) may be simpler.

## Inputs

- Thermo mass spectrometer RAW file (.raw)
- Raw file directory (batch processing)
- Instrument type metadata (Orbitrap, IonTrap)
- MS level specification (e.g., MS1, MS2, or MS1-3)

## Outputs

- mzML file (indexed or non-indexed) with MS1/MS2 scans
- MGF file with MS2 spectra and precursor m/z
- FT1 file (MS1 scans) or FT2 file (MS2 scans) with charge annotation
- Parquet file (columnar format alternative)
- JSON metadata (instrument info, scan counts, polarity)

## How to apply

Use ThermoRawFileParser or Raxport.net to convert proprietary RAW files to open formats: specify the input RAW file path and output format (mzML, indexed mzML, MGF, or FT1/FT2 for Orbitrap/IonTrap scans). For Orbitrap data, charge information is automatically included in the output; for IonTrap scans, charge may be omitted unless the scan originates from an Orbitrap detector. After conversion, validate the output by loading parsed scans into Aerith (via readAllScanMS1 for MS1 scans or equivalent MS2 readers) and confirm the scan structure contains retention time, m/z, and intensity arrays. Optional: apply peak picking via the `-p` flag in ThermoRawFileParser or disable it (default is enabled) based on whether your downstream analysis requires raw or centroided profiles.

## Related tools

- **ThermoRawFileParser** (Convert Thermo RAW files to mzML, MGF, or Parquet; supports peak picking, MS level filtering, and charge state detection for Orbitrap) — https://github.com/CompOmics/ThermoRawFileParser
- **Raxport.net** (Extract MS1 (FT1) and MS2 (FT2) scans from Thermo RAW files with charge information for Orbitrap; input for Aerith readAllScanMS1/MS2) — https://github.com/xyz1396/Raxport.net
- **Aerith** (Load and validate parsed MS scans (FT1/FT2, mzML, MGF); compute TIC and calculate theoretical isotopic envelopes) — https://github.com/xyz1396/Aerith
- **mzR (Bioconductor)** (R interface for direct parsing of mzML and MGF files in Aerith workflows)
- **MSnbase (Bioconductor)** (Parse pepXML files and PSM annotations for integration with MS scan data)

## Examples

```
ThermoRawFileParser -i=sample.raw -o=output_dir -f=1 -m=0 -p
```

## Evaluation signals

- Output file is well-formed (validates against mzML schema or MGF specification; no truncation or parsing errors).
- MS1 scans are present and contain ≥1 m/z-intensity pairs per scan with valid retention time indices (e.g., 0.1–60 min range).
- Charge states are populated for Orbitrap scans (FT1/FT2 output); IonTrap scans may lack charge without indicating failure.
- Scan count and MS level distribution in output metadata match the input RAW file statistics (e.g., 'MS1: 5000, MS2: 50000' if reported by ThermoRawFileParser `-m=0`).
- readAllScanMS1 in Aerith successfully loads the output file and produces a TIC table with retention time vs. summed intensity (no R errors or null values).

## Limitations

- ThermoRawFileParser requires .NET 8 runtime on Linux/macOS; framework-based releases are self-contained on Windows but add ~100 MB.
- Raxport.net currently supports only MS1 and MS2 scans; higher MS levels (MS3+) are not extracted.
- Charge state annotation is absent for IonTrap scans in both Raxport and ThermoRawFileParser; Orbitrap-only data yields the most complete output.
- Peak picking (enabled by default in ThermoRawFileParser) may distort isotopic fine structure; disable with `-p` for stable isotope labeling applications but increases file size.
- Batch processing of large RAW directories can be I/O-bound; consider parallelization or leverage subset files for method development (per Aerith guidance).

## Evidence

- [readme] extract-raw-files-statement: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans."
- [readme] charge-state-availability: "the generated `.FT1` or `.FT2` files will include charge information only if the scan is from an Orbitrap"
- [readme] ms-level-scope: "Currently, only MS1 and MS2 scans are supported."
- [readme] thermorawfileparser-formats: "ThermoRawFileParser: A tool allowing reading Thermo RAW mass spectrometer files and converting to common open formats on all platforms supporting .NET Core. Supported formats: * MGF * mzML and"
- [intro] aerith-file-input-support: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files"
- [results] readAllScanMS1-function: "Load the demo.FT1 file and extract all MS1 scans using the readAllScanMS1 function in Aerith"
- [readme] peak-picking-option: "Use the `-p` flag to disable the thermo native peak picking."
- [readme] ms-level-filtering: "Select MS levels (MS1, MS2, etc) included in the output, should be a comma-separated list of integers (1,2,3) and/or intervals (1-3)"
- [results] tictable-downstream-use: "Format the filtered table (retention time vs summed intensity) as input-ready for plotTIC visualization"
