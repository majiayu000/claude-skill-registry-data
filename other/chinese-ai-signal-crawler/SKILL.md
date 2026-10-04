---
name: chinese-ai-signal-crawler
description: Collect, route, normalize, and synthesize Chinese AI secondary-media and commercialization signals from machines/AI media sites, RSS/RSSHub feeds, AnySearch discovery, WeChat article URLs, Bilibili creators/videos/comments, and optional MediaCrawler-style self-media captures. Use when Codex needs sixth-priority Chinese AI diffusion evidence, breakout-signal monitoring, source triage for 机器之心, 量子位, PaperWeekly, 新智元, AI科技评论, 公众号, 视频号, B站技术UP, or auditable JSONL/CSV/Markdown reports that must be cross-checked against primary papers or official releases.
---

# Chinese AI Signal Crawler

## Overview

Use this skill for the sixth-priority lane: Chinese secondary propagation and commercialization observation. The default closure must work without private credentials by using public pages, RSS/Atom feeds, and AnySearch anonymous discovery first. WeChat, Bilibili, and MediaCrawler-style platform captures are optional and must keep credentials, cookies, browser state, and API keys private.

## Decision Tree

1. Identify the target:
   - paper, model, company, repo, benchmark, author, or Chinese topic phrase;
   - one media channel such as 机器之心, 量子位, PaperWeekly, 新智元, AI科技评论;
   - WeChat article URL, album URL, official-account list, Bilibili UP UID, Bilibili video URL, or MediaCrawler platform task;
   - cross-source report about whether an English paper/model broke into the Chinese AI circle.
2. Run a route plan before crawling:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py plan `
  --target "SWE-agent 论文 中文AI圈传播" `
  --needs media,anysearch,wechat,bilibili,report `
  --scale small
```

3. Execute only the needed lane:
   - public media pages: use `fetch-page` for light public homepage/article-index capture;
   - RSS/RSSHub: use `fetch-rss` when a feed or RSSHub route is known;
   - AnySearch: use `fetch-anysearch` for discovery, then verify important claims against primary sources;
   - WeChat: prefer `wespy-plus` for article URLs and Markdown/JSON export; use heavier WeChat crawlers only for user-approved research datasets;
   - Bilibili: use small UID/video/comment captures only for propagation signals, not authority;
   - MediaCrawler: use as optional platform capture for B站, 微博, 知乎, 小红书 and similar public content after setup.
4. Normalize before synthesis. Reports should cite normalized row IDs and source URLs, and mark all Chinese media claims as secondary until checked against original papers, official releases, or repositories.

## Common Commands

Classify a URL:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py inspect-url `
  "https://www.qbitai.com/"
```

Print the output schema:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py schema
```

Generate a run scaffold:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py scaffold `
  --output-dir output\chinese_ai_signal\swe_agent_cn_diffusion `
  --target "SWE-agent paper Chinese AI diffusion" `
  --needs media,anysearch,wechat,bilibili,report
```

Fetch public media pages:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py fetch-page `
  --url https://www.jiqizhixin.com/ `
  --url https://www.qbitai.com/ `
  --max-links 30 `
  --output output\chinese_ai_signal\raw\media_pages.json
```

Fetch RSS/Atom feeds:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py fetch-rss `
  --feed https://example.com/rss.xml `
  --max-entries 20 `
  --output output\chinese_ai_signal\raw\feeds.json
```

Discover via AnySearch:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py fetch-anysearch `
  --query "SWE-agent 机器之心 量子位 新智元 PaperWeekly" `
  --max-results 10 `
  --output output\chinese_ai_signal\raw\anysearch.md
```

Normalize a raw capture:

```powershell
python skills\chinese-ai-signal-crawler\scripts\chinese_ai_signal_crawler.py normalize `
  --input output\chinese_ai_signal\raw\media_pages.json `
  --source media-page `
  --output-dir output\chinese_ai_signal\normalized
