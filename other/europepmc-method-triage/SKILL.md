---
name: europepmc-method-triage
description: Use this skill to search life-science literature through Europe PMC when you need publication metadata oriented toward biomedical method triage. Do not use it when you need offline execution or cluster-scale batch processing.
---

## Purpose
Search Europe PMC and capture structured records for biomedical literature triage and method discovery.

## When to use
- You need PubMed-adjacent life-science coverage.
- You want a method-search corpus with stable JSON output.

## When not to use
- You need complete full-text retrieval.
- You are working without network access.

## Inputs
- Query string
- Optional `--page-size`, `--sort`, and `--out`

## Outputs
- Europe PMC JSON search payload

## Requirements
- Python 3.13+
- Network access to `www.ebi.ac.uk`

## Procedure
1. Run `python3 skills/scientific-knowledge/europepmc-method-triage/scripts/search_europepmc.py --query "single-cell RNA-seq" --page-size 5 --out skills/scientific-knowledge/europepmc-method-triage/assets/europepmc_single_cell.json`.
2. Review the `hitCount` and the first page of `resultList.result`.
3. Refine the query for organism, assay, benchmark, or package terms.

## Validation
- Command exits successfully.
- Output JSON contains `hitCount`.
- At least one result is returned for a common biomedical topic.

## Failure modes and fixes
- Empty result set: switch to broader biomedical wording.
- API timeout: reduce `--page-size` and retry.

## Safety and limits
- Use for literature discovery, not for unsafe operational biological guidance.
- Respect service limits and article-specific rights.

## Examples
- `python3 .../search_europepmc.py --query "spatial transcriptomics benchmark" --page-size 3`

## Provenance
- Europe PMC RESTful Web Service: https://europepmc.org/RestfulWebService
- Europe PMC Annotations API: https://europepmc.org/annotations_api

## Related skills
- `openalex-literature-search`
