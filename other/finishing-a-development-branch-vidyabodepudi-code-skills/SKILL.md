---
name: finishing-a-development-branch
description: >
  Complete work on a development branch with final verification,
  review, and merge/PR decision. Use when all plan tasks are done
  and the branch is ready for integration.
version: 1.0.0
permissions:
  - fs.read
  - shell.exec
triggers:
  - context: "all tasks completed"
  - context: "ready to merge"
  - context: "branch is done"
  - command: "/ship"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - verification-before-completion@^1.0.0
  - code-review-and-quality@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Finishing a branch is the transition from "development" to "integration." This skill ensures the branch is clean, tested, reviewed, and ready before asking the human how to proceed.

## When to Use

- When all plan tasks are marked complete
- When the branch is ready for merging
- After final code review is approved
- NOT when tasks remain incomplete (finish tasks first)

## Process

### 1. Final Verification

Run the complete verification suite:

```bash
# All tests
npm test           # or equivalent

# Build
npm run build      # or equivalent

# Lint (if configured)
npm run lint       # or equivalent
```

All must pass with zero failures.

### 2. Final Code Review

If not already done, dispatch a final code review of the entire branch diff:

```bash
git diff main...HEAD --stat   # Overview of all changes
git diff main...HEAD          # Full diff for review
```

### 3. Clean Up

- Remove any debugging code (`console.log`, `debugger`, `print()`)
- Remove any commented-out code
- Verify `.gitignore` covers generated files
- Squash fixup commits if appropriate

### 4. Present Options to Human

Present the human with clear options:

> "All tasks complete. Tests pass. Code reviewed. How would you like to proceed?"
>
> 1. **Merge to main** — I'll merge the branch and clean up the worktree
> 2. **Open a PR** — I'll create a pull request for team review
> 3. **Keep the branch** — Done for now, keep it for later
> 4. **Discard** — The work isn't needed, delete the branch

Wait for the human's decision. Don't assume.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Tests passed earlier, I don't need to rerun them" | Code could have changed since then. Rerun. Final verification catches last-minute issues. |
| "I'll clean up the debugging code later" | Debugging code in production is a bug. Clean it now. |
| "I'll just merge without asking" | The human decides how to integrate. They may want a PR, or they may not be ready. Ask. |

## Red Flags

- Merging without running the full test suite
- Console.log / print statements left in production code
- Merging without user consent
- Skipping final review

## Verification

- [ ] All tests pass (full suite)
- [ ] Build succeeds
- [ ] No debugging code remains
- [ ] No commented-out code
- [ ] Final code review completed
- [ ] Human has chosen the integration method (merge/PR/keep/discard)

## See Also

- `codehands:using-git-worktrees` — Where the branch was created
- `codehands:git-workflow-and-versioning` — Git workflow conventions
- `codehands:ci-cd-and-shipping` — For production deployments
