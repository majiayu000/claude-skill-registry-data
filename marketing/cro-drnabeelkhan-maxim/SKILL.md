---
skill_id: marketing-cro
name: Conversion Rate Optimization
version: 1.0.0
parent: marketing
office: CMO
reads_first: MARKETING-CONTEXT.md
triggers:
  - conversion
  - CRO
  - landing page optimization
  - signup flow
  - A/B test
  - conversion rate
  - funnel optimization
  - checkout optimization
  - form optimization
---

# Conversion Rate Optimization

> **Before starting:** Read `MARKETING-CONTEXT.md` in this domain for product, ICP, and positioning context.

## What This Skill Does

Systematically audits and optimizes conversion points across the entire funnel -- landing pages, signup flows, checkout processes, and onboarding sequences. Applies behavioral science (loss aversion, social proof, friction reduction) to every recommendation. Produces prioritized, testable hypotheses rather than opinion-based changes.

## Key Questions to Ask

1. What is the current conversion rate and what is the target?
2. Where in the funnel is the biggest drop-off?
3. What has already been tested (and what were the results)?
4. What is the primary CTA and does it match the ICP's desired outcome?
5. Is there existing analytics data (heatmaps, session recordings, funnel reports)?

## Framework / Approach

### Systematic Page Audit (for each conversion point)

1. **Hero Section** -- Does the headline match the visitor's intent? Is the value proposition clear within 5 seconds? Does the hero image support or distract?
2. **CTA Clarity** -- Is there one primary CTA? Is it above the fold? Does the button copy describe the outcome (not the action)?
3. **Social Proof** -- Are testimonials specific (name, role, metric)? Are logos relevant to the ICP? Is proof placed near decision points?
4. **Objection Handling** -- Are the top 3 objections addressed before the CTA? Is there a risk reversal (guarantee, free trial, no credit card)?
5. **Friction Points** -- How many form fields? How many steps to convert? Are there unnecessary distractions or navigation leaks?
6. **Trust Signals** -- Security badges, privacy statements, known-brand associations placed at friction points?

### Prioritization (ICE Framework)

For each hypothesis:
- **Impact** (1-10): How much will this move the conversion rate?
- **Confidence** (1-10): How certain are we based on data/best practices?
- **Ease** (1-10): How fast can we implement and test?

### Testing Protocol

- Define control vs. variant clearly
- Set minimum sample size before launching
- Run for at least 1 full business cycle (7 days minimum)
- Measure primary metric + guard-rail metrics
- Document learnings regardless of outcome

## Output Format

```markdown
## CRO Audit: [Page/Flow Name]

### Current State
- Conversion rate: [X%]
- Traffic source: [organic/paid/direct]
- Key drop-off: [where]

### Findings
| Element | Issue | Severity | Recommendation |
|---|---|---|---|
| Hero headline | Doesn't match search intent | High | Rewrite to mirror ICP pain point |
| ... | ... | ... | ... |

### Prioritized Hypotheses
| # | Hypothesis | ICE Score | Expected Lift |
|---|---|---|---|
| 1 | [If we X, then Y because Z] | [score] | [estimate] |
| ... | ... | ... | ... |

### Test Plan
- Variant description: [what changes]
- Success metric: [primary KPI]
- Sample size needed: [N]
- Estimated run time: [days]
```

## Related Skills
- `copywriting` -- headline and CTA copy optimization
- `paid-measurement` -- attribution and analytics for conversion tracking
- `growth-retention` -- post-conversion activation and retention
- `customer-research` -- qualitative insights to inform hypotheses

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
