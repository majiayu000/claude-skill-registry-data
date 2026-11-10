---
name: azure-devops-work-item-start
description: Use when the user wants to start implementation from one or more Azure DevOps Work Item IDs in the current repository.
---

# Azure DevOps Work Item Start

## Scope

Start Azure DevOps Work Item work from the current repository by creating
isolated worktrees. A single directly actionable Work Item gets one branch and
worktree. Multiple Work Items get separate worktrees only when they are safe to
parallelize.

Read `../azure-devops-common/references/context.md` before fetching Work Items.

When `azure-devops-work-item-delivery` supplies an implementation brief, prepare
the workspace and baseline first, then dispatch one worker per item as in
Workflow step 6, also for a single item when delegation is available. Follow the
brief's dialogue/preflight/review/publication order rather than starting
implementation immediately. Pass the user's request,
exact target, and existing approvals to the worker; a brief alone grants none.

## Workflow

1. Resolve the current Azure DevOps organization, project, repository, and parse
   every Work Item ID in the prompt.
2. Fetch Work Item metadata with `az boards work-item show --id <id> --expand all`.
   - Collect dependencies from `Predecessor` relations and from
     `Blocked by #<id>` lines in the description.
   - Collect each Work Item's `Touched Areas` section when present. When it is
     absent, infer likely areas from the description and repository, and label
     them as inferred.
   - When multiple Work Items were provided, list open PRs with
     `az repos pr list`. For each PR, check its source and target names as
     `az repos pr list` returns them before running any command with them.
     When either name uses any character other than ASCII letters, digits,
     `/`, `.`, `_`, and `-`, it is not a **safe branch name**: skip that PR's
     comparison without writing the names into any command, report the PR and
     its branch as not compared, and continue. Otherwise run
     `node <script> -- '<target>' '<source>'`, where `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory. When it exits 3, or exits non-zero
     with stderr of one or more `unsafe branch name: ` lines and nothing else,
     skip and report that PR the same way and continue. On any other non-zero exit, including
     when the check cannot run, stop and report it. On exit 0, compare
     changed files with `git diff --name-only <target>...<source>` when both
     branches are available as local or remote-tracking refs. Do not fetch or
     check out branches only for this.
3. Summarize and classify each Work Item:
   - directly actionable implementation work
   - parent/tracking item
   - blocked or dependent on another Work Item or PR, including any item with
     a blocker that is not in a completed state under the project's process
   - ambiguous and needing clarification
4. For each directly actionable Work Item, choose a branch name:
   - format: `type/<id>-<slug>`
   - use `fix` for bugs, `feat` for user-facing behavior, and `chore` for
     maintenance or internal cleanup.
   - Derive `<slug>` from the Work Item title using only lowercase ASCII
     letters, digits, and hyphens (`[a-z0-9-]`); drop or replace every other
     character. If no characters remain, write a short English slug from the
     Work Item content in the same character set.
   - A **safe branch name** passes `node <script> -- '<name>'` with exit 0,
     where `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory. Write a name into this or any command
     only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any
     other name is not safe, without running the check. Use a branch name
     supplied by the user or reused from an existing worktree as-is only when it
     is a safe branch name; otherwise, including when the check cannot run, stop
     and report it before running any command with it.
5. If exactly one Work Item was provided:
   - Follow **Worktree Preparation** below, then implement in that worktree, or
     in its worker when a delivery brief dispatches one.
