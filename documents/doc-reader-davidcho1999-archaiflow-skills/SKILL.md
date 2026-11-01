---
name: doc-reader
description: "Reads a non-drawing project PDF and answers questions about it: a specification, a code excerpt, a contract, a consultant report, or correspondence from an authority. Summarises, locates a clause, extracts values, or lists comments, and cites section and page for every claim it makes. Trigger on \"read this spec\", \"what does this document say\", \"summarize this report\", \"find clause X\", \"what is the authority asking for\", or a pasted path to a non-drawing project PDF. For drawing sheets use drawing-reader instead. Detects the document type, asks what is wanted before reading at length, and never answers from what a document of that kind usually says. Writes a per-read summary that points back at the source."
license: MIT
metadata:
  title: "Doc Reader"
  summary: "Read and interpret a specification, report, or contract PDF"
  discipline: "construction-admin"
  tags: "Design"
---


# Doc Reader


## Overview


Read and interpret a non-drawing AEC document PDF. The user drops in a spec book, a code chapter, an AIA contract, a geotech / structural / energy report, or an AHJ letter — and asks Claude to interpret it: summarize, find a specific section, extract key values, list comments, locate a clause, etc.


This skill is the **non-drawing sibling** of `drawing-reader`. It uses the same router pattern: detect document type → confirm with the user → ask intent → route to the appropriate read pattern. Output lives in `docs/doc-reads/` so each read is captured for the project record.


For drawing PDFs (single sheet, set, redline, record, shop, detail), use `drawing-reader` instead.


## Scope and limits — read first


This skill covers:

- **Specifications** — CSI MasterFormat 2020 organized 3-part sections (Part 1 General, Part 2 Products, Part 3 Execution).
- **Codes** — IBC, IRC, IECC, NFPA, ADA, ICC A117.1, ASCE 7 (chapter or full).
- **AIA contracts** — B101 (Owner-Architect), A201 (General Conditions), C401 (Architect-Consultant), G-series (administrative).
- **Reports** — geotech, structural calc, energy modeling output, daylight study, acoustic study, environmental site assessment.
- **AHJ correspondence** — plan-check comment letters, RFI responses, NOTC (Notice of Final Construction), permit conditions.

This skill does **NOT** cover:

- **Drawing PDFs** — single sheet, set, redline, record, shop, detail. Use `drawing-reader` instead.
- **DWG / RVT / IFC native files** — PDFs only.
- **Producing new documents** — reads existing documents, does not generate them.
- **Compliance verification** ("does this spec meet code") — that's `ada-tracker` / `code-analysis-builder` / etc.
- **Quantitative validation** of report calculations — read-only; user must verify calc validity.
- **Strategic interpretation** ("is this a good spec") — describe only.
- **Foreign / non-NA standards** (BS, EU, JIS, KS) — NA AEC focus only.

## When to use


Trigger on:

- "Read this spec PDF: <path>."
- "What does IBC say about <topic>?"
- "Summarize this geotech report."
- "Find clause 3.10 in the contract."
- "What does the AHJ want me to fix?"
- Pasted path to a non-drawing AEC PDF.

Do NOT trigger on:

- Drawing PDFs — use `drawing-reader`.
- "Score this LEED scorecard" — use `leed-tracker`.
- "Generate the code analysis from program data" — use `code-analysis-builder`.
- "Translate this spec for the contractor" — use `client-translator`.
- "Make a checklist from this spec" — use `submittal-log-builder`.

## Workflow


### Step 1 — Bootstrap if needed


Check whether `docs/doc-reads/index.md` exists. If not, create:


```bash
mkdir -p docs/doc-reads/.cache
```


And write a minimal index header (no script ships with this skill — keep it lean):


```markdown
# Doc Reads — Project Log

| Date | Source PDF | Doc Type | User Intent | Output |
|------|------------|----------|-------------|--------|
```


If `docs/` does not exist, confirm with the user before creating.


### Step 2 — Inventory the PDF


Use the `Read` tool to look at the first 2 pages of the document PDF. Note:

- Total page count (from PDF metadata if available, otherwise approximate).
- Page size + orientation (8.5×11 portrait is most common for non-drawings).
- Whether the first page looks like a spec section header, a code chapter, an AIA contract title page, a report cover, or a letter.

If the PDF is large (> 100 pages), tell the user up front and confirm before reading more — vision reads are token-heavy.


### Step 3 — Detect document type


Use `references/document-types.md` to classify the PDF as one of:

