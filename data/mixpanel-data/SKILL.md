---
name: mixpanel-data
description: Analyze Mixpanel analytics data using the mixpanel_data Python library or mp CLI. Use when working with Mixpanel event data, user profiles, funnels, retention, cohorts, segmentation queries, JQL scripts, or SQL analysis on local DuckDB. Triggers on mentions of Mixpanel, event analytics, funnel analysis, retention curves, user behavior tracking, JQL queries, filter expressions, 'fetch data from Mixpanel', 'query Mixpanel with SQL', 'run DuckDB queries on events', 'analyze user behavior', 'export Mixpanel data', 'mp command', or requests to work with analytics pipelines. Supports filter expressions for WHERE/ON clauses, JQL (JavaScript Query Language) for complex transformations, Python scripts with pandas integration, and CLI pipelines with jq/Unix tools.
---

# Mixpanel Data Analysis

Fetch Mixpanel data once into local DuckDB, then query repeatedly with SQL—preserving context for reasoning rather than consuming it with raw API responses.

## Documentation Access

Full documentation is hosted at **https://jaredmcfarland.github.io/mixpanel_data/** with LLM-optimized access:

| Resource | URL | Use Case |
|----------|-----|----------|
| **llms.txt** | `https://jaredmcfarland.github.io/mixpanel_data/llms.txt` | Index of all docs with descriptions |
| **llms-full.txt** | `https://jaredmcfarland.github.io/mixpanel_data/llms-full.txt` | Complete documentation (~400KB) |
| **Individual pages** | `https://jaredmcfarland.github.io/mixpanel_data/{path}/index.md` | Specific topic deep-dive |

### When to Fetch Documentation

- **Use this skill** for quick patterns, common examples, and API summaries
- **Fetch llms.txt** to discover what documentation exists
- **Fetch llms-full.txt** when you need comprehensive reference (API signatures, all parameters, edge cases)
- **Fetch individual .md** for focused deep-dives (e.g., `/api/workspace/index.md` for Workspace class details)

### Documentation Structure

| Path | Content |
|------|---------|
| `/getting-started/installation/index.md` | Installation options |
| `/getting-started/quickstart/index.md` | 5-minute tutorial |
| `/getting-started/configuration/index.md` | Credentials and config |
| `/guide/fetching/index.md` | Fetching events/profiles |
| `/guide/streaming/index.md` | Streaming without storage |
| `/guide/sql-queries/index.md` | DuckDB SQL patterns |
| `/guide/live-analytics/index.md` | Segmentation, funnels, retention |
| `/guide/discovery/index.md` | Schema exploration |
| `/api/workspace/index.md` | Workspace class reference |
| `/api/auth/index.md` | Authentication module |
| `/api/exceptions/index.md` | Exception hierarchy |
| `/api/types/index.md` | Result types |
| `/cli/commands/index.md` | CLI command reference |

## Reference Files Guide

When you need detailed information, read these reference files:

| File | When to Read |
|------|--------------|
| [library-api.md](references/library-api.md) | Complete Python API signatures, parameters, return types for all Workspace methods |
| [cli-commands.md](references/cli-commands.md) | Full CLI command reference with all options and examples |
| [query-expressions.md](references/query-expressions.md) | Complete filter expression syntax, JQL reference, built-in reducers, bucketing |
| [patterns.md](references/patterns.md) | JSON property queries in DuckDB, pandas integration, jq/Unix pipelines, data science workflows |
| [documentation.md](references/documentation.md) | How to fetch external documentation from llms.txt, page URLs, fetch strategy |

## When to Use

### Python Library (`mixpanel_data`)
- Building scripts, notebooks, or data pipelines
- Need DataFrame results for pandas/visualization
- Complex multi-step analysis
- Programmatic credential management

### CLI (`mp`)
- Quick one-off queries
- Shell scripting or Unix pipelines
- Streaming data to jq, awk, or other tools
- Non-Python environments

## Two Data Paths

