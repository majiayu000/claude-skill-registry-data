---
name: "lint-check"
description: "Run the repo's markdown lint checks over changed files before a PR. On demand, in Claude Code or any session with a shell."
---

# Lint check

Runs `scripts/check.sh` over the markdown files changed on the current branch and reports each problem with file and line.

## Procedure
1. List the changed `.md` files against `origin/main`.
2. Run `bash scripts/check.sh <files>`.
3. Report each line the script prints; if it prints nothing, say the files are clean.

## Known constraints
- Read-only: reports problems, never fixes them.
