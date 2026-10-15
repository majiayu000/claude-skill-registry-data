---
name: gomarble-skills-ecommerce-brands
description: "Use for ecommerce business questions beyond a single ad channel: which products to scale or cut, cart abandonment and conversion-rate bottlenecks, customer cohorts and repeat purchase, unit economics and contribution margin, channel mix, promotion impact, device and browser issues, and a weekly ecommerce summary. Works from Shopify and GA4 through GoMarble (read shopify-order-discipline and ga4-source-of-truth first), or from exports."
---

# GoMarble Skills for Ecommerce Brands

**9 Core Skills + Weekly Summary** for analyzing and optimizing product performance, unit economics, and revenue across all channels.

> **Read-and-recommend only.** These skills never change your accounts. The model reads data and produces recommendations in plain language; you apply them manually.

---

## The 9 Skills

### 1. Product Performance Ranker
**What it does:** Ranks SKUs by revenue, ROAS, and profit. Shows your true stars vs dead weight.

**How it works:**
- Pareto analysis — top 20% of SKUs drive 80%+ of profit
- Calculates ROI per product (accounts for COGS, not just ad spend)
- Identifies high-volume, low-margin vs high-margin, low-volume products
- Flags seasonal performers vs year-round winners

**Minimum data needed:** Product-level spend, sales count, revenue, COGS per SKU (last 30 days)

---

### 2. Cart Abandonment Debugger
**What it does:** Finds friction points in checkout. Calculates revenue at risk from abandonment.

**How it works:**
- Tracks add-to-cart vs purchase conversion rate by product
- Identifies high-abandonment products (>50% abandonment rate)
- Correlates with shipping cost, price tier, and product type
- Quantifies daily revenue recapturable via recovery email

**Minimum data needed:** Add-to-cart count, completed purchases, average cart value

---

### 3. Customer Cohort Analyzer
**What it does:** Tracks repeat purchase rate, LTV, and which cohorts are your best payers.

**How it works:**
- Segments customers by acquisition month / campaign
- Calculates repeat purchase rate and LTV by cohort
- Flags high-acquisition cost cohorts with low repeat rate
- Identifies best-performing audience segments for acquisition spend

**Minimum data needed:** Customer creation date, repeat purchase history, customer LTV

---

### 4. Unit Economics Calculator
**What it does:** Isolates profit per order and by product. Shows which channels and products are actually profitable.

**How it works:**
- Calculates all-in cost per unit (COGS + fulfillment + payment processing + ad spend)
- Shows profit margin per SKU
- Breaks down by channel (email, paid ads, organic)
- Flags unprofitable products or channels before they bleed cash

**Minimum data needed:** Sell price, COGS, fulfillment cost, payment fees, ad spend, units sold

---

### 5. Channel Mix Optimizer
**What it does:** Shows which channels (Meta, Google, email, organic) drive the most profitable revenue.

**How it works:**
- Calculates ROAS + profit per channel
- Compares customer LTV by acquisition channel (paid vs organic)
- Identifies channel overlap (same customer acquired twice?)
- Recommends budget allocation based on channel efficiency

**Minimum data needed:** Channel attribution, spend per channel, revenue per channel, customer source

---

### 6. Conversion Rate Auditor
**What it does:** Benchmarks your conversion rate against category norms. Finds the biggest bottleneck.

**How it works:**
- Benchmarks site-wide CVR against category average (e.g., apparel vs electronics)
- Breaks CVR by source (paid, organic, email, direct)
- Identifies product pages with below-category CVR
- Flags checkout vs product-page abandonment separately

**Minimum data needed:** Visits, add-to-cart, purchases (by source and product)

---

### 7. Promotional Impact Modeler
**What it does:** Measures true lift from discounts and sales. Catches discounts that cannibalize rather than expand revenue.

**How it works:**
- Compares baseline CVR and AOV to promotion period
- Calculates incremental revenue (not just total revenue during sale)
- Identifies customers who would have bought anyway (cannibalization)
- Measures payback period (how long until discount spending breaks even)

**Minimum data needed:** Date of promotion, daily revenue before/during/after, customer segment

---

### 8. Device & Browser Analyzer
**What it does:** Shows how mobile vs desktop CVR and AOV differ. Flags bad experiences.

**How it works:**
- Compares CVR by device (mobile, tablet, desktop)
- Tracks AOV by device (mobile users buy less? spend differently?)
- Flags high-traffic devices with low CVR (performance issue)
- Identifies browser-specific problems (Safari? Firefox?)

**Minimum data needed:** Traffic and conversion by device + browser

---

### 9. Weekly Ecommerce Summary
**What it does:** Top products, profit alerts, channel performance. One snapshot, all insights.

**Includes:**
- Top 5 products by profit this week
- Cart abandonment rate + revenue at risk
- Repeat purchase rate for this week's cohort
- Profitable vs unprofitable channels
- Conversion rate vs last week
- AOV trend + high-AOV products
- Recommended actions (pause, scale, test, fix)

