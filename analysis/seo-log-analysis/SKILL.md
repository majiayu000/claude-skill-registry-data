---
name: seo-log-analysis
description: >
  Analyze server log files for crawl budget insights. Reads Apache Combined/Common
  or Nginx access logs locally (no external calls). Classifies bot vs user traffic,
  identifies top crawled URLs, crawl frequency by path, and crawl budget concerns.
  Use when user says "log analysis", "crawl budget", "server logs", "bot traffic",
  "crawl frequency", "access log", "analyze logs".
allowed-tools:
  - Read
  - Bash
  - Glob
---

# Server Log Analysis

Analyzes local server log files for crawl budget breakdown. No MCP or external calls required.

## Inputs

- `file`: Absolute path to server log file (Apache Combined, Apache Common, or Nginx access log).
  If user provides relative path, resolve with `Bash: realpath <path>`.

## Execution

**Step 1: Format Detection**

Read the first 10 lines of the log file to detect format:
- Apache Combined: `%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-agent}i"` — 9+ fields, has referer and UA in quotes
- Apache Common: `%h %l %u %t "%r" %>s %b` — 7 fields, no referer/UA
- Nginx: similar to Apache Combined with slight field order differences
- Check for compressed files (.gz) — if detected, inform user to decompress first

**Step 2: Parse Log Lines**

Use Bash awk to extract fields. For Apache Combined/Nginx format (9 fields):
```bash
awk '{
  ip=$1; method_url=$7; status=$9; ua=$0
  match($0, /"([^"]+)"$/, arr)  # Extract UA from last quoted field
  print ip, $7, $9, arr[1]
}' logfile
```
For Apache Common (7 fields): ip=$1, request=$7, status=$9, ua="unknown"

**Step 3: Classify User-Agents**

Group each request into categories:
- **Googlebot**: `Googlebot`, `Googlebot-Image`, `Googlebot-News`, `AdsBot-Google`
- **Bingbot**: `bingbot`, `BingPreview`, `MicrosoftPreview`
- **Other search bots**: `Slurp` (Yahoo), `DuckDuckBot`, `Baiduspider`, `YandexBot`, `Sogou`
- **AI crawlers**: `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Bytespider`, `CCBot`, `anthropic-ai`
- **Monitoring tools**: `Pingdom`, `UptimeRobot`, `StatusCake`, `NewRelic`, `Datadog`
- **Real users**: everything else (browsers: `Mozilla`, `Chrome`, `Safari`, `Firefox`, `Edge`)
- **Unknown**: no UA or unrecognized

**Step 4: Calculate Metrics**

Using awk/grep on the log file:
1. Total request count
2. Requests by bot category (count per category, % of total)
3. Requests by HTTP status code (200, 301, 302, 404, 500, etc.)
4. Top 20 crawled URLs by frequency — sort by count descending
5. Top 10 crawled path prefixes (first 2 URL segments, e.g., `/blog/`, `/products/`) — aggregate by prefix
6. Requests by hour-of-day (extract hour from timestamp field `[DD/Mon/YYYY:HH:MM:SS]`)

**Step 5: Identify Crawl Budget Concerns**

Flag these patterns:
- **4xx error rate >5%**: crawlers wasting budget on broken URLs
- **5xx error rate >1%**: server errors burning crawl budget
- **Duplicate crawl patterns**: same URL crawled >10x without apparent content change
- **Low-value paths**: bots crawling `/wp-admin`, `/search?`, `?sort=`, `?page=`, session URLs
- **302 redirect overuse**: temporary redirects don't pass full crawl equity
- **Non-canonical crawls**: `?utm_` or tracking parameters in crawled URLs

## Output Format

```
## Server Log Analysis: [filename]

**File:** [path] | **Format:** [Apache Combined/Common/Nginx] | **Total Requests:** [N]

### Crawl Budget Summary

| Metric | Value |
|--------|-------|
| Total requests | N |
| Bot traffic | N (X%) |
| Human traffic | N (X%) |
| Crawl error rate | X% (4xx+5xx) |
| Date range | [first log entry] to [last log entry] |

### Bot Traffic Breakdown

| Bot Category | Requests | % of Total | Top URL |
|---|---|---|---|
| Googlebot | N | X% | /path |
| Bingbot | N | X% | /path |
| AI Crawlers | N | X% | /path |
| Monitoring | N | X% | /path |
| Real Users | N | X% | — |
| Other/Unknown | N | X% | — |

### Top 20 Crawled URLs

| Rank | URL | Requests | Status Codes |
|------|-----|----------|--------------|
| 1 | /path | N | 200: N, 404: N |

### Crawl Frequency by Path

| Path Prefix | Requests | % of Bot Traffic |
|---|---|---|
| /blog/ | N | X% |

### Status Code Distribution

| Status | Count | % | Interpretation |
|--------|-------|---|----------------|
| 200 | N | X% | OK |
| 301 | N | X% | Permanent redirect |
| 404 | N | X% | Not found (crawl waste) |

### Crawl Budget Recommendations

[Prioritized list of issues found — Critical/High/Medium/Low]

## Data Sources

- Source: Local server log file (no external calls)
```
