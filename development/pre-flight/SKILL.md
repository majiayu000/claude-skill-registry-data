---
name: pre-flight
description: Builder pre-flight check - git status, type check, and build check.
disable-model-invocation: true
---

# Pre-Flight Check

Run all checks in order. Stop and report on first failure.

1. **`git status`** - is the repo clean? If there are uncommitted changes from a prior agent, stop and report.
2. **`npx tsc --noEmit --skipLibCheck`** - must exit 0. If it fails, the app is already broken. Do not proceed. Report what's broken.
3. **`npx next build --no-lint`** - must exit 0. Skip ONLY if `.multi-agent-lock` exists. If it fails, stop and report.

If all checks pass, report green and proceed with the task.

If any check fails: you are NOT allowed to write new feature code. Fix the existing break first, or report it to the developer.