```

## Setup And External API Closure

Run the no-secret setup and smoke tests:

```powershell
powershell -ExecutionPolicy Bypass -File skills\chinese-ai-signal-crawler\scripts\setup_chinese_ai_signal_crawler.ps1 -RunNetworkSmoke
```

Required credentials: none.

Optional providers must be configured through `$external-api-onboarding` rules and stored only in private user-level paths:

```text
%USERPROFILE%\.codex\skills\chinese-ai-signal-crawler\.env
%USERPROFILE%\.codex\skills\anysearch\.env
```

Use the assisted helper for provider pages and hidden local secret prompts:

```powershell
powershell -ExecutionPolicy Bypass -File skills\chinese-ai-signal-crawler\scripts\assist_chinese_ai_signal_auth.ps1 -Provider anysearch
powershell -ExecutionPolicy Bypass -File skills\chinese-ai-signal-crawler\scripts\assist_chinese_ai_signal_auth.ps1 -Provider wechat
powershell -ExecutionPolicy Bypass -File skills\chinese-ai-signal-crawler\scripts\assist_chinese_ai_signal_auth.ps1 -Provider bilibili
powershell -ExecutionPolicy Bypass -File skills\chinese-ai-signal-crawler\scripts\assist_chinese_ai_signal_auth.ps1 -Provider mediacrawler
```

The helper opens official provider or repository pages only. The user completes login, MFA, CAPTCHA, key creation, cookie export, and secret copy. Do not paste secrets into chat.

Read `references/full-setup.md` before configuring optional providers.

## Source Routing

Read `references/source-routing.md` before selecting a backend.

- Use public media pages and RSS/RSSHub first for 机器之心, 量子位, PaperWeekly, 新智元, AI科技评论, and AI newsletter-style aggregation.
- Use AnySearch for discovery and recall, not as final authority.
- Use WeChat article/album tools for source text extraction when a URL is already known.
- Use Bilibili and MediaCrawler outputs as propagation and engagement signals only.
- For every important claim, add `needs_primary_source_check=true` until verified against the paper, official release, project repo, venue page, or company/lab blog.

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched AnySearch Markdown, RSS JSON, page-capture JSON, exported WeChat/Bilibili/MediaCrawler files, and logs.
- `normalized/items.jsonl`: media articles, feed entries, search hits, videos, posts, and crawler records.
- `normalized/comments.jsonl`: bounded comments/replies when comments are part of the task.
- `normalized/sources.jsonl`: source metadata, route status, auth requirement, and risk notes.
- `sources.csv`: human review table with URL, source type, priority, status, auth requirement, and risk.
- `manifest.json`: target, plan, commands, limits, credentials policy, timestamps, and blockers.
- `reports/summary.md`: synthesis grounded in normalized row IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Default work must remain useful without paid APIs, private tokens, cookies, proxies, login-gated data, or unofficial scrapers.
- Treat Chinese AI media, WeChat posts, and videos as secondary propagation evidence, not first-source research facts.
- Do not bypass paywalls, CAPTCHAs, login gates, rate limits, robots restrictions, deleted content, or platform controls.
- Do not bulk republish copyrighted articles, WeChat posts, video transcripts, or comments; summarize sparingly and cite URLs.
- Do not train models on user-generated content captured through this skill.
- Keep credentials, cookies, browser storage, proxy URLs, request headers, `.env`, and account details out of git and final answers.
- Run small smoke tests before bulk collection; record blocked or stale routes in `manifest.json`.

## Resources

- `scripts/chinese_ai_signal_crawler.py`: planner, URL inspector, scaffold generator, public page/RSS/AnySearch fetchers, schema printer, and normalizer.
- `scripts/setup_chinese_ai_signal_crawler.ps1`: no-secret setup and smoke-test helper.
- `scripts/assist_chinese_ai_signal_auth.ps1`: external-api-onboarding-compatible provider-page opener and secret-storage helper.
- `references/full-setup.md`: optional provider setup, env vars, storage paths, and smoke tests.
- `references/source-routing.md`: detailed source selection and fallback policy.
- `references/output-schema.md`: normalized JSONL fields and merge policy.
