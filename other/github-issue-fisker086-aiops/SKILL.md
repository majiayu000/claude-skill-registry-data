---
name: github-issue
description: Query GitHub issues, PRs, and repository info
activation_keywords: [github, issue, pr, pull request, repository, commit, branch]
execution_mode: server
---

# GitHub Issue Skill

Provides read-only GitHub operations:
- List repository issues
- Get issue details and comments
- List pull requests
- Get repository info

Use `builtin_github_issue` tool with fields:
- `operation`: one of "issues", "issue", "prs", "repo"
- `repo`: Repository in owner/repo format
- `issue_number`: Issue/PR number
- `state`: Filter by state (open, closed, all)

Note: Requires GitHub token for authenticated requests.
