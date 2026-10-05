---
name: customer-segmentation
displayName: Customer Segmentation
tagline: Segment customers by behavior, purchase history, and lifetime value for targeted marketing.
description: |
  Creates customer segments based on purchase behavior, engagement patterns,
  and lifetime value. Implements RFM (Recency, Frequency, Monetary) analysis
  and behavioral cohorts. Enables targeted marketing campaigns, personalized
  recommendations, and churn prediction for each segment.
department:
  - E-commerce
  - Marketing
  - Data & Analytics
use_cases:
  - Customer Analytics
  - Personalization
  - Retention Marketing
tools_required:
  - Shopify MCP
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
  Segment our Shopify customers by purchase behavior.
  Use RFM analysis. Identify VIPs and at-risk customers.
exampleOutput: |
  Customer Segmentation — RFM Analysis

  SEGMENTS (4,200 total customers)
  Champions (8%):      340 customers — High R, High F, High M
    Avg LTV: $1,240   Action: VIP rewards, early access
  Loyal (15%):         630 customers — Med R, High F, Med M
    Avg LTV: $680     Action: Loyalty program, upsell
  At Risk (12%):       504 customers — Low R, Med F, Med M
    Avg LTV: $420     Action: Win-back campaign, survey
  New (20%):           840 customers — High R, Low F, Low M
    Avg LTV: $85      Action: Onboarding sequence, welcome offer
  Dormant (45%):       1,886 customers — Low R, Low F, Low M
    Avg LTV: $45      Action: Re-engagement or sunset

  KEY INSIGHTS
  - Champions generate 35% of revenue (8% of customers)
  - 504 at-risk customers represent $211K in potential churn
  - New customer conversion to Loyal: 22% within 90 days
---

# Customer Segmentation

Segment customers by behavior, purchase history, and lifetime value for targeted marketing.

**Integrations:** Shopify

## When to Use

- The user wants to segment customers for targeted campaigns
- Customer lifetime value analysis is needed
- The user mentions "customer segmentation", "RFM", or "cohort analysis"

## Steps

### Step 1: Pull Customer Data

Extract purchase history, engagement data, and customer attributes.

### Step 2: Apply RFM Analysis

Score customers on recency, frequency, and monetary value.

### Step 3: Define Segments

Create actionable segments with recommended marketing strategies.

## Output

Deliver:
- Customer segments with counts and characteristics
- Recommended actions per segment
- LTV analysis and churn risk assessment
