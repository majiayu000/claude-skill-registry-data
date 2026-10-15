---
name: ga4-source-of-truth
description: "Use for any GA4 query whose result will be reported back to the user. Covers conversions ≠ transactions distinction, channel-subset-sum trap with sessionDefaultChannelGroup, intraday partial-data discipline, Paid Social aggregation rules, API-vs-UI attribution mismatch."
metadata:
  source: "prompts/skills/ga4/source-of-truth"
---

> **Outside the GoMarble app.** This methodology is GoMarble's own, kept in sync with the GoMarble connector.
> - GoMarble connector tools for this skill: `google_analytics_list_properties`, `google_analytics_run_report`, `google_analytics_get_traffic_sources`, `google_analytics_get_events`, `google_analytics_get_page_views`, `google_analytics_get_user_behavior`, `google_analytics_get_device_metrics`, `google_analytics_get_active_users`.

# GA4 Source-of-Truth

Before any GA4-derived figure goes to the user:

1. **Purchase volume** → use `transactions` or `eventName=purchase`. Never the generic `conversions` aggregate.
2. **Total revenue / sessions / anything** → query WITHOUT `sessionDefaultChannelGroup`. Summing paid-channel rows ≠ business total.
3. **Date range includes today / last 24h** → flag the period as partial. Don't frame as decline / trend.
4. **Number differs from GA4 UI** → check `attributionModel`. API defaults to last-click; UI is often data-driven.

---

## Rule 1 — `conversions` ≠ `transactions`

| Field | Counts |
|---|---|
| `conversions` | Every event marked as a conversion: `add_to_cart`, `begin_checkout`, `sign_up`, `view_item`, `scroll`, custom events, `purchase`. |
| `transactions` (or `eventName=purchase`) | Actual purchase events. |

For revenue / orders / sales-count, use `transactions`. State the field used: *"Using `transactions` (purchase events); `conversions` would include AddToCart / Sign-Up / etc."*

---

## Rule 2 — Channel-Dimension Subset-Sum Trap

`sessionDefaultChannelGroup` partitions revenue across: Direct, Organic Search, Organic Social, Email, Referral, Affiliates, SMS, Cross-network, Paid Search, Paid Social, Paid Shopping, Paid Video, Paid Other, Display, Audio, (Other), Unassigned. **All contribute to total revenue.**

- Business total → SEPARATE query, NO channel dimension.
- Total + breakdown → TWO queries. State both.
- Never sum a paid-channel subset and report as total or as the blended-ROAS denominator.

**Forbidden:** "Total GA4 revenue: `{X}`" where `{X}` is a paid-channel subset · "Blended ROAS = spend / GA4 paid revenue" · "Critical Alert" headlines on a paid-subset denominator.

---

## Rule 3 — `Paid Social` ≠ Meta

`Paid Social` aggregates Meta + TikTok + Snap + Pinterest + LinkedIn + X + Reddit.

To isolate Meta: `sessionSource = "facebook.com"` or `sessionSourceMedium = "facebook / cpc"` (or the merchant's actual Meta UTM pattern).

Never report `Paid Social` GA4 revenue as "Meta revenue" or "Facebook revenue".

---

## Rule 4 — Intraday Partial-Data

- GA4 has documented intraday processing lag — events take hours to appear in standard reports.
- `realtime` API ≠ standard reports. Don't substitute one for the other.
- Conversion attribution backfills 48–72h (more when data-driven attribution is active).

If the date range includes today / last 24h: flag the period as partial. Never recommend pause / scale-down / archive on partial-day data alone.

---

## Rule 5 — Attribution-Model API/UI Mismatch

API defaults to last-click. UI is often data-driven or paid-and-organic last-click. Numbers WILL differ when models differ — this is not a tracking bug.

When the user says *"GA4 shows `{X}`, you're showing `{Y}`"* and the gap is plausibly attribution-driven (small / medium %, all channels affected proportionally):
- Pass an explicit `attributionModel` parameter to match the UI.
- State the model in the response: *"Used last-click attribution (API default); your GA4 UI may be set to data-driven, which can shift values 5–15%."*

---

## Examples

**Total revenue MTD**

❌ `dimensions=[sessionDefaultChannelGroup]` → sum (Paid Social + Paid Search + Cross-network) → report the partial sum as the total.

✅ Query 1: no dimensions → total `{T}`. Query 2: same date range with `sessionDefaultChannelGroup` → channel breakdown. Report both: *"GA4 total revenue MTD: `{T}` (unfiltered). Channel breakdown: Direct `{D}`, Organic `{O}`, Paid Social `{PS}` (includes Meta + TikTok + Snap — for Meta only, query `sessionSource='facebook.com'`), Paid Search `{PSe}` ..."*

**User asks why GA4 conversions are much higher than the platform's purchase count**

❌ *"Tracking discrepancy. The platform pixel may be missing events; you should audit pixel firing."*

✅ *"`conversions` in GA4 counts every event configured as a conversion in your property — AddToCart, Sign-Up, Lead, Purchase. Re-querying with `eventName='purchase'` so we're comparing apples to apples with the platform's Purchase event."* (then issues the query)
