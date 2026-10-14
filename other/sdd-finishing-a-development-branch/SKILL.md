---
name: sdd-finishing-a-development-branch
description: Use when implementation is complete, tests and CI pass, and you need to decide how to integrate the work
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Finishing a Development Branch

## Overview

**Core principle:** Verify the green baseline → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the sdd-finishing-a-development-branch skill to complete this work."

## Step 1: Verify the Green Baseline

Start from a clean tree: `git status --porcelain -uno` prints nothing. Tracked changes left uncommitted are not in the branch you are about to integrate, so gates run on them prove nothing — commit or stash them first. (Untracked files are not in the branch either; commit them if they are deliverables.)

Run every local gate the project runs — lint, types, tests, build, audit, e2e — on the tree you are about to integrate; the full test suite (`npm test` / `cargo test` / `pytest` / `go test ./...`) at minimum. A green baseline means all of them passed.

**If the repo has CI and this branch has been pushed, check every run for the exact head SHA.** `gh run list`'s page cap (`--limit`, default 20) can hide older runs, so query the API with pagination instead (or the forge's equivalent):

```bash
gh api --paginate "repos/{owner}/{repo}/actions/runs?head_sha=$(git rev-parse HEAD)&per_page=100" \
  --jq '.workflow_runs[] | [.name, .status, .conclusion] | @tsv'
```

Every line must read `completed<TAB>success`; no output means no run exists for this SHA. The SHA is the authority — not a PR's current head. Any failed run stops the menu exactly like a red local suite; pending runs are waited for. Never disable, skip, or retry a gate into green — fix the failure (`sdd-systematic-debugging`) or raise it with your human partner.

**If no CI run exists for this SHA** — branch never pushed, local-only merge, or no CI configured — say so plainly when presenting the options. Local green is not CI evidence, and the PR path gets its CI verdict when it is pushed; do not block the menu on a run that cannot exist yet.

**If local tests fail or a CI run for this SHA failed**, report and stop — the menu comes after a green baseline:

```
Baseline not green (<N> failures / <check name> failing). Must fix before completing:

[Show failures]
```

**If local tests pass and every CI run for this SHA is green (or no run exists yet):** continue to Step 2.

