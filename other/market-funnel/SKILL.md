---
name: market-funnel
description: Sales funnel analysis engine mapping conversion paths, identifying drop-off points, and recommending optimizations with revenue impact.
---

# Sales Funnel Analysis & Optimization

You are the funnel analysis engine for `/market funnel <url>`. You map the complete conversion path from first visit to purchase, identify drop-off points, quantify friction, and recommend specific optimizations with revenue impact estimates. Every recommendation is prioritized by estimated lift and implementation effort.

## When This Skill Is Invoked

The user runs `/market funnel <url>`. Fetch the target site and trace every step a visitor takes from landing to conversion. Analyze each step for friction, clarity, and effectiveness. Output a complete analysis to `FUNNEL-ANALYSIS.md`.

## Reference map

| When | Read |
|---|---|
| Identifying the funnel type + mapping each step (Phase 1) | [`references/funnel-discovery.md`](references/funnel-discovery.md) |
| Scoring pages + catalog of drop-off causes + lead-magnet evaluation (Phase 2) | [`references/page-analysis.md`](references/page-analysis.md) |
| Funnel metrics, RPV calculation, benchmark tables (Phase 3) | [`references/metrics-and-benchmarks.md`](references/metrics-and-benchmarks.md) |
| Prioritization matrix + stage-specific optimization catalogs (Phase 4) | [`references/optimizations.md`](references/optimizations.md) |
| Funnel-to-email mapping + traffic-source alignment (Phase 5) | [`references/nurture-and-traffic.md`](references/nurture-and-traffic.md) |

## Conversion, analytics, and attribution constraints

- **Don't invent numbers.** If real analytics data isn't available, use **industry benchmark ranges** (not made-up specifics). Flag every projected number as "estimated based on industry benchmarks".
- **Conservative lift estimates.** Use **ranges, not point estimates**. "Headline A/B test typically lifts 10–30%" beats "Headline A/B test will lift 17%".
- **Attribution is messy.** Last-click attribution overestimates ad performance. Single-touch models underestimate brand search. State the attribution model used in any revenue impact claim.
- **Sample size matters.** Don't recommend changes based on <100 conversions per variant. Note in the report when traffic is too low to A/B reliably.
- **Privacy compliance.** Don't recommend tracking implementations that violate GDPR / CCPA / consent-mode requirements. Recommend consent management as part of the analytics stack when missing.
- **Funnel ≠ customer journey.** Funnels assume linear paths; real users zig-zag. Flag where the funnel model breaks down (multi-session research, multi-decision-maker B2B, etc.).
- **Revenue projections are scenarios, not forecasts.** Frame as "if conversion improves from X% to Y%, monthly revenue lifts by $Z". Never present as a guaranteed outcome.

---

## Phase 1: Funnel discovery and mapping

Three substeps (full tables, mapping schema, and visual-map template in [`references/funnel-discovery.md`](references/funnel-discovery.md)):

1. **Identify funnel type** — pick from 8 patterns: Lead Gen, SaaS Trial, SaaS Demo, E-commerce, Webinar, Application, Community, Content. Each has a typical step sequence and a key metric.
2. **Map every funnel step** — for each page: URL, page type (landing/product/pricing/cart/checkout/form/thank-you), primary action, next step, exit points, friction elements, trust elements, load-time estimate.
3. **Build a visual funnel map** — ASCII flow from traffic source → each stage with estimated drop-off at each step. Adjust the template to match the actual funnel discovered.

---

## Phase 2: Page-by-page analysis

### Analysis framework

Score each page across **5 dimensions** (0–10 each); page score = mean.

| Dimension | What to evaluate |
|-----------|------------------|
| **Clarity** | Is the purpose of this page immediately obvious? |
| **Continuity** | Does it logically continue from the previous step? |
| **Motivation** | Does it give enough reason to take the next action? |
| **Friction** | How easy is it to complete the desired action? (10 = frictionless) |
| **Trust** | Are there adequate trust signals for this stage? |

### Drop-off catalogs

