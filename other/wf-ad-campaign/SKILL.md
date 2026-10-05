---
name: wf-ad-campaign
version: 1.0.0
description: "Launch a paid ad campaign from strategy through testing. Use when the user wants to create and run paid ads end-to-end. Also trigger when the user mentions 'ad campaign workflow,' 'launch ads,' 'set up a paid campaign,' 'ads end-to-end,' 'PPC workflow,' or 'paid ads from scratch.' For ad copy variations only, see ad-creative. For campaign strategy only, see paid-ads."
---

# Ad Campaign

End-to-end workflow: define targeting and budget, generate ad creative, set up tracking, and design the test plan.

## Stage 1: Campaign Strategy

Load and run the `paid-ads` skill to define:
- Campaign objective (awareness, traffic, leads, conversions)
- Target platforms (Google, Meta, LinkedIn, Twitter/X)
- Audience targeting (demographics, interests, custom audiences, retargeting)
- Budget and bid strategy
- Landing page(s)
- Success metrics and targets

**Gate:** User approves the campaign strategy before creating assets.

## Stage 2: Ad Creative

Load and run the `ad-creative` skill to generate:
- Headlines (multiple variations per platform)
- Descriptions / primary text
- Ad copy for each audience segment
- Platform-specific formatting (RSA for Google, carousel for Meta, etc.)
- Visual direction notes (for design handoff)

Generate at least 3-5 variations per ad group for testing.

Pass forward: campaign goals, audience segments, landing page, key messages.

**Gate:** User approves ad creative variations.

## Stage 3: Tracking Setup

Load and run the `tracking-setup` skill to configure:
- Conversion events (form fills, signups, purchases)
- Platform pixels and tags
- UTM parameter conventions for this campaign
- GA4 event configuration
- Attribution setup

**Gate:** User approves the tracking plan.

## Stage 4: Test Plan

Load and run the `ab-test-setup` skill to design:
- What to test first (headline, audience, creative, landing page)
- Test structure (A/B or multivariate)
- Sample size and duration estimates
- Statistical significance threshold
- Decision criteria (when to kill a variant, when to scale)

**Gate:** User approves the test plan.

## Summary

```
## Ad Campaign Complete

### Campaign: [name]
- Objective: [objective]
- Platforms: [list]
- Budget: [amount / period]
- Audience: [segments]

### Creative
- Headlines: [count] variations
- Descriptions: [count] variations
- Ad sets: [count] → [paths]

### Tracking
- Conversion events: [list]
- UTM convention: [pattern]
- Pixels configured: [platforms]

### Test Plan
- First test: [what's being tested]
- Duration: [estimate]
- Success metric: [metric and target]

### Launch Checklist
- [ ] Landing page live and tracking verified
- [ ] Ad creative uploaded to platforms
- [ ] Audiences configured
- [ ] Budget set
- [ ] Conversion tracking firing
- [ ] Test plan documented
- [ ] Launch!
```

## Output Structure

All files go into a single project folder:

```
marketing/ads/[campaign-slug]/
  strategy.md
  ad-creative.md
  tracking-plan.md
  test-plan.md
```

Derive `[campaign-slug]` from the campaign name or product focus. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Generate enough variations for meaningful testing (3-5 minimum per ad group)
- All ad copy must match the landing page messaging
- Budget recommendations should be realistic and justified
- If the user wants to skip a stage, skip it
- All output goes into the project folder, not scattered across `marketing/`
