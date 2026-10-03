---
name: ls-unfuck-my-git-state
description: "Diagnose and recover broken Git state and worktree metadata with a staged, low-risk recovery flow. Use when Git reports detached or contradictory HEAD state, phantom worktree locks, orphaned worktree entries, missing refs, 0000000000000000000000000000000000000000 hashes, or branch operations fail with errors like already checked out, unknown revision, not a valid object name, or cannot lock ref."
metadata:
  version: "1.3"
---

# Unfuck My Git State

Recover a repository without making the blast radius worse.

## Core Rules

1. Snapshot first. Do not "just try stuff."
2. Write evidence only beneath the controller-assigned `.agents/state/<task-slug>/` directory.
3. Resolve the per-worktree and common Git directories; never assume `.git` is a directory.
4. Prefer non-destructive fixes before force operations.
5. Inspect reflog and create rescue refs before moving a branch pointer.
6. Create and verify a metadata backup before any manual metadata edit.
7. Obtain point-of-risk confirmation for the exact target and values before a force or manual edit.
8. After each fix, run verification before proceeding.

## Rule Ownership

This skill owns Git repair and broken-state recovery behavior. Public maintenance docs can point here, but recovery agents should load this skill before touching Git metadata, index files, worktree metadata, or refs.

- Use ordinary `ls-git-workflows` for healthy advanced Git operations.
- Use this skill when Git commands report contradictory state, missing objects, broken index/cache-tree data, zero hashes, or stale worktree locks.
- Use the controller-assigned Git-bound task slug. Do not invent a second task-state directory.
- Do not execute destructive recovery commands while diagnosing or generating a plan.

## Fast Workflow

Set the explicit private output boundary once:

```bash
TASK_STATE_DIR="$PWD/.agents/state/<controller-task-slug>"
```

1. Capture diagnostics beneath that directory:

```bash
python scripts/snapshot_git_state.py . --output-dir "$TASK_STATE_DIR"
```

2. Route by symptom using `references/symptom-map.md`.
3. Generate a plan from a new snapshot. The generator consumes the snapshot path through its JSON manifest rather than guessing the newest directory:

```bash
python scripts/guided_repair_plan.py --repo . --output-dir "$TASK_STATE_DIR"
```

4. Apply the smallest matching playbook.
5. Run the `references/recovery-checklist.md` verification gate.
6. Escalate only if the gate fails.

For an existing snapshot or explicit routing:

```bash
python scripts/guided_repair_plan.py --snapshot "$TASK_STATE_DIR/git-state-snapshots/<stamp>"
python scripts/guided_repair_plan.py --list
python scripts/guided_repair_plan.py --symptom phantom-branch-lock
```

## Snapshot Evidence Contract

`snapshot_git_state.py` records:

- porcelain-v2 status and branch headers
- current branch and symbolic `HEAD`
- a resolvable `HEAD^{commit}` probe
- per-worktree and common Git directory paths
- worktree, refs, reflog, remote, and fsck diagnostics
- `snapshot.json`, binding the emitted snapshot path to the explicit task output directory

A detached-HEAD diagnosis requires all three signals: `# branch.head (detached)`, an empty `git symbolic-ref -q HEAD` result, and a resolvable `HEAD^{commit}`. One signal alone is not enough.

## Regression Harness

Use disposable simulations before changing script logic:

```bash
python scripts/regression_harness.py
python scripts/regression_harness.py --scenario detached-head
```

The harness creates temporary repositories and never runs force, reset, prune, metadata-edit, or deletion commands against a user repository.

## Playbook A: Orphaned Worktree Metadata

Symptoms:

- `git worktree list` shows a path that no longer exists.
- Worktree entries include invalid or zero hashes.

Start non-destructively:

```bash
git worktree list --porcelain
git worktree prune -v
git worktree list --porcelain
```

If stale entries remain, resolve the shared metadata root:

```bash
git rev-parse --path-format=absolute --git-common-dir
```

Create a verified backup with `scripts/backup_git_metadata.py`. Then require explicit confirmation naming the exact stale path before removing anything beneath the resolved common Git directory.

## Playbook B: Phantom Branch Lock

Symptoms:

- `git branch -d` or `git branch -D` fails with "already used by worktree".
- `git worktree list` disagrees with observed branch ownership.

```bash
git worktree list --porcelain
```

Find the worktree using that branch, switch that worktree to another branch or intentionally detach it, then retry the branch operation in the main repository. Treat stale ownership metadata as Playbook A; do not guess a `.git/worktrees/...` path.

## Playbook C: Detached or Contradictory HEAD

For corroborated detached `HEAD`, preserve the current commit before switching:

```bash
git reflog --date=iso -n 20 HEAD
git branch rescue/$(date +%Y%m%d-%H%M%S) HEAD
git switch <known-good-branch>
```

For contradictory branch and symbolic-ref evidence, run the guided planner with `--repo` and `--output-dir`. It automatically creates and verifies a metadata archive before showing manual repair commands.

## Playbook D: Missing or Broken Refs

Symptoms: `unknown revision`, `not a valid object name`, or `cannot lock ref`.

Inspect and preserve local history first:

```bash
git reflog --date=iso -n 50 HEAD
git show <local-only-tip>
git branch rescue/$(date +%Y%m%d-%H%M%S) <local-only-tip>
git show-ref --verify refs/heads/rescue/<timestamp>
```

Then fetch and verify the exact remote target:

```bash
git fetch --all --prune
git show-ref --verify refs/remotes/origin/<branch>
git rev-parse --verify refs/remotes/origin/<branch>^{commit}
```

`git branch -f` moves a branch pointer. Immediately before it, obtain explicit point-of-risk confirmation naming the repository, local branch, verified remote ref, and resolved commit. Only that confirmation authorizes:

```bash
git branch -f <branch> refs/remotes/origin/<branch>
git switch <branch>
```

## Last Resort: Manual HEAD Repair

Resolve both metadata roots; linked worktrees have distinct values:

```bash
git rev-parse --path-format=absolute --git-dir
git rev-parse --path-format=absolute --git-common-dir
```

Create and verify the backup automatically:

```bash
python scripts/backup_git_metadata.py . --output-dir "$TASK_STATE_DIR"
```

The command archives the actual metadata directory or directories, verifies the required `HEAD` members, hashes the archive, and writes a JSON receipt. A failed or missing receipt blocks repair.

After checking the expected branch ref, obtain explicit point-of-risk confirmation naming the repository, expected branch, resolved ref, and backup receipt. Prefer:

```bash
git show-ref --verify refs/heads/<branch>
git symbolic-ref HEAD refs/heads/<branch>
```

If `symbolic-ref` cannot be used, obtain a second confirmation for the exact resolved per-worktree `HEAD` path. Use the fallback printed by `guided_repair_plan.py`; never write to a guessed `.git/HEAD` path. Immediately run the verification gate.

## Verification Gate

Run `references/recovery-checklist.md`. Minimum bar:

- `git status` exits cleanly with no fatal errors.
- symbolic `HEAD` matches the intended branch, or detached state is intentional and corroborated.
- `git worktree list --porcelain` has no missing paths and no unexplained zero hashes.
- `git fsck --no-reflogs --full` has no new critical errors.
- every rescue ref and changed branch pointer resolves to the expected commit.

## Escalation Path

1. Create a verified metadata archive with `scripts/backup_git_metadata.py`.
2. Clone fresh from the verified remote.
3. Recover unpushed work from rescue refs or reflog and cherry-pick into the fresh clone.
4. Document the failure mode and add a focused regression scenario.

## Automation Hooks

Worktree tooling must enforce:

- explicit controller task-state output
- preflight snapshot and state validation
- per-worktree/common metadata path resolution
- verified backup before manual metadata repair
- post-operation verification
- hard stop on unresolved HEAD/ref inconsistency
- point-of-risk confirmation before destructive commands

## Resources

- Symptom router: `references/symptom-map.md`
- Verification checklist: `references/recovery-checklist.md`
- Diagnostic snapshot script: `scripts/snapshot_git_state.py`
- Verified metadata backup: `scripts/backup_git_metadata.py`
- Guided plan generator: `scripts/guided_repair_plan.py`
- Disposable regression harness: `scripts/regression_harness.py`
