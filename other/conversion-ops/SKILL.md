---
name: conversion-ops
description: >-
  AI-powered conversion rate optimization: landing page audits, CRO scoring,
  survey segmentation, and lead magnet generation. Use when asked to audit a
  landing page, run a CRO analysis, segment survey responses, or generate lead
  magnets. For content quality scoring see content-ops.
when_to_use: |
  Use when auditing a landing page for CRO (scoring headline clarity, CTA visibility, social proof, trust signals, form friction, mobile responsiveness), segmenting survey responses by pain point, generating lead magnet briefs from survey data, or doing batch CRO analysis across multiple URLs.

  Not when: the goal is quality-scoring content copy or strategy docs against an expert panel — use `content-ops`. Not when the task is generating and multi-round-optimizing copy VARIANTS pre-launch (50+ variants scored by a simulated panel, winners evolved over rounds) rather than auditing a live URL — use `autoresearch`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# AI Conversion Ops

AI-powered conversion rate optimization: landing page audits, CRO scoring, survey segmentation, and lead magnet generation.

## Tools

### CRO Audit (`scripts/cro_audit.py`)

Fetches a landing page and scores it across 8 conversion dimensions (0–100 each): Headline Clarity, CTA Visibility, Social Proof, Urgency, Trust Signals, Form Friction, Mobile Responsiveness, Page Speed Indicators.

Output: per-dimension scores, priority fixes ranked by impact, before/after suggestions, industry benchmark comparison, overall letter grade (A+–F).

See [references/cro-audit.md](references/cro-audit.md) for full CLI usage and supported industries.

### Survey-to-Lead-Magnet Engine (`scripts/survey_lead_magnet.py`)

Ingests survey CSV data, clusters respondents by pain point, and generates lead magnet briefs for each segment.

Output: pain point clusters with respondent counts, segments ranked by size and commercial potential, per-segment lead magnet brief (title, format, hook, content outline, CTA, viral/conversion scores), prioritized implementation roadmap.

See [references/survey-lead-magnet.md](references/survey-lead-magnet.md) for full CLI usage and CSV format details.

## Configuration and Workflow

No API keys required. Both tools work with local analysis only.

See [references/recommended-workflow.md](references/recommended-workflow.md) for environment variables, dependencies, and recommended weekly/monthly cadence.

## Related skills

- [content-ops](../content-ops/SKILL.md) — quality scoring gate for the content before conversion work begins
- [autoresearch](../autoresearch/SKILL.md) — generates and multi-round-optimizes the conversion-copy variants this skill then audits and scores
