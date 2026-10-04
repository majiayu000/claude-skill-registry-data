---
name: reactome-event-summary
description: Use this skill to fetch a concise summary for a known Reactome event or pathway stable ID from the official Reactome Content Service. Do not use it for full pathway traversal, graph expansion, or unsupported Reactome endpoints.
---

## Purpose
Fetch a compact JSON summary for a known Reactome stable ID by calling the official Content Service `data/query/<stable-id>` endpoint.

## When to use
- You already know the Reactome stable ID, such as `R-HSA-141409`.
- You want a lightweight event or pathway summary with the display name, species, compartment, and summary text.

## When not to use
- You need pathway membership expansion or contained-event traversal.
- You need bulk downloading or unsupported Reactome endpoints.

## Inputs
- Reactome stable ID
- Optional output path

## Outputs
- A JSON summary derived from `https://reactome.org/ContentService/data/query/<stable-id>`

## Requirements
- Python 3.10+
- Network access to `reactome.org`

## Procedure
1. Run `python3 skills/systems-biology/reactome-event-summary/scripts/fetch_reactome_event_summary.py --stable-id R-HSA-141409 --out skills/systems-biology/reactome-event-summary/assets/r_hsa_141409_summary.json`.
2. Inspect the output fields: `display_name`, `schema_class`, `species`, `compartments`, and `summary_text`.
3. If the stable ID is unknown or invalid, retry with a confirmed public Reactome ID.

## Validation
- Command exits successfully.
- Output JSON contains the requested `stable_id` and a non-empty `display_name`.

## Failure modes and fixes
- HTTP 404: confirm the stable ID exists and is public in Reactome.
- Empty summary text: some records omit `summation`; rely on the other metadata fields.
- Need deeper traversal: build a separate skill around a documented Reactome endpoint first.

## Safety and limits
- This skill only uses the documented stable-ID query surface.
- It summarizes one Reactome record at a time and does not resolve downstream pathway structure.

## Example
- `python3 skills/systems-biology/reactome-event-summary/scripts/fetch_reactome_event_summary.py --stable-id R-HSA-141409`

## Provenance
- Reactome Content Service docs: https://reactome.org/dev/content-service

## Related skills
- `ncbi-pubmed-search`
