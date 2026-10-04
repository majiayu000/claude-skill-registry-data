---
name: pride-project-search
description: Use this skill to search PRIDE Archive v2 proteomics projects by keyword and return compact dataset-discovery summaries. Do not use it for raw file download orchestration or unsupported PRIDE endpoints.
---

## Purpose
Search PRIDE Archive v2 project metadata and summarize matching proteomics studies in a small stable JSON payload.

## When to use
- You need a quick proteomics dataset discovery entry point by keyword.
- You want PRIDE accessions, project titles, organisms, dates, and references before deeper analysis.

## When not to use
- You need raw file download planning or file-by-file manifest handling.
- You need peptide- or protein-level quantification results.
- You need large bulk exports.

## Inputs
- Keyword query
- Optional page and page size
- Optional output path

## Outputs
- JSON payload containing compact PRIDE project summaries with `accession`, `title`, `project_description`, `submission_type`, `publication_date`, `submission_date`, `updated_date`, `organisms`, `keywords`, `references`, `experiment_types`, and `project_url`.

## Requirements
- Python 3.10+
- Network access to `www.ebi.ac.uk`

## Procedure
1. Run `python3 skills/proteomics/pride-project-search/scripts/search_pride_projects.py --keyword phosphoproteomics --page-size 2 --out skills/proteomics/pride-project-search/assets/phosphoproteomics_projects.json`.
2. Inspect `projects` for `accession`, `title`, `project_description`, `submission_type`, `publication_date`, `submission_date`, `organisms`, `keywords`, and `references`.
3. Use the returned PRIDE accession in downstream dataset or literature workflows.

## Validation
- Command exits successfully.
- Output contains at least one `PXD...` accession for a known keyword.
- Each project summary includes a non-empty `title`.

## Failure modes and fixes
- No hits: broaden the keyword or try a better-known assay term.
- Unexpected payload shape: confirm the PRIDE Archive v2 search endpoint is still returning project lists.
- Need file manifests: build a separate PRIDE file-level skill instead of overloading this one.

## Safety and limits
- Metadata discovery only.
- This skill does not download raw data or interpret proteomics results.

## Example
- `python3 skills/proteomics/pride-project-search/scripts/search_pride_projects.py --keyword phosphoproteomics --page-size 2`

## Provenance
- PRIDE Archive API docs: https://www.ebi.ac.uk/pride/ws/archive/
- Search endpoint used by this skill: `https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects`

## Related skills
- `ebi-proteins-entry-summary`
