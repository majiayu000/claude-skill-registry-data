---
name: workflow-closeout
description: Use when workflow work needs validation, tracker closeout, commit, push, upload verification, or handoff.
---

# Workflow Closeout

Use this skill to finish tracked workflow work.

## Required Flow

1. Read `skills/control-repo-manager/SKILL.md`.
2. Run the gates that match the work: `npm test`, `npm run validate`, `npm run
   build` when UI/dashboard data changed, and `git diff --check`.
3. Close or checkpoint the tracker run with validation results.
4. Commit and push intended repo changes.
5. Run `npm run tracker:upload-gate`.
6. Report live upload truth.

Do not claim completion before upload verification passes.
