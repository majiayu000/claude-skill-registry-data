---
name: git-release-start
version: "1.0.0"
user-invocable: true
description: "Use when a version iteration starts and a release branch must be created — handles inconsistent branch-naming conventions across repos, multi-repo synchronized creation, and ensuring local tracking correctly points to origin/release/X.Y.Z rather than the base branch. Works with GitLab, GitHub, and other Git hosting platforms; single-repo or multi-repo. Triggers — 「创建release分支」「开release分支」「开分支」「迭代分支」 / create release branch."
---

# Git Release Start

## Overview

At the start of a version iteration, create a release branch from the main development branch. **Core principle: create on remote first, then sync to local** — `git checkout -b release/X origin/master` makes the local branch track `origin/master` instead of `origin/release/X`, planting a landmine for later push/pull confusion.

**Pairing**: `git-release-start` (iteration start, this skill) ↔ `git-release-finish` (iteration end, tag + merge).

---

## Platform CLI mapping

| Platform | CLI tool | Create branch on remote |
|------|---------|------------|
| GitLab (SaaS / self-hosted) | `glab` | `glab api POST "projects/:fullpath/repository/branches?branch=<NAME>&ref=<BASE>"` |
| GitHub | `gh` | `gh api repos/:owner/:repo/git/refs -f ref=refs/heads/<NAME> -f sha=<BASE_SHA>` |

**Convention**: `<GIT_CLI>` below stands for the platform's CLI tool — pick the row above that matches your environment, or the equivalent command for other platforms. Core git operations (fetch, checkout) are platform-agnostic.

---

## Use when / Do not use for

**Use when**:
- A version iteration starts and a new release branch needs to be created from the main branch
- Multiple repos need release branches for the same version, created in a coordinated way
- The branch's tracking must be verified correct (not accidentally pointing at master/main)
- An existing release-branch naming convention exists and must be followed

**Do not use for**:
- Non-Git hosting platforms

> **Principle: the flow must run end-to-end.** No phase can be skipped, regardless of repo count. "It's just creating a branch" is the most common cause of skipping verification and ending up with wrong tracking.

## Pre-conditions

- The corresponding platform CLI is installed and authenticated
- The version number is confirmed (e.g. `8.2.70`)
- The base branch is confirmed (e.g. `master` or `main`)

---

## Phase map

| Phase | Operation | Key tools |
|------|------|---------|
| 1 | Confirm version number and base branch | — |
| 2 | Analyze each repo's release-branch naming convention | `git branch -r` |
| 3 | Create the release branch on remote | `<GIT_CLI>` api |
| 3.5 | Read release protection; write only after the user accepts | `git-branch-protect` when installed |
| 4 | Sync locally + set tracking | `git fetch` + `git checkout --track` |
| 5 | Update environment file | `echo` / text write |
| 6 | Verify | `git branch` + `cat` |
| 7 | Output report | — |

---

## Phase 1: Confirm version number and base branch

> ⚠️ Confirm before creating, to avoid creating the wrong version or basing off the wrong branch.

### 1.1 Version number confirmation

If the user's message already states the version number, use it directly without asking again. Otherwise confirm with the user:
- The new version number (e.g. `8.2.70`)
- The previous version number (used in Phase 2 to compare historical branch naming, e.g. `8.2.60`)

Checks:
- Whether the new version's tag already exists: `git ls-remote origin refs/tags/<TAG_PATTERN>`
- Whether the new version's release branch already exists: `git ls-remote origin refs/heads/release/<VERSION>`
- If it already exists, abort with an error and ask whether to reuse it or rename

### 1.2 Base branch confirmation

Which branch should the release branch be created from? Usually the main development branch.

```bash
# Confirm the base branch exists and is up to date
git fetch origin <BASE_BRANCH>
git log --oneline origin/<BASE_BRANCH> -3
```

> ⚠️ **Remote HEAD may point at a deprecated branch**: after repo migrations or branch-policy changes, remote HEAD may still point at the old main branch (e.g. `master`) while the actually active main branch has become `main`. If the branch remote HEAD points to is hundreds of commits behind another candidate branch, HEAD is stale. **Trust merge history (`git log --merges | grep "into 'main'"`) as the source of truth, and confirm with the user if needed.**

