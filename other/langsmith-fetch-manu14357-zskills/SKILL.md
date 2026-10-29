---
name: langsmith-fetch
description: Debug LangChain and LangGraph agents by fetching execution traces from LangSmith. Analyze agent behavior, investigate errors, and review tool calls and performance metrics.
compatibility:
  use-case: Agent debugging, LLM workflow analysis, trace inspection
  frameworks: LangSmith, LangChain, LangGraph
---

# LangSmith Fetch — Agent Debugging

## Use This Skill When

- Debugging agent behavior to understand decision logic
- Investigating errors in LangChain or LangGraph applications
- Analyzing tool calls and their results
- Checking memory operations and long-term memory usage
- Examining agent performance (token usage, latency, cost)
- Reviewing recent traces to understand failure patterns
- Optimizing agent workflows based on execution data

## When NOT to Use

- Real-time production monitoring (use LangSmith dashboards)
- Tracing issues with LangSmith setup (consult LangSmith docs)
- Non-LangChain/LangGraph applications
- Live stream debugging (historical traces only)

## Context: Agent Debugging Capability Maturity

**Undeveloped**: Print logs manually; hard to trace agent decisions.

**Target**: Fetch recent traces programmatically, analyze tool calls, spot errors.

**Optimized**: Automatic anomaly detection, performance trends, cost optimization insights.

## Core Principle

**Traces tell the story.** Instead of guessing why an agent failed, fetch the execution trace, see exactly which tools were called with which inputs/outputs, and identify the failure point instantly.

## Instructions

### Step 1: Install and Configure

**Install CLI:**
```bash
pip install langsmith-fetch
```

**Set environment variables:**
```bash
export LANGSMITH_API_KEY="your_api_key"
export LANGSMITH_PROJECT="your_project_name"

# Verify setup
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT
```

**Get API key:**
- Visit https://smith.langchain.com
- Navigate to Settings → API Keys
- Copy and set as environment variable

### Step 2: Fetch Recent Traces

**Get traces from last N minutes:**

```bash
# Last 5 minutes (limit 5 traces)
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty

# Last 1 hour (limit 20 traces)
langsmith-fetch traces --last-n-hours 1 --limit 20 --format json > traces.json

# Last 7 days (all traces)
langsmith-fetch traces --last-n-days 7 --format json
```

**Output format:**

```markdown
## Recent Traces — LangSmith

### Trace 1: Agent-Query-2024-04-26-14:32:15
**Status**: ✅ SUCCESS
**Duration**: 2.3 seconds
**Tokens**: 412 input, 156 output (total: 568)
**Cost**: $0.012

### Trace 2: Agent-Query-2024-04-26-14:30:42
**Status**: ❌ ERROR
**Duration**: 5.1 seconds
**Tokens**: 345 input, 89 output (partial)
**Error**: Tool call returned None (tool: search_documents)

### Trace 3: Agent-Query-2024-04-26-14:28:03
**Status**: ✅ SUCCESS
**Duration**: 1.8 seconds
**Tokens**: 287 input, 124 output (total: 411)
**Cost**: $0.008
```

### Step 3: Analyze Trace Details

**Inspect specific trace:**

```bash
# Get details for a trace ID
langsmith-fetch trace-details \
  --trace-id "run-abc123def456" \
  --format pretty
```

**Trace breakdown:**

```markdown
## Trace Details: run-abc123def456

### Execution Flow

1️⃣ **Input Processing**
   - User Query: "Find recent AI news articles"
   - Elapsed: 0.1s
   - Tokens: 12 input

2️⃣ **Tool 1: search_news**
   - Input: { query: "artificial intelligence news", limit: 5 }
   - Duration: 1.2s
   - Output: [Article 1, Article 2, ...]
   - Tokens: 234 in/89 out

3️⃣ **Tool 2: summarize_articles**
   - Input: [Article 1, Article 2, ...]
   - Duration: 0.8s
   - Output: "Summary text..."
   - Tokens: 156 in/67 out

4️⃣ **Final Response**
   - Generated text: "Here are the latest articles..."
   - Total time: 2.3s
   - Total tokens: 412 in / 156 out

### Memory State (if applicable)
- Long-term memory accessed: 2 entries
- New memories saved: 1 entry
- Memory tokens: 45 in / 0 out
```

### Step 4: Identify Error Patterns

**Find failing traces:**

```bash
# Get only failed traces
langsmith-fetch traces \
  --status FAILED \
  --last-n-hours 24 \
  --limit 10 \
  --format pretty
```

**Analyze errors:**

