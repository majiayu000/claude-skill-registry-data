---
name: azure-devops-pr-publish
description: Use only when the user explicitly requests azure-devops-pr-publish, or its publication phase through azure-devops-work-item-delivery, for specified local Azure DevOps branches or worktrees. Publish as a PR without requesting AI review.
---

# Azure DevOps PR Publish

## Scope

Use this orchestration skill to publish one or more local branches or worktrees
as Azure DevOps pull requests. It covers the normal path from local changes to a
remote PR: inspect state, verify, commit when needed, push, and create or reuse
the PR.

Read `../azure-devops-common/references/context.md` before resolving targets.

## Approval Model

An explicit publication request can arrive directly or through
`azure-devops-work-item-delivery`. Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the target branches. Subject to governing approval
instructions,
treat that request as approval for ordinary non-destructive commits and normal
pushes for the requested target branches. Prepare the verified publication target
before asking for any missing approval.

Still stop and ask before:

- force push, branch deletion, reset, rebase, amend, or merge
- staging secret-like files, credentials, private keys, or local-only config
- staging unrelated files
- staging or publishing dependency manifests or lockfiles without explicit
  approval
- publishing from the default branch
- completing PRs, enabling auto-complete, changing policies, voting, approving,
  or requesting reviewers

## Workflow

1. Resolve targets from the user request. If none is specified, use the current
   worktree and branch. For multiple targets, process them sequentially and
   stop on the first failure.
2. Resolve Azure DevOps organization, project, repository, default branch, and
   current branch for each target.
   - Stop and report the branch unless it is a **safe branch name** before
     running any command with it: run `node <script> -- '<branch>'`, where
     `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory, and continue only on exit 0. Write a
     name into this or any command only when it uses solely ASCII letters,
     digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running
     the check. The check also refuses a leading `+`, which would make the push
     refspec a force push.
   - Stop and report the default branch, and a target the user specifies,
     unless each is a **safe branch name** before running any command with
     it: run `node <script> -- '<default branch>'`, adding `'<target>'` when
     the user specifies one, with the script above, and continue only on
     exit 0. Write a name into this or any command only when it uses solely
     ASCII letters, digits, `/`, `.`, `_`, and `-`; any other name is not
     safe, without running the check.
   - Resolve the push remote by the **push target rule**: push only to the
     remote the user names, or the single remote that names the repository,
     with an explicit `<branch>:refs/heads/<branch>` refspec; with more than one
     remote and none named, ask. Run `node <push-script> resolve --azure '<org>'
     '<project>' '<repo>'` with the resolved organization, project, and
     repository, percent-decoded (`My Project`, not `My%20Project`), writing
     each into the command only when it uses solely ASCII letters, digits,
     space, `.`, `_`, and `-` (otherwise stop and report),
     adding `--remote '<name>'` when the user names a remote that uses solely
     ASCII letters, digits, `/`, `.`, `_`, and `-` (ask again for any other
     name), where `<push-script>` is
     [`check-push-target.mjs`](../delivery-common/scripts/check-push-target.mjs)
     resolved from this skill's directory. It matches the accepted remote URL
     shapes from the common context. On exit 0, its output is `<remote>`. On
     exit 3, stop and ask the user to name the remote, listing the candidates
     it reports; stop and report any other status.
3. Inspect local state:
   - `git status --short --branch`
   - `git diff --stat`
   - `git diff --check`
   - `git log --oneline <default-branch>..HEAD` when available
4. Stop if there is no publishable work.
5. Confirm recent verification.
   - Use a successful verification log from the current conversation only if it
     happened after the latest changes.
   - Otherwise determine and run the repository's required verification command.
   - Stop if verification fails.
   - Before pushing, inspect any matching active PR for enabled auto-complete.
     If enabled, hold publication for an explicit decision: a push could merge
     the PR before separate merge approval. Do not silently disable it.
6. Commit when needed.
   - Use the `git-commit` skill.
   - Stage only files belonging to the requested work.
7. Push the branch.
   - `<remote>` is the push remote resolved in step 2. The PR base branch
     is the existing PR's target, otherwise the target
     `azure-devops-pr-create` uses: the default branch unless the user
     specifies another target.
   - Before the push, run `node <push-script> pre --branch '<branch>' --remote
     '<remote>' --base '<target>'` with the PR base branch and the script from
     step 2; stop and report an existing PR's target that does not use solely
     ASCII letters, digits, `/`, `.`, `_`, and `-`. Continue only on exit 0,
     and report the note it prints when the push replaces a PR base upstream.
     On exit 3, stop and report the upstream it names; it may back an existing
     PR.
   - Push with `git push -u <remote> <branch>:refs/heads/<branch>`.
   - After the push, run `node <push-script> post --branch '<branch>' --remote
     '<remote>'`; stop and report unless it exits 0.
8. Use `azure-devops-pr-create` to create or resolve the PR.
   - Pass along the actual publication request, exact target, existing approvals,
     known Work Item IDs, completion scope, and the user's state-transition intent.
9. Verify with `az repos pr show` and report branch, commit, push target, PR URL,
   and verification result.

## Guardrails

- Do not create PRs from the default branch.
- Do not force push, rewrite history, merge, complete, or clean up worktrees.
- Do not hardcode or print secrets while summarizing diffs, commits, or templates.
