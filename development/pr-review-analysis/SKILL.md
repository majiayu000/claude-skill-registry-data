---
name: pr-review-analysis
description: Analyze pull request review comments, classify each comment (correct, uncertain, incorrect), and produce an ordered implementation plan. Use this for PR review triage, code review feedback analysis, and planning follow-up changes based on reviewer comments.
---

# PR Review Analysis

## Purpose
Given a pull request (by URL, number, or branch name), fetch review comments and provide a structured, per comment assessment plus an ordered implementation plan. Prefer GitHub MCP for all GitHub data access.

## Inputs
- `pr` (required): PR URL, PR number, or feature branch name (e.g., `feature/foo`).

## Resolving the PR Identifier
1. If `pr` looks like a URL, parse the PR number and repository from it, then load that PR.
2. If `pr` is a number, treat it as a PR number for the current repository context.
3. Otherwise treat `pr` as a branch name and find the connected PR:
   - Use GitHub MCP to get the PR connected to this branch by using `github.vscode-pull-request-github/openPullRequest`
   - If none are open, look for the most recently updated closed PR from that head branch and clearly state it is closed.
   - If no PR exists for that head branch, stop and report that no connected PR was found, plus the exact branch name you searched for.

## Data to fetch (via GitHub MCP)
- PR metadata: title, state, draft status, base branch, head branch, commits, changed files summary.
- Full PR diff (or file-level diffs if the full diff is too large).
- Review threads and review comments (inline comments), including file path, line, side, and comment body.
- Optionally, check latest checks status if it helps validate comments about CI or tests.
- Use `vscode-websearchforcopilot_webSearch` and `mcp_ref_tools_ref_search_documentation` to verify claims, check documentation, or research uncertain comments.

## Classification rules
For each review comment, assign exactly one:
- `correct`: The comment is factually correct and actionable given the current PR diff and repository conventions.
- `uncertain`: The comment might be valid but cannot be confirmed from the PR context alone (missing context, subjective preference, requires product decision, or depends on runtime behavior you cannot verify).
- `incorrect`: The comment is wrong or inapplicable to this PR (for example the code already does it, the file/line changed, the rationale conflicts with the diff, or it misunderstands the architecture).

When in doubt between `correct` and `uncertain`, choose `uncertain`.

## Analysis procedure
1. Identify the resolved PR (see the PR resolution section). Print the resolved PR identifier at the top of the output (repo, PR number, head, base).
2. Load all review comments and group them by file.
3. For each comment:
   - Quote a short, relevant excerpt (max 2 sentences) of the comment.
   - Locate the exact file path and line range in the PR diff.
   - Validate the claim against the code shown in the diff and any relevant repository conventions.
   - Classify as `correct`, `uncertain`, or `incorrect`.
   - Provide rationale with specific references:
     - File: `path/to/file`
     - Lines: X to Y
     - If the comment references code outside the diff, fetch that file section via MCP and cite the exact lines.
   - Assess impact across these dimensions (only include those that apply):
     - correctness, maintainability, performance, security, tests, ux
   - If you disagree with the comment, explain why and propose the better alternative.

## Consolidation into an implementation plan
After analyzing all comments:
1. Extract only actionable items that are `correct`.
2. Optionally include `uncertain` items as "needs decision" with a short question to unblock.
3. Produce an ordered plan that minimizes churn and risk:
   - correctness and security first
   - tests next
   - refactors and style last
4. Each plan step should reference which comment(s) it addresses.
5. Verify correctness by running only the relevant test suite (unit, integration, or storybook) corresponding to the changes.

## Repository conventions (apply when relevant)
- Tests live in `tests/`.
- Schema and database changes must use the Payload CLI migrations workflow (no raw SQL or drizzle); ensure migrations are created and applied.
- Business logic and side effects belong in Payload hooks (see `src/hooks/**` and `collections/*/hooks/**`), not in React components.
- Access control must be centralized by reusing utilities in `src/access/` instead of adding ad-hoc role checks.
- Respect soft delete semantics for collections with `trash: true` and avoid patterns that assume hard deletes.
- Do NOT use the `any` type. Use `unknown` for uncertain data and narrow it using type guards, Zod schemas, or explicit casting (`as unknown as T`) if absolutely necessary.

## Confirmation before changes
If the user asks you to implement changes, first restate the ordered plan and ask for confirmation before writing code or proposing patches.

## Execution
When implementing fixes:
- Use `mcp_io_github_git_update_pull_request` to update PR details if needed.
- Close incorrect comments and add short comments when fixed.
- Commit and push changes to the PR branch by using conventional commits.

## Output format
Resolved PR:
- Repo: `<owner>/<repo>`
- PR: `#<number>`
- Head: `<head-branch>`
- Base: `<base-branch>`
- State: `<open|closed|merged>`, Draft: `<true|false>`

1. Comment 1
   - Location: `path/to/file` lines X to Y
   - Excerpt: "..."
   - Classification: correct | uncertain | incorrect
   - Rationale: ...
   - Impact: ...
   - Suggested action (if any): ...

2. Comment 2
   - Location: ...
   - Excerpt: "..."
   - Classification: ...
   - Rationale: ...
   - Impact: ...
   - Suggested action (if any): ...

Final Plan
1. ...
2. ...
3. ...

Needs decision (if any)
- ...

Confirmation
- Do you want me to implement the Final Plan in this PR (yes or no)?