**Output: confirmation table (Phase 1 only confirms version number and base branch; the release branch name is determined after Phase 2's analysis)**

| Repo | Version | Base branch |
|------|--------|--------|
| repo-A | 8.2.70 | master |

**After confirmation, proceed to Phase 2 (analyze release-branch naming convention).**

---

## Phase 2: Analyze release-branch naming convention

> ⚠️ Release-branch naming may not be simply `release/X.Y.Z` — check history. This phase outputs the final branch name; only after it completes can Phase 3 create the branch.

```bash
# List existing release branches
git branch -r | grep "origin/release"
```

### Identification rules

| Historical branch pattern | Naming convention |
|-------------|---------|
| `origin/release/8.2.60`, `origin/release/8.2.52` | `release/{VERSION}` |
| `origin/release/8.2.60-perf` | `release/{VERSION}-perf` |
| `origin/release/mobile-7.5.720` | `release/mobile-{VERSION}` (product prefix) |

**Multi-product repos**: each product line has its own release-branch naming; only create the branch for the current product line this time.

### Output: confirmation table

| Repo | Release branch name | Historical example |
|------|---------------|---------|
| repo-A | `release/8.2.70` | `release/8.2.60` |
| repo-B | `release/8.2.70-perf` | `release/8.2.60-perf` |

**Align with the user on the branch name before executing Phase 3.**

---

## Phase 3: Create the release branch on remote

> ⚠️ **Core lesson**: must create on remote first, then sync to local. Do not create locally first and push.
>
> Reason: a local branch created with `git checkout -b release/X origin/master` tracks `origin/master` instead of `origin/release/X`, causing confusion in later pushes and pulls.

Run in parallel for all repos:

```bash
# GitLab — create the branch on remote via API (`:fullpath` auto-resolves inside the repo directory)
glab api --method POST \
  "projects/:fullpath/repository/branches?branch=<RELEASE_BRANCH>&ref=<BASE_BRANCH>"

# GitHub — `:owner/:repo` auto-resolves when `gh` runs inside the repo directory
BASE_SHA=$(git rev-parse origin/<BASE_BRANCH>)
gh api repos/:owner/:repo/git/refs \
  -f ref="refs/heads/<RELEASE_BRANCH>" \
  -f sha="$BASE_SHA"
# If auto-resolution fails, substitute the actual values manually, e.g.: gh api repos/myorg/myrepo/git/refs ...
```

**Parameters**:
- `branch`: the full name of the new release branch (including path, e.g. `release/8.2.70`)
- `ref` / `sha`: which branch to create from (the main development branch)
- `:fullpath`: auto-resolved by GitLab; GitHub requires manually substituting `:owner/:repo`

---

## Phase 3.5: Read release protection

After the remote branch exists, load `git-branch-protect` when it is available. It reads the live rules with `glab` or `gh` and compares them with two conditions: unmatched `release/*` branches deny push and deny merge, and this exact branch denies push and allows maintainer merge.

| Read result | Action |
|-------------|--------|
| Skill is not available | Skip this phase. Leave protection unchanged |
| Both conditions already hold | Record the report and continue |
| A condition does not hold | Show the live rule and the target rule. Ask the user to accept each missing operation on its own. A yes for `ensure-default` is not acceptance of `allow-merge`. Run a write only after the user accepts that operation |

A decline leaves the rules unchanged and the release continues. This phase does not write trunk rules and does not run `set-trunk`. Phase 6 treats a rejected push as success when the protection report says this branch denies push and allows maintainer merge. That report may be `already-met` or an accepted `allow-merge`.

---

## Phase 4: Sync locally + set tracking

> ⚠️ Use `--track` to ensure the local branch tracks `origin/<RELEASE_BRANCH>`.

Run in parallel for all repos:

```bash
git fetch origin <RELEASE_BRANCH>
git checkout -b <RELEASE_BRANCH> --track origin/<RELEASE_BRANCH>
```

**Verify tracking**:

```bash
git branch -vv | grep '^\*'
# Expected output: * release/8.2.70  <SHA> [origin/release/8.2.70] <commit message>
```

> **If `[origin/master]` appears in the tracking column**: the branch was created the wrong way; fix it with `git branch -u origin/release/8.2.70`.

---

## Phase 5: Update environment file

> Some repos need the current branch name recorded in a `release-branch` file (which CI scripts etc. may read).

```bash
echo "<RELEASE_BRANCH>" > release-branch
git add release-branch
git commit -m "chore: update release-branch to <RELEASE_BRANCH>"
```

**Note**: if the repo doesn't use a `release-branch` file (no historical commits for it), skip this step.

```bash
# Check whether this file has existing history
git log --oneline -- release-branch | head -3
```

---

## Phase 6: Verify

Run the following verification for each repo:

```bash
git push --dry-run origin <RELEASE_BRANCH>
# Pass when the protection report says push is denied and maintainer merge is allowed: the push is rejected
# Pass when that report is absent, or the user declined a write and push is still allowed: the dry-run shows the update, or "Everything up-to-date"
# When the user declined a write and the push is still rejected, record the dry-run and continue. Leave the protection rules unchanged
```

**If a check other than this push dry-run fails, stop and fix it; only proceed to Phase 7 after confirming.** A rejected dry-run is a pass when the protection report says this branch denies push and allows maintainer merge. A declined write does not turn that rejection into a failure, and it does not authorize a protection change.

---

## Phase 7: Output report

Generate a confirmation table:

| Repo | Remote branch | Local tracking | release-branch | Status |
|------|---------|-------------|---------------|------|
| repo-A | `origin/release/8.2.70` | `[origin/release/8.2.70]` | `release/8.2.70` | ✅ |
| repo-B | `origin/release/8.2.70-perf` | `[origin/release/8.2.70-perf]` | N/A | ✅ |

---

## Error handling

| Scenario | Handling |
|------|---------|
| Tag already exists | Abort with an error; may indicate a duplicate release |
| Release branch already exists (remote) | Ask whether to reuse it (checkout directly) or rename |
| Base branch doesn't exist | Abort with an error, ask for the correct base ref |
| `glab api` returns 401 / 403 | Check `glab auth status`, re-authenticate |
| Tracking points to the wrong branch (`[origin/master]`) | Fix with `git branch -u origin/<RELEASE_BRANCH>` |
| A local branch with the same name already exists | `git branch -D <NAME>` to delete it locally, then checkout again |
| `push --dry-run` fails | Check the remote URL and permissions |

---

## Common mistakes

| ❌ Wrong | ✅ Right | Consequence |
|------------|------------|------|
| `git checkout -b release/X origin/master` then push | Create on remote via `<GIT_CLI>` api → fetch → `--track` | Tracking points to `origin/master`, causing confusion in later pull/push |
| Create the branch locally first, then push to remote | Create the branch on remote first, then fetch to local | Same as above |
| Skip Phase 5's check/update of `release-branch` | Confirm and update it | CI may read the wrong release-branch value |
| Assume all repos use the same naming | Check historical branch names per repo | Some repos' branch names carry special suffixes (e.g. `-perf`) and get missed |
| Consider the task done without verifying tracking | Verify each item in Phase 6 | Wrong tracking only surfaces later, during merge/push |

---

## Quick reference commands

```bash
# List existing release branches
git branch -r | grep "origin/release"

# GitLab — create on remote
glab api --method POST "projects/:fullpath/repository/branches?branch=<NAME>&ref=<BASE>"

# GitHub — create on remote
gh api repos/<OWNER>/<REPO>/git/refs -f ref="refs/heads/<NAME>" -f sha="$(git rev-parse origin/<BASE>)"

# Sync locally
git fetch origin <NAME>
git checkout -b <NAME> --track origin/<NAME>

# Fix tracking (if pointed wrong)
git branch -u origin/<NAME>

# Update release-branch
echo "<NAME>" > release-branch

# Verify
git branch --show-current
git branch -vv | grep '^\*'
git ls-remote origin refs/heads/<NAME>
git push --dry-run origin <NAME>
```
