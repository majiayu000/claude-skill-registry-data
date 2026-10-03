---
name: cro-optimizer
description: "CRO specialist that pulls live analytics data via the Humblytics MCP, analyzes conversion funnels, identifies drop-off points, and generates prioritized A/B test hypotheses. Use when analyzing conversion rates, diagnosing funnel leaks, optimizing signup flows, or creating test roadmaps. Triggers: CRO, conversion rate, funnel analysis, drop-off, optimize conversions, test hypothesis."
metadata:
  version: 1.0.0
  author: Humblytics
---

# CRO Optimizer

## Purpose

Analyze conversion funnels using live Humblytics analytics (via the Humblytics MCP), identify the highest-impact drop-off points, and generate prioritized A/B test hypotheses with expected conversion-rate / volume impact. This skill turns raw analytics into a ranked optimization roadmap.

## When to Use

- Diagnosing why a funnel is underperforming
- Identifying the biggest conversion bottleneck across a user journey
- Generating a prioritized list of A/B test ideas
- Preparing a CRO sprint plan or quarterly optimization roadmap
- Analyzing page-level or step-level drop-off rates
- Comparing conversion performance across segments (device, source, geography)

## Credentials

Live data comes from the **Humblytics MCP** (server `humblytics`). Connect it once — see the repo README — and this skill calls `mcp__humblytics__*` tools directly. No API keys, base URLs, or `.env` plumbing live in the skill.

- **Never paste API keys into chat** — they persist in transcripts and logs. Your key lives in the MCP connection headers, set once at connect time, and is never committed to the repo.
- **Property**: the MCP auto-resolves your property for a single-property key (the common case). For a multi-property key, call `list_properties` and pass the `propertyId` you want to analyze.
- **Docs**: https://docs.humblytics.com/api

## Before You Start

1. **Confirm the property** — The MCP auto-resolves the property for a single-property key. If the key covers multiple properties, call `list_properties` and confirm which one to analyze.
2. **Identify the funnel** — Clarify which conversion flow to examine (e.g., homepage > pricing > signup > onboarding)
3. **Check for context** — Look for existing project docs, AGENTS.md, or product briefs that describe the business model, target audience, and current conversion goals
4. **Establish the time range** — Default to last 30 days; ask if the user wants a different window
5. **Confirm MCP access** — Verify the Humblytics MCP (server `humblytics`) is connected before pulling data

## Core Workflow

### Step 1: Pull Funnel Data

Live data comes from the Humblytics MCP — the relevant tools here are `get_pages_breakdown`, `get_page_details`, `query_funnel`, `get_funnel_sankey`, `get_forms_breakdown`, and `get_clicks_details`. Retrieve:

- **Page views and sessions** for each step in the funnel
- **Event data** for key conversion actions (signups, clicks, form submissions)
- **Device and source breakdowns** to identify segment-specific issues
- **Scroll depth via `get_page_details`** and **click density via `get_clicks_details`** (there is no heatmap tool) for high-traffic pages

The analytics tools take `start`, `end` (ISO-8601), and `timezone`:

- `get_pages_breakdown` — Page-level traffic across the site
- `get_page_details` (`page: "/path"`) — Single-page deep dive (UTM, device, country breakdowns, scroll depth)
- `query_funnel` (`steps: [{ page: "/" }, ...]`) — Funnel step data. Optional: `mode: "unbounded" | "sequential"`, `breakdownBy`
- `get_funnel_sankey` (same `steps`) — Sankey path diagram for the same funnel

> **Fallback when funnels are down.** `query_funnel` and `get_funnel_sankey` can return HTTP 500. If they fail, approximate the funnel from the tools that do work: pull per-step page volume from `get_pages_breakdown` (and `get_funnel_suggestions` with `page: "/path"` for the ranked next-page sequence), and pull conversion-event volume for the final step(s) from `get_forms_breakdown`. Compute step-to-step conversion / drop-off from these `unique_sessions` (pages) and submission counts (forms). Note in your output that the funnel is an approximation from page + form breakdowns because the native funnel tool was unavailable.
- `get_forms_breakdown` and `get_forms_details` (`page: "/path"`) — Form/conversion event data (there is no generic `events` tool)
- `get_clicks_details` (`page: "/path"`) — Click heatmap data for a specific page (no heatmap tool exists; click data is the closest analogue)
- `get_clicks_breakdown` — Cross-page click comparison

### Step 2: Map the Funnel

Build a complete picture of the user journey:

```
Traffic Source → Landing Page → Key Action → Conversion → Retention
```

For each step, calculate:
- **Volume**: How many users reach this step
- **Conversion rate**: Percentage who proceed to the next step
- **Drop-off rate**: Percentage who abandon at this step
- **Absolute drop-off**: Raw number of users lost

### Step 3: Identify the Biggest Leak

Apply the **Largest Leak First** principle:

1. Calculate the absolute number of users lost at each step
2. Rank steps by absolute drop-off (not percentage)
3. The step losing the most users in absolute terms is your highest-priority optimization target

Why absolute over percentage: A 50% drop-off at a step with 100 visitors loses 50 people. A 10% drop-off at a step with 10,000 visitors loses 1,000 people. Fix the 1,000-person leak first.

### Step 4: Diagnose Root Causes

For each high-drop-off step, investigate:

