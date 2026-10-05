---
name: wf-campaign-launch
version: 1.0.0
description: "Plan and execute a multi-channel marketing campaign. Use when the user wants to launch a campaign, coordinate across channels, or run a full go-to-market push. Also trigger when the user mentions 'launch campaign,' 'campaign workflow,' 'multi-channel launch,' 'GTM campaign,' 'full campaign,' or 'coordinate a launch.' For product launch strategy only, see launch-strategy. For ads only, see paid-ads."
---

# Campaign Launch

End-to-end workflow: plan the campaign, write the core messaging, then build out email, social, and ad assets with tracking.

## Stage 1: Campaign Strategy

Load and run the `launch-strategy` skill to define:
- Campaign goals and success metrics
- Target audience segments
- Channel strategy (which channels, in what order)
- Timeline and phases
- Key messages per phase

Then write the campaign brief using [references/campaign-brief.md](references/campaign-brief.md) (brief structure, channel mix by campaign type, KPI framework).

**Gate:** User approves the campaign brief before creating assets.

## Stage 2: Core Messaging

Load and run the `copywriting` skill to write:
- Campaign headline and tagline
- Core value proposition for this campaign
- Key proof points and supporting messages
- Landing page copy (if needed)

**Gate:** User approves the messaging foundation.

## Stage 3: Email Sequence

Load and run the `email-sequence` skill to build:
- Launch announcement email
- Follow-up nurture sequence (2-5 emails depending on campaign)
- Segmentation recommendations

Pass forward: campaign goals, audience segments, key messages, timeline.

**Gate:** User approves the email sequence.

## Stage 4: Social Content

Load and run the `social-content` skill to create:
- Platform-specific posts for each campaign phase
- Launch day posts
- Ongoing promotion posts
- Employee advocacy posts (if applicable)

Pass forward: campaign messaging, timeline, key dates.

**Gate:** User approves social content.

## Stage 5: Ad Creative

Load and run the `ad-creative` skill to generate:
- Headlines and descriptions for each target platform
- Multiple variations for testing
- Audience-specific messaging variants

Pass forward: campaign goals, audience segments, key messages, landing page URL.

**Gate:** User approves ad creative.

## Stage 6: Tracking & Measurement

Load and run the `tracking-setup` skill to define:
- Campaign-specific UTM conventions
- Conversion events to track
- Dashboard or reporting setup
- Attribution model

**Gate:** User approves the tracking plan.

## Summary

```
## Campaign Launch Complete

### Campaign: [name]
- Goal: [primary goal]
- Audience: [segments]
- Timeline: [dates]

### Assets Created
- Landing page: [path/URL]
- Emails: [count] emails in sequence → [paths]
- Social posts: [count] across [platforms] → [paths]
- Ad creative: [count] variations → [paths]

### Tracking
- UTM convention: [pattern]
- Key events: [list]

### Launch Checklist
- [ ] Landing page live
- [ ] Email sequence scheduled
- [ ] Social posts queued
- [ ] Ads submitted for review
- [ ] Tracking verified
- [ ] Team notified
```

## Output Structure

All files go into a single project folder:

```
marketing/campaigns/[campaign-slug]/
  strategy.md
  core-messaging.md
  landing-page-copy.md          (if landing page needed)
  email-sequence.md
  social-linkedin.md
  social-twitter.md
  ad-creative.md
  tracking-plan.md
```

Derive `[campaign-slug]` from the campaign name. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Campaign messaging must stay consistent across all channels
- Carry audience segments, key messages, and timeline through every stage
- If the user wants to skip a channel, skip it
- All output goes into the project folder, not scattered across `marketing/`
