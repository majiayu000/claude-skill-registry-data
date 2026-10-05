---
name: execution-gate-auditor
description: Use this skill to verify that selected valuation, freshness, provenance, risk, and output modules were actually executed or explicitly blocked. Trigger before final reports, after model routing, or when silent skips and incomplete analysis are suspected.
---

# Execution Gate Auditor Skill

## Purpose

Check whether the investment analysis actually executed the modules it selected.

## Workflow

1. Read selected valuation models.
2. Read selected investment style modules.
3. Read data freshness requirements.
4. Check whether each selected module has:
   - Result
   - Blocked reason
   - Not applicable reason
5. Identify silent skips.
6. Assign severity.
7. Produce Execution Gate Checklist.

## Output

```text
Execution Gate Checklist

| Gate | Status | Severity | Note |
|---|---|---|---|
| Data Freshness | Passed / Blocked / N/A |  |  |
| Reverse DCF | Passed / Blocked / N/A |  |  |
| Margin of Safety | Passed / Blocked / N/A |  |  |
```

## Hard Rule

The final report must not include a final investment rating if any Critical gate is blocked.
