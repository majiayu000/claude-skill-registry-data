---
name: seo-ops
description: >-
  AI-powered SEO operations: keyword intelligence, competitor gap analysis,
  Google Search Console optimization, and trend detection. Use when asked to
  research keywords, analyze competitor content gaps, audit GSC performance, or
  detect trending topics. For growth experiments see growth-engine; for content
  optimization see autoresearch.
when_to_use: |
  Use when performing keyword research or generating a content brief, finding
  quick-win striking-distance keywords from Google Search Console, running a
  competitor content gap analysis, detecting trending topics for content
  creation, identifying decaying pages with traffic drops, or building a
  prioritized keyword target list scored by Impact × Confidence.

  Not when: running growth experiments or A/B tests — use growth-engine instead.
  Not when the content-gap analysis is REVENUE/pipeline-driven (which content
  drives deals or revenue, buyer-journey gaps) rather than SEO/search-driven —
  use revenue-intelligence; this skill's gap analysis is keyword/search-demand-driven.
  For deep content research and optimization use [autoresearch](../autoresearch/SKILL.md).
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# AI SEO Ops

AI-powered SEO operations: keyword intelligence, competitor gap analysis, GSC optimization, and trend detection.

## Core Tools

| Tool | Purpose |
|------|---------|
| `scripts/content_attack_brief.py` | Full keyword intelligence pipeline: BOFU keywords, competitor gaps, decaying pages |
| `scripts/gsc_client.py` | Google Search Console API client (CLI + library) |
| `scripts/gsc_auth.py` | One-time OAuth setup for GSC access |
| `scripts/trend_scout.py` | Multi-source trend detection across Google Trends, HN, Reddit, X |

## Core Rules

1. Run `scripts/gsc_auth.py` once before any GSC tool — it saves the OAuth token locally.
2. Keywords are prioritized by Impact × Confidence (max 100) — focus on high-score BOFU targets first.
3. Check the playbook in [growth-engine](../growth-engine/SKILL.md) before creating new content to apply proven patterns.
4. Weekly cadence: full brief + daily striking-distance check + 2×/week trend scout.

## References

- [references/tool-reference.md](references/tool-reference.md) — full CLI and library usage for all four tools
- [references/configuration-and-scoring.md](references/configuration-and-scoring.md) — environment variables, scoring model, funnel classification, workflow, dependencies
