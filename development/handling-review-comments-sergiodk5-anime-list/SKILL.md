---
name: handling-review-comments
description: Handles GitHub pull request review comments. Use when asked to fix review comments, address PR feedback, or resolve review threads. Fetches comments via GitHub CLI, fixes issues in code, replies to reviewers, and resolves threads.
---

# Handling Review Comments

Process for addressing GitHub PR review comments efficiently using GitHub CLI.

## Prerequisites

- GitHub CLI installed and authenticated: `gh auth status`
- Repository cloned locally with push access

## Workflow

1. **Fetch comments** - Get all review comments from the PR
2. **Fix issues** - Implement fixes for each comment
3. **Run checks** - Verify fixes pass tests and linting
4. **Commit and push** - Group related fixes logically
5. **Reply to comments** - Confirm fixes with commit references
6. **Resolve threads** - Mark resolved via GraphQL API

## Fetching Comments

### Get All PR Comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments

# Example
gh api repos/sergiodk5/anime-list/pulls/9/comments
```

### Get Review Threads (with resolution status)

```bash
gh api graphql -f query='{
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr_number}) {
      reviewThreads(first: 20) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              body
              databaseId
            }
          }
        }
      }
    }
  }
}'
```

## Replying to Comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -X POST \
  -f body="Fixed in commit {hash}. {description of fix}"

# Example
gh api repos/sergiodk5/anime-list/pulls/9/comments/123456/replies \
  -X POST \
  -f body="Fixed in commit abc123. Added validation as suggested."
```

## Resolving Threads

### Single Thread

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID_HERE"}) {
    thread { isResolved }
  }
}'
```

### Multiple Threads

```bash
for thread_id in PRRT_abc123 PRRT_def456 PRRT_ghi789; do
  gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$thread_id\"}) { thread { isResolved } } }"
done
```

## Comment Categories

| Type | Action |
|------|--------|
| Bug/Security | Fix immediately, add tests if needed |
| Nitpick | Fix if reasonable, explain if not |
| Enhancement | Acknowledge, create follow-up issue if needed |
| Question | Answer clearly, add code comments if helpful |

## Before Pushing

```bash
npm run format && npm run lint && npm run test:unit
```

## Commit Message Format

Group related fixes in logical commits:

```bash
git commit -m "fix: address security review feedback

- Add input validation for user-provided colors
- Escape HTML in dynamic attributes
- Use separate timeout variables to prevent race conditions"
```

## Response Patterns

**For fixes:**
```
Fixed in commit abc123. Added validation as suggested.
```

**For acknowledged issues:**
```
Acknowledged. This will be addressed in a follow-up PR.
```

**For clarifications:**
```
This is intentional because [reason]. Happy to discuss further.
```

**For questions:**
```
Good question! This works by [explanation]. Added a code comment for clarity.
```

## Verify Resolution

```bash
gh api graphql -f query='{
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr_number}) {
      reviewThreads(first: 20) {
        nodes { isResolved }
      }
    }
  }
}'
```

## Complete Workflow Example

```bash
# 1. Fetch comments
gh api repos/sergiodk5/anime-list/pulls/9/comments

# 2. Fix issues in code (manual step)

# 3. Run checks
npm run format && npm run lint && npm run test:unit

# 4. Commit and push
git add . && git commit -m "fix: address review feedback" && git push

# 5. Reply to each comment
gh api repos/sergiodk5/anime-list/pulls/9/comments/{id}/replies \
  -X POST \
  -f body="Fixed in commit abc123..."

# 6. Resolve threads
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "..."}) { thread { isResolved } } }'
```

## Best Practices

1. **Fix Before Responding** - Implement fix before replying to ensure accuracy
2. **Reference Commits** - Include commit hashes so reviewers can verify
3. **Group Related Fixes** - Combine related changes in logical commits
4. **Run All Checks** - Ensure tests/lint pass before pushing
5. **Be Concise** - Keep replies brief but informative
