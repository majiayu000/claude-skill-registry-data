---
name: cw-debug
disable-model-invocation: true
argument-hint: <log_group> <filter_pattern> <hours_back> <region> "<issue_description>"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /cw-debug — CloudWatch Log Investigation Skill

You are investigating a production issue using CloudWatch Logs Insights. Follow the structured methodology below, adapting queries based on what you discover in each phase.

## Arguments

The user will invoke this skill as:
```
/cw-debug <log_group> <filter_pattern> <hours_back> <region> "<issue_description>"
```

- `log_group`: The CloudWatch log group path (e.g., `/aws/ecs/my-service`)
- `filter_pattern`: Any string to filter logs — a user ID, request ID, service name, error code, or any identifier relevant to the investigation
- `hours_back`: How many hours of logs to search (e.g., `24`, `168` for 7 days)
- `region`: AWS region (e.g., `us-east-1`)
- `issue_description`: Free-text description of the problem being investigated (bug, performance issue, unexpected behavior, etc.)

## Setup

- Always use `.venv/bin/python` to run scripts
- The skill has its own self-contained CloudWatch utility at `${CLAUDE_PLUGIN_ROOT}/skills/cw-debug/scripts/cw.py`
- **Do NOT import from `cloudwatch_utils.py`** — use the skill's own module instead
- To use in inline scripts, add the scripts dir to `sys.path` then import:
  ```python
  import sys, os
  sys.path.insert(0, os.path.expanduser("${CLAUDE_PLUGIN_ROOT}/skills/cw-debug/scripts"))
  from cw import CWClient

  cw = CWClient(region="{region}")
  results = cw.query("{query}", hours_back={hours_back}, log_group="{log_group}")
  cw.print_table(results)
  ```
- Or use the CLI directly:
  ```bash
  .venv/bin/python ${CLAUDE_PLUGIN_ROOT}/skills/cw-debug/scripts/cw.py \
      --region {region} --log-group "{log_group}" --hours {hours_back} \
      --query "fields @timestamp, @message | limit 25"
  ```
- Available `CWClient` methods:
  - `cw.query(query_string, hours_back, log_group)` — single log group query
  - `cw.query_multi(query_string, hours_back, log_groups)` — query multiple log groups, merge results with `_log_group` tag
  - `CWClient.summarize_stats(results, value_field, group_field=None)` — compute count/avg/min/p50/p90/p95/p99/max from fetched results
  - `CWClient.time_bucket_counts(results, timestamp_field, bucket_minutes)` — group into time buckets for spike detection
  - `CWClient.print_table(results)` — ASCII table output
  - `CWClient.print_json(results)` — JSON output
  - `cw.save(results, name)` — save to `investigations/<name>.csv`
- Refer to `${CLAUDE_PLUGIN_ROOT}/skills/cw-debug/query_library.md` for pre-built query templates

## Rules

- **Analyze before querying**: After every query result, analyze the data and explain what you found before running the next query. Never chain queries blindly.
- **Adapt parse patterns**: Phase 1 reveals the actual log format. Use those discovered patterns (field names, delimiters, JSON structure) in all subsequent phases. Do NOT assume a log format before seeing real logs.
- **Do not write files unless user explicitly asks.** Print findings to stdout. Only save CSVs or reports when the user requests it.
- **Read the local codebase to correlate log findings with source code when investigating bugs.** Use Grep and Read to find relevant code paths that correspond to log patterns.
- **Be iterative**: If a phase reveals something unexpected, adjust the investigation plan. Skip strategies that don't apply; repeat queries with refined parameters if needed.

---

## Phase 1 — Reconnaissance (always runs)

**Goal**: Understand what's in the logs before writing targeted queries.

1. **Sample raw logs** — Fetch 20-30 raw log entries to see the actual format:
   ```
   fields @timestamp, @message
   | filter @message like /{filter_pattern}/
   | sort @timestamp desc
   | limit 25
   ```
2. **Read the raw logs carefully**. Identify:
   - Log format (JSON, key-value, plain text?)
   - Available field names and delimiters
   - What `parse` patterns will work
