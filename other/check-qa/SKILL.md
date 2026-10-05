---
name: check-qa
description: Perform a structured QA pass on current changes or a feature, testing happy path, edge cases, and regression risks.
---

> **[Orchestrator Instructions]** Do NOT execute this skill yourself. You MUST use the invoke_subagent tool to spawn an independent subagent with the Role: **QA Automation Engineer**.


QA target: $ARGUMENTS (feature name, PR number, or file path — leave blank to QA current changes)

> This is the single-agent QA pass. For a multi-agent QA workflow (parallel functional / edge-case / regression analysts, consolidated report), use [workflow-qa](../workflow-qa/SKILL.md). That workflow drives this skill.

Gather what's being tested:

```bash
git diff main...HEAD --stat 2>/dev/null || git diff --stat HEAD~1
git log --oneline -5
```

Run a structured QA pass:

## 1. Acceptance criteria check

- What is this feature/fix supposed to do? List the expected behaviors.
- Verify each one is actually implemented (read the code, run if possible).
- Flag any acceptance criteria that are missing or only partially implemented.

## 2. Happy path

Walk through the primary use case step by step. For each step:
- What input/action?
- What is the expected output/state?
- Does the code produce that? (Check logic, not just syntax.)

## 3. Systematic Edge Cases & Boundaries

Utilize advanced matrix testing. Mark each ✅ pass / ❌ fail / ⚠️ untested:

| Category | Examples |
|---|---|
| Empty / null | empty string, null/undefined, empty array/object |
| Boundary | min/max values, off-by-one, $Min-1, $Max+1, max length |
| Invalid / Format | wrong data type, negative numbers, invalid regex |
| State Transition | test all valid and invalid state transitions |
| Concurrency | race conditions, double-submit, stale data |
| HTTP/API Routing | **(BE only)** explicit checks for accurate 400, 401, 403, 404, 500 status codes |
| Error states | network failure, timeout, invalid input from external source |

## 4. Automation Triaging & Manual Handoff

Evaluate if a test case is deterministic. 
- **Level 1 (Fully Auto)**: Clear oracle, deterministic (e.g., math, formatting, data mapping). Proceed to test it.
- **Level 2 & 3 (Manual Handoff)**: Highly subjective (UI visual diffs), timing-dependent, or requires third-party black-box interaction. **Do NOT attempt to run these automatically.** Mark them as `HANDOFF` and append them to the Manual Testing List for the user.

## 5. Regression risk

List 3-5 existing features most likely to break from this change. Check each one in the code.

## 6. QA report

Write your report to `.harness/reports/qa-report.md`. Your chat response must ONLY be the path to this file (e.g. "QA complete. See .harness/reports/qa-report.md"). Do NOT output the report text in the chat. Format for the file:
```
## QA Report — <feature>

### ✅ Passing
- ...

### ❌ Failing
- <issue>: <expected> vs <actual>

### ⚠️ Needs manual testing
- ...

### Verdict
PASS / FAIL / CONDITIONAL PASS (needs fix before merge)
```
