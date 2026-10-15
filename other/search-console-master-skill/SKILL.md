---
name: search-console-master-skill
description: "Use when analyzing Google Search Console data: organic search analysis, GSC data interpretation, opportunity scoring."
metadata:
  source: "prompts/skills/search_console/master-skill"
---

> **Outside the GoMarble app.** This methodology is GoMarble's own, kept in sync with the GoMarble connector.
> - GoMarble connector tools for this skill: `gsc_list_properties`, `gsc_get_performance_overview`, `gsc_get_search_analytics`, `gsc_get_advanced_search_analytics`, `gsc_get_search_by_page_query`, `gsc_compare_search_periods`, `gsc_check_indexing_issues`, `gsc_inspect_url`, `gsc_inspect_url_enhanced`, `gsc_batch_url_inspection`, `gsc_get_site_details`, `gsc_get_sitemaps`, `gsc_list_sitemaps_enhanced`, `gsc_get_sitemap_details`.

# Organic Search (Google Search Console) – Master Skill

## Skill Objective

Turn raw Search Console data into:
- Revenue opportunities
- Ranking leverage
- Paid + Organic crossover insights
- Actionable prioritization, not SEO busywork

## HARD SOURCE-OF-TRUTH RULE

All organic query, impression, CTR, and position data **MUST** come from **Google Search Console**.
- No synthetic keywords.
- No model-estimated demand.
- No substitutions.

## Available Skills

| # | Skill | Path | Purpose |
|---|--------|------|---------|
| 1 | GSC Analysis Protocol | `references/gsc-analysis-protocol.md` | Extraction, normalization, intent/value, opportunity scoring, page-level intelligence |

## Rules

- **Order:** Run the GSC Analysis Protocol first. All recommendations must use **Google Search Console data only**.
- **Guardrails:** Follow `references/guardrails.md` before any organic/SEO recommendation.
- **No data = no guess:** If GSC access or data is missing, do not infer keywords or estimate traffic—ask for access or stop.

## When This Skill Is Triggered

Route here when user intent includes:
- "organic growth"
- "SEO opportunities"
- "Search Console analysis"
- "why organic traffic dropped"
- "what content should we create"
- "organic vs paid overlap"
- "where should we focus SEO effort"
