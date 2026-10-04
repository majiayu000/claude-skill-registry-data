---
name: metabolights-study-search
description: Use this skill to search MetaboLights studies and resolve a compact summary for each matched accession through the official JSON API.
---

## Purpose
Search public metabolomics studies through the official MetaboLights API and summarize matched study metadata.

## When to use
- You need a lightweight metabolomics dataset-discovery starter.
- You want study accessions, titles, factors, and release metadata without manually browsing the portal.

## When not to use
- You need full ISA parsing for every assay, source, and sample table.
- You need raw metabolomics files or downstream analysis workflows.

## Inputs
- A free-text study query such as `diabetes`.
- Small page and row limits.

## Outputs
- A JSON summary with study accessions and compact metadata.

## Requirements
- Network access to `ebi.ac.uk`
- Python standard library only

## Provenance
- MetaboLights API Swagger UI: https://www.ebi.ac.uk/metabolights/ws/api/spec.html
