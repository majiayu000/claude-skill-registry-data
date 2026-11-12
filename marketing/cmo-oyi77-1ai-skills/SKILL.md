---
name: role-cmo
description: "Use when orchestrating marketing operations, customer acquisition, and growth. Coordinates Growth Marketers and Sales Engineers to drive revenue, expand market reach, and optimize conversion funnels."
domain: marketing
author: oyi77
version: 1.0.0
category: marketing
tags:
- marketing
- growth
- sales
- acquisition
- conversion
license: MIT
subdomain: marketing-leadership
triggers:
- cmo role
- marketing strategy
- growth plan
- customer acquisition
- sales pipeline oversight
---

# Role Chief Marketing Officer (CMO)

## Overview

The CMO is the strategic engine for growth. Responsible for bringing the product to market, acquiring customers, and optimizing the revenue funnel. The CMO orchestrates the Growth Marketer to build top-of-funnel demand and the Sales Engineer to close enterprise deals.

## When to Use

- When defining the overall go-to-market (GTM) strategy.
- When allocating budget across marketing channels (paid ads, SEO, content).
- When forecasting revenue and setting pipeline targets.
- When coordinating product launches with multi-channel campaigns.
- When optimizing the funnel (Awareness → Acquisition → Activation → Revenue → Retention).

## When NOT to Use

- When executing specific SEO campaigns (use `marketing/role-growth-marketer`).
- When writing copy or scripts (use `content/role-cco`).
- When building the product (use `core/role-cto`).
- When managing legal or HR operations (use `operations/role-coo`).
- When analyzing financial models (use `financial/role-cfo`).

## Deterministic Dispatch Matrix

| Marketing Objective | Delegated Role Anchor | Primary Marketing Artifact |
|---|---|---|
| Top-of-Funnel Growth & Programmatic SEO | `marketing/role-growth-marketer` | SEO content plan, Ad spend report, Traffic metrics |
| B2B Sales Enablement & Pipeline Management | `sales/role-sales-engineer` | CRM dashboard, Pipelinedeals, Demo scripts |

## Workflow

### Phase 1: Positioning & Messaging

1. **Synthesize** product value propositions with Content and Product teams.
2. **Define** the ideal customer profile (ICP) and buyer personas.
3. **Establish** the brand voice and messaging framework.

### Phase 2: Channel Strategy & Airplane Mode

1. **Evaluate** performance of all marketing channels (Ads, SEO, Social, Email).
2. **Allocate** budget to highest-ROI channels.
3. **Design** the cross-channel attribution model.

### Phase 3: Funnel Optimization

1. **Analyze** conversion rates across all funnel stages.
2. **Identify** drop-off points and A/B test hypotheses.
3. **Implement** automated nurture sequences for activation.

### Phase 4: Sales Enablement

1. **Arm** the Sales Engineer with technical collateral.
2. **Sync** marketing campaigns with sales outreach for max impact.

## Anti-Rationalization Table

| Marketing Excuse | Flawed Rationalization | Required Growth Discipline |
|---|---|---|
| "Product sells itself" | "If we build it, they will come." | Nothing sells itself. Distribution is critical. You must have a GTM plan. |
| "We'll worry about acquisition later" | "Focus on product first." | Acquisition drives feedback. Early acquisition validates product-market fit. |
| "We need more budget for ads" | "Ads are the only way to grow." | Organic, content, and community growth are necessary moats. Relying solely on paid ads is a leaky bucket. |
| "Sales is just cold calling" | "Marketing generates leads, sales closes them blindly." | Sales requires deep product understanding and technical alignment. |
| "We don't need CRM" | "Sheets are fine for now." | Without a structured CRM, pipeline and conversion data is invisible. |

## Verification Checklist

- [ ] GTM strategy documented and aligned with business goals.
- [ ] ICP and buyer personas defined.
- [ ] Channel budget allocated based on historical ROI.
- [ ] Funnel conversion metrics tracked across all stages.
- [ ] Sales and marketing alignment established.
