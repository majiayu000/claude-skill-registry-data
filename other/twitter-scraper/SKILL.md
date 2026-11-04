---
name: twitter-scraper
description: "X/Twitter CDP Tweet Scraper — Scrapes a user's complete tweet history via browser CDP protocol. Use when the user needs to fully and accurately collect all tweets from a specific Twitter/X user. Applicable scenarios: collecting all tweets from a user for a given year, exporting a Twitter timeline, bulk-fetching tweet data for analysis. Preferred over x-tweet-fetcher (Nitter-based) when full long-form tweets, precise timestamps, or higher completeness is required. Supports Arc, Chrome, Edge, Brave, and all Chromium-based browsers. Requires the user to be logged into Twitter in the browser."
---

# X/Twitter CDP Tweet Scraper v2

Extracts authentication from a Chromium browser via CDP, then calls the Twitter GraphQL API directly with httpx for high-speed bulk tweet collection. Outputs JSON + Markdown.

## Quick Start

```bash
# By date range (recommended)
python3 <skill-path>/scripts/cdp_tweet_fetcher.py <username> --since 2026-02 [--until 2026-02-28] [--output-dir DIR]

# By year (shorthand)
python3 <skill-path>/scripts/cdp_tweet_fetcher.py <username> --year 2026 [--output-dir DIR]

# No date specified -> defaults to current year to date
python3 <skill-path>/scripts/cdp_tweet_fetcher.py <username> [--output-dir DIR]
```

**Arguments:**
- `username` (required): Twitter username (without @)
- `--since`: Start date (inclusive). Accepts `YYYY-MM-DD`, `YYYY-MM`, `YYYY`
- `--until`: End date (inclusive), defaults to today
- `--year`: Target year (shorthand for `--since YYYY-01-01`)
- `--output-dir`: Output directory, defaults to current working directory
- `--page-delay`: Seconds between API pages, default 1.0
- `--max-pages`: Maximum pages to fetch, default 200
- `--cdp-port`: CDP debugging port, default 9222

**Output files:**
- `{username}_tweets_{YYYYMMDD}_{YYYYMMDD}.json` — Full structured data
- `{username}_tweets_{YYYYMMDD}_{YYYYMMDD}.md` — Human-readable Markdown report

## Prerequisites

1. **Chromium-based browser** (Chrome / Edge / Brave / Arc / Chromium) installed and logged in to Twitter/X
2. **Python dependencies**: `pip install playwright httpx && playwright install chromium`
3. Browser must be launched with CDP enabled — the script auto-detects your OS and shows the correct launch command

**Launch browser with CDP (pick your browser):**

macOS:
```bash
# Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
# Edge
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9222
# Brave
/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222
# Arc
/Applications/Arc.app/Contents/MacOS/Arc --remote-debugging-port=9222
```

Linux:
```bash
google-chrome --remote-debugging-port=9222
# or: chromium-browser / microsoft-edge / brave-browser
```

