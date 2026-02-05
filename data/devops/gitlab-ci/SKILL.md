---
name: gitlab-ci
description: Use when working with GitLab using the glab CLI tool. Currently provides guidance for CI/CD pipelines including checking pipeline status, viewing job logs, and working with branches and tags.
---

# GitLab CI/CD with glab CLI

## Core Principle

**Always use `--branch` to specify branches or tags, never use pipeline IDs directly.**

## Common Workflows

### 1. Check Pipeline Status

```bash
# Check current branch
glab ci status

# Check specific branch or tag
glab ci status --branch=<branch-or-tag>

# Compact view
glab ci status --compact --branch=<branch-or-tag>
```

### 2. Get Pipeline Details

```bash
# Get pipeline info for a branch/tag
glab ci get --branch=<branch-or-tag>

# Include job IDs and details
glab ci get --branch=<branch-or-tag> --with-job-details
```

### 3. View Job Logs

```bash
# By job name (recommended when you know the name)
glab ci trace <job-name> --branch=<branch-or-tag>

# By job ID (use after getting job IDs from `glab ci get --with-job-details`)
glab ci trace <job-id>
```

**Example workflow:**
```bash
# 1. Check status and see job names
glab ci status --branch=staging

# 2. Get logs for a specific failed job
glab ci trace check-pending-migrations --branch=staging
```

### 4. List Pipelines

```bash
# List recent pipelines (overview only)
glab ci list

# Filter by ref (branch/tag)
glab ci list --ref=<branch-or-tag>

# Filter by status
glab ci list --status=failed
```

## Important Notes

- **NEVER use `glab ci view`** - it only works interactively. Use `glab ci status --live` for monitoring or `glab ci trace` for job logs instead
- Job names and job IDs work with `glab ci trace`, but pipeline IDs do not
- Always specify `--repo` if working with a repository other than the current directory
- Use `--branch` for both branches and tags (the flag name is `--branch` even for tags)

## Quick Reference

| Task | Command |
|------|---------|
| Pipeline status | `glab ci status --branch=<ref>` |
| Pipeline details | `glab ci get --branch=<ref>` |
| Job logs | `glab ci trace <job-name\|job-id> [--branch=<ref>]` |
| List pipelines | `glab ci list [--ref=<ref>]` |
