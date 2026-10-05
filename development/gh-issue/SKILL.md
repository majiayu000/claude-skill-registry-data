---
description: Fetch a GitHub issue, branch, implement with TDD, open a PR
argument-hint: "[issue-number]"
disable-model-invocation: true
---

# /gh-issue

## Context

!`gh issue view ${ARGUMENTS#\#} --json number,url,title,body,labels,assignees,state,comments 2>/dev/null || echo "Provide an issue number"`

Read the body **and every comment** - later comments often refine or override the original.

## Steps

1. Strip `#` from `$ARGUMENTS`. Self-assign: `gh issue edit <num> --add-assignee @me`.
2. Branch from a fresh `main`. Prefix by label: `bug` → `fix/`, `enhancement` → `feat/`, `documentation` → `docs/`, else `feat/`. Format: `<prefix><num>-<slug>`.
3. **Plan** the change: which file (`src/pdo.phel` connection-side, `src/pdo/statement.phel` statement-side), what `deftest` covers it, whether README API table + CHANGELOG need updating. Present the plan.
4. **TDD** via the `tdd-coach` agent (red → green → refactor).
5. `composer test` - fix everything before continuing.
6. Update `## [Unreleased]` in `CHANGELOG.md`.
7. Commit:
   ```
   <type>(<scope>): <description>

   Related to #<num>
   ```
8. **Mandatory polish commit** (separate `ref(...)`): re-review every touched file against `.claude/rules/*.md`. Drop duplication, dead branches, leftover debug, naming drift, premature abstractions. If nothing surfaces, note that in the PR body.
9. `/pr #<num>`.
10. `gh pr checks <pr> --watch`. Fix red checks on the branch.
11. Merge: `gh pr merge <pr> --squash --admin --delete-branch`. Fallback `--auto --squash --delete-branch` if `--admin` is rejected. Never `--no-verify` past a failing required check.
12. Sync main: `git checkout main && git fetch origin main && git reset --hard origin/main`.
