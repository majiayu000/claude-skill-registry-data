---
name: wiki-ingest
description: Ingest a new source (confirmed finding, FP lesson, technique) into wiki pages with cross-links. Idempotent. Use when a finding is reported, after a teach-me FP, or when user says "ingest this". Run after report-finding.
---

# wiki-ingest

## Purpose
Apply Karpathy's llmwiki pattern: when a new fact lands, the LLM
updates *all* the places that should know about it, in one pass. The
wiki compounds over time so future engagements start informed.

## Inputs
- A source. One of:
  - `targets/<name>/findings/<id>/<id>.md` (confirmed TP)
  - `targets/<name>/opus/<chain_id>.md` (FP with teaching value)
  - A user-supplied note (raw markdown)

## Steps
1. Classify source:
   - sink_kind (DOM XSS, prototype pollution, IDOR, ...)
   - target_program (which bounty program)
   - tools_involved (Caido, mock_backend, framework...)
2. Decide pages to touch:
   - `wiki/techniques/<sink_kind>/<pattern_slug>.md` — create or
     append a "Seen-in-the-wild" entry with date and target.
   - `wiki/targets/<program>.md` — append to "Prior findings" list
     with cross-link.
   - `wiki/findings/<id>.md` — new page summarizing the finding
     with backlinks to engagement + technique + tools.
   - `wiki/tools/<tool>/notes.md` — append if a tool quirk was
     discovered.
3. Cross-link discipline:
   - Every new page MUST link to ≥1 existing page (technique or
     target) and SHOULD be linked-from ≥1 existing page within 24
     hours (handled by the next `wiki-lint`).
4. After writing, re-embed touched pages into the wiki RAG collection
   (`wiki` collection name) so `docs_query` retrieves the new state.

## Outputs
- Updated/created wiki pages.
- Updated `wiki` RAG collection.

## Failure modes
- Source classification ambiguous → ask user one tight question
  ("which technique slug fits this best: <list of 3>?").
- A page that should be touched doesn't exist → create it; use
  `wiki/SCHEMA.md` for naming + frontmatter.
- Cross-link orphan (new page, no inbound link yet) → ok this pass;
  `wiki-lint` will surface it next run.

## Result block
appended to a wiki-side log at `wiki/_ingest_log.jsonl`:
```json
{ "ts": "...", "source": "...", "pages_touched": [...],
  "pages_created": [...], "cross_links_added": N }
```
