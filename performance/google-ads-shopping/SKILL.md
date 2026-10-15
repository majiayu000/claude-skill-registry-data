---
name: google-ads-shopping
description: "Use when analyzing or optimizing Google Ads Shopping campaigns: feed health gate, item KILL/DOWNGRADE/PROMOTE rules, product groups, search-term negatives, SCALE/T/CAP."
metadata:
  source: "prompts/skills/google_ads/shopping"
---

# Google Ads Shopping — Optimization Protocol

Product-led optimization: validate feed → classify items → manage structure → scale or cut.

## Step 0: Feed Health (BLOCKING — fail = STOP)

Before any optimization, verify:
- ≥ 80% products approved in Merchant Center
- Purchase conversion tracking is active (conversions_value > 0 in data)
- Price and availability are accurate (requires manual verification or Merchant Center check)

**If ANY check fails → STOP all optimization. Fix feed first.**

---

## Step 1: Data Pull

Query using `google_ads_run_gaql`:

1. **Account AOV**: total conversions_value / total conversions from `customer` resource, LAST_30_DAYS
2. **Item-level performance**: product_item_id, product_title, product_brand, cost, conversions, conv_value, clicks, impressions from `shopping_performance_view`. Sort by cost DESC, limit 200. Filter: `SHOPPING` campaigns.
3. **Campaign-level**: campaign id/name/status, budget, cost, conversions, conv_value from `campaign`. Filter: `SHOPPING`, `ENABLED`.
4. **Search terms**: search_term, cost, clicks, conversions from `search_term_view`. Filter: `SHOPPING`. Sort by cost DESC, limit 200.
5. **Daily budget utilization**: campaign id, date, cost from `campaign`. Filter: `SHOPPING`, `LAST_14_DAYS`.

**Lookback**: 14 days if ≥ 100 purchases/month, otherwise 30 days.

Ask user for **target ROAS**. Default: historical 30-day ROAS.

---

## Step 2: Item-Level Classification

Sort items by cost (highest first). For each item:

| Classification | Condition | Action |
|---------------|-----------|--------|
| **KILL** | Cost ≥ 2× AOV AND conversions = 0 | Exclude item ID immediately. No learning window. |
| **DOWNGRADE** | ROAS < 0.7× target AND cost ≥ 0.5× AOV | Lower bid or exclude. Item is spending but underperforming. |
| **PROMOTE** | Conversions ≥ 2 AND ROAS ≥ target | Isolate into own product group/campaign to protect budget. |

Items not matching any rule: monitor, no action needed.

---

## Step 3: Product Group Structure

- Maximum 3 product groups per campaign
- Split ONLY when economics differ (different margins, price bands, seasonal risk)
- If groups don't have meaningfully different ROAS targets → consolidate

---

## Step 4: Search Term Negatives

Add negatives ONLY for wrong-intent terms:
- Price objection: free, cheap, budget, discount code, coupon
- DIY/repair: diy, repair, fix, how to, tutorial
- Used/second-hand: used, second hand, refurbished, pre-owned
- Products not in feed (compare search terms to product titles)
- Irrelevant attributes (colors/sizes not offered)

Do NOT negate high-intent commercial terms even if they haven't converted yet.

---

## Step 5: Budget & Bid Decisions

### SCALE (increase budget 10–20%)
ALL must be true:
- Campaign ROAS ≥ target
- Budget utilization ≥ 90% on 10+ of last 14 days
- Top 20% of SKUs by conversions account for ≥ 60% of spend (winners getting the budget)

### CUT/CAP (reduce budget or exclude SKUs)
ANY true:
- Campaign ROAS < target
- SKUs with ROAS < 0.7× target receiving increasing spend share WoW

→ Reduce budget OR exclude underperforming SKUs first, then reassess.

---

## Step 6: Device & Location (last)

Only analyze if segment spend ≥ 2× AOV (enough data to judge).

- Exclude device/location ONLY if ROAS ≤ 0.6× account average AND no operational explanation (e.g., mobile site is broken)
- Check for technical issues before excluding (site speed, checkout flow)

---

## Step 7: Campaign Kill Conditions

Pause the Shopping campaign if:
- ROAS < 0.6× target after total spend ≥ 2× AOV
- Shopping ROAS consistently worse than Search ROAS over 30+ days

---

## Prohibitions

- Never optimize by CTR alone (Shopping is ROAS-driven)
- Never let cheap, low-converting SKUs dominate spend
- Never scale without confirming winners are getting the budget

Output must include: item classification summary (KILL/DOWNGRADE/PROMOTE counts + savings), search term negatives, budget recommendation with rationale, expected 7-day ROAS impact.
