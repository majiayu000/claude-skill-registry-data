---
name: ahrefs
description: >-
  Pulls Ahrefs data for any domain and runs staged keyword research under a unit budget. Lookups: organic
  keywords, top pages, backlinks, referring domains, Domain Rating, traffic history, anchors, organic competitors,
  the SERP for a keyword, units left. Keyword research: expand seed topics, price keywords, pull top-10 SERPs,
  cluster the keywords one page can rank for, read which page type each SERP rewards, join your Google positions
  from Search Console, and suggest improve / new article / landing page / skip. Works through the Ahrefs MCP tools
  (any paid plan from Lite) or an API v3 key for scripts. Use when someone asks for a domain's SEO metrics, a
  competitor's organic traffic or backlinks, keyword volumes, or what to write about. Triggers: "check in Ahrefs",
  "organic traffic of X", "backlinks of X", "competitor SEO metrics", "keyword research", "keyword clustering",
  "what should we write about", "keywords for the German market", "content gap", "how much traffic does X get".
---

# Ahrefs

Two jobs: quick lookups for any domain, and staged keyword research. Every Ahrefs call spends API units from the
plan, so both keep a log of what was spent. Setup: `connections/ahrefs-mcp.md`, or run the `connect` skill.

Two ways in, and they are not interchangeable:

- **The Ahrefs MCP server** (default, any paid plan from Lite). Tools are named `mcp__ahrefs__*`. The agent calls
  them. Do not write scripts against the MCP endpoint: Ahrefs' terms do not permit custom scripts, bridges or
  standalone JSON-RPC clients there.
- **API v3** with `AHREFS_API_KEY` (an API v3 key; Ahrefs lists "direct access to API v3" from the Lite plan up,
  checked 2026-10-21; generate it under Account settings → API keys). Scripts use it: `https://api.ahrefs.com/v3/<path>`, `Authorization: Bearer <key>`. An MCP key on
  API v3, or an API key on MCP, returns 401.

The key is read from the environment first, then from `~/.config/marketing-agent-kit/.env` (or `MARKETING_KIT_ENV`).

## Mode 1: quick lookups (any domain)

Use the MCP tools. If they are not loaded, search for them (for example "ahrefs organic keywords"); if the server
is not connected, send the user to `connections/ahrefs-mcp.md`. Server rules:

- Call the `doc` tool before the first use of any tool.
- Every money value is in **USD cents**. Divide by 100.
- If a response carries `render_with` metadata, call that render tool with the data.
- Save what you will quote: write each response to `raw/seo/<name>.json` next to the analysis.

With an API v3 key, the same calls work from the script (repeatable, saved, units logged):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ahrefs_api.py site-explorer-organic-keywords target=example.com date=2026-09-30 \
    select=keyword,sum_traffic,best_position limit=100 order_by=sum_traffic:desc --out raw/seo/kw.json
