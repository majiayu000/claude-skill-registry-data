---
name: tea-cli
description: Use when interacting with Gitea via command line - managing issues, PRs, releases, repos, or any git forge operations with tea CLI
---

# Tea CLI for Gitea

## Overview

Tea is the official CLI for Gitea. Use it for quick operations, scripting, and CI/CD workflows. For complex automation or custom integrations, use the `gitea:go-sdk` skill instead.

## Quick Setup

```bash
# Install
brew install tea  # or: go install code.gitea.io/tea@latest

# Authenticate
tea login add --name myserver --url https://gitea.example.com --token YOUR_TOKEN
```

See `references/authentication.md` for detailed auth options.

## Quick Reference

| Task | Command |
|------|---------|
| **Issues** | |
| List issues | `tea issues` |
| Create issue | `tea issues create --title "Bug" --body "Details"` |
| Close issue | `tea issues close 123` |
| **Pull Requests** | |
| List PRs | `tea pr` |
| Create PR | `tea pr create --head feature --base main` |
| Checkout PR | `tea pr checkout 45` |
| Merge PR | `tea pr merge 45` |
| Review PR | `tea pr review 45 --approve` |
| **Releases** | |
| List releases | `tea releases` |
| Create release | `tea release create --tag v1.0.0 --title "Release"` |
| Upload asset | `tea release assets create --tag v1.0.0 FILE` |
| **Repos** | |
| List repos | `tea repos` |
| Create repo | `tea repos create --name myrepo` |
| Clone repo | `tea clone owner/repo` |
| Fork repo | `tea repos fork owner/repo` |

## Command Categories

See `references/commands.md` for complete command reference:
- Issues & comments
- Pull requests & reviews
- Releases & assets
- Repositories & branches
- Labels, milestones, organizations
- Webhooks, notifications, time tracking
- Actions (secrets/variables)

## Common Workflows

See `references/workflows.md` for patterns:
- Feature branch to merged PR
- Release with assets
- Issue triage
- Multi-instance management

## Output Formats

```bash
tea issues --output json    # JSON
tea issues --output yaml    # YAML
tea issues --output csv     # CSV
tea issues --output simple  # Plain text
```

## Repository Context

Tea auto-detects repo from current directory's git remote. Override with:
```bash
tea issues --repo owner/repo
tea issues --login myserver  # specific Gitea instance
```

## Common Mistakes

| Problem | Solution |
|---------|----------|
| "not logged in" | Run `tea login add` first |
| Wrong repo context | Use `--repo owner/repo` flag |
| Can't find PR | Check `--state` flag (open/closed/all) |
| Token expired | Re-run `tea login add` with new token |
