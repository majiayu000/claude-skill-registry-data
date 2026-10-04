---
name: verification-before-completion
description: >
  Mandatory proof that work is actually done before declaring completion.
  Use before saying "done," "complete," or "finished" for any task.
  Prevents the agent anti-pattern of declaring success without evidence.
version: 1.0.0
permissions:
  - fs.read
  - shell.exec
triggers:
  - context: "about to declare task complete"
  - context: "about to say done or finished"
  - command: "/test"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    gate_phrasing: "Before I tell you this is done, let me verify everything actually works."
  gemini:
    enforcement_style: "structured-checklist"
    gate_phrasing: "COMPLETION GATE: ☐ Tests pass ☐ Build succeeds ☐ Requirements met ☐ Evidence collected"
  gpt:
    enforcement_style: "directive-imperative"
    gate_phrasing: "You MUST run tests and verify the build before declaring any task complete."
author: codehands-core
signed: true
tier: 0
---

## Overview

"Done" means proven done, not believed done. This skill is the final gate before any task is declared complete. It prevents the most damaging agent behavior: confidently declaring success when the code doesn't actually work.

## When to Use

- Before EVERY task completion declaration
- Before saying "done," "complete," "finished," or "ready"
- Before marking a plan task as complete
- Before opening a PR
- This skill is NON-NEGOTIABLE. There are no exceptions.

## Process

### The Verification Checklist

Before declaring completion, confirm ALL of these:

1. **Tests pass.**
   ```bash
   npm test        # or pytest, go test ./..., cargo test, etc.
   ```
   If there are no tests, you haven't followed `codehands:test-driven-development`. Go back and add them.

2. **Build succeeds.**
   ```bash
   npm run build   # or equivalent
   ```
   TypeScript compiles. No warnings treated as errors. No build failures.

3. **Requirements met.** Re-read the spec/task. Compare each requirement against what you built. Every requirement must have evidence.

4. **No regressions.** The FULL test suite passes, not just your new tests.

5. **Code is committed.** All changes are committed with a descriptive message. Nothing is left in an uncommitted state.

### Evidence Requirement

For each completed task, provide evidence:

```markdown
## Completion Evidence
- Tests: 47 passing, 0 failing (output attached)
- Build: Clean build with 0 warnings
- Requirements: FR-001 ✅, FR-002 ✅, FR-003 ✅
- Commit: abc1234 "Add user registration with email verification"
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know it works — I just wrote it" | You believe it works. Belief is not evidence. Run the tests. |
| "Tests are passing in my head" | Run them for real. "Passing in your head" is the leading cause of broken deployments. |
| "The build will pass — I only changed one file" | One file change can break the build via type errors, import cycles, or missing exports. Confirm it. |
| "I'll verify at the end after all tasks are done" | Each task must independently pass verification. Deferring creates compound verification debt. |
| "The user is in a hurry" | Breaking the user's build to save 30 seconds is not a favor. Verify. |

## Red Flags

- "Done!" without test output
- Declaring completion on a task that has no tests
- Not running the full test suite (only new tests)
- Build not run before declaring complete
- Spec requirements not individually verified

## Verification

- [ ] All tests pass (full suite, not just new tests)
- [ ] Build succeeds with no errors
- [ ] Every spec requirement has been verified against implementation
- [ ] No regressions introduced (full test suite passing)
- [ ] All changes committed with descriptive message
- [ ] Completion evidence provided (test output, build output, requirement mapping)

## See Also

- `codehands:test-driven-development` — Tests that power verification
- `codehands:code-review-and-quality` — Review before final completion
- `codehands:systematic-debugging` — When verification reveals issues
