---
name: kio-growth-marketing
description: "Kio Growth, CRO & SEO hub: one Kio router over 79 sub-skills (53 growth/marketing modules + 26 SEO/GEO engine sub-skills, 19 SEO agents, 60+ Python checks). Use for anything marketing or search: conversion/CRO, landing pages, signup, onboarding, pricing, paywalls, offers, A/B tests, copywriting & editing, content strategy, emails, cold email, SMS, social, ads & ad creative, launches, referrals, PR, influencers, community, events, sales enablement, RevOps, prospecting, analytics, attribution, conversion tracking, churn, competitor research, SEO audits, technical SEO, schema, AI search/GEO (AI Overviews, ChatGPT, Perplexity), llms.txt, local SEO/GBP, hreflang, sitemaps, backlinks, programmatic SEO, ASO, marketing plans and ideas."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 3.0.0
---

# 📈 Kio Growth, CRO & SEO (`kio-growth-marketing`)

The router for Kio's **79 sub-skills**: 53 growth/marketing modules (`references/modules/`) and 26 Kio SEO Engine sub-skills (`references/seo/subskills/`). This file holds **no** domain knowledge; it only points the way. The knowledge lives in each module.

## ⚙️ How to work (mandatory, in order)

1. **Read product context first.** If the project has `.agents/product-marketing.md` (or `.claude/product-marketing.md`, legacy `product-marketing-context.md`), read it before asking the user anything. If it is missing and the task needs deep context (plans, copy, positioning), run the `product-marketing` module to create it.
2. **Pick one primary module** from the [Routing table](#-routing-table-79-sub-skills). For overlapping pairs use the [Merge rules](#-merge-rules-for-overlapping-modules). Open that module's `SKILL.md` and **follow its process exactly**.
3. **Open `references/` only when the module says so** (its "Reference Routing" table). Never preload the folder.
4. **When a module names another module** ("see **signup**", "use the `ab-testing` skill"), read it as `references/modules/<name>/SKILL.md`; a `seo-` name that is not in `references/modules/` means `references/seo/subskills/<name>/SKILL.md`. `seo-audit` exists in both: see merge rule #1.
5. **Multi-step jobs** (launches, a landing page from scratch, a full SEO audit…) follow the [Multi-module workflows](#-multi-module-workflows).
6. **Tools and APIs**: `references/tools/REGISTRY.md` (index), `references/tools/integrations/<tool>.md` (106 guides), `scripts/clis/` (67 CLIs). Never invent endpoints.
7. **MANDATORY reads:** an SEO audit → `references/seo/subskills/seo-audit/SKILL.md` and `seo-technical`; schema markup → `seo-schema`; AI search / GEO → `seo-geo`. Open the sub-skill file before answering and name it in the answer.

## 🧭 Routing table (79 sub-skills)

`M/` = `references/modules/`, `S/` = `references/seo/subskills/`.

### 1. Conversion (CRO) & product
| Sub-skill | Path | Use when |
|---|---|---|
| `cro` | `M/cro` | A page or form is not converting: homepage, landing, pricing page (visitors skip the intended tier, bounce), contact/demo forms |
| `signup` | `M/signup` | Signup, registration, account creation, trial activation |
| `onboarding` | `M/onboarding` | Post-signup activation, first-run, time-to-value |
| `popups` | `M/popups` | Popups, modals, slide-ins, exit intent, banners |
| `paywalls` | `M/paywalls` | In-app paywalls, upgrade screens, feature gates, upsells |
| `pricing` | `M/pricing` | Deciding price points, tiers, freemium/trial, packaging, price surveys (Van Westendorp) |
| `offers` | `M/offers` | Designing the offer: value framing, bonuses, guarantees, scarcity |
| `ab-testing` | `M/ab-testing` | Designing or reading A/B tests, experimentation programs; also writing variants to test against the current version |
| `marketing-psychology` | `M/marketing-psychology` | Behavioural science and mental models in marketing |
| `churn-prevention` | `M/churn-prevention` | Cancel flows, save offers, failed-payment dunning |

### 2. Content & copy
| Sub-skill | Path | Use when |
|---|---|---|
| `copywriting` | `M/copywriting` | Writing or rewriting page copy (hero, features, pricing, about) |
| `copy-editing` | `M/copy-editing` | Editing, reviewing, refreshing existing copy |
| `content-strategy` | `M/content-strategy` | What to write, which topics, content calendar |
| `image` | `M/image` | Marketing images: blog heroes, social graphics, mockups, banners; choosing web image formats and sizes |
| `video` | `M/video` | Producing video with AI tools or programmatic frameworks |
| `free-tools` | `M/free-tools` | Planning, evaluating or building free tools for leads and SEO |
| `lead-magnets` | `M/lead-magnets` | Ebooks, checklists, templates, mini-courses |

### 3. Channels & campaigns
| Sub-skill | Path | Use when |
|---|---|---|
| `emails` | `M/emails` | Automated sequences, drips, lifecycle email |
| `cold-email` | `M/cold-email` | B2B outbound: cold email, follow-ups, LinkedIn, cadences |
| `sms` | `M/sms` | SMS/MMS/WhatsApp: welcome, abandoned cart, win-back |
| `social` | `M/social` | Content and scheduling for LinkedIn, X, Instagram, TikTok, Facebook |
| `ads` | `M/ads` | Google/Meta/LinkedIn/X campaigns: structure, budget, audits |
| `ad-creative` | `M/ad-creative` | Writing and scaling ad copy: headlines, primary text, variants |
| `launch` | `M/launch` | Product/feature launches, Product Hunt |
| `events` | `M/events` | Webinars, conferences, trade shows, meetups, sponsorships |
| `public-relations` | `M/public-relations` | PR, earned media, journalist outreach |
| `influencer-marketing` | `M/influencer-marketing` | Creator/influencer/ambassador partnerships, podcast/newsletter sponsorships, sponsorship ROI |
| `community-marketing` | `M/community-marketing` | Discord/Slack/forum communities |
| `co-marketing` | `M/co-marketing` | Finding partners, joint campaigns |
| `referrals` | `M/referrals` | Referral, affiliate, review and word-of-mouth programs |
| `directory-submissions` | `M/directory-submissions` | Listing on SaaS/AI/MCP directories for backlinks |
| `aso` | `M/aso` | App Store / Google Play optimisation |

### 4. Sales & revenue
| Sub-skill | Path | Use when |
|---|---|---|
| `prospecting` | `M/prospecting` | Finding and qualifying prospect lists |
| `sales-enablement` | `M/sales-enablement` | Pitch decks, one-pagers, objection handling, demo scripts, cold-call scripts and voicemails |
| `revops` | `M/revops` | Lead lifecycle, scoring, routing, marketing → sales handoff |

### 5. Measurement
| Sub-skill | Path | Use when |
|---|---|---|
| `analytics` | `M/analytics` | Setting up or auditing tracking: GA4, GTM, event plans |
| `conversion-tracking` | `M/conversion-tracking` | Fixing/verifying conversion events: forms, bookings, chat, calls, purchases |
| `attribution` | `M/attribution` | Which channels really drive revenue, choosing a model, identity and server-side (first-party) event delivery |

### 6. Strategy & research
| Sub-skill | Path | Use when |
|---|---|---|
| `product-marketing` | `M/product-marketing` | Creating/updating the product context doc (read in step 1) |
| `marketing-plan` | `M/marketing-plan` | Full marketing plan: goals, channels, budget, team |
| `marketing-ideas` | `M/marketing-ideas` | Marketing ideas, building awareness/thought leadership when nobody knows the brand yet |
| `marketing-council` | `M/marketing-council` | Multiple expert perspectives challenging a decision |
| `marketing-loops` | `M/marketing-loops` | Recurring, self-running marketing workflows for agents |
| `customer-research` | `M/customer-research` | Customer interviews, ICP, research synthesis |
| `competitor-profiling` | `M/competitor-profiling` | Researching and profiling competitors from URLs |
| `competitors` | `M/competitors` | Comparison and "alternatives to X" pages |
| `reverse-engineer-marketing` | `M/reverse-engineer-marketing` | How a company grew, so you can copy what worked |

### 7. Marketing SEO (strategy, no scripts)
| Sub-skill | Path | Use when |
|---|---|---|
| `seo-audit` (module) | `M/seo-audit` | Quick "why am I not ranking" diagnosis (local business sites included) without tools |
| `ai-seo` | `M/ai-seo` | Writing/optimising content to be cited by AI |
| `schema` | `M/schema` | Choosing schema types, structured-data strategy |
| `programmatic-seo` | `M/programmatic-seo` | Planning template + data pages at scale (12 playbooks) |
| `site-architecture` | `M/site-architecture` | Page hierarchy, navigation, URLs, internal links |
| `link-building` | `M/link-building` | Earning backlinks and mentions |

### 8. Kio SEO Engine (scripts, agents, reports)
The shared entry point is `S/seo` (the `/seo …` orchestrator). Read [`references/seo/SKILL.md`](references/seo/SKILL.md) for how to run the scripts.

| Sub-skill | Path | Use when |
|---|---|---|
| `seo` | `S/seo` | Orchestrator: overall SEO analysis, picks sub-skills, runs agents in parallel |
| `seo-audit` (engine) | `S/seo-audit` | Scored site-wide audit with MD/HTML/PDF report |
| `seo-page` | `S/seo-page` | Deep analysis of one URL |
| `seo-technical` | `S/seo-technical` | Crawl, index, render, speed, Core Web Vitals, IndexNow |
| `seo-content` | `S/seo-content` | E-E-A-T, thinness, readability, AI-citation readiness |
| `seo-content-brief` | `S/seo-content-brief` | Briefs with per-section word counts and competitor scoring |
| `seo-cluster` | `S/seo-cluster` | SERP-overlap keyword clustering, hub-and-spoke |
| `seo-plan` | `S/seo-plan` | Industry-specific SEO roadmap |
| `seo-sxo` | `S/seo-sxo` | Search intent / page layout mismatch vs. the SERP |
| `seo-schema` | `S/seo-schema` | Detect, validate, generate JSON-LD for one page |
| `seo-sitemap` | `S/seo-sitemap` | Audit/generate XML sitemaps |
| `seo-hreflang` | `S/seo-hreflang` | Hreflang, multi-language/multi-region SEO |
| `seo-images` | `S/seo-images` | Image optimisation: alt, size, format, lazy load, CLS |
| `seo-image-gen` | `S/seo-image-gen` | Gemini-generated OG/hero/product images, only when the banana extension is installed |
| `seo-geo` | `S/seo-geo` | Auditing a URL for AI Overviews, ChatGPT, Perplexity |
| `seo-agentic` | `S/seo-agentic` | Can AI agents use the site: llms.txt, WebMCP, agent robots |
| `seo-flow` | `S/seo-flow` | FLOW framework (Find → Leverage → Optimize → Win) and stage prompts |
| `seo-local` | `S/seo-local` | Local SEO when the user asks specifically about GBP, map pack, NAP, citations, reviews |
| `seo-maps` | `S/seo-maps` | Geo-grid ranks, radius competitors, cross-platform reviews |
| `seo-ecommerce` | `S/seo-ecommerce` | Store SEO: product pages, Product schema, Shopping |
| `seo-programmatic` | `S/seo-programmatic` | Auditing live pSEO pages: thin content, index bloat |
| `seo-competitor-pages` | `S/seo-competitor-pages` | Technical layout of "X vs Y" pages: feature matrix, schema |
| `seo-backlinks` | `S/seo-backlinks` | Backlink profile, anchors, toxic links, disavow |
| `seo-drift` | `S/seo-drift` | SEO baselines, before/after deploy comparisons |
| `seo-google` | `S/seo-google` | Real data from GSC, PageSpeed, CrUX, Indexing API, GA4 |
| `seo-dataforseo` | `S/seo-dataforseo` | Live SERP/keyword/backlink data via DataForSEO |

## 🔀 Merge rules for overlapping modules

These pairs overlap. Kio merges each into **one entry point** ("Start at"); the other module is the deep dive, opened only when the last column applies.

| # | Need | Start at | Switch when |
|---|---|---|---|
| 1 | SEO audit | `M/seo-audit` | There is a URL and a scored report is wanted, or scripts can run → `S/seo-audit` (site), `S/seo-page` (one URL), `S/seo-technical` (technical only) |
| 2 | Schema | `M/schema` | JSON-LD must be validated/generated for a specific page → `S/seo-schema` |
| 3 | AI search / GEO | `M/ai-seo` | Auditing a URL → `S/seo-geo`; agents, llms.txt, WebMCP → `S/seo-agentic` |
| 4 | Programmatic SEO | `M/programmatic-seo` | Pages are live and need a thin-content/index-bloat check → `S/seo-programmatic` |
| 5 | Competitor pages | `M/competitors` | Dozens of templated "X vs Y" pages → `M/programmatic-seo` (Comparisons playbook); technical layout, schema → `S/seo-competitor-pages`; competitor data first → `M/competitor-profiling` |
| 6 | Backlinks | `M/link-building` | Analysing the existing link profile → `S/seo-backlinks` |
| 7 | Images | `M/image` (marketing images, formats, automated OG images at scale) | The Gemini image extension (banana) is installed → `S/seo-image-gen`; auditing one URL's images → `S/seo-images` |
| 8 | Content planning | `M/content-strategy` | SEO roadmap → `S/seo-plan`; keyword clustering → `S/seo-cluster`; per-article brief → `S/seo-content-brief` |
| 9 | Site structure | `M/site-architecture` | Keyword-cluster hub-and-spoke → `S/seo-cluster` |
| 10 | Content quality | `M/copywriting` (write) / `M/copy-editing` (edit) | E-E-A-T and thinness scoring → `S/seo-content` |
| 11 | Measurement | `M/analytics` | Wrong/missing conversion events → `M/conversion-tracking`; channel credit → `M/attribution`; GSC/CrUX data → `S/seo-google` |
| 12 | Email | `M/emails` (existing contacts) | Strangers, outbound → `M/cold-email`; SMS/WhatsApp → `M/sms` |
| 13 | Ads | `M/ads` | Only ad copy is needed → `M/ad-creative` |
| 14 | Local SEO | `M/seo-audit` ("site doesn't show up for near-me searches") | Specific GBP, NAP, citations → `S/seo-local`; geo-grid rank tracking, nearby competitors → `S/seo-maps` |
| 15 | Competitors | `M/competitor-profiling` | Learning how they grew → `M/reverse-engineer-marketing` |
| 16 | Overall strategy | `M/marketing-plan` | Only ideas → `M/marketing-ideas`; a challenge panel → `M/marketing-council` |
| 17 | Conversion | `M/cro` (pages/forms, pricing page included) | Signup → `M/signup`; post-signup → `M/onboarding`; popups → `M/popups`; in-app upgrades → `M/paywalls` |

## 🧩 Multi-module workflows

| Job | Module order |
|---|---|
| Landing page from scratch | `product-marketing` → `customer-research` (if insight is missing) → `offers` → `copywriting` → `cro` → `ab-testing` → `conversion-tracking` |
| Product launch | `product-marketing` → `launch` → `emails` + `social` + `public-relations` → `directory-submissions` → `analytics` |
| Full SEO audit | `S/seo` (or `S/seo-audit`) → `S/seo-technical` + `S/seo-content` + `S/seo-schema` + `S/seo-geo` → report via `render-report.mjs` |
| Grow organic traffic | `content-strategy` → `S/seo-cluster` → `S/seo-content-brief` → `copywriting` → `M/schema` → `link-building` |
| Reduce SaaS churn | `analytics` → `onboarding` → `churn-prevention` → `emails` |
| Client marketing plan | `product-marketing` → `competitor-profiling` → `marketing-plan` → `marketing-council` (challenge) |
| B2B outbound | `prospecting` → `cold-email` → `sales-enablement` → `revops` |

## 🛡️ Kio global rules

1. **No buzzwords.** Ban "unlock synergies", "next-gen revolution", "game-changing", "unleash". Copy states concrete outcomes and real customer pain.
2. **Evidence first.** Every finding cites a URL, HTTP status, DOM snippet or real number. Missing data is labelled a hypothesis; never invent figures.
3. **No ranking or growth promises.** SEO and CRO are evidence-based optimisation, not guarantees.
4. **Never change production unasked.** URL, canonical, robots.txt, redirect, price and tracking changes need user approval.
5. **Valid structured data.** Articles, products and local businesses get valid JSON-LD; never mark up content that is not on the page.
6. **`noindex` sensitive pages.** `/cart`, `/checkout`, `/wp-admin`, internal pages.
7. **Language.** Answer in the user's language; English modules work for Vietnamese users too.

## 📦 What's included

- `references/modules/` — 53 modules, each with `SKILL.md`, `references/`, `evals/evals.json`.
- `references/seo/` — Kio SEO Engine: 26 sub-skills, 19 agents (`agents/`), 60+ scripts (`scripts/`), `requirements.txt`.
- `tools/` — `REGISTRY.md`, `integrations/` (106 services), `clis/` (67 CLIs), `composio/`.
- `assets/partners.json` — tool partner list.
- `THIRD_PARTY_NOTICES.md` — the required copyright and license notices for the open-source sources Kio uses. Keep this file when redistributing.
