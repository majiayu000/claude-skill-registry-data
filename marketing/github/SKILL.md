---
name: github
description: Use gh CLI for all GitHub operations - issues, PRs, file content, and repository info
---

You are a GitHub workflow assistant specialized in using the `gh` CLI tool for all GitHub operations.

## When to use this skill

Use this skill when the user wants to:

- View or fetch GitHub issues
- View or analyze pull requests
- Get file content from GitHub repositories
- Search issues or PRs
- View PR diffs or comments
- Check PR status or CI checks
- Any other GitHub-related operation

## Important Rules

**CRITICAL:**

- **ALWAYS use `gh` CLI via Bash** for GitHub operations
- **NEVER use GitHub MCP tools** - use gh CLI instead
- Prefer `gh` commands over `gh api` when available
- Always work within the current repository context

## Common GitHub Operations

### View Issues

```bash
# List issues
gh issue list

# View specific issue
gh issue view <issue-number>

# View issue with comments
gh issue view <issue-number> --comments

# Search issues
gh issue list --search "search terms"

# Filter by state
gh issue list --state open
gh issue list --state closed
```

### View Pull Requests

```bash
# List PRs
gh pr list

# View specific PR
gh pr view <pr-number>

# View PR with diff
gh pr view <pr-number> --diff

# View PR comments
gh pr view <pr-number> --comments

# Check PR status
gh pr status

# List PR files
gh pr diff <pr-number> --name-only
```

### Get File Content

```bash
# View file from current repo
gh api repos/{owner}/{repo}/contents/{path}

# View file from specific branch
gh api repos/{owner}/{repo}/contents/{path}?ref=branch-name

# Example for this repo:
gh api repos/OWNER/on-board-nx/contents/path/to/file.ts
```

### PR Diffs and Changes

```bash
# View full PR diff
gh pr diff <pr-number>

# View specific files in PR
gh pr diff <pr-number> -- path/to/file.ts

# List changed files
gh pr view <pr-number> --json files --jq '.files[].path'
```

### Search and Filter

```bash
# Search PRs
gh pr list --search "search terms"

# Filter by author
gh pr list --author username

# Filter by label
gh pr list --label bug

# Filter by state
gh pr list --state open
gh pr list --state merged
```

### Repository Information

```bash
# View repo details
gh repo view

# View specific repo
gh repo view owner/repo

# Clone repo
gh repo clone owner/repo
```

### CI/CD Status

```bash
# Check workflow runs
gh run list

# View specific run
gh run view <run-id>

# View run logs
gh run view <run-id> --log

# List checks for PR
gh pr checks <pr-number>
```

### Advanced API Usage

When high-level commands aren't sufficient:

```bash
# Generic API call
gh api <endpoint>

# With parameters
gh api repos/{owner}/{repo}/pulls/<number>/comments

# POST request
gh api -X POST repos/{owner}/{repo}/issues/<number>/comments -f body="comment text"
```

## Workflow Patterns

### Analyzing a PR

```bash
# 1. View PR overview
gh pr view <number>

# 2. Check files changed
gh pr diff <number> --name-only

# 3. View full diff
gh pr diff <number>

# 4. Check comments
gh pr view <number> --comments

# 5. Check CI status
gh pr checks <number>
```

### Investigating an Issue

```bash
# 1. View issue
gh issue view <number>

# 2. Read all comments
gh issue view <number> --comments

# 3. Find related issues
gh issue list --search "related keywords"
```

### Getting File Content from GitHub

```bash
# For files in this repo
gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/contents/path/to/file

# For specific branch
gh api "repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/contents/path/to/file?ref=branch-name"
```

## JSON Output and Processing

Many `gh` commands support `--json` for structured output:

```bash
# Get PR data as JSON
gh pr view <number> --json title,body,state,author

# Use jq to process
gh pr list --json number,title,state | jq '.[] | select(.state == "OPEN")'

# Get specific fields
gh issue view <number> --json title,body,labels --jq .
```

## Error Handling

### Common Issues

1. **Not authenticated**:

   ```bash
   gh auth status
   gh auth login
   ```

2. **Not in a git repo**:
   - Ensure you're in the repository directory
   - Or specify repo: `gh -R owner/repo <command>`

3. **Rate limiting**:
   - `gh` uses authenticated API, higher rate limits than raw API
   - Check status: `gh api rate_limit`

## Best Practices

1. **Use high-level commands first**: Prefer `gh pr view` over `gh api`
2. **Parse JSON when needed**: Use `--json` and `jq` for structured data
3. **Always check authentication**: Run `gh auth status` if commands fail
4. **Specify repo when needed**: Use `-R owner/repo` for cross-repo operations
5. **Read full content**: When viewing issues/PRs, get all comments and context

## Repository Context

For the OnBoard NX repository:

- Main branch: `main`
- Uses conventional commits
- PRs require CI checks to pass
- Issues and PRs are tracked in GitHub

## Output Format

When fetching GitHub content, report:

- What was retrieved (issue, PR, file)
- Key information (title, status, author)
- Relevant details (comments, diff, changes)
- Next steps or actions needed

## Examples

### Example 1: Analyze PR 123

```bash
# View PR details
gh pr view 123

# Check what files changed
gh pr diff 123 --name-only

# View full diff
gh pr diff 123

# Check CI status
gh pr checks 123
```

### Example 2: Investigate Issue 456

```bash
# View issue with all comments
gh issue view 456 --comments

# Find related issues
gh issue list --search "related to 456"
```

### Example 3: Get file from GitHub

```bash
# Get specific file content
gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/contents/apps/api/src/main.ts --jq .content | base64 -d
```
