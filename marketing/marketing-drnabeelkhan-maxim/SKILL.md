---
skill_id: marketing
name: Marketing & Growth
description: "Growth marketing and go-to-market — campaign, GTM, brand awareness, conversion, growth hacking, user acquisition, funnel, social media strategy. The CMO office's full-funnel growth domain."
version: 1.0.0
category: marketing
office: CMO
lead_agent: content-strategist
triggers:
  - marketing
  - campaign
  - growth
  - social media
  - GTM
  - brand awareness
  - conversion
  - growth hacking
  - user acquisition
  - funnel
  - retention
  - email marketing
  - landing page
collaborates_with:
  - growth-hacker
  - seo-specialist
  - brand-guardian
  - behavioral-designer
  - compliance
  - content-strategist
---

# Marketing & Growth -- Domain Dispatcher

> Office: CMO | Lead: content-strategist
> Sub-skills: 17 | Frameworks: AARRR Pirate Metrics, Growth Loops, AIDA, Cialdini, PAS, StoryBrand, Obviously Awesome, Hook Model, JTBD
> Hub file: MARKETING-CONTEXT.md (read by all sub-skills before executing)

## Purpose

The CMO's growth marketing domain -- covering campaign execution, GTM strategy, channel-specific social media strategy, and full-funnel growth. This skill orchestrates channel specialists (Instagram, TikTok, Twitter/X, Reddit), growth experimentation, app store optimization, and content creation. Maxim applies behavioral science to every campaign output -- persuasion triggers, conversion psychology, and social proof frameworks -- ensuring marketing drives measurable behavior change.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| app store listing, ASO, app rankings, keyword optimization | app-store-optimizer | app-store-optimizer/SKILL.md |
| content creation, copywriting, blog, newsletter | content-creator | content-creator/SKILL.md |
| user acquisition, viral growth, growth experiments, referral loops | growth-hacker | growth-hacker/SKILL.md |
| Instagram strategy, reels, stories, visual-first content | instagram-curator | instagram-curator/SKILL.md |
| Reddit engagement, subreddit authority, AMA strategy, community-native | reddit-community-builder | reddit-community-builder/SKILL.md |
| TikTok strategy, short-form video, trend participation, creator campaigns | tiktok-strategist | tiktok-strategist/SKILL.md |
| Twitter/X engagement, thought leadership, real-time, thread strategy | twitter-engager | twitter-engager/SKILL.md |
| conversion, CRO, landing page optimization, signup flow, A/B test | cro | cro/SKILL.md |
| headline, copy, tagline, CTA, messaging, AIDA, PAS, StoryBrand | copywriting | copywriting/SKILL.md |
| email campaign, drip sequence, onboarding email, retention email, nurture | email-sequences | email-sequences/SKILL.md |
| positioning, messaging, value proposition, competitive positioning, differentiation | positioning | positioning/SKILL.md |
| growth, retention, churn, activation, engagement, user lifecycle | growth-retention | growth-retention/SKILL.md |
| paid ads, Google Ads, Facebook Ads, attribution, analytics, tracking, ROAS | paid-measurement | paid-measurement/SKILL.md |
| sales enablement, go-to-market, launch strategy, sales deck, outbound | sales-gtm | sales-gtm/SKILL.md |
| content strategy, editorial calendar, content pillars, topic clusters, thought leadership | content-strategy | content-strategy/SKILL.md |
| customer research, user interviews, survey, NPS, feedback analysis, voice of customer | customer-research | customer-research/SKILL.md |
| referral program, advocacy, word of mouth, viral loop, ambassador | referral-program | referral-program/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-cmo`
- Task contains keywords: marketing, campaign, growth, social media, GTM, brand awareness, conversion, growth hacking, user acquisition, funnel, retention, email marketing, landing page, Instagram, TikTok, Twitter, Reddit
- Executive router detects marketing, growth, or campaign signals
- Other Maxim skills proactively loop here: behavior-science-persuasion (campaign psychology), search-visibility (SEO/AEO alignment), brand (brand consistency), content-creation (campaign content)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Ethics gate: none -- standard Maxim behavioral output quality applies. Exception: `localization-specialist` outputs touching Bill 96 or language law auto-loop compliance skill (CSO auto-loop rule).
- Frameworks: AARRR Pirate Metrics (Acquisition, Activation, Retention, Revenue, Referral), Growth Loops, AIDA (Attention, Interest, Desire, Action), Cialdini's 6 Principles, Hook Model (engagement), Fogg Behavior Model (campaign triggers)

## External Sources

- Primary: community-packs/claude-skills-library/marketing-skill/ (growth frameworks, channel playbooks, campaign templates, GTM patterns)
- Conflict resolution: Maxim ALWAYS WINS

## Hub-and-Spoke Architecture

All marketing sub-skills read `MARKETING-CONTEXT.md` before executing. This foundation file contains the project's product definition, ICP, positioning, brand voice, pricing, active campaigns, and funnel stages. Fill it in per-project to ensure consistent, contextual marketing outputs across all 17 sub-skills.

### Shared Resources

- `shared-resources/funnel-frameworks.md` -- Quick reference of all funnel frameworks (AARRR, AIDA, Flywheel, Hook Model, RACE, STP, Bow-Tie)
- `shared-resources/pricing-models.md` -- Quick reference of pricing strategies (value-based, usage-based, freemium, tiered, per-seat, flat-rate)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
