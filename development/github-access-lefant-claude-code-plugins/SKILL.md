---
name: github-access
description: Access GitHub repositories programmatically using gh CLI or REST API. Use this skill when needing to interact with GitHub issues, pull requests, workflows, discussions, or actions. The skill automatically adapts based on available tools (gh CLI or curl) and requires GH_TOKEN for authentication.
---

# GitHub Access

## Overview

This skill enables programmatic access to GitHub repositories through either the `gh` CLI tool or the REST API with `curl`. Use this skill to interact with GitHub issues, pull requests, workflows, discussions, and GitHub Actions. The skill provides comprehensive commands and patterns for common GitHub operations.

## Prerequisites and Tool Selection

Before performing any GitHub operations, follow this workflow:

### 1. Check for GH_TOKEN

**CRITICAL**: Always verify that the `GH_TOKEN` environment variable is set before attempting any GitHub operations:

```bash
echo $GH_TOKEN
```

**If `GH_TOKEN` is not set:**
- Abort the operation immediately
- Inform the user that a GitHub token is required
- Instruct them to set `GH_TOKEN` with a valid GitHub personal access token

**Example message:**
```
GitHub operations require authentication. Please set the GH_TOKEN environment variable with a valid GitHub personal access token:

export GH_TOKEN="your_token_here"

You can create a token at: https://github.com/settings/tokens
```

### 2. Check for gh CLI Availability

If `GH_TOKEN` is set, check if the `gh` CLI tool is available:

```bash
which gh
```

### 3. Load the Appropriate Reference

Based on availability, load the corresponding reference document:

- **If `gh` is available**: Read and use `references/gh-commands.md` for command examples
- **If `gh` is NOT available**: Read and use `references/curl-api.md` for REST API calls with curl

The `references/mcp-tools.md` file provides a comprehensive list of all available GitHub MCP tools and their parameters for reference.

## Key Operations

These are the most commonly used GitHub operations. Detailed commands for both `gh` and `curl` are provided in the reference documents.

### 1. Read Issue Content

**Use case**: Get the full details of a GitHub issue including title, body, state, labels, and metadata.

**When to use**: When the user provides an issue number or URL, or when following up on search results.

**With gh:**
```bash
gh issue view ISSUE_NUMBER --repo OWNER/REPO
gh issue view ISSUE_NUMBER --json title,body,state,labels --repo OWNER/REPO
```

**With curl:**
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER
```

### 2. Read Pull Request Comments

**Use case**: Retrieve comments and reviews on a pull request. GitHub has several types of PR comments:
- **Regular comments**: General discussion comments on the PR (use `/issues/` endpoint)
- **Review summaries**: Top-level review with overall feedback (use `/reviews` endpoint)
- **Inline review comments**: Code-specific comments on file changes (use `/pulls/.../comments` endpoint)

**When to use**: When reviewing feedback on a PR, understanding discussion context, or analyzing review comments.

**With gh:**
```bash
# Get all comments and reviews
gh pr view PR_NUMBER --comments --repo OWNER/REPO

# Get as structured JSON
gh pr view PR_NUMBER --json comments,reviews --repo OWNER/REPO
```

**With curl:**
```bash
# Get all PR reviews (summary level with overall feedback)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/reviews

# Get all inline review comments (code-specific comments on file changes)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/comments

# Get regular PR comments (general discussion, not inline code comments)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/PR_NUMBER/comments

# Get comments from a specific review (rarely needed - usually use /pulls/.../comments instead)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/reviews/REVIEW_ID/comments
```

### 3. Check Workflow Status and Fetch Failure Logs

**Use case**: Diagnose CI/CD failures by checking workflow run status and retrieving logs from failed jobs.

**When to use**: When a PR has failing checks, when investigating build failures, or when debugging CI/CD issues.

**With gh:**
```bash
# 1. Check PR status
gh pr checks PR_NUMBER --repo OWNER/REPO

# 2. Get the most recent workflow run for the PR
RUN_ID=$(gh pr view PR_NUMBER --json headRefName --jq -r '.headRefName' | \
  xargs -I {} gh run list --branch {} --limit 1 --json databaseId --jq '.[0].databaseId' --repo OWNER/REPO)