```markdown
## Failed Trace Analysis

### Error Pattern: Tool Timeout (3 occurrences in 24h)
**Traces**: run-123, run-456, run-789
**Tool**: search_documents
**Common Pattern**: Query is complex (>100 tokens)
**Duration**: 5.0s (exceeded timeout)
**Recommendation**: Simplify query or increase timeout

### Error Pattern: Tool Returns None (2 occurrences)
**Traces**: run-234, run-567
**Tool**: fetch_weather_api
**Likely Cause**: API down or rate-limited
**Recommendation**: Add retry logic with exponential backoff

### Error Pattern: Agent Hallucination (1 occurrence)
**Trace**: run-890
**Tool**: search_database
**Issue**: Agent claimed tool returned [X], but actually returned [Y]
**Recommendation**: Add output validation before agent processing
```

### Step 5: Review Tool Call Patterns

**Analyze which tools are used most:**

```bash
# Get summary of tool usage
langsmith-fetch tool-stats --last-n-days 7 --format json | \
  jq -r '.[] | "\(.tool_name): \(.call_count) calls, \(.avg_duration)s avg"'
```

**Output:**
```
search_documents: 24 calls, 1.2s avg
send_email: 18 calls, 0.8s avg
fetch_user_data: 12 calls, 0.5s avg
calculate_score: 8 calls, 0.2s avg
```

**Find slow/expensive tools:**

```markdown
## Tool Performance Analysis (Last 7 Days)

| Tool | Calls | Avg Duration | Total Cost | Success Rate |
|------|-------|--------------|-----------|--------------|
| search_documents | 24 | 1.2s | $0.18 | 92% |
| send_email | 18 | 0.8s | $0.04 | 100% |
| fetch_user_data | 12 | 0.5s | $0.02 | 100% |
| calculate_score | 8 | 0.2s | $0.01 | 100% |

**Opportunities for optimization**:
- search_documents: Lowest success rate; consider caching
- send_email: Relatively slow; batch if possible
- Overall cost: $0.25/day = $7.50/month for this project
```

### Step 6: Examine Memory Operations

**Check long-term memory usage:**

```bash
# Get memory activity
langsmith-fetch memory-ops \
  --last-n-hours 24 \
  --format pretty
```

**Analysis:**

```markdown
## Memory Operations (Last 24 Hours)

### Writes
- Saved 12 new memories
- Updated 3 existing memories
- Deleted 1 memory (expired)
- Total: 16 operations

### Reads
- Accessed memory 8 times
- Retrieved 3-5 memories per access
- Memory hit rate: 78% (relevant memories found)

### Issues
- ⚠️ One memory write failed (auth error)
- ⚠️ Memory retrieval slow (1.2s avg) — consider indexing
```

### Step 7: Generate Debugging Report

**Create actionable insights:**

```markdown
# Agent Debugging Report — April 26, 2026

## Summary
- Total traces analyzed: 47
- Success rate: 85%
- Avg performance: 2.1s per query
- Avg cost: $0.012 per query

## Issues Found

### Critical ❌
1. **Tool Timeout Pattern** (3 failures)
   - Tool: search_documents
   - Root cause: Complex queries exceed timeout
   - Fix: Increase timeout from 5s to 10s, or simplify query decomposition
   - Impact: Fixes ~6% of failures

2. **Memory Retrieval Slow** (1.2s avg)
   - Root cause: Sequential lookup of 100+ memories
   - Fix: Add vector index to memory store
   - Impact: Would reduce agent latency by ~40%

### Medium ⚠️
3. **Tool Success Rate Variance**
   - search_documents: 92% success
   - send_email: 100% success
   - Recommendation: Add retries for search_documents

## Optimization Opportunities

| Opportunity | Effort | Impact | Priority |
|-----------|--------|--------|----------|
| Add vector index for memory | Medium | 40% latency ↓ | High |
| Increase search timeout | Low | 6% failures ↓ | Medium |
| Batch email sends | Medium | 20% cost ↓ | Medium |
| Simplify query decomposition | High | 30% latency ↓ | Low |

## Next Steps
- [ ] Implement vector index for memory
- [ ] Test with increased timeout (5s → 10s)
- [ ] Monitor failure rate post-fix
- [ ] Consider query simplification if still hitting timeout
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **API key not set** | Run `export LANGSMITH_API_KEY="key"` and verify with `echo $LANGSMITH_API_KEY` |
| **Project name missing** | Set `export LANGSMITH_PROJECT="project-name"` from LangSmith dashboard |
| **No traces found** | Ensure agent ran recently; traces visible within 30s |
| **Outdated data** | Traces may lag; wait 1-2 min and retry fetch |

## Output

**Deliver:**

1. **Trace Summary** (count, status, duration, cost)
2. **Error Analysis** (patterns identified, failure causes)
3. **Tool Performance** (usage, speed, success rates)
4. **Memory Operations** (read/write patterns, bottlenecks)
5. **Optimization Report** (recommendations with impact estimates)