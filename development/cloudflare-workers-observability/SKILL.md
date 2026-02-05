---
name: Cloudflare Workers Observability
description: This skill should be used when the user asks about "worker logs", "debug worker", "worker errors", "request analytics", "worker metrics", "performance monitoring", "error rate", "invocation logs", "troubleshoot worker", "worker analytics", or needs to debug and monitor Cloudflare Workers.
version: 1.0.0
---

# Cloudflare Workers Observability

Debug and monitor Cloudflare Workers using logs and analytics from the Observability MCP server.

## Available Tools

| Tool | Purpose |
|------|---------|
| `query_worker_observability` | Query logs and metrics from Workers |
| `observability_keys` | Discover available data fields in logs |
| `observability_values` | Find available values for specific fields |

## Query Workflow

### 1. Discover Available Fields
Use `observability_keys` to find what data is available:
- Metadata fields (timestamps, status codes)
- Worker-specific fields (script name, route)
- Custom logged fields from console.log

### 2. Explore Field Values
Use `observability_values` to find valid values for filtering:
- Status codes present in logs
- Script names deployed
- Custom field values

### 3. Query Logs and Metrics
Use `query_worker_observability` to:
- List recent events/invocations
- Calculate metrics (error rates, latency)
- Find specific invocations by criteria

## Common Queries

| Goal | Approach |
|------|----------|
| Recent errors | Query for events with error status |
| Latency analysis | Query for execution time metrics |
| Traffic patterns | Query for invocation counts over time |
| Specific request | Query by request ID or timestamp |
| Script comparison | Query metrics grouped by script name |

## Debugging Workflow

1. **Identify the problem**
   - Query recent errors with `query_worker_observability`

2. **Find patterns**
   - Use `observability_keys` to discover relevant fields
   - Use `observability_values` to see error types

3. **Narrow down**
   - Add filters for specific routes, times, or status codes

4. **Analyze specific invocations**
   - Query for detailed logs of problematic requests

## Post-Deployment Monitoring

After deploying, check for issues:
1. Query for errors in the last 5-10 minutes
2. Compare error rates before/after deployment
3. Check latency metrics for performance regression

## Tips

- Start broad, then add filters to narrow results
- Use `observability_keys` when unsure what fields exist
- Custom console.log output appears in queryable fields
- Combine with builds tools to correlate issues with deployments
