---
name: funnel-analyzer
description: Analyze conversion funnel drop-offs and identify biggest leak points with impact-ranked recommendations
tags: [funnel, conversion, analytics, drop-off, optimization]
---

# Funnel Analyzer

Analyzes conversion funnel drop-offs by mapping the full customer journey from traffic source through purchase. Identifies the biggest leak points in the funnel, quantifies revenue impact, and recommends fixes ranked by potential uplift. Works with provided analytics data or estimates from page-level analysis when data is unavailable.

## Prerequisites

- `agency.config.json` at repo root with `services` and `icp` sections
- WebFetch tool available (for page analysis when no analytics data provided)
- Optional: Analytics data provided by user (GA4 export, Shopify analytics, or manual numbers)
- Optional: `cro-auditor` skill for detailed page-level optimization

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[].keywords` -- for CRO-relevant context
   - `icp.segments[]` -- audience context for funnel expectations
   - `case_studies[]` -- benchmark data from past work
3. Accept parameters:
   - `store_url` -- the store/site to analyze (required)
   - `analytics_data` -- structured funnel data if available (default: none, estimate from pages)
   - `funnel_type` -- type of funnel: `ecommerce | saas | lead_gen | content` (default: ecommerce)
   - `time_period` -- analysis period (default: "last 30 days")
   - `revenue_data` -- AOV, monthly revenue if available (default: estimate)
   - `traffic_sources` -- breakdown by source if available (default: estimate)

### Analytics data format (if provided):
```json
{
  "sessions": 10000,
  "unique_visitors": 8500,
  "product_page_views": 4200,
  "add_to_cart": 850,
  "reached_checkout": 420,
  "completed_purchase": 210,
  "average_order_value": 2500,
  "monthly_revenue": 525000,
  "traffic_sources": {
    "organic": 3500,
    "paid": 2800,
    "social": 1500,
    "direct": 1200,
    "referral": 500,
    "email": 500
  }
}
```

## Phase 1: Funnel Mapping

### Ecommerce funnel stages:
1. **Traffic** -- Sessions/visitors arriving at the site
2. **Landing** -- First meaningful page view (homepage, collection, product)
3. **Browse** -- Product page views (indicates interest)
4. **Add to Cart** -- Items added to cart (indicates intent)
5. **Initiate Checkout** -- Reached checkout page (indicates commitment)
6. **Payment** -- Entered payment details
7. **Purchase** -- Completed transaction

### If analytics data provided:
Map provided numbers directly to funnel stages. Calculate conversion rate between each consecutive stage.

### If no analytics data (estimation mode):
Use WebFetch on the store URL to analyze pages and estimate:

**Traffic estimation:**
- WebSearch: `"{store_url}" site traffic OR visitors` to find any published data
- WebSearch: `site:similarweb.com "{store_domain}"` for traffic estimates
- Check for review counts, social followers, and other public proxy signals

**Page analysis for friction estimation:**
- WebFetch homepage: Assess bounce risk (load time, clarity, CTA visibility)
- WebFetch a product page: Assess browse-to-cart friction (images, descriptions, reviews, price clarity, variant UX)
- WebFetch cart page: Assess cart-to-checkout friction (shipping info, trust signals, upsells)
- WebFetch checkout: Assess checkout friction (field count, payment options, guest checkout)

Apply industry benchmark rates where actual data is missing:
```json
{
  "ecommerce_benchmarks": {
    "landing_to_browse": "40-60%",
    "browse_to_add_to_cart": "15-25%",
    "add_to_cart_to_checkout": "40-60%",
    "checkout_to_purchase": "45-65%",
    "overall_conversion": "1.5-3.5%"
  }
}
```

## Phase 2: Drop-Off Analysis

For each funnel transition, calculate:

```json
{
  "stage_from": "Browse",
  "stage_to": "Add to Cart",
  "visitors_in": 4200,
  "visitors_out": 850,
  "conversion_rate": "20.2%",
  "drop_off_rate": "79.8%",
  "drop_off_count": 3350,
  "benchmark_rate": "20%",
  "performance_vs_benchmark": "AT_BENCHMARK | ABOVE | BELOW",
  "gap_percentage": "+0.2%",
  "revenue_impact_if_fixed": "Improving to 25% would yield Rs 131,250/month additional revenue"
}
```

### Revenue impact calculation:
For each stage, calculate the potential revenue from improving to benchmark or +5% above current:
- `additional_conversions = visitors_in * (target_rate - current_rate)`
- `additional_revenue = additional_conversions * downstream_conversion_rates * AOV`
- This gives a dollar/rupee value to each leak point.

### Leak severity classification:
- **CRITICAL LEAK**: Drop-off rate is 15%+ worse than benchmark AND revenue impact > 10% of monthly revenue
- **MAJOR LEAK**: Drop-off rate is 10-15% worse than benchmark OR revenue impact > 5% of monthly revenue
- **MINOR LEAK**: Drop-off rate is 5-10% worse than benchmark
- **HEALTHY**: Within or above benchmark

## Phase 3: Root Cause Analysis

For each CRITICAL and MAJOR leak, diagnose likely causes:

### Landing to Browse drop-off causes:
- Poor headline/hero messaging (no clear value prop above the fold)
- Slow page load (heavy images, unoptimized scripts)
- Navigation confusion (too many options, unclear categories)
- Irrelevant traffic (paid ads sending wrong audience)
- No social proof visible on landing page
- Mobile layout issues

### Browse to Add-to-Cart drop-off causes:
- Poor product images (few, low quality, no lifestyle shots)
- Unclear pricing or hidden costs
- Missing size/variant guidance
- No reviews or social proof on product page
- Weak product descriptions (features without benefits)
- Confusing variant selection UI
- No urgency elements (stock levels, shipping deadlines)

### Add-to-Cart to Checkout drop-off causes:
- Surprise shipping costs revealed in cart
- No guest checkout option
- Cart page lacks trust signals
- Aggressive upsells or distractions
- No order summary clarity
- Coupon field creates "let me go find a code" abandonment

### Checkout to Purchase drop-off causes:
- Too many form fields
- Limited payment options
- No trust badges or security indicators
- Mandatory account creation
- Shipping time uncertainty
- Return policy not visible

For each root cause, assign:
- `confidence`: HIGH (clearly visible on page) | MEDIUM (likely based on patterns) | LOW (speculative)
- `evidence`: What specifically indicates this cause

## Phase 4: Recommendations

For each identified leak, generate prioritized fixes:

```json
{
  "leak_stage": "Browse to Add to Cart",
  "recommendation": "Add customer reviews section below product images",
  "category": "social_proof",
  "expected_uplift": "3-5% improvement in add-to-cart rate",
  "revenue_impact": "Rs 37,500-62,500/month",
  "effort": "LOW | MEDIUM | HIGH",
  "priority_score": 8.5,
  "implementation_notes": "Use Shopify app (Judge.me or Loox) for review collection. Display star rating above fold, full reviews below.",
  "ab_test_suggestion": "Test with/without reviews for 2 weeks, minimum 500 visitors per variant"
}
```

### Priority scoring:
`priority_score = (expected_uplift_midpoint * revenue_multiplier) / effort_score`
- effort_score: LOW=1, MEDIUM=2, HIGH=3
- Revenue multiplier: scales impact relative to total monthly revenue

Sort recommendations by priority_score descending.

## Phase 5: Output

Return structured funnel analysis:

```json
{
  "analysis_summary": {
    "store_url": "https://...",
    "funnel_type": "ecommerce",
    "data_source": "provided | estimated",
    "time_period": "last 30 days",
    "overall_conversion_rate": "2.1%",
    "benchmark_conversion_rate": "2.5%",
    "estimated_monthly_revenue": 525000,
    "estimated_revenue_leakage": 75000
  },
  "funnel_stages": [
    {
      "stage": "Traffic",
      "visitors": 10000,
      "next_stage": "Browse",
      "conversion_rate": "42%",
      "drop_off_rate": "58%",
      "benchmark": "50%",
      "status": "MAJOR_LEAK",
      "revenue_impact": 52500
    }
  ],
  "leaks_ranked": [
    {
      "rank": 1,
      "stage": "Browse to Add to Cart",
      "severity": "CRITICAL",
      "current_rate": "15%",
      "benchmark_rate": "20%",
      "revenue_impact": 65000,
      "root_causes": [],
      "recommendations": []
    }
  ],
  "action_plan": {
    "immediate": ["Fix #1 leak with quick wins"],
    "this_month": ["Implement medium-effort fixes"],
    "next_quarter": ["Major redesign items"],
    "ongoing": ["A/B testing program"]
  }
}
```

Present formatted summary:

```
FUNNEL ANALYSIS: {store_url}
Period: {time_period} | Data: {source}

