---
name: github-issue
description: 'GitHub issue conventions: types, [Level] titles, branches, commits, native sub-issues, plan-to-issue creation. Use for any GitHub issue work.'
---

## Overview

Conventions for the GitHub issue lifecycle. Detect the issue type, then follow the matching reference document. One issue per session; running several issues is the runner's job.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Run from repo root
- Check `git status` first; never commit unrelated pre-existing changes (add files explicitly, never `git add -A`/`.`)

## Issue Types

Issues follow this hierarchy (the repository's `.github/ISSUE_TEMPLATE/` holds the templates when present; this table is the definition):

| Label     | Title (always `[<Level>] <summary>`)        | Sub-issues |
| --------- | ------------------------------------------- | ---------- |
| `epic`    | `[Epic] <outcome>`                          | Features   |
| `feature` | `[Feature] <capability>`                    | PBIs       |
| `pbi`     | `[PBI] feat(scope): …`, `[PBI] refactor: …` | —          |
| `bug`     | `[Bug] fix: <symptom>`                      | —          |

Label `release-test` (together with `pbi`, usually `interactive`) marks the RC test of a milestone: one per milestone, always the last item (`references/milestones.md`).

Titles are always written with the bracket prefix. Legacy titles (`Epic: …`, `Feature: …`, `[EPIC] …`) are still recognized when reading, never written. `[Task]` issues (label `task`) of older plans are read and closed together with their PBI, never created (`references/sub-issues.md`, "Legacy Task issues").

Parent/child links are **native GitHub sub-issues** — see `references/sub-issues.md` for how to
read, create, move and verify them. Markdown checklists are not used.

Milestones: a PBI and a Bug always have one; a Feature only when all its PBIs are in that milestone; an Epic never (`references/milestones.md`).

## Routing

1. Read the issue(s): `gh issue view <nr> --json title,body,labels`
2. Detect type from the `labels` field (`epic` / `feature` / `pbi` / `bug`; legacy `task`)
3. Follow `references/standalone-issue.md`.
4. A plan from `planner` (`plan.json`) → `references/create-from-plan.md`: create the issues, sub-issue and blocked-by links.

## Shared constraints (all workflows)

- Work branches are cut from and merged into the integration branch (`release/next` by default, explicit `release/<x.y>` only for parallel lines), never `main` (`references/release-branches.md`); `github-release` cuts and finishes it.
- Branch name `<type>/<nr>-<slug>` per `references/conventional-commits.md`; `<slug>` from the issue title after stripping `^\[(Epic|Feature|PBI|Task|Bug)\] ` (case-insensitive) and the legacy `Epic: ` / `Feature: `, then the conventional type and scope (lowercase, spaces → `-`, drop parenthetical scope, max ~40 chars).
- One logical change per commit; commit format per `references/conventional-commits.md`.
- Commit and PR titles reference the issue: `<type>: <description> (#<nr>)`; the PR body contains `Closes #<nr>` for every issue it completes (only partly delivered: `Refs #<nr>` and `## Not delivered`, see `github-pull-request`).
- Verify per `implementation` (targeted tests per commit, one full run before the pull request); never commit or move on with a red run.
- Never merge a PR with failing checks.
- `.agents/config.json` has `governance`: an issue whose outcome is a decision follows `references/decisions.md`.
- Closing a child is all that's needed — the native sub-issue link updates the parent's progress automatically. There is no checklist to tick. If a child turns out not to be linked to its parent, link it (`references/sub-issues.md`) instead of adding a checklist.
