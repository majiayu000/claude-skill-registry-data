---
name: filtering-event-datasets
description: Filter and search event datasets (logs) using OPAL. Use when you need to find specific log events by text search, regex patterns, or field values. Covers contains(), tilda operator ~, field comparisons, boolean logic, and limit for sampling results. Does NOT cover aggregation (see aggregating-event-datasets skill).
---

# Filtering Event Datasets

Event datasets (logs) represent point-in-time occurrences with a single timestamp. This skill teaches you how to filter and search log data to find specific events using OPAL.

## When to Use This Skill

- Searching logs for specific text patterns (errors, warnings, exceptions)
- Finding logs matching a regex pattern (log levels, error codes, structured formats)
- Filtering by field values (namespace, pod, container, stream, severity)
- Combining multiple filter conditions with boolean logic
- Sampling raw log events for investigation

## Prerequisites

- Access to Observe tenant via MCP
- Understanding that Events have a single timestamp (not duration)
- Dataset with `log` interface (or any Event dataset)

## Key Concepts

### Event Datasets

Event datasets represent discrete occurrences at specific points in time. Unlike Intervals (which have start/end times), Events are instantaneous observations.

**Characteristics:**
- Single `timestamp` field (sometimes named `time`, `eventTime`, etc.)
- Commonly used for logs
- Interface type often `log`
- High volume, text-heavy data

### Common Field Structure

Most log datasets follow this pattern:
- `body`, `message`, or `log` - The actual log message text
- `timestamp`, `time`, `eventTime`, etc - When the log occurred
- `resource_attributes.*` or `labels` - Nested metadata about the source
- Standard fields like `cluster`, `namespace`, `pod`, `container`, `stream`, `level`

### Nested Field Access

Fields with dots in their names MUST be quoted:
```opal
resource_attributes."k8s.namespace.name"  ✓ Correct
resource_attributes.k8s.namespace.name    ✗ Wrong
```

## Discovery Workflow

Always start by finding and exploring your log dataset.

**Step 1: Search for log datasets**

```
discover_context("logs kubernetes")
```

Look for datasets with interface type `log` or category "Logs".

**Step 2: Get detailed schema**

```
discover_context(dataset_id="YOUR_DATASET_ID")
```

Note the exact field names (case-sensitive!) and nested field structure. Pay attention to:
- The `body`, `message`, `log`, or similar field for main log content
- `resource_attributes.*`, `labels` or other nested objects for dimensions
- Fields like `namespace`, `pod`, `container`, `stream`, `level`

## Basic Patterns

### Pattern 1: Simple Text Search

**Use case**: Find logs containing specific text

```opal
filter contains(body, "error")
| limit 100
```

**Explanation**: Searches the `body` field for the substring "error" and returns the first 100 matching logs in their default order (typically reverse chronological, most recent first).

**When to use**: Quick text search to find recent examples of specific log messages.

### Pattern 2: Case-Insensitive Regex Search

**Use case**: Find logs matching a pattern regardless of case

```opal
filter body ~ /error/i
| limit 100
```

**Explanation**: Uses regex operator `~` with forward slashes `/pattern/` for POSIX ERE pattern matching. The `/i` flag makes matching case-insensitive (matches "error", "ERROR", "Error", etc.). Without `/i`, matching is case-sensitive.

**Regex syntax**:
- `/pattern/` - Case-sensitive regex
- `/pattern/i` - Case-insensitive regex
- POSIX Extended Regular Expression (ERE) syntax
- Special chars need escaping: `/\[ERROR\]/` to match literal "[ERROR]"

### Pattern 3: Structured Pattern Matching

**Use case**: Find logs matching a specific format (log levels, codes, structured fields)

```opal
filter body ~ /level=warn/i
| limit 100
```

**Explanation**: Matches logs containing "level=warn" (case-insensitive). Useful for structured logging formats with key=value pairs.

**More examples**:
```opal
# Match HTTP status codes
filter body ~ /status=[45][0-9]{2}/

# Match IP addresses
filter body ~ /[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/

# Match specific log levels
filter body ~ /\[WARN\]|\[ERROR\]/  # Note: May have issues with MCP tool due to pipe
```

### Pattern 4: Field-Based Filtering

**Use case**: Filter by specific field values (not text search)

```opal
filter stream = "stderr"
| limit 100
```

**Explanation**: Filters logs written to stderr stream. Field comparisons use `=`, `!=`, `>`, `<`, `>=`, `<=` operators.

**More examples**:
```opal
# Filter by namespace (nested field)
filter string(resource_attributes."k8s.namespace.name") = "production"
| limit 100

# Filter by pod
filter pod = "api-gateway-abc123"
| limit 100
```

### Pattern 5: Multiple Conditions

**Use case**: Combine multiple filters with boolean logic

```opal
filter (contains(body, "error") or contains(body, "exception"))
| filter string(resource_attributes."k8s.namespace.name") = "production"
| limit 100
```

**Explanation**: Chains multiple filters together. First filters for text content (error OR exception), then filters for specific namespace. Each `filter` verb can be chained with `|`.

