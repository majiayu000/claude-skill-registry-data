---
name: google-analytics
description: Query Google Analytics 4 data for traffic analysis, page performance, user engagement, and realtime monitoring.
allowed-tools: Bash, Read, Write
env:
  - GA4_PROPERTY_ID
  - GOOGLE_PROJECT_ID
---

# Google Analytics Reporting

Query GA4 data directly via the Analytics Data API.

## Quick Start

```bash
# Overall summary (28 days default)
bun .claude/skills/google-analytics/scripts/ga-report.ts summary

# Summary for last 7 days
bun .claude/skills/google-analytics/scripts/ga-report.ts summary 7

# Top pages
bun .claude/skills/google-analytics/scripts/ga-report.ts pages

# Top pages (last 14 days, top 10)
bun .claude/skills/google-analytics/scripts/ga-report.ts pages 14 10

# Traffic sources
bun .claude/skills/google-analytics/scripts/ga-report.ts sources

# Traffic by country
bun .claude/skills/google-analytics/scripts/ga-report.ts countries

# Realtime active users
bun .claude/skills/google-analytics/scripts/ga-report.ts realtime

# Top events
bun .claude/skills/google-analytics/scripts/ga-report.ts events
```

## Available Commands

| Command | Description | Args |
|---------|-------------|------|
| `summary` | Overall metrics (users, sessions, views, bounce rate) | `[days]` |
| `pages` | Top pages by views | `[days] [limit]` |
| `sources` | Traffic sources (source/medium) | `[days] [limit]` |
| `countries` | Traffic by country | `[days]` |
| `realtime` | Current active users | - |
| `events` | Top events by count | `[days] [limit]` |

## Configuration

- **Auth**: Uses Application Default Credentials (`~/.config/gcloud/application_default_credentials.json`)
- **Required Scope**: `analytics.readonly`
- Set your GA4 property: `GA4_PROPERTY_ID=YOUR_PROPERTY_ID`

### Setup

1. Find your GA4 Property ID in Google Analytics: Admin > Property Settings (numeric value, not G-XXXXXX)
2. Set it as environment variable:
```bash
export GA4_PROPERTY_ID=123456789
```
3. Authenticate with Google Cloud:
```bash
gcloud auth application-default login \
  --scopes https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform
```

## Dependencies

Install required packages before using:

```bash
bun add google-auth-library
```

## When to Use

- **SEO Analysis**: Correlate with Search Console data
- **Content Performance**: See which pages engage users
- **International Traffic**: Check country breakdown
- **Campaign Tracking**: Analyze traffic sources
- **Real-time Monitoring**: See current visitors

## Combining with Search Console

For complete SEO analysis:
1. Use Search Console MCP for organic search data (clicks, impressions, position)
2. Use this skill for engagement data (time on page, bounce rate, events)

## Troubleshooting

### Auth Error
Refresh your Application Default Credentials:
```bash
gcloud auth application-default login \
  --scopes https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform
```

### Wrong Property
Verify the property ID — it's a numeric value (not G-XXXXXX measurement ID).
