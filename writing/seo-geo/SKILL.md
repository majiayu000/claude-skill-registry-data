---
name: seo-geo-for-saas
description: >
  Complete SEO + GEO (Generative Engine Optimization) system for SaaS companies wanting to rank on both Google and AI search engines (ChatGPT, Perplexity, Gemini, Claude).
  Use this skill whenever the user asks about SEO strategy, keyword research, content planning, writing SEO-optimized articles, auditing their search performance, creating a content calendar, analyzing competitors, or optimizing for AI search visibility.
  Trigger on: "seo", "keyword research", "content calendar", "rank on google", "search traffic", "write an article", "blog post", "serp", "backlinks", "competitor analysis", "content cluster", "seo audit", "geo optimization", "ai search", "search console", "organic traffic", "content strategy", "publish article", "seo setup", "ranking", "impressions", "ctr", "meta description", "schema markup", "faq schema".
  Also trigger when a user wants to set up their SaaS blog SEO from scratch, analyze their current rankings, or create a publishing workflow.
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_CLIENT_ID
        - GOOGLE_CLIENT_SECRET
        - GOOGLE_REFRESH_TOKEN
        - DATAFORSEO_LOGIN
        - DATAFORSEO_PASSWORD
      bins:
        - curl
    recommendedSkills:
      - seo-geo
      - ga4
      - dataforseo
---

# SEO + GEO for SaaS

A battle-tested SEO system built by a bootstrapped SaaS founder who grew from 0 to 30k+ organic sessions/month. This isn't theory — it's the exact methodology, templates, and checklists used to rank a real SaaS product.

This skill covers two modes:
1. **Setup** — onboard a new SaaS, analyze existing SEO, build a strategy, create a content calendar
2. **Publish** — write, optimize, and ship SEO+GEO articles using proven templates

---

## First-time setup

If the user has never used this skill before (no `seo/` directory in their project), run the onboarding flow. Read `references/onboarding.md` for the full step-by-step process.

**Onboarding creates these files in the user's project:**
```
seo/
├── overview.md        # Site architecture, clusters, competitor landscape — context for spawning new agents
├── keywords.md        # Master keyword table — local cache, avoids repeat API calls
├── opportunities.md   # Prioritized gaps, CTR fixes, quick wins
├── published.md       # Log of every published article — avoids needing a database
├── calendar.md        # 5-month content calendar with progress tracking
├── positioning.md     # Current rankings snapshot — updated during audits
├── templates.md       # Article templates adapted for the user's SaaS
└── screenshots/       # Product screenshots to use as article images
├── positioning.md     # Current rankings snapshot
└── templates.md       # Article templates adapted for their SaaS
```

---

## Choosing your SEO data source

This skill works with two data providers. During onboarding, ask the user which they have access to:

**Option A: SemRush** (preferred if available)
- More accurate keyword data, better competitor intelligence
- If the user has the `semrush-research` skill installed, use it directly
- Otherwise, ask the user to export data from SemRush web UI (CSV exports)

**Option B: DataForSEO** (recommended if no SemRush)
- Cheaper, API-first, good enough for most SaaS
- If the user has the `dataforseo` skill installed, use it directly
- If the user has an account, help them configure credentials

**Option C: Manual data**
- User pastes data from Google Search Console, exports, or screenshots
- Works but slower — encourage API setup for ongoing use

Always check which skills are available before asking the user to install anything.

---

## Two operating modes

### Mode 1: Strategy & Analysis

Use when the user asks to analyze their SEO, find opportunities, audit performance, or plan content.

**Workflow:**
1. Read the user's `seo/` files to understand current state
2. Pull fresh data (via SemRush, DataForSEO, or user-provided exports)
3. Update the relevant files (keywords.md, opportunities.md, positioning.md)
4. Recommend next actions based on the data

**Key analyses available:**
- Keyword gap analysis (what competitors rank for that you don't)
- CTR audit (high-impression pages with low CTR = quick wins)
- Content cluster mapping (identify missing hub/spoke pages)
- Competitor benchmarking (traffic, keywords, content strategy)
- Ranking movement tracking (what's improving, what's dropping)

For keyword research methodology, read `references/keyword-research.md`.
For content cluster strategy, read `references/content-strategy.md`.
For the biweekly audit framework, read `references/audit-framework.md`.

### Mode 2: Content Publishing

Use when the user asks to write an article, blog post, or any SEO content.

**Workflow:**
1. Read `seo/templates.md` to pick the right template
2. Read `seo/keywords.md` to identify target keywords
3. Write the article following the template structure
4. Apply GEO optimization (read `references/geo-optimization.md`)
5. Run pre-publish checklist (read `references/pre-publish-checklist.md`)
6. Generate thumbnail if needed (read `references/thumbnail-guide.md`)

**Important:** Before writing ANY article, invoke the `seo-geo` companion skill for validation (listed in recommended skills above). It handles technical SEO validation, schema markup, AI bot access, and GEO scoring. This skill handles strategy, templates, and the publishing workflow. They complement each other.

For article templates, read `references/templates.md`.
For the pre-publish checklist, read `references/pre-publish-checklist.md`.

---

## Reference files

| File | When to read |
|------|-------------|
| `references/onboarding.md` | First-time setup, when user says "set up SEO" or no `seo/` folder exists |
| `references/keyword-research.md` | Keyword analysis, finding opportunities, gap analysis |
| `references/content-strategy.md` | Cluster planning, content architecture, competitor mapping |
| `references/templates.md` | Writing any article or blog post |
| `references/pre-publish-checklist.md` | Before publishing any content (ALWAYS read this) |
| `references/geo-optimization.md` | Optimizing for AI search engines (ChatGPT, Perplexity, etc.) |
| `references/audit-framework.md` | Biweekly performance audits, tracking progress |
| `references/thumbnail-guide.md` | Creating blog post thumbnails |

---

## Key principles

**This skill is built for SaaS companies.** Every recommendation assumes:
- You're selling software, not content
- Articles exist to drive signups, not ad revenue
- Your product IS the CTA — not affiliate links
- Competitor comparisons are a core content type
- Technical credibility matters more than content volume

**Content clusters, not random articles.** Every piece of content belongs to a cluster with a pillar page. Orphan content is wasted effort.

**CTR fixes before new content.** If you have pages with thousands of impressions but <1% CTR, fix those first. It's the fastest ROI in SEO.

**GEO is not optional.** AI search engines (ChatGPT, Perplexity, Gemini, Claude) are sending increasing traffic. Every article must be optimized for both Google AND AI citation. The Princeton 9 methods are baked into every template.

**Measure everything.** Biweekly audits are built into the calendar. No audit = no idea if your strategy is working.
