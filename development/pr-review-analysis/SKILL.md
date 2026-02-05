---
name: pr-review-analysis
description: Analyze pull request from github review comments, classify each comment (correct, uncertain, incorrect), and produce an ordered implementation plan. Use this for PR review triage, code review feedback analysis, and planning follow-up changes based on reviewer comments.
---

# PR Review Analysis

## Purpose

Given a pull request (by URL, number, or branch name), fetch review comments and provide a structured, per comment assessment plus an ordered implementation plan.
**CONSTRAINT:** Use GitHub MCP for ALL GitHub data access and interactions. Do NOT use the `gh` CLI.

## Resolving the PR Identifier

Take the branch name and find the connected PR:

- Use GitHub MCP to get the PR connected to this branch by using `openPullRequest`.
- If none are open, look for the most recently updated closed PR from that head branch and clearly state it is closed.
- If no PR exists for that head branch, stop and report that no connected PR was found, plus the exact branch name you searched for.

## Data to fetch (via GitHub MCP only)

- PR metadata: title, state, draft status, base branch, head branch, commits, changed files summary.
- Full PR diff (or file-level diffs if the full diff is too large).
- Review threads and review comments (inline comments), including file path, line, side, and comment body.
- Optionally, check latest checks status if it helps validate comments about CI or tests.
- Use `ms-vscode.vscode-websearchforcopilot/websearch` and `ref.tools/*` to verify claims, check documentation, or research uncertain comments.

## Classification rules

For each review comment, assign exactly one:

- `correct`: The comment is factually correct and actionable given the current PR diff and repository conventions.
- `uncertain`: The comment might be valid but cannot be confirmed from the PR context alone (missing context, subjective preference, requires product decision, or depends on runtime behavior you cannot verify).
- `incorrect`: The comment is wrong or inapplicable to this PR.

When in doubt between `correct` and `uncertain`, choose `uncertain`.

## Repository conventions

**CRITICAL:** Do NOT hallucinate rules. Instead of relying on generic knowledge, you MUST read and apply the detailed rules found in the repository instruction files:

- Use `read_file` to read relevant files in `.github/instructions/` (e.g., `dev-instructions.instructions.md`, `payload.instructions.md`, `frontend.instructions.md`, `pull-requests.instructions.md`).
- Adhere strictly to the patterns and constraints defined in these files.

## Analysis procedure

1. Identify the resolved PR. Print the identifier.
2. Load all review comments.
3. For each comment:
   - Quote a short excerpt.
   - Locate the exact file/line in the PR diff.
   - Validate the claim against the code and **repository instruction files**.
   - **Verification:** If using `ms-vscode.vscode-websearchforcopilot/websearch` or `ref.tools/*` to verify the comment, you **MUST** include:
     - A link/reference to the source.
     - A direct text excerpt from that source supporting your rationale.
   - Classify as `correct`, `uncertain`, or `incorrect`.
   - Provide rationale with specific references:
     - File: `path/to/file`
     - Lines: X to Y
     - If the comment references code outside the diff, fetch that file section via MCP and cite the exact lines.
   - Assess impact across these dimensions (only include those that apply):
     - correctness, maintainability, performance, security, tests, ux
   - If you disagree with the comment, explain why and propose the better alternative.

## Consolidation into an implementation plan

**Requirement:** You MUST produce a clear, ordered plan.
After analyzing all comments:

1. Extract only actionable items that are `correct`.
2. Optionally include `uncertain` items as "needs decision" with a short question to unblock.
3. Produce an ordered plan that minimizes churn and risk:
   - correctness and security first
   - tests next
   - refactors and style last
4. Each plan step should reference which comment(s) it addresses.
5. Verify correctness by running only the relevant test suite (unit, integration, or storybook) corresponding to the changes.

## Confirmation before changes

Restate the ordered plan and ask for confirmation before writing code or proposing patches.

## Execution

When implementing fixes:

1. **Apply Changes:** Make the necessary code changes.
2. **Commit:** You MUST commit your changes after implementation.
   - If working with local files, ask the user to commit or use `run_in_terminal` with `git commit`.
   - If working remotely, use `mcp_io_github_git_create_or_update_file`.
3. **Reply & Resolve:** You MUST report back to the review thread and resolve the conversation.
   - Use `github/add_comment_to_pending_review` or `github/pull_request_review_write` to reply to the specific comment, stating that the fix has been applied (and referencing the commit SHA if possible).
   - Ensure the comment thread is resolved.
4. **Update PR:** Use `github/update_pull_request` if PR metadata details need updating.

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