python3 ${CLAUDE_SKILL_DIR}/scripts/ahrefs_api.py subscription-info-limits-and-usage      # units left (free)
python3 ${CLAUDE_SKILL_DIR}/scripts/ahrefs_api.py endpoints site-explorer                 # list endpoints (no key, no units)
python3 ${CLAUDE_SKILL_DIR}/scripts/ahrefs_api.py params site-explorer/top-pages          # one endpoint's parameters
```

The script takes an API path or an MCP tool name. A tool name becomes `<group>/<rest>`
(`site-explorer-top-pages` → `site-explorer/top-pages`) with a few exceptions it knows: `serp-overview` →
`serp-overview/serp-overview`, `batch-analysis` → `batch-analysis/batch-analysis`, `site-explorer-referring-domains`
→ `site-explorer/refdomains`, `site-explorer-linked-domains` → `site-explorer/linkeddomains`. `doc`, `render-*` and
the `*-entities` tools exist only in MCP. Each call prints its units (response header
`x-api-units-cost-total-actual`) and appends them to `~/.local/share/marketing-agent-kit/seo/ahrefs_units.jsonl`
(override with `AHREFS_UNITS_LOG`).

| Task | Tool |
|---|---|
| DR and summary metrics | `site-explorer-domain-rating`, `site-explorer-metrics` |
| Organic keywords (top by traffic) | `site-explorer-organic-keywords` (order by traffic, `limit<=150`) |
| Top organic pages | `site-explorer-top-pages` |
| Referring domains / backlink summary | `site-explorer-referring-domains`, `site-explorer-backlinks-stats` |
| Anchors | `site-explorer-anchors` |
| Traffic / keyword history | `site-explorer-metrics-history`, `site-explorer-keywords-history` |
| Organic competitors | `site-explorer-organic-competitors` |
| Organic by country | `site-explorer-metrics-by-country` |
| SERP for a keyword | `serp-overview` |
| Keyword ideas | `keywords-explorer-matching-terms`, `keywords-explorer-related-terms` |
| Keyword volume and difficulty | `keywords-explorer-overview` |
| AI citations of a brand | `brand-radar-*` |
| Units left | `subscription-info-limits-and-usage` (free) |

Rules: `limit<=150` by default. Never pull raw backlinks by the thousand: `site-explorer-all-backlinks` is the most
expensive tool; start with stats and referring domains. Check units left before a long series of calls. Numbers in a
report must be checkable against the saved raw files. **Do not use Ahrefs paid-traffic or ad-budget estimates** in
reports: they are systematically wrong. Saying that a domain has paid keywords is fine; dollar figures are not. Ad
libraries do not disclose budgets either.

## Mode 2: keyword research (staged)

`scripts/kw.py STAGE --project <name> [--country xx]`, one project per topic and market. It reads the site config
`~/.config/marketing-agent-kit/seo/<site>.toml` (`[keywords]`: default country, markets, optional monthly unit cap;
`[site] hosts` to find your own pages in SERPs; format in `../gsc-insights/references/config.md`). For the GSC join,
run gsc-insights' `gsc_pull.py` first. Project files live in `<data>/keywords/<project>/`.

| Stage | What it does | Cost (units) |
|---|---|---|
| `discover --seeds "a,b" [--related] [--from-gsc]` | Candidates: matching (and related) terms, strings only; your GSC queries containing a seed in that market (free) | ~1 per row, 50 minimum per call |
| `price [--max N] [--fields …] [--min-volume 10]` | Volume, difficulty, parent topic, intents; seeds and GSC queries first; batches of 20 (API) or 5 (MCP); via API a failing batch is split to drop the keyword Ahrefs cannot price | ~32 per keyword with data; no-data keywords are free |
| `serp [--top 60]` | Top-10 SERP for the biggest keywords | ~50–60 each, cached 14 days |
| `cluster [--min-shared 3]` | Keywords sharing ≥ N top-10 URLs form one cluster (one page targets them), per market | free |
| `prioritize [--sheet]` | Joins your GSC position and page for the market, scores clusters, suggests an action; report.md, clusters.csv, optional sheet tab | free |
| `budget` | Units this month by tool (keyword research + script lookups) and, with an API key, the account limits | free |

Use `--dry-run` on `price` and `serp` first. Answers are cached in `<data>/ahrefs_cache.sqlite` (30 days, SERPs 14);
units go to `<data>/ahrefs_units.jsonl`. The monthly cap (`[keywords] monthly_unit_cap`, 0 = log only) is checked
before each call, across parallel runs.

### Transport A: API v3 (`--via api`)

With `AHREFS_API_KEY` set, `discover`, `price` and `serp` call API v3 themselves. Units come from the
`x-api-units-cost-total-actual` response header; a call without that header is logged with `units_unreported`. A 429
(60 requests per minute by default) is retried once after `Retry-After`.

### Transport B: the MCP tools (`--via mcp`, the default without an API key)

Most plans have MCP access and no API v3 key. Then the stages do the bookkeeping and you make the calls:

1. Run the stage, e.g. `kw.py price --project de-dubbing --country de`. It applies every answer already in the cache,
   writes the calls still needed to `<project>/mcp_plan.json` and prints them with ids (`price-001` …).
2. For each planned call, one at a time (parallel calls fail): call the MCP tool (`mcp__ahrefs__<tool>`) with exactly
   the planned arguments and save its output to a file. Keep both text blocks if there are two: the second one,
   `apiUsageCosts`, holds the real unit cost. If Claude Code already saved a long output to a file, use that file.
3. `kw.py import --project de-dubbing --call price-001 <file>`. Import checks the rows, caches them under the same key
   the API path uses, updates the project files and logs the units (from `apiUsageCosts`, or the documented estimate
   marked `units_estimated` when the file has none). Importing the same file twice does nothing.
4. Re-run the stage: with every answer cached it plans nothing and you go on to the next stage.

For a call that is not in the plan, pass `--tool keywords-explorer-overview --args '<the JSON arguments you sent>'`
instead of `--call`, or save a wrapper `{"tool": …, "arguments": {…}, "result": <output>}`. If a pricing call fails
with an internal server error, one keyword in the batch is one Ahrefs has never indexed: re-run `price --batch 1`
for the rest and skip the keyword that fails alone. `cluster`, `prioritize` and `budget` are the same for both
transports. `budget` without an API key shows the logged units; ask the free MCP tool
`subscription-info-limits-and-usage` for the account's limits.

### Workflow and decision rules

Agree topic, market and language; **research each language natively** (seeds in the market's language;
`--from-gsc` shows how people there phrase it); discover → read candidates → price (dry run first) → serp for the top
30–60 → cluster → prioritize; check the SERPs of the top clusters yourself before recommending.

- **SERP page type decides the format**: articles → an article can rank; landing/product pages → a landing page;
  app stores or vendor homepages → usually skip.
- **Existing page first**: if you rank 4–20 for the cluster in GSC, improve that page.
- **One cluster, one page.** Do not split keywords that share a SERP.
- **AI Overview present** → fewer clicks at the same position; commercial queries get AIOs too.
- **Metrics are estimates**; KD is often missing for small non-English keywords. Calibrate with GSC impressions.
- score = volume × (1 − KD/100) × (1.0 commercial, 0.5 informational) ranks clusters; it does not forecast traffic.
- Never present a keyword list as research without the SERP check.

## Unit costs

Read `references/unit-costs.md` before pricing more than a few dozen keywords. The short version: cost per call =
max(50, per-row cost × rows); volume-type fields (`volume`, `global_volume`, `difficulty`, `traffic_potential`,
`parent_volume`, `intents`) cost about 10 units per row each, `keyword` about 1. Discover with `select=keyword` first,
then price only the shortlist; put the volume floor into `where` (only kept rows are billed); send pricing calls
sequentially.

## Adapt it

- Put your own domains, hosts and markets into the site config (`[site] hosts`, `[keywords] default_country`,
  `markets`) so SERPs mark your pages and `--from-gsc` uses your queries.
- Set `[keywords] monthly_unit_cap` to the share of the plan's units that keyword research may spend, and put a cap
  on the Ahrefs key itself (Account settings → API keys).
- Keep a `domains.json` with your domain and your usual competitors, so "compare us with the usual three" needs no
  lookups.
- Change the action rules in `kw.py` (`action()`) and the score weights if your business values informational
  content differently.
- If you run the same SEO snapshot every month, turn the lookups into a fixed `ahrefs_api.py` script (API v3) and
  keep the agent for interpreting the changes.
