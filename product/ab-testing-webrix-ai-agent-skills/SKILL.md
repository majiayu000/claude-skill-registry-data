---
name: ab-testing
displayName: A/B Testing
tagline: Design, run, and analyze A/B tests for marketing campaigns and product features.
description: |
  Helps design statistically rigorous A/B tests for marketing campaigns,
  landing pages, and product features. Calculates required sample sizes,
  defines success metrics, sets up test variants, and analyzes results
  with confidence intervals. Prevents common testing mistakes like
  peeking and underpowered tests.
department:
  - Marketing
  - Product
  - Data & Analytics
use_cases:
  - Experimentation
  - Conversion Optimization
  - Campaign Optimization
tools_required:
  - Google Analytics MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Design an A/B test for our pricing page.
  Goal: increase trial signups by 15%.
  Current conversion rate: 3.2%.
exampleOutput: |
  A/B Test Plan — Pricing Page

  HYPOTHESIS
  Simplifying the pricing page from 4 tiers to 3 will increase
  trial signups by 15% (from 3.2% to 3.68%).

  TEST DESIGN
  Control (A):   Current 4-tier pricing page
  Variant (B):   Simplified 3-tier pricing page
  Metric:        Trial signup rate
  Traffic Split: 50/50

  SAMPLE SIZE
  Required:      12,400 visitors per variant
  Duration:      ~18 days (at 1,400 visitors/day)
  Confidence:    95%
  Power:         80%

  RESULTS (after 18 days)
  Control:   3.2% (398/12,438)
  Variant:   3.9% (487/12,487)
  Lift:      +21.9%  ✅ Statistically significant (p=0.003)
---

# A/B Testing

Design, run, and analyze A/B tests for marketing campaigns and product features.

**Integrations:** Google Analytics

## When to Use

- The user wants to test different versions of a page or campaign
- Data-driven decisions are needed for feature or design changes
- The user mentions "A/B test", "experiment", or "conversion optimization"

## Steps

### Step 1: Define Hypothesis

Formulate a testable hypothesis with expected outcome.

### Step 2: Calculate Sample Size

Determine required traffic and test duration for statistical significance.

### Step 3: Set Up Variants

Configure control and variant with tracking.

### Step 4: Analyze Results

Evaluate statistical significance and make recommendations.

## Output

Deliver:
- Test plan with hypothesis and sample size
- Variant configuration details
- Results analysis with confidence intervals