Windows (PowerShell):
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
# or: msedge.exe / brave.exe in their respective paths
```

## Architecture — Why It's Fast

v2 minimizes browser interaction: authentication is extracted once (~5 s), then all API calls go through httpx directly.

| Change | Effect |
|--------|--------|
| Browser only used for cookie + query ID extraction (one-time) | Init drops from ~18 s to ~5 s |
| httpx direct HTTP requests (no CDP round-trips) | Each API call 3-5x faster |
| Single endpoint: UserTweetsAndReplies (superset) | Half the pagination |
| count=40 (was 20) | Half the pagination again |
| page-delay 1.0 s (was 2.5 s) | 60% less wait per page |

## Execution Flow

1. **Connect to browser**: CDP connection, extract cookies and CSRF token
2. **Discover API**: Parse JS bundles for GraphQL query IDs (no page navigation)
3. **HTTP client**: Create httpx client with extracted auth
4. **Resolve user ID**: Via UserByScreenName API
5. **Bulk fetch**: UserTweetsAndReplies endpoint, 40 tweets/page, direct HTTP
6. **Output**: JSON + Markdown files

## Output Schema

Each tweet contains:

```json
{
  "tweet_id": "123456789",
  "text": "Full tweet text...",
  "datetime": "2026-01-15T10:30:00+00:00",
  "url": "https://x.com/user/status/123456789",
  "author": "username",
  "is_reply": false,
  "reply_to": null,
  "reply_to_tweet_id": null,
  "is_retweet": false,
  "retweet_of": null,
  "is_quote": false,
  "quoted_tweet_url": null,
  "likes": 100,
  "retweets": 20,
  "replies": 5,
  "bookmarks": 30,
  "views": 10000,
  "media": ["https://pbs.twimg.com/..."],
  "links": ["https://example.com/..."]
}
```

## Fetching Twitter Articles (Long-Form Posts)

Links in tweets matching `x.com/i/article/{article_id}` are Twitter Articles (long-form posts). Article content is NOT in the tweet API response and requires additional steps to extract.

### Usage

```bash
python3 <skill-path>/scripts/fetch_articles.py <tweets_json> [--output-dir DIR] [--cdp-port 9222]
```

- `tweets_json`: Path to a JSON file previously output by `cdp_tweet_fetcher.py`
- `--output-dir`: Directory for article Markdown files (default: `./articles`)
- `--cdp-port`: CDP debug port (default: 9222)

### Technical Details

1. **API endpoint**: `TweetResultByRestId` (GET), queried with the article's associated `tweet_id`
2. **Critical parameter**: `fieldToggles: {"withArticleRichContentState": true, "withArticlePlainText": false}`
3. **Data location**: `data.tweetResult.result.article.article_results.result.content_state`
4. **Content format**: Draft.js — `blocks` (paragraphs / headings / lists / blockquotes / code blocks / atomic) + `entityMap` (links / media references)
5. **Type pitfall**: `entityMap` is sometimes a `dict` (keyed by string index) and sometimes a `list` (indexed by position) — must handle both

### Browser Request Parameters (Verified 2026-02)

```json
{
  "variables": {
    "tweetId": "<tweet_id>",
    "includePromotedContent": true,
    "withBirdwatchNotes": true,
    "withVoice": true,
    "withCommunity": true
  },
  "fieldToggles": {
    "withArticleRichContentState": true,
    "withArticlePlainText": false
  }
}
```

## Lessons Learned

| Date | Lesson | Action |
|------|--------|--------|
| 2026-02-27 | Twitter timeline is reverse-chronological; if all tweets on a page are before the target date, subsequent pages are even older | Added early-stop condition to script |
| 2026-02-27 | DOM validation wastes time when API phase yields 0 tweets in target range | Skip DOM validation directly |
| 2026-02-27 | DOM scrolling has no date filter, collects many irrelevant IDs | Snowflake ID date filtering |
| 2026-02-27 | v1 architecture bottleneck: page.evaluate relay is slow, dual endpoints redundant, count=20 conservative, DOM validation heavy | v2 rewrite: httpx direct, single endpoint, count=40, DOM disabled by default |
| 2026-02-28 | Twitter Article (long-form) content is NOT in the tweet text; requires separate extraction | Added `fetch_articles.py` script |
| 2026-02-28 | `TweetResultByRestId` does not return article body by default; requires `fieldToggles: {"withArticleRichContentState": true}` | Critical parameter documented |
| 2026-02-28 | Article content is in Draft.js format (`content_state.blocks` + `entityMap`); `entityMap` can be either a list or a dict | Script handles both types |
| 2026-02-28 | Playwright CDP `dialog` event dismiss can throw `ProtocolError: No dialog is showing` and kill the Node process | Must wrap in `try/except` |
| 2026-02-28 | When facing unknown API behavior, trace the browser's actual request parameters first, then write scraping code | Methodology: observe before guessing |
