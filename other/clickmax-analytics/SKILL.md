---
name: clickmax-analytics
description: Use when the user asks business/revenue/KPI questions like how much they made, how they are performing, top products, lead counts, funnel performance, or campaign/email open rates over a period.
---

## When this applies

Use this skill for business/KPI questions answered by specific analytics cuts over a date range: revenue totals, period-over-period sales, lead/conversion metrics, funnel step performance, messaging engagement, campaign (broadcast) and per-channel message performance, top products, most-accessed sales pages, and recent workspace activity.

## Not this skill

- payment dashboard browsing, my-sales rows, or drilling into one loss/recovery cohort (`failed`, `canceled`, `refunded`, `chargedBack`, `dispute`, `pending`) -> `clickmax-payments-dashboard-analysis` (the sales-overview bundle below stays here)
- refund/chargeback operations on a transaction -> `clickmax-transaction-operations`
- raw per-lead timelines or owner activity aggregates -> `clickmax-leads-activity-analysis`
- finding/filtering individual leads -> `clickmax-leads`
- building or reading a saved Insights dashboard of opportunities BI -> `clickmax-insights-dashboards`

## Key assumptions

- these are workspace-scoped read-only cuts; do not ask for workspace/owner ids.
- date filters are `startDate` / `endDate` (ISO date strings); backend clamps start to two-years-ago and end to today/tomorrow, so out-of-range dates are silently trimmed.
- comparison tools (`analytics_sales_metrics`, `analytics_leads_metrics`, `analytics_messages_metrics`) take a current window plus a `previousStartDate` / `previousEndDate` window; set both windows explicitly for honest growth reads.
- `projectSlugs`, `funnelIds`, `pageIds` are optional array filters; empty means whole workspace.
- percentage fields are 0..1 fractions (multiply by 100 for display); money fields are already amounts, not cents-strings.
- revenue splits: `analytics_total_sales` returns `totalInSales` (internal/native), `totalExternalSales` (imported platforms, with `externalBreakdown` per platform), and `totalRevenue` (sum). State which one you mean.
- there is no direct "lost/refused revenue" cut in this skill; `previousPeriodGrowth` (in `analytics_sales_metrics`) can be negative but means decline vs the prior window, not lost money.
- `analytics_top_products` `limit` defaults 5 (max 100); `analytics_sales_pages` `limit` defaults 5 (max 20).

## Sales overview bundle (MANDATORY)

Sales-overview question ("como estão minhas vendas", "quanto faturei", "quanto vendi hoje", "quantas vendas", "quanto estou perdendo", "resumo das vendas", "how are my sales") = ONE complete answer, never only the literal number. Sellers expect faturado + a recuperar + why sales fail + what to do, without asking one by one.

Run in the SAME Code Mode script, same window + filters:

|Call|Gives|
|-|-|
|`mcp__plugin_clickmax_clickmax__analytics_total_sales`|faturado (`totalRevenue` + internal/external split)|
|`mcp__plugin_clickmax_clickmax__recovery_recoverable_revenue`|total a recuperar (deduplicated buckets: failed, canceled, refunded, pixPending, boletoPending, cartAbandonment)|
|`mcp__plugin_clickmax_clickmax__transactions_failure_breakdown`|failures by stable `code` + value|

- Map `from`/`to` (failure breakdown) and `transactionPeriod` (recovery) to the same `startDate`/`endDate` window.
- Translate failure `code` → label + next action via the `clickmax-failure-diagnosis` map (`activate_skill` it); never print raw gateway reasons or raw `code`.
- Headline "a recuperar" = recovery total (deduplicated). Failure-breakdown `count`/`value` are per ATTEMPT (same buyer retrying counts N times) → label them "tentativas", never "pessoas", never sum them into the recoverable headline.
- NEVER page `dashboard_my_sales` rows to hand-count failures or buyers for this answer.
- One tool failing → still answer with the others and say which part is missing.
- Skip the bundle only when the user asks for ONE specific cut ("só o faturamento", "top produtos", "quantos leads").

## Thought process