**Boolean operators**:
- `and` - Both conditions must be true
- `or` - At least one condition must be true
- `not` - Negates a condition

**More examples**:
```opal
# Multiple fields
filter namespace = "production" and stream = "stderr"
| limit 100

# Negation
filter not contains(body, "debug")
| limit 100

# Complex conditions
filter (level = "error" or level = "warn") and namespace != "test"
| limit 100
```

## Complete Example

End-to-end workflow for finding recent errors in production.

**Scenario**: You need to investigate errors in the production namespace from the last hour.

**Step 1: Discovery**

```
discover_context("kubernetes logs")
```

Found: Dataset "Kubernetes Explorer/Kubernetes Logs" (ID: 42161740) with interface `log`

**Step 2: Get schema details**

```
discover_context(dataset_id="42161740")
```

Key fields identified: `body`, `namespace`, `pod`, `container`, `stream`, `resource_attributes.*`

**Step 3: Build query**

```opal
filter (contains(body, "error") or contains(body, "ERROR"))
| filter string(resource_attributes."k8s.namespace.name") = "production"
| filter stream = "stderr"
| limit 100
```

**Step 4: Execute**

```
execute_opal_query(
    query="[query above]",
    primary_dataset_id="42161740",
    time_range="1h"
)
```

**Step 5: Interpret results**

Returns up to 100 most recent logs (reverse chronological) that:
- Contain "error" or "ERROR" in the body
- Are from the production namespace
- Were written to stderr

You can now examine these logs to identify the issue.

## Common Pitfalls

### Pitfall 1: Not Quoting Nested Fields

❌ **Wrong**:
```opal
filter resource_attributes.k8s.namespace.name = "production"
```

✅ **Correct**:
```opal
filter string(resource_attributes."k8s.namespace.name") = "production"
```

**Why**: Field names containing dots must be quoted. Also wrap in `string()` for type safety.

### Pitfall 2: Using String Quotes for Regex

❌ **Wrong**:
```opal
filter body ~ "error[0-9]+"  # This is string matching, not regex
```

✅ **Correct**:
```opal
filter body ~ /error[0-9]+/  # Forward slashes for regex
```

**Why**: Regex patterns must use forward slashes `/pattern/`. Double quotes are for string literals.

### Pitfall 3: Forgetting Case Sensitivity

❌ **Wrong**:
```opal
filter contains(body, "Error")  # Only finds "Error", not "error" or "ERROR"
```

✅ **Correct**:
```opal
# Option 1: Multiple conditions
filter contains(body, "error") or contains(body, "Error") or contains(body, "ERROR")

# Option 2: Case-insensitive regex
filter body ~ /error/i
```

**Why**: `contains()` is case-sensitive. Use regex with `/i` flag for case-insensitive matching.

### Pitfall 4: Confusing limit with topk

❌ **Wrong** (for filtered raw events):
```opal
filter contains(body, "error")
| topk 100, max(timestamp)  # topk is for aggregated results!
```

✅ **Correct**:
```opal
filter contains(body, "error")
| limit 100  # limit is for raw events
```

**Why**: `limit` returns the first N results in their current order (for raw events). `topk` is for aggregated results (see aggregating-event-datasets skill).

## Tips and Best Practices

- **Start broad, then narrow**: Begin with simple filters, add specificity iteratively
- **Use `limit` for sampling**: Always add `| limit N` when exploring to avoid overwhelming results
- **Default ordering**: Events are typically ordered reverse chronological (most recent first)
- **Check field names**: Use `discover_context()` to get exact field names (case-sensitive!)
- **Quote nested fields**: Any field with dots in the name must be quoted
- **Type conversion**: Wrap nested fields in `string()`, `int64()`, etc. for type safety
- **Test patterns**: Use small time ranges (1h) when developing queries
- **Regex testing**: Test regex patterns with simple examples first before adding to complex queries

## Regex Reference

**Common POSIX ERE patterns**:
- `.` - Any character
- `*` - Zero or more of previous
- `+` - One or more of previous
- `?` - Zero or one of previous
- `[abc]` - Character class (a, b, or c)
- `[0-9]` - Digit
- `[a-z]` - Lowercase letter
- `^` - Start of line
- `$` - End of line
- `\` - Escape special character

**Flags**:
- `/i` - Case-insensitive
- Default (no flag) - Case-sensitive

## Additional Resources

For more details, see:
- [RESEARCH.md](../../RESEARCH.md) - Tested patterns and findings
- [OPAL Documentation](https://docs.observeinc.com/en/latest/content/query-language-reference/) - Official OPAL docs

## Related Skills

- [aggregating-event-datasets] - For summarizing events with statsby, make_col, group_by
- [time-series-analysis] - For trending events over time with timechart
- [working-with-nested-fields] - Deep dive on nested field access

---

**Last Updated**: November 14, 2025
**Version**: 2.0 (Split from combined skill)
**Tested With**: Observe OPAL v2.x
