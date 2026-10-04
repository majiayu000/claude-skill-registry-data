---
name: early-signal-intel
description: Collect, route, normalize, and synthesize early research discussion signals from alphaXiv, Hacker News, lab/research blogs via RSS, Bluesky/AT Protocol, and carefully scoped Reddit sources. Use when Codex needs a no-required-key baseline plus optional authenticated setup for paper discussion, community controversy, engineering spread, scholar-post signals, lab blog monitoring, or auditable JSONL/CSV/Markdown reports from fourth-priority "discussion and early signal" channels.
---

# Early Signal Intel

## Overview

Use this skill for "fourth priority" research-signal sources: alphaXiv, Hacker News, Reddit r/MachineLearning, Bluesky/X scholar posts, and lab blogs. The default closure must work without private credentials by using HN public APIs and RSS/Atom feeds first. Optional alphaXiv, Bluesky, Reddit, and X routes require explicit setup and must keep secrets private.

## Decision Tree

1. Identify the target:
   - arXiv paper discussion or alphaXiv URL;
   - Hacker News story, user, URL, or keyword search;
   - lab/company/university research blog feed;
   - Bluesky scholar account, keyword, or short real-time firehose window;
   - Reddit subreddit/topic anecdotal context;
   - cross-source early-signal report for a paper, model, repo, benchmark, or research direction.
2. Run a route plan before crawling:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py plan `
  --target "2603.04379 agent frameworks discussion" `
  --needs alphaxiv,hn,rss,bluesky,report `
  --scale small
```

3. Execute only the needed lane:
   - HN: use official Firebase API for story/comment trees and Algolia HN Search for search. No key required.
   - RSS/lab blogs: use RSS/Atom feeds and lightweight HTML discovery. No key required.
   - alphaXiv: prefer `alphaxiv-py` when installed; use public paper/comment endpoints only. API key is optional.
   - Bluesky: prefer public AT Protocol/Jetstream routes for short windows; use app passwords or OAuth only after explicit setup.
   - Reddit: use official Reddit API/PRAW only after explicit OAuth setup; treat as anecdotal/community signal.
   - X/Twitter: do not use unofficial scrapers by default. Use official X API only if the user approves cost and credentials.
4. Normalize before synthesis. Reports should cite normalized row IDs and source URLs, not loose snippets or browser state.

## Common Commands

Classify a URL:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py inspect-url `
  "https://news.ycombinator.com/item?id=41478690"
```

Print the normalized artifact contract:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py schema
```

Generate a run scaffold:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py scaffold `
  --output-dir output\early_signal\alphaxiv_hn_agent_papers `
  --target "agent framework paper discussion" `
  --needs alphaxiv,hn,rss,report
```

Run safe no-key setup and smoke tests:

```powershell
powershell -ExecutionPolicy Bypass -File skills\early-signal-intel\scripts\setup_early_signal_intel.ps1 -RunNetworkSmoke
```

Search HN with Algolia and save raw JSON:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py fetch-hn `
  --query "alphaXiv arXiv discussion" `
  --output output\early_signal\hn_search.json
```

The default HN search uses `--tags story` for story-level diffusion signals. Add a more specific tag only when you intentionally need HN comments or other Algolia filters.

Fetch a Hacker News thread via the official Firebase API:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py fetch-hn `
  --item-id 41478690 `
  --include-comments `
  --max-comments 40 `
  --output output\early_signal\hn_thread.json
```

Fetch RSS/Atom feeds:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py fetch-rss `
  --feed https://openai.com/news/rss.xml `
  --feed https://research.google/blog/rss/ `
  --output output\early_signal\lab_blog_feeds.json
```

Normalize a raw capture:

```powershell
python skills\early-signal-intel\scripts\early_signal_intel.py normalize `
  --input output\early_signal\hn_thread.json `
  --source hn `
  --output-dir output\early_signal\normalized
```

## Full Setup And Credentials

Read `references/full-setup.md` before configuring optional providers. For credential setup, use `$external-api-onboarding` and the helpers below so secrets stay out of chat, command output, repo files, and final summaries.

```powershell
powershell -ExecutionPolicy Bypass -File skills\early-signal-intel\scripts\assist_early_signal_auth.ps1 -Provider alphaxiv
powershell -ExecutionPolicy Bypass -File skills\early-signal-intel\scripts\assist_early_signal_auth.ps1 -Provider reddit
powershell -ExecutionPolicy Bypass -File skills\early-signal-intel\scripts\assist_early_signal_auth.ps1 -Provider bluesky
```

Store optional provider secrets only under:

`%USERPROFILE%\.codex\skills\early-signal-intel\.env`

Never commit `.env`, OAuth tokens, app passwords, cookies, browser storage, or auth headers.

## Source Routing

Read `references/source-routing.md` before selecting a backend.

- Use HN Firebase and Algolia first for engineering diffusion signals.
- Use RSS/Atom first for lab blog monitoring; fall back to HTML discovery only when no feed is visible.
- Use alphaXiv for arXiv-specific discussion, comments, resources, and community attention.
- Use Bluesky for time-sensitive scholar/account signals; prefer bounded windows and seed accounts over broad firehose collection.
- Use Reddit as anecdotal context only, with official API/PRAW and strict rate limits after user-approved setup.
- Keep X/Twitter optional and official-API-only by default; do not install login scrapers unless the user explicitly asks and accepts the risk.

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched API JSON, RSS XML/JSON transforms, fetched HTML, and logs.
- `normalized/items.jsonl`: normalized stories, posts, feed entries, paper discussion entries, and search hits.
- `normalized/comments.jsonl`: normalized comments, replies, and thread excerpts.
- `normalized/sources.jsonl`: source metadata, feeds, accounts, API routes, and access status.
- `sources.csv`: source review table with URL, source type, priority, status, and auth requirement.
- `manifest.json`: plan, commands, timestamps, limits, credentials policy, and blockers.
- `summary.md`: human-facing synthesis grounded in normalized row IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Default work must remain useful without paid APIs, private credentials, login-gated data, or unofficial scrapers.
- Prefer official public APIs, RSS feeds, and provider docs over search snippets and scraped web UI.
- Treat Reddit, HN, Bluesky, and X as community signals, not authoritative paper facts.
- Summarize and cite URLs; do not bulk republish copyrighted comments or posts.
- Do not train models on user-generated content captured through this skill.
- Do not bypass paywalls, CAPTCHAs, login gates, rate limits, platform controls, or deleted/removed content.
- Keep API keys, OAuth tokens, app passwords, cookies, `.env`, browser storage, request headers, and proxy URLs out of git and final answers.
- Use small smoke tests before bulk collection; record rate limits and blockers in `manifest.json`.

## Resources

- `scripts/early_signal_intel.py`: planner, URL inspector, scaffold generator, HN/RSS fetchers, schema printer, and normalizer.
- `scripts/setup_early_signal_intel.ps1`: safe setup and smoke-test helper for no-key baseline plus optional Python runtime.
- `scripts/assist_early_signal_auth.ps1`: visible, external-api-onboarding-compatible credential setup helper.
- `references/full-setup.md`: optional provider setup matrix, env var names, and smoke tests.
- `references/source-routing.md`: detailed source selection, API boundaries, and caution flags.
- `references/output-schema.md`: normalized JSONL fields and merge policy.
