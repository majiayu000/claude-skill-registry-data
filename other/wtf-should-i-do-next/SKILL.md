---
name: wtf-should-i-do-next
description: Cross-source growth diagnostic. Pulls Stripe, Supabase, Amplitude, GA4 and GSC into one AARRR funnel and returns a prioritized action list sorted by impact/effort. Use when asking "what should I work on next", "where is the bottleneck", "why is revenue flat", or for a periodic growth review.
---

# WTF Should I Do Next

Answers one question: **given everything the data says, what is the single highest-leverage thing to build next?**

Output is an AARRR funnel with real numbers plus a table of moves sorted by `impact / effort` descending.

When this skill activates: `WTF Mode: scanning all data sources...`

## Rule Zero: the funnel is a product, not a metric

Never report a single-source conclusion. Every claim needs a number from a named source and a date window. If two sources disagree, say so and dig — the disagreement is usually the finding.

---

## Step 1 — Credentials

All production secrets live in GCloud Secret Manager, **not** in local `.env.*` (local files hold test/placeholder values). See `.claude/skills/gcloud-secrets/SKILL.md`.

```bash
gcloud auth activate-service-account --key-file=./cloud/keys/myimageupscaler-auth-6348371fe8c6.json
gcloud config set project myimageupscaler-auth

SP=/tmp/wtf && mkdir -p $SP/creds
gcloud secrets versions access latest --secret=myimageupscaler-api-prod    > $SP/creds/api.env
gcloud secrets versions access latest --secret=myimageupscaler-client-prod > $SP/creds/client.env
```

Then `set -a && . $SP/creds/api.env; set +a` in each shell that needs them.

**Google (GA4/GSC) uses a different service account.** The key above will 403. Use:

```bash
export GCP_KEY_FILE=$HOME/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json
```

Read-only. Never write these files back to Secret Manager.

## Step 2 — Pull every source in parallel

| Source                     | Command                                                                                                                    | Gives you                                               |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Stripe**                 | REST via `$STRIPE_SECRET_KEY` (paginate `/v1/charges`, `/v1/subscriptions?status=all`)                                     | Net revenue by month, MRR, AOV, churn, refunds          |
| **Supabase**               | Supabase MCP `execute_sql` — Claude: `mcp__supabase__execute_sql`; Codex: `[mcp_servers.supabase]` in `.codex/config.toml` | Cohort conversion, activation, retention, credit ledger |
| **Amplitude**              | `/api/2/events/segmentation`, Basic `API_KEY:SECRET_KEY`                                                                   | Event funnel, error breakdown, paywall impressions      |
| **GA4**                    | `node .claude/skills/ga-analysis/scripts/ga-fetch.cjs --output=$SP/ga.json`                                                | Sessions, channel mix, engagement                       |
| **GSC**                    | `node .claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --output=$SP/gsc.json`                                             | Clicks, impressions, position, query opportunities      |
| **Cloudflare**             | GraphQL analytics — see below                                                                                              | Edge requests, uniques, threats, status codes, cache    |
| **Supabase logs/advisors** | `mcp__supabase__get_logs`, `mcp__supabase__get_advisors`                                                                   | API/Postgres errors, security + performance advisories  |
| **Replicate**              | `GET api.replicate.com/v1/predictions`, `$REPLICATE_API_TOKEN`                                                             | **COGS per upscale** — margin, not just revenue         |
| **Brevo**                  | `GET api.brevo.com/v3/smtp/statistics/*`, `$BREVO_API_KEY`                                                                 | Marketing email delivered/bounced/opened/clicked        |
| **git log**                | `git log --since --until --format="%h %ad %s"`                                                                             | **Correlate every inflection with a deploy**            |

Launch GA4 + GSC as background tasks; they take 2-4 minutes. Do the Stripe and Supabase work while they run.

Amplitude event names: `GET /api/2/events/list` for the live taxonomy. Canonical type is `server/analytics/types.ts`.

### Cloudflare edge analytics

Independent of GA4/Amplitude — it sees every request before any JS runs, so it distinguishes "traffic fell" from "our analytics broke."

```bash
curl -s https://api.cloudflare.com/client/v4/graphql \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  --data "{\"query\":\"{ viewer { zones(filter:{zoneTag:\\\"$CLOUDFLARE_ZONE_ID\\\"}) { httpRequests1dGroups(limit:30, filter:{date_geq:\\\"$FROM\\\", date_leq:\\\"$TO\\\"}, orderBy:[date_ASC]) { dimensions { date } sum { requests pageViews threats cachedRequests } uniq { uniques } } } } }\"}"
```

