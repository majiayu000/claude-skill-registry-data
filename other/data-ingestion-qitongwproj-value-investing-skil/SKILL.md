---
name: data-ingestion
description: Use this skill to fetch, normalize, validate, and confidence-score public or user-provided investment data. Trigger before valuation when the analysis needs SEC filings, market quotes, IR releases, financial metrics, or structured data packets.
---

# Data Ingestion Skill

## Purpose

Fetch, normalize, validate, and score data confidence.

## Inputs

- Target
- Market
- Industry
- Available data
- User requested depth
- Prior assumptions, if any

## Outputs

- Structured analysis
- Assumptions
- Missing data
- Confidence level
- Next required action

## Rules

- State assumptions explicitly.
- Flag missing or low-confidence data.
- Prefer conservative assumptions.
- Keep output auditable.
