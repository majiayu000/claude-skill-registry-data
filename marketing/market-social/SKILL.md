---
name: market-social
description: Social media content calendar and generation producing 30-day platform-specific calendars with posts, hooks, and hashtags.
---

# Social Media Content Calendar & Generation

Use this skill for `/market social <topic/url>`. Generate a complete 30-day platform-specific content calendar with posts, hooks, hashtags, content mix, engagement plan, and repurposing strategy. Write the deliverable to `SOCIAL-CALENDAR.md`.

## Invocation Triggers

- User runs `/market social <topic/url>`.
- User wants a 30-day social calendar, platform-specific posts, hooks, hashtags, or a repurposing plan.
- If a URL is provided, inspect the site for brand, audience, offer, voice, and themes.
- If a topic is provided, build the strategy around that topic and clearly label assumptions.

## Required Input Contract

Gather or infer:

- Brand/topic, industry, audience, voice, product/service, differentiators, and primary social goal.
- Existing source files: `BRAND-VOICE.md`, `COPY-SUGGESTIONS.md`, `COMPETITOR-REPORT.md`, `EMAIL-SEQUENCES.md`.
- Preferred platforms or constraints; otherwise choose 2-3 primary platforms based on audience and business type.
- Content pillars, proof assets, available media, regulated-category concerns, and date range.
- Whether claims, results, customer names, stats, partnerships, or testimonials are verified.

## Claims, Compliance, and Platform-Policy Constraints

Apply to every post:

- No fabricated proof: testimonials, customer names, results, stats, user counts, awards, partnerships, or press.
- No engagement bait such as "Like if you agree", "Comment YES", or "Share with 5 friends".
- Disclose paid, sponsored, affiliate, or partner content with `#ad`, `#sponsored`, or `#partner` at the start.
- No exaggerated outcome claims. Use realistic ranges and disclaimers when needed.
- Substantiate factual claims or label them as illustrative examples.
- For regulated categories, provide general information only and recommend qualified professional advice.
- Use copyright-cleared audio, video, and images; verify commercial-use rights for brand accounts.
- Avoid platform-banned promotional topics and personal-attribute implications.
- Use content-relevant hashtags only.
- Pause or flag posts during politically sensitive moments, breaking-news cycles, and crisis windows.

When in doubt, flag for legal or platform-policy review. This skill is not legal advice.

## Core Workflow

1. Discover brand, audience, voice, offer, differentiators, and existing marketing assets.
2. Select 2-3 primary platforms based on business model, audience, content strengths, and posting capacity.
3. Define 4-5 content pillars and content mix.
4. Pick platform-appropriate content types, hooks, hashtags, and engagement tactics.
5. Generate a 30-day calendar with pillar coverage, platform-native formats, and no back-to-back promotional posts.
6. Add repurposing plan, trend adaptation guidance, metrics, and validation notes.
7. Save `SOCIAL-CALENDAR.md` and provide a concise terminal summary.

## Platform Selection Logic

| Platform | Best For | Default Frequency |
|---|---|---|
| LinkedIn | B2B, SaaS, agencies, professionals | 3-5x/week |
| Twitter/X | Tech, media, creators, real-time commentary | 1-3x/day |
| Instagram | E-commerce, lifestyle, creators, visual brands | 4-7x/week feed, daily Stories |
| TikTok | Consumer brands, creators, education | 1-3x/day |
| YouTube | Education, demos, long-form search | 1-2x/week |
| Facebook | Local business, communities, older audiences | 3-5x/week |

Use [brand-strategy-and-hashtags.md](references/brand-strategy-and-hashtags.md) for discovery tables, content pillars, hashtag tiers, and platform details.

## Calendar Rules

- Each content pillar appears at least 6 times across the month.
- Promotional content never appears 2 days in a row.
- Engagement posts are spread every 2-3 days.
- Platform-specific content uses each platform's strengths instead of identical cross-posting.
- Content types are mixed within each platform.
- Trending slots stay flexible and include adaptation guidance.

## Output Expectations

Create `SOCIAL-CALENDAR.md` with:

- Brand context.
- Content pillars and content mix.
- Hashtag strategy.
- 30-day calendar grouped by week.
- Repurposing strategy.
- Engagement playbook.
- Trending format opportunities.
- Metrics to track.

Report selected platforms, period, total posts, content mix, pillar coverage, validation notes, and output path.

## Reference Map

| Need | Read |
|---|---|
| Brand discovery, platform selection, content pillars, hashtag tiers | [brand-strategy-and-hashtags.md](references/brand-strategy-and-hashtags.md) |
| Content types per platform | [content-types-by-platform.md](references/content-types-by-platform.md) |
| Hook formulas | [hooks.md](references/hooks.md) |
| Engagement tactics and repurposing | [engagement-and-repurposing.md](references/engagement-and-repurposing.md) |
| Calendar entry structure and trending formats | [calendar-and-trends.md](references/calendar-and-trends.md) |
| Output template, terminal summary, and cross-skill integration | [output-and-integration.md](references/output-and-integration.md) |
