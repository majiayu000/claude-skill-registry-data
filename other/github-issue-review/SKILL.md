---
name: github-issue-review
description: Use only when the user explicitly invokes `$github-issue-review` or names `github-issue-review` to review a GitHub issue in the current repository before implementation.
---

# GitHub Issue Review

## Scope

Use this skill to review whether a GitHub issue is ready for implementation in
the current local repository. The review covers the issue body, comments,
related issues and pull requests, repository guidance, and the local codebase.

This skill is read-only. It is not for creating, editing, labeling, assigning,
closing, or commenting on issues. It is not for starting implementation.

## Target Resolution

- Require an issue number such as `#123`, an issue number such as `123`, or a
  GitHub issue URL for the current repository.
- If no issue number or URL is provided, stop and ask for the issue number.
- Do not infer the issue from the current branch name.
- If a URL points to a different repository, stop and explain that this skill is
  current-repository only.

## Workflow

1. Resolve repository context.
   - Confirm local state with `git status --short --branch`.
   - Resolve the current GitHub repository with
     `gh repo view --json nameWithOwner,url,defaultBranchRef`.
   - Read applicable repository instructions such as `AGENTS.md` before making
     recommendations.
2. Fetch the target issue.
   - Use `gh issue view <number> --json number,title,body,labels,assignees,author,comments,url,state,createdAt,updatedAt,milestone`.
   - If GitHub authentication, permissions, or network access blocks the read,
     report the blocker and stop.
3. Inspect one-hop related GitHub context.
   - Parse clearly related same-repository issue and PR references from the
     issue body and comments.
   - Check same-repository linked issues and PRs one level deep only.
   - Use `gh issue view` and `gh pr view` for linked items. Use read-only
     `gh api` queries only when the regular `gh` commands do not expose needed
     relationship data.
   - Do not traverse links found inside the linked items.
4. Check for duplicate or already-active work.
   - List open PRs with
     `gh pr list --state open --limit 100 --json number,title,headRefName,baseRefName,labels,updatedAt,url,body`.
   - Look for PRs that reference the issue number or URL, implement the same
     title, or cover the same files or behavior.
5. Read the local codebase.
   - Use `rg` and `rg --files` first.
   - Inspect repository docs and likely implementation areas named by the issue.
   - Check whether the requested behavior already exists, conflicts with local
     architecture, needs schema or config decisions, or has a larger blast
     radius than the issue describes.
   - Do not edit files.
6. Apply the readiness gate.
   - Mark the issue ready only when acceptance criteria are verifiable and the
     scope boundary and dependencies are clear.
   - If the issue is broad, ambiguous, missing acceptance criteria, blocked, or
     dependent on unresolved design choices, prefer "needs revision", "split",
     or "hold" over "ready".
7. For large issues, review by risk.
   - Build a quick risk map from the requested behavior, touched subsystems,
     dependency chain, and existing code.
   - Review high-risk areas first.
   - State which areas were inspected and which were not.

## Output Format

Respond in the user's language. Use this structure:

```markdown
**Verdict**
- Ready to implement | Needs revision before implementation | Split before implementation | Hold
- <one-sentence reason>

**Critical Gaps**
- <missing acceptance criteria, ambiguous behavior, dependency, or "None found">

**Scope & Dependencies**
- <related issues/PRs, blockers, sequencing, duplicates, or "No blockers found">

**Codebase Fit**
- <existing implementation notes, affected areas, feasibility, risks>

**Suggested Revision**
- <specific issue-body changes that would make the issue clearer>

**Implementation Notes**
- <guidance for the eventual implementer without starting implementation>

**Open Questions**
- <questions for the owner/user, or "None">

**Reviewed Scope**
- <only include when the issue was large or partially inspected>

**Suggested GitHub Comment**
- <only include a short paste-ready comment when the issue needs revision, split, or hold>
```

Keep the review concise but auditable. Tie claims to issue text, comments,
linked GitHub objects, repository docs, or local code references.

## Guardrails

- Do not create, edit, label, assign, close, or comment on GitHub issues.
- Do not create worktrees, branches, commits, pull requests, or implementation
  changes.
- Do not install dependencies or edit dependency manifests or lockfiles.
- Do not assume cross-repository context.
- Do not invent requirements. Unknowns should become open questions or suggested
  issue revisions.
- Do not treat a parent tracking issue as implementation-ready unless its
  actionable child scope is already explicit and complete.
