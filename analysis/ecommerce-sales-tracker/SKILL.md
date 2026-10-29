---
name: ecommerce-sales-tracker
description: Use when someone asks to track e-commerce sales performance, set up a sales KPI dashboard, analyze sales trends, detect sales anomalies, or run cohort analysis for Amazon, Shopify, WooCommerce, Walmart, TikTok Shop, Etsy, eBay, BigCommerce, or other platforms. Works only from sales data the user supplies — never connects to live accounts, never invents missing figures.
argument-hint: "[sales data or scope]"
allowed-tools: AskUserQuestion, Read, Write, Glob, Grep, Artifact, Skill
---

# E-commerce Sales Tracker

Turn user-supplied sales data into a KPI dashboard, trend analysis, anomaly flags, and cohort insights, with a visual sales-performance dashboard as the core deliverable alongside the written analysis — not just KPI advice.

**Read-only / advisory.** This skill never connects to a live platform account, API, or reporting tool, and never invents or estimates a figure the user didn't supply. Every number in the output traces back to data the user typed, pasted, or uploaded in the conversation.

For a sales drop that might have a traditional SEO cause (rankings, crawlability, on-page issues), use `ecommerce-seo-auditor`. For sales issues tied to AI-shopping/AI-search visibility (whether AI assistants understand, cite, or recommend the product), use `ecommerce-geo-auditor`. For overall channel/budget strategy once trends and anomalies are understood, use `ecommerce-marketing-strategy-builder` — optional, not a dependency.

## Usage examples

```text
Help me set up sales tracking for my business. I sell on Amazon ($30K/mo) and Shopify ($10K/mo). What KPIs should I track and how often?
Here's my last 8 weeks of daily Shopify revenue [pasted table] — build a dashboard and flag anything unusual.
I have a CSV export of customer orders with first-purchase and repeat-purchase dates — run a cohort analysis.
```

## Inputs and collection

Collect, for each data set supplied: platform, market, date range, currency, the metric(s) and their definitions, and any known reporting limitations (e.g. refunds excluded, timezone, partial period) — but only ask what isn't already obvious from what the user typed or attached (see In-workflow questions below).

- Accept sales data typed directly in chat, pasted as a table/CSV, or uploaded as a file/export. Read any supplied file directly; where the user points to a folder or export bundle rather than a single file, search it to find the relevant file(s) first.
- Never fetch or connect to a live platform account, dashboard, or API under any circumstance — this skill works only from data the user has actually provided in this conversation.
- If the supplied data is short of what a requested analysis needs (see the minimum-data requirements under Anomaly detection and Cohort analysis below), don't attempt that analysis — explain the framework instead and state exactly what additional data would make it possible.
- Never estimate, extrapolate, or invent a missing figure. Mark it **Not provided** and either ask the user for it or exclude it from calculations, whichever they prefer.
- **If no sales data is supplied at all, ask before proceeding** — one clickable question, recommended option first, free-text override open: "Typed figures (Recommended)" / "CSV or spreadsheet file" / "Screenshot" / "Other". Once picked, ask directly (free text) for the actual figures, date range, and metric definitions matching that format — don't force a further clickable step once real data starts arriving.
  - If the chosen format is a file (CSV/spreadsheet/screenshot), follow with one more clickable question for how to access it: "Paste it directly in chat (Recommended)" / "Provide a file path or location for me to read" — free-text override open.
  - Skip this intake question entirely once the user has already pasted or uploaded usable data — never re-ask what's already been supplied. Never guess or invent a placeholder business.
