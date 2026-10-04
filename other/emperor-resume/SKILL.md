---
name: emperor-resume
description: >-
  Resume from disk instead of restating the session. SessionStart MUST-route
  activation (must-route.md + emperor activate) fires without waiting for
  "emperor time". Use at session start, after compaction, or when the user
  says continue, resume, where were we. Planning-with-files pattern:
  PLAN.md FINDINGS.md PROGRESS.md.
license: MIT
metadata:
  version: 0.4.5
  part-of: emperor-time
---

# Emperor Resume

## Before resume: MUST-route (silent activation)

At SessionStart, run `scripts/emperor activate` and open `must-route.md`.
Do **not** wait for the client to name Emperor Time. Quote `ACTIVATION next=`.
Then continue below when the target is this skill (or after that skill finishes).

## Resume from disk

0. Load L0 super-context before mass-grep when `.emperor/context/l0.md` exists (`scripts/emperor context l0` / `references/super-context.md`).
1. Read `.emperor/state.md` if it exists. Then the latest
   `.emperor/tasks/<id>/{PROGRESS,PLAN,FINDINGS,DONE,ledger}.md`.
   If `.emperor/context/l0.md` exists, read it before mass-grep (`scripts/emperor context l0` / `references/super-context.md`).
2. Do not recap what those files already say. One line: current gate + blocker.
3. If DONE.md exists and `scripts/emperor done` still fails, you are not done.
4. If DONE passes and no PR, open `skills/emperor-forge/SKILL.md` (finish menu first).
5. If nothing is in flight, open `skills/emperor-queue/SKILL.md`.
