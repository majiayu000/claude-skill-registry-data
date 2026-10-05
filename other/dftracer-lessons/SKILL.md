---
name: dftracer-lessons
description: How to use and update the lessons-learned cache at .goose/lessons-learned.md — proactive lookup before any build/install/annotate step
---

## Lessons-Learned Cache

A structured log of past failures and their fixes lives at `.goose/lessons-learned.md`.

**Before attempting any build, install, configure, or annotation step:**
1. Read `.goose/lessons-learned.md`.
2. Search for entries whose `tags` or `error` match the current task (package name, build tool, error text).
3. Apply the recorded fix proactively — do not repeat a known failure.

**After resolving any non-trivial error (not a simple typo):**
Append a new entry to `.goose/lessons-learned.md` using this format:

```markdown
---
date: YYYY-MM-DD
context: <one-line description of what was being attempted>
error: |
  <exact error message or key excerpt>
root_cause: <why it happened>
fix: |
  <exact steps or code change that resolved it>
tags: [<package>, <build-tool>, <error-keyword>, ...]
---
```

Keep entries cumulative — never delete old ones. They are the institutional memory for this project.