## Step 2: Detect Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)  # empty means detached HEAD
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` can also be true inside a submodule. If `git rev-parse --show-superproject-working-tree` returns a path, treat it as a normal repo, never as a linked worktree.

This determines which menu to show and how cleanup works:

| State                          | Menu                         | Cleanup                       |
| ------------------------------ | ---------------------------- | ----------------------------- |
| Normal repo, on a branch       | Standard 3 options           | No worktree to clean up       |
| Normal repo, detached HEAD     | Reduced 2 options (no merge) | No worktree to clean up       |
| Linked worktree, named branch  | Standard 3 options           | Provenance-based (see Step 6) |
| Linked worktree, detached HEAD | Reduced 2 options (no merge) | Provenance-based (see Step 6) |

## Step 3: Determine Base Branch

The base branch is whatever this work forked from — usually named in the
plan, the conversation, or the branch's upstream. If it is not already
known, ask: "This branch split from <your best guess> - is that correct?"
Confirm before merging: merging into the wrong base is expensive to undo.

## Step 4: Present Options

**On a branch (normal repo or linked worktree) — present exactly these 3 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**Detached HEAD (either repo type) — present exactly these 2 options:**

```
Implementation complete. You're on a detached HEAD (no branch to merge).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Present the menu exactly as written — concise, with every option coming
from the list above. Discarding the work happens only in response to your
human partner explicitly asking for it (see "If your human partner asks to
discard the work" below). Wait for their answer; the integration decision
is theirs.

**Surface what review left open, with the options.** If a reviewed execution
flow (e.g. sdd-subagent-driven-development) left parked findings, deferred
minors, or unresolved rulings that bear on integration, report them in the
message that presents the options — one line each with what it costs if
wrong, referencing the flow's rulings list rather than repeating it. The
menu text stays exactly as written; the findings precede it.

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify the full green baseline on the merged result — same gates as Step 1
<lint / types / tests / build commands>
```

If the merge hits conflicts, resolve them with
`sdd-resolving-merge-conflicts` — never by taking one side wholesale.

If the baseline fails on the merged result: stop, leave the worktree and branch in
place, and investigate — nothing has been pushed, so the merge is local
and recoverable.

Once the merged result is green: clean up the worktree (Step 6), then
delete the branch:

```bash
git branch -d <feature-branch>
```

### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

Then create the pull/merge request against <base-branch> with the forge's
tooling — its CLI if one is available, or the creation URL most forges
print when you push — following the repo's PR template and conventions if
present, and report the URL to your human partner.

Keep the worktree — your human partner iterates on PR feedback there.

### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

### If your human partner asks to discard the work

This path exists only as a response to an explicit request to throw the
work away. Confirm first:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for that exact confirmation. When it arrives:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then clean up the worktree (Step 6) and force-delete the branch:

```bash
git branch -D <feature-branch>
```

## Step 6: Cleanup Workspace

**Runs for Option 1 and confirmed discards.** Options 2 and 3 always
preserve the worktree. Both callers have already changed directory to the
main repo root — worktree removal must run from outside the worktree —
and use the `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` values captured in
Step 2, from before that directory change.

**If `GIT_DIR == GIT_COMMON`, or Step 2's submodule guard applied:** Normal repo, no worktree to clean up. Done.

**If `WORKTREE_PATH` is under `.worktrees/` or `worktrees/`:** Superpowers
created this worktree — we own cleanup:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**If removal is refused** (`contains modified or untracked files`): the
worktree holds files that exist nowhere else — uncommitted plans, notes,
or scratch work. Never `--force` on your own initiative. Show your human
partner what is at stake and ask:

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
Worktree removal refused — these files were never committed:

<file list>

1. Commit them to <branch> before cleanup
2. Move them into <main repo root>
3. Delete them (unrecoverable)

Which?
```

Carry out the choice, then remove the worktree.

**Otherwise:** The host environment owns this workspace — leave it in
place. If your platform provides a workspace-exit tool, use it.

## Quick Reference

| Option                          | Merge | Push | Keep Worktree | Cleanup Branch |
| ------------------------------- | ----- | ---- | ------------- | -------------- |
| 1. Merge locally                | yes   | -    | -             | yes            |
| 2. Create PR                    | -     | yes  | yes           | -              |
| 3. Keep as-is                   | -     | -    | yes           | -              |
| Discard (explicit request only) | -     | -    | -             | yes (force)    |

## Common Rationalizations

| Excuse                                                                  | Reality                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Tests passed earlier this session"                                     | Run the suite on the tree you are about to integrate. A green run only proves the tree it ran on.                                                                                                                             |
| "Local tests pass — CI is just a formality"                             | If the repo has CI, its verdict on the head SHA is the merge gate. Local green proves the tree, not the gate.                                                                                                                 |
| "The failing check is flaky — I'll re-run it"                           | Flakes are defects. Re-running to green launders them; fix the flake or surface it.                                                                                                                                           |
| "The gate is inconvenient — I'll disable the check"                     | Never lower a gate to finish. If a check is wrong, fix the check in its own change.                                                                                                                                           |
| "The parked findings were already adjudicated — no need to repeat them" | Parked means ruled on, not hidden. The finish menu is where your human partner sees them; report them alongside the options.                                                                                                  |
| "They obviously want it merged"                                         | Integration is your human partner's decision. Present the menu and wait.                                                                                                                                                      |
| "They seem done with this feature — I'll offer to discard it"           | The menu is complete as written. Discard happens only when your human partner asks for it in so many words.                                                                                                                   |
| "'Yeah, get rid of it' counts as confirmation"                          | Only the typed word `discard` authorizes deletion.                                                                                                                                                                            |
| "The PR is up, so the worktree is clutter now"                          | PR feedback gets fixed in that worktree. It stays until the work lands.                                                                                                                                                       |
| "This other worktree looks stale — I'll clean it too"                   | Clean up only worktrees under `.worktrees/` or `worktrees/`. Everything else belongs to the host.                                                                                                                             |
| "Removal refused — `--force` is just finishing the cleanup"             | The refusal means files exist only in that worktree. `--force` destroys them permanently. Show your human partner and ask.                                                                                                    |
| "The merged-result failure is probably flaky"                           | A failing merged result stops everything. Branch and worktree stay put while you investigate.                                                                                                                                 |
| "The base branch is obviously main"                                     | Confirm the fork point or ask. Merging into the wrong base is expensive to undo.                                                                                                                                              |
| "The push was rejected — force-push will fix it"                        | Fetch and inspect the rejection first: protection rules, permissions, and a diverged remote all look alike. Resolve divergence via `sdd-resolving-merge-conflicts`; force-push only on your human partner's explicit request. |
