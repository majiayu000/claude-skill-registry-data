---
name: langfuse-advanced-filters
description: Precisely filter and query Langfuse traces/observations using advanced filter operators for debugging and optimization workflows
allowed-tools: "*"
---

# Langfuse Advanced Filters Skill

Leverage Langfuse's new advanced filtering API to perform surgical, precise queries on traces and observations. Perfect for debugging specific issues, analyzing performance patterns, and optimizing workflows with exact filter criteria.

## When to Use This Skill

- "Find all traces with latency > 5 seconds for case 0001"
- "Show me observations where the edit node failed validation"
- "Get traces with metadata case_id=0001 AND profile_name='The Prep'"
- "Find all ERROR level observations from the last 24 hours"
- "Query traces where custom_metric > threshold"
- "Analyze traces with specific tag combinations"
- "Debug why tool selection is failing for financial topics"

## What Makes This Different

**Existing langfuse-optimization skill**: Great for config analysis, but uses simple tag/name filters
**This skill**: Surgical precision with advanced operators (`>`, `<`, `=`, `contains`, etc.) and complex filter combinations

## Advanced Filter Capabilities

### Filter Operators

Based on Langfuse Launch Week 4 (Oct 2025), the API now supports:

- `=` - Exact match
- `>` - Greater than (numeric, datetime)
- `<` - Less than (numeric, datetime)
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `contains` - String contains (case-sensitive)
- `not_contains` - String does not contain
- `in` - Value in list
- `not_in` - Value not in list
I
### Filter Structure

```json
{
  "column": "string",      // Column to filter on (e.g., "name", "level", "metadata")
  "operator": "string",    // Operator (=, >, <, contains, etc.)
  "value": "any",          // Value to compare against
  "type": "string",        // Data type: "string", "number", "stringObject", "datetime"
  "key": "string"          // Required for metadata filters (e.g., "case_id")
}
```

### Filterable Fields

**Traces**:
- `name` - Trace name
- `user_id` - User identifier
- `session_id` - Session identifier
- `tags` - Tags array
- `metadata` - Custom metadata (use `key` parameter)
- `timestamp` - Trace timestamp
- `input` - Input data
- `output` - Output data

**Observations**:
- `name` - Observation name
- `type` - Observation type (SPAN, GENERATION, EVENT)
- `level` - Log level (DEBUG, DEFAULT, WARNING, ERROR)
- `trace_id` - Parent trace ID
- `parent_observation_id` - Parent observation ID
- `start_time` - Observation start time
- `end_time` - Observation end time
- `metadata` - Custom metadata (use `key` parameter)
- `latency` - Computed latency (ms)

## Required Environment Variables

