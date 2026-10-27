---
name: debug
description: Root cause analysis for bugs and errors. Use when something is broken and the cause is not obvious. Applies the 5-step investigation method — observe, hypothesize, trace backwards, binary search, prove.
---

# Debug Skill

Systematic root cause analysis.

## When to use
- An error is happening and the cause is not obvious
- A test is failing unexpectedly
- Behavior changed after a refactor
- Production incident requiring root cause identification

## 5-Step Investigation Method

### Step 1 — OBSERVE: Gather exact evidence
Do NOT guess. Collect all available evidence first:
- Exact error message (full stack trace, not summary)
- Exact input that triggers the failure
- Exact expected vs. actual output
- When it started failing (which commit? which change?)
- Environment where it fails (dev? CI? prod? all?)

### Step 2 — HYPOTHESIZE: Form concrete hypotheses
Based on the evidence, generate 2-3 specific hypotheses:
- Each hypothesis must be falsifiable (testable)
- Rank by probability based on evidence
- Do NOT assume the most complex explanation — prefer simple causes

### Step 3 — TRACE BACKWARDS: Follow the execution path
From the failure point, trace backwards:
```bash
grep -rn --color=never '<error_symbol_or_message>' . | head -20
```
- Find the function that threw the error
- Find its caller
- Find the caller's caller
- Keep tracing until you reach user input or a boundary

### Step 4 — BINARY SEARCH: Narrow the scope
If the trace is long, use bisection:
- Does it fail with the same input after reverting X? (git bisect or manual)
- Does it fail with minimal input? (reduce the test case)
- Does it fail in isolation? (extract the failing unit)

### Step 5 — PROVE: Verify the root cause
Before fixing, prove you found the right root cause:
- Write a test that reproduces the bug exactly
- Verify the test fails (red) with the current code
- Apply the fix
- Verify the test passes (green)
- Run the full test suite — no regressions

## Rules
- NEVER fix before proving the root cause
- NEVER submit a fix without a reproducing test
- If two hypotheses remain after Step 4, test the simpler one first
- Document the root cause in `claude/tasks/lessons.md` if it's a non-obvious pattern
