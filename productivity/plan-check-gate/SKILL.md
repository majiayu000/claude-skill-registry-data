---
name: plan-check-gate
description: Require fact-backed research and an explicit implementation plan before writing code. Use when the user asks for planning first, wants verification/citations, says they may be wrong, or when the task is high-risk/high-cost and code should stay blocked until plan approval.
---

# Plan Check Gate

## Overview

Enforce a pre-code quality gate. Do research first, separate verified facts from assumptions, and produce an approval-ready plan before any file edits.

## Pre-Code Workflow

1. Define scope
- Restate objective, constraints, and acceptance criteria.
- Identify what must be true for the task to be considered done.

2. Build fact set
- Collect only relevant facts.
- Mark each item as `verified` or `assumption`.

3. Research and verify
- Prefer primary sources for technical claims (official docs/specs/repos/papers).
- If information can change (versions, APIs, pricing, policies, benchmarks), re-check before coding.
- Record source links and concrete dates.

4. Propose plan
- Provide implementation steps, test plan, risks, and rollback idea.
- Keep steps small and reversible.

5. Approval gate
- Ask for explicit go/no-go.
- Do not write code until approved.

## Output Contract

Before coding, return:
- `objective`
- `constraints`
- `verified_facts` (with sources)
- `assumptions`
- `plan_steps`
- `test_strategy`
- `risks`
- `decision` (`hold` or `go`)

## Coding Unlock Conditions

Only start implementation when all are true:
- At least one high-signal source exists for each unstable or critical claim.
- Assumptions are explicitly listed.
- Plan is testable and scoped.
- User approved execution.

## Resources

- Checklist and prompt snippets: `references/plan-check-checklist.md`
- Artifact generator: `scripts/emit_plan_check.py`

Use the script to create a reusable planning record:

```powershell
python scripts/emit_plan_check.py --task "your task" --out ".codex-plan-check/your-task.md" --requires-research --source "https://example.com/doc"
```