- **Specification (CSI section)** — formatted as Part 1/2/3, MasterFormat number (e.g. `08 14 16` Wood Doors), specifier signature block.
- **Code excerpt** — chapter or section heading (e.g. `Chapter 10 — Means of Egress`, `§1006.2.1`), code year on cover.
- **AIA contract** — AIA logo, document code (e.g. `AIA Document B101™ – 2017`), Owner / Architect signature blocks.
- **Report** — cover with project name, report title (e.g. "Geotechnical Investigation Report"), preparer firm, date, table of contents.
- **AHJ letter** — agency letterhead (NYC DOB, CA HCAI, etc.), comment-by-comment numbered list, action-required column.

State the detected type explicitly to the user. Ask them to confirm or correct before proceeding.


### Step 4 — Confirm user intent


Ask the user what they want from the document. Use `references/read-patterns.md` to map common intents to handling:

- "Summarize" → high-level prose summary, key findings, page count, table of contents excerpt.
- "Find section/clause X" → locate by CSI / IBC / AIA reference, render that page, quote verbatim.
- "Extract key values" → numerical / parameter extraction (geotech soil bearing, energy model EUI, structural loads, ADA dimensions).
- "List AHJ comments" → tabulate comments + action required + responsible party + due date.
- "What does <code section> require" → verbatim quote with §X.Y.Z citation.
- "What does <contract clause> say" → verbatim quote with AIA section + paragraph.

If the user's intent doesn't fit a specialized pattern, handle directly via vision read.


### Step 5 — Read or delegate


If delegating: inform the user that the request is better handled by `<other-skill>` and stop there (or suggest installing it via `npx archtmpl@latest --skill <other-skill>`).


If reading directly: open the relevant pages, vision-read for the user's intent, and produce the output. For multi-section queries, batch reads (e.g. read 5 pages at a time) to keep within token budget.


### Step 6 — Write the output


Write `docs/doc-reads/<read-slug>.md` with:

- Header: source PDF path, doc type, user intent, date.
- Body: the read result (summary, quoted clause, extracted values, comment table, etc.).
- Citations: page number AND the document's native reference (CSI section number / IBC §X.Y.Z / AIA section + paragraph / report page + section).
- Confidence flag (`high` for verbatim text, `medium` for inferred / paraphrased, `low` for vision approximation of dense tables).

Slug rule: `YYYY-MM-DD_<short-intent-tag>` (e.g. `2026-05-08_ibc-egress-1006`).


### Step 7 — Update the project log


Append one row to `docs/doc-reads/index.md`:


```bash
echo "| 2026-05-08 | <pdf-path> | <type> | <intent> | <output-md> |" >> docs/doc-reads/index.md
```


### Step 8 — Report


Tell the user:

- Path to the read output `.md`.
- Confidence summary (how many claims are `high` vs `medium` vs `low`).
- Caveats — any sections too dense to read fully, any clauses that referred outward (e.g. "see §1006.3" not in the bundled excerpt).
- If a more specialized skill applies for follow-up, name it.

## Rules

- Every quoted clause / value must cite the document's native reference (CSI section, IBC §X.Y.Z, AIA section + paragraph, report page + section). Bare-page-number-only is insufficient.
- Verbatim quotes must be reproduced exactly — no paraphrasing of code text or contract text without flagging it.
- Confidence flag (`high` / `medium` / `low`) is required on every extracted value or claim.
- Document type classification must come from `references/document-types.md` recognition signals — not invented.
- When delegating, name the specific skill and stop — do not partially do that skill's work inline.
- Output files live in `docs/doc-reads/` of the user's project.

## Anti-patterns

- Reading 500 pages of a spec book without confirming with the user first. Token-heavy reads must be authorized.
- Paraphrasing code text or contract clauses. Verbatim or flag.
- Treating drawings (NCS-titleblock PDFs) as documents. They are not — use `drawing-reader`.
- Inventing CSI / IBC / AIA section numbers when the document's own numbering is unclear. Mark as "UNKNOWN" and flag.
- Compliance judgments ("this spec meets ADA"). The skill quotes; specialized trackers verify.
- Strategic / qualitative judgments ("this is a strong spec"). Describe only.
- Doing partial work that belongs to specialized skills (`leed-tracker`, `ada-tracker`, `submittal-log-builder`).

## Resources

- `references/_provenance.md` — sources for document-type recognition + AEC document conventions
- `references/document-types.md` — recognition signals for 5 doc types (spec / code / contract / report / AHJ letter) + typical user requests per type
- `references/read-patterns.md` — user-intent → handling pattern mapping (delegation rules + direct-read recipes)
