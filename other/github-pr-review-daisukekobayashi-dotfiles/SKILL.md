---
name: github-pr-review
description: Use only when the user explicitly invokes `$github-pr-review` or names `github-pr-review` to review a GitHub pull request in the current repository before merge.
---

# GitHub PR Review

## Scope

Use this skill to perform a read-only pull request review in the current local
repository. The review covers PR metadata, body, diff, review comments and
thread state, CI, linked issues, repository guidance, and the local codebase.

This skill reports an approval-equivalent, comment-equivalent, or request
changes-equivalent verdict, but it does not submit a GitHub review.

This skill is not for creating PRs, requesting reviewers, applying fixes,
commenting on GitHub, resolving threads, merging, committing, pushing, or
checking out branches.

## Target Resolution

- Accept a PR number, a same-repository PR URL, or the PR associated with the
  current branch.
- If no PR number or URL is provided, resolve the current branch PR with
  `gh pr view --json number,url,headRefName,baseRefName`.
- If no PR can be resolved from the current branch, stop and ask for the PR
  number or URL.
- If a URL points to a different repository, stop and explain that this skill is
  current-repository only.
- Do not run `gh pr checkout` or otherwise change branches.
- If the target PR is the current branch's PR, include the current working tree
  as review evidence. Distinguish PR diff findings from uncommitted local
  working-tree observations.

## Workflow

1. Resolve repository and local state.
   - Confirm the branch and dirty state with `git status --short --branch`.
   - Resolve the current GitHub repository with
     `gh repo view --json nameWithOwner,url,defaultBranchRef`.
   - Read applicable repository instructions such as `AGENTS.md` before making
     recommendations.
2. Resolve and fetch the target PR.
   - Use `gh pr view <number> --json number,title,body,author,baseRefName,headRefName,isDraft,mergeable,reviewDecision,labels,assignees,comments,reviews,url,state,createdAt,updatedAt,additions,deletions,changedFiles,files,commits,statusCheckRollup`.
   - Fetch the diff with `gh pr diff <number> --patch`.
   - If GitHub authentication, permissions, or network access blocks the read,
     report the blocker and stop.
3. Fetch CI state.
   - Use `gh pr checks <number>` when available.
   - Treat failing required checks, failing tests, build failures, or unknown
     required CI as review evidence.
4. Fetch review comments with thread state when possible.
   - Do not rely only on flat PR comments when thread state matters.
   - Use a read-only GraphQL query through `gh api graphql` to fetch
     `reviewThreads` with `isResolved`, file path, line, and comments when
     available.
   - If thread state cannot be fetched, state that thread resolution state was
     not verified.
5. Inspect linked issues.
   - Parse same-repository issue references from the PR body, branch name,
     commit messages, comments, and closing keywords.
   - Fetch linked issues one level deep with `gh issue view`.
   - Do not traverse links found inside linked issues.
6. Inspect the local codebase.
   - Use `rg` and `rg --files` first.
   - Review touched files, nearby code, tests, configuration, schemas,
     migrations, and runtime paths affected by the diff.
   - For the current branch's PR, use the current working tree directly, while
     separating uncommitted local changes from the PR diff.
   - For non-current-branch PRs, review through `gh pr diff`, fetched metadata,
     and local repository context without changing branches.
7. Run local verification only when safe and clear.
   - Always read CI state.
   - Run local lint or tests only when repository instructions or scripts make a
     lightweight relevant command clear.
   - Prefer focused commands over full suites for large repositories.
   - If a verification command fails, stop additional verification, identify the
     likely cause, and include the failure in the review.
   - Do not install dependencies or edit manifests/lockfiles to make tests run.
8. Review by risk for large PRs.
   - Build a quick risk map from changed files, diff size, critical paths,
     linked issue requirements, CI, and review threads.
   - Prioritize high-risk areas over shallow coverage of every file.
   - State inspected and uninspected areas when coverage is partial.

## Findings Criteria

Use findings-first code review judgment.

Request changes-equivalent issues include user-visible regressions, data loss or
data corruption risk, security problems, CI failures, broken migrations,
operational risk, or failing to satisfy the linked issue or PR objective.

Comment-equivalent issues include non-blocking maintainability concerns, small
test gaps, naming, minor refactors, and style preferences.

Approve-equivalent is appropriate only when no blocking findings are found and
remaining risks or test gaps are clearly non-blocking.

## Output Format

Respond in the user's language. Lead with findings.

```markdown
**Findings**
- [Severity] <title> - <file:line or diff reference>
  <impact, evidence, and recommended fix>
- If no issues are found: No blocking findings found.

**Issue Alignment**
- <whether the PR satisfies linked issue(s) and PR description>

**Test Gaps**
- <missing tests, CI failures, skipped local verification, or "None found">

**Review Comments State**
- <unresolved/stale/duplicate/resolved comments, or note that thread state was not verified>

**Residual Risk**
- <remaining merge risk and uninspected areas>

**Verdict**
- Approve equivalent | Comment equivalent | Request changes equivalent
- <one-sentence reason>

**Suggested GitHub Comment**
- <only include a short paste-ready comment for request changes-equivalent reviews or significant gaps>
```

For each finding, include a concrete file and line or diff reference whenever
possible. If exact line numbers are unavailable from `gh pr diff`, reference the
file and hunk context instead.

## Guardrails

- Do not submit a GitHub review, comment, resolve threads, request reviewers, or
  merge the PR.
- Do not edit files, apply fixes, create commits, push, or create branches.
- Do not run `gh pr checkout`, `git checkout`, or any command that changes the
  current branch to inspect the PR.
- Do not install dependencies or edit dependency manifests or lockfiles.
- Do not assume cross-repository context.
- Do not hide uncertainty. If CI, review thread state, linked issues, or local
  verification could not be checked, say so in the review.
- Do not inflate style preferences into blocking findings.
