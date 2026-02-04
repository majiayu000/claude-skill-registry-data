---
name: verification-checklist
description: Use before marking any task complete to ensure all requirements are met
---

# Verification Checklist

A task is NOT complete until all verification passes. No exceptions.

## Completion Criteria

- [ ] All planned todo items marked done
- [ ] Diagnostics clean on changed files
- [ ] Build passes (if applicable)
- [ ] Tests pass (if applicable)
- [ ] User's original request fully addressed

## Evidence Requirements

| Action | Required Evidence |
|--------|-------------------|
| File edit | `lsp_diagnostics` clean on changed files |
| Build command | Exit code 0 |
| Test run | Pass (or explicit note of pre-existing failures) |
| Delegation | Agent result received and verified |

**NO EVIDENCE = NOT COMPLETE.**

## Verification Steps

### 1. Run Diagnostics

```
lsp_diagnostics on each changed file
```

### 2. Run Build (if project has build)

```
npm run build / cargo build / etc.
```

### 3. Run Tests (if project has tests)

```
npm test / cargo test / etc.
```

### 4. Check Against Original Request

Re-read the user's original request. Does your implementation:
- Address ALL requirements mentioned?
- Handle edge cases discussed?
- Follow any constraints specified?

## If Verification Fails

1. Fix issues caused by YOUR changes
2. Do NOT fix pre-existing issues unless asked
3. Report: "Done. Note: found N pre-existing lint errors unrelated to my changes."

## Pre-existing Failures

If tests/build/lint were failing BEFORE your changes:

1. Document the pre-existing failures
2. Ensure you didn't make them worse
3. Report them separately from your work

## Before Final Delivery

- Cancel ALL running background tasks: `background_cancel(all=true)`
- Summarize what was done
- Note any caveats or follow-up items