### Path 1: Live Queries (Quick Answers)
Call Mixpanel API directly for real-time metrics without local storage.

```python
# Python
result = ws.segmentation("Purchase", from_date="2024-01-01", to_date="2024-01-31", on="country")
print(result.df)
```

```bash
# CLI
mp query segmentation -e Purchase --from 2024-01-01 --to 2024-01-31 --on country
```

### Path 2: Local Analysis (Deep Analysis)
Fetch data into DuckDB, then query with SQL repeatedly.

```python
# Python - use parallel=True for large date ranges (up to 10x faster)
ws.fetch_events("events", from_date="2024-01-01", to_date="2024-03-31", parallel=True)
df = ws.sql("SELECT event_name, COUNT(*) FROM events GROUP BY 1")
```

```bash
# CLI - use --parallel for large date ranges (up to 10x faster)
mp fetch events --from 2024-01-01 --to 2024-03-31 --parallel
mp query sql "SELECT event_name, COUNT(*) FROM events GROUP BY 1"
```

**Parallel Fetching**: For date ranges > 7 days, use `--parallel` (CLI) or `parallel=True` (Python) for significantly faster exports. Required for ranges > 100 days.

### Path 3: Streaming (Pipelines)
Stream to stdout for processing with external tools.

```bash
mp fetch events --from 2024-01-01 --to 2024-01-01 --stdout | jq '.event'
mp fetch events --stdout | jq -r '[.event, .distinct_id] | @csv' > events.csv
```

## JSON Property Access (Critical)

Events and profiles store properties as JSON. Access with `properties->>'$.fieldname'`:

```sql
-- DuckDB SQL (local queries)
SELECT properties->>'$.country' as country FROM events
WHERE properties->>'$.plan' = 'premium'
```

For complete JSON query patterns (type casting, filtering, aggregation), see [references/patterns.md](references/patterns.md).

## Filter Expressions (WHERE/ON)

Filter expressions use SQL-like syntax for filtering and segmenting data in API calls.

**ON Parameter** (segmentation): Accepts bare property names (auto-wrapped) or full expressions
```bash
mp query segmentation -e Purchase --on country
```

**WHERE Parameter** (filtering): Always uses full expression syntax
```bash
mp fetch events --where 'properties["amount"] > 100 and properties["plan"] in ["premium", "enterprise"]'
```

For complete expression syntax (comparison, logical, set operations, existence functions, date/time functions), see [references/query-expressions.md](references/query-expressions.md).

## JQL (JavaScript Query Language)

Full JavaScript-based query language for complex transformations. Use `Events()`, `People()`, `join()` with transformations like `.filter()`, `.map()`, `.groupBy()`, `.reduce()`.

```bash
mp query jql script.js --param from_date=2024-01-01
```

For complete JQL reference (data sources, transformations, built-in reducers, bucketing, common patterns), see [references/query-expressions.md](references/query-expressions.md).

## Credentials

Resolution priority:
1. Environment variables: `MP_USERNAME`, `MP_SECRET`, `MP_PROJECT_ID`, `MP_REGION`
2. Named account: `Workspace(account="prod")` or `mp --account prod`
3. Default account from `~/.mp/config.toml`

## Quick Start Examples

### Python: Fetch and Analyze

```python
import mixpanel_data as mp

ws = mp.Workspace()
ws.fetch_events("jan", from_date="2024-01-01", to_date="2024-01-31")

# SQL queries
df = ws.sql("""
    SELECT properties->>'$.country' as country, COUNT(*) as cnt
    FROM jan GROUP BY 1 ORDER BY 2 DESC
""")

# Introspection
ws.event_breakdown("jan")  # Event distribution
ws.summarize("jan")        # Column statistics

ws.close()
```

### Python: Ephemeral Workspace

```python
with mp.Workspace.ephemeral() as ws:
    ws.fetch_events("events", from_date="2024-01-01", to_date="2024-01-01")
    count = ws.sql_scalar("SELECT COUNT(*) FROM events")
# Database automatically deleted
```

