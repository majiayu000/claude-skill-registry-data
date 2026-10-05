---
name: artifact
description: "Create and review artifact/report pages: research findings, project status, architecture, decisions, handoffs and reference pages. Select the structure from the reader question, write understandable copy, then inspect rendered figures and perform a fresh-reader review. Use for 写artifact、做报告、状态报告、架构报告; product UI and marketing sites use frontend-design."
when_to_use: "write an artifact page, report page, research finding page, status report page, RCA page, handoff page, paper-quality figure, chart colours for a report, architecture diagram for a report, 写artifact, 发一个artifact, 做一页报告, 研究报告页, 汇报页面, 论文图, 图表配色, 架构图页面 — NOT for a whole-system cross-repo landscape (use /landscape), the hub publishing mechanics alone (use /internal-deploy), product UI or a marketing site (use /frontend-design), or a blog chart (use /blog-chart)"
argument-hint: '[type: finding|status|architecture|rca|handoff|decision|reference|worklog] [source files or notes]'
user_invocable: true
---

# Artifact

One page that answers, from its first screen, what the problem is now, how
sure we are, and what the next step is — then carries the evidence. The
executable instructions live in `prompt.md`; this body is the Codex-facing
summary.

## What it does

1. Reads `references/review.md` to set acceptance answers, then routes the
   reader's question through `references/spines.md` to choose the type and
   container; resolves the organisation's design system.
2. Collects every number with its source, population, window and date, and
   grades each claim verified / inferred / speculation.
3. Uses the selected spine as question coverage, combining short answers and
   choosing only relevant parts from `references/anatomy.md`. Argued pages
   lead with the answer, evidence and uncertainty; reference/worklog pages
   retain their lookup/state structure. No invented metrics or empty sections.
4. Draws the figures needed to answer the question (`references/figures.md`)
   and, for architecture pages, C4 context and container diagrams with a
   legend (`references/diagrams.md`) — inline SVG, tokens for both themes,
   captions that state the takeaway.
5. Edits language for meaning, first-use definitions and consistency against
   the facts, using `references/review.md`.
6. Runs `python3 ~/.claude/scripts/artifact-lint.py <page>`; fixes every FAIL
   and fixes or explains WARNs. Reviews all figures and the first screen in
   light/dark at desktop/phone widths, then performs a fresh-reader review.
   Repairs and re-renders until the applicable checks pass; records evidence
   in `artifact-review.md`. Checks the served output after authorized publishing.
   An invisible figure or wrong takeaway blocks completion even with clean lint.

## Usage

```
/artifact finding notes/v9-xref.md          # a research result page
/artifact status                            # where the project stands, from the repo + hub
/artifact architecture apps/halo            # as-built system page with C4 L1 + L2
/artifact rca incident-2026-09-21.md        # post-mortem in the SRE field order
/artifact worklog                           # the living Goal · Now · Human TODO · Blockers page
```

Publishing goes through `/internal-deploy` (hub) or the Artifact tool
(Claude Artifacts); this skill owns what is on the page, not where it lands.
