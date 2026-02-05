---
name: gitea-tea
description: Manage Gitea via CLI. Use when user mentions "tea", "gitea cli", or needs terminal-based Gitea operations.
version: 1.0.0
---

# Gitea CLI (tea)

## Overview

Official command-line interface for Gitea. Manage issues, PRs, releases, and repos from terminal.

## Instructions

1. **Verify authentication**: Run `tea whoami` to confirm login
2. **Check context**: Run in git repo for auto-detection, or use `--repo owner/repo`
3. **Use non-interactive mode**: Always use `--output` flag and provide all arguments
4. **Choose operation**: See command reference sections below

## Installation

```bash
# macOS
brew install tea

# Linux (binary)
curl -sL https://dl.gitea.io/tea/main/tea-main-linux-amd64 -o tea
chmod +x tea && sudo mv tea /usr/local/bin/

# From source
go install code.gitea.io/tea@latest
```

## Authentication

```bash
# Interactive login (recommended)
tea login add
# Select: Application Token
# Enter Gitea URL and token from User Settings → Applications

# List logins
tea login list

# Set default
tea login default gitea.example.com

# Delete login
tea login delete gitea.example.com

# Verify
tea whoami
```

## Issues

### List Issues
```bash
# Open issues in current repo
tea issues list

# All issues (including closed)
tea issues list --state all

# Filter by milestone
tea issues list --milestone "v1.0.0"

# Filter by assignee and labels
tea issues list --assignee username --label bug,critical

# From specific repo
tea issues list --repo owner/repo --login gitea.com
```

### View Issue
```bash
# View issue with comments
tea issue 42

# Without comments
tea issue 42 --comments=false

# Open in browser
tea open 42
```

### Create Issue
```bash
# Interactive
tea issues create

# With arguments
tea issues create \
  --title "Fix authentication bug" \
  --body "Users cannot login with special characters" \
  --label bug,security \
  --assignee developer1 \
  --milestone "v1.2.0"

# From file
tea issues create \
  --title "Feature request" \
  --body "$(cat feature-request.md)"
```

### Modify Issues
```bash
# Close issue
tea issues close 42

# Reopen issue
tea issues reopen 42

# Edit issue
tea issues edit 42 \
  --title "Updated title" \
  --assignee newdev \
  --add-labels "enhancement"
```

## Pull Requests

### List PRs
```bash
# Open PRs
tea pulls

# Closed PRs
tea pulls --state closed

# Filter by reviewer and labels
tea pulls --reviewer username --label "needs-review"
```

### View PR
```bash
# View PR details
tea pr 15

# Without comments
tea pr 15 --comments=false

# Open in browser
tea open 15
```

### Create PR
```bash
# Interactive
tea pulls create

# With arguments
tea pulls create \
  --title "Implement user authentication" \
  --description "Adds OAuth and JWT support" \
  --base main \
  --head feature/auth \
  --assignee reviewer1,reviewer2 \
  --label "enhancement"

# Description from file
tea pulls create \
  --title "Major refactor" \
  --description "$(cat pr-description.md)"
```

### Checkout PR
```bash
# Checkout PR locally
tea pulls checkout 20

# Custom branch name
tea pulls checkout 20 pr-20-custom-name

# Clean up checked out PRs
tea pulls clean
```

### Review & Merge
```bash
# Approve PR
tea pulls approve 20 --comment "LGTM!"

# Request changes
tea pulls reject 20 --comment "Please add tests"

# Leave comment
tea pulls review 20 \
  --state comment \
  --comment "Consider refactoring this section"

# Merge PR (squash)
tea pulls merge 20 --style squash --message "feat: implement auth"

# Merge PR (rebase)
tea pulls merge 20 --style rebase

# Close PR
tea pulls close 20

# Reopen PR
tea pulls reopen 20
```

## Releases

### List Releases
```bash
tea releases list
tea releases list --limit 10
tea releases list --repo owner/project
```

### Create Release
```bash
# Basic release
tea releases create v1.0.0 \
  --title "Version 1.0.0" \
  --note "First stable release"

# From changelog file
tea releases create v1.2.0 \
  --title "Version 1.2.0" \
  --note-file CHANGELOG.md

# Draft release
tea releases create v2.0.0-beta \
  --title "Beta Release" \
  --draft \
  --note "Beta for testing"

# With assets
tea releases create v1.1.0-rc1 \
  --title "Release Candidate 1" \
  --prerelease \
  --asset dist/binary-linux-amd64 \
  --asset dist/binary-darwin-amd64

# Create tag + release
tea releases create v1.3.0 \
  --target main \
  --title "Version 1.3.0" \
  --note "New features"
```

### Edit/Delete Release
```bash
# Update release
tea releases edit v1.0.0 \
  --title "Version 1.0.0 - Updated" \
  --note-file NEW-NOTES.md

# Publish draft
tea releases edit v2.0.0 --draft=false

# Delete release
tea releases delete v0.9.0
tea releases delete v1.0.0-beta --confirm
```

## Labels

