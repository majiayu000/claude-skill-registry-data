---
name: research-evidence
description: Use when research writing, reviews, rebuttals, or related-work planning needs academic evidence. Searches literature, screens candidate papers, audits novelty and missing work, verifies DOI/BibTeX/reference metadata and citation authenticity, and checks whether sources support the stated claims.
license: MIT
---

# Research Evidence

## Overview

Use this skill as the shared evidence layer for paper writing, related work, review, and rebuttal work. It does not replace domain judgment: it finds and checks evidence, then reports support level, gaps, and risks.

## Hard Boundaries

- Use public metadata, open-access PDFs, and user-provided local PDFs only.
- Do not use Sci-Hub or any route that bypasses access control.
- Do not write Markdown, JSON, CSV, or report files unless the user explicitly asks for saved artifacts.
- Run RefChecker in non-LLM mode by default. Enable LLM-assisted extraction or hallucination checks only when the user explicitly requests it and accepts the privacy/cost tradeoff.
- Treat tool output as evidence to inspect, not final truth. Mark weak coverage, metadata mismatches, and unsupported claims clearly.

## Venue Defaults

Prefer these venues when the user does not specify otherwise:

- Computer Vision: CVPR, ICCV, ECCV.
- ML/AI: ICLR, NeurIPS/NIPS, ICML.
- Autonomous driving, robotics, and collaborative perception secondary venues: CoRL, ICRA, IROS, AAAI, IJCAI, T-ITS, RA-L.

Do not let secondary venues outrank the primary top-conference set unless the user's task or subfield demands it.

## Workflows

### Literature Search

1. Translate the research question into compact queries with venue/year terms when useful.
2. Use the dedicated tool environment from `references/tooling.md`; start with arXiv metadata search for CV/ML topics.
3. Return a compact candidate list with title, source, year/date, identifier, URL, and why each candidate is relevant.
4. Label coverage risk when search sources are unavailable, too broad, too recent, or missing known top-venue work.

### Recent Literature / Novelty Risk Audit

Use this workflow when the user asks about novelty, recent work, missing related
work, reviewer risk, rebuttal readiness, score prediction, first/SOTA/new
benchmark claims, or whether a close paper conflicts with the current claim.

1. Decompose the claim into axes before searching: domain/input, method family,
   task/output, evaluation protocol, dataset/benchmark, and reliability or
   failure mode.
2. Expand the search across direct terms, synonyms, neighboring tasks, older
   terminology, and broad recent-work queries. Do not stop at the user's exact
   phrasing.
3. For high-stakes checks, cross-check at least two evidence routes: direct
   arXiv API or official venue metadata; local `reference/`, PDF, BibTeX, or
   LaTeX sources; and the local `paper-search` wrapper as a smoke or secondary
   check.
4. Classify candidates after inspecting metadata and abstracts: direct
   competitor, claim limiter, table candidate, prose citation, background, or
   irrelevant.
5. Report the search matrix, source-coverage limits, and claim-impact verdict.
   Never answer "not found" without stating which query families and sources
   were checked.

Read `references/recent-literature-audit.md` for the full checklist. Use
`scripts/arxiv_query_matrix.py` when a repeatable arXiv query matrix would make
the search less ad hoc.

### Citation Check

1. Prefer local PDF, LaTeX, BibTeX, or reference-list files supplied by the user.
2. Run RefChecker without LLM flags unless explicitly requested.
3. Summarize reference authenticity, metadata mismatches, missing fields, suspicious entries, and false-positive risk.
4. Do not automatically rewrite references. Recommend exact follow-up checks or edits.

### Claim Evidence Check

1. Extract the claim and required support type: paper text, citation, experiment result, table/figure, code/log artifact, or user-confirmed fact.
2. Search or verify only the minimum evidence needed for the claim.
3. Report one of: `verified`, `likely`, `unsupported`, or `needs user input`.
4. Do not strengthen claims based on weak evidence. Recommend weakening, adding a citation, deleting the claim, or asking the user for missing evidence.

## Output Shape

Default response shape:

- `query`: search or verification intent.
- `sources`: tools/sources used and key records found.
- `verdict`: `verified`, `likely`, `unsupported`, or `needs user input`.
- `risks`: source coverage, metadata mismatch, citation error, weak venue fit, or stale evidence.
- `next action`: write, weaken, cite, delete, continue search, or ask the user.

For novelty-risk audits, include:

- `search matrix`: query families and evidence routes checked.
- `candidate classification`: direct competitor, claim limiter, table candidate,
  prose citation, background, or irrelevant.
- `claim impact`: keep, weaken, add citation/table row, revise positioning, or
  avoid first/SOTA language.
- `residual risk`: what the search still may have missed.

## Tooling

Read `references/tooling.md` before running installed commands or changing tool behavior.
