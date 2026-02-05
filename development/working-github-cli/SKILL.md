---
name: working-github-cli
description: Use when working with GitHub repositories, pull requests, issues, releases, or other GitHub operations via the gh CLI
---

# Working with GitHub CLI

Use the `gh` CLI tool via the Bash tool for all GitHub operations.

## Authentication & Account Issues

**IMPORTANT**: If you encounter "repository not found" or authentication errors:

1. Check authentication status:
   ```bash
   gh auth status
   ```

2. If multiple accounts are configured, try switching accounts:
   ```bash
   gh auth switch
   ```

3. If not authenticated, prompt user to run:
   ```bash
   gh auth login
   ```

## Commands & Usage

See @common-commands.md for detailed command reference, examples, and common operations.

## Best Practices

- Use `gh` commands instead of git+web workflows when possible
- Always check `gh <command> --help` for options
- Use `--json` flag for machine-readable output when parsing
- Use heredoc for multiline bodies (PR descriptions, issue bodies)