- `LANGFUSE_PUBLIC_KEY`: Your Langfuse public API key
- `LANGFUSE_SECRET_KEY`: Your Langfuse secret API key
- `LANGFUSE_HOST`: Langfuse host URL (default: https://cloud.langfuse.com)

## Workflow

### Step 1: Understand User's Query Intent

Ask clarifying questions to build precise filters:

**For debugging**:
- What specific issue are you investigating?
- What time range? (last hour, last 24h, specific date range)
- Any known trace IDs or patterns?
- Which component/node is problematic?

**For optimization**:
- What metric are you optimizing? (latency, error rate, check failures)
- What threshold defines "problematic"? (> 5s, < 0.7 score)
- Which case or workflow?
- Do you need aggregated metrics or individual traces?

**For analysis**:
- What pattern are you looking for?
- Do you need comparison across time periods?
- Should results be grouped by metadata field?

### Step 2: Build Filter Query

Use the advanced filter helpers to construct precise queries:

#### Helper A: Query Traces with Advanced Filters

```bash
cd /home/user/writing_ecosystem/.claude/skills/langfuse-advanced-filters/helpers

# Example 1: Find slow traces (latency > 5000ms) for a specific case
python3 query_with_filters.py \
  --view traces \
  --filters '[
    {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
    {"column": "latency", "operator": ">", "value": 5000, "type": "number"}
  ]' \
  --from-date "2025-11-01" \
  --to-date "2025-11-04" \
  --limit 50 \
  --output /tmp/langfuse_queries/slow_traces.json

# Example 2: Find ERROR level observations in edit node
python3 query_with_filters.py \
  --view observations \
  --filters '[
    {"column": "name", "operator": "=", "value": "edit_node", "type": "string"},
    {"column": "level", "operator": "=", "value": "ERROR", "type": "string"}
  ]' \
  --from-date "2025-11-03" \
  --limit 100 \
  --output /tmp/langfuse_queries/edit_errors.json

# Example 3: Complex AND filter - case AND profile AND time range
python3 query_with_filters.py \
  --view traces \
  --filters '[
    {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
    {"column": "metadata", "operator": "=", "key": "profile_name", "value": "The Prep", "type": "stringObject"},
    {"column": "timestamp", "operator": ">=", "value": "2025-11-03T00:00:00Z", "type": "datetime"}
  ]' \
  --limit 25 \
  --output /tmp/langfuse_queries/prep_case_traces.json

# Example 4: Find traces with specific tags AND name pattern
python3 query_with_filters.py \
  --view traces \
  --filters '[
    {"column": "name", "operator": "contains", "value": "workflow", "type": "string"},
    {"column": "tags", "operator": "contains", "value": "production", "type": "string"}
  ]' \
  --from-date "2025-11-01" \
  --output /tmp/langfuse_queries/prod_workflows.json
```

**Output**: JSON file with filtered traces/observations matching ALL criteria (AND logic)

#### Helper B: Query Metrics with Filters (Aggregated Analysis)

For aggregated insights, use the Metrics API with filters:

```bash
cd /home/user/writing_ecosystem/.claude/skills/langfuse-advanced-filters/helpers

# Example 1: Average latency by case_id, filtered by time range
python3 query_metrics.py \
  --view traces \
  --metrics '[{"measure": "latency", "aggregation": "avg"}]' \
  --dimensions '[{"field": "metadata.case_id"}]' \
  --filters '[
    {"column": "metadata", "operator": "!=", "key": "case_id", "value": null, "type": "stringObject"}
  ]' \
  --from-date "2025-11-01" \
  --to-date "2025-11-04" \
  --output /tmp/langfuse_queries/latency_by_case.json

# Example 2: Error count by observation name (which nodes fail most?)
python3 query_metrics.py \
  --view observations \
  --metrics '[{"measure": "count", "aggregation": "count"}]' \
  --dimensions '[{"field": "name"}]' \
  --filters '[
    {"column": "level", "operator": "=", "value": "ERROR", "type": "string"}
  ]' \
  --from-date "2025-11-01" \
  --output /tmp/langfuse_queries/error_counts.json

# Example 3: P95 latency histogram for specific case (performance distribution)
python3 query_metrics.py \
  --view traces \
  --metrics '[{"measure": "latency", "aggregation": "p95"}]' \
  --filters '[
    {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"}
  ]' \
  --from-date "2025-10-01" \
  --to-date "2025-11-04" \
  --time-granularity "day" \
  --output /tmp/langfuse_queries/latency_p95_trend.json

# Example 4: Count traces by user, filtered by metadata
python3 query_metrics.py \
  --view traces \
  --metrics '[{"measure": "count", "aggregation": "count"}]' \
  --dimensions '[{"field": "userId"}]' \
  --filters '[
    {"column": "metadata", "operator": "=", "key": "workflow_version", "value": "2", "type": "stringObject"}
  ]' \
  --from-date "2025-11-01" \
  --output /tmp/langfuse_queries/user_trace_counts.json
```

**Output**: Aggregated metrics grouped by dimensions

#### Helper C: Build Filter JSON (Interactive Builder)

For complex queries, use the interactive builder:

```bash
cd /home/user/writing_ecosystem/.claude/skills/langfuse-advanced-filters/helpers

# Interactive mode
python3 build_filters.py --interactive

# Or programmatic mode
python3 build_filters.py \
  --add-filter '{"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"}' \
  --add-filter '{"column": "latency", "operator": ">", "value": 3000, "type": "number"}' \
  --validate \
  --output /tmp/langfuse_queries/my_filters.json
```

### Step 3: Analyze Results

Once you have filtered data, extract insights:

```bash
cd /home/user/writing_ecosystem/.claude/skills/langfuse-advanced-filters/helpers

# Analyze filtered traces for patterns
python3 analyze_filtered_results.py \
  --input /tmp/langfuse_queries/slow_traces.json \
  --analysis-type latency-breakdown \
  --output /tmp/langfuse_queries/analysis_report.json

# Compare two filter result sets
python3 analyze_filtered_results.py \
  --input /tmp/langfuse_queries/before_fix.json \
  --compare /tmp/langfuse_queries/after_fix.json \
  --analysis-type comparison \
  --output /tmp/langfuse_queries/comparison_report.json
```

### Step 4: Generate Insights Report

Synthesize findings into actionable recommendations:

```markdown
# Filter Query Results - [Query Description]

**Query**: [Natural language description]
**Filters Applied**:
```json
[Show filter JSON]
```

**Results**:
- Total matches: X traces / Y observations
- Time range: [start] to [end]
- Key patterns:
  1. [Pattern 1 with counts]
  2. [Pattern 2 with counts]

---

## Findings

### Issue #1: [Title]
**Severity**: High/Medium/Low
**Frequency**: X occurrences (Y% of filtered set)
**Pattern**: [Description]

**Evidence**:
- Trace IDs: [list top 3-5]
- Common metadata: [shared values]
- Time distribution: [pattern]

**Root Cause Hypothesis**:
[Analysis based on filtered data]

**Recommended Fix**:
[Specific action item]

---

## Next Steps

1. [Action item 1]
2. [Action item 2]
3. [Follow-up query to validate fix]
```

## Common Use Cases

### Use Case 1: Debug Slow Workflows

**Query**: "Why are traces for case 0001 suddenly taking >10s?"

**Filters**:
```json
[
  {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
  {"column": "timestamp", "operator": ">=", "value": "2025-11-03T00:00:00Z", "type": "datetime"},
  {"column": "latency", "operator": ">", "value": 10000, "type": "number"}
]
```

**Analysis**:
1. Retrieve matching traces
2. Extract observations for each trace
3. Compare node latencies
4. Identify bottleneck node (research, write, edit)

### Use Case 2: Find Failing Validation Checks

**Query**: "Which traces have failing style checks for tone_consistency?"

**Approach**:
1. Filter traces by case
2. Get edit node observations
3. Extract validation_report from output
4. Count tone_consistency failures

**Filters**:
```json
[
  {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
  {"column": "name", "operator": "contains", "value": "edit", "type": "string"}
]
```

### Use Case 3: Analyze Tool Selection Patterns

**Query**: "Is the research node selecting finnhub for financial topics?"

**Filters**:
```json
[
  {"column": "name", "operator": "contains", "value": "research", "type": "string"},
  {"column": "metadata", "operator": "contains", "key": "topic", "value": "stock", "type": "stringObject"}
]
```

**Analysis**:
1. Extract tool selection from research node output
2. Count finnhub vs other tools
3. Identify cases where finnhub was NOT selected but should have been

### Use Case 4: Performance Regression Detection

**Query**: "Did latency increase after deploying new workflow version?"

**Strategy**:
1. Query metrics for workflow_version=1 (before)
2. Query metrics for workflow_version=2 (after)
3. Compare p95 latency

**Filters (Before)**:
```json
[
  {"column": "metadata", "operator": "=", "key": "workflow_version", "value": "1", "type": "stringObject"},
  {"column": "timestamp", "operator": ">=", "value": "2025-10-01", "type": "datetime"},
  {"column": "timestamp", "operator": "<", "value": "2025-10-15", "type": "datetime"}
]
```

**Filters (After)**:
```json
[
  {"column": "metadata", "operator": "=", "key": "workflow_version", "value": "2", "type": "stringObject"},
  {"column": "timestamp", "operator": ">=", "value": "2025-10-15", "type": "datetime"}
]
```

### Use Case 5: Error Spike Investigation

**Query**: "Why did ERROR observations spike in the last 6 hours?"

**Filters**:
```json
[
  {"column": "level", "operator": "=", "value": "ERROR", "type": "string"},
  {"column": "start_time", "operator": ">=", "value": "2025-11-04T12:00:00Z", "type": "datetime"}
]
```

**Analysis**:
1. Group errors by observation name (which node?)
2. Group by trace_id to find affected workflows
3. Extract error messages from status_message
4. Identify common patterns

## Filter Syntax Reference

### Metadata Filters

Metadata filters require special syntax:

```json
{
  "column": "metadata",
  "operator": "=",           // or ">", "<", "contains", etc.
  "key": "your_metadata_key", // REQUIRED for metadata
  "value": "expected_value",
  "type": "stringObject"     // Always "stringObject" for metadata
}
```

**Example metadata keys** (from writing ecosystem):
- `case_id` - Case identifier (0001, 0002, etc.)
- `profile_name` - Profile name ("The Prep", "Stock Deep Dive")
- `workflow_version` - Workflow version number
- `langgraph_node` - Node name
- `langgraph_step` - Step number
- `topic` - Topic string
- `style_id` - Style identifier

### Combining Multiple Filters

All filters in the array are combined with **AND logic**:

```json
[
  {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
  {"column": "level", "operator": "=", "value": "ERROR", "type": "string"},
  {"column": "latency", "operator": ">", "value": 5000, "type": "number"}
]
```
→ Matches: `case_id=0001 AND level=ERROR AND latency>5000`

### Time Range Filters

Two approaches:

**Approach 1: Query-level parameters** (recommended):
```bash
--from-date "2025-11-01T00:00:00Z"
--to-date "2025-11-04T23:59:59Z"
```

**Approach 2: Filter-level** (for precise control):
```json
[
  {"column": "timestamp", "operator": ">=", "value": "2025-11-01T00:00:00Z", "type": "datetime"},
  {"column": "timestamp", "operator": "<=", "value": "2025-11-04T23:59:59Z", "type": "datetime"}
]
```

### Numeric Comparisons

```json
// Latency greater than 5 seconds
{"column": "latency", "operator": ">", "value": 5000, "type": "number"}

// Token count less than 1000
{"column": "usage_total", "operator": "<", "value": 1000, "type": "number"}

// Score exactly 8.5
{"column": "value", "operator": "=", "value": 8.5, "type": "number"}
```

### String Operations

```json
// Name contains "workflow"
{"column": "name", "operator": "contains", "value": "workflow", "type": "string"}

// Name exactly matches
{"column": "name", "operator": "=", "value": "write_node", "type": "string"}

// User ID in list
{"column": "user_id", "operator": "in", "value": ["user1", "user2", "user3"], "type": "string"}
```

## Tips & Best Practices

### 1. Start Broad, Then Narrow

```bash
# Step 1: Find all traces for case
python3 query_with_filters.py --view traces \
  --filters '[{"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"}]' \
  --limit 100

# Step 2: Narrow to slow traces
python3 query_with_filters.py --view traces \
  --filters '[
    {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
    {"column": "latency", "operator": ">", "value": 5000, "type": "number"}
  ]' \
  --limit 50
```

### 2. Use Metrics API for Aggregation

Don't retrieve 1000 traces just to count them - use metrics:

```bash
# WRONG: Retrieve all traces and count in Python
python3 query_with_filters.py --view traces --limit 1000 | wc -l

# RIGHT: Use metrics API
python3 query_metrics.py --view traces \
  --metrics '[{"measure": "count", "aggregation": "count"}]' \
  --dimensions '[{"field": "metadata.case_id"}]'
```

### 3. Validate Filters Before Large Queries

```bash
# Test with small limit first
python3 query_with_filters.py --filters '[...]' --limit 5

# Once validated, increase limit
python3 query_with_filters.py --filters '[...]' --limit 500
```

### 4. Save Filter Definitions

```bash
# Save complex filters for reuse
cat > /tmp/my_filters/slow_case_0001.json <<EOF
[
  {"column": "metadata", "operator": "=", "key": "case_id", "value": "0001", "type": "stringObject"},
  {"column": "latency", "operator": ">", "value": 5000, "type": "number"}
]
EOF

# Reuse saved filters
python3 query_with_filters.py --filters-file /tmp/my_filters/slow_case_0001.json
```

### 5. Combine with Existing Skills

```bash
# Step 1: Use advanced filters to find problematic traces (THIS SKILL)
python3 query_with_filters.py --filters '[...]' --output /tmp/filtered_traces.json

# Step 2: Analyze those traces with langfuse-optimization skill
# (Switch to langfuse-optimization skill with filtered trace IDs)
```

## Troubleshooting

**"No results returned"**:
- Verify filters are correct (check column names, types)
- Try broader time range
- Remove filters one by one to isolate issue
- Check if data exists with basic query first

**"Invalid filter syntax"**:
- Ensure JSON is valid (use `python3 build_filters.py --validate`)
- Check `type` matches data type (string, number, datetime, stringObject)
- For metadata, ensure `key` is specified

**"Query timeout"**:
- Reduce time range
- Add more specific filters
- Use pagination (multiple queries with smaller limits)

**"Metadata filter not working"**:
- Ensure `type` is `"stringObject"` (not `"string"`)
- Verify `key` matches exact metadata field name
- Check metadata exists in traces (inspect raw trace first)

## Success Criteria

Good queries should:
1. ✅ Use precise filters (not retrieving 10x more data than needed)
2. ✅ Combine multiple filters for surgical precision
3. ✅ Validate results match expectation
4. ✅ Lead to actionable insights (not just data dumps)
5. ✅ Be reproducible (save filter definitions)

---

**Remember**: This skill is about **precision filtering**, not general trace analysis. Use it when you need:
- Exact matching criteria
- Numeric thresholds
- Complex AND conditions
- Metadata-based filtering
- Aggregated metrics

For general config optimization, use the `langfuse-optimization` skill instead.