# 3. View failed job logs
gh run view $RUN_ID --log-failed --repo OWNER/REPO
```

**With curl:**
```bash
# 1. Get PR details to find HEAD SHA
PR_DATA=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER)

HEAD_SHA=$(echo "$PR_DATA" | jq -r '.head.sha')

# 2. Get check runs for that SHA
curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/$HEAD_SHA/check-runs

# 3. Get failed workflow runs
RUNS=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs?head_sha=$HEAD_SHA")

FAILED_RUN_ID=$(echo "$RUNS" | jq -r '.workflow_runs[] | select(.conclusion == "failure") | .id' | head -1)

# 4. Get failed jobs
curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/$FAILED_RUN_ID/jobs?filter=failed"

# 5. Get logs for specific job
JOB_ID=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/$FAILED_RUN_ID/jobs?filter=failed" | jq -r '.jobs[0].id')

curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/actions/jobs/$JOB_ID/logs
```

### 4. Search Issues

**Use case**: Find issues when the user doesn't provide a specific issue number or URL.

**When to use**: When the user mentions an issue by description, keyword, or topic rather than by number.

**With gh:**
```bash
# Search in specific repository
gh issue list --search "QUERY" --repo OWNER/REPO

# Search with filters
gh issue list --state open --label bug --repo OWNER/REPO

# Search across organization
gh search issues "QUERY" --owner OWNER
```

**With curl:**
```bash
# Search issues in repository
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=QUERY+repo:OWNER/REPO+type:issue"

# Search with filters (e.g., open bugs)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=is:open+label:bug+repo:OWNER/REPO+type:issue"
```

### 5. Search Pull Requests

**Use case**: Find pull requests when the user doesn't provide a specific PR number or URL.

**When to use**: When the user references a PR by description, author, branch name, or topic rather than by number.

**With gh:**
```bash
# Search in specific repository
gh pr list --search "QUERY" --repo OWNER/REPO

# Search with filters
gh pr list --state open --author USERNAME --repo OWNER/REPO

# Search across organization
gh search prs "QUERY" --owner OWNER
```

**With curl:**
```bash
# Search PRs in repository
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=QUERY+repo:OWNER/REPO+type:pr"

# Search with filters (e.g., open PRs by author)
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/search/issues?q=is:open+author:USERNAME+repo:OWNER/REPO+type:pr"
```

## Extracting Repository Information

When the user provides a GitHub URL, extract the owner and repository name:

**Example URL formats:**
- `https://github.com/owner/repo/issues/123`
- `https://github.com/owner/repo/pull/456`
- `https://github.com/owner/repo`

**Extraction with sed:**
```bash
URL="https://github.com/owner/repo/issues/123"
OWNER_REPO=$(echo "$URL" | sed -E 's|https://github.com/([^/]+/[^/]+)/.*|\1|')
OWNER=$(echo "$OWNER_REPO" | cut -d'/' -f1)
REPO=$(echo "$OWNER_REPO" | cut -d'/' -f2)
```

## Resources

This skill includes three reference documents with comprehensive command examples:

### references/mcp-tools.md
Complete list of all available GitHub MCP tools and their parameters. Use this as a reference for understanding available functionality and parameter requirements.

### references/gh-commands.md
Comprehensive `gh` CLI commands for all GitHub operations. Load this document when `gh` is available. Includes:
- Actions and workflow operations
- Issue management
- Pull request operations
- Discussions (via GraphQL)
- Common patterns and tips

**Official documentation**: https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28&tool=cli

### references/curl-api.md
REST API calls using `curl` for environments without `gh` CLI. Load this document when `gh` is not available. Includes:
- Complete REST API endpoints
- Request headers and authentication
- Response parsing with `jq`
- GraphQL queries for discussions
- Pagination and rate limiting

**Official documentation**: https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28&tool=curl

## Additional Operations

Beyond the key operations listed above, the reference documents provide detailed commands for:

- **Workflows**: Trigger, list, rerun, cancel, download artifacts
- **Issues**: Create, update, comment, label, assign, close
- **Pull Requests**: Create, update, merge, review, request reviewers, get diff
- **Discussions**: List, view, comment (via GraphQL)
- **Labels**: Get, create, update, delete
- **Repository operations**: Various repository-level operations

Consult the appropriate reference document (`gh-commands.md` or `curl-api.md`) for complete examples.
