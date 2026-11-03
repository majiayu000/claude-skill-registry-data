---
name: debug
description: Root-cause debugging for runtime errors, failing tests, regressions, and unexpected behavior. Use when you need to isolate the failure, prove the cause, and fix the smallest thing that restores correct behavior.
origin: Betopia
slash: /debug
order: 20
---

# Debug

Find the root cause, change the smallest thing that actually failed, and verify the failure is gone.

## When to Activate

- Runtime error or stack trace
- Failing test or regression
- Unexpected behavior after a recent change
- User says "debug", "fix", or "why is this failing"

## Inputs to Collect

- Exact error text, stack trace, or log line
- Failing command, screen, endpoint, or file
- Recent diff, especially the touched files
- Environment details that can affect the failure
- Minimal reproduction steps

## Workflow

### 1. Lock the failure

- Capture the exact failure message and the command that produced it
- Re-run the failing path so the issue is concrete
- Note what changed most recently before the break

### 2. Narrow the blast radius

- Inspect the touched files first with `git diff HEAD~1`
- Reproduce with the smallest possible input or test
- Remove unrelated variables until one path still fails

### 3. Trace the boundary

- Follow the data flow across input, transform, and output
- Verify the actual runtime values instead of guessing from symptoms
- Add temporary logging only when it answers a specific question

### 4. Prove the cause

- Form one hypothesis at a time
- Confirm or reject it with a direct check
- Do not widen the edit before the cause is proven

### 5. Fix the source

- Make the smallest change that restores correct behavior
- Keep unrelated refactors out of the patch
- If the bug is in test or config, fix the actual source of truth

### 6. Verify and clean up

- Re-run the failing path
- Run the narrowest relevant test or build step
- Remove temporary logs
- Explain the root cause, evidence, fix, and verification

## Quality Rules

- Do not guess from partial errors
- Do not widen scope before the root cause is proven
- Prefer the smallest safe change
- If evidence is still missing, say exactly what is needed

## Examples

- "debug why login fails on submit"
- "debug the failing vitest case"
- "debug why the deploy button never enables"

## Output Standard

Report:

- What failed
- Why it failed
- What you changed
- How you verified it
