---
name: chrome-devtools-performance-trace
description: Record and analyze Chrome performance traces via DevTools MCP. Capture CPU flame graphs, long tasks, layout thrash, and JS execution timelines. Extract actionable insights from trace data.
origin: https://github.com/ChromeDevTools/chrome-devtools-mcp (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Chrome DevTools Performance Trace

Record detailed performance traces and extract AI-analyzed insights using 3 MCP tracing tools.

## When to Use

- Profiling JS execution bottlenecks (long tasks, GC pauses, layout thrash)
- Identifying frame drops and jank during animations or scroll
- Measuring Time-to-Interactive (TTI) and Total Blocking Time (TBT)
- Comparing before/after performance for a specific code change
- Finding render-blocking work on the main thread

## Do NOT use for

- Simple LCP/FCP measurement (use `chrome-devtools-lcp-debug` — lighter weight)
- Memory leak detection (use `chrome-devtools-memory-leak` — heap snapshots)
- Network-only analysis (use `chrome-devtools-network-inspector`)

## MCP Tools (3)

```
browser_start_trace        — begin recording performance trace (CPU, network, rendering)
browser_stop_trace         — stop trace, returns raw trace JSON path
browser_trace_insights     — AI analysis of trace: top bottlenecks, actionable fixes
```

## Usage Pattern

```yaml
# Standard profiling flow
1. browser_navigate: url: "https://app.example.com"
2. browser_wait_for: networkIdle: true   # stable baseline

3. browser_start_trace:
     categories: ["devtools.timeline", "v8", "blink.user_timing"]

4. # perform the interaction to profile:
   browser_click: selector: "#load-data-button"
   browser_wait_for: selector: "[data-loaded]"

5. browser_stop_trace:
   # → returns: tracePath, duration, longTaskCount, totalBlockingTime

6. browser_trace_insights:
   # → returns: top 5 bottlenecks with file:line references + fix suggestions
```

## Trace Insight Output

```json
{
  "totalBlockingTime": 340,
  "longTasks": [
    {
      "duration": 180,
      "culprit": "bundle.js:4521 — processUserData()",
      "suggestion": "Chunk into async batches using scheduler.postTask()"
    },
    {
      "duration": 95,
      "culprit": "bundle.js:2103 — renderList() forced layout",
      "suggestion": "Read layout properties outside write loops (layout thrash)"
    }
  ],
  "gcPauseTotal": 45,
  "frameDrop": { "count": 12, "worst": 67 }
}
```

## Performance Budget Enforcement

```yaml
# Fail agent task if TBT exceeds budget
trace_result = browser_stop_trace()
if trace_result.totalBlockingTime > 200:
  report: "FAIL — TBT ${trace_result.totalBlockingTime}ms exceeds 200ms budget"
  browser_trace_insights: # get fix list
else:
  report: "PASS — TBT ${trace_result.totalBlockingTime}ms within budget"
```

## Key Metrics to Watch

| Metric | Good | Needs Work | Bad |
|--------|------|------------|-----|
| Total Blocking Time | < 200ms | 200–600ms | > 600ms |
| Longest task | < 50ms | 50–150ms | > 150ms |
| Layout thrash events | 0 | 1–3 | > 3 |
| GC pause total | < 50ms | 50–200ms | > 200ms |

## Anti-Fake-Pass Checklist

- [ ] `browser_start_trace` called on a fully-loaded page (after networkIdle)
- [ ] Interaction recorded BETWEEN start and stop — not before start
- [ ] `browser_trace_insights` used to parse results — not raw JSON eyeballing
- [ ] TBT and longTask data cross-checked against real user scenario, not idle page
- [ ] Trace categories include `devtools.timeline` for accurate main-thread data
