---
name: address-pr-comments
description: Automatically address unresolved PR review comments, commit fixes, and resolve threads
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(git *) Read Edit Grep
---

# Address PR Comments

Fetch unresolved PR review comments, propose fixes for user approval, implement approved changes, commit and push, then mark comments as resolved.

## Invocation

- `/address-pr-comments` - Uses current branch's PR
- `/address-pr-comments 123` - Addresses comments on PR #123
- "address the PR comments" or "fix the PR review comments"

## Instructions

### 1. Identify the Pull Request

If a PR number is provided as an argument, use that. Otherwise:

```bash
git branch --show-current
gh pr list --head <branch-name> --json number,url --jq '.[0]'
```

### 2. Fetch Unresolved Review Threads

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          path
          line
          comments(first: 10) {
            nodes {
              body
              author { login }
            }
          }
        }
      }
    }
  }
}' -f owner=<OWNER> -f repo=<REPO> -F pr=<PR_NUMBER>
```

Filter to only unresolved threads (`isResolved: false`).

### 3. Present Comments and Get User Approval

**CRITICAL: Always ask for user confirmation before making changes.**

For each unresolved comment:
1. Read the file mentioned in the thread's `path` field
2. Analyze the comment — understand what change is being requested
3. Propose a fix — explain what you plan to change
4. Use AskUserQuestion to get approval before implementing

Options:
- "Apply this fix" - Implement the proposed change
- "Skip this comment" - Don't address, don't resolve
- "Mark resolved without changes" - Already fixed or not applicable

### 4. Implement Approved Changes

Only after user approval — make code changes for approved fixes.

### 5. Commit and Push Changes

```bash
git add -A
git commit -m "fix: address PR review comments

- <summary of changes made>"
git push origin <branch-name>
```

### 6. Resolve Approved Threads

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) { thread { isResolved } }
}'
```

### 7. Report Summary

- Number of comments addressed vs. skipped
- Files modified
- Commit hash
- Link to the PR