1. Sales-overview question → run the bundle above. Otherwise map the question to the narrowest tool:
   - revenue-only cut ("só o faturamento") -> `analytics_total_sales` for the range (headline revenue: internal + external + total), or `analytics_sales_metrics` when they also want conversion, top product, or growth vs a prior period.
   - "quantos leads" / lead conversion / lead price -> `analytics_leads_metrics`; lead-engagement overview across lists -> `analytics_leads_overview`.
   - "top produtos" / best sellers -> `analytics_top_products`.
   - "desempenho do funil" -> `analytics_funnel` (step + aggregate stats + sales history).
   - messaging engagement -> `analytics_messages_metrics`; automation reach/executions -> `analytics_flows_overview`.
   - campaign open/click rate, per-channel delivery/open/bounce, WhatsApp template reads -> see `### Campaign and message performance`.
   - page traffic -> `analytics_sales_pages`; latest workspace movement -> `analytics_recent_activities`.
2. "quanto estou perdendo" / lost money → the bundle's recovery total + failure ranking IS the answer (recoverable money, not consummated loss). Extra leakage signals, labeled as such, never as a loss total: low `salesConversionPercentage`, `totalViews` vs `totalProductsSold`, negative `previousPeriodGrowth` (all from `analytics_sales_metrics`).
3. For period-over-period questions, always pass an explicit previous window so growth is meaningful.

## Execute guide

- Headline revenue for a window: use `mcp__plugin_clickmax_clickmax__analytics_total_sales` with `startDate` and `endDate` covering the window, optionally scoped by `projectSlugs`; read `totalRevenue` plus the `totalInSales` / `totalExternalSales` split.
- Sales performance with comparison: use `mcp__plugin_clickmax_clickmax__analytics_sales_metrics` with `startDate`/`endDate` for the current window and `previousStartDate`/`previousEndDate` for the prior window; read `totalAmount`, `salesConversionPercentage`, `totalProductsSold`, `products`, `topConversionProduct`, and `previousPeriodGrowth`.
- Lead metrics: use `mcp__plugin_clickmax_clickmax__analytics_leads_metrics` with the same window/previous-window pattern plus optional `funnelIds` / `pageIds`; read `totalLeads`, `leadConversionPercentage`, `leadAveragePrice`, and `leadsPerMonth`.
- Lead-engagement overview: use `mcp__plugin_clickmax_clickmax__analytics_leads_overview` with `startDate`/`endDate` for engaged contacts, active flows, and per-list engagement.
- Top products: use `mcp__plugin_clickmax_clickmax__analytics_top_products` with `startDate`/`endDate`, optional `funnelIds` or `productId`, and `limit` for how many to rank.
- Funnel performance: use `mcp__plugin_clickmax_clickmax__analytics_funnel` with `funnelIds` and/or `projectSlugs` plus the date window; read `steps`, `stats`, and `salesHistory`.
- Messaging engagement: use `mcp__plugin_clickmax_clickmax__analytics_messages_metrics` with window + previous window; read `totalMessagesSent` and per-channel (`mail`, `whatsApp`, `telegram`) engaged percentages.
- Automation reach: use `mcp__plugin_clickmax_clickmax__analytics_flows_overview` with `projectSlugs` and the window for `activeFlows`, `totalExecutions`, and `topFlows`.
- Sales-page traffic: use `mcp__plugin_clickmax_clickmax__analytics_sales_pages` with optional `projectSlugs` / `funnelIds` and `limit`.
- Recent activity: use `mcp__plugin_clickmax_clickmax__analytics_recent_activities` with `startDate`/`endDate` and optional `projectIds`, `funnelIds`, `categories`.
- Showcase prompt "quanto faturei nos últimos 15 dias e quanto estou perdendo":
  1. Window: `endDate` = today, `startDate` = today − 15d; prior 15 days → `previousStartDate` / `previousEndDate`.
  2. Run the bundle + `mcp__plugin_clickmax_clickmax__analytics_sales_metrics` (conversion, top product, `previousPeriodGrowth`) over the same 15 days.
- Keep the same date window and filters across tools in one answer so numbers stay comparable.

### Campaign and message performance

