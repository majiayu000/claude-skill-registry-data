---
name: drawing-reader
description: "Reads an architectural drawing PDF and answers questions about it: a single sheet, a full set, a redline, a record drawing, a shop drawing, or a detail. Summarises, finds a sheet, explains a detail, lists disciplines, or pulls a callout. Trigger on \"read this drawing\", \"what is in this set\", \"summarize this drawing\", \"show me sheet X\", \"what is on this sheet\", or a pasted path to a drawing PDF. For specifications, codes, contracts, and reports use doc-reader instead. Detects the drawing type, asks what is wanted before reading at length, and hands off to schedule-extractor, drawing-set-bookmarker, or drawing-checklist when one of those fits better. Never reports a dimension or a note it did not read off the sheet."
license: MIT
metadata:
  title: "Drawing Reader"
  summary: "Read and interpret an architectural drawing PDF"
  discipline: "construction-admin"
  tags: "Design"
---


# Drawing Reader


## Overview


Read and interpret an architectural drawing PDF. The user drops in any drawing artifact — a single sheet, a multi-discipline set, a markup PDF, a record drawing, a shop drawing, or a single detail — and asks Claude to interpret it in whatever direction they need: summarize, locate a sheet, explain a detail, find a callout, extract a schedule, count something, list disciplines, etc.


This skill is a **router** — it identifies what kind of drawing artifact was provided and what the user wants, then either reads it directly or delegates to a more specialized skill (`schedule-extractor` for schedule pulls, `drawing-set-bookmarker` for set tabulation, `drawing-checklist` for QA). Output lives in `docs/drawing-reads/` so each read is captured for the project record.


## Scope and limits — read first


This skill covers:

- **Drawing PDFs** — single sheet, multi-sheet set, markup/redline, record drawing, shop drawing, detail.
- **NCS-compliant titleblocks** (US National CAD Standard v6) — discipline letter, sheet-type digit, sheet number conventions.
- **Routing to specialized skills** when the user's intent matches a more focused tool — `schedule-extractor`, `drawing-set-bookmarker`, `drawing-checklist`, `code-analysis-builder`, `area-takeoff` (when shipped), etc.
- **Direct vision read** for queries that don't fit a specialized pattern (e.g. "what's on this detail", "summarize this sheet", "what's in this set").

This skill does **NOT** cover:

- **Specifications, code excerpts, contracts, reports, AHJ correspondence** — these are non-drawing AEC PDFs. Drawing reader is drawing-only. (A future broader `doc-reader` may cover those.)
- **DWG / RVT / IFC native files** — drawings only via PDF. For native CAD/BIM, use a different toolchain.
- **Producing new drawings** — the skill reads existing drawings, does not generate them.
- **AHJ compliance verification** — that's `code-analysis-builder` / `ada-tracker` / `climate-zone-mapper` etc.
- **Strategic interpretation** ("is this a good design?") — vision can describe, not judge.
- **Exact-dimension takeoffs** — vision is approximate; do not trust per-cell dimensions reconstructed from rendered PDF cells. Read the original PDF page for any dimension that matters.

## When to use


Trigger on:

- "Read this drawing PDF: <path>."
- "What's in this set?"
- "Summarize sheet A-301."
- "What discipline is this?"
- "Tell me what's on this redline."
- Pasted path to a drawing PDF without a specific extractor request.

Do NOT trigger on:

- "Extract the door schedule" — use `schedule-extractor`.
- "Bookmark this set" — use `drawing-set-bookmarker`.
- "QA this DD set" — use `drawing-checklist`.
- "Read this spec / code / contract PDF" — out of scope; not a drawing.
- "Compare addendum 1 to addendum 2" — use `issue-set-comparison` (when shipped).

## Workflow


### Step 1 — Bootstrap if needed


Check whether `docs/drawing-reads/index.md` exists. If not, create:


```bash
mkdir -p docs/drawing-reads/.cache
```


And write a minimal index header (no script needed):


```markdown
# Drawing Reads — Project Log

| Date | Source PDF | Drawing Type | User Intent | Output |
|------|------------|--------------|-------------|--------|
```


If `docs/` does not exist, confirm with the user before creating.


### Step 2 — Inventory the PDF


Use the `Read` tool to look at the first 2 pages of the drawing PDF. Note:

- Total page count (from PDF metadata if available, otherwise approximate).
- Page size + orientation (helps identify sheet vs detail).
- Whether the first page looks like a cover sheet, a single drawing, or a redline markup.

If the PDF is large (> 50 pages), tell the user up front and confirm before reading more — vision reads are token-heavy.


