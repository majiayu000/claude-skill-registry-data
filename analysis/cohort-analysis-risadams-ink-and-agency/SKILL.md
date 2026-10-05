---
name: cohort-analysis
category: research-analysis
description: >
  Use when the user wants to analyze retention, cohort behavior, engagement trends, or
  understand how different user groups perform over time. Triggers on: 'cohort analysis',
  'retention analysis', 'user retention', 'cohort retention', 'week 1 retention', 'retention
  curve'.
codex-short-description: "Analyze retention, cohort behavior, and engagement trends over time"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
related-skills:
  - idea-generate
  - clarity-council
loop-eligible: false
compatibility: claude-code codex opencode
---

# Cohort Analysis

You track how groups of users behave over time. The technique's whole value is separating real
change from composition change.

## Define the cohort and the event precisely

Cohort by acquisition date, first-purchase date, or plan — each answers a different question.
"Retained" must be a specific event in a specific window. Analyses that skip this produce
numbers nobody can reconcile against anything else.

## Equal observation windows or the trend is an artifact

A cohort from last month has not had time to reach month three. Comparing incomplete cohorts to
complete ones produces a decline that does not exist — the most common cohort-analysis error.
Truncate to the window every cohort has actually had.

## Look for the composition explanation first

A retention change usually reflects a change in who was acquired, not a change in the product. A
marketing push into a cheaper channel drags the cohort down while nothing about the product
moved. Segment by channel, plan, or geography before concluding anything about product changes.

## Separate the curve's shape from its level

Early drop-off, the plateau it settles to, and whether it plateaus at all are different findings
with different responses. A cohort that never flattens has no retained base regardless of its
month-one number.

## Absolute counts alongside rates

A retention rate improving while the cohort shrinks may be selection, not improvement. Show the
denominator.

## Reporting

State the cohort and event definitions, the observation window, the curve with counts, the
segment breakdown, and whether an observed change is composition or behavior.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/cohort-analysis.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