6. If multiple Work Items were provided:
   - Stop before creating worktrees unless the set is safe to parallelize.
   - Treat items as safe only when their touched areas do not overlap,
     including shared resources such as schemas, config, migrations,
     lockfiles, or public interfaces; they have no ordering dependency; and
     they do not require the same schema, config, workflow, or policy
     decision.
   - Also treat overlap between an item's touched areas and an open PR's
     changed files as a conflict with in-flight work. When stopping, report
     the overlapping areas.
   - Follow **Worktree Preparation** for each safe Work Item, keeping one branch
     and worktree per item with separate worker ownership.
   - Dispatch one worker per item/worktree within host capacity. Give it the
     Work Item/spec, assigned branch/path, base and baseline, repository rules,
     implementation brief, its touched areas marked as declared or inferred,
     the touched areas assigned to sibling workers, and expected
     verification/blocker report including files changed outside its touched
     areas. Keep every worker inside its assigned scope. The delivery caller
     coordinates these workers rather than launching a second set.
   - Before editing outside its touched areas, especially in a sibling's areas
     or shared resources, a worker pauses and reports the needed change instead
     of making it. Decide whether the change conflicts with a sibling before
     letting it continue; when it does, sequence the work or report the
     conflict to the user.
   - A worker chooses defaults only for implementation tactics. It returns
     contract, boundary, compatibility, and security decisions to the
     coordinator as questions with options and a recommendation, even when they
     look low-risk, and continues only work that does not depend on them. It
     never asks the user directly, and its report lists open questions and
     every default it chose.
7. Report each Work Item summary, branch, worktree path, base commit, baseline
   command/result, worker assignment when applicable, and next implementation step.

## Worktree Preparation

Use available worktree tools or Git directly; no separate worktree skill is required.

1. Inspect `git status --short` and `git worktree list --porcelain` before changing
   state. Reuse a worktree only when its branch, changes, and ownership match this
   Work Item and no other worker is using it. When reusing one, resolve its
   base as in step 2 and check its upstream as in step 5. Stop at a reused
   branch that is not a safe branch name, as in Workflow step 4.
2. Resolve the base from the user's request or repository convention. Otherwise
   inspect the default branch and local branch state, asking only if the intended
   base remains ambiguous. Do not assume a local ref is current or silently branch
   from another Work Item's branch. Record the chosen base ref and commit.
3. Prefer an available native worktree tool that supports the required base and
   dedicated branch; otherwise use Git. For manual creation, choose the location
   by user preference, then repository instructions or an established worktree
   directory, then `.worktrees/` at the repository root. Check path and branch
   collisions without overwriting or repurposing another item's workspace.
4. Before project-local creation, verify the actual target path with
   `git check-ignore`. Resolve missing ignore configuration under repository change
   and approval rules before creation; do not automatically commit that change.
   External locations do not need this check.
5. Follow applicable approval rules, honoring existing authorization for this
   Work Item's worktree, then use the selected tool or
   `git worktree add --no-track -b <branch> <path> <base>`. Verify the resulting path
   and branch; a detached workspace needs a dedicated Work Item branch before
   implementation. Read the upstream with
   `git config --get-all branch.<branch>.remote` and
   `git config --get-all branch.<branch>.merge`, which work without a
   remote-tracking ref; no output means no upstream, and more than one value
   for either key means stop and report. Keep no upstream or the
   same-named branch on the publication remote; publication sets it on first
   push. If the upstream is the base or its local branch (remote `.`), remove
   it with
   `git branch --unset-upstream <branch>`. Stop and report any other upstream,
   such as a differently named branch or another remote; it may back an
   existing PR.
6. Read instructions in the selected worktree and use documented setup commands.
   Use `repo-execution-context` when commands are unclear. Do not
   infer install commands solely from manifest filenames. Restore dependencies
   only as repository rules permit, without modifying manifests or lockfiles.
7. Run the smallest relevant documented baseline check before editing. Report
   existing failures or unavailable checks without claiming a clean baseline.
   Include the path, branch, base commit, and check result in each worker handoff.

If creation fails, diagnose and report it; do not silently implement in the
original checkout. Preserve unrelated changes in their original workspace and
obtain required approval before removing worktrees or branches during cleanup.

## Guardrails

- Do not assume cross-project Work Items.
- If no Work Item ID is provided, stop and ask for one.
- Do not commit or push without explicit approval.
- Dependency changes and manifest or lockfile edits require explicit approval;
  restoration from existing manifests and lockfiles follows repository rules.
- If setup, tests, or worktree creation fails, stop and report the failure.
- Do not close, update, assign, tag, transition, or comment on Work Items unless
  the user explicitly asks.
