---
name: usi-namespace-parsing
description: Use when when you need to retrieve mass spectrometry spectrum data from
  a metabolomics repository but only have a USI string (e.g., 'mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943'
  or 'mzspec:MASSBANK::accession:SM858102').
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MS2LDA
  - GNPS Spectral Libraries
  - ProteoXchange Repository
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
- MS2LDA Reference Motifs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabolomics_spectrum_resolver_cq
    doi: 10.1101/2020.05.09.086066
    title: Metabolomics Spectrum Resolver
  dedup_kept_from: coll_metabolomics_spectrum_resolver_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.05.09.086066
  all_source_dois:
  - 10.1101/2020.05.09.086066
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# USI Namespace Parsing and Repository Dispatch

## Summary

Parse Unified Spectrum Identifier (USI) strings to extract namespace prefixes and resource identifiers, then dispatch retrieval requests to the correct metabolomics data source backend. This skill enables consistent, programmatic access to spectrum data across seven distinct repositories by decoding USI structure and routing queries appropriately.

## When to use

When you need to retrieve mass spectrometry spectrum data from a metabolomics repository but only have a USI string (e.g., 'mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943' or 'mzspec:MASSBANK::accession:SM858102'). Apply this skill when the data source is unknown a priori and must be inferred from the USI format, or when you are building a resolver that must support multiple repositories transparently.

## When NOT to use

- Input is a spectrum already in memory or a parsed spectrum object—parsing is unnecessary and will add latency.
- USI namespace is not one of the seven supported types (GNPS, MASSBANK, MS2LDA, ProteoXchange, MetaboLights, Metabolomics Workbench, MassIVE)—dispatch will fail.
- You need to validate USI syntax without retrieving data; use a lightweight USI format validator instead of the full resolver.

## Inputs

- USI string (mzspec or mzdraft prefix with colon-delimited namespace and resource identifier)
- USI format specification document or mapping table for the seven supported repository types

## Outputs

- Repository backend identifier (GNPS, MASSBANK, MS2LDA, ProteoXchange, MetaboLights, Metabolomics Workbench, or MassIVE)
- Parsed resource identifier (task ID, accession number, file path, scan number as appropriate)
- Spectrum data object in standardized format (JSON with m/z, intensity, metadata)

## How to apply

1. Extract the USI namespace prefix (the second colon-delimited field after 'mzspec:', e.g., 'GNPS', 'MASSBANK', 'MS2LDA') from the input USI string. 2. Match this prefix against a supported-source mapping table that tracks the seven repository types: GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench. 3. Extract the resource identifier fields following the namespace according to the USI format specification for that source (e.g., task ID and scan number for GNPS, accession for MassBank). 4. Dispatch the retrieval request to the corresponding repository backend API or data access layer. 5. Return the spectrum data in a standardized format (JSON spectrum object with m/z, intensity, and metadata fields). Validate that the parsed namespace is recognized before dispatching; reject unrecognized prefixes with an informative error.

## Related tools

- **GNPS Molecular Networking** (Source repository for clustered spectra; namespace prefix 'GNPS' with task ID and file path) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **GNPS Spectral Libraries** (Source repository for library spectra; namespace prefix 'GNPS' with library accession) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **MassBank** (Source repository for library spectra; namespace prefix 'MASSBANK' with accession number) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **MS2LDA** (Source repository for reference motifs; namespace prefix 'MS2LDA' with task and accession) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **ProteoXchange Repository** (Source repository for repository data; namespace prefix 'PXD' with dataset ID and file path) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **MetaboLights** (Source repository for dataset spectra; namespace uses MetaboLights MSV identifier) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **Metabolomics Workbench** (Source repository for dataset spectra; namespace uses Metabolomics Workbench MSV identifier) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
https://metabolomics-usi.ucsd.edu/json/?usi=mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943
```

## Evaluation signals

- Parsed namespace prefix matches exactly one of the seven supported repository types without error or ambiguity.
- Resource identifier fields are successfully extracted and conform to the expected format for that repository (e.g., task ID + file path for GNPS task spectra, accession for MassBank).
- Dispatch to the correct backend API completes without routing error, and the returned spectrum object contains non-empty m/z and intensity arrays with matching length.
- Spectrum data is returned in standardized JSON format with required metadata fields present (e.g., precursor m/z, retention time if available).
- Unrecognized or malformed USI strings are rejected with an informative error message identifying the invalid namespace prefix.

## Limitations

- USI identifiers are based on draft specifications and are subject to change; the resolver uses 'mzdraft' prefix instead of 'mzspec' for draft identifiers, which may cause forward compatibility issues.
- The resolver supports exactly seven repository types; any spectrum residing in repositories outside this list cannot be retrieved via USI dispatch.
- Complex USI formats with nested file paths or ambiguous scan specifiers (e.g., 'GNPS:TASK-...-spectra/specs_ms.mgf:scan:X' vs. 'GNPS:TASK-...-spectra:scan:X') require careful format specification to avoid parsing errors.
- No changelog is available for version tracking or breaking changes to USI namespace mappings.

## Evidence

- [other] The resolver supports seven distinct USI types corresponding to different metabolomics data sources: "The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository"
- [other] Parsing and namespace matching workflow: "1. Parse the input USI to extract its namespace prefix and resource identifier. 2. Match the namespace against a mapping table to identify the supported source repository. 3. Dispatch the retrieval"
- [other] Standardized output format requirement: "4. Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields)."
- [readme] Example USI formats for different repositories: "mzspec:MASSBANK::accession:<MassBank Accession> ... mzspec:GNPS:TASK-<GNPS Task ID>-<File name in task>:scan:<scan number> ... mzspec:MOTIFDB::accession:<Motif DB accession>"
- [readme] Draft specification caveat: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in"
