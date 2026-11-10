---
name: azure-devops-pr-review
description: Use only when the user explicitly invokes `$azure-devops-pr-review` or names `azure-devops-pr-review` to review an Azure DevOps pull request in the current repository before merge.
---

# Azure DevOps PR Review

## Scope

Use this skill to perform a read-only Azure DevOps pull request review in the
current local repository. It reports an approval-equivalent, comment-equivalent,
or request-changes-equivalent verdict, but does not submit a vote or comment.

Read `../azure-devops-common/references/context.md` before resolving the target.

## Target Resolution

- Accept a PR ID, a same-repository Azure DevOps PR URL, or the PR associated
  with the current branch.
- If no PR can be resolved, stop and ask for the PR ID or URL.
- If a URL points to a different organization, project, or repository, stop.
- Do not checkout the PR branch.

## Workflow

1. Resolve repository and local state with `git status --short --branch`, git
   remotes, and `az devops configure --list`.
2. Resolve and fetch the PR with `az repos pr show`.
3. Fetch linked Work Items with `az repos pr work-item list`.
4. Fetch policy state with `az repos pr policy list`.
5. Fetch reviewers with `az repos pr reviewer list` when useful.
6. Fetch comments/thread state with Azure CLI if available, otherwise use
   read-only Azure DevOps REST API fallback when target resolution is certain.
7. Inspect the diff.
   - Prefer Azure DevOps CLI or REST diff when available.
   - Otherwise use read-only git fetch and local diff without changing branches.
8. Inspect local codebase with `rg` and `rg --files`.
9. Run local verification only when repository guidance makes a lightweight
   relevant command clear.
10. Review by risk for large PRs.

## Output Format

Lead with findings:

```markdown
**Findings**
- [Severity] <title> - <file:line or diff reference>
  <impact, evidence, and recommended fix>
- If no issues are found: No blocking findings found.

**Work Item Alignment**
- <whether the PR satisfies linked Work Item(s) and PR description>

**Test Gaps**
- <missing tests, build/policy failures, skipped local verification, or "None found">

**Review Comments State**
- <unresolved/stale/duplicate/resolved comments, or note that thread state was not verified>

**Residual Risk**
- <remaining merge risk and uninspected areas>

**Verdict**
- Approve equivalent | Comment equivalent | Request changes equivalent
- <one-sentence reason>

**Suggested Azure DevOps Comment**
- <only include a short paste-ready comment for request-changes-equivalent reviews or significant gaps>
```

## Guardrails

- Do not submit votes, comments, approvals, requests for changes, or reviewer
  requests.
- Do not resolve threads, complete, merge, checkout, commit, push, or edit files.
- Do not install dependencies or edit dependency manifests or lockfiles.
- If CI, policy, thread state, linked Work Items, or local verification cannot
  be checked, say so.