FUNNEL OVERVIEW:
Traffic:     {N} visitors
  |  {rate}% convert ({status})
Browse:      {N} product views
  |  {rate}% convert ({status})
Add to Cart: {N}
  |  {rate}% convert ({status})
Checkout:    {N}
  |  {rate}% convert ({status})
Purchase:    {N}

Overall: {rate}% (Benchmark: {benchmark}%)
Revenue leakage estimate: {amount}/month

BIGGEST LEAKS (by revenue impact):
1. [{severity}] {stage} -- {current_rate}% vs {benchmark}% benchmark
   Impact: {revenue}/month
   Root cause: {cause}
   Fix: {recommendation}
   Effort: {level} | Expected uplift: {range}

2. ...

QUICK WINS:
1. {recommendation} -- {revenue_impact} -- Effort: LOW

ACTION PLAN:
Immediate: {actions}
This month: {actions}
Next quarter: {actions}
```

## Example Usage

Trigger phrases:
- "Analyze the conversion funnel for [store URL]"
- "Where are we losing customers in the funnel?"
- "Find the biggest funnel leak points"
- "Run funnel analysis with this data: [paste analytics]"
- "What's causing cart abandonment?"
- "Estimate funnel drop-offs for [URL]"

```
User: Analyze the funnel for shop.kibisports.com
Assistant: [reads config, fetches key pages, estimates funnel metrics using benchmarks and page analysis, identifies leaks, calculates revenue impact, presents ranked recommendations]
```

```
User: Here's our GA4 data: [paste]. Find the biggest leaks.
Assistant: [maps provided data to funnel stages, calculates drop-offs vs benchmarks, identifies root causes, presents revenue-ranked fix list]
```
