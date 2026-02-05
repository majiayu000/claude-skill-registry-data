---
name: spec-metadata
description: Generates metadata for research documents and specifications including date/time, git commit, branch, and repository info. Use when creating research documents, handoffs, or any documentation that needs timestamp and git metadata.
allowed-tools: Bash
---

# Spec Metadata Generator

This skill generates metadata for documentation files including research documents, handoffs, and specifications.

## When to Activate

Activate this skill when:
- Creating research documents in `thoughts/shared/research/`
- Creating handoff documents in `thoughts/shared/handoffs/`
- Creating implementation plans
- Any documentation that needs timestamp and git metadata

## Process

### 1. Collect Metadata

Run the following commands to gather all necessary metadata:

**For git users:**
```bash
# Current date/time with timezone
date '+%Y-%m-%d %H:%M:%S %Z'

# Timestamp for filename
date '+%Y-%m-%d_%H-%M-%S'

# Git information
git rev-parse --show-toplevel  # Repo root
basename "$(git rev-parse --show-toplevel)"  # Repo name
git branch --show-current  # Current branch
git rev-parse HEAD  # Current commit hash
```

**For jj users:**
```bash
# Current date/time with timezone
date '+%Y-%m-%d %H:%M:%S %Z'

# Timestamp for filename
date '+%Y-%m-%d_%H-%M-%S'

# Jujutsu information
jj workspace root  # Repo root (or use pwd if in repo)
basename "$(pwd)"  # Repo name
jj log -r @ --no-graph -T 'bookmarks'  # Current bookmark(s)
jj log -r @ --no-graph -T 'commit_id.short()'  # Current commit hash
```

### 2. Output Format

Present the metadata to the user in this format:

```
Current Date/Time (TZ): [date with timezone]
Current Git Commit Hash: [commit hash]
Current Branch Name: [branch name]
Repository Name: [repo name]
Timestamp For Filename: [filename timestamp]
```

### 3. Usage in Documents

This metadata should be used in YAML frontmatter:

```yaml
---
date: [Current date and time with timezone in ISO format]
git_commit: [Current commit hash]
branch: [Current branch name]
repository: [Repository name]
last_updated: [Current date in YYYY-MM-DD format]
---
```

## Notes

- The filename timestamp format uses underscores and 24-hour time (e.g., `2025-01-08_13-55-22`)
- Always include timezone information in the date field
- For jj users, if multiple bookmarks exist, use the most relevant one or all if applicable
