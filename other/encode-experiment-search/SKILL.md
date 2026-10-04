---
name: encode-experiment-search
description: Use this skill to search ENCODE experiments by assay or free-text keyword and return compact metadata summaries for public epigenomics records.
---

## Purpose
Search the official ENCODE portal for public experiment metadata and summarize a small result set.

## When to use
- You need a quick ENCODE metadata search starter.
- You want public assay, biosample, and accession metadata for epigenomics planning or triage.

## When not to use
- You need raw file downloads or workflow execution.
- You need full ENCODE schema coverage instead of a compact summary.

## Inputs
- A free-text search term such as `ATAC-seq`.
- A small result limit.

## Outputs
- A JSON summary with ENCODE experiment accessions and key metadata fields.

## Requirements
- Network access to `encodeproject.org`
- Python standard library only

## Provenance
- ENCODE REST API documentation: https://www.encodeproject.org/help/rest-api/