|Question|Tool + input|Read|
|-|-|-|
|"how did my campaigns do" / "what is my open rate"|`mcp__plugin_clickmax_clickmax__broadcasts_list` with `channel = email`, `perPage = 20` (`50` for a baseline)|each campaign's `rates` (open/click/bounce over `sent`) + volume-weighted average across sent campaigns; campaign sends only|
|"how is email/WhatsApp performing overall in a period" (campaigns + automations)|`mcp__plugin_clickmax_clickmax__messages_metrics` for the window, again for the previous window of the same length; optional `platform` (WhatsApp = `gupshup`)|per-platform `total`, `reached`, `opened`, `failed`, `bounced`, `spamComplaints`, `openRate` / `failureRate` / `bounceRate`, trend vs previous window|
|"why did this campaign do well/badly" / "when do people open"|`mcp__plugin_clickmax_clickmax__broadcasts_insights` with `broadcastId` from `mcp__plugin_clickmax_clickmax__broadcasts_list`|`opensByHour`, `topLinks`, `devices`, `clients`, `geo`, `engagement` (open/click rate + delta vs previous campaign), `creditCost`|
|WhatsApp template reads/clicks|`mcp__plugin_clickmax_clickmax__gupshup_template_analytics` with the template `externalId` from `mcp__plugin_clickmax_clickmax__gupshup_templates_list` (only templates submitted to Meta have one)|`sent`, `delivered`, `read`, `clicked`, `readRate` / `clickRate` over delivered|

- `messages_metrics` `openRate` = opened / reached, first opens only; no clicks there → click rates come from `broadcasts_list`.
- automation (flow) emails are not in `broadcasts_list` → `messages_metrics` covers campaigns + automations combined.
- rates here are 0..1 fractions or `null` when the denominator is 0; show `null` as "no data", not 0%.

## Report

- Open with the period assumed and the workspace scope (all projects unless the user narrowed it).
- Answer in plain business language with formatted currency and percentages (fractions ×100); never surface UUIDs, slugs, or raw payloads.
- Lead with the headline number the user asked for, then the strongest supporting cut (growth vs prior period, top product, conversion).
- The runtime renders presentation cards: emit a `cx-metric` for each headline KPI (revenue, conversion, leads) and a `cx-ranking` for top-products / top-flows lists instead of long inline tables.
- Bundle answer order: `cx-hero` faturado (`value-tone="positive"`) → `cx-hero` a recuperar (`icon="database-sync"`, `warning`) → `cx-ranking` of failure reasons by value, every row `tone="warning"`, `hint` = next action (`clickmax-failure-diagnosis` rules) → close with ONE opt-in next step (e.g. recovery automation for the top reason) via the `question` tool. No markdown tables for this data. Empty recovery → "Nada a recuperar no período 🎉".
- Cap ranked lists and summarize the tail as `+N more`.
- When "loss" was requested, report the recoverable total from the bundle (recoverable, not lost); never invent a loss total.
- Treat follow-up actions as opt-in only.

## Warnings

- Do not present `previousPeriodGrowth` or a negative trend as "money lost"; it is a period-over-period delta.
- Do not merge `totalExternalSales` into native-sales conclusions without labeling it; external is imported-platform revenue.
- Comparison tools need both windows; a missing previous window makes growth meaningless.
- Do not invent refund, chargeback, or abandoned-cart totals — take them only from `recovery_recoverable_revenue`.
- Backend clamps dates to the last two years; flag it if the user asked for older data.
- Never compare a campaign open rate (`broadcasts_list`, over sent) with a `messages_metrics` open rate (over reached, campaigns + automations) as if they were the same number: different denominators and scopes.

## Anti-patterns

- Answering a sales-overview question with only the revenue number and making the user ask for recoverable value, failures, and next action one by one.
- Answering "quanto estou perdendo" with a fabricated loss number instead of the bundle's recoverable total.
- Dumping every product/page/activity row instead of a ranked, capped summary.
- Reporting fractions as if they were already percentages.
- Reusing this skill for per-lead timelines or transaction refund operations.
- Asking the user for workspace or owner ids.

---

Clickmax skill revision: `b8294822a4d6`
