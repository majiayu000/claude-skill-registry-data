---
name: review-25-zotero-pdf-pipeline
description: Screen candidate papers, classify inclusion status, obtain or flag PDFs, prepare RIS/NBIB exports for Zotero, and use Zotero metadata/full text for evidence-based medical review writing. Use when papers cannot be downloaded, when deciding which references enter Zotero, when importing literature into Zotero, or when Codex should continue writing from Zotero evidence.
---

# Review 25 Zotero PDF Pipeline

## Overview

Use this skill after literature search and before deep writing. The goal is to separate search hits from usable evidence: not every found paper is readable, relevant, high quality, or safe to cite.

For Chinese users, explain decisions in Chinese. Keep stable tags and table field names in English when useful for Zotero, CSV, or Excel.

## Core Principle

Do not treat a paper as fully usable until its metadata, relevance, quality, and full-text status are known. If only the abstract is available, use it only for background screening unless the claim is simple and explicitly abstract-supported.

## Pipeline

### 1. Candidate Pool

Start from PubMed, Crossref, Web of Science, Semantic Scholar, OpenAlex, journal pages, or `review-23-reference-curator` outputs.

Minimum fields:

- title
- authors
- year
- journal
- PMID
- DOI
- abstract
- article type
- source database
- candidate claim or section

### 2. Screening Levels

Assign each paper one decision:

- `core_include`: must read and likely cite.
- `background_include`: useful for context, not central evidence.
- `table_candidate`: contains extractable data for a table.
- `figure_source`: contains a mechanism, pathway, schema, or dataset useful for figure planning.
- `maybe`: needs full-text check.
- `exclude`: not relevant, low quality, wrong population/model, wrong article type, old without justification, missing DOI/PMID, or user-excluded journal.

Record exclusion reasons. Do not silently drop papers.

### 3. PDF Acquisition Tiers

Use legal and traceable routes:

1. PubMed Central or Europe PMC open full text.
2. Publisher open access PDF.
3. Institutional access or link resolver if configured.
4. Zotero Connector from browser.
5. Author manuscript, repository, or preprint only if it matches the cited version or is clearly labeled.
6. Manual request or mark as unavailable.

Do not rely on unauthorized access routes. If full text cannot be obtained, mark `pdf_status = missing`.

### 4. Missing PDF Policy

For each missing PDF, choose:

- `replace`: if a better accessible paper exists.
- `abstract_only_background`: if abstract supports only broad context.
- `manual_fetch_needed`: if the paper is central or table data are needed.
- `drop`: if the paper is not essential.

Never extract detailed numeric results, figure content, methods, or nuanced claims from a paper that has not been read in full.

### 5. Zotero Import And Codex Reading

If an import/write tool is available, use it. If not, prepare an import file and user-facing import route:

- PubMed NBIB for PubMed records.
- RIS for Zotero/EndNote/Mendeley.
- DOI list for Zotero magic-wand lookup.
- CSV/Excel for screening logs.

After import, Codex can use Zotero tools when available:

- Search Zotero by title, author, year, DOI, or tags.
- Read Zotero metadata.
- Read Zotero full text when an attachment exists and is indexed.

Do not claim that Codex imported items into Zotero unless a write/import tool actually did so.

### 6. Zotero Tags

Recommended tags:

- `review-topic-[shortname]`
- `core_include`
- `background_include`
- `table_candidate`
- `figure_source`
- `pdf_available`
- `pdf_missing`
- `fulltext_read`
- `claim_checked`
- `replace_needed`
- `do_not_use`

### 7. Evidence Handoff To Writing

Before `review-24` or section writing continues, produce:

- `zotero_screening_log.csv`
- `pdf_status_table.csv`
- `core_reading_queue.md`
- `section_evidence_map.csv`

Each core paper should have:

- one-sentence usable finding
- claim it supports
- evidence level
- PMID
- DOI
- full-text status
- Zotero key if available

## Output Format

Return:

1. Screening summary.
2. Included papers by role.
3. Missing PDF list with action.
4. Zotero import/read plan.
5. Next writing handoff.

## Reference File

Read `references/pdf-zotero-gates.md` when deciding whether a paper can be cited, table-extracted, figure-adapted, or only used for background.
