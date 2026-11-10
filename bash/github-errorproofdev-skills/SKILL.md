---
name: github
description: Create and manage GitHub issues, pull requests, workflows, and repositories using the gh CLI. Use when asked to open a PR, merge a pull request, check repo actions, list issues, create a branch, or manage GitHub projects.
metadata:
  author: odyssey4me
  version: "0.2.2"
  category: code-hosting
  tags: "issues, pull-requests, workflows"
  complexity: lightweight
license: MIT
---

# GitHub Skill

This skill provides GitHub integration using the official `gh` CLI tool. A Python wrapper script produces markdown-formatted output for read/view operations. Action commands (create, merge, close, comment) should use `gh` directly.

## Network access

GitHub commands (`gh` and the Python wrapper) require outbound HTTPS to GitHub API and authentication endpoints, or the configured GitHub Enterprise host. Git fetch/push requires HTTPS or SSH to the repository host. Remote operations require outbound network access. If the agent environment restricts it, obtain access through that environment's approval or network controls before the first remote command, reusing authorization already granted. Local help and file processing do not need network access. Skill instructions do not grant network permission. Report DNS, connection, and timeout failures as network errors; do not reset credentials to resolve them. If approved access also fails, stop and report it. Authentication and permission errors require user action.

## Resolving script paths

`SKILL_DIR` in the examples is the directory containing this loaded `SKILL.md`.
Set it to that absolute path before running commands; do not assume the agent
sets this shell variable. Quote the script path if it contains spaces.

## Prerequisites

