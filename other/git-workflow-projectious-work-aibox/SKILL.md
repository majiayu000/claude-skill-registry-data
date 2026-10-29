---
name: git-workflow
description: |
  Git workflow conventions — branch naming, conventional commits, PR descriptions, and merge strategy. Use when deciding on a branch name, writing a commit message or PR description, or choosing a merge strategy.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-git-workflow
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: engineering
    layer: 3
---

# Git Workflow

## Intro

Use typed branch names, Conventional Commits, and PR descriptions
that explain the why. Squash-merge feature branches for a clean
history. Keep commits atomic and never force-push to shared
branches.

## Overview

### Branch naming

Format: `<type>/<issue>-<short-description>`

Types: `feat/`, `fix/`, `refactor/`, `docs/`, `chore/`

Examples:

- `feat/42-add-user-auth`
- `fix/17-null-pointer-crash`
- `refactor/89-extract-payment-service`

### Version-line release branches

For concurrently maintained major lines, use explicit development and
release-integration branches. `main` is the published-history branch, not
the active development or tagging authority.

| Line | Development | Integration and tag authority | Publication |
| --- | --- | --- | --- |
| v0.x | `v0.x-dev` | `v0.x-release` | merge tagged release into `main` |
| v1.x prerelease | `v1.x-dev` | `v1.x-pre-release` | prerelease tag stays on integration branch |
| v1.x GA | `v1.x-pre-release` | `v1.x-release` | merge tagged release into `main` |

- Create a version-line release branch from the currently published tag,
  then create its development branch from that release branch.
- Merge development into the relevant integration branch for each release;
  validate, prepare, and tag only on that integration branch.
- Immediately merge the tagged integration branch into `main`, so every
  stable release tag is reachable from `main`.
- Do not commit directly to `main` or an integration branch. Protect them
  and use merge commits for long-lived branch integration.
- For a maintenance hotfix, branch from the latest stable tag, merge into
  the release branch, tag, merge the release branch into `main`, then
  merge the result back into the development branch.

### Commit messages

Follow Conventional Commits:

- **Format:** `<type>: <description>` — lowercase, imperative
  mood, no trailing period
- **Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`,
  `ci`
- **Body:** explain WHY, not WHAT (the diff shows what)
- **Footer:** `fixes #N` or `refs #N` for issue links

### PR descriptions

- **Title:** same format as commit messages, under 70 characters
- **Body:** Summary (what and why), test plan, breaking changes
- Link related issues

### Merge strategy

- **Squash merge** for feature branches — keeps mainline history
  clean
- **Merge commit** for long-lived branches — preserves context
  across the merge
- **Rebase** to keep a feature branch up to date before opening
  the PR

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Mega-commits ("various fixes", 40 files changed).** A commit that mixes unrelated changes is impossible to review, impossible to revert selectively, and tells a lie in its message. Each commit should represent one logical change that can stand alone.
- **Force-pushing to shared branches.** Force-pushing to `main` or any branch others have checked out rewrites history they depend on, causing diverged local states that are painful to recover. Never force-push to a shared branch.
- **Branches that live for months.** Long-lived branches diverge from main, accumulate merge conflicts, and eventually require heroic merge efforts. Rebase weekly or split long-running work into shorter-lived feature branches.
- **Tagging a development branch.** A development branch has not passed the
  integration and release gate. Stable and prerelease tags must originate
  on their designated integration branch.
- **PRs with no description.** "See commits" is not a description. The PR description is for the reviewer — it explains what changed, why it changed, and how to verify it. Write it before requesting review.
- **Conventional Commit type misuse.** Using `fix:` for features or `feat:` for refactors corrupts any automation that generates changelogs or determines version bumps from commit types. Match the type to the nature of the change.
- **Squash-merging a long-lived integration branch.** Squash-merge is for feature branches with noisy "wip" commits. A long-lived branch with meaningful commit history should be merge-committed so the history is preserved for future investigation.
- **Committing unrelated changes in the same PR to "save time".** Reviewers are slower on unrelated changes combined in one PR; rollback becomes more expensive if one change needs reverting. Split unrelated changes into separate PRs.

## Full reference

### General rules

- Commit early and often on feature branches; squash at merge time.
- Never force-push to shared branches (`main`, `develop`, release
  branches).
- Keep commits atomic — one logical change per commit. A commit
  that touches three unrelated concerns is three commits.
- A commit message body wraps at 72 columns; the subject line at
  50 if you can.

### Worked example

User: "What should I name this branch for adding search?"

Suggest `feat/30-add-search-functionality` if there's an issue
#30; otherwise `feat/add-search-functionality`. Match the
existing repo's convention if it differs.

### Anti-patterns

- **Mega-commits** — "various fixes" with 40 files changed.
  Impossible to review or revert.
- **Force-push to main** — destroys other contributors' work.
- **Commit messages like "wip", "fix", "stuff"** — every commit
  should be reviewable on its own.
- **PRs with no description** — the PR description is for the
  reviewer, not the author. "See commits" is not a description.
- **Branches that live for months** — long-lived branches
  diverge from main and become merge nightmares. Rebase weekly
  or split the work.

### When to break the rules

Solo-on-a-private-branch force-pushes are fine. Trivial typo
fixes don't need a long body. Use judgment, but the defaults
above are right for almost every team setting.
