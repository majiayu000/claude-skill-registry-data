---
name: cloudflare-worker-logs
description: Query and analyze Cloudflare Workers logs. Use for debugging workers, checking error rates, viewing request logs. Activates with phrases like "check worker logs", "what errors are in the worker", "cloudflare logs", "worker observability".
---

# Cloudflare Worker Logs

Query historical logs from Cloudflare Workers using the Workers Observability API.

## Requirements

Requires environment variables (should be defined in env already; if not, available via `uv run poe init-secrets`):

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

## Real-time Logs

For real-time log streaming (not historical queries), use wrangler tail instead:

```sh
cd terraform/cloudflare && wrangler tail llms --format pretty
```

This requires a terminal session that stays open.

## Available Scripts

All scripts are in the `scripts/` directory relative to this skill. Run them with:

```sh
uv run scripts/<script_name>.py [args]
```

### cf_workers_list.py

List all Workers in the Cloudflare account. If you only need details of a single Worker, use `cf_worker_get.py` instead.

```sh
uv run scripts/cf_workers_list.py
```

No arguments required.

### cf_worker_get.py

Get the details of a Cloudflare Worker.

```sh
uv run scripts/cf_worker_get.py <script_name>
```

**Arguments:**

- `script_name` (required): The name of the worker script to retrieve

### cf_observability_keys.py

Find keys in the Workers Observability data.

**Best Practices:**

- Set a high limit (1000+) to ensure you see all available keys
- Add the `$metadata.service` filter to narrow results to a specific Worker

**Troubleshooting:**

- If expected fields are missing, verify the Worker is actively logging
- For empty results, try broadening your time range

```sh
uv run scripts/cf_observability_keys.py [options]
```

**Options:**

- `--minutes N`: Time range in minutes (default: 60, max: 10080 for 7 days)
- `--limit N`: Max keys to return (default: 100, set high like 1000 for comprehensive list)
- `--key-needle PATTERN`: Pattern to match key names
- `--key-needle-regex`: Treat key-needle as regex
- `--needle TEXT`: General text search in log content
- `--needle-regex`: Treat needle as regex
- `--filter KEY:OP:TYPE:VALUE`: Filter (can be repeated)

**Example:**

```sh
uv run scripts/cf_observability_keys.py --limit 1000 --filter '$metadata.service:eq:string:llms'
```

### cf_observability_values.py

Find values in the Workers Observability Data.

**Troubleshooting:**

- For no results, verify the field exists using `cf_observability_keys.py` first
- If expected values are missing, try broadening your time range

```sh
uv run scripts/cf_observability_values.py <key> [options]
```

**Arguments:**

- `key` (required): The key to get values for (e.g., `$metadata.service`, `$metadata.level`)

**Options:**

- `--key-type {string,number,boolean}`: Type of the key (default: string)
- `--minutes N`: Time range in minutes (default: 60, max: 10080 for 7 days)
- `--limit N`: Max values to return (default: 50)
- `--needle PATTERN`: Pattern to match values
- `--needle-regex`: Treat needle as regex
- `--filter KEY:OP:TYPE:VALUE`: Filter (can be repeated)

**Example:**

```sh
uv run scripts/cf_observability_values.py '$metadata.service' --limit 100
```

### cf_observability_query.py

Query the Workers Observability API to analyze logs and metrics from Cloudflare Workers.

**Core Capabilities:**

This script provides three primary views of your Worker data:

1. **events** (default): Browse individual request logs and errors
2. **calculations**: Compute statistics across requests (avg, p99, etc.)
3. **invocations**: Find specific request invocations matching criteria

**Examples by View Type:**

_Events View:_

- "Show all errors for worker llms in the last 30 minutes"
- "Show events where the path contains /api"

_Calculation View:_

- "What is the p99 wall time for worker llms?"
- "Count requests grouped by status code"

_Invocation View:_

- "Find a request that resulted in a 500 error"
- "List successful requests with status 200"

