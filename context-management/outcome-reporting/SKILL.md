---
name: outcome-reporting
description: Report task outcomes after using recall/search results so engram can measure whether memory helps. Trigger after completing a task that used recall, search, or symbol_context results.
---

# Outcome Reporting Skill

When you use engram's `recall`, `search`, or `symbol_context` to find information
and then complete a task based on that information, report the outcome.

## When to report

After completing ANY task where you used engram retrieval results:
- Found the right file/symbol → report success
- Found partial information → report success with note
- Found nothing useful → report failure
- Found WRONG information → report failure (interference data!)

## How to report

```
report_outcome({
    "query_id": "<from the recall response header>",
    "success": true|false,
    "capability": "<what task you were doing>",
    "recalled_targets": ["<symbols/files that helped>"],
    "verifier": "<your agent name>"
})
```

## Why this matters

Every outcome feeds the ΔP measurement — the proof that memory improves
agent performance. Report honestly: failures are MORE valuable than
successes because they identify interference and gaps.

## Check the aggregate

Run `outcome_report` periodically to see success rates by capability
and interference candidates.
