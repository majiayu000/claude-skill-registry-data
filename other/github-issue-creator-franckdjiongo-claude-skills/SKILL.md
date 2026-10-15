---
name: github-issue-creator
description: Create GitHub issues via API from drafted content. Use when the user provides a drafted issue (title, body, labels, assignees) and wants to create it in a GitHub repository. The user will specify the target repository each time.
---

# GitHub Issue Creator

Create GitHub issues directly from drafted content using the GitHub REST API.

## When to Use This Skill

Use this skill when:
- The user has a fully drafted issue (from another skill or manual drafting)
- They want to create the issue in a GitHub repository
- They will specify the repository name in the format `owner/repo`

## Prerequisites

Before using this skill for the first time, the user must set their GitHub personal access token as an environment variable:

```bash
export GITHUB_TOKEN='ghp_your_token_here'
```

The token needs the `repo` scope to create issues.

## Usage

Call the `create_issue.sh` script with the following parameters:

```bash
scripts/create_issue.sh <repo> <title> <body> [labels] [assignees]
```

### Parameters

1. **repo** (required) - Repository in format `owner/repo` (e.g., `octocat/Hello-World`)
2. **title** (required) - Issue title
3. **body** (required) - Issue body/description (can include markdown)
4. **labels** (optional) - Comma-separated labels (e.g., `bug,urgent`)
5. **assignees** (optional) - Comma-separated GitHub usernames (e.g., `user1,user2`)

### Example Usage

Basic issue:
```bash
scripts/create_issue.sh "myorg/myrepo" "Fix login bug" "Users cannot log in when using SSO"
```

Issue with labels:
```bash
scripts/create_issue.sh "myorg/myrepo" "Feature: Dark mode" "Add dark mode support to the app" "enhancement,ui"
```

Issue with labels and assignees:
```bash
scripts/create_issue.sh "myorg/myrepo" "Critical bug" "Database connection failing" "bug,critical" "john,jane"
```

## Output

On success, the script returns:
- Issue number
- Direct URL to the created issue

On failure, the script returns:
- HTTP error code
- Error message from GitHub API

## Tips

- Always verify the repository name format (`owner/repo`)
- Escape special characters in title and body if needed
- Multi-line bodies should be passed as a single string
- The script requires `jq` and `curl` to be installed (usually pre-installed on most systems)
