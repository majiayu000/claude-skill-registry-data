---
name: ai-lab-blog-intel
description: Collect, crawl, normalize, and synthesize AI company and laboratory research blog intelligence from first-party RSS/Atom feeds, sitemaps, public HTML indexes, and optional third-party search/API helpers. Use when Codex needs no-required-key monitoring or auditable reports for OpenAI, Anthropic, Google DeepMind, Google Research, Meta AI, Microsoft Research, NVIDIA Research, Apple Machine Learning Research, Allen AI, Stanford HAI, BAIR, MIT CSAIL, CMU ML, or similar fifth-priority "company and lab research blog" channels.
---

# AI Lab Blog Intel

## Overview

Use this skill for the "fifth priority" source class: company and lab research blogs. The default closure must work without private credentials by using first-party RSS/Atom feeds, sitemaps, and lightweight public HTML extraction. Optional AnySearch, Apify, provider APIs, or MCP routes are enhancements and must be configured through `$external-api-onboarding`.

This skill is for tracking how frontier research becomes product, engineering, alignment/safety, agent tooling, benchmark, and system-design narratives. It complements `paper-review-source-intel` and `code-model-benchmark-intel`; use those skills when the user needs official paper/proceedings/review evidence or code/model/benchmark evidence.

## Decision Tree

1. Identify the target:
   - one organization or lab blog;
   - a set of frontier AI company blogs;
   - model release, system design, safety/alignment, agent tooling, benchmark controversy, or productization trend;
   - a URL that may be a feed, sitemap, blog index, or individual article.
2. Run a route plan before crawling:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py plan `
  --target "frontier model release blogs" `
  --org openai --org anthropic --org deepmind --org meta-ai `
  --needs posts,links,report `
  --scale small
```

3. Execute only the needed lane:
   - RSS/Atom: use first-party feeds first.
   - Sitemap: use first-party XML sitemaps to discover posts when feeds are missing or stale.
   - HTML index: use lightweight link extraction for public blog indexes and pagination.
   - Article extraction: fetch individual public articles only when full-text summaries, linked papers/repos, or topic labels are needed.
   - AnySearch: use only for discovery or freshness cross-checking when the user asks for live search or a feed/index is unclear.
   - Apify or third-party actors: optional fallback after explicit setup; do not make paid services mandatory.
4. Normalize before synthesis. Reports should cite normalized row IDs and source URLs, not loose search snippets.

## Common Commands

Classify a URL:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py inspect-url `
  "https://www.anthropic.com/research"
```

Print the normalized artifact contract:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py schema
```

Generate a run scaffold:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py scaffold `
  --output-dir output\ai_lab_blog\frontier_releases `
  --target "frontier lab model release blogs" `
  --org openai --org anthropic --org deepmind --org google-research --org meta-ai `
  --needs posts,links,report
```

Run safe setup and no-key smoke tests:

```powershell
powershell -ExecutionPolicy Bypass -File skills\ai-lab-blog-intel\scripts\setup_ai_lab_blog_intel.ps1 -RunNetworkSmoke
```

Fetch default first-party feeds:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py fetch-feeds `
  --org openai --org google-research --org deepmind --org microsoft-research `
  --output output\ai_lab_blog\raw\feeds.json
```

Fetch HTML indexes for sources without RSS:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py fetch-index `
  --org anthropic --org meta-ai `
  --max-pages 2 `
  --output output\ai_lab_blog\raw\indexes.json
```

Fetch sitemaps:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py fetch-sitemap `
  --url https://www.anthropic.com/sitemap.xml `
  --include "/research/" --include "/news/" `
  --output output\ai_lab_blog\raw\anthropic_sitemap.json
```

Normalize a raw capture:

```powershell
python skills\ai-lab-blog-intel\scripts\ai_lab_blog_intel.py normalize `
  --input output\ai_lab_blog\raw\feeds.json `
  --source feed `
  --output-dir output\ai_lab_blog\normalized
```

## External API Setup

Read `references/full-setup.md` before configuring optional providers. For credential setup, use `$external-api-onboarding` and the helper below so secrets stay out of chat, command output, repo files, and final summaries.

```powershell
powershell -ExecutionPolicy Bypass -File skills\ai-lab-blog-intel\scripts\assist_ai_lab_blog_auth.ps1 -Provider anysearch
powershell -ExecutionPolicy Bypass -File skills\ai-lab-blog-intel\scripts\assist_ai_lab_blog_auth.ps1 -Provider apify
```

Store optional provider secrets only under:

`%USERPROFILE%\.codex\skills\ai-lab-blog-intel\.env`

Never commit `.env`, API keys, OAuth tokens, cookies, browser storage, request headers, or provider console screenshots that reveal secrets.

## Source Routing

Read `references/source-routing.md` before selecting a backend.

- Use first-party RSS/Atom feeds for OpenAI, Google Research, Google DeepMind, Microsoft Research, NVIDIA, Apple ML, Allen AI, BAIR, MIT News, and similar sources when available.
- Use HTML/Next.js or sitemap extraction for Anthropic and Meta AI because current RSS endpoints may be absent or stale.
- Use AnySearch only for discovery, verification, or finding current source URLs; do not treat snippets as canonical evidence.
- Use third-party feed generators only as fallback or implementation inspiration; mark them `secondary` unless the generated feed is owned by the observed organization.

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched feed JSON transforms, sitemap captures, fetched HTML snippets, article text, and logs.
- `normalized/posts.jsonl`: normalized post, article, announcement, research note, and blog index rows.
- `normalized/links.jsonl`: linked papers, arXiv/DOI URLs, GitHub repos, model cards, datasets, benchmark pages, docs, and product pages.
- `normalized/sources.jsonl`: source metadata, feed/index/sitemap routes, access status, credential policy, and freshness.
- `sources.csv`: source review table with URL, source type, priority, status, and auth requirement.
- `manifest.json`: plan, commands, timestamps, limits, credentials policy, and blockers.
- `reports/summary.md`: human-facing synthesis grounded in normalized row IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Default work must remain useful without paid APIs, private credentials, login-gated data, or unofficial scrapers.
- Prefer first-party feeds, sitemaps, official pages, and provider docs over search snippets and aggregator claims.
- Do not bypass paywalls, CAPTCHAs, login gates, robots controls, rate limits, platform controls, or deleted/removed content.
- Keep crawls small by default; run smoke tests before bulk collection and record rate limits or blockers in `manifest.json`.
- Respect copyright: summarize and cite links; do not bulk republish full articles.
- Keep API keys, OAuth tokens, cookies, `.env`, browser storage, request headers, and proxy URLs out of git and final answers.
- Preserve `source_url`, `source_id`, `fetched_at`, and `source_priority` for every normalized row.

## Resources

- `scripts/ai_lab_blog_intel.py`: planner, URL inspector, scaffold generator, RSS/sitemap/index fetchers, schema printer, and normalizer.
- `scripts/setup_ai_lab_blog_intel.ps1`: safe setup and no-key smoke-test helper.
- `scripts/assist_ai_lab_blog_auth.ps1`: external-api-onboarding-compatible optional provider setup helper.
- `references/full-setup.md`: optional provider setup matrix, env var names, and smoke tests.
- `references/source-routing.md`: detailed source selection, API boundaries, and fallback policy.
- `references/output-schema.md`: normalized JSONL fields and merge policy.