**Install gh CLI**: [installation guide](https://cli.github.com/manual/installation)

## Authentication

```bash
# Authenticate with GitHub
gh auth login

# Verify authentication
gh auth status
```

See [GitHub CLI Authentication](https://cli.github.com/manual/gh_auth_login) for details.

## Script Usage

The wrapper script (`scripts/github.py`) formats output as markdown. Use it for read/view operations to get agent-consumable output. Use `gh` directly for action commands (create, merge, close, comment). See [permissions.md](references/permissions.md) for read/write classification of each command.

```bash
# Check gh CLI is installed and authenticated
$SKILL_DIR/scripts/github.py check

# Issues
$SKILL_DIR/scripts/github.py issues list --repo OWNER/REPO
$SKILL_DIR/scripts/github.py issues view 123 --repo OWNER/REPO

# Pull Requests
$SKILL_DIR/scripts/github.py prs list --repo OWNER/REPO
$SKILL_DIR/scripts/github.py prs view 456 --repo OWNER/REPO
$SKILL_DIR/scripts/github.py prs checks 456 --repo OWNER/REPO
$SKILL_DIR/scripts/github.py prs status --repo OWNER/REPO

# Workflow Runs
$SKILL_DIR/scripts/github.py runs list --repo OWNER/REPO
$SKILL_DIR/scripts/github.py runs view 12345 --repo OWNER/REPO

# Repositories
$SKILL_DIR/scripts/github.py repos list
$SKILL_DIR/scripts/github.py repos view OWNER/REPO

# Search
$SKILL_DIR/scripts/github.py search repos "machine learning"
$SKILL_DIR/scripts/github.py search issues "label:bug is:open"
$SKILL_DIR/scripts/github.py search prs "is:open review:required"
```

All commands support `--limit N` for list commands (default 30).

## Commands (Direct gh Usage)

For action commands, use `gh` directly:

### Issues

```bash
gh issue list                    # List issues
gh issue view 123                # View issue details
gh issue create                  # Create new issue
gh issue comment 123             # Add comment
gh issue close 123               # Close issue
gh issue edit 123 --add-label bug  # Edit issue
```

Full reference: [gh issue](https://cli.github.com/manual/gh_issue)

### Pull Requests

```bash
gh pr list                       # List PRs
gh pr view 456                   # View PR details
gh pr create                     # Create new PR
gh pr review 456 --approve       # Approve PR
gh pr merge 456 --squash         # Merge PR
gh pr checkout 456               # Checkout PR branch
gh pr diff 456                   # View PR diff
gh pr checks 456                 # View CI status
```

Full reference: [gh pr](https://cli.github.com/manual/gh_pr)

### Workflows & Actions

```bash
gh workflow list                 # List workflows
gh workflow run "CI"             # Trigger workflow
gh run list                      # List workflow runs
gh run view 123456               # View run details
gh run watch 123456              # Watch run progress
gh run download 123456           # Download artifacts
gh run rerun 123456 --failed     # Rerun failed jobs
```

Full references:
- [gh workflow](https://cli.github.com/manual/gh_workflow)
- [gh run](https://cli.github.com/manual/gh_run)

### Repositories

```bash
gh repo list                     # List repositories
gh repo view OWNER/REPO          # View repository
gh repo create                   # Create repository
gh repo clone OWNER/REPO         # Clone repository
gh repo fork OWNER/REPO          # Fork repository
```

Full reference: [gh repo](https://cli.github.com/manual/gh_repo)

### Search

```bash
gh search repos "machine learning"   # Search repositories
gh search issues "is:open label:bug" # Search issues
gh search prs "is:open"              # Search pull requests
gh search code "function auth"       # Search code
```

Full reference: [gh search](https://cli.github.com/manual/gh_search)

## Examples

### Daily PR Review

```bash
# Show PRs needing your attention
$SKILL_DIR/scripts/github.py prs status

# Review a specific PR
$SKILL_DIR/scripts/github.py prs view 456
$SKILL_DIR/scripts/github.py prs checks 456
gh pr diff 456
gh pr review 456 --approve

# Verify approval was recorded
$SKILL_DIR/scripts/github.py prs view 456  # check review status
```

### Create Issue and Link PR

```bash
# Create issue
gh issue create --title "Bug: Login fails" --body "Description" --label bug
# Verify: note the issue number from output

# Create PR that fixes it (use issue number from above)
gh pr create --title "Fix login bug (#123)" --body "Fixes #123"
# Verify PR was created and linked
$SKILL_DIR/scripts/github.py prs view <number>
```

### Monitor CI Pipeline

```bash
# Watch latest workflow run
gh run watch $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')

# Check failed runs
gh run list --status failure

# Rerun failed jobs
gh run rerun RUNID --failed
# Verify rerun started
$SKILL_DIR/scripts/github.py runs view RUNID
```

See [common-workflows.md](references/common-workflows.md) for more examples.

## Advanced Usage

### JSON Output for Scripting

```bash
# Get specific fields
gh issue list --json number,title,author

# Process with jq
gh pr list --json number,title | jq '.[] | "\(.number): \(.title)"'

# Export to CSV
gh issue list --json number,title,author | jq -r '.[] | @csv'
```

### GitHub API Access

For operations not covered by gh commands:

```bash
# Make authenticated API request
gh api repos/OWNER/REPO/issues

# POST request
gh api repos/OWNER/REPO/issues -X POST -f title="Issue" -f body="Text"

# Process response
gh api repos/OWNER/REPO | jq '.stargazers_count'
```

Full reference: [gh api](https://cli.github.com/manual/gh_api)

### Aliases for Frequent Operations

```bash
# Create shortcuts
gh alias set prs 'pr list --author @me'
gh alias set issues 'issue list --assignee @me'
gh alias set review 'pr list --search "review-requested:@me"'

# Use them
gh prs
gh issues
gh review
```

## Configuration

```bash
# View configuration
gh config list

# Set default editor
gh config set editor vim

# Set git protocol
gh config set git_protocol ssh
```

Configuration stored in `~/.config/gh/config.yml`

## Model Guidance

This skill wraps an official CLI. A fast, lightweight model is sufficient.

## Troubleshooting

```bash
# Check authentication
gh auth status

# Re-authenticate
gh auth login

# Enable debug logging
GH_DEBUG=1 gh issue list

# Check gh version
gh --version
```

## Official Documentation

- **GitHub CLI Manual**: <https://cli.github.com/manual/>
- **GitHub CLI Repository**: <https://github.com/cli/cli>
- **GitHub API Documentation**: <https://docs.github.com/en/rest>
- **GitHub Actions**: <https://docs.github.com/en/actions>

## Summary

The GitHub skill uses the official `gh` CLI with a Python wrapper for markdown-formatted output on read/view commands.

**Quick start:**
1. Install: `brew install gh` (or equivalent for your OS)
2. Authenticate: `gh auth login`
3. Verify: `$SKILL_DIR/scripts/github.py check`
4. Read: `$SKILL_DIR/scripts/github.py issues list --repo OWNER/REPO`
5. Write: `gh issue create`, `gh pr create`, etc. (use `gh` directly)

For detailed command reference, use `gh <command> --help` or visit <https://cli.github.com/manual/>.
