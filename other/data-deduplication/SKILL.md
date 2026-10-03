---
name: data-deduplication
description: Use when after parsing and validating a .csv file containing comma-separated
  SMILES strings, and before formatting the molecule list for CypReact input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3314
  tools:
  - RDKit
  - pandas
  - CypReact
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  dedup_kept_from: coll_cypreact_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-deduplication

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove duplicate molecular structures from a parsed dataset of SMILES strings before submission to CypReact. Deduplication ensures that redundant molecules are not processed multiple times, reducing computational overhead and preventing inflated result sets.

## When to use

After parsing and validating a .csv file containing comma-separated SMILES strings, and before formatting the molecule list for CypReact input. This is essential when the source file may contain repeated SMILES representations of the same molecule, which would otherwise result in duplicate predictions across CYP isoforms.

## When NOT to use

- The input SMILES file has already been deduplicated by the source provider (e.g., curated database with unique entries)
- Isobaric or stereoisomeric variants are intended to be retained as separate entries in the CypReact analysis
- The workflow requires tracking all occurrences (e.g., for epidemiological or frequency-weighted analyses)

## Inputs

- Parsed SMILES dataset (pandas DataFrame or JSON object)
- Validated SMILES strings with metadata fields
- Molecule identifier or index column (optional)

## Outputs

- Deduplicated SMILES dataset (CSV or JSON format)
- Deduplicated molecule count and metadata
- Deduplication report (optional: list of removed duplicates)

## How to apply

Load the validated SMILES dataset into a pandas DataFrame or equivalent structure. Identify duplicate SMILES strings using exact string matching (case-sensitive) or canonical SMILES normalization via RDKit to account for alternative notation of the same structure. Remove duplicates while preserving the first occurrence or a representative entry with associated metadata. Optionally, track and log the number and identities of removed duplicates for quality-control reporting. Output the deduplicated molecule list in the same structured format (DataFrame or JSON) compatible with CypReact input specifications.

## Related tools

- **RDKit** (Validate SMILES syntax and normalize to canonical form for comparison-based deduplication)
- **pandas** (Load CSV, perform duplicate detection via drop_duplicates(), and export deduplicated DataFrame)
- **CypReact** (Accepts deduplicated .csv or .sdf files as input for CYP metabolism prediction) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
import pandas as pd
df = pd.read_csv('molecules.csv')
df_dedup = df.drop_duplicates(subset=['SMILES'])
df_dedup.to_csv('molecules_dedup.csv', index=False)
```

## Evaluation signals

- Deduplicated dataset row count is equal to or less than the input count; difference equals the number of removed duplicates
- All SMILES strings in the output are unique when compared by exact match or canonical form
- Metadata integrity is preserved: no rows are corrupted, truncated, or have missing fields after deduplication
- CypReact processes the deduplicated .csv without errors and produces one result entry per unique molecule
- Deduplication log (if generated) lists all removed duplicate entries with their counts, totaling to input − output row difference

## Limitations

- Deduplication by exact SMILES string match may miss equivalent structures with alternative SMILES notations; canonical SMILES normalization via RDKit is recommended but adds computational overhead
- Stereoisomers and tautomers represented by distinct SMILES are not detected as duplicates; domain knowledge or explicit tautomer rules are needed to resolve these
- Large datasets (millions of molecules) may require memory-efficient deduplication strategies (e.g., set-based or streaming algorithms) not covered by simple pandas operations
- No changelog or version history available for CypReact to document whether deduplication behavior has changed across releases

## Evidence

- [other] Extract and deduplicate the molecule list: "Extract and deduplicate the molecule list."
- [intro] CSV format with comma-separated SMILES: "If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [other] Validation and structured data formatting: "Validate each SMILES string for syntactic correctness using RDKit or equivalent molecular structure validator."
- [other] Output format compatibility: "Format the parsed molecule list as a structured data object (DataFrame or JSON) compatible with CypReact input specifications."
