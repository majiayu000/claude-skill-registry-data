---
name: shopify-order-discipline
description: "Use when querying Shopify orders or reconciling against a merchant dashboard. Default NO financial_status filter (dashboard parity), gross vs net revenue, created_at vs processed_at, refunds handling, multi-currency confirmation."
metadata:
  source: "prompts/skills/shopify/order-discipline"
---

> **Outside the GoMarble app.** This methodology is GoMarble's own, kept in sync with the GoMarble connector.
> - GoMarble connector tools for this skill: `shopify_list_shops`, `shopify_run_analytics_query`, `shopify_list_orders_by_query`, `shopify_list_products_by_query`, `shopify_list_customers_by_query`, `shopify_get_all_details_by_gid`.

# Shopify Order Discipline

Before any Shopify order / revenue or checkout/session funnel query goes to the user:

1. **Default to NO `financial_status` filter.** Shopify's "Total orders" / "Gross sales" tile counts ALL statuses (`pending`, `authorized`, `partially_paid`, `paid`, `partially_refunded`, `refunded`, `voided`). Adding `financial_status:paid` agent-side silently excludes pending + partially-paid orders and produces a number the merchant cannot reconcile against their dashboard.
2. **Clarify gross vs net BEFORE reconciling.** Shopify "Gross sales" = line items × qty (before discounts, refunds). "Net sales" = gross − discounts − refunds. 3rd-party MTAs (Cosmise, Triple Whale, Northbeam, etc.) typically report net. Never compare gross-against-net silently.
3. **Be explicit about timestamp field + timezone.** `created_at` (order created) vs `processed_at` (payment processed) can differ by hours. Orders placed near midnight UTC may roll to the next day in the merchant's local timezone.
4. **Shopify sessions analytics is the source of truth for checkout sessions.** For checkout sessions, sessions reaching checkout, checkout drop, cart-to-checkout, or funnel-session questions, use `shopify_run_analytics_query` with `dataset="sessions"` and metric `sessions_that_reached_checkout`.
5. **If Shopify analytics cannot run, say so.** If the tool reports missing `read_reports`, state that Shopify checkout/session metrics cannot be verified with current permissions. GA4 `begin_checkout` / `checkouts` can only be used as a clearly labeled proxy.
6. **Never use orders as checkout sessions.** `shopify_list_orders_by_query`, order counts, and revenue are completed-purchase/order data. They are not a fallback for checkout starts or checkout sessions.

---

## Rule 0 — Checkout / Session Funnel Source of Truth

For requests about **checkout sessions**, **sessions reaching checkout**, **checkout-session decline**, **cart-to-checkout dropoff**, **checkout funnel**, **session decline tied to checkout**, or regional checkout sessions such as **Ontario checkout sessions**, Shopify sessions analytics is the primary source of truth when Shopify is connected.

Use `shopify_run_analytics_query` before substituting another source:

- Dataset: `sessions`
- Core metrics: `sessions`, `sessions_with_cart_additions`, `sessions_that_reached_checkout`, `sessions_that_completed_checkout`, `conversion_rate`
- Common dimensions: `session_country`, `session_region`, `session_city`, `referrer_source`, `utm_source`, `utm_medium`, `utm_campaign`
- For time trends: use `timeseries: "day"` or `timeseries: "week"` and explicit `start_date` / `end_date`
- Preserve the standard sessions filter from the tool recipes: `human_or_bot_session IN ('human', 'bot')`

If ShopifyQL fails because `read_reports` is missing, say exactly that Shopify checkout/session metrics cannot be verified with the current Shopify permissions. You may use GA4 `begin_checkout`, GA4 `checkouts`, or GA4 funnel reports only as a labeled proxy, not as Shopify checkout sessions.

Never use Shopify orders, order counts, revenue, or `shopify_list_orders_by_query` as a fallback for checkout sessions. Orders represent completed order records; they do not measure sessions that reached checkout.

---
## Rule 1 — No `financial_status` Filter By Default

| Status | Meaning | In "Total orders" tile |
|---|---|---|
| `pending` | Order placed, payment not captured | YES |
| `authorized` | Payment authorized, not captured | YES |
| `partially_paid` | Partial payment received | YES |
| `paid` | Full payment captured | YES |
| `partially_refunded` | Order kept; partial refund issued | YES (full original stays in gross) |
| `refunded` | Order fully refunded | YES (in gross; net subtracts the refund) |
| `voided` | Order voided | Typically excluded |

- Default Shopify orders query → NO `financial_status` filter. Result should match the merchant's "Total orders" / "Gross sales" tile.
- Add `financial_status:paid` ONLY when the user explicitly says "paid only" / "captured payments only" / "exclude pending".
- If the filter is set and the result doesn't match the dashboard, FIRST fix is to remove the filter and re-query — never invent "Meta + Google attribution overlap" or similar explanations.

