---
name: readwise-api
description: Fetch and analyze Readwise reading activity for any date range. Use when user asks about articles saved, highlights created, or most-highlighted content for today, yesterday, last week, last month, or custom date ranges (e.g., "show my Readwise activity from Jan 1-7"). Requires READWISE_API_TOKEN env var. Connects to Readwise Highlights API (v2) and Reader API (v3).
allowed-tools: Bash(pnpm tsx*)
---

# Readwise API

Connect to Readwise APIs to fetch and analyze reading activity.

## Overview

Fetch saved articles, highlights, and identify most-highlighted content from user's Readwise account for any date range. Uses Readwise v2 Highlights API and v3 Reader API.

**Default behavior**: Last 7 days (when no date flags specified)

## Prerequisites

**API Token**: Set `READWISE_API_TOKEN` environment variable
- Get token: https://readwise.io/access_token
- `export READWISE_API_TOKEN="your_token_here"`

**Dependencies**: Installed via pnpm (auto on first use)
- chalk (terminal colors)
- ora (spinners)
- TypeScript support

## Date Range Options

All commands support flexible date ranges via flags:

### Preset Shortcuts
- `--today`: Midnight today → now
- `--yesterday`: Yesterday (full day)
- `--last-week`: Last 7 days (default when no flags specified)
- `--last-month`: Last 30 days

### Custom Ranges
- `--from YYYY-MM-DD`: Start date (inclusive)
- `--to YYYY-MM-DD`: End date (inclusive)
- Can use together: `--from 2025-01-01 --to 2025-01-07`

### Examples
```bash
# Today only
pnpm tsx scripts/fetch-todays-activity.ts articles --today

# Yesterday
pnpm tsx scripts/fetch-todays-activity.ts highlights --yesterday

# Custom range
pnpm tsx scripts/fetch-todays-activity.ts all --from 2025-01-01 --to 2025-01-07

# Default (no flags) = last 7 days
pnpm tsx scripts/fetch-todays-activity.ts all
```

**Note**: Reader API doesn't support end dates natively. Articles filtered client-side for accurate date ranges.

## Core Capabilities

### Default: Comprehensive Activity Summary

**Command**:
```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts all [date-flags]
```

**Output**: Four-section analysis w/ insights-first approach:

1. **🧠 Key Learnings**
   - Top 5 insights extracted from highlight content
   - Domain-tagged bullets (emoji + category: insight)
   - Reading context paragraph (pattern + domain mix)

2. **📈 Activity Timeline**
   - Daily breakdown w/ visual bars (unicode blocks)
   - Peak days identified
   - Reading pattern analysis (consistent/burst/weekend/weekday)

3. **📂 By Category**
   - Domain grouping w/ visual bars + percentages
   - Auto-inferred from content (Architecture, Performance, Psychology, etc.)
   - Top 2 focus areas highlighted

4. **📊 Stats Dashboard**
   - Articles saved, highlights created
   - Unique sources, avg/day
   - Top source by highlight count

**When to use**: User asks "Show my Readwise activity", "What have I been learning?", "My reading summary"

### Individual Modes

#### 1. Key Learnings Only

**Command**:
```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts learnings [date-flags]
```

**Output**: Insights + context only (no timeline/stats)

**When to use**: User wants just the learnings/insights

#### 2. Activity Timeline Only

**Command**:
```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts timeline [date-flags]
```

**Output**: Daily activity visualization + peaks + pattern

**When to use**: User asks "When am I most active?" or "Show my reading schedule"

#### 3. Category Breakdown Only

**Command**:
```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts categories [date-flags]
```

**Output**: Domain distribution w/ visual bars

**When to use**: User asks "What topics am I focusing on?" or "My reading categories"

#### 4. Stats Dashboard Only

**Command**:
```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts dashboard [date-flags]
```

**Output**: Stats summary box

**When to use**: User wants quick metrics only

### Legacy Modes (Still Available)

#### Articles

**Command**: `pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts articles [date-flags]`

**Output**: List of saved articles w/ categories, titles, authors, URLs

#### Highlights

**Command**: `pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts highlights [date-flags]`

**Output**: All highlights grouped by source, showing text + notes

#### Top Highlighted

**Command**: `pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts top-highlighted [N] [date-flags]`

**Output**: Top N sources ranked by highlight count

## Usage Examples

### Example 1: "What have I been learning on Readwise this week?"

```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts all
```

Returns comprehensive analysis: insights, timeline, categories, stats (default = last 7 days)

### Example 2: "Show my key insights from today"

```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts learnings --today
```

Returns top 5 insights extracted from today's highlights + reading context

### Example 3: "When am I most active on Readwise?"

```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts timeline --last-month
```

Returns daily activity visualization for last 30 days w/ peak identification

### Example 4: "What topics am I focusing on?"

```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts categories
```

Returns domain distribution w/ visual bars (default = last 7 days)

### Example 5: "Show Readwise stats from Jan 1-7"

```bash
pnpm tsx skills/readwise-api/scripts/fetch-todays-activity.ts dashboard --from 2025-01-01 --to 2025-01-07
```

Returns metrics dashboard for custom date range

## Error Handling

**Missing API token**: Clear error with link to get token

**Rate limits**: Automatic 3s delays between paginated requests (20 req/min limit)

**Network errors**: Graceful failure with error messages via spinner

**Empty results**: Friendly "no activity yet" messages

## API Details

**Rate Limits**: 20 requests/minute per access token
- Script auto-throttles with 3s delays between requests
- Pagination handled automatically

**Date Filtering**:
- Presets: today, yesterday, last-week (7d), last-month (30d)
- Custom ranges via --from/--to flags (ISO 8601: YYYY-MM-DD)
- Default: last 7 days
- Timezone: Local (dates converted to UTC for API)

**Reader API Limitation**:
- Supports only start date (`updatedAfter`), no end date
- End date filtering done client-side after fetch
- May fetch extra data that gets filtered locally

**Pagination**: Automatically follows `next` URLs (v2) and `pageCursor` (v3)

## Implementation

**API Client**: `scripts/readwise-client.ts`
- Pure functions, typed errors
- Handles pagination and rate limiting
- Returns `ApiResult<T>` with success/error

**Analysis**: `scripts/analyze-highlights.ts`
- Daily grouping + peak detection
- Domain inference (14 categories: Architecture, Performance, Psychology, etc.)
- NLP-style insight extraction (sentence scoring, clustering, ranking)
- Pattern analysis (consistent/burst/weekend/weekday reader)
- Pure functions, immutable transformations

**CLI**: `scripts/fetch-todays-activity.ts`
- Human-readable terminal output w/ unicode visual bars
- Colored text via chalk, spinners via ora
- Eight modes: learnings, timeline, categories, dashboard, articles, highlights, top-highlighted, all
- Default order: insights → timeline → categories → stats

**Tests**: `scripts/__tests__/analyze-highlights.test.ts`
- Comprehensive coverage (52 tests)
- Edge cases: empty data, date boundaries, pattern detection

## References

Detailed API documentation: `references/api_reference.md`
- Endpoint details
- Authentication
- Rate limits
- Request/response formats
- Example code
