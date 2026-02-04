---
name: git-push
description: |
  Multi-remote git push workflow for GitHub and Azure DevOps. Use when the user says
  "push to github", "push to azure", "push to origin", "push to secondary", "push to devops",
  "push to both", "sync remotes", or any variation requesting git push operations.
  Handles the azure-sync branch workflow that excludes .claude/, specs/, and CLAUDE.md from Azure.
---

# Git Multi-Remote Push

## Remotes

| Remote | Platform | Branch |
|--------|----------|--------|
| `origin` | GitHub | `main` (full repo) |
| `secondary` | Azure DevOps | `main` (excludes .claude/, specs/, CLAUDE.md) |

## Push Workflows

### GitHub (origin)

```bash
git push origin main
```

### Azure DevOps (secondary)

Azure excludes `.claude/`, `specs/`, and `CLAUDE.md`. Use the persistent `azure-sync` branch:

```bash
# Update azure-sync from main, remove excluded files, push
git checkout -B azure-sync main && \
git rm -r .claude CLAUDE.md specs 2>/dev/null || true && \
git commit -m "chore: sync to Azure (excludes .claude, CLAUDE.md, specs)" && \
git push secondary azure-sync:main --force && \
git checkout main --force
```

### Both Remotes

```bash
# GitHub first
git push origin main

# Then Azure (filtered)
git checkout -B azure-sync main && \
git rm -r .claude CLAUDE.md specs 2>/dev/null || true && \
git commit -m "chore: sync to Azure (excludes .claude, CLAUDE.md, specs)" && \
git push secondary azure-sync:main --force && \
git checkout main --force
```

## Pre-Push Checklist

1. Check for uncommitted changes: `git status`
2. If changes exist, commit them first (no AI metadata in commit messages)
3. Then push

## Commit Message Format

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

**No AI metadata** - no "Generated with Claude", no "Co-Authored-By: Claude", no emojis.

## Intent Mapping

| User Says | Action |
|-----------|--------|
| "push to github" / "push to origin" | `git push origin main` |
| "push to azure" / "push to secondary" | Use azure-sync workflow |
| "push to both" / "sync remotes" | Push to origin, then azure-sync workflow |
