---
name: nyc-zoning-lookup
description: "This skill should be used when the user asks NYC-specific zoning questions and wants citation-backed answers from the NYC Zoning Resolution. Trigger on NYC zoning terms (FAR, lot coverage, setback, side/rear yard, sky exposure plane, height factor, dwelling unit factor, use group, accessory use), district codes (R1-R10, C1-C8, M1-M3), Special Districts (Special Hudson Yards District, Special West Chelsea District, etc.), or direct §X-XX citation requests. Downloads the official NYC ZR Complete PDF (~100 MB) on first use, caches a section-to-page outline at ~/.archtmpl/pdfs/nyc-zoning/, and answers each query by reading targeted pages and citing them as `§X-XX, p.N`. Operates with zero external dependencies — no Python, no embeddings, no API key beyond Claude Code subscription. Do NOT trigger for non-NYC zoning (use zoning-summary) or NYC Building Code questions (different document)."
license: MIT
metadata:
  title: "NYC Zoning Lookup"
  summary: "Answer NYC zoning questions with citations"
  discipline: "code-life-safety"
  jurisdiction: "New York City"
  tags: "Compliance"
---


# NYC Zoning Lookup


## Overview


Answer questions about the New York City Zoning Resolution by downloading the official combined PDF (~100 MB, ~1700 pages) once, building a section-to-page outline, and reading the targeted pages on demand. Every answer quotes the relevant clause and cites it with section number and page (e.g., `§23-145, p.142`). The skill operates with zero external dependencies — only Claude Code's built-in Bash and Read tools.


## Scope and limits — read first


**What this does.** Downloads the official Zoning Resolution once, builds a
section-to-page outline from its table of contents, then answers each question
by reading the pages that hold the answer and quoting them. Every value comes
back with a section and a page: `§23-145, p.142`.

**What this does not do.**

- **It does not answer from memory.** Every FAR, height, yard, setback, and use
  group is quoted out of the cached PDF. When the sections checked do not hold
  the answer it names the sections it read and stops, rather than assembling a
  plausible one.
- It does not cover zoning outside New York City. Any other municipality is
  `zoning-summary`.
- It does not cover the NYC Building Code, the Multiple Dwelling Law, the
  Housing Maintenance Code, or the Administrative Code. Different documents,
  different citations, and confusing them is the common failure here.
- It does not tell you a lot's zoning district. That is a DCP zoning map or GIS
  lookup; the Resolution holds text and tables, not maps.
- It does not know about an amendment made after the cache date. That date sits
  in the outline header and is reported with any answer that could turn on it.
- It does not file with DOB, CPC, or BSA, and it does not advise on variance or
  special permit procedure.

**What you need before starting.** Network access and roughly 100 MB of disk for
the first run, and the district or section you are asking about. If you do not
know the parcel's district yet, that comes from the DCP zoning map first.

## When to use


Trigger on:

- NYC-specific zoning terms: FAR, lot coverage, setback, side/rear/front yard, sky exposure plane, height factor, dwelling unit factor (DUF), use group, accessory use, community facility, daylight evaluation.
- District codes: R1–R10 residence, C1–C8 commercial, M1–M3 manufacturing, contextual variants (R6A, R6B, etc.), commercial overlays (C2-4 over R6, etc.).
- Special District names: Special Hudson Yards District, Special West Chelsea District, Special Midtown District, Special Garment Center District, etc.
- Direct citation requests: `what does §23-145 say`, `look up ZR Article II Chapter 3`, `Special Permit §74-71`.
- ZR text amendments referenced by NYC DOB, DCP, or BSA filings.

Do NOT trigger for:

- Non-NYC zoning (any other US city or Canadian municipality) — use `zoning-summary`.
- NYC Building Code (Title 28) questions — different document, different lookup.
- DCP zoning maps / GIS lookups (current zoning of a specific lot, rezoning history) — the ZR PDF has text and tables, not maps.
- NYC Multiple Dwelling Law, Housing Maintenance Code, NYCEEC — different documents.
- Procedural questions about how to file a variance, special permit, or text amendment with BSA / CPC — those belong elsewhere.

## Workflow


### Step 1 — Check the cache


Run:


```bash
test -f ~/.archtmpl/pdfs/nyc-zoning/zr-complete.pdf \
  && test -f ~/.archtmpl/pdfs/nyc-zoning/outline.md \
  && echo cached || echo missing
```


If `cached`, skip to Step 4. If `missing`, run Steps 2 and 3.


### Step 2 — Download the NYC ZR Complete PDF (first time only)


```bash
mkdir -p ~/.archtmpl/pdfs/nyc-zoning
curl -fSL --progress-bar \
  "https://zoningresolution.planning.nyc.gov/sites/default/files/article/Zoning%20Resolution%20Complete.pdf" \
  -o ~/.archtmpl/pdfs/nyc-zoning/zr-complete.pdf
```


Verify:


```bash
file ~/.archtmpl/pdfs/nyc-zoning/zr-complete.pdf   # expect: "PDF document"
ls -lh ~/.archtmpl/pdfs/nyc-zoning/zr-complete.pdf  # expect: ~95–100 MB
```


