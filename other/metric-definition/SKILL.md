---
name: metric-definition
description: Define business, product, financial, and operational metrics. Use when Codex is asked to create a metrics dictionary, clarify KPI definitions, specify formulas, owners, grains, filters, caveats, or source-of-truth rules.
license: MIT
---

# Metric Definition

## Core Workflow

1. Identify metric purpose, decision use, audience, owner, and source system.
2. Define formula, grain, time window, filters, inclusions, exclusions, and
   segmentation.
3. Specify source of truth, freshness, data quality checks, and known caveats.
4. Distinguish input metrics, output metrics, leading indicators, and lagging
   indicators.
5. Add examples and counterexamples so users avoid common misinterpretations.
6. Define review cadence and change-control expectations.

## Safety Rules

- Do not invent formulas, source systems, baselines, or business definitions.
- Do not publish financial, investor, compliance, or compensation metrics
  without reviewer confirmation.
- Flag metrics that can be gamed or misread without segmentation.

## Deliverable Shape

For metric definitions, provide:

- Metric name and purpose
- Formula and grain
- Source of truth
- Filters and exclusions
- Segments and time windows
- Caveats and quality checks
- Owner and review cadence
- Example interpretation

## References

- Read `references/metric-definition-checklist.md` when creating or reviewing a
  metrics dictionary.