### Step 3 — Detect drawing type


Use `references/drawing-types.md` to classify the PDF as one of:

- **Single sheet** — one drawing on one page.
- **Multi-sheet set** — 10+ pages, NCS-style titleblocks, varied disciplines.
- **Redline markup** — drawing pages with cloud/cloudless markup overlays + comment bubbles.
- **Record drawing / as-built** — drawing pages with "RECORD" or "AS-BUILT" stamp + revision clouds.
- **Shop drawing** — fabricator-stamped, often 11×17 or larger, frequently with "SHOP DRAWING" titleblock.
- **Detail page** — single detail (e.g. wall section), often pulled from a larger set.

State the detected type explicitly to the user. Ask them to confirm or correct before proceeding.


### Step 4 — Confirm user intent


Ask the user what they want from the drawing. Use `references/read-patterns.md` to map common intents to handling:

- "Summarize" → high-level prose summary, sheet count, disciplines, key features.
- "Find sheet X" → locate by NCS sheet number, render that page, summarize content.
- "Extract <schedule>" → delegate to `schedule-extractor`.
- "Tabulate the whole set" → delegate to `drawing-set-bookmarker`.
- "QA check" → delegate to `drawing-checklist`.
- "Explain this detail" → vision-read the detail, identify components, callouts, materials.
- "What's the egress" / "where's the wall section" / "show me the elevations" → topical search across the set.
- "Compare to previous version" → out of scope here; redirect to `issue-set-comparison` when shipped.

If the user's intent doesn't fit a specialized skill, handle directly via vision read.


### Step 5 — Read or delegate


If delegating: inform the user that the request is better handled by `<other-skill>` and stop there (or suggest installing it via `npx archtmpl@latest --skill <other-skill>`).


If reading directly: open the relevant pages, vision-read for the user's intent, and produce the output. For multi-sheet queries, batch reads (e.g. read 5 pages at a time) to keep within token budget.


### Step 6 — Write the output


Write `docs/drawing-reads/<read-slug>.md` with:

- Header: source PDF path, drawing type, user intent, date.
- Body: the read result (summary, sheet content, extraction, etc.).
- Citations: page number(s) + sheet number(s) of every claim.
- Confidence flag (`high` for verbatim text/labels, `medium` for inferred content, `low` for vision approximation).

Slug rule: `YYYY-MM-DD_<short-intent-tag>` (e.g. `2026-05-08_egress-summary`).


### Step 7 — Update the project log


Append one row to `docs/drawing-reads/index.md` with the read metadata (use shell `printf` or manual `Edit` since no script ships with this skill — keep it lean):


```bash
echo "| 2026-05-08 | <pdf-path> | <type> | <intent> | <output-md> |" >> docs/drawing-reads/index.md
```


### Step 8 — Report


Tell the user:

- Path to the read output `.md`.
- Confidence summary (how many claims are `high` vs `medium` vs `low`).
- Caveats — any pages too dense to read fully, any callouts that couldn't be resolved.
- If a more specialized skill applies for follow-up (e.g. "for a full schedule extract, use `schedule-extractor`"), say so.

## Rules

- Every claim about content on a sheet must cite the sheet number AND page number. No bare claims.
- Confidence flag (`high` / `medium` / `low`) is required on every extracted value or claim.
- For dimension-sensitive readings, the skill explicitly tells the user to verify against the original PDF — vision is approximate.
- Drawing type classification must come from `references/drawing-types.md` recognition signals — not invented.
- When delegating, name the specific skill (`schedule-extractor`, etc.) and stop — do not partially do that skill's work inline.
- Output files live in `docs/drawing-reads/` of the user's project.

## Anti-patterns

- Reading 200 pages of a set without confirming with the user first. Token-heavy reads must be authorized.
- Trusting per-cell dimensions reconstructed from PDF vision. Always tell the user to verify dimensions in the source PDF.
- Treating spec books / code excerpts / contracts as drawings. They are not — out of scope.
- Doing a partial schedule extract inline. Delegate to `schedule-extractor`.
- Doing partial QA inline. Delegate to `drawing-checklist`.
- Inventing sheet numbers from titleblock vision when the titleblock is illegible. Mark as "UNKNOWN" and flag.
- Strategic / qualitative judgments ("this is a good plan"). Describe only.

## Resources

- `references/_provenance.md` — sources for drawing-type recognition + NCS conventions
- `references/drawing-types.md` — drawing-type recognition signals (single / set / redline / record / shop / detail) + typical user requests per type
- `references/read-patterns.md` — user-intent → handling pattern mapping (delegation rules + direct-read recipes)
