---
name: celebrant
description: Use when the user runs /celebrant [target] [--full] [--auto]. Merges the current feature branch into the repo's default branch with a --no-ff merge commit, pushes, then deletes the now-merged branch local and remote. Runs a pre-merge /argonath gate (--quick by default, full under --full); a Hold warns but does not hard-stop. Refuses a dirty tree or being already on the target. One confirm before anything destructive — --auto skips it for unattended callers, and then a Hold stops the merge instead.
purpose: Merges the current feature branch into the default branch and deletes it, local and remote.
user_invocable: true
stage: merge
composes: argonath:dispatch, branch:dispatch, commit:dispatch
---

# Celebrant — The Confluence

The Celebrant, the Silverlode, runs down from the Misty Mountains through Lothlórien and pours itself into Anduin, the Great River — a tributary that joins the trunk and flows apart no longer. So this skill: a feature branch, its work done, is merged up into the repo's default branch, pushed, and cleared away — local and remote — its separate course at an end.

## Ethos

- **Confirm before the confluence.** The merge, the push, and the branch delete are destructive. One gate stands before them; the slash invocation alone is not authority for the irreversible. `--auto` is that authority given up front — and with no one to weigh a warning, a Hold becomes a stop.
- **The default branch is not assumed.** Not every repo flows to `master`. The target is resolved per-repo, the same way `/celebrimbor` resolves its base.
- **Safe-delete, never force.** The branch is removed with `git branch -d` (lowercase) — since it was just merged, `-d` succeeds; if anything is off, it stops loud rather than force-deleting work.
- **A clean tree only.** A half-committed state must not ride into the default branch. A dirty working tree is refused before any change.

## Argument parsing

`/celebrant [target] [--full] [--auto]`

| Argument | Required | Meaning |
|---|---|---|
| `target` | no | The branch to merge into. If omitted, resolved per the order below. |
| `--full` | no | Run the full `/argonath` gate (with the `/nazgul` + `/mithrandir` advisory rows). Default is `/argonath --quick` — artefact commands and the secret scan only. |
| `--auto` | no | Skip the step-4 confirm. An Argonath **Hold** then stops the run before any change, instead of warning. |

## Target resolution

The default branch is resolved in order; first hit wins:

1. explicit `target` argument
2. `base_branch.md` memory entry keyed by this repo's root path (the same map `/celebrimbor` reads)
3. `git symbolic-ref refs/remotes/origin/HEAD`, with the `refs/remotes/origin/` prefix stripped
4. fall back to `master` if it exists locally, else `main`

If none of these resolves, ask via AskUserQuestion (options `master`, `main`, plus the "Other" affordance) and stop if the user declines to name one.

## Workflow

### 1. Orient

```bash
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
```

If the first errors, stop:
> Not in a git repo — nothing to merge.

Hold the repo root and the current (feature) branch. Resolve `target` per the order above.

### 2. Refuse early

- If the current branch **is** the target, stop:
  > Already on `<target>` — there is no feature branch to merge up.
- Check the working tree:
  ```bash
  git status --porcelain
  ```
  If the output is non-empty, stop and report the dirty paths:
  > Working tree is dirty — commit or stash first (see `/commit`, `/branch`). Refusing to merge a half-finished state into `<target>`.

### 3. Pre-merge gate

Invoke `/argonath` via the Skill tool — `/argonath --quick` by default, or `/argonath` (full) when `--full` was given. Capture its **Pass / Hold** verdict.

Unless `--auto` (below), a **Hold** does not stop the flow here. Carry it into the confirm step as a warning; the user keeps the final say.

Under `--auto` there is no confirm to carry it to, so a **Hold** stops the run:
> Argonath holds — `--auto` will not merge past it. `<feature>` is left as it stands.

### 4. Confirm once

Present the plan via AskUserQuestion, including the Argonath verdict:

```
Merge  : <feature> → <target>
Steps  : pull <target> · merge --no-ff · push · delete <feature> (local + remote if present)
Gate   : <Pass | Hold — with one-line reason>
```

Proceed only on the user's word. If they decline, stop — nothing has changed.

Under `--auto`, skip this step: print the same block as plain text, then go straight to step 5.

### 5. Run the flow

```bash
git checkout <target>
git pull origin <target>
git merge --no-ff --no-edit <feature>
git push
```

`git pull origin <target>` is explicit rather than bare, so a `<target>` with no
upstream tracking branch still updates cleanly. If `git pull` or `git merge`
reports a conflict, **stop**: leave the tree as git left it, report the conflicting paths, and do **not** push or delete. The user resolves the conflict by hand.

On a clean merge and push, remove the branch:

```bash
git branch -d <feature>
```

Then delete the remote branch only if it exists:

```bash
git ls-remote --exit-code --heads origin <feature> && git push origin --delete <feature>
```

A remote branch that is absent is not an error — skip the remote delete silently.

### 6. Report

```
Merged : <feature> → <target>
Commit : <merge-commit subject>
Cleared: local ✓  remote <✓ | — absent>
Gate   : <Pass | Hold>
Confirm: <given | skipped — --auto>
```

A run stopped under `--auto` by a Hold renders no report — the stop message from step 3 stands in its place.

## Rules

- Never `git branch -D` (force) — only `-d`. If `-d` refuses, surface why and stop; do not escalate to force.
- Never merge a dirty tree, and never merge while standing on the target.
- One confirm gate covers the whole destructive sequence; do not prompt per git command. `--auto` removes that gate and nothing else — the dirty-tree, on-target, conflict, and `-d` rules all still stop the run, and a Hold stops it too.
- On any conflict, stop with the tree as git left it — no push, no delete.
- This skill operates on local + remote branches, not on the forge — it opens and closes no PR/MR.
