---
name: azure-devops-pr-create
description: Use only when the user explicitly requests azure-devops-pr-create, or azure-devops-pr-publish delegates PR creation for an explicitly user-requested publication workflow. Create or resolve an Azure DevOps PR without committing, pushing, or requesting review.
---

# Azure DevOps PR Create

## Scope

Use this skill to create or resolve an Azure DevOps pull request from the
current branch. This skill does not commit, push, request reviewers, vote,
complete, merge, or edit implementation files.

Read `../azure-devops-common/references/context.md` before resolving the target.

Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the branch and target branch, for PR creation or update.

## Workflow

1. Resolve repository context.
   - Confirm `git status --short --branch`.
   - Resolve the current branch and default branch.
   - Stop and report the branch unless it is a **safe branch name** before
     running any command with it: run `node <script> -- '<branch>'`, where
     `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory, and continue only on exit 0. Write a
     name into this or any command only when it uses solely ASCII letters,
     digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running
     the check.
   - Stop and report the target branch, the default branch unless the user
     specifies another target, unless it is a **safe branch name** before
     running any command with it: run `node <script> -- '<target>'` with the
     script above, and continue only on exit 0. Write a name into this or any
     command only when it uses solely ASCII letters, digits, `/`, `.`, `_`, and
     `-`; any other name is not safe, without running the check.
   - Resolve Azure DevOps organization, project, and repository.
   - Stop if the current branch is the default branch.
2. Find an optional PR template:
   - `docs/agents/azure-devops-pr-template.md`
   - `.azuredevops/PULL_REQUEST_TEMPLATE.md`
   - `.azuredevops/pull_request_template.md`
   - If no template exists, use a minimal body with summary and verification.
3. Build the PR body in a temporary file.
   - Preserve selected template headings and checklist structure.
   - Fill only facts supported by the current diff, commits, issue context, or
     verification logs.
   - Leave unknown fields as clear placeholders.
   - Apply [Work Item Links And State Transitions](../azure-devops-common/references/context.md#work-item-links-and-state-transitions)
     when preparing the body and selecting Work Item links.
4. Avoid duplicate PRs.
   - Use `az repos pr list` to check for an active PR from the current source
     branch to the selected target branch in the resolved repository.
   - If one exists, verify it with `az repos pr show`, check its Work Item links,
     and add only missing links authorized by this publication request. Preserve
     existing content and unrelated links; return the PR without creating another.
   - If multiple PRs match, stop and report the ambiguity.
   - After an uncertain create result, search again before retrying creation.
5. Create the PR.
   - Use the repository default branch unless the user specifies another target.
   - Use `az repos pr create`, applying the Work Item links selected in step 3.
6. Verify with `az repos pr show` and report the PR URL and whether it was new
   or existing.

## Guardrails

- Do not commit, push, complete, merge, vote, approve, or request reviewers.
- Do not create duplicate PRs.
- Do not modify repository files while preparing the PR body.
- Stop if Azure DevOps target resolution is ambiguous.