### CLI: Discover and Fetch

```bash
# Discover available events
mp inspect events --format table

# Fetch events to local database
mp fetch events --from 2024-01-01 --to 2024-01-31

# Query locally
mp query sql "SELECT COUNT(*) FROM events" --format table
mp inspect breakdown -t events  # Event distribution
```

### CLI: Live Queries

```bash
# Segmentation
mp query segmentation -e Purchase --from 2024-01-01 --to 2024-01-31 --on country

# Funnel (requires saved funnel ID)
mp inspect funnels  # List funnels to get ID
mp query funnel 12345 --from 2024-01-01 --to 2024-01-31

# Retention
mp query retention --born "Sign Up" --return "Purchase" --from 2024-01-01 --to 2024-01-31
```

## Data Storage

Events: `(event_name, event_time, distinct_id, insert_id PRIMARY KEY, properties JSON)`
Profiles: `(distinct_id PRIMARY KEY, properties JSON, last_seen)`

Full schema and query patterns in [references/patterns.md](references/patterns.md).

## Output Formats (CLI)

`--format json` (default), `jsonl`, `table`, `csv`, `plain`

### Filtering with --jq

Commands that output JSON also support the `--jq` option for client-side filtering using jq syntax:

```bash
# Get first 5 events
mp inspect events --format json --jq '.[:5]'

# Filter by name pattern
mp inspect events --format json --jq '.[] | select(contains("User"))'

# Extract fields from query results
mp query segmentation -e Purchase --from 2024-01-01 --to 2024-01-31 \
  --format json --jq '.total'

# Filter SQL results
mp query sql "SELECT * FROM events" --format json --jq '.[] | select(.event_name == "Purchase")'
```

Note: `--jq` only works with `--format json` or `--format jsonl`.

## API Overview

The Workspace class provides three main capability areas:

1. **Discovery**: `events()`, `properties()`, `funnels()`, `cohorts()` - Explore project schema
2. **Data Fetching**: `fetch_events()`, `fetch_profiles()`, `stream_*()` - Get data locally or stream
3. **Analytics**: `segmentation()`, `funnel()`, `retention()`, `jql()` - Live queries and analysis
4. **Local SQL**: `sql()`, `sql_scalar()`, `sql_rows()` - Query DuckDB with SQL
5. **Introspection**: `info()`, `tables()`, `sample()`, `summarize()` - Inspect local data

### Advanced Profile Fetching

`fetch_profiles()` and `stream_profiles()` support advanced filtering:

```python
# Fetch specific users by ID
ws.fetch_profiles("vips", distinct_ids=["user_1", "user_2"])

# Fetch group profiles (companies, accounts, etc.)
ws.fetch_profiles("companies", group_id="companies")

# Fetch users by behavior (e.g., purchased in last 30 days)
ws.fetch_profiles(
    "purchasers",
    behaviors=[{"window": "30d", "name": "buyers", "event_selectors": [{"event": "Purchase"}]}],
    where='(behaviors["buyers"] > 0)'
)

# Query historical profile state
ws.fetch_profiles("historical", as_of_timestamp=1704067200)

# Cohort membership analysis (include non-members with flag)
ws.fetch_profiles("cohort_analysis", cohort_id="12345", include_all_users=True)
```

**Parameter constraints**: `distinct_id`/`distinct_ids` mutually exclusive; `behaviors`/`cohort_id` mutually exclusive; `include_all_users` requires `cohort_id`.

For complete method signatures and parameters, see [references/library-api.md](references/library-api.md).

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `TableExistsError` | Table already exists | Use `--replace` or `--append` |
| `AuthenticationError` | Invalid credentials | Check `mp auth test` |
| `RateLimitError` | API rate limited | Wait for retry_after seconds |
| `DateRangeTooLargeError` | >100 days range (sequential) | Use `--parallel` flag |
| `EventNotFoundError` | Event not in project | Check `mp inspect events` |
