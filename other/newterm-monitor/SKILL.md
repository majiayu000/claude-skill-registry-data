---
name: newterm-monitor
description: >-
  Use when setting up or running daily emerging-keyword / meme monitoring:
  sources, gates, prescan→broadcast schedule, Trends cost controls, and report
  format.
---
# Emerging keyword monitor (newterm)

Reusable playbook for a bot that finds new searchable keywords / AI memes and sends Chinese broadcasts. No API keys belong in this skill — store them in the owner's `.env` or secret store only.

## Schedule (Asia/Shanghai)
- **Prescan** (data only, no user message): ~08:20, 10:20, 16:20 → slots `morning` / `noon` / `evening`
- **Broadcast**: 09:30, 11:58, 17:50 (noon = new items only; silence if none)
- **Night collect** (no broadcast): ~00:30, 04:30

Prescan writes under `prescan_<YYYYMMDD>_<slot>/`. Broadcasts only summarize; they do **not** re-run the heavy dry scan.

## Heat unit
Always report heat as **GPTs × N** = global past-7-day mean interest ÷ GPTs baseline (same idea as heat_ratio from keyword feeds that already provide it). Never dump raw Trends index numbers as the main figure.

## Source rules (what enters the broadcast)
**First-hand → broadcast when first seen; Trends is display-only (no gate):**
- Social: TikTok / X / TikHub-style meme search
- Reddit (first appearance + human noise filter)
- Big-site inner pages from sitemap radar
- Own first-hand: tool directories / GitHub (high-velocity new repos) / **GitHub Trending daily** / Hugging Face
- CapCut public trending templates
- Product Hunt new products (Atom; optional GraphQL if owner has a token)

**Still Trends-gated:**
- Curated keyword feed with verdicts (e.g. 「值得做」「可以试试」) + heat_ratio ≥ ×0.2
- Root rising / Trends hot searches ≥ ×0.2

**TikTok:** ≥ ×0.05 formal push (must note approximate appear time inside 来源); below → 「TikTok 早期观察」, first sighting must still be listed.

## Intent filters (not “no volume”)
Skip evergreen commerce/how-to, pure domain navigation, sports schedule noise, seasonal evergreen, brand shopping, one-day spikes that collapse, political news. For Reddit/CapCut, drop resolutions, quant names, pure param fragments; keep product / model / game / meme-like searchable terms.

## Dedup
Track pushed spellings in `pushed.json`. Same-day re-push of the same spelling: no. Prior days still over gate: may re-push. Noon: only brand-new terms or new spellings of old topics.

## Report shape (mobile-friendly, from 2026-10-25)
No tables. Never squeeze fields with `／`.

**Lead (max 2 lines):** title + one count line, e.g. `新增 23：新词 5 · 新写法 12 · TikTok早期 4`. No batch IDs, gate essays, or prescan status walls.

**Whitespace:** blank line between sections; blank line before each numbered term.

**Each formal term:** bold `**N. term**` alone on a line, then Markdown list lines. Drop the redundant `新词：` line (title already has the term).
- Required: 热度 (GPTs × N), 来源 (include roughly when it started rising), 是做什么的 (at most two short sentences: what it is; what searchers want)
- Optional one-per-line: 走势, 别称 (only if different from the title; replaces old 主流写法), 竞品网站, 推过记录, 哥飞, 风险
- Appear time is merged into 来源 (no separate 出现时间 line)

**New spellings:** shorter — 热度, 推过记录, 是做什么的; 来源 optional one line.

**Empty sections:** section title then `无` only.

**Sections:** 一新词；二新写法；三再推；四 TikTok+早期观察；五 Reddit/CapCut/Product Hunt/GitHub Trending；六大站内页；七过线但没推 (subheads by source, list lines; same-reason terms can share one line).

Owner-local sample file often lives at `BROADCAST_FORMAT.md` next to the pipeline.

## Pipeline layout (owner rebuilds code locally)
Typical tree under a workspace dir (e.g. `/workspace/newterm`):
- `prescan.sh <slot>` — orchestrates dry scan + TikTok + radars
- `night_collect.sh` — night-only collect
- Collectors: sitemap radar, Reddit RSS, CapCut public `/template`, Product Hunt Atom, **GitHub Trending daily** (`radar_github_trending.py`), TikTok merger (X + public tags + TikHub)
- Trends client via a Google Trends explore/live proxy (prefer UTC day cut; drop incomplete last hour; empty→0). Fallback to unofficial Trends libs only if proxy fails.
- Keyword-batch API client for the curated feed (batches list + batch detail)
- State: `pushed.json`, seen sets per radar, Trends cache

### Cost controls (important)
- `CACHE_TTL_H≈18`, `ROOTS_TTL_H≈24` so evening does not fully re-query morning
- Noon/evening TikTok scan: `--no-trends` (Trends once in morning)
- Daytime sitemap: `--no-score` (same as night)
- Do **not** put SERP volume APIs on the daily cron

### Env var **names** only (never pack values)
Owner supplies their own: Trends proxy key, TikHub (or equivalent), curated keyword API token if required, optional Product Hunt token, optional `GH_TOKEN`/`GITHUB_TOKEN` for GitHub API fallback. Scripts must read from env / `.env` and never echo secrets.

## Sitemap big sites (example set; owner may edit)
Template/trend product sites + gaming content sites commonly watched for new inner pages: makeviral, getstarrd, viberot, trendswap, kavel, kie, opentrend, pokemongohub, esportsdriven, keengamer (plus snowball expansions). New inner page for an unpushed term → broadcast with no heat gate.

## Services to connect (no secrets in template)
- Built-in or plugin **X** reads for recent meme posts (free public reads where available)
- Owner's Trends proxy / DataForSEO-style explore live
- Optional TikHub-class TikTok search API
- Optional Product Hunt GraphQL
- Curated SEO keyword batch API if used
- Optional GitHub token for Trending API fallback

When importing: ask the owner for which slots they want, which sources to enable, and where to put API keys — then create routines and a local `.env` without writing key values into memory or skills.