**Minimum data needed:** Full Shopify/WooCommerce export (products, orders, customers, events)

---

## How to Use These Skills

1. **Identify the question** — Which products to scale? Where's the CVR bottleneck? Is this cohort profitable?
2. **Gather the data** — Product performance, customer data, channel data
3. **Run the relevant skill** — Get diagnosis + financial impact
4. **Take action** — Scale profitable products, pause unprofitable ones, fix high-abandonment

---

## Data Requirements by Source

| Skill | Shopify API | CSV Export | GA4 | Manual |
|---|---|---|---|---|
| Product Performance Ranker | ✅ | ✅ | ⚠️ (need revenue) | ✅ |
| Cart Abandonment Debugger | ✅ | ✅ | ✅ | ⚠️ |
| Customer Cohort Analyzer | ✅ | ✅ | ✅ | ✅ |
| Unit Economics Calculator | ✅ | ✅ | ❌ | ✅ (need COGS) |
| Channel Mix Optimizer | ✅ (w/ UTM) | ✅ | ✅ | ⚠️ |
| Conversion Rate Auditor | ✅ | ✅ | ✅ | ✅ |
| Promotional Impact Modeler | ✅ | ✅ | ✅ | ✅ |
| Device & Browser Analyzer | ❌ | ⚠️ | ✅ | ⚠️ |
| Weekly Ecommerce Summary | ✅ | ✅ | ✅ | ❌ |

✅ = works perfectly | ⚠️ = requires manual input or separate export | ❌ = not possible from this source

---

## Key Metrics Reference

| Metric | Definition | Good Benchmark |
|---|---|---|
| CVR (Conversion Rate) | Purchases ÷ Sessions | 1–3% (varies by category) |
| AOV (Average Order Value) | Total Revenue ÷ Orders | Varies by industry |
| ROAS | Revenue ÷ Ad Spend | ≥3.0 for profitability |
| LTV (Lifetime Value) | Total customer revenue over time | ≥3x CAC |
| Repeat Purchase Rate | Repeat customers ÷ Total customers | ≥20% is strong |
| Cart Abandonment | Abandons ÷ (Abandons + Purchases) | 50–80% is normal |
| Profit Margin | (Revenue − COGS − Fulfillment) ÷ Revenue | ≥30% healthy |
| CAC (Customer Acquisition Cost) | Ad Spend ÷ New Customers | ÷ LTV should be ≥3 |

---

## Output Format for Recommendations

```
### [Skill Name]: [Product/Channel/Cohort Name]

Finding:
[1–2 sentences describing the issue or opportunity]

Financial Impact:
| Metric | Current | Benchmark | Gap | Annual Impact |
|--------|---------|-----------|-----|---------------|
| ROAS | X | Y | $Z | $ABC |

Recommendation:
1. [Specific action with financial rationale]
2. [Specific action with financial rationale]
```

---

## When to Run Each Skill

| Situation | Use Skill | Timeline |
|---|---|---|
| Deciding which products to advertise | Product Performance Ranker | Weekly |
| Revenue is down | Conversion Rate Auditor | Immediately |
| Scaling one product | Cart Abandonment Debugger | Before scaling |
| New cohort acquired | Customer Cohort Analyzer | Every acquisition campaign |
| Want to discount | Promotional Impact Modeler | Before promotion |
| Checking profitability | Unit Economics Calculator | Weekly/Monthly |
| Comparing channels | Channel Mix Optimizer | Monthly |
| Mobile traffic is high | Device & Browser Analyzer | Monthly |
| Planning sprint | Weekly Ecommerce Summary | Every Monday |

---

## Common Guardrails

**Before scaling a product:**
- ✅ Confirm profit margin is positive (not just positive ROAS)
- ✅ Confirm inventory is sufficient
- ✅ Confirm repeat purchase rate (scaling one-time buyers is unprofitable)

**Before discounting:**
- ✅ Confirm baseline (non-discount) revenue and margin
- ✅ Calculate breakeven point (how many extra orders to justify discount?)
- ✅ Segment discount only to high-LTV cohorts

**Before pausing a channel:**
- ✅ Confirm it's truly unprofitable (not just high-LTV payback period)
- ✅ Confirm brand impact (organic traffic may suffer if you pause paid)

---

## Questions to Ask Yourself

- What's my most profitable product? Am I spending enough on it?
- Which cohort has the highest LTV? Can I find more customers like them?
- Is my CVR dropping? Is it a device issue or a general site problem?
- Are customers abandoning because of price, shipping cost, or something else?
- Which channel gives me the most repeat customers (not just first order)?

---

## Next Steps

1. Pull product-level data for last 30 days
2. Run Product Performance Ranker
3. Audit Unit Economics for top 5 products
4. Check Channel Mix + repurchase by channel
5. Fix highest-impact issue first (usually CVR or product selection)

