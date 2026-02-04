---
name: github-interaction
description: Comprehensive guide for working with GitHub data and APIs. Use when fetching issues, PRs, discussions, comments, reviews, or any GitHub content. Covers tool selection (mcp_github vs fetch vs semantic search), complete conversation fetching patterns, pagination handling, and common workflows. Critical for avoiding standard API failures when fetching comments/reviews—MCP tools required.
---

# GitHub Interaction

Guide for effective GitHub data retrieval covering tool selection, complete conversation fetching, and common patterns.

## Critical Rule: MCP Tools for Comments and Reviews

**ALWAYS use GitHub MCP tools (`mcp_github_*`) to fetch PR/issue comments and reviews. Standard API access will fail.**

This is the most common mistake. When you need comments, reviews, or discussion threads, you MUST use the MCP tools.

## Tool Selection Decision Tree

### When to use `mcp_github_*` tools

Use for ALL GitHub data operations:
- ✅ Fetching issues, PRs, discussions (individual or lists)
- ✅ **Getting comments** (issue comments, PR review comments, discussion comments)
- ✅ **Getting reviews** (PR reviews and review threads)
- ✅ Getting file contents from repos
- ✅ Creating/updating issues, PRs, comments
- ✅ Searching issues, PRs, code, repositories, users
- ✅ Managing branches, commits, assignees, labels

**Examples**:
```
mcp_github_issue_read (method: get, get_comments, get_sub_issues, get_labels)
mcp_github_pull_request_read (method: get, get_diff, get_files, get_review_comments, get_reviews, get_comments)
mcp_github_get_discussion + mcp_github_get_discussion_comments
mcp_github_search_issues, mcp_github_search_pull_requests, mcp_github_search_code
mcp_github_get_file_contents
```

### When to use `fetch_webpage`

Use ONLY for external web content:
- ✅ Public documentation sites
- ✅ Blog posts, articles (not on GitHub)
- ✅ External APIs or services
- ❌ NEVER for GitHub issues/PRs/discussions/comments

### When to use `github_repo` semantic search

Use for finding code patterns across GitHub repositories:
- ✅ Searching for function/class implementations across repos
- ✅ Finding usage examples in codebases
- ✅ Discovering patterns in specific GitHub repo source code
- ❌ Not for issues/PRs/discussions (use `mcp_github_search_*` instead)

### When to use `grep_search` / `semantic_search`

Use for LOCAL workspace files only:
- ✅ Searching files in current VS Code workspace
- ✅ Finding patterns in brain repository notes
- ✅ Locating local code or documentation
- ❌ NEVER for GitHub remote content

## Complete Conversation Fetching Patterns

### Fetching a Full Issue

**Pattern**: Get issue + get all comments

```
1. mcp_github_issue_read (method: get, issue_number: X)
   → Returns issue details (title, body, state, assignees, labels, etc.)

2. mcp_github_issue_read (method: get_comments, issue_number: X, perPage: 100)
   → Returns all comments with author, timestamp, body
   → Use pagination if > 100 comments (page parameter)
```

**What you get**: Complete issue thread including description and all discussion

### Fetching a Full Pull Request

**Pattern**: Get PR + diff + files + review comments + reviews + general comments

```
1. mcp_github_pull_request_read (method: get, pullNumber: X)
   → Returns PR metadata (title, body, state, base/head, mergeable, etc.)

2. mcp_github_pull_request_read (method: get_diff, pullNumber: X)
   → Returns unified diff of all changes

3. mcp_github_pull_request_read (method: get_files, pullNumber: X, perPage: 100)
   → Returns list of changed files with stats
   → Paginate if many files changed

4. mcp_github_pull_request_read (method: get_review_comments, pullNumber: X, perPage: 100)
   → Returns review threads (line-specific comments grouped by thread)
   → Each thread has metadata: isResolved, isOutdated, isCollapsed
   → Use cursor-based pagination (after parameter) if needed

5. mcp_github_pull_request_read (method: get_reviews, pullNumber: X, perPage: 100)
   → Returns formal reviews (APPROVE, REQUEST_CHANGES, COMMENT)
   → Includes review body and state

6. mcp_github_pull_request_read (method: get_comments, pullNumber: X, perPage: 100)
   → Returns general PR comments (not line-specific)
   → These are issue-style comments on the PR conversation
```

**What you get**: Complete PR context including code changes, all review feedback, and discussion

**Important distinctions**:
- `get_review_comments`: Line-specific code review threads
- `get_reviews`: Formal review submissions (approve/request changes)
- `get_comments`: General conversation comments (not tied to code lines)

### Fetching a Full Discussion

**Pattern**: Get discussion + get all comments with pagination

```
1. mcp_github_get_discussion (owner: X, repo: Y, discussionNumber: Z)
   → Returns discussion details (title, body, category, state)

2. mcp_github_get_discussion_comments (owner: X, repo: Y, discussionNumber: Z, perPage: 100)
   → Returns nested comment threads
   → Use cursor-based pagination (after: endCursor from previous response)
   → Each comment includes replies (nested threads)
```

**What you get**: Complete discussion with all threaded replies

