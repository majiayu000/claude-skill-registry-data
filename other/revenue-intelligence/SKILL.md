---
name: revenue-intelligence
description: >-
  AI-powered revenue intelligence: sales call insight extraction, content-to-revenue
  attribution, and multi-source client reporting. Use when asked to analyze sales
  calls, build revenue attribution models, or generate client reports.
when_to_use: |
  Use when extracting structured insights from Gong sales call transcripts (objections, buying signals, competitive mentions), proving content ROI by mapping content pieces to pipeline and closed revenue, generating unified client reports from GA4 + HubSpot + Ahrefs + Gong, identifying content gaps in the buyer journey, or detecting anomalies across marketing metrics.

  Not when: drafting or optimizing cold outbound sequences — even if seeded from Gong call data — use outbound-engine. This skill produces follow-up *drafts* from a specific call's context; sequence building, delivery, and optimization are outbound-engine's. Not when: the content-gap analysis is SEO/keyword-driven (competitor coverage, search demand) — use seo-ops; this skill's gap analysis is buyer-journey/pipeline-driven.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Revenue Intelligence

AI-powered revenue intelligence: sales call insight extraction, content-to-revenue attribution, and multi-source client reporting.

## Core Tools

| Tool | Purpose |
|------|---------|
| `scripts/gong_insight_pipeline.py` | Extract objections, buying signals, and competitive mentions from call transcripts |
| `scripts/revenue_attribution.py` | Map content to closed revenue with first-touch, linear, and time-decay models |
| `scripts/client_report_generator.py` | Generate unified GA4 + HubSpot + Ahrefs + Gong client reports |

## References

- [references/tool-reference.md](references/tool-reference.md) — full CLI flags and output specifications for all three tools
- [references/configuration.md](references/configuration.md) — environment variables, data flow, recommended workflow, and dependencies
