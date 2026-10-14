---
name: clickmax-payments-dashboard-analysis
description: Use when the user wants payment dashboard KPIs, paginated dashboard views, my-sales queries, filter lookups, or a recoverable-revenue reading (how much is failed/canceled/refunded/pending/abandoned to win back) for seller revenue analysis in Clickmax.
---

## When this applies

Use this skill for payment dashboard browsing and seller revenue analysis: headline KPIs, dashboard filter discovery, paginated transactions/subscriptions/affiliate lists, my-sales queries, external sales charts, and the recoverable-revenue reading (how much money is still winnable back across failed, canceled, refunded, pending, and abandoned-cart cohorts).

Not this skill:

- detailed refund operations -> `clickmax-transaction-operations`
- customer subscription lifecycle mutation -> `clickmax-seller-subscriptions`
- why sales are failing, grouped by reason with the recoverable value per reason -> `clickmax-failure-diagnosis`

## Key assumptions

- `dashboard_filters` is the discovery surface for valid filter values
- `dashboard_my_sales` supports richer filter bodies than the simpler paginated lists
- `dashboard_my_sales` splits into rows and KPIs: `dashboard_my_sales_aggregations` returns the KPI object alone, and `dashboard_my_sales` with `includeAggregations: false` returns the rows alone. Asking for both when you need one costs ~15 full scans for nothing.
- list endpoints and KPI endpoints can derive time windows differently from the chosen range
- external sales are a separate surface and should not be merged blindly into native sales conclusions
- `recovery_recoverable_revenue` is the cheap aggregate for "how much can I recover" — it returns deduplicated buckets (failed, canceled, refunded, pixPending, boletoPending, cartAbandonment) plus reason/stage breakdowns, without paginating rows; prefer it over paging `dashboard_my_sales` just to re-sum recoverable money
- `dashboard_get` and `dashboard_my_sales_aggregations` scope sales DIFFERENTLY — not interchangeable for a count: `dashboard_get.byStatus` blends owner + affiliate + coproducer roles into one number; the my-sales aggregations (`totalNumberOfSalesPaid/Failed/Canceled/Refunded`) scope strictly to `sellerId = ownerId`, matching what the visual dashboard's sales table/tab shows. Using `dashboard_get` to answer "how many sales did I make" overcounts vs. what the user sees on screen.
- KPI values are cached briefly per (workspace + filters), so a sale made seconds ago can be in the rows before it is in the totals. Do not reconcile a row-level count against the KPI object in the same breath.

## Thought process

0. ANY sales value/count question ("quantas vendas hoje", "quanto vendi", "quanto faturei", "como estão minhas vendas", "e agora?" refresh) → MANDATORY sales-overview bundle (defined in `clickmax-analytics`): in the SAME script also call `mcp__plugin_clickmax_clickmax__recovery_recoverable_revenue` (or reuse `aggregations.recovery` when `dashboard_my_sales_aggregations` already ran) + `mcp__plugin_clickmax_clickmax__transactions_failure_breakdown`, same window. Skip only when the user explicitly limits the answer ("só o número", "só vendas pagas").
1. Identify whether the user needs KPIs, paginated rows, filter discovery, deeper my-sales queries, or the recoverable-revenue total.
2. Prefer the narrowest dashboard surface that answers the question.
3. Use my-sales when the filter logic is more expressive than the lightweight dashboard lists.
4. For "how much is there to recover", size it with the recoverable-revenue aggregate first, then drill into a specific cohort only if the user asks.

## Execute guide

- For "how many sales did I make" / seller-scoped counts (matches the visual dashboard), use `mcp__plugin_clickmax_clickmax__dashboard_my_sales_aggregations` (`totalNumberOfSalesPaid/Failed/Canceled/Refunded`, `totalSales`), NOT `dashboard_get` — see scope warning in Key assumptions. It takes the same filter body minus pagination and sorting.
- For top-level KPI snapshots that intentionally blend owner+affiliate+coproducer (balance, overall earnings trend), use `mcp__plugin_clickmax_clickmax__dashboard_get` with the requested range and only the narrow filters that materially change the reading, such as product.
- For available filter values before analysis, use `mcp__plugin_clickmax_clickmax__dashboard_filters` with an empty body once per session, then reuse discovered project/product/client/status values instead of guessing ids or labels.
- Keep filter shape explicit: date ranges, status/project/product/client filters, pagination (`page` / `perPage`), and sorting (`column` / `order`) materially change dashboard rows.
- For paginated dashboard browsing, use the smallest list that matches the request:
  - transactions -> `mcp__plugin_clickmax_clickmax__dashboard_transactions_list`
  - subscriptions -> `mcp__plugin_clickmax_clickmax__dashboard_subscriptions_list`
  - affiliates -> `mcp__plugin_clickmax_clickmax__dashboard_affiliates_list`