If the file is below 50 MB or `file` reports anything other than `PDF document`, the URL likely returned an error or redirect. Stop and report — do not proceed with a corrupt cache.


### Step 3 — Build the section-to-page outline (first time only)


The NYC ZR is organized as 14 Articles, each with multiple Chapters and numbered §X-XX sections (where the first digit is the Article number for Articles I–IX, and the first two digits for Articles X–XIV).


Locate the Table of Contents:

- Use the Read tool with `pages: "1-15"` to find the TOC or `Article Listing`.
- If not in the first 15 pages, scan in chunks (`pages: "15-35"`, `"35-60"`) until the TOC is located.

Read the full TOC across whatever page range it occupies. Extract every Article heading, every Chapter heading within each Article, and every numbered §X-XX section with its starting page.


Write `~/.archtmpl/pdfs/nyc-zoning/outline.md` with sections like:


```javascript
# NYC Zoning Resolution — Outline
Total pages: <N>
Last cached: <YYYY-MM-DD>

## Article I — General Provisions — pp. X–Y
### Chapter 1 — Title, Establishment of Districts and Incorporation of Maps — pp. X–Y
- §11-00 Title — p. X
- §11-10 Establishment of Districts — p. X
```


Skip detailed sub-paragraph numbering like `(a)(2)(i)` — those are reached by reading the section's pages, not by indexing.


If the document's TOC is incomplete or non-standard, fall back to extracting Article and Chapter headings only, by sampling every 30–50 pages and recording the first §X-XX section number on each sampled page. Note this fallback approach in the outline header.


### Step 4 — Answer the user's question


For each question:

1. **Re-read the outline.** Always start by reading `~/.archtmpl/pdfs/nyc-zoning/outline.md` to refresh the section map.
2. **Identify the 1–3 most relevant §X-XX sections.** State them explicitly before reading. Use `references/zr_structure.md` to map the question topic to the likely Article and Chapter. Examples:
    - `Max FAR in R6` → §23-145 (R6 bulk regulations) and §23-15X (height-factor alternative).
    - `Side yard for R5 detached` → §23-462 (side yards in R3–R5).
    - `Use Group 6 in C2` → §32-15 (use groups by district).
    - `Special Hudson Yards bulk` → §93-2X (Article IX).
3. **Read those pages with the Read tool.** Stay within the 20-page-per-call limit; chunk across calls if needed.
4. **Quote the relevant clause verbatim and cite it.** Use the format defined in `references/citation_format.md`:
    > `<exact quoted text from the ZR>`
    > 
    > — §23-145, p.142
5. **If the answer is missing, expand once.** Read the adjacent sections (one more Read call). If still not found, say `Not found in the sections checked: [list]`. Never invent section numbers, FAR ratios, height limits, setback distances, or use group assignments.

## Rules

- Quote NYC ZR values **verbatim**. Never paraphrase a FAR ratio, height limit, sky exposure plane angle, required yard depth, or use group number.
- Cite every quoted value with section + page: `§X-XX, p.N`. Multiple sources separated by semicolons. Page numbers refer to the cached PDF's page index.
- Cross-references inside the ZR (e.g., `as set forth in §23-32`) are normative — chase the chain by reading the referenced section before answering.
- Definitions live in **§12-10** (Article I, Chapter 2). When a quoted clause depends on a defined term whose meaning materially affects the answer, look up the definition there and quote it too.
- The Zoning Resolution is amended frequently. The cached PDF reflects the date in `outline.md`'s `Last cached` header — when answering questions about a recent amendment, mention the cache date and offer to re-cache.
- Tables (use group lists, bulk tables, parking schedules) often span multiple pages. Read the full range when quoting tabular data, and quote cell values verbatim.
- Output language: English with NA conventions (FAR as a unitless ratio, heights in feet, distances in feet/inches).

## Anti-patterns

- Answering NYC zoning questions from memory without reading the cached PDF. Always quote-and-cite.
- Reading the entire 1700-page PDF into context. Use the outline to target the 5–15 pages most likely to contain the answer.
- Citing only the section without the page number (`§23-145` alone). Always append `, p.N`.
- Inventing section numbers when the targeted pages did not contain the §X-XX needed. Expand the read once, then report not found.
- Falling back to `zoning-summary` for NYC questions — that skill produces a generic NA worksheet, not citation-grade NYC ZR answers.
- Confusing the Zoning Resolution with the NYC Building Code (Title 28), Multiple Dwelling Law, NYC Administrative Code, or Housing Maintenance Code — different documents, different citations.
- Re-downloading the PDF on every query. Cache is reused; refresh only on explicit user request or when `outline.md` is older than 90 days.
- Recommending the user check the document elsewhere when the cached PDF already answers the question.

## Resources

- `references/citation_format.md` — exact citation conventions for NYC ZR (§X-XX, p.N), Special District naming, definition lookups, cross-reference handling
- `references/zr_structure.md` — Article-by-Article overview and topic-to-Article quick lookup (where to find FAR, yards, use groups, special districts, parking, definitions)