**Known gap (2026-07-25):** the prod `CLOUDFLARE_API_TOKEN` lacks `com.cloudflare.api.account.zone.analytics.read` and this returns an authz error. Ask the user to add that permission — do not silently skip the source. For 4xx/5xx breakdown swap `httpRequests1dGroups` for `httpRequestsAdaptiveGroups` with `dimensions { edgeResponseStatus }`.

Workers observability (errors, CPU limits) is separate: `npx wrangler tail --format=json`, or the `cloudflare-worker-debugger` agent.

### Unit economics — do not skip

A revenue number without COGS cannot tell you whether growth helps. Replicate is billed per prediction and `MODEL_CREDIT_COSTS` (`shared/config/credits.config.ts`) ranges 1-16 credits per job. Pull spend per model from Replicate, divide by credits consumed (`credit_transactions type='usage'`), and compare against realized revenue per credit sold. **A pack that sells credits below the cost of the models people spend them on loses more money the better it converts.**

## Step 3 — Two traps that have already produced wrong answers here

### Trap 1: `type='purchase'` is not a purchase

The `credit_transactions.type` column is unreliable. Rows describing `'Processing refund'` are stored with `type='purchase'`. In Feb 2026 this made 159 refunds look like purchases and produced a fake "5.2% → 0.9% conversion collapse" that a later diagnostic had to walk back.

**Always filter on description, not type:**

```sql
WHERE amount > 0 AND (description ILIKE 'Credit pack purchase%' OR type='subscription')
```

Genuine packs are 50 / 200 / 600 credits. If your average "purchase" is under 50 credits, you are counting refunds.

### Trap 2: unmatched cohort maturity

A February cohort has had six months to convert; this month's has had days. Comparing them raw always shows a decline. Restrict to cohorts older than the window and measure a **fixed window per cohort**:

```sql
WITH cohort AS (
  SELECT id, created_at, to_char(created_at,'YYYY-MM') AS m FROM profiles
  WHERE created_at < now() - interval '30 days'
), genuine AS (
  SELECT user_id, min(created_at) AS paid_at FROM credit_transactions
  WHERE amount > 0 AND (description ILIKE 'Credit pack purchase%' OR type='subscription')
  GROUP BY 1
)
SELECT c.m, count(*) AS signups,
  count(*) FILTER (WHERE g.paid_at <= c.created_at + interval '30 days') AS paid_30d,
  round(100.0*count(*) FILTER (WHERE g.paid_at <= c.created_at + interval '30 days')/count(*),3) AS conv_pct
FROM cohort c LEFT JOIN genuine g ON g.user_id=c.id GROUP BY 1 ORDER BY 1;
```

Related trap: `credit_transactions.amount < 0` includes `clawback`, so it overstates activation. Use `type='usage'` for real activation.

### Trap 3: monthly aggregates hide mid-month incidents

**Always plot the daily series before writing a single sentence about a trend.**

On 2026-07-25 this skill's first run reported "acquisition is working, signups +17% MoM." July's total was genuinely up — and it was concealing a 41% signup collapse that started July 18 and was still ongoing. The 28-day GSC and GA4 windows agreed with the monthly view, which made the error feel corroborated when it was the same mistake three times.

Aggregates over a window containing an incident are the average of "before" and "broken". Minimum daily series to pull every run:

```sql
SELECT created_at::date AS day, count(*) FROM profiles
WHERE created_at > now() - interval '45 days' GROUP BY 1 ORDER BY 1;
```

Then normalize against traffic — `ga.json` → `organic.dailyTrend`. **Signups per session is the metric that survives a traffic swing**; raw signup counts do not tell you whether you have a traffic problem or a conversion problem. Correlate any inflection against `git log --since` for that date.

### Trap 4: `account_created` is not the signup count

Amplitude `account_created` captured ~13% of real `profiles` rows before the July incident and ~4% after. Any signup metric, dashboard, or alert built on it is wrong. **`profiles` is ground truth for signups; `credit_transactions` is ground truth for usage and revenue.**

More generally: when an event count and a database count disagree, the database is right and the disagreement is itself a finding. Check whether instrumentation changed inside your comparison window (`git log` the analytics paths) before attributing an event-volume change to user behavior.

### Trap 5: never let a comparison window straddle an event

**Split the window at the event boundary and check whether the metric recovered before you claim a persistent effect.**

This one produced a fabricated P0. Signups dropped on 2026-07-18. I compared Jul 13-17 against Jul 18-24 and reported "a 25% conversion regression the rollback didn't fix." Five of the seven "post" days were the outage itself. The truth: it was a **one-day** SEV-1, fixed the same day, fully recovered on Jul 19 — three days _before_ the rollback I claimed had failed.

The check that settles it in one query, because it needs no instrumentation and no external tool:

```sql
WITH u AS (SELECT created_at::date d, count(DISTINCT user_id) active
           FROM credit_transactions WHERE type='usage' GROUP BY 1),
     s AS (SELECT created_at::date d, count(*) signups FROM profiles GROUP BY 1)
SELECT s.d, s.signups, u.active, round(u.active::numeric/NULLIF(s.signups,0),3) AS active_per_signup
FROM s LEFT JOIN u ON u.d=s.d WHERE s.d > now()::date - 30 ORDER BY 1;
```

**A ratio of two DB columns beats any cross-tool comparison.** GA4 sessions, Amplitude events and DB rows have different denominators, lags and failure modes; comparing across them invents effects. When volume falls but every internal ratio holds, the cause is upstream (traffic), not the funnel — that distinction is usually the whole answer.

## Step 4 — Build the AARRR frame

| Stage           | Primary metric                                    | Where it comes from                                                                  |
| --------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Acquisition** | sessions, clicks, impressions, signups            | GA4 `channelMix`, GSC `summary`, `profiles` by month                                 |
| **Activation**  | % of signups that produce _and download_ a result | `type='usage'` cohort + Amplitude `image_uploaded → image_upscaled → image_download` |
| **Retention**   | % with usage on 2+ distinct days; D7/D30          | `credit_transactions` distinct usage days                                            |
| **Revenue**     | maturity-matched cohort conversion, MRR, AOV      | Supabase cohort SQL + Stripe                                                         |
| **Referral**    | invites, viral coefficient                        | _(not implemented in this product)_                                                  |

Add these two — they catch what AARRR misses:

- **Friction**: `error_occurred` grouped by `errorType` _and_ `errorMessage`. Rejections of valid inputs are pure lost revenue.
- **Monetization surface**: does the paywall ever fire? Compare `insufficient_credits` errors against `free_limit_gate_shown`. If errors greatly exceed gate impressions, the paywall is being rendered as a failure instead of an offer — the single most common silent revenue leak here.

Sanity check the free tier against actual usage. If the median user consumes far fewer credits than the free grant, the paywall is structurally unreachable and no amount of checkout optimization will help.

## Step 5 — Score and sort

Score each candidate move:

- **Impact (1-10)** — projected effect on revenue or on the metric that gates revenue. Justify with a number from Step 2.
- **Effort (1-10)** — 1 ≈ under an hour, 5 ≈ a day, 10 ≈ multi-week.
- **Score = Impact / Effort**, sorted descending.

Rules:

- **An open incident outranks every optimization, whatever it scores.** Rank it first and say why.
- Bugs that reject paying-intent users outrank new features, always.
- A fix to a surface that never fires scores zero regardless of elegance — check the surface fires before optimizing it.
- **Before recommending a change, `git log` whether it was already tried.** This codebase rolled back a paywall gate on 2026-07-22 after it cost 60-80% of payments; the first run of this skill then recommended re-adding it. Search `docs/PRDs/done/` and `docs/PRDs/rollback-*` for the settled question before proposing it as new.
- If a recommendation depends on a surface you have not confirmed exists in live code, say so and make instrumenting it Phase 1 — do not quote a baseline you cannot reproduce.
- Prefer moves that are reversible and measurable within two weeks.
- State the verification metric and its current baseline for every row, so the follow-up review can tell whether it worked.

## Step 6 — Report

Structure: **TL;DR** (the one thing) → **Scoreboard** (numbers per stage, with deltas) → **AARRR walk-through** → **prioritized table** → **what I'd ignore and why**.

Be blunt about which finding is the bottleneck. A report that lists twelve equal-weight problems is a report that will not be acted on.

Write to `docs/reports/growth-diagnostic-YYYY-MM-DD.md`.

## Settled questions — do not propose these

- **Guest / anonymous upscaling.** Tried and rejected. The browser-based upscaler does not work, and the owner will not put a cost-bearing API (Replicate) behind a public unauthenticated route. Ignore the unwired scaffolding (`shared/config/guest-limits.config.ts`, `server/services/guest-processor.ts`, the `guest_upscale_completed` events) — it reads like an unfinished feature and is not one. Signup is the intended hard gate before first value.
- **Non-dismissible paywall gates.** Cost 60-80% of payments and 45% of signups in July 2026; rolled back in `1c95953c`.

## Known dead ends

- `scripts/seo/fetch-gsc-seo-equity-export.ts` is an intentional no-op stub.
- `backlink-analyzer/` is an empty directory; `AHREFS_ANALYTICS_KEY` is a tracking pixel, not an API key.
- `seo-serp-analysis.ts` uses hardcoded competitors — no real SERP API is wired.
- Baselime is write-only from this repo; no query script exists.
- `GA4_API_SECRET` is Measurement Protocol (ingestion), not a read credential.
- All `yarn *:prod` scripts fail unless `.env.api.prod` / `.env.client.prod` are materialized from Secret Manager first — the deploy script deletes them after every run.