- For seller-revenue analysis with richer filter bodies, prefer `mcp__plugin_clickmax_clickmax__dashboard_my_sales`, especially when the question depends on `productIds`, `transactionStatus`, or an explicit `transactionPeriod` window. When you are scanning rows (cohorts, per-buyer joins, exports), pass `includeAggregations: false`.
- For "how much do I have to recover" (aggregated recoverable revenue across every loss/pending cohort), use `mcp__plugin_clickmax_clickmax__recovery_recoverable_revenue` with an optional period and product/offer/project scope. It reconciles with the recovery totals shown on the my-sales screen. Do not page `mcp__plugin_clickmax_clickmax__dashboard_my_sales` with non-paid statuses just to re-sum what this aggregate already returns.
- For listing recent abandoned carts (the concrete people, offer, and stage `personal_data`/`payment_data`), use `mcp__plugin_clickmax_clickmax__lead_activities_list` filtered to the `cart.abandonment.v1` event. Take the cart value from the offer's current price.
- For external-sales trend reading, use `mcp__plugin_clickmax_clickmax__dashboard_external_sales_chart` with explicit `from`, `to`, and period granularity such as `daily`.
- For external-sales row analysis, use `mcp__plugin_clickmax_clickmax__dashboard_external_sales`; keep those conclusions separate from native dashboard KPIs unless the user explicitly wants a combined comparison.

## Report

- Lead with the business takeaway and the period assumption.
- Order results from highest-signal KPI or cohort insight to supporting rows.
- Cap long row dumps and prefer ranked summaries with `+N more` when needed.
- Treat follow-up actions as opt-in only.
- **A sales-count/value answer ("quantas vendas", "quanto vendi") ALWAYS leads with a `cx-hero`** for the paid value + count (`value-tone="positive"`), even for a single sale or a small amount — never state the sales value only in prose. This mirrors the recovery rule below and holds regardless of how many sales there are. Then, same reply: `cx-hero` a recuperar (`warning`, `icon="database-sync"`) + `cx-ranking` of top failure reasons (`warning`, `hint` = next action per `clickmax-failure-diagnosis`) + one opt-in next step. Refresh follow-ups ("e agora?") re-run the whole bundle and keep the same shape.
- **Recoverable revenue is money still winnable back, not a consummated loss** — present it end to end in the `warning` money tone, never `negative`. Lead a recovery answer with a `cx-hero` for the total recoverable value (`icon="database-sync"`), then a `cx-breakdown` (`layout="kanban"`) by origin/stage; differentiate sub-cases (bank decline vs pending vs abandoned) via `hint`/label text, not by changing the tone. Empty state: "Nada a recuperar no período 🎉". Never surface card data or CPF/document.

## Warnings

- Do not merge external-sales semantics into native dashboard KPIs without stating it.
- Dashboard ranges and filter bodies matter to interpretation.
- Recoverable revenue is an opportunity, not realized revenue — never colour it green (`positive`) or red (`negative`); it is `warning` (yellow).

## Anti-patterns

- Answering "quantas vendas / quanto vendi" with only the paid hero and making the user ask for recoverable value, failures, and next action one by one.
- Stating the sales value/count only in prose instead of a `cx-hero` — the model may plan a hero in its own reasoning and then drop it when writing the final answer; the hero is mandatory output, not optional polish.
- Pulling my-sales for every small dashboard question.
- Dumping raw paginated rows without synthesis.
- Paging `dashboard_my_sales` with non-paid statuses to re-count recoverable money that `recovery_recoverable_revenue` already aggregates.
- Paging `dashboard_my_sales` to sum a KPI that `dashboard_my_sales_aggregations` returns in one call.
- Scanning rows without `includeAggregations: false`, which recomputes every KPI on every page.

---

Clickmax skill revision: `b8294822a4d6`
