---
name: github-info
description: 'Retrieve GitHub user profile and repository information using the gh CLI tool. Use when the user asks about their GitHub profile, statistics, repositories, or wants to view their GitHub information. Examples: Show me my GitHub profile, What are my top repositories, Get my GitHub stats.'
---

# GitHub Info

## Overview

Retrieve comprehensive GitHub information using the GitHub CLI (`gh`) tool. This skill provides scripts and commands to fetch user profile data, repository statistics, and other GitHub-related information.

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- Run `gh auth login` if not already authenticated

## Quick Start

### Get Profile Information

Use the `gh_profile.sh` script to retrieve your GitHub profile:

```bash
bash scripts/gh_profile.sh
```

This displays:
- Username, name, and bio
- Company and location
- Email and blog
- Follower/following counts
- Public repository and gist counts
- Account creation and update dates

### Get Repository Information

Use the `gh_repos.sh` script to list your repositories:

```bash
# Get top 10 repositories (default)
bash scripts/gh_repos.sh

# Get top 20 repositories
bash scripts/gh_repos.sh --limit 20

# Sort by creation date
bash scripts/gh_repos.sh --sort created
```

This displays for each repository:
- Repository name and description
- Primary language
- Star and fork counts
- Private/public status
- Last update date

## Direct gh CLI Usage

For queries not covered by the scripts, use `gh` directly:

```bash
# Get specific user information
gh api user --jq '.login, .name, .bio'

# List repositories with custom fields
gh repo list --json name,stargazerCount --jq '.[] | "\(.name): \(.stargazerCount) stars"'

# Get total stars across all repos
gh api user/repos --paginate --jq '[.[] | .stargazers_count] | add'
```

## Complete `gh` CLI Documentation

Work seamlessly with GitHub from the command line.

USAGE: `gh <command> <subcommand> [flags]`

CORE COMMANDS
  auth:          Authenticate gh and git with GitHub
  browse:        Open repositories, issues, pull requests, and more in the browser
  codespace:     Connect to and manage codespaces
  gist:          Manage gists
  issue:         Manage issues
  org:           Manage organizations
  pr:            Manage pull requests
  project:       Work with GitHub Projects.
  release:       Manage releases
  repo:          Manage repositories

GITHUB ACTIONS COMMANDS
  cache:         Manage GitHub Actions caches
  run:           View details about workflow runs
  workflow:      View details about GitHub Actions workflows

EXTENSION COMMANDS
  copilot:       Extension copilot

ALIAS COMMANDS
  co:            Alias for "pr checkout"

ADDITIONAL COMMANDS
  alias:         Create command shortcuts
  api:           Make an authenticated GitHub API request
  attestation:   Work with artifact attestations
  completion:    Generate shell completion scripts
  config:        Manage configuration for gh
  extension:     Manage gh extensions
  gpg-key:       Manage GPG keys
  label:         Manage labels
  preview:       Execute previews for gh features
  ruleset:       View info about repo rulesets
  search:        Search for repositories, issues, and pull requests
  secret:        Manage GitHub secrets
  ssh-key:       Manage SSH keys
  status:        Print information about relevant issues, pull requests, and notifications across repositories
  variable:      Manage GitHub Actions variables
FLAGS
  --help      Show help for command
  --version   Show gh version

LEARN MORE
  Use `gh <command> <subcommand> --help` for more information about a command.
  Read the manual at https://cli.github.com/manual
  Learn about exit codes using `gh help exit-codes`
  Learn about accessibility experiences using `gh help accessibility`

## Advanced Usage

For additional `gh` CLI patterns and commands, see [references/gh_commands.md](references/gh_commands.md) which includes:
- Pull request and issue management
- GitHub Actions workflow queries
- Gist operations
- Advanced API queries with `jq` filters

## Resources

### scripts/

- `gh_profile.sh` - Get user profile information
- `gh_repos.sh` - Get repository information with sorting options

### references/

- `gh_commands.md` - Comprehensive reference of useful `gh` CLI commands and patterns
