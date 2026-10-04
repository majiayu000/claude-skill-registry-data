---
name: github-cli
description: This skill should be used when working with GitHub CLI (gh) for repository management, pull requests, issues, API access, GitHub Actions, or automation workflows. Provides comprehensive guidance on gh command patterns, security considerations, and best practices.
allowed-tools: Read, Grep, Glob, Bash(gh:*), WebSearch, WebFetch
---

# GitHub CLI (gh) Usage Skill

## Purpose

GitHub CLI (`gh`) is the official command-line interface to GitHub, enabling direct interaction with repositories, pull
requests, issues, GitHub Actions, and the GitHub API without leaving the terminal. This skill provides systematic
guidance for using gh effectively while maintaining security through the integrated write-guard protection.

## When to Use This Skill

Invoke this skill when:

- Creating or managing pull requests and issues via command line
- Querying GitHub API (REST or GraphQL) for repository data
- Automating GitHub workflows and Actions
- Managing releases, gists, projects, or codespaces
- Scripting GitHub operations for CI/CD pipelines
- User explicitly mentions "gh", "github cli", or requests GitHub interactions

## Core Concepts

### Authentication First

Before any gh operations, verify authentication status:

```bash
gh auth status              # Check current authentication
gh auth login               # Interactive authentication setup
gh auth refresh             # Refresh expired tokens
```

Authentication automatically stores Git credentials when HTTPS is selected as the preferred protocol.

### gh vs git Distinction

- **`git`**: Version control operations (commit, push, pull) - works with any remote service
- **`gh`**: GitHub-specific operations (PRs, issues, API, Actions) - GitHub only

Use `gh` for GitHub platform interactions; use `git` for repository version control.

## Quick Command Reference

### Common Operations

**Repositories:**
```bash
gh repo view OWNER/REPO     # View repository details
gh repo clone OWNER/REPO    # Clone repository
gh repo list OWNER          # List repositories
```

**Pull Requests:**
```bash
gh pr list                  # List pull requests
gh pr view 123              # View PR details
gh pr checkout 123          # Checkout PR branch
gh pr create --draft        # Create draft PR (⚠️ write operation)
```

**Issues:**
```bash
gh issue list               # List issues
gh issue view 456           # View issue details
gh issue create             # Create issue (⚠️ write operation)
```

**GitHub API:**
```bash
gh api repos/{owner}/{repo}                    # GET request (read-only)
gh api -X GET /endpoint -f param=value         # GET with parameters
gh api --paginate /endpoint                    # Paginated requests
gh api repos/{owner}/{repo} --jq '.stars'      # JSON filtering with jq
```

**Search:**
```bash
gh search prs --review-requested=@me           # Search PRs
gh search issues "is:open label:bug"           # Search issues
gh search code "function name"                 # Search code
```

**For detailed commands, patterns, and examples, see:**

- `references/gh-commands.md` - Complete command catalog by category
- `references/gh-api-patterns.md` - REST/GraphQL API examples and authentication
- `references/gh-scripting.md` - Automation patterns, output formatting, and best practices

## Security Considerations

### Write Protection

This plugin includes a **security guard** that blocks write operations by default:

**Blocked operations:**

- Repository modifications: `gh repo create`, `gh repo delete`, `gh repo archive`
- PR/Issue changes: `gh pr create`, `gh pr merge`, `gh issue close`, `gh issue edit`
- Release management: `gh release create`, `gh release delete`
- API write methods: `gh api -X POST`, `gh api -X PUT`, `gh api -X PATCH`, `gh api -X DELETE`
- Workflow triggers: `gh workflow run`, `gh run cancel`

**Allowed operations:**

- All read commands: `gh repo view`, `gh pr list`, `gh issue list`
- API GET requests: `gh api repos/{owner}/{repo}`
- Search operations: `gh search prs`, `gh search issues`

### Authorization Workflow

When write operations are needed:

1. **Ask user for explicit permission first**
2. User authorizes the specific write operation
3. Perform authorized write operations only after confirmation

### API Method Security

```bash
# ❌ Blocked - Write methods
gh api -X POST /repos/{owner}/{repo}/issues
gh api -X PUT /repos/{owner}/{repo}
gh api -X DELETE /repos/{owner}/{repo}/issues/123

# ❌ Blocked - Implicit POST via field parameters
gh api /repos/{owner}/{repo}/issues -f title="Bug"

# ✅ Allowed - Explicit GET with parameters
gh api -X GET /repos/{owner}/{repo}/issues -f state=open -f labels=bug
```

**Note:** Field parameters (`-f`, `-F`, `--field`) trigger implicit POST unless `-X GET` is explicitly specified.

## Configuration

The security guard can be configured in `~/.claude/settings.json`:

```json
{
  "githubWriteGuard": {
    "enabled": true
  }
}
```

**Note**: The guard is enabled by default. Set `enabled: false` to disable write protection.

### Available Commands

- `/gh-cli-status` - View current guard status

## Environment Variables

```bash
export GH_REPO="owner/repo"              # Override repository context
export GH_HOST="github.example.com"      # Use specific GitHub instance
export GITHUB_TOKEN="ghp_..."            # Set API token (not recommended)
export PAGER="less -FX"                  # Configure pager
```

## Troubleshooting

**Authentication:**
```bash
gh auth status          # Check authentication state
gh auth refresh         # Refresh expired token
gh auth login           # Re-authenticate
```

**API Rate Limits:**
```bash
gh api rate_limit                               # Check rate limit
gh api --cache 1h repos/{owner}/{repo}/releases # Use caching
```

**Debug Mode:**
```bash
gh pr create --title "Test" --verbose           # Verbose output
GH_DEBUG=api gh api repos/{owner}/{repo}        # See HTTP requests
```

## References

**Detailed documentation:**

- `references/gh-commands.md` - Complete command catalog by category
- `references/gh-api-patterns.md` - REST/GraphQL examples and authentication
- `references/gh-scripting.md` - Automation patterns and best practices

**Official resources:**
- GitHub CLI Manual: https://cli.github.com/manual/
- GitHub Docs: https://docs.github.com/en/github-cli
- Repository: https://github.com/cli/cli
- Scripting Guide: https://github.blog/engineering/engineering-principles/scripting-with-github-cli/