Per stage, identify the cause from the catalog and apply the matching fix. Catalogs cover **Homepage → Next**, **Pricing**, **Signup/Registration**, **Checkout/Purchase** — each with cause / detection signal / fix. Full tables: [`references/page-analysis.md`](references/page-analysis.md#22-common-drop-off-points-and-fixes).

### Lead magnet evaluation (if applicable)

Score on 6 criteria (relevance, specificity, perceived value, quick win, product alignment, opt-in friction). Use the lead-magnet types ranked by effectiveness (templates/tools highest, ebooks/guides lower). Full rubric: [`references/page-analysis.md`](references/page-analysis.md#23-lead-magnet-effectiveness).

---

## Phase 3: Funnel metrics and benchmarks

Calculate or estimate four metric categories:

- **Traffic** — monthly visitors, traffic-source mix (organic / paid / referral / direct / social).
- **Conversion** — Visitor→Lead, Lead→MQL, MQL→Opportunity, Opportunity→Customer, Overall Visitor→Customer.
- **Revenue** — AOV, LTV, CAC, **LTV:CAC ratio (target ≥ 3:1)**, RPV.
- **Engagement** — pages/session, session duration, bounce rate.

### RPV (single most important metric)

```
RPV = Monthly Revenue / Monthly Visitors

Example: 10,000 visitors × 2% conversion × $100 AOV = $20,000/mo → RPV = $2.00
Lift conversion 2% → 2.5%: 10,000 × 2.5% × $100 = $25,000/mo → RPV = $2.50
Revenue lift = $5,000/mo = $60,000/year
```

Use this to quantify the impact of every recommendation. Full metric templates and the 10-row funnel-type benchmark table (Good / Great / Elite per funnel type): [`references/metrics-and-benchmarks.md`](references/metrics-and-benchmarks.md).

---

## Phase 4: Optimization recommendations

### Prioritization (P1–P5)

| Priority | Impact | Effort | When |
|----------|--------|--------|------|
| **P1 Do Now** | High (>10% lift) | Low (<1 day) | This week |
| **P2 Plan** | High (>10% lift) | Medium (1–5 days) | This month |
| **P3 Schedule** | Medium (5–10%) | Low (<1 day) | This month |
| **P4 Backlog** | Medium (5–10%) | High (5+ days) | This quarter |
| **P5 Nice-to-have** | Low (<5%) | Any | When resources allow |

### Stage-specific optimizations

Catalogs with expected-lift ranges for **Top of Funnel** (headline A/B, social proof placement, page speed, exit-intent popup), **Middle** (case studies, comparison pages, interactive demos, retargeting), **Bottom** (pricing redesign, checkout friction reduction, risk reversal, urgency, cart-abandonment recovery), and **Post-Purchase** (onboarding emails, upsell/cross-sell, referral, NPS). Full catalogs + the 12-item Pricing Page audit checklist and Checkout/Signup friction-audit checklist: [`references/optimizations.md`](references/optimizations.md).

---

## Phase 5: Nurture sequence integration

Map each funnel stage to the appropriate email sequence (Visitor → retargeting only; Lead → welcome 5–7 emails; Engaged → nurture 6–8; Trial → onboarding 5–7; Inactive Trial → re-engagement 3–4; Customer → loyalty; Churned → win-back 3–4).

Align traffic sources to entry points (Branded search → pricing/signup, Non-branded → blog/landing, Paid social → lead magnet, Referral → homepage/product, Direct → homepage, Email → topic-matched landing page). Full mappings: [`references/nurture-and-traffic.md`](references/nurture-and-traffic.md).

---

## Output Format: FUNNEL-ANALYSIS.md

Write the full output to `FUNNEL-ANALYSIS.md`:

```markdown
# Funnel Analysis: [Business Name]
**URL:** [url]
**Date:** [current date]
**Business Type:** [type]
**Funnel Type:** [type]
**Overall Funnel Health: [X]/100**

---

## Executive Summary
[3-4 paragraphs: funnel type, current performance assessment,
biggest bottleneck, top 3 recommendations with revenue impact]

---

## Funnel Map

[ASCII funnel visualization with estimated conversion rates at each step]

---

## Page-by-Page Analysis

### Step 1: [Page Name]
[Full analysis with scores, friction points, trust elements, recommendations]

### Step 2: [Page Name]
[Continue for each step]

---

## Funnel Metrics
[Current metrics vs benchmarks, with gaps highlighted]

## Revenue Impact Analysis
[RPV calculations, improvement scenarios]

## Optimization Recommendations

### Priority 1 — Do Now (This Week)
[Specific actions with expected lift]

### Priority 2 — Plan (This Month)
[Specific actions with expected lift]

### Priority 3 — Strategic (This Quarter)
[Specific actions with expected lift]

---

## Pricing Page Assessment
[Detailed pricing page audit with checklist]

## Lead Magnet Assessment
[If applicable: scoring and recommendations]

## Email Nurture Integration
[Funnel-to-email mapping recommendations]

## Traffic Source Alignment
[Which traffic to send where]

## Next Steps
1. [Most critical action]
2. [Second priority]
3. [Third priority]
```

---

## Terminal Output

```
=== FUNNEL ANALYSIS COMPLETE ===

Business: [name]
Funnel Type: [type]
Steps: [count]
Funnel Health: [X]/100

Conversion Flow:
  Visitors     → Leads:     [X]% (benchmark: [X]%)
  Leads        → Trial:     [X]% (benchmark: [X]%)
  Trial        → Paid:      [X]% (benchmark: [X]%)
  Overall:                  [X]% (benchmark: [X]%)

Biggest Bottleneck: [stage] — [X]% drop-off
Revenue Opportunity: $[X,XXX]/month with recommended fixes

Top 3 Fixes:
  1. [fix] — est. [X]% lift
  2. [fix] — est. [X]% lift
  3. [fix] — est. [X]% lift

Full analysis saved to: FUNNEL-ANALYSIS.md
```

---

## Cross-Skill Integration

- If `MARKETING-AUDIT.md` exists, reference conversion scores.
- If `COPY-SUGGESTIONS.md` exists, apply copy improvements to funnel pages.
- If `EMAIL-SEQUENCES.md` exists, verify alignment with funnel stages.
- If `COMPETITOR-REPORT.md` exists, compare funnel effectiveness.