3. **Get message type distribution** — Count unique message types:
   ```
   fields @timestamp, @message
   | filter @message like /{filter_pattern}/
   | stats count(*) by msg
   ```
   (Adapt `msg` to whatever field holds the message type in the actual logs)
4. **Check log volume over time** to spot anomalies:
   ```
   filter @message like /{filter_pattern}/
   | stats count(*) as cnt by bin(1h)
   | sort bin asc
   ```
5. **Classify the issue type** based on logs and the issue description. Determine which category best fits:
   - **Error/Bug** — exceptions, failures, unexpected responses
   - **Performance** — slow responses, timeouts, high latency
   - **Data/Behavioral** — unexpected data, wrong outputs, logic issues
   - **Unknown** — insufficient signal, needs broader exploration

Summarize reconnaissance findings before moving on: log format, key fields, volume patterns, and issue classification.

---

## Phase 2 — Adaptive Investigation

**Goal**: Based on Phase 1 findings and the issue classification, select 2-4 strategies from the table below. Explain why each strategy was chosen before executing it.

| Strategy | When to use | What it does |
|---|---|---|
| Error Analysis | Errors or exceptions found in logs, or issue describes a bug | Count errors by type, examine temporal distribution, extract stack traces |
| Performance Analysis | Slow responses, timeouts, or latency mentioned in issue | Parse response times, compute percentiles, find slowest operations |
| Deep Trace | Need to understand the full lifecycle of a specific request or event | Trace a request/correlation ID through its complete lifecycle |
| Code Correlation | Bug or unexpected behavior, need to find root cause in source | Read local codebase to find code paths matching log patterns, identify potential root cause |
| Entity Tracking | Need to understand a specific user, session, or entity's experience | Trace all activity for a given identifier over time |
| Cross-Service | Evidence suggests the issue spans multiple services | Fan out to other log groups using `query_multi`, correlate timestamps |

### Error Analysis
- Filter for error-level logs, exceptions, HTTP 4xx/5xx, or failure keywords
- Count errors by type/message and bin by time intervals (5m or 15m) to find spikes
- Extract representative stack traces or error messages for the most frequent errors

### Performance Analysis
- Parse response times or duration fields from logs (adapt parse pattern to Phase 1 findings)
- Compute stats: count, avg, p50, p90, p95, p99, max using `CWClient.summarize_stats()`
- Identify the slowest operations and correlate with the reported issue timeline

### Deep Trace
- Pick 3-5 request or correlation IDs from prior findings (slowest, most errors, etc.)
- Query full lifecycle for each ID:
  ```
  fields @timestamp, @message
  | filter @message like /{request_id}/
  | sort @timestamp asc
  | limit 200
  ```
- Build a timeline of each request: identify where time was spent and what failed

### Code Correlation
- Use Grep to search the local codebase for function names, error messages, or log strings found in logs
- Read the matching source files to understand the code paths involved
- Identify potential root causes: missing error handling, race conditions, incorrect logic

### Entity Tracking
- Use the filter pattern or a discovered entity ID to trace all activity over the time window
- Build a chronological timeline of events for that entity
- Identify patterns: repeated retries, long gaps, error sequences, state transitions

### Cross-Service
- Identify related log groups from log content (references to other services, queue names, etc.)
- Use `cw.query_multi()` to query the same time windows or correlation IDs across multiple log groups
- Correlate timestamps to determine where the issue originates and how it propagates

---

## Phase 3 — Summary

**Goal**: Synthesize findings into a clear investigation summary.

Print to stdout:

1. **Root Cause / Hypotheses** — ranked by strength of evidence. If the root cause is clear, state it directly. If inconclusive, list top hypotheses with confidence levels.
2. **Supporting Evidence** — key log entries, patterns, and data points that support each hypothesis.
3. **Actionable Recommendations** — concrete next steps to fix, mitigate, or further investigate.

---

## Output

Print a concise investigation summary to stdout. If the user asks for a written report, use the RCA template at `${CLAUDE_PLUGIN_ROOT}/skills/cw-debug/rca_template.md`.
