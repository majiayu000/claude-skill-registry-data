---
name: github-pr-create
description: Use only when the user explicitly requests `github-pr-create`, or when `github-pr-publish` delegates PR creation for an explicitly user-requested publication workflow. Create or resolve a PR from the current branch without committing, pushing, or requesting review.
---

# GitHub PR Create

## Scope

Use this skill to create a GitHub pull request from the current branch while
respecting the repository's pull request template when one exists. Templates
are optional; if no template exists, create a minimal generic body with summary
and test sections.

Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the branch and base, for PR creation.

This skill is not for:
- committing changes
- pushing branches
- requesting AI, Copilot, Codex, or human review
- merging pull requests
- editing implementation files

## Workflow

1. Resolve repository context.
   - Confirm the working directory is inside a git repository.
   - Resolve the current branch with `git branch --show-current`.
   - Stop and report the branch unless it is a **safe branch name** before running any command with it: run `node <script> -- '<branch>'`, where `<script>` is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs) resolved from this skill's directory, and continue only on exit 0. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check.
   - Resolve the remote repository with `gh repo view --json nameWithOwner,url,defaultBranchRef`. This is the PR **base repository**; `<base host>` is the host of its `url`.
   - Stop and report the base branch, the default branch unless the user specifies another base, unless it is a **safe branch name** before running any command with it: run `node <script> -- '<base>'` with the script above, and continue only on exit 0. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check.
   - Stop if the current branch is the default branch.
   - Resolve the **head repository**, the `<owner>/<repo>` the branch was pushed to. Use the push remote and `<owner>/<repo>` that `github-pr-publish` passes, as given, or a head `<owner>/<repo>` the user names. Otherwise, when the skill is invoked directly, resolve it by the push target rule in `github-pr-publish` step 2: run `node <push-script> resolve --github '<base host>' '<owner>/<repo>'` with the base repository's `nameWithOwner`, writing the host into the command only when it uses solely ASCII letters, digits, `.`, and `-`, optionally followed by `:` and digits, and `<owner>/<repo>` only when it uses solely ASCII letters, digits, `.`, `_`, `-`, and one `/` (otherwise stop and report), adding `--remote '<name>'` when the user names a remote that uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`, where `<push-script>` is [`check-push-target.mjs`](../delivery-common/scripts/check-push-target.mjs) resolved from this skill's directory. On exit 0, line 2 is the head repository. Otherwise stop and ask the user to name the head `<owner>/<repo>` or the remote; do not fall back to a bare `--head <branch>`.
   - Stop and report the head owner unless it is a **safe owner name**, using only `[A-Za-z0-9-]` and not starting with `-`. Check it before any command uses it, including an owner that `github-pr-publish` passes.
   - The PR is **cross-repository** when the head repository differs from the base repository, compared case-insensitively.
2. Find an optional pull request template.
   - Check these paths in order:
     - `.github/pull_request_template.md`
     - `.github/PULL_REQUEST_TEMPLATE.md`
     - `.github/PULL_REQUEST_TEMPLATE/*.md`
   - If multiple files exist under `.github/PULL_REQUEST_TEMPLATE/` and the right one is not obvious from the user request, stop and ask which template to use.
   - If no template exists, use a minimal generic body with summary and test sections.
3. Build the PR body in a temporary file.
   - Preserve the selected template headings and checklist structure.
   - Fill only facts supported by the current diff, commits, or verification logs.
   - Leave unknown template fields as clear placeholders instead of inventing details.
   - In the related issues section, use `Closes #123` when this PR fully
     satisfies the issue acceptance criteria and the issue should close when the
     PR merges.
   - Use `Refs #123` for parent trackers, umbrella issues, design/context
     issues, partial implementation, follow-up work, or related issues that are
     not fully completed by this PR.
   - Prefer `Closes` as the canonical auto-close keyword. Use `Fixes` only when
     the repo or user explicitly wants bug-fix wording. Do not use `Relates to`;
     use `Refs` for non-closing relationships.
   - For multiple completed issues, repeat the keyword for each issue, for
     example `Closes #123` and `Closes #124`, then add any parent tracker as
     `Refs #316`.
   - Do not use an auto-closing keyword for a parent tracker unless this PR
     completes the whole tracker.
4. Avoid duplicate PRs.
   - Run `gh pr view --json number,url,state,headRefName,baseRefName,headRepository,headRepositoryOwner` on the current branch.
   - If a PR exists and its head repository is the head repository (`headRepositoryOwner.login`/`headRepository.name`, compared case-insensitively), return that PR and do not create another one.
   - If a PR exists with another head repository or none, stop and report its number, URL, and head repository; do not create or reuse a PR.
5. Create the PR.
   - Use the repository default branch as the base unless the user specifies another base.
   - Use `gh pr create --base <base> --head <branch> --body-file <tmp-file>`.
   - For a cross-repository PR, pass `--head <owner>:<branch>` with the head repository's owner instead of `--head <branch>`.
   - If a title is not provided, derive a concise title from the branch name and recent commits.
6. Verify the result.
   - Run `gh pr view <number> --json number,url,title,state,baseRefName,headRefName,headRepository,headRepositoryOwner` with the PR number from step 4 or the URL `gh pr create` printed.
   - Stop and report unless the PR's head repository is the head repository.
   - Report the PR URL and whether it was newly created or already existed.

## Guardrails

- Do not commit, push, merge, or request reviews.
- Do not hardcode or print secrets while summarizing diffs or templates.
- Do not modify repository files while preparing the PR body.
- If GitHub authentication, permissions, or branch publication blocks PR creation, report the blocker and stop.
