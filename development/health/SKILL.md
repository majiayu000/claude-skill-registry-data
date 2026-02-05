---
name: health
description: Soul system health check with remediation. Use to verify setup or diagnose issues.
execution: task
---

# Health

Spawn a Task agent to check soul health. This saves context.

## Execute

```
Task(
  subagent_type="general-purpose",
  description="Soul health check",
  prompt="""
Check the soul system health using MCP tools.

## 1. Get Status

Call these tools:
- mcp__soul__soul_context(format="json") - Get coherence and node statistics
- mcp__soul__harmonize() - Check voice agreement

## 2. Evaluate Health

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Coherence (tau_k) | > 0.7 | 0.5-0.7 | < 0.5 |
| Hot nodes % | > 50% | 30-50% | < 30% |
| Voice agreement | Yes | Partial | No |
| Mean voice coherence | > 60% | 40-60% | < 40% |

## 3. Remediate if Needed

If coherence is low or many cold nodes:
- mcp__soul__cycle(save=true) - Run decay, prune, recompute coherence

## 4. Report

Return a concise health report (8-10 lines):
- Overall status: Healthy / Warning / Critical
- Node count and hot/cold ratio
- Coherence scores (global, local, temporal, tau_k)
- Voice harmony (mean %, agreement)
- Any remediation actions taken
"""
)
```

After the agent returns, present the health report.