- Continue with a partial dashboard/analysis whenever some usable data exists. Classify every finding as **Calculated** (computed from supplied data), **Data-dependent** (framework explained, but supplied data doesn't meet the minimum to actually run it), or **Not provided**.

## In-workflow questions

This skill defaults to asking about **any** decision point that has a real, finite set of good answers — not just a short fixed list. Scan the request for every genuine open decision. The only hard limit is: **skip anything already evident** from the supplied data or the conversation — never ask what you can already tell, and never pad the interview with questions that have an obvious or inconsequential answer.

Common decision points (not exhaustive):

- **Platform(s)** — if the business sells on more than one platform and it's unclear whether the user wants one combined cross-platform dashboard or separate per-platform sections.
- **Business stage** — if KPI target-setting is wanted and stage (e.g. early-stage / growth / mature) isn't stated, since target benchmarks scale by stage (see KPI framework below).
- **Analysis depth** — if it's unclear whether the user wants a quick top-KPI snapshot or the full dashboard (KPIs + trends + anomaly detection + cohort analysis).
- **Which analyses to run** — if the supplied data would support anomaly detection and/or cohort analysis but the user's request didn't ask for them explicitly, ask whether to include them or stick to KPIs/trends only.
- **Currency/period normalization** — if multiple supplied data sets use different currencies, timezones, or period lengths, ask how to normalize or combine them (e.g. convert to one currency at a stated rate, or keep separate).
- **Multiple plausible scopes** — if the request could mean the whole business, one platform, or one product/SKU line, ask which.
- **Partial-data tradeoff** — if only partial data is available and more could plausibly be supplied, ask whether to proceed now with a partial dashboard (labeling gaps "Not provided") or wait for more.

Ask one question at a time, using a clickable-question tool where available: state the question, offer the recommended option first labeled "(Recommended)" plus 2-3 genuinely distinct alternatives, and always keep a free-text override open. Where no clickable-question tool is available, ask the identical question as plain numbered text with the same "(Recommended)" marking and free-text override. See Platform adapters below for which mechanism applies where.

Before starting the Workflow below, if any of these were asked and answered, post a one-line **scope recap** (e.g. "Tracking Amazon + Shopify combined, growth-stage targets, full dashboard with anomaly detection — sound right?") as a final clickable confirm/adjust question — recommended option "Yes, proceed" — rather than launching straight into the analysis unconfirmed. Skip this recap entirely if nothing needed asking (everything was already evident).

## Workflow

Resolve all applicable In-workflow questions (including the scope recap) before starting this list.

1. Record the exact scope: business, platform(s), date range(s), currency, the data actually supplied, and the reference date used for period comparisons.
2. Check each requested analysis against its minimum-data requirement (KPI snapshot works from any real supplied numbers; trend analysis needs 2+ comparable periods; anomaly detection and cohort analysis have their own thresholds below). Mark anything short of the minimum **Data-dependent** rather than attempting it.
3. Define the KPI set from the KPI framework below, scaled to the stated (or asked) business stage.
4. Compute trend analysis (period-over-period, and YoY where enough history exists) strictly from supplied numbers.
5. Run anomaly detection if the minimum data is met (see Anomaly detection); otherwise explain the framework and the data that would be needed.
6. Run cohort analysis if the minimum data is met (see Cohort analysis); otherwise explain the framework and the data that would be needed.
7. Build the dashboard: generate an interactive dashboard artifact where the environment supports it, otherwise render the same content as structured tables and explicit chart specifications in chat (see Platform adapters below). Either way, the dashboard must cover the same KPIs, trends, and any calculated anomaly/cohort findings — no tool dependency is required by the workflow itself.
8. Turn calculated findings into prioritized action items using the priority scale below; mark any figure derived from incomplete data with ⚠️.
9. Post the full report (and, in Claude Code, the dashboard artifact) in chat, then save the report per Output format below where that's possible.

## KPI framework

Scale the recommended KPI set to business stage — ask if not stated and target-setting was requested (see In-workflow questions):

| Stage | Primary focus | Core KPIs |
|---|---|---|
| Early-stage (pre-$10K/mo or new platform) | Validate demand, find repeatable channels | Revenue, orders, conversion rate, traffic (if supplied), AOV |
| Growth ($10K–$100K/mo) | Scale efficiently, protect margin | Revenue, AOV, conversion rate, CAC (if cost data supplied), repeat-purchase rate, refund/return rate |
| Mature ($100K/mo+) | Optimize mix, defend against erosion | All growth-stage KPIs plus SKU-level contribution margin, cohort LTV, channel mix, YoY trend by segment |

Trend cadence: report daily for operational monitoring, weekly for trend confirmation, monthly/YoY for strategic review — use whichever cadences the supplied data's granularity actually supports; never fabricate a finer cadence than the data allows.

## Anomaly detection

**Minimum data required:** a dated time series of one consistent metric, in one currency/unit, with enough prior periods to establish a baseline (recommend at least 5-7 comparable prior periods; state the actual baseline length used).

**Method:** compare each period's value to a trailing baseline (e.g. trailing-period average or median) and flag a period as a candidate anomaly only when it deviates beyond a stated threshold (e.g. a stated percentage or standard-deviation band) — always state the exact method, baseline window, period, and threshold next to the finding.

Before labeling anything a confirmed anomaly, rule out and explicitly note if it's more likely:
- normal seasonality (e.g. known sales events, weekday/weekend pattern) apparent in the data itself,
- a partial or incomplete period in the export (e.g. current period cut off mid-day/mid-week),
- a tracking or reporting gap (e.g. a missing day, platform outage) rather than a real sales change.

Label every anomaly finding **data-dependent** and never present a candidate anomaly as a confirmed root cause — pair it with a suggested validation step (e.g. cross-check against a marketing calendar, platform status page, or the raw export).

## Cohort analysis

**Minimum data required:** a customer identifier or cohort label, each customer's/cohort's first-order (or cohort-start) date, and later purchase/activity dates or values for the same identifiers.

**Method:** group customers/orders into cohorts by their first-order period (e.g. month acquired), then compute retention or repeat-purchase rate for each cohort across subsequent periods. State the cohort definition, period grain, and how many cohorts/customers the data actually covers.

Label every cohort finding **data-dependent**, and never generalize a single cohort's pattern as representative of the whole customer base without saying how many cohorts/customers back it.

## Domain rules

- Never invent, estimate, or extrapolate a number the user didn't supply — an unavailable figure is always **Not provided**, never a guess.
- Distinguish **Calculated**, **Data-dependent**, and **Not provided** on every finding in the output; missing data never gets silently treated as zero or as evidence of a negative trend.
- Normal seasonality, a partial export, or a tracking gap is never presented as a confirmed anomaly (see Anomaly detection).
- One period, one cohort, or one platform's data is never proof of an overall, business-wide pattern.
- Currency, timezone, or period-length mismatches across supplied data sets must be normalized (with the method stated) or explicitly kept separate — never silently combined.
- Never forecast future revenue or sales without a transparent, stated model built on the user's own historical data.
- If the user reports what they saw on a live platform dashboard themselves (typed or pasted), treat that as user-supplied data like any other export — the skill still never fetches it directly.

Use this scale for prioritized action items:

| Priority | Meaning |
|---|---|
| Now | Calculated finding materially affects revenue or signals an active problem (e.g. confirmed conversion drop, confirmed anomaly with ruled-out alternate causes) |
| Next | Calculated finding meaningfully improves a KPI or process (e.g. AOV opportunity, cohort retention gap) |
| Then | Data-dependent opportunity — worth pursuing once the needed data is available |
| Watch | Low-severity or data-dependent item worth monitoring, no immediate action needed |

## Output format

Post this in chat:

```markdown
# E-commerce Sales Tracking Report — [business or scope]

## Scope and data
- Platform(s): [context] | Market: [context] | Currency: [context]
- Date range(s) and granularity: [context]
- Data supplied: [what was typed/pasted/uploaded, and how]
- Not provided: [figures/areas the analysis couldn't cover]

## Executive summary
- [most important calculated conclusion]
- [highest-priority next action]

## KPI snapshot
| KPI | Value | Period | Status (Calculated/Data-dependent/Not provided) | Target (if business stage given) |
|---|---|---|---|---|

## Trend analysis
[period-over-period and YoY findings, cadence limited to what the data supports]

## Anomaly findings
[data-dependent findings per Anomaly detection, or: "Not run — minimum data not met; needs: ..."]

## Cohort findings
[data-dependent findings per Cohort analysis, or: "Not run — minimum data not met; needs: ..."]

## Dashboard
[interactive artifact link/embed in Claude Code, or the same dashboard as tables + chart specs elsewhere — see Platform adapters]

## Prioritized action items
1. Now: [action]
2. Next: [action]
3. Then: [action]
4. Watch: [item]

## Related audits
- Sales tied to a traffic/ranking drop → run `ecommerce-seo-auditor`.
- Sales tied to AI-shopping/AI-search visibility → run `ecommerce-geo-auditor`.
- Overall channel/budget strategy once trends and anomalies are understood → run `ecommerce-marketing-strategy-builder` (optional, not a dependency).
```

The complete report posted in chat is the required output on every platform. Only where persistent file writing is actually available, ask the user via a clickable `AskUserQuestion` ("Save this report to `output/ecommerce-sales-tracker/`?" / "Save it (Recommended)" vs "Just the chat copy") before writing anything — never save without that confirmation, and ask it fresh for every report rather than assuming a standing yes from an earlier one. If confirmed, save the same markdown to `output/ecommerce-sales-tracker/<business-or-scope-slug>-<YYYY-MM-DD>-report.md`, using a safe, readable slug and the report date; if a prior report file exists for that slug, create a new dated file rather than overwriting it, so sequential reports stay comparable. Where file writing isn't available, or the user declines, don't claim a file was saved — say the complete copyable report is the one above.

## Platform adapters

**Claude Code adapter:** Read local files/exports the user points to; use Glob/Grep to locate the relevant files first when pointed at a folder or export bundle rather than a single file. Use AskUserQuestion for every in-workflow clarifying question (see In-workflow questions above) and for the save-confirmation in Output format above. Build the dashboard as a published Artifact: load the `dataviz` skill before choosing chart types/colors, and the `artifact-design` skill before publishing, per those skills' own trigger rules — then use the Artifact tool to publish it. Once confirmed, save the completed report to `output/ecommerce-sales-tracker/<slug>-<date>-report.md` via Write, never overwriting a prior report for the same slug. `allowed-tools: AskUserQuestion, Read, Write, Glob, Grep, Artifact, Skill`.

**Other platforms** (Claude web chat, Claude Cowork, ChatGPT web chat, Codex, or any other surface): build the dashboard as structured tables and explicit chart specifications (chart type, axes, series, values) directly in the chat report — same content and findings as the artifact version, just without an interactive rendering. Ask in-workflow clarifying questions as plain numbered text (recommended option marked, free-text override open) since no clickable-question tool is assumed. The report posted in chat is the complete, required output; offer it as a downloadable file or ask the user where to save it if the platform supports persistent storage the user has authorized — otherwise state plainly that no file was saved.

## Limitations

- This skill computes only from data the user actually supplies — it cannot verify that supplied figures match the underlying platform's live records.
- Anomaly and cohort findings require the minimum data stated above; short of that, only the framework is provided, not a computed result.
- KPI targets by business stage are general benchmarks, not guarantees — actual healthy ranges vary by category, margin structure, and market.
- This skill does not forecast future revenue, traffic, or sales, and does not diagnose SEO or AI-search causes directly — see Related audits above for those.