**Filtering Best Practices:**

- Before applying filters, use `cf_observability_keys.py` and `cf_observability_values.py` to confirm available fields and values
- Common filter fields: `$metadata.service`, `$metadata.origin`, `$metadata.trigger`, `$metadata.message`, `$metadata.level`, `$metadata.requestId`

**Calculation Best Practices:**

- Before applying calculations, use `cf_observability_keys.py` to confirm the key exists

**Troubleshooting:**

- If no results returned, try broadening the time range or relaxing filters
- For errors about invalid fields, use `cf_observability_keys.py` to see available options

```sh
uv run scripts/cf_observability_query.py [options]
```

**Options:**

- `--view {events,calculations,invocations}`: Query view type (default: events)
- `--minutes N`: Time range in minutes (default: 60, max: 10080 for 7 days)
- `--limit N`: Max results to return (default: 10)
- `--offset ID`: Pagination offset (use `$metadata.id` from previous results)
- `--offset-by N`: Numeric offset for pagination
- `--offset-direction {next,prev}`: Pagination direction
- `--dry`: Dry run - validate query without executing
- `--granularity N`: Time bucket granularity for calculations
- `--filter KEY:OP:TYPE:VALUE`: Filter (can be repeated)
- `--filter-combination {and,or}`: How to combine filters (default: and)
- `--calculation OPERATOR[:KEY[:TYPE[:ALIAS]]]`: Calculation (can be repeated, for calculations view)
- `--group-by VALUE[:TYPE]`: Field to group by (can be repeated)
- `--order-by ALIAS`: Calculation alias to sort by
- `--order {asc,desc}`: Sort order (default: desc)
- `--needle TEXT`: Full-text search in log content
- `--needle-regex`: Treat needle as regex

**Filter Format:**

Filters use format `key:operation:type:value` where:

- `key`: Field name (e.g., `$metadata.service`)
- `operation`: One of `includes`, `not_includes`, `starts_with`, `regex`, `exists`, `is_null`, `in`, `not_in`, `eq`, `neq`, `gt`, `gte`, `lt`, `lte`
- `type`: One of `string`, `number`, `boolean`
- `value`: Comparison value

**Calculation Format:**

Calculations use format `operator[:key[:key_type[:alias]]]` where:

- `operator`: One of `uniq`, `count`, `max`, `min`, `sum`, `avg`, `median`, `p001`, `p01`, `p05`, `p10`, `p25`, `p75`, `p90`, `p95`, `p99`, `p999`, `stddev`, `variance`
- `key`: Field to calculate on (optional for `count`)
- `key_type`: Type of the key (default: number)
- `alias`: Name for this calculation in results

**Examples:**

Show recent errors for the llms worker:

```sh
uv run scripts/cf_observability_query.py --filter '$metadata.service:eq:string:llms' --filter '$metadata.level:eq:string:error' --limit 20
```

Get p99 wall time grouped by service:

```sh
uv run scripts/cf_observability_query.py --view calculations --calculation 'p99:wallTime:number:p99_wall' --group-by '$metadata.service'
```

Count requests by status code:

```sh
uv run scripts/cf_observability_query.py --view calculations --calculation 'count' --group-by 'response.status:number'
```

Search for specific text in logs:

```sh
uv run scripts/cf_observability_query.py --needle 'timeout' --minutes 120
```

### cf_analytics_query.py

Query Workers Analytics Engine datasets using the SQL API. This is for custom metrics written via `writeDataPoint()`, not request logs (use `cf_observability_query.py` for logs).

**Key Features:**

- Automatic semantic aliases for known datasets (e.g., `blob1` → `path`, `double1` → `latency_ms`)
- Built-in sampling-aware aggregation helpers
- Raw SQL mode for complex queries

**Schema for llms_usage dataset:**

