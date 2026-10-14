---
name: civiltekk-startup-docs-skill
description: >-
  Founder business documents and startup presentations — reports, quotations,
  spreadsheets, presentations with professional formatting, plus pitch deck
  structures, board updates, launch decks, palettes, investor-readiness
  checklists. Triggers: create a report, generate quotation, make a
  spreadsheet, prepare a proposal, build a financial model, create a tracking
  sheet, draft an investor update, pitch deck, investor deck, board deck,
  board update, demo day, product launch slides, Series A deck, pre-seed
  deck, investor-readiness.
license: Apache-2.0
compatibility: opencode
category: Startup/Business
---

Consolidates startup-business-docs-skill + startup-pitch-deck-skill (#603).

## What I do

Produce founder-grade business documents and investor-grade startup decks:

1. **Detect the route** (§Routes) — explicit > inferred > ask-once.
   Explicit: the request names the artifact ("create a report", "generate
   quotation", "make a spreadsheet", "prepare a proposal", "build a
   financial model", "write a client email" → `business-docs`; "pitch
   deck", "investor deck", "board update", "demo day", "product launch
   slides", "investor-readiness" → `pitch-decks`). Inferred: the artifact
   shape (a written or numeric business document → `business-docs`; slides
   aimed at investors, the board, or a launch audience → `pitch-decks`).
   Ambiguous ("startup materials", "deck plus the numbers behind it") →
   ask once — one ask per run, then proceed on the answer.
2. **Load the route's values file** (`references/business-docs.md` /
   `references/pitch-deck.md`) and apply its contract.
3. The routes chain naturally — a board deck starts from the report
   metrics of `business-docs` and ends in the board structure of
   `pitch-decks`; a full fundraising pass uses both files, the route only
   decides which leads.

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/business-docs.md` | route `business-docs` | Five document workflows (report, quotation, spreadsheet, presentation delegation, communications) with structure templates, formula and output-format references, best practices, error handling, skill integrations |
| `references/pitch-deck.md` | route `pitch-decks` | Deck-type matrix, 10-12 slide pitch sequence, board-update and launch-deck outlines, demo-day structure, design principles (visual philosophy, typography, palettes, layouts), investor-readiness checklist, stage-specific guidance, common mistakes |

Side files carry VALUES only; this file carries the METHOD. A document
or presentation concern outside founder business documents and startup
decks (technical documentation, changelogs, generic corporate slides,
construction proposals) is not this skill's space —
`technical-writing-skill` owns prose standards, `construction-bd-skill`
owns construction BD, `pptx-specialist-subagent` owns generic deck
production.

## Routes

| Situation | Route |
|-----------|-------|
| "create a report", "generate quotation", "update slides", "make a spreadsheet", "prepare a proposal", "build a financial model", "create a tracking sheet", "draft an investor update", "write a client email"; any written or numeric business document for investors, board, team, or clients | `business-docs` |
| "pitch deck", "investor deck", "fundraising presentation", "startup slides", "board deck", "board update", "product launch slides", "demo day presentation", "Series A/B/C deck", "pre-seed deck", palette selection, investor-readiness check; any slide artifact aimed at investors, board, or launch | `pitch-decks` |
| Ambiguous ("fix the docs", "startup materials") | ask once (§What I do step 1), then route |

## Boundaries

- The two routes were formerly peer skills (the business-docs workflow
  delegated pitch/board decks onward; the pitch-deck knowledge consumed
  report metrics) — that boundary is internal now; the route table above
  is the boundary logic.
- Actual PPTX production is delegated, not performed here —
  `startup-ceo-subagent` for startup decks, `pptx-specialist-subagent`
  for sales decks and internal slides; this skill supplies structure,
  content, and design direction (values-file doctrine).
- File engines stay outside: reports and quotations export through
  `docx-creation`/`pdf-specialist`, spreadsheets through
  `xlsx-specialist`; this skill owns the workflow and templates, not the
  engines.

## Agent behavior rules

- One ask per run maximum (route detection); headless/CI: no asks —
  infer from the request, defaulting to `business-docs` (documents
  first; decks apply once the content exists).
- Clarify scope before generating (audience, format, deadline) and
  verify every number before finalizing — a wrong figure in an investor
  artifact is worse than a late draft.
- Offer fast revision cycles; don't over-engineer initial versions
  (values-file contract).

> **Harness binding — interactive asks** (AGENTS.md §Portability contract):
> OpenCode — `question` tool. Claude Code — `AskUserQuestion`. Other/none —
> ask in a plain reply; headless/no-answer rule above applies.
