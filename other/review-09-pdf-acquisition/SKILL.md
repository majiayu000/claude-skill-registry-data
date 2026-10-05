---
name: review-09-pdf-acquisition
description: Track full-text PDF acquisition for included or high-priority references. Use when downloading, locating, naming, and auditing PDFs for evidence extraction.
---

# Review 09 PDF Acquisition

## Purpose

Make sure full texts are available for any paper used to support manuscript claims.

## Required Inputs

- Classified reference list.
- Zotero library status.
- User-provided PDFs or institutional access notes.

## Output

Create `06_pdf_fulltext/pdf_manifest.csv` with:

- Citation key.
- DOI/PMID.
- PDF filename.
- Source.
- Access status.
- Missing reason.
- Copyright/use note for figures if relevant.

## Completion Gate

Pass only when all high-priority included papers are either available as full text or explicitly marked missing.

## Stop Rules

Do not use inaccessible full texts as evidence beyond title/abstract-level statements.
