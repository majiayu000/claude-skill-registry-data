---
name: github-cli-helper
description: Execute GitHub CLI commands using the correct Homebrew path. Use when interacting with GitHub PRs, issues, repos, or any gh command.
---

# GitHub CLI Helper

## Instructions

Always use the full Homebrew path when executing GitHub CLI commands to ensure reliability across different shell environments.

**IMPORTANT:** Use `/opt/homebrew/bin/gh` instead of just `gh` for all GitHub CLI operations.

## Common Operations

### Pull Requests

```bash
# Create a pull request
/opt/homebrew/bin/gh pr create --base main --title "Title" --body "Description"

# List pull requests
/opt/homebrew/bin/gh pr list

# View PR details
/opt/homebrew/bin/gh pr view <number>

# Check PR status
/opt/homebrew/bin/gh pr status

# Merge a pull request
/opt/homebrew/bin/gh pr merge <number>

# Close a pull request
/opt/homebrew/bin/gh pr close <number>

# Review a pull request
/opt/homebrew/bin/gh pr review <number>
```

### Issues

```bash
# Create an issue
/opt/homebrew/bin/gh issue create --title "Title" --body "Description"

# List issues
/opt/homebrew/bin/gh issue list

# View issue details
/opt/homebrew/bin/gh issue view <number>

# Close an issue
/opt/homebrew/bin/gh issue close <number>
```

### Repository Operations

```bash
# Clone a repository
/opt/homebrew/bin/gh repo clone <owner>/<repo>

# View repository details
/opt/homebrew/bin/gh repo view

# Create a repository
/opt/homebrew/bin/gh repo create <name>

# Fork a repository
/opt/homebrew/bin/gh repo fork
```

### Workflow & Actions

```bash
# List workflow runs
/opt/homebrew/bin/gh run list

# View workflow run details
/opt/homebrew/bin/gh run view <run-id>

# Re-run a workflow
/opt/homebrew/bin/gh run rerun <run-id>
```

### Authentication & Configuration

```bash
# Check authentication status
/opt/homebrew/bin/gh auth status

# Login to GitHub
/opt/homebrew/bin/gh auth login

# Set default repository
/opt/homebrew/bin/gh repo set-default
```

## Best Practices

1. **Always use full path**: `/opt/homebrew/bin/gh` not `gh`
2. **Check authentication first**: Run `/opt/homebrew/bin/gh auth status` before operations
3. **Use heredocs for multi-line content**: When creating PRs or issues with complex bodies
4. **Leverage JSON output**: Use `--json` flag for programmatic processing
5. **Handle errors gracefully**: Check exit codes and provide helpful error messages

## Examples

### Create PR with detailed body

```bash
/opt/homebrew/bin/gh pr create \
  --base main \
  --title "feat: add new feature" \
  --body "$(cat <<'EOF'
## Description
Detailed description here

## Changes
- Change 1
- Change 2
EOF
)"
```

### List PRs in JSON format

```bash
/opt/homebrew/bin/gh pr list --json number,title,state,author
```

### Create issue with labels

```bash
/opt/homebrew/bin/gh issue create \
  --title "Bug: Something is broken" \
  --body "Description of the bug" \
  --label bug,priority-high
```

### Comment on a PR

```bash
/opt/homebrew/bin/gh pr comment 123 --body "Thanks for the contribution!"
```

## Troubleshooting

### Command not found

If `/opt/homebrew/bin/gh` doesn't exist, check alternative locations:

- `/usr/local/bin/gh` (Intel Macs)
- Use `which gh` to find the actual location

### Authentication errors

Run `/opt/homebrew/bin/gh auth login` and ensure `repo` scope is granted.

### Enterprise GitHub

Set the `GH_HOST` environment variable:

```bash
export GH_HOST=github.company.com
/opt/homebrew/bin/gh pr list
```

## Tips

- Use `--help` flag to see all available options for any command
- Combine with `jq` for advanced JSON processing
- Use `--web` flag to open resources in browser
- Set aliases in shell config for frequently used commands
