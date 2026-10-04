---
name: multi-repo-explorer
description: Use when you need to understand how internal libraries work, trace dependencies across repositories, or explore code patterns in reference repos - clones/updates a configured list of repos and provides exploration guidance
---

# Multi-Repo Explorer

## Overview

Maintain a local cache of reference repositories for exploring large codebases that span multiple repos. Clone missing repos, pull updates for existing ones, then explore to understand patterns and copy code snippets.

## Configuration

Edit `repos.txt` in this skill directory. Add one repo URL per line:

```
git@github.com:your-org/auth-service.git
git@github.com:your-org/shared-utils.git
https://github.com/public/some-library.git
```

**Default repos location:** `~/.reference-repos`
**Override with:** `REPOS_DIR=/custom/path ./sync.sh`

## Usage

### Step 1: Sync Repos

Run the sync script to clone missing repos and pull updates:

```bash
~/.claude/skills/multi-repo-explorer/sync.sh
```

Output shows status for each repo:
- `✓ repo-name (cloned)` - newly cloned
- `✓ repo-name (updated)` - pulled latest
- `✓ repo-name (up to date)` - no changes
- `✗ repo-name (clone/pull failed)` - check URL and auth
- `⚠ repo-name (dirty)` - has local changes, skipped pull

### Step 2: Explore

Use standard tools to explore the repos:

```bash
# Search across all repos
Grep pattern ~/.reference-repos

# Search specific repo
Grep pattern ~/.reference-repos/auth-service

# Find files
Glob "**/*.ts" ~/.reference-repos/repo-name

# Read files
Read ~/.reference-repos/repo-name/src/file.ts
```

### Rules

1. **Read-only** - Never modify files in reference repos
2. **Copy and adapt** - Can copy snippets into current project, adapt to fit conventions
3. **Cite sources** - When copying significant patterns, note which repo it came from

## Common Exploration Patterns

| Question | Approach |
|----------|----------|
| "How does X handle Y?" | Grep for Y in repo X, read relevant files |
| "What's the API for X?" | Look for exports, public interfaces, README |
| "Find examples of pattern" | Grep across all repos |
| "Trace data flow" | Start at entry point, follow imports |

## Troubleshooting

**Auth failures:** Ensure SSH keys are configured for private repos, or use HTTPS with token.

**Dirty working directory:** Commit or stash changes in the repo before pulling.

**Repo not found:** Verify URL is correct and you have access.
