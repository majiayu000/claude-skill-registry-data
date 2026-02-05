---
name: gh-pr-issue
description: Keep pull requests and issues healthy using gh CLI (list, view, comment, close).
---

## When to Use
Invoke this skill when triaging review queues, summarizing checks, or updating GitHub issues. It wraps `gh pr` and `gh issue` commands so you can stay on top of reviews without leaving Opencode.

## Prerequisites
1. `gh` CLI authenticated (`gh auth login --scopes repo,workflow`).
2. `jq` installed for JSON parsing.
3. Environment variables (ask for them if absent):
   - `GITHUB_REPOSITORY`
   - `DEFAULT_BRANCH`

## Pull Request Procedures

### List Pull Requests (`/pr-list`)
1. Command template:
   ```bash
   gh pr list --repo "$GITHUB_REPOSITORY" \
     --state ${STATE:-open} \
     ${LABEL:+--label "$LABEL"} \
     ${SEARCH:+--search "$SEARCH"} \
     --limit ${LIMIT:-20} \
     --json number,title,author,reviewDecision,updatedAt,url
   ```
2. Pipe to `jq '.'`.
3. Highlight numbers, titles, reviewDecision, and last updated timestamps.

### View Pull Request (`/pr-checks`, `/pr-open`)
1. Fetch metadata + checks:
   ```bash
   gh pr view "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" \
     --json number,title,author,baseRefName,headRefName,isDraft,mergeable,reviewDecision,checks
   ```
2. Summarize failing checks with names, status, and URLs.
3. To open in browser, run `gh pr view "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" --web` (gh will launch the default browser; echo the URL when possible).

### Comment on Pull Request (`/pr-comment`)
1. Ensure a comment body exists; request it if missing.
2. Run `gh pr comment "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" --body "$BODY"`.
3. Share the resulting comment URL from gh output.

### Close / Reopen Pull Request (`/pr-close`)
1. Optional: leave a note explaining why the PR is closing.
2. If deleting the branch, append `--delete-branch`.
3. Command:
   ```bash
   [ -n "$BODY" ] && gh pr comment "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" --body "$BODY"
   gh pr close "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" ${DELETE_BRANCH:+--delete-branch}
   ```
4. Report final state.

## Issue Procedures

### List Issues (`/issue-list`)
1. Command template:
   ```bash
   gh issue list --repo "$GITHUB_REPOSITORY" \
     --state ${STATE:-open} \
     ${LABEL:+--label "$LABEL"} \
     ${SEARCH:+--search "$SEARCH"} \
     --limit ${LIMIT:-20} \
     --json number,title,author,assignees,updatedAt,url
   ```
2. Use `jq '.'` and summarize.

### View Issue (`/issue-view`)
1. Fetch metadata:
   ```bash
   gh issue view "$ISSUE_NUMBER" --repo "$GITHUB_REPOSITORY" \
     --json number,title,state,body,labels,assignees,url
   ```
2. Surface body excerpt, labels, assignees, and share the URL.

### Comment on Issue (`/issue-comment`)
1. Confirm comment body.
2. Run `gh issue comment "$ISSUE_NUMBER" --repo "$GITHUB_REPOSITORY" --body "$BODY"`.
3. Return confirmation output.

### Close or Reopen Issue (`/issue-close`, `/issue-reopen`)
1. For closing:
   - Optionally comment with context first.
   - Run `gh issue close "$ISSUE_NUMBER" --repo "$GITHUB_REPOSITORY"`.
2. For reopening:
   - Optionally state the reason.
   - Run `gh issue reopen "$ISSUE_NUMBER" --repo "$GITHUB_REPOSITORY"`.
3. Confirm the resulting state.

## Safety Checks
- Never mutate PRs/issues outside `GITHUB_REPOSITORY`.
- Validate required arguments (PR/issue numbers, comment bodies) before running gh commands.
- When summarizing checks, focus on failing or pending contexts to avoid noisy output.
