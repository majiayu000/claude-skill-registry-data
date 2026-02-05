---
name: Platform Integration (GitHub/GitLab)
description: This skill should be used when the user asks to "fetch GitHub issue", "get GitLab issue", "analyze GitHub PR", "search GitHub repo", "check GitLab commits", "use GitHub API", "use GitLab API", or mentions fetching data from GitHub or GitLab for incident investigation. Provides guidance for integrating with GitHub and GitLab APIs for RCA.
version: 0.1.0
---

# Platform Integration (GitHub/GitLab)

## Overview

GitHub and GitLab are popular code hosting platforms that also track issues, pull requests, and commits. This skill provides guidance for fetching and analyzing data from these platforms during root cause analysis, particularly when production issues are reported via GitHub/GitLab issues.

## When to Use This Skill

Apply this skill when:
- Analyzing GitHub or GitLab issues reporting production problems
- Fetching commit history for affected code
- Using git blame to identify code authors
- Searching repositories for error-related code
- Correlating issues with pull requests or merges
- Tracking who made changes related to incidents

## Platform Similarities and Differences

Both GitHub and GitLab provide similar capabilities:
- Issue tracking
- Pull/Merge request management
- Repository hosting
- Commit history and blame
- Code search
- API access

**Key differences**:
- **GitHub**: Uses "Pull Requests" (PRs)
- **GitLab**: Uses "Merge Requests" (MRs)
- **API endpoints**: Different base URLs and authentication
- **Issue references**: GitHub uses `#123`, GitLab uses `!123` for MRs

This skill covers both platforms; adapt examples to your platform of choice.

## Authentication

### GitHub Personal Access Token

Create token at: https://github.com/settings/tokens

**Required scopes**:
- `repo` - Full repository access (includes issues, commits, code)
- `read:org` - Read organization data (if using org repos)

**Usage in API calls**:
```
Authorization: Bearer ghp_yourtoken
```

### GitLab Personal Access Token

Create token at: https://gitlab.com/-/profile/personal_access_tokens

**Required scopes**:
- `api` - Full API access
- `read_repository` - Read repository data

**Usage in API calls**:
```
Authorization: Bearer glpat_yourtoken
```

**Configure in Thufir settings** (`.claude/thufir.local.md`):
```yaml
github:
  token: "ghp_your_token_here"
  default_repo: "owner/repository"

gitlab:
  token: "glpat_your_token_here"
  default_project: "group/project"
```

## Working with Issues

### Fetching Issue Details

**GitHub API**:
```
GET /repos/{owner}/{repo}/issues/{issue_number}
```

**GitLab API**:
```
GET /projects/{id}/issues/{issue_iid}
```

### Issue Structure

Issues contain:
- **Title**: Brief description
- **Body/Description**: Detailed description, often includes error logs
- **Labels**: Tags like "production", "incident", "bug"
- **State**: open, closed
- **Created/Updated timestamps**
- **Comments**: Discussion and updates
- **Assignees**: Who's working on it

### Extracting RCA Information

From issue body, extract:
- **Error messages**: Search for stack traces, error codes
- **Reproduction steps**: How to trigger the issue
- **Affected features**: Which part of the system broke
- **Time of occurrence**: When users first noticed
- **User impact**: How many users affected

**Example parsing**:
```
Issue body:
"Users are getting 500 errors when trying to log in.
Error: ConnectionPoolExhausted at 2025-12-19 14:32 UTC
Approximately 15,000 users affected."

Extracted:
- Error: ConnectionPoolExhausted
- Time: 2025-12-19 14:32 UTC
- Impact: 15,000 users
- Feature: Login
```

### Filtering Issues

**GitHub - List issues with labels**:
```
GET /repos/{owner}/{repo}/issues?labels=production,incident&state=open
```

**GitLab - List issues with labels**:
```
GET /projects/{id}/issues?labels=production,incident&state=opened
```

## Commit Analysis

### Fetching Recent Commits

**GitHub - List commits**:
```
GET /repos/{owner}/{repo}/commits?since=2025-12-19T00:00:00Z
```

**GitLab - List commits**:
```
GET /projects/{id}/repository/commits?since=2025-12-19T00:00:00Z
```

### Commit Information

Each commit includes:
- **SHA**: Unique identifier
- **Message**: Commit description
- **Author**: Name and email
- **Timestamp**: When committed
- **Files changed**: List of modified files
- **Diff**: Changes made

### Finding Relevant Commits

Filter commits by:
1. **Time range**: Commits before incident start
2. **Files**: Commits touching affected files
3. **Author**: Specific developer
4. **Message content**: Keywords like "fix", "update", "config"

### Using Git Blame

Git blame identifies who last modified each line.

**GitHub - Get blame**:
```
GET /repos/{owner}/{repo}/blame/{ref}/{path}
```

**GitLab - Get blame**:
```
GET /projects/{id}/repository/files/{path}/blame?ref=main
```

**Parse blame output** to find:
- Line number
- Commit SHA
- Author
- Timestamp
- Original code

**Use for RCA**:
- Identify who changed problematic code
- Find when change was introduced
- Trace back to original commit

## Code Search

### Searching for Error Messages

**GitHub - Search code**:
```
GET /search/code?q=ConnectionPoolExhausted+repo:owner/repo
```

**GitLab - Search in project**:
```
GET /projects/{id}/search?scope=blobs&search=ConnectionPoolExhausted
```

### Search Strategies

**Search for error strings**:
- Remove variable parts: `ConnectionPoolExhausted` not `ConnectionPoolExhausted: timeout=5000ms`
- Search exact phrases with quotes: `"Could not acquire connection"`
- Use AND/OR for multiple terms

