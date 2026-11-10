---
name: github-pr-publish
description: Use only when the user explicitly requests `github-pr-publish`, or its publication phase through `github-pr-codex-review-cycle`, `github-pr-publish-and-ai-review-request`, or `github-issue-delivery`, for specified local branches or worktrees. Publish as a PR without requesting AI review in this phase.
---

# GitHub PR Publish

## Scope

Use this orchestration skill to publish one or more local branches or worktrees
as GitHub pull requests. It covers the normal path from local changes to a
remote PR: inspect state, verify, commit when needed, push, and create or reuse
the PR. Pull request templates are optional; use them when present and fall
back to a minimal generic PR body when absent.

This skill is not for:
- implementing feature changes before publication
- applying review feedback
- requesting AI, Copilot, Codex, or human review
- merging pull requests
- deleting branches or worktrees
- force pushing
- cleaning up after merge

## Approval Model

An explicit publication request can arrive directly or through the named
composing workflows. Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the target branches. Subject to governing approval
instructions, treat
the explicit publication request as approval for ordinary non-destructive commits
and normal pushes for the requested target branches. Ask for any missing approval
after preparing the verified publication target.

Still stop and ask before any action outside that narrow scope, including:

- force push, branch deletion, reset, rebase, amend, or merge
- staging secret-like files, credentials, tokens, private keys, or local-only config
- staging unrelated files that are not part of the requested work
- staging or publishing dependency manifests or lockfiles when the user did not explicitly ask for those changes
- publishing from the default branch

## Workflow

1. Resolve targets.
   - Identify each branch or worktree requested by the user.
   - If no target is specified, use the current worktree and branch.
   - For multiple targets, process them sequentially and stop on the first failure.
2. Resolve repository context for each target.
   - Confirm the target is inside a git repository.
   - Resolve the current branch with `git branch --show-current`. Stop and report the branch unless it is a **safe branch name** before running any command with it: run `node <script> -- '<branch>'`, where `<script>` is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs) resolved from this skill's directory, and continue only on exit 0. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check. The check also refuses a leading `+`, which would make the push refspec a force push.
   - Resolve the remote repository with `gh repo view --json nameWithOwner,url,defaultBranchRef`.
   - Stop and report the default branch, and a base the user specifies, unless each is a **safe branch name** before running any command with it: run `node <script> -- '<default branch>'`, adding `'<base>'` when the user specifies one, with the script above, and continue only on exit 0. Write a name into this or any command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running the check.
   - Resolve the push remote and the **head repository** by the **push target rule**: push only to the remote the user names, or the single remote that names the repository, with an explicit `<branch>:refs/heads/<branch>` refspec; with more than one remote and none named, ask. Run `node <push-script> resolve --github '<host>' '<owner>/<repo>'` with the resolved repository's `url` host and `nameWithOwner`, writing the host into the command only when it uses solely ASCII letters, digits, `.`, and `-`, optionally followed by `:` and digits, and `<owner>/<repo>` only when it uses solely ASCII letters, digits, `.`, `_`, `-`, and one `/` (otherwise stop and report), adding `--remote '<name>'` when the user names a remote that uses solely ASCII letters, digits, `/`, `.`, `_`, and `-` (ask again for any other name), where `<push-script>` is [`check-push-target.mjs`](../delivery-common/scripts/check-push-target.mjs) resolved from this skill's directory. On exit 0, line 1 is `<remote>` and line 2 is the head repository `<owner>/<repo>`. On exit 3, stop and ask the user to name the remote, listing the candidates it reports; stop and report any other status.
   - Stop if the current branch is the default branch.
3. Inspect local state before changing anything.
   - Run `git status --short --branch`.
   - Run `git diff --stat`.
   - Run `git diff --check`.
   - If `git diff --check` fails, stop and report the whitespace or conflict-marker problem.
   - Run `git log --oneline <default-branch>..HEAD` when the default branch is available locally.
   - Look for untracked or modified secret-like files such as `.env`, credentials, tokens, private keys, or local config. Do not stage them; stop or ask when they affect the requested commit.
   - Separate requested work from unrelated local changes. Do not stage unrelated files.
4. Confirm there is publishable work.
   - If the branch has no commits ahead of the base and no working tree changes for the requested work, stop and report that there is nothing to publish.
   - If there are working tree changes for the requested work, plan one logical commit from the implementation diff and the current conversation context.
   - If the branch already has suitable commits and no requested working tree changes, skip committing.
5. Confirm recent verification.
   - If the current conversation already has a successful verification log after the target's latest code changes, use it.
   - Otherwise determine the repository's required verification command from local guidance and run it before committing.
   - If the required verification command is not discoverable, ask the user which command to run before publishing.
   - If verification fails, stop that target and report the likely cause without committing, pushing, or creating a PR.
6. Commit when needed.
   - Use the `git-commit` skill for staging and commit message generation.
   - Stage only files belonging to the requested work.
   - Derive the commit message from the implementation diff, issue context, branch name, and current conversation.
   - Never stage secrets or unrelated local files.
7. Push the branch.
   - `<remote>` is the push remote resolved in step 2. The PR base branch is the existing PR's base, otherwise the base `github-pr-create` uses: the default branch unless the user specifies another base.
   - Before the push, run `node <push-script> pre --branch '<branch>' --remote '<remote>' --base '<base>'` with the PR base branch and the script from step 2; stop and report an existing PR's base that does not use solely ASCII letters, digits, `/`, `.`, `_`, and `-`. Continue only on exit 0, and report the note it prints when the push replaces a PR base upstream. On exit 3, stop and report the upstream it names; it may back an existing PR.
   - Push with `git push -u <remote> <branch>:refs/heads/<branch>`.
   - After the push, run `node <push-script> post --branch '<branch>' --remote '<remote>'`; stop and report unless it exits 0.
   - Do not force push, delete remote branches, or rewrite history.
8. Create or resolve the PR.
   - Use the `github-pr-create` skill for the target branch.
   - Pass the push remote and the head repository `<owner>/<repo>` from step 2; that skill uses them as given and opens a PR from another repository than the base as `--head <owner>:<branch>`.
   - That skill should use a pull request template when present and a minimal generic body when no template exists.
   - That skill should apply its related issue rules: `Closes #123` for issues fully completed by the PR, and `Refs #123` for parent trackers, partial work, follow-ups, or context.
   - Reuse an existing PR when one already exists for the branch.
9. Verify and report the result.
   - Run `gh pr view <number> --json number,url,title,state,baseRefName,headRefName` with the PR number from step 8.
   - Report the branch, commit SHA if one was created, push target, PR URL, whether the PR was new or existing, and the verification command/result.

## Output Format

Use this structure:

```markdown
**Published**
- Branch: `<branch>`
- Commit: `<sha>` or "No new commit needed"
- Push: `<remote>/<branch>`
- PR: <url>
- Verification: `<command>` passed

**Notes**
- <any skipped files, existing PR reuse, or follow-up needed>
```

For multiple targets, repeat the same fields per target.

## Guardrails

- Do not create a PR from the default branch.
- Do not force push, merge, delete remote branches, rewrite history, or clean up worktrees.
- Do not stage dependency manifests or lockfiles, edit them, or install dependencies unless the user explicitly asks.
- Do not hardcode or print secrets while summarizing diffs, commits, or templates.
