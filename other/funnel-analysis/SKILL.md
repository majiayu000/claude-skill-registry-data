---
name: funnel-analysis
description: Plan or interpret funnel analyses for activation, conversion, checkout, onboarding, sales, support, or product flows. Use when Codex is asked to define funnel steps, drop-off, conversion rates, segments, instrumentation, or funnel improvement memos.
license: MIT
---

# Funnel Analysis

## Core Workflow

1. Identify funnel goal, start/end events, ordered steps, user/account grain,
   time window, and segments.
2. Define conversion, drop-off, re-entry, timeout, deduplication, and exclusion
   rules.
3. Check instrumentation quality and whether each step is observable.
4. Compare segments and time periods without assuming causality.
5. Identify biggest drop-offs, confidence, and likely follow-up questions.
6. Recommend experiments, UX checks, or instrumentation fixes.

## Safety Rules

- Do not invent event names, volumes, conversion rates, or causal drivers.
- Do not recommend high-risk pricing, billing, or user-flow changes without
  human review.
- Flag funnels with missing or inconsistent tracking.

## Deliverable Shape

For funnel analyses, provide:

- Funnel goal and steps
- Metric definitions and rules
- Segment and time window
- Instrumentation quality notes
- Drop-off and conversion summary
- Caveats and confidence
- Recommended next actions

## References

- Read `references/funnel-analysis-checklist.md` when planning or reviewing a
  funnel analysis.