**Forbidden** (without explicit user request): `query="created_at:>={start} AND created_at:<={end} financial_status:paid"` · any agent-authored exclusion of pending / partially-paid / refunded statuses.

---

## Rule 2 — Gross vs Net Revenue

| Concept | Definition | Where it shows up |
|---|---|---|
| **Gross sales** | line items × qty (before discounts, refunds) | "Gross sales" tile · API `total_line_items_price` |
| **Net sales** | gross − discounts − refunds | "Net sales" tile |
| **Total sales** | net + shipping + taxes | "Total sales" tile · API `total_price` |

3rd-party MTAs (Cosmise, Triple Whale, Northbeam, Wicked Reports, Lifetimely, Profitmetrics, Hyros, Rockerbox) typically report a NET-style figure.

- When the user says *"`{tool}` shows `{X}` for revenue"* and your number differs, FIRST hypothesis is gross-vs-net (or refund timing), not "tracking is broken".
- Never silently compare Shopify gross against a 3rd-party MTA net number — surface the methodology difference.
- State the revenue concept: *"Querying `total_price` for `{X}` gross; if `{tool}` shows net (after refunds), the gap is likely the partially-refunded portion."*

---

## Rule 3 — `created_at` vs `processed_at`

| Field | Meaning |
|---|---|
| `created_at` | When the order was created in Shopify |
| `processed_at` | When payment was processed / order moved out of pending |

Usually within minutes. Late-night UTC orders or delayed-capture gateways (Klarna, AfterPay batch overnight) can shift dates by a day.

- State the field + timezone: *"Querying `created_at:>={start} AND created_at:<={end}` in shop timezone `{tz}`."*
- If the dashboard total differs by a small count of orders, check whether the gap is `created_at` vs `processed_at` near the period boundary.
- When the merchant says "orders for `{month}`", confirm: orders CREATED in that month, or orders PROCESSED in that month?

---

## Rule 4 — Refund Handling

| Status | What happened | How to count |
|---|---|---|
| `partially_refunded` | Order kept, partial refund issued | Stays in count; gross stays in gross. Refunded $$ is in `refunds[].transactions[]` |
| `refunded` | Order fully refunded | Stays in count; gross stays in gross. Net subtracts entirely. |

- For gross, include all orders regardless of refund status.
- For net, subtract refund totals from gross. `refunds[].transactions[]` has per-order refund amounts.
- For partial refunds: deduct only the refunded portion, not the full order value. If your number is higher than the MTA's, partial refunds are the likely cause.

---

## Rule 5 — Multi-Currency

Shops can have a base `currency` AND orders denominated in other currencies. `total_price` is in the order's own currency; `total_price_set.shop_money.amount` is in the shop's base currency.

- Confirm the shop's base currency before reporting revenue. Don't assume USD.
- For consistency when summing across orders, use `total_price_set.shop_money.amount`.
- State the currency: *"All revenue figures in shop's base currency: `{CCY}`."*

---

## Rule 6 — User Disputes Your Shopify Number → Re-Query

When the user disputes your number with *"shopify said `{X}`"* / *"my dashboard shows `{X}`"* / *"in Shopify it's `{X}`"*:

1. Acknowledge the gap without defending the prior number.
2. Re-run with NO `financial_status` filter (Rule 1) and the right revenue field (Rule 2).
3. If the result now matches the dashboard: *"You're right — removing the `financial_status:paid` filter (which I had added) returns `{X}`, matching your dashboard."*
4. Do NOT blame "Meta + Google attribution overlap" or claim the dashboard is wrong.

---

## Examples

**Default order count for a window — user disputes**

❌ `query="created_at:>={start} AND created_at:<={end} financial_status:paid"` → `{N1}` orders. (User: *"shopify said `{N2}`"*.) Then: *"The gap is Meta + Google attribution overlap."*

✅ `query="created_at:>={start} AND created_at:<={end}"` (no `financial_status`) → `{N2}` orders. *"For `{period}` (shop tz `{tz}`): `{N2}` orders, `{gross}` gross sales. Includes pending, partially_paid, paid, partially_refunded — same scope as your Total Orders tile."*

**MTA shows lower gross than your Shopify number**

❌ *"4-hypothesis discrepancy: date logic, refund timing, status filter, timezone."* (Zero tool calls.)

✅ Re-pull Shopify with refund handling explicit. Then: *"Shopify net (gross minus refunds within the period): `{net}` — matches `{tool}`'s `{X}` within rounding. My earlier `{gross}` was gross (before refunds). The gap is `{N}` fully-refunded orders + the refunded portions of `{M}` partially-refunded orders."*
