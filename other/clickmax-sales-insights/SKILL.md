---
name: clickmax-sales-insights
description: Use when the user wants to know what is selling — top offers/products by revenue and quantity, order-bump attach rate, or period-over-period sales trend (revenue, average ticket, sales count) for seller sales analysis in Clickmax.
---

## When this applies

Use this skill for ready-made sales insights that need aggregation across many transactions: ranking the best-selling offers/products by revenue and quantity in a window, the attach rate of order bumps, and period-over-period sales movement (revenue, average ticket, sales count with the delta versus the previous comparable window). These answers require server-side aggregation — prefer the insight operations here over paging raw sales rows and re-summing them by hand.

Not this skill:

- headline KPIs, filter discovery, paginated my-sales/transactions browsing, or the recoverable-revenue reading -> `clickmax-payments-dashboard-analysis`
- why sales are failing, grouped by reason with the recoverable value per reason -> `clickmax-failure-diagnosis`
- customer subscription lifecycle mutation -> `clickmax-seller-subscriptions`

## Key assumptions

- All three insights read realized (paid) sales only, in a default 30-day window when the user gives no explicit period.
- `insights_top_offers` groups by offer by default; pass a product grouping when the user asks about products rather than individual offers. `revenue` uses the same sales-value expression as the dashboard, so it reconciles with the my-sales revenue for the same period.
- `insights_order_bump_attach` reports attach rate as paid orders that included the bump divided by paid orders of the main offer the bump is attached to — one row per (bump, main offer) pair. It is a rate over eligible orders, not a share of revenue; for the revenue share of bumps use the dashboard skill instead.
- `insights_trend` compares the current window against the immediately preceding window of the same length. It does not cover conversion rate (traffic is not part of the sales domain) — answer revenue, average ticket, and sales count only, and say conversion is out of scope if asked.

## Thought process

1. Decide which question is being asked: what sold most (ranking), how well bumps attach (rate), or whether sales grew/fell versus a prior period (trend).
2. Pick the single matching insight operation; do not page raw sales rows to reconstruct these aggregates.
3. Honour an explicit period when given; otherwise state the 30-day default in the answer.
4. Keep the window and any product/offer/project scope consistent across follow-up questions so numbers stay comparable.

## Execute guide

- For "what sold most / best offers / best products", use `mcp__plugin_clickmax_clickmax__insights_top_offers` with an optional `transactionPeriod` and product/offer/project scope. Set the grouping to product when the user asks about products; otherwise keep the default offer grouping. Limit the ranking to the top few unless the user wants more.
- For "what is the attach rate of my order bumps", use `mcp__plugin_clickmax_clickmax__insights_order_bump_attach` with an optional period and scope. Present the rate per order bump against its main offer; make explicit that the denominator is the main offer's paid orders.
- For "did sales grow / how do the last N days compare", use `mcp__plugin_clickmax_clickmax__insights_trend` with the target window. Report revenue, average ticket, and sales count, each with the delta versus the previous window. If the user asks about conversion, state that it is not available from sales data here.

## Report

- Lead with the business takeaway and the period assumption (state the 30-day default when the user gave no window).
- **Sales insights are realized revenue and growth — a gain, presented in the `positive` money tone (green), never `warning` or `negative`.** Use `negative` only when a trend delta is an actual drop.
- For a top-offers answer, lead with a `cx-hero` for the period revenue (`value-tone="positive"`, `icon="search-graph"`) with context pills (sales count, and the trend delta when known), then a `cx-ranking` (`medals="true"`) of the offers: `value` = revenue, `tag` = quantity, `pct` proportional to the top row. The card replaces the same numbers in prose — do not repeat them in a paragraph.
- For an attach-rate answer, use a `cx-ranking` of attach % per order bump (`value` = attach rate, `tag` = attached/eligible count), ordered highest first; or a `cx-breakdown` (`layout="list"`) when comparing with/without bump.
- For a period comparison, use `cx-compare` with two bars per row (current vs previous) and a `tag` showing the signed delta with its base (e.g. "+12% vs período anterior"). Positive movement uses `positive`/`acid` accents; a drop uses `negative`/`torch`.
- Order results highest-signal first; cap long rankings with `+N more`.
- Question also asks the period's sales value ("quanto vendeu hoje e de cada oferta") → add the sales-overview bundle (`clickmax-analytics`: a recuperar + failure reasons with next action) after the ranking, same window.
- Treat follow-up actions as opt-in only. Never surface card data, CPF/document, or internal ids as visible text.
- Empty state: "Nenhuma venda no período."

## Warnings

- Do not colour realized sales or growth as recoverable (`warning`) or as loss (`negative`); paid revenue and growth are `positive` (green). A trend `negative` tone is only for an actual decline.
- Attach rate is a rate over eligible paid orders of the main offer, not the revenue share of bumps — do not conflate the two.
- Trend does not include conversion; do not invent a conversion figure from sales data.
- State the window explicitly; the same question over a different period is a different answer.

## Anti-patterns

- Paging raw sales rows to rebuild a ranking, attach rate, or trend that these insight operations already aggregate.
- Reporting attach rate against total orders instead of the main offer's orders.
- Presenting sales growth in yellow or red instead of green.
- Dumping the full offer list instead of a ranked, capped summary.

---

Clickmax skill revision: `b8294822a4d6`
