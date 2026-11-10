---
name: github-issue-start
description: Use when the user wants to start implementation from one or more GitHub issue numbers in the current repository, especially requests involving multiple issue IDs, separate workstreams, parallel issue work, or isolated issue worktrees.
---

# GitHub Issue Start

## Overview

Start GitHub issue work from the current repository by creating isolated
worktrees. A single issue gets one branch/worktree. Multiple issues are treated
as separate work items: create one branch/worktree per issue and run them in
parallel only after confirming the issues are independent enough to work safely.

When `github-issue-delivery` supplies an implementation brief, prepare the
workspace and baseline first, then dispatch one worker per issue under
**Parallel Worker Rules**, also for a single issue when delegation is available.
Follow the brief's dialogue, preflight, review, and publication order rather
than starting implementation immediately. Pass the user's request, exact target,
and existing approvals to the worker; a brief alone grants none.

## Workflow

1. Resolve the current repo from local git context and parse every `#<issue>` in the prompt.
2. Fetch the issue metadata with the GitHub plugin.
   - Collect dependencies from `Blocked by #<n>` lines in each body and from GitHub's native relationships with `gh api repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by`. If the relationship API is unavailable or fails, use the body lines alone and say so.
   - Collect each issue's `Touched Areas` section when present. When it is absent, infer likely areas from the body and repository, and label them as inferred.
   - When multiple issues were provided, list open PRs and fetch changed files with `gh pr view <number> --json files` for PRs that may overlap with the requested issues.
3. Summarize each issue in 1-2 lines and classify it:
   - directly actionable implementation work
   - parent/tracking issue
   - blocked or dependent on another issue/PR, including any issue with an open blocking issue
   - ambiguous and needing user clarification
4. For each directly actionable issue, choose a branch name:
   - format: `type/<id>-<slug>`
   - use a conventional-commit-style branch prefix such as `fix`, `feat`, or `chore`
   - use `fix` for bug fixes, `feat` for new user-facing behavior, and `chore` for maintenance or internal cleanup
   - Derive `<slug>` from the issue title using only lowercase ASCII letters, digits, and hyphens (`[a-z0-9-]`); drop or replace every other character. If no characters remain, write a short English slug from the issue content in the same character set.
   - A **safe branch name** passes `node <script> -- '<name>'` with exit 0, where `<script>` is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs) resolved from this skill's directory. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check. Use a branch name supplied by the user or reused from an existing worktree as-is only when it is a safe branch name; otherwise, including when the check cannot run, stop and report it before running any command with it.
5. If exactly one issue was provided:
   - Prepare the issue workspace using **Worktree Preparation** below.
   - Continue implementation in that worktree, or in its worker when a delivery brief dispatches one.
   - Report the issue summary, branch name, worktree path, baseline check result, and next implementation step.
6. If multiple issues were provided:
   - Decide whether the issues are safe to run in parallel before creating worktrees.
   - Treat issues as safe to parallelize only when their touched areas do not overlap, including shared resources such as schemas, config, migrations, lockfiles, or public interfaces; they have no ordering dependency; and they do not require the same schema/config/workflow decisions.
   - Also treat overlap between a requested issue's touched areas and an open PR's changed files as a conflict with in-flight work.
   - If any issue is blocked, ambiguous, a parent tracker, or likely to conflict with another requested issue or open PR, stop before creating worktrees. Report the unsafe grouping and the overlapping areas, and recommend a sequential order or a smaller safe parallel subset.
   - For every safe issue, follow **Worktree Preparation** separately, keeping one branch/worktree per issue.
   - Dispatch one worker per issue/worktree. Each worker owns only its assigned worktree and issue scope.
   - Continue coordinating the workers in parallel, then review and integrate their results when they finish.
   - Report the parallelization decision, each issue summary, branch name, worktree path, baseline check result, worker assignment, and expected next checkpoint.

## Worktree Preparation

Use the available worktree tools or ordinary Git commands directly; no separate
worktree skill is required.

