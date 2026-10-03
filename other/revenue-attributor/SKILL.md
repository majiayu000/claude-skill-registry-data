---
name: revenue-attributor
description: "Revenue attribution specialist that connects Meta Ads, Google Ads, and Stripe revenue to show which campaigns actually pay back. Generates campaign-level ROAS breakdowns with waste detection and budget reallocation recommendations. Use when analyzing ad ROI, finding wasted ad spend, comparing channel performance, or reallocating budget. Triggers: attribution, ROAS, ad spend, campaign performance, channel mix, budget reallocation, ad waste."
metadata:
  version: 1.0.0
  author: Humblytics
---

# Revenue Attributor

## Purpose

Connect ad spend to on-site conversion signals using Humblytics attribution, and rank campaigns by spend efficiency (sessions and `ad_conversions` per dollar). True revenue/ROAS, `revenue_conversions`, and `trial_count` are only populated when a Stripe/ChartMogul revenue connector is attached to the property — without one, those fields are `0`. For true ROAS, join Humblytics spend + on-site conversion data to Stripe/ChartMogul revenue separately. This skill moves marketing teams from raw click counts to spend efficiency, and to revenue accountability once a revenue connector is in place.

## When to Use

- Planning next month's ad budget and need data to reallocate
- Diagnosing why spend is up but revenue is flat
- Comparing paid vs organic vs direct revenue contribution
- Auditing campaign-level ROAS across Meta, Google, TikTok, LinkedIn
- Building a quarterly ad performance review for leadership
- Deciding whether to kill, scale, or hold a specific campaign

## Connecting Humblytics

Live data comes from the **Humblytics MCP** (server `humblytics`). This skill calls `mcp__humblytics__*` tools — `get_ads_attribution`, `list_meta_connections`, `get_meta_daily_insights`, `list_google_ads_connections`, and friends — so there are no base URLs, curl calls, or API keys to wire up here. Connect the MCP once (see the repo README); the API key lives in the connection headers, set a single time.

- **Never paste API keys into chat** — they persist in transcripts and logs. The key belongs in the MCP connection config, never in `CLAUDE.md`, `.cursorrules`, or any file committed to git.
- **Property**: for a single-property key the MCP auto-resolves the property, so nothing to pass. For a multi-property key, call `list_properties` and pass the chosen `propertyId`.
- **Stripe/ChartMogul requirement**: the Humblytics property must have a Stripe/ChartMogul revenue connector attached for revenue attribution to populate. No separate Stripe key is needed here — Humblytics handles ingestion internally. Without a revenue connector, `revenue`, `roas`, `revenue_conversions`, and `trial_count` come back `0`.

### Three paths to ad data (Meta Ads + Google Ads)

#### Path A — Humblytics connectors (preferred, read-only)

If the property has Meta Ads or Google Ads connected at **Connectors** in the Humblytics dashboard, this skill pulls campaign metadata, daily insights, and full-funnel attribution directly through the Humblytics MCP — no Meta App Review, no Google Ads developer token. This is the default path. The connectors are **read-only** — they let the agent see campaign data and revenue, but not pause campaigns or change budgets.

- Detect availability via `list_meta_connections` and `list_google_ads_connections`. Empty `connections` arrays mean nothing is connected; fall back to Path A2 below.

#### Path A2 — User-provided CSV (fallback)

If no connectors are set up, the skill asks the user to paste ad spend from Meta Ads Manager or Google Ads Editor. Pair the CSV columns with Humblytics-attributed revenue from `get_ads_attribution` (which still works for revenue even without a spend connector — it just leaves spend fields zero).

#### Path B — Meta CLI (only when the agent needs to *manage* campaigns)

For pausing laggards, shifting budget, or other write actions, point the user at Meta's official `meta ads` CLI (released April 29, 2026). It's a published, supported tool that creates resources in `PAUSED` status by default. Scope the access token to a single ad account, store it in `.env` (never `CLAUDE.md`), and review every campaign before flipping it active. This skill does not call the Meta CLI itself — it just hands off when management actions are required.

#### Path C — Don't roll your own Meta app

**Do not give the agent direct Meta Marketing API access through a system user on an unapproved developer app.** Routing production API traffic through a draft or unpublished Meta App — regardless of how the access token was issued — is how ad accounts, including long-standing ones with seven-figure spend, are getting permanently banned. Meta is actively enforcing against unapproved-app API traffic. Use Path A or Path B instead. The only safe DIY route is a Meta Developer App with the Marketing API product and **full App Review completed** for the permissions you need (e.g. `ads_read`) — budget weeks for review.

