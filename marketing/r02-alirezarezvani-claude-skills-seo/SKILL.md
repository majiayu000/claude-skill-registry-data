---
name: "r00-alirezarezvani-claude-skills--seo"
description: >
  📈 SEO & Content Marketing skill suite derived from alirezarezvani/claude-skills.
  Keyword research, content audits, SERP analysis, technical SEO and content strategy.
  Provides 10 specialised commands for seo, content, marketing workflows.
version: "1.0.0"
domain: seo
tags: ["seo", "content", "marketing", "serp", "keywords"]
source: "https://github.com/alirezarezvani/claude-skills"
license: MIT
---

# 📈 SEO & Content Marketing Skill Suite

> Derived from **alirezarezvani/claude-skills** · Focus: _235 skills across engineering, marketing, C-level, finance_

## Overview

This skill provides 10 production-ready commands tailored for
**SEO & Content Marketing** workflows. All commands follow a consistent
interaction pattern with structured output, progress tracking and
actionable recommendations.

## Available Commands

- `/keyword-research` — Deep keyword clustering and opportunity scoring with SERP intent mapping
- `/content-audit` — Full-site content quality score, duplication check and cannibalization report
- `/technical-seo` — Crawl budget, Core Web Vitals, schema markup and indexability audit
- `/competitor-gap` — Backlink gap, topic gap and featured-snippet opportunity analysis
- `/content-brief` — AI-generated SEO content brief with outline, NLP terms and word count targets
- `/serp-monitor` — Daily rank tracking report with volatility alerts and CTR optimisation tips
- `/link-prospecting` — Quality backlink prospect list with DA/DR filters and outreach templates
- `/page-speed-seo` — Render-blocking, LCP, CLS, FID diagnosis mapped to ranking impact
- `/local-seo` — NAP consistency, Google Business Profile optimisation and local citation audit
- `/content-calendar` — Data-driven editorial calendar built from search demand and seasonality

## Interaction Pattern

Every command follows this structured response format:

```
1. CONTEXT CHECK   — Verify inputs and confirm scope with user
2. ANALYSIS        — Deep analysis with live progress display
3. FINDINGS TABLE  — Structured results with severity / priority
4. RECOMMENDATIONS — Prioritised action list (quick wins first)
5. NEXT STEPS      — Suggested follow-up commands
```

## UI Conventions

| Symbol | Meaning              |
|--------|----------------------|
| ✓      | Passed / complete    |
| ✗      | Failed / critical    |
| ⚠      | Warning / review     |
| ⟳      | In progress          |
| ░      | Pending              |
| 🔴     | Critical severity    |
| 🟠     | High severity        |
| 🟡     | Medium severity      |
| 🟢     | Low / informational  |

Progress bars use block characters:
`[████████░░] 80%`

## Quick Start

```bash
# Install this skill
cp -r . ~/.claude/skills/r00-alirezarezvani-claude-skills--seo/

# In Claude Code
/read ~/.claude/skills/r00-alirezarezvani-claude-skills--seo/SKILL.md
```

Then simply describe your task and Claude will route to the
appropriate command automatically.