- **Page load time** — Slow pages kill conversions. Check if the step has performance issues.
- **Mobile vs desktop** — Is the drop-off concentrated on mobile? Layout/UX issue.
- **Traffic source** — Do certain acquisition channels show higher drop-off? Expectation mismatch.
- **Scroll depth** — Are users seeing the CTA? Check scroll depth via `get_page_details` and click density via `get_clicks_details` (there is no heatmap tool).
- **Click patterns** — Are users clicking non-interactive elements? Confusing UI.
- **Form fields** — For forms, which field has the highest abandonment rate?

When the leak appears concentrated in **paid traffic** (drop-off significantly worse for `utm_source=google` or `utm_source=facebook` than for organic), call `get_ads_attribution` (`startDate`, `endDate` as `YYYY-MM-DD`) to see which specific campaigns are landing on the underperforming page. A creative/landing-page mismatch on one campaign can drag down a whole step's conversion rate. Hand off to `revenue-attributor` for the full ROAS picture or `ad-expert` to fix the creative.

### Step 5: Generate Test Hypotheses

For each identified issue, create a hypothesis using the ICE framework:

**Format:**
```
IF we [change], THEN [metric] will [improve/increase/decrease]
BECAUSE [evidence from data]

Impact: [1-10] — How much will this move the needle?
Confidence: [1-10] — How sure are we this will work?
Ease: [1-10] — How quickly can we implement and test this?
ICE Score: [average of three]
```

### Step 6: Prioritize and Recommend

Rank all hypotheses by ICE score and present:

1. **Top 3 Quick Wins** — High ease, decent impact (ship this week)
2. **Top 3 High-Impact Tests** — High impact, may require more effort (sprint backlog)
3. **Strategic Bets** — Lower confidence but potentially transformative (quarterly roadmap)

For each recommendation, include:
- The specific page or funnel step
- What to change and why
- Expected impact on conversion rate
- Suggested test duration based on traffic volume

## Analysis Frameworks

### The RICE Prioritization (for larger teams)

- **Reach**: How many users per month does this affect?
- **Impact**: Expected lift (minimal / low / medium / high / massive)
- **Confidence**: Data quality supporting the hypothesis (low / medium / high)
- **Effort**: Engineering/design time (days)

Score = (Reach x Impact x Confidence) / Effort

### Segment Analysis Checklist

Always break down conversion data by:
- Device type (mobile / desktop / tablet)
- Traffic source (organic / paid / direct / referral / social)
- Geography (if international)
- New vs returning visitors
- Entry page

### Common Funnel Archetypes

| Funnel Type | Key Metrics | Common Leaks |
|------------|-------------|--------------|
| SaaS Free Trial | Visit > Signup > Activate > Convert | Signup form friction, activation failure |
| E-commerce | PDP > Cart > Checkout > Purchase | Cart abandonment, checkout form |
| Lead Gen | Landing > Form > Thank You | Form length, trust signals |
| Content > Conversion | Blog > CTA > Signup | CTA visibility, relevance match |

## Output Format

Present findings as:

1. **Funnel Overview** — Visual step-by-step with volumes and rates
2. **Key Finding** — The single biggest insight in one sentence
3. **Drop-off Analysis** — Ranked list of leaks with absolute numbers
4. **Root Cause Diagnosis** — What is causing each major leak
5. **Prioritized Test Roadmap** — ICE-scored hypotheses ready for execution
6. **Expected Impact** — If top 3 tests succeed, projected conversion lift

## Related Skills

- **ab-test-generator** — Take the hypotheses from this skill and generate actual test configurations
- **funnel-reporter** — Pull comprehensive funnel reports with traffic & conversion volume (revenue only if a Stripe/ChartMogul revenue connector is attached)
- **page-cro** — Deep-dive into a specific page's conversion issues
- **copywriting** — Generate optimized copy for test variants

## Shared Frameworks (REQUIRED reading)

Before producing recommendations, anchor your analysis against the shared primitives in `skills/_shared/`. Skipping these is the #1 cause of generic, low-confidence output.

- **`_shared/frameworks/preflight-checklist.md`** — five context items to verify before scoring (URL, time range, goal, vertical, statistical reachability). If anything's missing AND would change the recommendation, ask one focused question; otherwise state assumptions explicitly.
- **`_shared/frameworks/largest-leak-first.md`** — rank by absolute people lost, not by percentage drop. A 10% drop on 10,000 visitors outranks a 50% drop on 100. Always compute absolute loss per step before applying ICE.
- **`_shared/frameworks/percentile-framing.md`** — report current metrics against vertical p25/p50/p75 bands from `_shared/benchmarks/baselines.json`. Replace "your CVR is low" with "your CVR is at p35 — meaningful headroom to p50".
- **`_shared/frameworks/ice-confidence-rubric.md`** — anchor ICE.Confidence on evidence quality, not familiarity. 9–10 = ≥2 sources with n≥1000 in target vertical; 5–6 = general best practice; 1–3 = directional hunch.
- **`_shared/frameworks/anti-patterns.md`** — counter-evidence for canon advice (customer logos LOST in most DoWhatWorks tests, "free" CTAs lose −16.8% platform-wide on Unbounce, hero video net-negative on mobile, etc.). Read before recommending the "best practice" version of any well-known pattern.
- **`_shared/frameworks/base-rate-priors.md`** — realistic priors: only ~14% of CTA tests reach significance; ~31% of headline rewrites beat control. Anchor expectations against base rates, not best-case outliers.
- **`_shared/benchmarks/patterns.json`** — 54 curated patterns with cited lift ranges, prerequisites, anti-patterns. When recommending a change, find the matching `pattern_id` and quote `evidence[].lift_range_pct` instead of guessing.