## Before You Start

1. **Confirm a revenue connector is attached** — Attribution requires Stripe/ChartMogul revenue events; without one, you only get click data
2. **Confirm UTM hygiene** — Campaigns without UTM parameters can't be attributed to source
3. **Time range** — Default to last 30 days; 60-90 days for monthly comparison; 12 months for strategic planning
4. **Attribution model** — Default to last-touch; switch to first-touch or linear if specified
5. **Property** — The MCP auto-resolves the property for a single-property key; for a multi-property key, call `list_properties` and pass the chosen `propertyId`

## Core Workflow

### Step 1: Pull Revenue + Spend Data

**Primary call** — full-funnel attribution merging ad spend with sessions and revenue:

- `get_ads_attribution` with `startDate` and `endDate` (both `YYYY-MM-DD`)

This returns per-campaign rows with `campaign`, `utm_campaign`, `platforms`, `target_urls`, `top_landing_page`, `spend`, `impressions`, `clicks`, `sessions`, `ad_conversions`, `revenue_conversions`, `revenue`, `roas`, `trial_count`, `true_cpa`, `cost_per_trial`, `click_to_session_rate`, `avg_hours_to_convert`, plus top-level `totals`, `unmatched_ad_campaigns` (UTM hygiene gaps), `unmatched_utm_campaigns` (organic/email traffic), `breakdowns`, `date_range`, and `connections`. NOTE revenue and roas are 0/null on properties without a revenue connector. Empty `campaigns[]` with non-empty `unmatched_*` is the strongest signal that UTM tagging needs work — the data is flowing, it just isn't joining.

**Spend supplement (Path A — connectors connected):**

- Meta: `list_meta_connections` → pick a connection → `get_meta_daily_insights` with that connection `id`, its `accountId`, and `since`/`until` (`YYYY-MM-DD`)
- Google: `list_google_ads_connections` → pick a connection → `list_google_ads_campaigns` with that connection `id` and `customerId`

**Path A2 fallback (no connectors):** ask the user to paste a CSV from Ads Manager. The skill joins those rows to the `get_ads_attribution` revenue side.

**Context tools** for source/page-level breakdowns:

- `get_traffic_breakdown` — UTM source/medium/campaign + device + location dimensions
- `get_forms_breakdown` — Conversion events (signups, purchases)
- `get_pages_breakdown` — Page performance (there's no `page_group` filter; pull all pages and filter client-side if needed)

### Step 2: Build the Attribution Table

For each source → campaign → ad level:

| Source | Campaign | Spend | Clicks | Signups | Revenue | ROAS |
|--------|----------|-------|--------|---------|---------|------|
| google/cpc | brand-search | $1,200 | 340 | 28 | $4,200 | 3.5× |
| meta/paid | lookalike-v3 | $2,800 | 1,240 | 42 | $1,680 | 0.6× |
| organic | seo-longtail | $0 | 860 | 31 | $3,720 | ∞ |

### Step 3: ROAS Ranking + Waste Detection

**Precondition — only tier by ROAS when `totals.revenue != 0`.** If `revenue` is `0` across all campaigns (no Stripe/ChartMogul revenue connector attached), do NOT tier or recommend kills by ROAS. Instead, report `spend` plus on-site conversion signals (`sessions`, `ad_conversions`) and explicitly flag that revenue attribution is unavailable until a revenue connector is connected. Only apply the tier table below once `totals.revenue != 0`.

Sort campaigns into four tiers:

| Tier | ROAS | Action |
|------|------|--------|
| **Scale** | > 3× | Increase budget 20-50% |
| **Hold** | 1.5-3× | Optimize creative/audience; budget stays |
| **Fix** | 0.5-1.5× | Audit targeting, creative, landing page before killing |
| **Kill** | < 0.5× | Reallocate budget immediately |

**Waste detection rules:**
- Campaign has > $500 spend and < 1× ROAS → hard flag
- Ad set has > 100 clicks and 0 conversions → landing page or audience mismatch
- Campaign clicks but no UTMs → invisible to attribution, fix tracking first

### Step 4: Channel Mix Analysis

Compare revenue contribution across channels:

- **Paid share**: % of revenue from paid ads
- **Organic share**: % from SEO/direct
- **Referral share**: % from partner/affiliate sources
- **Blended CAC**: Total ad spend / total acquired customers

**Red flags:**
- Paid share > 80% → business is dependent on ad spend; diversify
- Paid share < 10% with high spend → attribution is broken, fix UTMs
- One campaign > 50% of revenue → concentration risk

### Step 5: Reallocation Recommendation

Build a specific reallocation plan:

```
CURRENT ALLOCATION (monthly):
- Google Ads: $8,000 (2.1× ROAS)
- Meta Ads:   $12,000 (0.9× ROAS)
- LinkedIn:   $3,000 (4.2× ROAS)

RECOMMENDED REALLOCATION:
- Google Ads: $9,000 (+$1,000) — scale branded search
- Meta Ads:   $6,000 (-$6,000) — kill "lookalike-v3", keep retargeting only
- LinkedIn:   $7,000 (+$4,000) — scale the 4.2× ROAS campaign
- Reserve:    $4,000 — test new channel (TikTok or YouTube)

NET CHANGE: $0 (same total budget)
EXPECTED ROAS LIFT: 1.6× → 2.4× (projected)
```

### Step 6: Output Format

```
PERIOD: [start] to [end]
TOTAL AD SPEND: $X
TOTAL ATTRIBUTED REVENUE: $Y
BLENDED ROAS: Z×

TOP 3 PERFORMERS:
1. [Campaign] — [ROAS]× — [Recommendation]
2. [Campaign] — [ROAS]× — [Recommendation]
3. [Campaign] — [ROAS]× — [Recommendation]

BOTTOM 3 (KILL CANDIDATES):
1. [Campaign] — [ROAS]× — $[spend] wasted
2. [Campaign] — [ROAS]× — $[spend] wasted
3. [Campaign] — [ROAS]× — $[spend] wasted

CHANNEL MIX:
- Paid: X%   Organic: Y%   Direct: Z%   Referral: W%

REALLOCATION PLAN:
[Specific budget moves with dollar amounts]

PROJECTED IMPACT:
[Expected ROAS lift and revenue gain]

TRACKING GAPS:
[Campaigns missing UTMs, ad sets with zero attribution, Stripe integration issues]
```

## Attribution Principles

1. **Revenue over clicks.** A campaign with 10× the clicks of another means nothing if it doesn't drive revenue.
2. **Absolute wins matter, not just ROAS.** A 10× ROAS campaign at $200/mo spend matters less than a 2× ROAS campaign at $20K/mo.
3. **Kill slowly, scale cautiously.** A low ROAS campaign might be the top-funnel driver. Check assisted conversions before killing.
4. **UTM hygiene is everything.** Without clean UTMs, attribution is fiction. Fix tracking before fixing spend.
5. **Blended CAC is the truth.** Per-campaign ROAS is useful, but blended CAC tells you whether the business model works.

## Creative Inspection (Path A only)

When `get_ads_attribution` flags a high-spend Meta campaign, drill into the underlying creative before recommending action. `get_ads_attribution` does NOT return Meta's internal campaign IDs, so you must first resolve the connection and campaign IDs from `list_meta_connections` — the ads call requires a real Meta `campaignId`, not the `utm_campaign` string (an unknown/fake id returns a Graph API "object does not exist" error). Verified live flow (2026-05-29):

1. `list_meta_connections` → take the connection `id` (and `adAccounts[].id`).
2. `list_meta_campaigns` (with the connection `id`) → list campaigns per account with their real Meta `id`, `name`, `status`. (Equivalently `list_meta_account_campaigns` with the connection `id` and `accountId`.) Match the flagged `utm_campaign`/name to its Meta campaign `id`.
3. `list_meta_campaign_ads` (with the connection `id` and `campaignId`) — list ads in that campaign with creative (`thumbnailUrl`, `imageUrl`, title, body), `status`, `adsetId`, destination URL.
4. `get_meta_ad_creative` (with the connection `id` and `adId`) — full creative metadata (name, title, body, etc.) for one ad.

Also available when you need connection health or a single account's campaigns over a window: `get_meta_connection_status` (connection `id`) for status, and `list_meta_account_campaigns` (connection `id`, `accountId`, `since`, `until`) for the per-account campaign list.

Look for: destination URL mismatch (ad copy promises X, lands on Y), broken links, low-quality stock visuals, or one ad in the campaign hogging the spend with poor performance. This is the read-only diagnostic step. To pause the ad, hand off to Meta CLI (Path B).

## Related Skills

- `funnel-reporter` — End-to-end funnel metrics for the periods you're analyzing
- `ad-expert` — Creative and targeting fixes once you've identified waste
- `cro-optimizer` — If ads are working but landing pages aren't converting, pair with CRO
