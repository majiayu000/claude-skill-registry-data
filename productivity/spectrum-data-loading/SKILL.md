---
name: spectrum-data-loading
description: Use when when you have a USI (e.g., mzspec:MTBLS1124:QC07.mzML) pointing
  to a public mzML or related spectrum file in MetaboLights, MassIVE, or GNPS repositories,
  and need to load the spectrum data for interactive visualization, quality control
  assessment, or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GNPS LCMS Visualization Dashboard
  - pymzML
  - mzML validator / indexer
  - MetaboLights REST API
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-data-loading

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load mass spectrometry spectrum data from public repositories (MetaboLights, MassIVE, GNPS) into memory via Universal Spectrum Identifier (USI) resolution, validation, and parsing into spectrum container objects. This skill enables downstream LC-MS visualization, feature extraction, and spectral comparison workflows.

## When to use

When you have a USI (e.g., mzspec:MTBLS1124:QC07.mzML) pointing to a public mzML or related spectrum file in MetaboLights, MassIVE, or GNPS repositories, and need to load the spectrum data for interactive visualization, quality control assessment, or downstream analysis. The USI format allows rapid access to multi-vendor instrument data (Thermo, Sciex, Bruker, Waters, Agilent) without manual download.

## When NOT to use

- Input is already a parsed spectrum object or in-memory data structure (spectrum container already loaded).
- Target file is in a proprietary vendor format (raw, d, or yep) without prior conversion to mzML.
- Repository access is restricted (non-public datasets requiring authentication not handled by USI resolver).
- File size exceeds available system memory for full in-memory loading.

## Inputs

- Universal Spectrum Identifier (USI) string (e.g., mzspec:MTBLS1124:QC07.mzML)
- Repository accession code (MTBLS*, MSV*, or GNPS TASK-* identifier)
- File path or name within repository (e.g., QC07.mzML)

## Outputs

- Downloaded mzML file (binary XML, validated against schema)
- In-memory spectrum container object (pymzML or equivalent) with indexed scan access
- Spectrum metadata (retention time, precursor m/z, scan number, polarity)
- Chromatogram data (base peak intensity over retention time)

## How to apply

First, parse the USI string to extract the repository prefix (MTBLS, MSV, or GNPS) and the accession or file identifier. Second, resolve the USI to a remote download URL using the GNPS LCMS Visualization Dashboard's USI resolution logic (implemented in download.py's _resolve_usi_remotelink function). Third, download the mzML file from the remote repository to local storage. Fourth, validate the downloaded file against the mzML XML schema, checking for spectrum list presence and indexed offset integrity using an mzML validator (e.g., pymzML parser or mzML indexer). Fifth, load the validated mzML into an in-memory spectrum container (e.g., pymzML object) to enable scan-level access, metadata retrieval, and chromatogram extraction. Sixth, verify successful load by confirming non-empty spectrum counts and accessible m/z and retention time fields.

## Related tools

- **GNPS LCMS Visualization Dashboard** (USI resolution, remote URL lookup, and spectrum rendering interface) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **pymzML** (mzML parser and spectrum container for indexed scan access and validation)
- **mzML validator / indexer** (Schema validation and indexed offset integrity verification)
- **MetaboLights REST API** (File manifest retrieval and download service lookup)

## Evaluation signals

- USI string successfully parsed into repository prefix, accession, and file identifier components.
- Remote download URL correctly resolved and HTTP response status is 200 OK with non-zero file size.
- Downloaded mzML file passes XML schema validation (well-formed XML, spectrum list present, indexedmzML offsets readable).
- In-memory spectrum container loads without parsing errors; spectrum count > 0 and each scan has non-null retention time and m/z array.
- Chromatogram or XIC (extracted ion chromatogram) can be rendered without missing scan data; retention time and intensity arrays align.

## Limitations

- USI resolver currently supports only MetaboLights (MTBLS), MassIVE (MSV), and GNPS (GNPS TASK-*) repositories; other public or private repositories require custom resolver implementation.
- Large mzML files (>1–2 GB) may exceed typical system memory when loaded fully into spectrum container; streaming or indexed access may be needed for proteomics datasets.
- Metabolites and proteomics data may use different mzML profiles (centroided vs. profile mode, MS2 vs. MS3); validator ensures schema compliance but does not detect instrument-specific data quality issues.
- Network latency and repository availability affect download speed; no retry or caching logic is documented in the README.
- File paths with special characters or long names in repositories may not resolve correctly; USI specification conformance depends on correct accession format.

## Evidence

- [other] Can the MetaboLights dataset identifier mzspec:MTBLS1124:QC07.mzML be successfully resolved to retrieve the corresponding deposited file?: "Can the MetaboLights dataset identifier mzspec:MTBLS1124:QC07.mzML be successfully resolved to retrieve the corresponding deposited file?"
- [other] Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML). Query the MetaboLights REST API or download service using accession MTBLS1124 to retrieve the file manifest and locate QC07.mzML. Download QC07.mzML from the MetaboLights repository to local storage.: "Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML). Query the MetaboLights REST API or download service using accession"
- [other] Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity.: "Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity."
- [other] Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval.: "Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval."
- [other] GNPS LCMS Visualization Dashboard documentation lists mzspec:MTBLS1124:QC07.mzML as an example MetaboLights public dataset source, indicating this USI format is supported for dataset retrieval and visualization.: "GNPS LCMS Visualization Dashboard documentation lists mzspec:MTBLS1124:QC07.mzML as an example MetaboLights public dataset source, indicating this USI format is supported for dataset retrieval and"
- [readme] Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from. If you want to provide a new data source, you'll have to implement the following: USI Specification that denotes what the resource is and how to get data. Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI.: "Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from. If you want to provide a new data source, you'll have to implement the following: USI"