| Raw Field | Semantic Name   | Description                                                                           |
| --------- | --------------- | ------------------------------------------------------------------------------------- |
| `index1`  | `method`        | HTTP method or "unauthorized"                                                         |
| `blob1`   | `path`          | Request path                                                                          |
| `blob2`   | `status`        | HTTP status code                                                                      |
| `blob3`   | `request_type`  | Category: provider, amp-tab, amp-telemetry, amp-admin, management, oauth, other       |
| `blob4`   | `provider`      | LLM provider: anthropic, google, openai, etc. (empty for non-provider requests)       |
| `blob5`   | `model`         | Model name from path (Gemini only; empty for Anthropic/OpenAI where model is in body) |
| `blob6`   | `client`        | Client identifier: "VS Code CLI", "VS Code Insiders", "Bun", "node", etc.             |
| `double1` | `latency_ms`    | Response time in milliseconds                                                         |
| `double2` | `input_tokens`  | Input/prompt tokens (non-streaming provider requests only; 0 for streaming)           |
| `double3` | `output_tokens` | Output/completion tokens (non-streaming provider requests only; 0 for streaming)      |

```sh
uv run scripts/cf_analytics_query.py [options]
```

**Options:**

- `--dataset NAME`: Analytics Engine dataset (default: llms_usage)
- `--minutes N`: Time range in minutes (default: 60)
- `--limit N`: Max results (default: 20)
- `--field FIELD`: Field to select (can be repeated). Omit for default fields with aliases.
- `--agg EXPR`: Aggregation expression (e.g., `SUM(_sample_interval) AS count`). Can be repeated.
- `--group-by FIELD`: Field to group by (can be repeated). Use with --agg.
- `--where CONDITION`: WHERE clause condition (can be repeated). E.g., `"blob2 = '401'"`
- `--order-by FIELD`: Field or alias to order by
- `--order {asc,desc}`: Sort order (default: desc)
- `--raw QUERY`: Execute raw SQL (ignores other query options)
- `--format {json,jsonl,tsv}`: Output format (default: json)
- `--show-query`: Print generated SQL
- `--show-schema`: Show schema mapping for dataset
- `--list-datasets`: List available datasets

**Examples:**

Show recent events with semantic field names:

```sh
uv run scripts/cf_analytics_query.py --limit 10
```

Request counts by path and status (last 24 hours):

```sh
uv run scripts/cf_analytics_query.py --agg 'SUM(_sample_interval) AS request_count' --group-by blob1 --group-by blob2 --minutes 1440
```

Average latency by method:

```sh
uv run scripts/cf_analytics_query.py --agg 'SUM(_sample_interval * double1) / SUM(_sample_interval) AS avg_latency_ms' --group-by index1
```

Filter by status code (show 401 errors):

```sh
uv run scripts/cf_analytics_query.py --where "blob2 = '401'" --minutes 1440
```

Raw SQL query:

```sh
uv run scripts/cf_analytics_query.py --raw "SELECT blob1, SUM(_sample_interval) AS count FROM llms_usage GROUP BY blob1 ORDER BY count DESC LIMIT 10"
```

**Sampling Notes:**

Analytics Engine may sample high-volume data. Always use `_sample_interval` for accurate counts:

- Count: `SUM(_sample_interval)` instead of `COUNT()`
- Sum: `SUM(_sample_interval * field)` instead of `SUM(field)`
- Average: `SUM(_sample_interval * field) / SUM(_sample_interval)` instead of `AVG(field)`

## Preferred Filter Keys

These keys are faster and always available:

- `$metadata.service`: Worker name
- `$metadata.origin`: Trigger type (fetch, scheduled, queue, etc.)
- `$metadata.trigger`: Request method and path (e.g., GET /users)
- `$metadata.message`: Log message text
- `$metadata.error`: Error message (when applicable)
- `$metadata.level`: Log level (log, warn, error)
- `$metadata.requestId`: Unique request identifier

## Regex Notes

For `regex` operations, Cloudflare uses ClickHouse RE2 syntax (not PCRE/JavaScript):

- No lookaheads/lookbehinds
- Escape backslashes with double backslash
