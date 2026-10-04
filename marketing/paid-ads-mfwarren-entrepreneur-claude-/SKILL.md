---
name: paid-ads
version: 1.0.0
category: Marketing & Growth
domain: paid-advertising
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "ad copy"
  - "Facebook ad"
  - "Meta ad"
  - "Google ad"
  - "paid ads"
  - "ad creative"
  - "A/B test ads"
  - "ad headline"
  - "ad campaign"
tools: []
---

# Paid Ads

Meta Ads and Google Ads creative, copy, A/B test variants, and performance analysis frameworks.

## Purpose

Create high-converting ad copy and creative briefs for paid acquisition channels. Focus on hook, offer, and CTA — the three elements that determine ad performance.

## Workflow

### Step 1: Gather Context
- Platform: Meta (Facebook/Instagram), Google Search, Google Display
- Campaign objective: awareness, traffic, leads, conversions
- Product/offer being advertised
- Target audience (demographics, interests, pain points)
- Budget range and current performance (if running ads)
- Landing page URL

### Step 2: Ad Copy Creation

**Meta Ads (Facebook/Instagram):**
- Primary text: Hook → problem → solution → CTA (125 chars above fold)
- Headline: Under 40 chars, benefit-focused
- Description: Supporting detail, under 30 chars
- Generate 5 variants for A/B testing

**Google Search Ads:**
- Headlines (up to 15): 30 chars each, keyword-rich
- Descriptions (up to 4): 90 chars each
- Include numbers, benefits, and CTAs
- Match search intent

### Step 3: A/B Test Matrix
- Test one variable at a time: hook, offer, CTA, audience
- Provide 3-5 variants of each element
- Recommend test duration and budget allocation

### Step 4: Creative Brief (for designers)
- Visual direction: what the image/video should show
- Text overlay (if any)
- Format specs per placement
- Reference examples (describe, don't link)

## Output Format
```markdown
## Ad Campaign: [Product/Offer]

### Meta Ads — Variant Set
| # | Primary Text | Headline | CTA |
|---|-------------|----------|-----|
| 1 | [text] | [headline] | [cta] |

### Google Search Ads
**Headlines:** [list]
**Descriptions:** [list]

### A/B Test Plan
[Test matrix]
```

## Constraints
- Follow platform ad policies (no prohibited claims)
- Never make health, income, or guarantee claims that can't be substantiated
- Headlines must be under character limits
- Always note that ads need creative assets the user must provide
