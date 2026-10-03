---
name: msp-file-parsing
description: Use when you have a Mass Spectrum Point (MSP) file containing electron
  ionization mass spectral records with header fields and peak intensity pairs, and
  you need to load it into an R data structure for library searching, format validation,
  or round-trip conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0218
  tools:
  - mssearchr
  - R
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users for conducting library searches against electron ionization mass spectral
  databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users
- enhance the capabilities of R users for conducting library searches
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00322
  all_source_dois:
  - 10.1021/jasms.5c00322
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msp-file-parsing

## Summary

Parse and validate electron ionization mass spectral library files in MSP format, extracting spectral records with their metadata annotations, peak lists, and precursor m/z values for downstream library search or format conversion workflows. This skill is essential for enabling reproducible mass spectral database operations in R environments.

## When to use

You have a Mass Spectrum Point (MSP) file containing electron ionization mass spectral records with header fields and peak intensity pairs, and you need to load it into an R data structure for library searching, format validation, or round-trip conversion. Apply this skill when input is an MSP-formatted spectral library file and your goal is to extract individual spectrum objects with their associated metadata for programmatic access.

## When NOT to use

- Input is already a parsed spectrum object or R data structure in memory — parsing is unnecessary.
- Input file format is not MSP (e.g., JSON, NetCDF, mzML) — use format-specific parsers instead.
- Spectral library is only needed for metadata lookup without full record extraction — a lightweight indexing strategy may be more efficient.

## Inputs

- MSP spectral library file (text format with header fields and peak intensity pairs)
- Spectral metadata annotations (compound identifiers, chemical names, CAS numbers)

## Outputs

- In-memory R data structure (list or data frame) of parsed spectrum objects
- Extracted spectral fields (precursor m/z, peak m/z and intensity pairs, metadata)
- Validated MSP output file (optionally written for verification)

## How to apply

Use the mssearchr package's MSP parser to load the spectral library file into an in-memory R data structure (list or data frame of spectrum objects). Extract and validate key spectral fields from each record, including precursor m/z, peak lists (m/z and intensity pairs), and metadata annotations such as compound name and CAS number. Ensure compliance with MSP specification conventions for header field formatting, peak list delimiters, and record boundaries. For quality assurance, verify the parsed output by writing the spectrum objects back to a new MSP file using mssearchr's MSP writer, then read the output file and compare parsed fields against the original input records to confirm lossless round-trip conversion.

## Related tools

- **mssearchr** (Provides MSP file parsing and writing functionality, as well as spectral field extraction and format validation) — https://github.com/AndreySamokhin/mssearchr
- **R** (Host environment for executing mssearchr MSP parsing and data structure operations)

## Evaluation signals

- Round-trip validation: Parsed spectrum objects written back to MSP and re-parsed yield identical spectral fields (m/z, intensities, metadata) as the original records.
- Schema compliance: All required header fields (precursor m/z, compound name) are extracted and non-null for each spectrum object.
- Field consistency: Extracted peak m/z and intensity pairs match the original file format and preserve numeric precision.
- Record count: Number of parsed spectrum objects equals the number of spectral records in the input MSP file.
- Delimiter detection: Peak list format and field separators conform to MSP specification (e.g., tab or space delimiters, correct line break handling).

## Limitations

- MSP parser assumes well-formed input files adhering to MSP specification; malformed records or non-standard field names may be silently skipped or cause parsing errors.
- Large MSP files may consume significant memory when loaded entirely into R data structures; streaming or chunked parsing strategies are not mentioned in the article.
- Metadata field support depends on MSP file structure; optional or user-defined annotation fields may not be reliably extracted without schema specification.

## Evidence

- [readme] Parse and validate MSP spectral library files into R data structures: "reading/writing *msp* files"
- [other] Extract precursor m/z, peaks, and metadata annotations from each MSP record: "Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations)"
- [other] Ensure MSP format compliance via round-trip conversion: "Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, ensuring format compliance with MSP specification (header fields, peak list format, delimiter conventions)"
- [other] Verify parsing correctness by comparing input and output records: "Verify output file structure by reading it back and comparing parsed fields to the original input records"