**Pagination note**: Discussions use GraphQL cursor-based pagination. Check `pageInfo.hasNextPage` and use `pageInfo.endCursor` in `after` parameter.

## Common Patterns and Workflows

### Searching for PRs/Issues with Filters

**Date filtering**:
```
mcp_github_search_pull_requests
  query: "author:jonmagic created:2025-11-01..2025-11-30"

mcp_github_search_issues
  query: "involves:jonmagic updated:>=2025-11-01"
```

**State filtering**:
```
# Merged PRs only
query: "is:merged author:jonmagic repo:github/github"

# Open issues assigned to you
query: "is:open assignee:jonmagic"

# Closed issues in date range
query: "is:closed closed:2025-11-01..2025-11-30"
```

**Combining filters**:
```
query: "is:pr is:merged author:jonmagic repo:github/hamzo created:2025-11-01..2025-11-30"
```

### Fetching Multiple Items Efficiently

**Batch pattern** (for small lists):
```
1. Search for items: mcp_github_search_pull_requests
2. For each result (up to 5-10), fetch details in parallel:
   - mcp_github_pull_request_read (method: get, pullNumber: N)
```

**Avoid**: Fetching full details for 50+ items at once. Instead, ask user which specific items to deep-dive.

### Creating PRs with Proper Formatting

```
mcp_github_create_pull_request
  title: "Clear, specific title"
  body: "## Summary\n\n...\n\n## Changes\n\n- Item 1\n- Item 2"
  head: "feature-branch-name"
  base: "main"
  draft: false (or true for work-in-progress)
```

**Body formatting tips**:
- Use Markdown (headings, lists, code blocks)
- Reference issues: `Closes #123` or `Relates to #456`
- Include context for reviewers
- Add testing notes or screenshots if relevant

### Adding Comments vs Reviews

**Issue comment** (general discussion):
```
mcp_github_add_issue_comment
  issue_number: X
  body: "Your comment text"
```

**PR review** (formal approval/changes requested):
```
1. Create pending review:
   mcp_github_pull_request_review_write (method: create)
     body: "Overall feedback"
     event: null (omit to create pending)

2. Submit review:
   mcp_github_pull_request_review_write (method: submit_pending)
     body: "Final summary"
     event: "APPROVE" | "REQUEST_CHANGES" | "COMMENT"
```

## Pagination Best Practices

### REST-based Pagination (page/perPage)

Used by: `list_issues`, `list_pull_requests`, `get_comments`, `get_files`, `get_reviews`

```
perPage: 100 (max)
page: 1, 2, 3, ... (1-based)
```

**Pattern**:
```
1. First call: perPage: 100, page: 1
2. If results.length === 100, likely more pages
3. Next call: perPage: 100, page: 2
4. Repeat until results.length < 100
```

### GraphQL Cursor Pagination (after/endCursor)

Used by: `list_issues` (GraphQL mode), `get_discussion_comments`, `get_review_comments`

```
perPage: 100
after: "cursor-string-from-previous-response"
```

**Pattern**:
```
1. First call: perPage: 100 (no after)
2. Check response.pageInfo.hasNextPage
3. If true, next call: perPage: 100, after: response.pageInfo.endCursor
4. Repeat until hasNextPage === false
```

## Common Mistakes to Avoid

❌ **Using `fetch_webpage` for GitHub issues/PRs**
- Standard web scraping doesn't work for GitHub content
- Always use MCP tools

❌ **Forgetting pagination**
- Default limits are often 30 items
- Set `perPage: 100` to reduce round trips
- Check for more pages before concluding

❌ **Mixing up comment types**
- Issue comments ≠ PR review comments ≠ PR general comments
- Use correct method for each type

❌ **Not filtering by date range**
- Fetching all historical data when you only need recent work
- Use `created:`, `updated:`, `merged:` filters

❌ **Ignoring PR state when searching for completed work**
- Open PRs should go to "Ideas" section in snippets
- Only merged/closed PRs belong in "Ships"
- Use `is:merged` or `is:closed` filters

## Quick Reference: Method Cheat Sheet

### Issues
- Get issue: `issue_read (method: get)`
- Get comments: `issue_read (method: get_comments)`
- Get sub-issues: `issue_read (method: get_sub_issues)`
- Create/update: `issue_write (method: create | update)`
- Search: `search_issues`

### Pull Requests
- Get PR: `pull_request_read (method: get)`
- Get diff: `pull_request_read (method: get_diff)`
- Get files: `pull_request_read (method: get_files)`
- Get review comments: `pull_request_read (method: get_review_comments)`
- Get reviews: `pull_request_read (method: get_reviews)`
- Get general comments: `pull_request_read (method: get_comments)`
- Create PR: `create_pull_request`
- Update PR: `update_pull_request`
- Search: `search_pull_requests`

### Discussions
- Get discussion: `get_discussion`
- Get comments: `get_discussion_comments`
- List: `list_discussions`

### Other
- Search code: `search_code`
- Search repos: `search_repositories`
- Get file: `get_file_contents`
- List branches: `list_branches`
- Get commit: `get_commit`
