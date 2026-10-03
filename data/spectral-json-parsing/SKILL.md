---
name: spectral-json-parsing
description: Use when after submitting an LC-MS/MS fragmentation spectrum to the MSNovelist
  web service and receiving a JSON response containing ranked de-novo structure candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  tools:
  - MSNovelist
  - SIRIUS
  - RDKit
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans:
- The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-021-01045-9
  all_source_dois:
  - 10.1038/s41587-021-01045-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-json-parsing

## Summary

Parse and deserialize JSON-formatted spectral query responses from the MSNovelist web service into structured candidate structure records with SMILES, ranks, scores, and metadata. This skill bridges the gap between REST API output and downstream analysis by converting ranked structural predictions into a tabular or hierarchical format suitable for inspection, filtering, or further analysis.

## When to use

Apply this skill after submitting an LC-MS/MS fragmentation spectrum to the MSNovelist web service and receiving a JSON response containing ranked de-novo structure candidates. Use it when you need to extract and organize the returned candidate structures, scores, and associated metadata into a format compatible with chemical informatics pipelines or publication-ready tables.

## When NOT to use

- Input is a spectral library or reference database in mzML or mgf format—use spectral import and library search workflows instead.
- You have already imported the MSNovelist results into SIRIUS GUI or command-line tool, which handles JSON parsing automatically—redundant application.
- Query input does not include a molecular ion mass or valid MS/MS spectrum—MSNovelist requires these to generate candidates.

## Inputs

- JSON-formatted response from MSNovelist REST API endpoint (array of ranked candidate structures)
- Molecular ion mass (in the original query)
- Optional fragmentation spectrum data

## Outputs

- Structured JSON file (array of candidate records with SMILES, rank, score, metadata fields)
- CSV table with columns: SMILES, rank, score, and optional metadata (InChI, formula, confidence)
- Parsed RDKit molecule objects or canonical SMILES representations

## How to apply

Receive the JSON response from the MSNovelist REST API endpoint containing an array of ranked candidate structures, each with fields for SMILES string, rank integer, score value, and optional metadata (e.g., InChI, molecular formula, confidence). Iterate through the JSON array and extract each candidate's SMILES, rank, score, and metadata fields. Validate that SMILES strings are parseable by a cheminformatics library (e.g., RDKit) to catch malformed structures. Serialize the validated records into a structured output file (JSON array or CSV table) with rows ordered by rank and columns for SMILES, rank, score, and any supplementary metadata. Optional: filter candidates by score threshold or rank cutoff if only high-confidence predictions are needed for downstream analysis.

## Related tools

- **MSNovelist** (Web service that accepts molecular ion mass and fragmentation spectra and returns JSON-formatted ranked candidate structures.) — https://github.com/sirius-ms/sirius
- **SIRIUS** (Java-based framework that integrates MSNovelist web service and provides REST API client for submitting queries and receiving JSON responses; handles automatic JSON parsing in GUI and CLI modes.) — https://github.com/sirius-ms/sirius
- **RDKit** (Optional cheminformatics library for validating and canonicalizing SMILES strings extracted from parsed JSON.)

## Evaluation signals

- JSON response is successfully parsed without syntax errors; all required fields (SMILES, rank, score) are present in every candidate record.
- Output file (JSON or CSV) contains the same number of records as the input JSON response array.
- SMILES strings in the output are valid and parseable by RDKit (no truncation, encoding, or malformation).
- Rank field is a monotonically increasing integer (1, 2, 3, …) matching the sort order of candidates.
- Score field is a numeric value in the expected range (e.g., 0–1 or 0–100, depending on MSNovelist version) with no missing or non-numeric entries.

## Limitations

- JSON response structure and field names may vary between MSNovelist API versions; parsing logic must be adapted if the API schema changes.
- SMILES strings returned by MSNovelist may not be canonical or may differ from alternative valid SMILES representations; canonicalization via RDKit is recommended for comparison.
- No changelog or version history is documented in the repository; breaking changes to the JSON API may not be communicated in advance.
- MSNovelist web service is for academic research and education use only; non-academic users must obtain a license from Bright Giant GmbH and cannot rely on the free service.
- The skill assumes successful connectivity to the MSNovelist web endpoint and valid HTTP response; network failures, rate limiting, or service downtime are not handled.

## Evidence

- [other] Submit HTTP POST request to the MSNovelist web service with the prepared payload. 3. Retrieve JSON-formatted response containing ranked candidate structures and associated scores. 4. Parse and serialize the candidate structures into a structured output file (JSON or CSV) with fields for structure SMILES, rank, score, and metadata.: "Retrieve JSON-formatted response containing ranked candidate structures and associated scores. 4. Parse and serialize the candidate structures into a structured output file (JSON or CSV) with fields"
- [other] MSNovelist is offered as a web service component within the SIRIUS framework alongside CSI:FingerID and CANOPUS for scientific analysis.: "MSNovelist is offered as a web service component within the SIRIUS framework alongside CSI:FingerID and CANOPUS for scientific analysis."
- [readme] Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface.: "Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface."
- [readme] The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only"
