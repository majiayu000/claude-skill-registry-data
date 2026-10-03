---
name: jj
description: Jujutsu (jj) skill for the ikigai project
---

# Jujutsu (jj)

## Description
Standard jj operations for day-to-day development work.

## CRITICAL: Commits Are Permanent

**When user says "commit": IMMEDIATELY use `jj commit -m "msg"`**

- Committed changes are **permanent** and stored forever in operation log
- Uncommitted changes **can be lost** during rebases/restores
- Every commit is **recoverable** via `jj op restore`

Run `make check` periodically to catch issues early.

## Configuration

- **Remote**: origin (github.com:mgreenly/ikigai.git)
- **Primary branch**: main (bookmark)

## Commit Policy

Use `jj commit -m "msg"` to create permanent commits. NOT `jj describe` (only updates description without creating commit).

## Prohibited Operations

This skill does NOT permit:
- Modifying the `main` bookmark locally
- Merging into main locally
- Force pushing to main

**Merges to main only happen via GitHub PRs.** All work is done on feature bookmarks, pushed to origin, and merged through pull requests on GitHub. Never merge locally.

## Permitted Operations

- Commit to feature/fix bookmarks
- Push feature/fix bookmarks to remote
- Create new bookmarks
- Create and push tags
- Fetch from remote
- Rebase commits
- Create new commits on any mutable revision

## Squashing (Permission Required)

**NEVER squash without explicit user permission.** Only when user says "squash" or "squash commits".

**Squashing workflow:**
1. `jj edit <revision>` - Move to commit to squash
2. `jj squash -m "message"` - Squash into parent (MUST use `-m` flag in CLI)
3. Repeat for additional commits

**Flag limitations:**
- ✗ `jj squash -r <rev> --into <dest>` - INVALID (flags cannot combine)
- ✓ `jj edit <rev>` then `jj squash -m "msg"` - VALID

**Recovery:** `jj op log` then `jj op restore <id>` (all operations are logged)

## Common Flags

| Flag | Why Use It |
|------|------------|
| `-m "message"` | Provide commit/squash message inline (required in non-interactive environments) |
| `-r <revision>` | Specify which revision to operate on (alternative to `jj edit` first) |
| `--into <dest>` | Squash into specific destination (cannot combine with `-r`) |
| `--no-graph` | Show log output without tree visualization (cleaner for parsing) |
| `--stat` | Show file change statistics in diff (lines added/removed per file) |
| `--bookmark <name>` | Push specific bookmark to remote |
| `-d <dest>` | Set destination for rebase operation |

## Common Commands

| Task | Command |
|------|---------|
| Check status | `jj status` |
| View changes | `jj diff` |
| View log | `jj log` |
| **Commit all files** | **`jj commit -m "msg"`** |
| Squash into parent | `jj squash -m "msg"` |
| Edit a commit | `jj edit <revision>` |
| Create bookmark | `jj bookmark create <name>` |
| Update bookmark to @ | `jj bookmark set <name>` |
| Push bookmark | `jj git push --bookmark <name>` |
| Fetch from remote | `jj git fetch` |
| Restore working copy | `jj restore` |
| Create commit on revision | `jj new <revision>` |
| Rebase | `jj rebase -d <destination>` |
| Create tag | `jj tag set <name> -r <revision>` |
| Push tag | `git push origin <tag>` |
| List tags | `jj tag list` |

## Key Concepts

- **Working copy** (`@`): Always a commit being edited (no staging area)
- **Bookmarks**: Equivalent to git branches (named pointers to commits)
- **Immutability**: `◆` = permanent, `○` = mutable, `@` = mutable (lost if not committed)
- **Update bookmark**: Find recent bookmark in ancestry, use `jj bookmark set <name>`
