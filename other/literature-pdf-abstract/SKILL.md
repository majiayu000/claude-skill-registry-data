---
name: literature-pdf-abstract
description: Extract traceable metadata and abstract-level notes from local PDF first pages or covers without claiming full-text review.
---

# PDF First Pages and Abstracts

Read [shared contract](../../references/shared-contract.md) and [record schema](../../references/records.md). This module handles PDF evidence, not Zotero metadata screening or WoS citation analysis.

1. Run `ingest.py --input INPUT --output OUTPUT --backend pdfium`. Check actual page counts and text quality.
2. Find the article page rather than assuming PDF page 1; publisher/ResearchGate covers may precede it. Render ambiguous pages with render_pages.py; use OCR only when needed and compare author affiliations visually.
3. Read title, author line, affiliations, abstract and original keywords. Write curated*.json with source_sha256, source_page and per-field evidence. Themes are model-inferred; original keywords stay separate. Do not record editors or funding bodies as affiliations.
4. Run build_catalog.py with --scope first_page or abstract, then verify_catalog.py. Empty institution lists are valid when the provided page lacks them.
5. Deliver structured JSON and per-paper notes. Route requested XLSX/CSV to literature-export and figures to literature-figures. Full-text requests belong to literature-deep-read.
