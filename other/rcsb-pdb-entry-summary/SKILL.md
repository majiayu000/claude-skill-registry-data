---
name: rcsb-pdb-entry-summary
description: Use this skill to fetch a canonical RCSB PDB entry record by accession when you need quick structural metadata. Do not use it for search ranking or full structure parsing pipelines.
---

## Purpose
Fetch a structure entry summary from the official RCSB data API using a PDB ID.

## When to use
- You already know the PDB accession.
- You want a small, official structural metadata payload.

## When not to use
- You need text search across the whole archive.
- You need atom-level coordinate processing.

## Inputs
- PDB entry ID
- Optional output path

## Outputs
- JSON payload from `data.rcsb.org/rest/v1/core/entry/<id>`

## Requirements
- Python 3.13+
- Network access to `data.rcsb.org`

## Procedure
1. Run `python3 skills/structural-biology/rcsb-pdb-entry-summary/scripts/fetch_pdb_entry.py --entry-id 4HHB --out skills/structural-biology/rcsb-pdb-entry-summary/assets/4hhb_entry.json`.
2. Review the returned title, resolution, and audit fields.
3. Use related RCSB endpoints later for deeper polymer or assembly inspection.

## Validation
- Command exits successfully.
- Output includes top-level entry metadata for the requested PDB ID.

## Failure modes and fixes
- 404 or empty data: confirm the accession exists and is current.
- Need archive search: use the RCSB search API in a later, separate skill.

## Safety and limits
- Metadata lookup only.
- This skill does not download coordinate files or run structural analysis.

## Examples
- `python3 .../fetch_pdb_entry.py --entry-id 1STP`

## Provenance
- RCSB data API docs: https://data.rcsb.org/redoc/index.html

## Related skills
- `ensembl-gene-lookup`
