---
name: analytics
version: 1.0.0
description: "Pull performance metrics from HubSpot, LinkedIn, X, and YouTube. Use when the user asks 'how are we doing,' 'what's our engagement,' 'show me metrics,' 'analytics,' 'email performance,' 'landing page stats,' 'campaign results,' 'LinkedIn analytics,' 'X analytics,' 'Twitter stats,' 'YouTube metrics,' or any question about marketing performance that real data can answer."
---

# Analytics

Unified marketing analytics skill. Pulls real data from HubSpot, LinkedIn, X, and YouTube via CLI scripts.

## How It Works

Each platform has a standalone TypeScript script in `scripts/`. Run them with `npx tsx` from the repo root. They read credentials from `.env` and output markdown tables to stdout.

**All scripts live in:** `.claude/skills/analytics/scripts/`

## Platform Status

| Platform | Status | Env Vars Needed |
|----------|--------|-----------------|
| HubSpot | Ready | `HUBSPOT_PRIVATE_APP_TOKEN` |
| LinkedIn | Needs setup | `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_ORG_ID` |
| X / Twitter | Needs setup | `X_BEARER_TOKEN`, `X_USERNAME` |
| YouTube | Needs setup | `YOUTUBE_ACCESS_TOKEN`, `YOUTUBE_CHANNEL_ID` |

Setup instructions for each platform are in `setup/`.

## Commands

### HubSpot Email Performance

```bash
npx tsx .claude/skills/analytics/scripts/hubspot-emails.ts [period] [limit]
```
- **period:** 7d, 30d, 90d, all (default: 30d)
- **limit:** number of top emails to show (default: 10)
- **Output:** aggregate metrics (sent, delivered, open rate, click rate, CTOR, bounce rate) + top emails table

### HubSpot Landing Page Analytics

```bash
npx tsx .claude/skills/analytics/scripts/hubspot-pages.ts [period] [limit]
```
- **period:** 7d, 30d, 90d (default: 30d)
- **limit:** number of pages to show (default: 10)
- **Output:** summary (views, submissions, conversion rate) + page breakdown + traffic sources

### HubSpot Campaign Performance

```bash
npx tsx .claude/skills/analytics/scripts/hubspot-campaigns.ts [period] [limit]
```
- **period:** 7d, 30d, 90d, all (default: 30d)
- **limit:** number of campaigns to show (default: 5)
- **Output:** campaign overview + per-campaign asset metrics (emails, pages, forms, blog posts)

### LinkedIn Analytics

```bash
npx tsx .claude/skills/analytics/scripts/linkedin.ts [command] [period] [limit]
```
- **command:** overview, posts, followers (default: overview)
- **period:** 7d, 30d, 90d (default: 30d)
- **limit:** number of posts to show (default: 10)
- **Output:** follower count + follower growth + post performance (impressions, clicks, likes, engagement)

### X (Twitter) Analytics

```bash
npx tsx .claude/skills/analytics/scripts/x-analytics.ts [command] [period] [limit]
```
- **command:** posts, profile (default: posts)
- **period:** 7d, 30d, 90d (default: 30d)
- **limit:** number of tweets to show (default: 20)
- **Output:** profile stats + aggregate tweet metrics + top tweets by impressions

### YouTube Analytics

```bash
npx tsx .claude/skills/analytics/scripts/youtube.ts [command] [period] [limit]
```
- **command:** channel, videos (default: channel)
- **period:** 7d, 30d, 90d (default: 30d)
- **limit:** number of videos to show (default: 10)
- **Output:** channel overview + period metrics (views, watch time, subs, engagement) + top videos

## Dispatch Logic

When the user asks a performance question, run the appropriate script(s):

| User asks about... | Script to run |
|---------------------|---------------|
| Email open rates, click rates, email performance | `hubspot-emails.ts` |
| Landing page views, conversions, bounce rates | `hubspot-pages.ts` |
| Campaign results, which campaign performed best | `hubspot-campaigns.ts` |
| LinkedIn engagement, post performance, followers | `linkedin.ts` |
| Twitter/X metrics, tweet impressions, follower count | `x-analytics.ts` |
| YouTube views, subscribers, watch time, video performance | `youtube.ts` |
| "How are we doing?" / "What's working?" / cross-platform | Run all configured platforms |
| Baseline metrics before creating new content | Run the relevant platform script |
| Comparing channels | Run multiple platform scripts and summarize |

## Proactive Usage

Don't wait for the user to ask "show me analytics." Run the appropriate script whenever:

- **Planning new content:** Pull current metrics to set baselines
- **Evaluating what worked:** Show real numbers, not guesses
- **CRO work:** Pull landing page data before making recommendations
- **Social content planning:** Check what posts performed best before drafting new ones
- **Email sequence work:** Pull email performance to establish benchmarks
- **Reporting or reviews:** Always lead with real data

## Interpreting Results

When presenting analytics data, don't just dump the table. Add context:

1. **Call out standouts** (best/worst performers, unusual spikes or drops)
2. **Compare to benchmarks** when relevant (B2B SaaS averages: email open 20-25%, click 2-3%, landing page conversion 3-5%)
3. **Connect to actions** ("Our top post was about X, suggesting the audience responds to Y")
4. **Note data gaps** ("LinkedIn analytics not yet configured, so we can only compare HubSpot and X")

## Error Handling

If a script fails with a missing env var error, check the setup doc for that platform and guide the user through configuration. Don't guess at credentials or make up data.

## Output Location

**Output location:** `marketing/reports/[report-slug]/` — confirm the project slug with the user before creating files.

---

## Related Skills

- **tracking-setup**: For setting up website analytics tracking (GA4, GTM, events, consent mode)
- **social-content**: For creating social posts informed by analytics data
- **page-cro**: For optimizing pages based on landing page analytics
- **email-sequence**: For designing email flows using email performance baselines
