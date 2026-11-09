---
name: pre-push-review
description: Get a branch ready for a pull or merge request. Use when the user says "ready this PR", "pre-push", "write the PR description", "am I ready to push", or before opening or un-drafting a change. Runs the self-review checklist reviewers taught, regenerates derived files, checks whether the change should be split, and drafts the description and commit message in the plain-voice style. Does not push or open anything unless told.
argument-hint: "[base branch, default main]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(git:*), Bash(gh pr view:*), Bash(gh issue view:*), Bash(glab mr view:*), Bash(glab issue view:*), Bash(jq:*), Bash(cat:*)
---

# Pre-push review

Base branch: what the user named, else the repository default (`main` or `master`). Load the `plain-voice` skill and the project's own conventions (its `AGENTS.md`, contributing guide, documented checklists) before starting.

Load [git-workflow](../git-workflow/SKILL.md) for repository inspection, staging, commits and any history changes. This workflow drafts by default; checking readiness does not authorize a commit, squash or push. Include staged and unstaged work separately when reviewing work not yet committed.

## 1. Look at the whole branch

```sh
BASE=$(git merge-base HEAD <base>)
git diff --stat $BASE...HEAD
git diff --name-only $BASE...HEAD
git log --oneline $BASE..HEAD
```

More than about ten files or two concerns: propose the split and stop until the user decides. A reviewer facing two concerns reviews neither well.

## 2. Seam and test sweep

1. For every new or changed UI component, open its parent. Does an ancestor already fetch this data (then take a prop)? Is every loading, empty and error branch reachable given the parent's guards? Does a render condition repeat the one above it? Fix or explain. A green standalone test does not prove any of this.
2. Every test file in the diff: the name states a behaviour, one behaviour per test, no reaching into component or module internals to assert.
3. A shared contract changed (a query, schema, API client, design-system component): run the tests of every consumer, not just the touched ones.
4. Derived files: when the project has generators or fix hooks (locale catalogs, generated schemas, snapshots, lockfile checks), run them now, not in CI.
5. Run the touched tests and the linter on touched files. Report pass or fail with output.

Inspect assertions for false confidence: a missing matcher, a callback that may never execute, a negative selector check with no positive control, or a mock asserting only its own configured return. An expected value imported from the implementation can repeat the same mistake. Replace these with observable behavior and appropriate async completion checks.

For a bug fix, show that the regression test fails with only the fix removed and passes with it restored. Use an isolated workspace or an exact reversible edit that preserves the user's work. Never reset, stash or overwrite unrelated changes to create this proof. If unsafe or unavailable, mark the proof not run and explain why.

Optional targeted mutation check: with authorization to edit the test workspace, temporarily flip a condition or omit an effect and confirm the relevant test fails. Restore only that edit, inspect the resulting diff, and rerun the test. Stop on unexpected differences. This strengthens evidence; it does not prove complete coverage.

## 3. Description

Use the project's pull request template when it has one. Otherwise use [pr-description.md](../../../templates/pr-description.md), in the `plain-voice` style. Leave screenshot cells as placeholders. Never describe screenshots you did not take.

## 4. Commit message

Follow the project's message convention; otherwise use an imperative subject under 72 characters and a body explaining why when useful. Project trailers (changelog, ticket references) follow the documented convention. Suggest squashing fixup noise if useful, but do not rewrite history without explicit authorization under `git-workflow`.

## 5. Labels and reviewers (suggest, the user applies)

Suggest the labels the project uses (area, type, flag) and the reviewer domains the diff touches. When a dependency change is still open, say which one in the description.

## 6. Output

Checklist with what ran and what it found, the description in a fenced block, the commit message, suggested labels. Then stop. Pushing and opening the pull request happen only on an explicit instruction in the current message.
