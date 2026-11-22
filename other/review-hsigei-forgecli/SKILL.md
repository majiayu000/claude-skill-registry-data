---
name: review
description: Review uncommitted changes (or named files) for bugs, security issues and unclear code
---
# Code review

1. Find what changed. If this is a git repo, run `git status` and `git diff` (and `git diff --staged`).
   If the user named files instead, read those.
2. Read enough surrounding code to understand each change. Do not review code you have not read.
3. Look for, in this order:
   - Bugs: wrong logic, off-by-one, unhandled errors, None/null cases, race conditions.
   - Security: injection, secrets in code, unsafe file or shell use, missing input validation.
   - Breakage: changed function signatures whose callers were not updated (grep for them).
   - Clarity: misleading names, dead code, duplicated logic.
4. Report findings most severe first, each as: `path:line` — what is wrong — a concrete fix.
   Say plainly if you found nothing serious. Do not edit files unless the user asks.