```bash
# List labels
tea labels list
tea labels list --repo owner/project
tea labels list --save  # Save labels to file

# Create label
tea labels create bug \
  --color "#ff0000" \
  --description "Something isn't working"

tea labels create enhancement \
  --color "0,255,0" \
  --description "New feature"

# Update label
tea labels update bug --color "#cc0000"
tea labels update old-name --name new-name

# Delete label
tea labels delete bug
```

## Milestones

```bash
# List milestones
tea milestones list
tea milestones list --state open
tea milestones list --state closed

# View milestone issues
tea milestones issues "v1.0.0"
tea milestones issues "v1.0.0" --kind pull  # Only PRs
tea milestones issues "v1.0.0" --state all

# Add issue/PR to milestone
tea milestones issues add "v1.0.0" 42

# Remove issue/PR from milestone
tea milestones issues remove "v1.0.0" 42

# Create milestone
tea milestones create "v2.0.0" \
  --description "Major version release" \
  --deadline "2024-12-31"

# Close milestone
tea milestones close "v1.0.0"

# Reopen milestone
tea milestones reopen "v1.0.0"

# Delete milestone
tea milestones delete "v0.9.0"
```

## Repositories

```bash
# List repos
tea repos list
tea repos list --org myorg
tea repos list --watched  # Watched repos
tea repos list --starred  # Starred repos
tea repos list --type fork  # Filter: fork, mirror, source
tea repos list --output yaml

# Search repos
tea repos search "keyword" --login gitea.com

# View repo details
tea repos owner/repo

# Create repo
tea repos create --name myrepo --private --init
tea repos create \
  --name myrepo \
  --owner myorg \
  --description "My project" \
  --private \
  --init \
  --gitignores Go \
  --license MIT

# Create from template
tea repos create-from-template \
  --template owner/template-repo \
  --name new-repo

# Fork repo
tea repos fork --repo owner/repo
tea repos fork --repo owner/repo --owner myorg

# Delete repo
tea repos delete owner/repo

# Clone repo (without git)
tea clone owner/repo
tea clone owner/repo ./target-dir
tea clone gitea.com/owner/repo  # With host
```

## Time Tracking

```bash
# List time entries
tea times list
tea times list --issue 42
tea times list --user username
tea times list --from "2024-01-01" --until "2024-12-31"

# Add time
tea times add 42 --time "2h"
tea times add 42 --time "1h30m" --message "Implemented auth logic"

# Delete entry
tea times delete 42 --id 123
```

## Notifications

```bash
# List notifications (current repo)
tea notifications list

# List all notifications
tea notifications list --mine

# Filter by type
tea notifications list --types issue,pull

# Filter by state
tea notifications list --states unread,pinned

# Mark as read
tea notifications read  # All filtered
tea notifications read 123  # Specific ID

# Mark as unread
tea notifications unread 123

# Pin/unpin
tea notifications pin 123
tea notifications unpin 123
```

## Organizations

```bash
# List organizations
tea organizations list

# View organization details
tea organizations myorg

# Create organization
tea organizations create myorg

# Delete organization
tea organizations delete myorg
```

## Branches

```bash
# List branches
tea branches list
tea branches list --output json

# View branch details
tea branches main

# Protect branch
tea branches protect main

# Unprotect branch
tea branches unprotect main
```

## Comments

```bash
# Add comment to issue or PR
tea comment 42 "This is my comment"

# From specific repo
tea comment 42 "Comment text" --repo owner/repo
```

## Admin (requires admin access)

```bash
# List users
tea admin users list
tea admin users list --output json
```

## Non-Interactive Mode (AI Agents)

**IMPORTANT:** When using tea in AI agent environments (no TTY), avoid interactive prompts:

```bash
# Use --output to disable interactive mode
tea issues --output simple
tea pulls --output json

# Provide ALL required arguments upfront
tea issue create --title "Bug title" --body "Description here"
tea pr create --title "PR title" --head feature-branch --base main

# Use -y or --yes for confirmations
tea pr merge 5 --yes
tea releases delete v0.9.0 --yes

# Set default login to avoid prompts
tea login default <login-name>
```

**Always prefer explicit flags over interactive prompts.**

## Guidelines

### Do
- Use `--output simple` or `--output json` for non-interactive mode
- Provide all required arguments upfront to avoid prompts
- Run `tea whoami` to verify authentication before operations
- Use `tea open <number>` to quickly view in browser

### Don't
- Use interactive commands in AI agent context (no TTY)
- Forget `--repo owner/repo` when outside git repository
- Skip `--yes` flag for destructive operations in scripts
- Use `tea login add` interactively (configure beforehand)

## Examples

### Example: Feature Branch → PR
```bash
git checkout -b feature/new-feature
# ... make changes ...
git add . && git commit -m "feat: add new feature"
git push -u origin feature/new-feature
tea pulls create --title "Add new feature" --base main --head feature/new-feature
```

### Example: Review & Merge PR
```bash
tea pulls checkout 20
# ... review code ...
tea pulls approve 20 --comment "LGTM!"
tea pulls merge 20 --style squash
```

### Example: Create Release with Assets
```bash
git tag v1.0.0
git push origin v1.0.0
tea releases create v1.0.0 \
  --title "v1.0.0" \
  --note-file CHANGELOG.md \
  --asset dist/app-linux \
  --asset dist/app-darwin
```