**Search for code patterns**:
- Function names from stack traces
- Class names
- Configuration keys
- API endpoint paths

**Example RCA search workflow**:
1. Extract error from issue: `ConnectionPoolExhausted`
2. Search code for error string
3. Find where error is raised
4. Use blame to identify recent changes
5. Review commits for root cause

## Pull/Merge Request Analysis

### Fetching PR/MR Details

**GitHub - Get pull request**:
```
GET /repos/{owner}/{repo}/pulls/{pr_number}
```

**GitLab - Get merge request**:
```
GET /projects/{id}/merge_requests/{mr_iid}
```

### PR/MR Information

Includes:
- **Title and description**
- **Author**
- **Created/merged timestamps**
- **Files changed**
- **Diff**: Code changes
- **Commits**: List of commits in the PR/MR
- **Status**: open, merged, closed

### Correlating Issues with PRs/MRs

**Link issues to PRs**:
- PR descriptions often reference issues: "Fixes #123"
- GitHub automatically links PRs that fix issues
- Check if incident-related issue has linked PRs

**Identify problematic merge**:
- Find PRs merged around incident time
- Check PRs that modified affected files
- Review PRs from specific authors

## Integration with Thufir MCP

Thufir provides MCP servers for GitHub and GitLab:

### GitHub MCP Tools

**get_issue**:
- Fetch issue by number
- Returns title, body, labels, timestamps

**list_commits**:
- List commits in time range
- Filter by path, author

**get_blame**:
- Get blame for specific file
- Identify line authors

**search_code**:
- Search repository for code patterns
- Find error strings in codebase

### GitLab MCP Tools

**get_issue**:
- Fetch issue by IID
- Returns description, labels, timestamps

**list_commits**:
- List commits with filters
- Since/until time range

**get_blame**:
- Get blame for file path
- Identify code authors

**search_code**:
- Search project blobs
- Find error patterns

### Using MCP for RCA

**Workflow example**:

1. **Fetch issue details**:
```
Use MCP: github_get_issue
Parameters: issue_number=456
Result: Issue describes login failures at 14:32 UTC
```

2. **Extract error and search code**:
```
Use MCP: github_search_code
Parameters: query="ConnectionPoolExhausted"
Result: Found in src/config/database.js
```

3. **Get blame for suspicious file**:
```
Use MCP: github_get_blame
Parameters: path="src/config/database.js"
Result: Line 45 changed by Developer X in commit abc123
```

4. **List recent commits**:
```
Use MCP: github_list_commits
Parameters: since="2025-12-19T00:00:00Z", path="src/config/database.js"
Result: Commit abc123 at 10:15 UTC changed pool size
```

## Best Practices

### Issue Analysis

- Read full issue body, not just title
- Check comments for additional context
- Look for error logs in code blocks
- Note timestamps in issue description
- Check for related/duplicate issues

### Commit Investigation

- Focus on commits in time window before incident
- Prioritize commits to affected files
- Read commit messages for clues
- Review full diffs, not just summaries
- Check for configuration changes

### Code Search

- Start with exact error strings
- Broaden search if no results
- Use repo/project scoping
- Search in relevant file paths
- Check multiple branches if needed

### Blame Usage

- Blame specific suspicious lines
- Don't blame entire files (too much data)
- Cross-reference with commit history
- Correlate blame timestamps with incident timeline
- Use blame to find commit, then review commit details

## Common Patterns

### Pattern 1: Issue Reports Production Error

1. Fetch issue via MCP
2. Extract error message from body
3. Search code for error string
4. Use blame on file containing error
5. Review recent commits to that file
6. Identify root cause commit

### Pattern 2: Deployment Caused Issue

1. List commits merged around deployment time
2. Review PRs merged just before deployment
3. Check files changed in those PRs
4. Correlate changed files with error location
5. Identify problematic PR/commit

### Pattern 3: Configuration Change

1. Search for config files in recent commits
2. Use `git diff` to see what changed
3. Identify configuration value changes
4. Correlate config change with incident symptoms
5. Validate hypothesis with evidence

## Integration with Other Skills

This skill works with:
- **root-cause-analysis skill**: Provides evidence from GitHub/GitLab
- **git-investigation skill**: Deep git analysis using local repository
- **prometheus-analysis skill**: Correlate issue timestamps with metrics
- **RCA agent**: Agent orchestrates API calls to gather issue data

## Additional Resources

### Reference Files

For detailed API patterns and examples:
- **`references/api-examples.md`** - Complete API call examples for common scenarios

## Quick Reference

**GitHub**:
- Base URL: `https://api.github.com`
- Auth: `Authorization: Bearer ghp_token`
- Issues: `/repos/{owner}/{repo}/issues/{number}`
- Commits: `/repos/{owner}/{repo}/commits`
- Blame: `/repos/{owner}/{repo}/blame/{ref}/{path}`
- Search: `/search/code?q=query+repo:owner/repo`

**GitLab**:
- Base URL: `https://gitlab.com/api/v4`
- Auth: `Authorization: Bearer glpat_token`
- Issues: `/projects/{id}/issues/{iid}`
- Commits: `/projects/{id}/repository/commits`
- Blame: `/projects/{id}/repository/files/{path}/blame`
- Search: `/projects/{id}/search?scope=blobs&search=query`

**Workflow**: Issue → Error → Search → Blame → Commits → Root Cause

---

Use GitHub and GitLab APIs to gather comprehensive incident context, correlate issues with code changes, and identify specific commits that introduced problems.
