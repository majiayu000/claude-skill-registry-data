---
name: ebi-proteins-entry-summary
description: Use this skill to fetch a compact accession summary from the EBI Proteins API. Do not use it for bulk downloads, unsupported endpoints, or full protein annotation export.
---

## Purpose
Resolve a protein accession through the EBI Proteins API and return a compact protein summary with names, organism, sequence size, keywords, and a small subset of comments and features.

## When to use
- You already know a protein accession such as `P38398`.
- You want a quick official protein summary before deeper proteomics or protein-biology work.

## When not to use
- You need bulk UniProt-scale exports.
- You need peptide evidence tables or full annotation payloads.
- You need offline execution.

## Inputs
- Protein accession
- Optional output path

## Outputs
- JSON payload containing a compact protein-entry summary

## Requirements
- Python 3.10+
- Network access to `www.ebi.ac.uk`

## Procedure
1. Run `python3 skills/proteomics/ebi-proteins-entry-summary/scripts/fetch_protein_summary.py --accession P38398 --out skills/proteomics/ebi-proteins-entry-summary/assets/brca1_protein_summary.json`.
2. Inspect `recommended_name`, `gene_names`, `organism_scientific_name`, `sequence_length`, `keywords`, `comments`, and `features`.
3. Use the compact summary as a lookup layer before downstream structural or proteomics workflows.

## Validation
- Command exits successfully.
- Output contains the requested accession and a non-empty recommended protein name.
- Known human accessions report the correct organism and a positive sequence length.

## Failure modes and fixes
- HTTP 404: confirm the accession exists and is public.
- Empty optional fields: some accessions have sparse comments or features; use the stable core fields first.
- Need bulk access: build a separate batch-oriented skill instead of overloading this single-entry helper.

## Safety and limits
- Metadata lookup only.
- This skill does not perform protein design, therapeutic recommendation, or wet-lab planning.

## Example
- `python3 skills/proteomics/ebi-proteins-entry-summary/scripts/fetch_protein_summary.py --accession P38398`

## Provenance
- EBI Proteins API docs: https://www.ebi.ac.uk/proteins/api/doc/

## Related skills
- `pride-project-search`
- `rcsb-pdb-entry-summary`
