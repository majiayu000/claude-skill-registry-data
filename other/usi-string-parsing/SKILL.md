---
name: usi-string-parsing
description: Use when when you have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3281
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - GNPS LCMS Visualization Dashboard
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

# usi-string-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse Unified Spectrum Identifier (USI) strings to extract repository identifiers, file paths, and scan numbers, enabling programmatic retrieval of mass spectrometry data from distributed repositories (GNPS, MassIVE, MetaboLights). This skill bridges human-readable spectrum citations with machine-actionable data access.

## When to use

When you have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171) and need to programmatically resolve it to retrieve the corresponding mass spectrum peak list, chromatographic data, or metadata from GNPS analysis tasks, MassIVE public datasets, or MetaboLights repositories.

## When NOT to use

- USI string is malformed or does not conform to mzspec specification (no repository prefix or invalid separator structure)
- Dataset or task ID does not exist in the specified repository (resolution will fail and require manual verification)
- Network access to GNPS or target repository is unavailable or rate-limited

## Inputs

- USI string (format: mzspec:REPOSITORY:IDENTIFIER:PATH or mzspec:REPOSITORY:IDENTIFIER:PATH:scan:SCANNUMBER)
- USI format specification document
- Network access to GNPS repository API or GNPS LCMS Visualization Dashboard

## Outputs

- Parsed components: repository, dataset ID, file path, scan number (if applicable)
- Remote data URL for the spectrum
- Peak list (m/z and intensity pairs) in CSV or JSON format
- Spectrum metadata (retention time, scan number, MS level)

## How to apply

Parse the USI string following the mzspec format specification to extract three key components: the data repository prefix (GNPS, MSV, or MTBLS), the dataset/task identifier, and the file path plus optional scan number. Use the GNPS LCMS Visualization Dashboard API or repository-specific endpoints to construct the remote data URL. Query the endpoint with the parsed identifiers to retrieve spectrum metadata and scan data. Extract the peak list (m/z and intensity pairs) from the resolved scan and validate that the returned data matches the expected schema (numeric m/z and intensity columns). Format and export as CSV or JSON depending on downstream analysis requirements.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Resolves USI strings and retrieves spectrum data via web API; serves as primary endpoint for mzspec USI resolution and data visualization) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Evaluation signals

- Parsed repository identifier matches one of: GNPS, MSV (MassIVE), MTBLS (MetaboLights), MSV (proteomics)
- Dataset/task ID is non-empty and conforms to repository naming convention (e.g., TASK-* for GNPS, MSV* for MassIVE)
- File path contains expected extension (.mzXML, .mzML, or vendor format); if scan number is present, it is a positive integer
- Remote URL resolves without HTTP error; returned peak list contains at least one m/z–intensity pair with numeric values in expected ranges (m/z typically 50–2000, intensity ≥ 0)
- Data schema matches expected output (e.g., two-column CSV with m/z and intensity; no missing or null values in peak list)

## Limitations

- USI resolution depends on the target repository maintaining stable API endpoints and data availability; datasets may be embargoed, deleted, or relocated
- Scan numbers are optional in USI strings; if absent, the parser must return file-level data or require additional disambiguation
- Different repositories (GNPS, MassIVE, MetaboLights) may have different data access policies, rate limits, or authentication requirements not handled by the USI parser alone
- Large datasets may require pagination or streaming to retrieve complete peak lists; single USI resolution may return metadata only, not full spectrum data

## Evidence

- [other] GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number: "GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number, which the GNPS LCMS Visualization Dashboard uses as a data source to retrieve"
- [other] Parse the USI string to extract the GNPS task ID and scan number using the USI format specification.: "Parse the USI string to extract the GNPS task ID and scan number using the USI format specification."
- [readme] USI Specification that denotes what the resource is and how to get data. Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI.: "USI Specification that denotes what the resource is and how to get data. Update the code in ```download.py```, specifically in ```_resolve_usi_remotelink``` to implement how to get the remote URL for"
- [readme] Example data sources include GNPS Analysis Tasks, GNPS/MassIVE public datasets, MassIVE Proteomics datasets, and MetaboLights public datasets: "1. GNPS Analysis Tasks - mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171
1. GNPS/MassIVE public datasets -"
