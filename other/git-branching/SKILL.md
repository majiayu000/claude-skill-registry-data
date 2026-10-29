---
name: git-branching
description: |
  Select, document, and evolve a Git branching strategy for a repository.
  Use when comparing Gitflow, GitHub Flow, trunk-based development,
  feature branches, release branches, or concurrent version lines.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-git-branching
    version: "1.0.0"
    created: 2026-07-21T19:05:00Z
    category: engineering
    layer: null
    uses:
      - skill: git-workflow
        purpose: "Apply the chosen strategy through branch names, commits, pull requests, and merge methods."
      - skill: release-semver
        purpose: "Prepare, tag, publish, and verify releases on the strategy's designated release branch."
    provides:
      processes: [branching-strategy-selection]
---

# Git Branching

## Intro

Choose a branching strategy from the repository's delivery cadence,
supported versions, deployment environments, and release controls. Then
write a small branch contract that makes integration and tagging authority
unambiguous.

## Overview

### Select a strategy

Answer these questions before naming branches:

1. Is `main` continuously deployable, or is there a separate release gate?
2. Are older versions supported while new major work continues?
3. Do environments promote the same commit through test and production?
4. Can incomplete work be hidden with feature flags?
5. Is the team able to keep shared branches continuously integrated?

Use the smallest model that meets those constraints.

| Strategy | Best fit | Long-lived branches | Release authority |
| --- | --- | --- | --- |
| Feature Branch Workflow | Shared integration branch, periodic releases | integration branch | integration or release branch |
| GitHub Flow | Frequent deployment and one supported production line | `main` | `main` |
| Trunk-Based Development | Strong CI, feature flags, rapid integration | `main`; optional short release branch | `main` or just-in-time release branch |
| Gitflow | Scheduled releases and formal stabilization | `main`, `develop`, temporary release branches | release branch |
| GitLab Flow | Environment promotion or maintained stable lines | `main`, environment or stable branches | production or stable branch |
| Version-line integration | Concurrent major lines or long-lived maintenance | one dev and release branch per line | designated line release branch |

Read [strategy catalog](references/strategies.md) before choosing a model
with release branches, multiple environments, or concurrent version lines.

### Write the branch contract

For each protected long-lived branch, record:

- purpose and allowed changes;
- source branches and merge direction;
- tag authority and release validation command;
- hotfix and backport path;
- required checks, review, force-push, and deletion policy.

Keep task branches short-lived and name them according to `git-workflow`.
Use merge commits for meaningful integration between long-lived branches;
use the repository's chosen merge method for task branches.

### Apply the version-line integration model

Use this model when v0 maintenance and v1 development, or any two supported
major lines, must progress independently:

```text
line.x-dev -> line.x-release -> tag stable release -> main

next.x-dev -> next.x-pre-release -> tag alpha/beta/rc
                                     -> next.x-release -> tag GA -> main
```

- Create `line.x-release` from the latest stable tag and `line.x-dev` from
  that release branch.
- Merge development into the release branch, validate there, and tag only
  there. Merge the tagged stable release into `main` immediately afterwards.
- For prereleases, merge development into `next.x-pre-release` and tag only
  on that branch. Create `next.x-release` only for general availability.
- Hotfix from the latest stable tag, then merge to the release branch, tag,
  merge to `main`, and merge back to the development branch.

## Gotchas

- **Treating `main` as both active development and release authority.**
  This makes concurrent version lines indistinguishable. State whether
  `main` is trunk or published history before creating branches.
- **Copying Gitflow mechanically.** Gitflow's `develop` and release branches
  add synchronization cost. Choose it only when scheduled stabilization or
  parallel release preparation needs that cost.
- **Tagging a development branch.** A development head may not have passed
  integration checks. Tag only the contract's designated release branch.
- **Using environment branches as feature integration branches.** Environment
  branches promote tested commits; they are not a substitute for a developer
  integration target unless the contract explicitly says so.
- **Forgetting the return path for hotfixes.** A production fix that is not
  merged back into active development will recur in the next release.
- **Protecting a branch without defining how automation merges it.** Check
  required reviews, checks, merge queue, and allowed merge methods before
  making the branch the only release path.

## Full reference

### Required output

Deliver a branch contract in this form:

```text
Strategy:
Reason for fit:
Protected branches:
Merge directions:
Tag authority:
Hotfix and backport policy:
Required checks and release commands:
Migration steps and rollback point:
```

Do not migrate a live repository by renaming, deleting, or force-updating
branches until its existing tags, release consumers, and protection rules
have been inspected.

### Anti-patterns

- **A branch per person or indefinitely open feature branch.** Prefer a
  focused task branch and merge it promptly.
- **A release branch for every routine deployment.** If the product can
  release directly from a healthy trunk, extra release branches add delay.
- **One undocumented catch-all branch.** A branch without a stated authority
  eventually receives incompatible development, release, and hotfix changes.

### Cross-references

- [Strategy catalog](references/strategies.md)
- `git-workflow` — naming, commits, pull requests, and merge methods
- `release-semver` — changelog, tags, publishing, and release verification
