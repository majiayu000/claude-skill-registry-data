---
skill_id: search-visibility
name: Search Visibility
description: "SEO, AEO and GEO — search, keywords, ranking, visibility, answer engine optimization, generative engine optimization, voice search, organic traffic, featured snippets, technical search audit, E-E-A-T, structured data."
version: 1.0.0
category: search-visibility
office: CMO
lead_agent: seo-specialist
triggers:
  - SEO
  - search
  - keywords
  - ranking
  - visibility
  - AEO
  - voice search
  - Google
  - organic traffic
  - featured snippets
  - generative search
  - Core Web Vitals
  - backlinks
collaborates_with:
  - aeo-strategist
  - authority-builder
  - geo-optimizer
  - keyword-intent-researcher
  - seo-specialist
  - technical-seo-auditor
  - content-strategist
  - behavioral-designer
  - compliance
---

# Search Visibility -- Domain Dispatcher

> Office: CMO | Lead: seo-specialist
> Sub-skills: 6 | Frameworks: E-E-A-T, Search Intent Mapping, Topic Authority Model

## Purpose

SEO, AEO (Answer Engine Optimization), GEO (Generative Engine Optimization), technical search auditing, keyword intelligence, and authority building. The full search visibility lifecycle -- from technical health to AI-era generative search optimization. The seo-specialist is the unified agent that absorbs all 5 sub-specialists via Op-D mode routing.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| Answer engine, featured snippets, voice search, Schema.org | aeo-strategist | search-visibility/aeo-strategist/SKILL.md |
| Backlink strategy, digital PR, domain authority, brand mentions | authority-builder | search-visibility/authority-builder/SKILL.md |
| ChatGPT Search, SGE, Perplexity, generative AI search | geo-optimizer | search-visibility/geo-optimizer/SKILL.md |
| Keyword research, search intent mapping, content gap analysis | keyword-intent-researcher | search-visibility/keyword-intent-researcher/SKILL.md |
| Full search visibility strategy, multi-mode orchestration | seo-specialist | search-visibility/seo-specialist/SKILL.md |
| Crawlability audits, indexing, Core Web Vitals, site health | technical-seo-auditor | search-visibility/technical-seo-auditor/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-seo`
- Task contains keywords: SEO, search, keywords, ranking, visibility, AEO, voice search, Google, organic traffic, featured snippets, generative search, Core Web Vitals, backlinks, domain authority, E-E-A-T, schema markup, structured data, rich snippets

## Behavioral Layer

- Confidence: 🟢 HIGH
- Compliance: reads project-manifest.json
- Handoff: writes .mxm-skills/agents-handoff.md
- Frameworks: E-E-A-T, Search Intent Mapping, Topic Authority Model

## External Sources

- Primary: community-packs/claude-skills-library/marketing-skill/
- Merge rule: Maxim ALWAYS WINS -- behavioral science + proactive triggers + confidence tagging non-negotiable

---
*Maxim Search Visibility Skill -- Version 1.0.0*
*Maxim behavioral layer: ACTIVE | External merge: marketing-skill ABSORBED | Confidence: 🟢 HIGH*

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
