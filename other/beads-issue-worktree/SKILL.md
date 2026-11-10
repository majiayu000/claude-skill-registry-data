---
name: beads-issue-worktree
description: Start implementation work from one or more Beads issue IDs in the current repository using isolated git worktrees and branches. Use when the user asks to work on a bead, start a bd issue, create a branch/worktree for a bead, or run multiple independent Beads workstreams.
---

# Beads Issue Worktree

## Overview

Start Beads issue work safely from the current repository. A single actionable bead gets one branch/worktree. Multiple beads get separate worktrees only when they are independent enough to work in parallel.

## Workflow

1. Run `bd prime`; if needed, run `bd where`.
2. Resolve bead IDs from the user prompt. If no ID is provided, run `bd ready` and ask which ready bead to start.
3. Inspect every target:
   - `bd show <id>`, including dependencies and the `Touched areas` section when present. When it is absent, infer likely areas from the description and repository, and label them as inferred.
   - classify as actionable, parent/tracker, blocked, already in progress, or ambiguous. Use `bd` dependencies as the source of truth for blocked; if a `Blocked by` section names a blocker that `bd` does not record, treat the bead as blocked and note the disagreement.
   - When multiple beads were requested, also inspect in-progress or claimed beads so their touched areas can be checked for conflicts.
4. Stop before creating worktrees if a bead is blocked, closed, a parent tracker, ambiguous, or likely to conflict with another requested bead or in-progress bead. Report the overlapping areas.
5. Choose branch/worktree names for actionable beads.
   - Branch format: `<type>/<bead-id>-<slug>`.
   - Use `fix` for bugs, `feat` for features, `chore` for maintenance/internal workflow.
   - Derive `<slug>` from the bead title using only lowercase ASCII letters, digits, and hyphens (`[a-z0-9-]`); drop or replace every other character. If no characters remain, write a short English slug from the bead content in the same character set.
   - A **safe branch name** passes `node <script> -- '<name>'` with exit 0, where `<script>` is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs) resolved from this skill's directory. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check. Use a branch name supplied by the user or reused from an existing worktree as-is only when it is a safe branch name; otherwise, including when the check cannot run, stop and report it before running any command with it.
6. Claim each actionable bead before editing:
   - `bd update <id> --claim`
7. Prepare the isolated workspace using **Worktree Preparation** below.
8. In the worktree, verify baseline before implementation.
   - Use repo docs and `repo-execution-context` to choose the smallest relevant documented test/build check.
   - If baseline fails, report the failure and ask before proceeding.
   - If checks are unavailable, report the limitation without claiming a clean baseline.
9. Report bead summary, branch, worktree path, base commit, baseline command/result, and next implementation step. Include these details in each worker handoff.

## Worktree Preparation

Use Beads or Git directly; no separate worktree skill is required.

1. Inspect `git status --short` and `git worktree list --porcelain` before changing workspace state. Reuse a worktree only when its branch, changes, and ownership match this bead and no other worker is using it. When reusing one, resolve its base as in step 2 and check its upstream as in step 5. Stop at a reused branch that is not a safe branch name, as in Workflow step 5.
2. Resolve the base from the user's request or repository convention. Otherwise inspect the default branch and local branch state, asking only if the intended base remains ambiguous. Do not assume a local ref is current or silently branch from another bead's branch. Record the chosen base ref and commit.
3. Choose the path by user preference, then repository instructions or an established worktree directory, then `.worktrees/<bead-id>-<slug>`. Check path and branch collisions without overwriting or repurposing another bead's workspace.
4. Before project-local creation, verify the actual target path with `git check-ignore`. Resolve missing ignore configuration under repository change and approval rules before creation; do not automatically commit that change. External locations do not need this check.
5. Follow applicable approval rules, honoring existing authorization for this bead's worktree. Prefer `bd worktree create` when it supports the required base, branch, and path; consult installed CLI help for supported options. Otherwise use `git worktree add --no-track -b <branch> <path> <base>`. Verify the resulting path and dedicated bead branch before implementation. Verify the upstream on either path: read it with `git config --get-all branch.<branch>.remote` and `git config --get-all branch.<branch>.merge`, which work without a remote-tracking ref; no output means no upstream, and more than one value for either key means stop and report. Keep no upstream or the same-named branch on the publication remote; publication sets it on first push. If the upstream is the base or its local branch (remote `.`), remove it with `git branch --unset-upstream <branch>`. Stop and report any other upstream, such as a differently named branch or another remote; it may back an existing PR.
6. Read instructions in the selected worktree and run its documented setup. Use `repo-execution-context` if commands are unclear; do not infer install commands solely from manifest filenames. Restore dependencies only as repository rules permit, without modifying manifests or lockfiles.

If creation fails, diagnose and report it; do not silently implement in the
original checkout. Obtain required approval before removing worktrees or branches
during cleanup.

## Multiple Beads

Create separate worktrees only when the beads' touched areas do not overlap, including shared resources such as schemas, config, migrations, lockfiles, or public interfaces; they have no dependency relationship; and they do not share schema/config/workflow decisions. Otherwise recommend a sequential order.

For parallel work, each worker owns exactly one bead and one worktree. Do not let two workers edit the same worktree.

Give each worker its bead's touched areas, marked as declared or inferred, and the touched areas assigned to sibling workers. Before editing outside its touched areas, especially in a sibling's areas or shared resources, the worker pauses and reports the needed change instead of making it. Its report lists files changed outside its touched areas. Decide whether such a change conflicts with a sibling before letting the worker continue; when it does, sequence the work or report the conflict to the user.

## Guardrails

- Do not commit, merge, push, close, or delete anything unless explicitly asked.
- Do not create a worktree for blocked or closed beads.
- Do not combine multiple beads into one branch unless the user explicitly approves.
- Preserve dirty worktree changes in the main checkout; do not revert user-owned changes.
- If worktree creation partially fails, inspect state before retrying.