1. Inspect `git status --short` and `git worktree list --porcelain` before changing state. Reuse an existing worktree only when its branch, changes, and ownership match this issue and no other worker is using it. Being in a linked worktree alone does not establish that it belongs to this issue. When reusing one, resolve its base as in step 2 and check its upstream as in step 5. Stop at a reused branch that is not a safe branch name, as in Workflow step 4.
2. Resolve the base, and for a new workspace its starting commit, from the user's requested base or the repository's documented convention. If neither identifies a base, inspect the default branch and local branch state; ask only if the intended base remains ambiguous. Do not silently branch from another issue's branch or assume a local ref is current. Record the chosen base ref and commit.
3. Prefer an available native worktree tool when it supports the required base and dedicated issue branch; otherwise plan to use Git directly. For manual creation, choose the location by explicit user preference, then repository instructions or an established worktree directory, then `.worktrees/` at the repository root. Check for path and branch collisions; do not overwrite, force checkout, or repurpose another issue's workspace.
4. Before creating a project-local worktree, verify the actual target path is ignored with `git check-ignore`. If it is not, resolve the ignore configuration under the repository's change and approval rules before creation. Do not automatically commit an ignore change. External worktree locations do not need this check.
5. Follow applicable approval rules, honoring authorization already given for this issue's worktree, then create it with the selected tool or `git worktree add --no-track -b <branch> <path> <base>`. Verify the resulting path and branch; a detached workspace still needs an issue branch before implementation. Read the upstream with `git config --get-all branch.<branch>.remote` and `git config --get-all branch.<branch>.merge`, which work without a remote-tracking ref; no output means no upstream, and more than one value for either key means stop and report. Keep no upstream or the same-named branch on the publication remote; publication sets it on first push. If the upstream is the base or its local branch (remote `.`), remove it with `git branch --unset-upstream <branch>`. Stop and report any other upstream, such as a differently named branch or another remote; it may back an existing PR.
6. Read the instructions in the selected worktree and run its documented setup. If commands are unclear, use `repo-execution-context`. Do not infer an install command solely from a manifest filename. Restore dependencies only as permitted by repository rules, using existing manifests and lockfiles without modifying them.
7. Run the smallest relevant documented baseline check before editing. Report the command and result, including existing failures or unavailable checks; do not claim a clean baseline when verification was blocked. Include the worktree path, branch, and base commit in the handoff.

If workspace creation fails, diagnose and report it; do not silently switch to
implementation in the original checkout. Keep unrelated changes in their
original workspace, and obtain required approval before removing worktrees or
branches during cleanup.

## Parallel Worker Rules

Give each worker a focused prompt with:

- the GitHub issue number, title, URL, and concise summary
- the assigned branch name and worktree path
- the issue's touched areas, marked as declared or inferred, and the touched areas assigned to sibling workers
- the repository guardrails from this skill and local project instructions
- clear ownership: work only inside the assigned worktree and only on the assigned issue
- a stop rule: before editing outside its touched areas, especially in a sibling worker's areas or shared resources, pause and report the needed change instead of making it
- a reminder that other workers may be active in sibling worktrees, so do not revert or edit outside the assigned scope
- a decision rule: choose defaults only for implementation tactics; return contract, boundary, compatibility, and security decisions to the coordinator as questions with options and a recommendation, even when they look low-risk, and continue only work that does not depend on them; never ask the user directly
- the expected return format: status, files changed, files changed outside its touched areas, tests run, open questions, every default chosen, blockers, and any follow-up needed

Do not use one worker for all requested issues. Do not let multiple workers edit
the same worktree. If a worker reports that its issue depends on another active
issue, pause that worker and report the dependency instead of forcing progress.
If a worker needs to edit outside its touched areas, decide whether the change
conflicts with a sibling worker before letting it continue; when it does,
sequence the work or report the conflict to the user.

## Guardrails

- Do not assume cross-repository work. This skill is current-repo only.
- If the prompt does not include at least one issue number, stop and ask for one.
- Do not commit or push without explicit approval.
- Dependency changes and manifest or lockfile edits require explicit approval; restoration from existing manifests and lockfiles follows repository rules.
- If setup, tests, or worktree creation fails, stop and report the failure before proceeding with additional worktrees or workers.
- Do not combine multiple requested issues into one branch just because the user listed them together.
- Do not dispatch parallel workers for issues with known ordering dependencies, shared migrations, shared schema decisions, overlapping touched areas, or likely edits to the same files.
- Do not close, label, assign, or comment on issues unless the user explicitly asks.
