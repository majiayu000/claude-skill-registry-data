---
name: om-auto-create-pr
description: Repo-local extension of om-auto-create-pr - per-phase test, copy and generated-file discipline, commit style and the dependency freeze.
---

# om-auto-create-pr (money-tracker.online)

This file extends the shared `om-auto-create-pr` skill installed at
`.claude/skills/om-auto-create-pr/SKILL.md`. Follow its full workflow (claim, plan, worktree,
phase-by-phase commits, gate, PR, review loop, summary) with the rules below layered on top.

## Per phase

- Test-first at the seam (skill `tdd`). A new repository function ships with its tenant-isolation
  case; a money-touching write path with its money-invariant case (`AGENTS.md` → Always).
- Copy through the catalogue (skill `i18n-messages`): EN + PL in the same commit.
- Regenerate `src/routeTree.gen.ts` after a route change and `drizzle/` after a schema change, and
  commit the outputs with the change that caused them.
- Commits are Conventional Commits in English with the module or plan area as scope
  (`feat(budgets): …`). Check `git status` before the first commit: `.dev.vars` and `.ai/qa/`
  state are gitignored, and nothing else that is not part of the change may be staged.
- No suppressions, no skipped tests, no deleted test files (`.ai/review-checklist.md`).
- Money stays in integer minor units; SQL stays in `src/server/repos`.

## PR body

Keep the shared template. Under `## 🧪 Tests` list the tenant-isolation and money-invariant cases
added. Under `## What Changed` name every screen whose rendered output changes, so a human can take
the blind pair (ADR 0016).

## Dependencies

The dependency set is frozen (`docs/SPEC.md` §3). A run that needs a package stops and reports it as
a blocker instead of installing it.
