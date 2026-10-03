---
name: manifest-generation
description: Use when you maintain a local repository of biological sequences (such
  as MIBiG) and need to produce a searchable inventory that links local files to their
  metadata and external database availability status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3293
  tools:
  - Git
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/nar/gkz882
  title: MIBiG 2.0
evidence_spans:
- github.com/mibig-secmet/mibig-json
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_2_0_cq
    doi: 10.1093/nar/gkz882
    title: MIBiG 2.0
  dedup_kept_from: coll_mibig_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkz882
  all_source_dois:
  - 10.1093/nar/gkz882
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# manifest-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate a structured manifest (CSV or JSON) that documents sequence files, their metadata, and cross-referenced availability status against external databases. This skill is essential for tracking curation status and identifying sequences unavailable from canonical public repositories.

## When to use

Use this skill when you maintain a local repository of biological sequences (such as MIBiG) and need to produce a searchable inventory that links local files to their metadata and external database availability status. Specifically, apply it when you have parsed JSON or similar structured formats containing accession information and cluster status fields, and you need to compile that into a machine-readable manifest for auditing, reuse, or distribution.

## When NOT to use

- Input sequence files lack structured metadata or accession identifiers — manifest generation requires parseable linking information.
- NCBI connectivity or query rate limits prevent systematic cross-referencing — manifest will be incomplete or require manual verification.
- Your goal is to filter sequences *in place* rather than document them — use query and filtering skills instead.

## Inputs

- JSON metadata files containing cluster.status field and GenBank/RefSeq accession identifiers
- Local sequence file directory (e.g., genbanks directory)
- NCBI GenBank/RefSeq accession numbers to cross-reference

## Outputs

- Manifest CSV file with columns: filename, accession, availability_status, metadata_notes
- Manifest JSON file recording filename, accession, availability status, and curation metadata

## How to apply

After parsing JSON metadata from local sequence files to extract the cluster.status field and GenBank/RefSeq accession information, cross-reference each entry against NCBI GenBank/RefSeq databases to determine availability. Record filename, accession identifier, availability status (present/absent/restricted), and any metadata indicating why the sequence is unavailable from NCBI into a structured manifest. Use CSV for tabular distribution or JSON to preserve nested metadata structures. The manifest serves as both a discovery index and a quality-assurance record, enabling future agents to quickly identify which sequences exist only in your local repository.

## Related tools

- **Git** (Clone and access the mibig-json repository to retrieve local sequence files and JSON metadata) — github.com/mibig-secmet/mibig-json

## Evaluation signals

- Manifest contains one row per sequence file with no missing accession identifiers or cluster.status values.
- Cross-referencing against NCBI databases is complete: all accessions have been queried and marked as present, absent, or unavailable.
- Manifest structure is consistent (all rows have same number of columns in CSV; all JSON objects have identical key sets).
- Entries marked 'absent from NCBI' are traceable back to original JSON metadata with documented reasons (e.g., cluster.status='pending', 'removed', or 'private').
- Manifest is machine-parseable and reproducible: re-running the workflow with identical inputs produces identical output.

## Limitations

- NCBI GenBank/RefSeq databases are continuously updated; accession availability status may change between manifest generations, requiring periodic refresh.
- Cross-referencing is rate-limited by NCBI query policies; large manifests may require batching or caching strategies.
- Metadata quality depends on the completeness and accuracy of the upstream JSON files; missing or malformed accessions will result in incomplete or ambiguous manifest entries.
- No changelog is maintained in the mibig-json repository, so version history of the manifest or underlying data is not available for audit trails.

## Evidence

- [readme] The genbanks directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases.: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases"
- [readme] Entry status is tracked via the cluster.status field in JSON format.: "entry status is now tracked via the `cluster.status` field"
- [intro] Manifest documents filename, accession, availability status, and metadata.: "Compile a manifest CSV or JSON file recording filename, accession, availability status, and any metadata indicating why the sequence is unavailable from NCBI"
- [intro] Parse JSON metadata to extract cluster.status and accession information for each file.: "For each file, parse the JSON metadata to extract the cluster.status field and GenBank/RefSeq accession information"
- [intro] Cross-reference entries against NCBI to determine availability status.: "Cross-reference each entry against NCBI GenBank/RefSeq databases to determine availability status"
