---
name: jcamp-file-parsing
description: Use when you receive uploaded spectral data in JCAMP format (jcamp) as
  input to the /api/v1/chemspectra/file/convert endpoint, or when you need to extract
  and validate metadata and peak information from an existing JCAMP file before converting
  to another format or performing spectral analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Python 3
  - Flask
  - Docker
  - proteowizard/pwiz-skyline
  - chem-spectra-app
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- Use the file pyproject.toml to determine the version of Python required.
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0
  --port=3007
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data
  proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemspectra_cq
    doi: 10.1186/s13321-020-00481-0
    title: ChemSpectra
  dedup_kept_from: coll_chemspectra_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00481-0
  all_source_dois:
  - 10.1186/s13321-020-00481-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# jcamp-file-parsing

## Summary

Parse and validate JCAMP spectral files received via HTTP POST to the ChemSpectra App file-conversion API, extracting metadata and spectral parameters for standardized internal representation. This skill is essential when ingesting vendor-neutral NMR/IR/MS data in JCAMP format for downstream spectral processing and format conversion.

## When to use

Apply this skill when you receive uploaded spectral data in JCAMP format (jcamp) as input to the /api/v1/chemspectra/file/convert endpoint, or when you need to extract and validate metadata and peak information from an existing JCAMP file before converting to another format or performing spectral analysis.

## When NOT to use

- Input file is in RAW or mzML format — use vendor-specific or proteowizard-based parsing instead.
- JCAMP file is already embedded in a serialized database record — extract the file first before parsing.
- Metadata validation is not required and only raw binary spectral arrays are needed — use direct array extraction without full JCAMP parsing.

## Inputs

- JCAMP spectral file (binary or text format)
- HTTP POST request body containing uploaded JCAMP file
- JCAMP metadata headers (e.g., TITLE, JCAMP-DX, DATATYPE)
- JCAMP data blocks (e.g., NMR, IR, MS spectral arrays)

## Outputs

- Parsed spectral metadata (sample name, acquisition parameters, spectral type)
- Extracted peak table (chemical shifts, intensities, multiplicities for NMR)
- Standardized internal spectral representation
- Validated JCAMP structure (confirmed header and data block integrity)

## How to apply

Receive the JCAMP file as part of an HTTP POST request to the file-conversion endpoint. Parse the JCAMP format using the ChemSpectra App backend parser (built into the Flask service) to extract spectral metadata (e.g., sample name, acquisition parameters, spectral type) and peak tables. Validate that required JCAMP header fields and data blocks are present and correctly formatted. Convert the parsed JCAMP data into the backend's standardized internal representation for NMR/IR/MS spectral data. If the JCAMP file is well-formed and metadata is complete, proceed to serialization or further processing; if validation fails, return an error response indicating the parsing issue. The skill succeeds when metadata and peak tables are accurately extracted without data loss.

## Related tools

- **Flask** (HTTP framework routing POST requests to /api/v1/chemspectra/file/convert and parsing JCAMP payloads) — https://flask.palletsprojects.com/
- **Python 3** (Language in which JCAMP file parsing and metadata extraction logic is implemented) — https://github.com/ComPlat/chem-spectra-app
- **chem-spectra-app** (Backend web service that orchestrates JCAMP parsing, validation, and conversion) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/file/convert -F 'file=@spectrum.jcamp'
```

## Evaluation signals

- Parsed metadata matches expected JCAMP header fields (TITLE, JCAMP-DX, DATATYPE, DATACLASS present and non-empty).
- Extracted peak table contains same number and order of peaks as the original JCAMP data block (verified by count comparison).
- Spectral parameters (frequency, nucleus type, solvent for NMR; resolution, range for IR) are correctly transferred to internal representation.
- HTTP response status is 200 OK with converted file artifact when parsing succeeds; 4xx error when JCAMP structure is malformed.
- No data truncation or loss in chemical shift values, intensities, or multiplicities during parsing and serialization.

## Limitations

- JCAMP variant/version differences may cause parsing failures if the backend does not support all JCAMP-DX versions or extensions.
- Files with non-standard or corrupted JCAMP header lines will fail validation; error messages may not pinpoint the exact malformed field.
- Large JCAMP files (many data points or complex peak structures) may incur parsing latency and consume significant memory during internal representation construction.
- Metadata extraction assumes standard JCAMP naming conventions; custom or proprietary metadata fields in JCAMP files may be silently dropped.

## Evidence

- [other] Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint.: "Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint."
- [other] Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats.: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats."
- [other] Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters.: "Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters."
- [intro] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Serialize the converted file to jcamp output format with peak tables and metadata.: "Serialize the converted file to jcamp output format with peak tables and metadata."
