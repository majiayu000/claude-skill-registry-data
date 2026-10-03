---
name: data-quality-gating
description: Use when after curating and integrating structure-organism pairs from
  heterogeneous sources when you need to enforce quality thresholds before publishing
  or analyzing a reference dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0091
  tools:
  - R
  - 2_validating.R
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-quality-gating

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A validation filtering step that cross-references curated structure-organism pairs against organism, structure, and reference dictionaries to retain only high-confidence pairs meeting platinum-tier standards. This skill ensures that only pairs with complete metadata, consistent dictionary mappings, and resolved literature citations advance to downstream analysis.

## When to use

Apply this skill after curating and integrating structure-organism pairs from heterogeneous sources when you need to enforce quality thresholds before publishing or analyzing a reference dataset. Specifically use it when you have a curated table of candidate pairs and corresponding reference dictionaries (organism, structure, reference), and you want to identify and retain only those pairs that pass validation against all three dictionaries with no conflicting assertions.

## When NOT to use

- Input curated table has already been validated against reference dictionaries — skip to downstream analysis.
- Reference dictionaries are incomplete, outdated, or known to contain inconsistencies — delay gating until dictionaries are reconciled.
- Your use case requires retention of all curated pairs regardless of validation status (e.g., for sensitivity analysis) — use the full curated table instead.

## Inputs

- interim/tables/3_curated/table.tsv.gz (curated structure-organism pairs table)
- interim/dictionary/organism/dictionary.tsv.gz (organism reference dictionary)
- interim/dictionary/structure/dictionary.tsv.gz (structure reference dictionary)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference metadata)
- interim/dictionary/reference/metadata.tsv.gz (reference citation metadata)

## Outputs

- platinum.tsv.gz (validated high-confidence structure-organism pairs with validation flags and complete metadata)

## How to apply

Load the curated table (interim/tables/3_curated/table.tsv.gz) and the three reference dictionaries (organism, structure, reference) along with their metadata files into R. For each structure-organism pair in the curated table, perform a cross-reference lookup against the organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to verify that both the organism and structure identifiers are present and consistent. Then validate the reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) associated with each pair's literature citations. Apply inclusion filters to retain only pairs that meet platinum-tier standards: high-confidence mappings (no ambiguous or partial matches), complete metadata (all required columns populated), and no conflicting assertions across dictionaries. Write the passing pairs to platinum.tsv.gz, preserving all validation flags and metadata columns to enable downstream traceability.

## Related tools

- **R** (Execution environment for loading, cross-referencing, and filtering curated pairs against dictionaries; writing validated output table.) — https://www.r-project.org/
- **2_validating.R** (Script that implements the validation filter logic within the 3_analyzing stage of the LOTUS workflow.) — https://github.com/lotusnprod/lotus-processor

## Evaluation signals

- All rows in platinum.tsv.gz have non-null organism identifiers and structures that match entries in their respective reference dictionaries.
- No row in platinum.tsv.gz contains conflicting organism-structure assertions or partial/ambiguous mappings flagged during dictionary lookup.
- All reference metadata columns (literature citations, dictionaryOrganism links) are populated and resolved for 100% of output rows.
- Row count in platinum.tsv.gz is ≤ row count in curated input table (i.e., filtering removes or retains rows; never adds).
- Validation flags and metadata columns are preserved in platinum.tsv.gz output, enabling traceability of which pairs passed each validation gate.

## Limitations

- Gating quality depends entirely on completeness and accuracy of the three reference dictionaries; errors or gaps in those dictionaries will propagate to rejection decisions.
- High-confidence filtering may be overly stringent for exploratory analyses that tolerate incomplete metadata; consider retaining intermediate filtering tiers (e.g., silver or bronze collections) for relaxed thresholds.
- Conflicting assertions can only be detected if the reference dictionaries contain explicit conflict information; silent inconsistencies across dictionaries may not be caught.

## Evidence

- [other] The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output.: "The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output."
- [other] Cross-reference each structure-organism pair against organism dictionary and structure dictionary to verify presence and consistency, validate reference metadata for each pair's associated literature citations, and apply quality filters to retain only pairs meeting platinum-tier standards.: "Cross-reference each structure-organism pair against organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to"
- [methods] LOTUS is a comprehensive collection of documented structure-organism pairs originating from 31 initial open databases, with 588694 unique referenced structure-organism pairs and 231330 unique curated structures.: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs ... 231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms ... originating from 31 initial open databases"
- [methods] The 3_analyzing stage includes sampling and validation against dictionaries and metadata, producing platinum.tsv.gz.: "3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz"
