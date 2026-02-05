---
name: jj-version-control
description: This skill should be used when the user works with Jujutsu (jj) version control, asks to "commit with jj", "rebase in jj", "use revsets", "create bookmarks", "push to git with jj", "split commits", "squash changes", "edit history", or mentions jj-specific concepts like changes, revsets, bookmarks, operation log, or anonymous branches.
---

# Jujutsu (jj) Version Control

Jujutsu (jj) is a Git-compatible distributed version control system with a fundamentally better mental model. It treats the working copy as a commit, distinguishes changes from revisions, and provides first-class conflict handling.

## Core Mental Model

### Key Paradigm Shifts from Git

| Git Concept | jj Concept | Implication |
|-------------|------------|-------------|
| Staging area/index | None - working copy IS a commit | No `jj add` needed; use `jj split` for selective commits |
| Detached HEAD | Anonymous branches (default) | Work freely; create bookmarks only when sharing |
| Branches auto-advance | Bookmarks are static pointers | Must `jj bookmark set` before `jj git push` |
| Conflicts block work | Conflicts are first-class objects | Commit through conflicts, resolve later |
| Commit hashes only | Change IDs + commit hashes | Stable identifiers even as commits evolve |

### The @ Symbol

`@` always refers to the current working copy commit. Most commands operate on `@` by default.

## Essential Commands

### Daily Workflow

```bash
# View status and log
jj status                    # Current state (alias: jj st)
jj log                       # Commit graph with smart defaults
jj diff                      # Changes in current working copy
jj diff -r <revset>          # Changes in specific revision

# Working with changes
jj describe -m "message"     # Set/update commit message (any revision with -r)
jj new                       # Create new empty change (signals "done with this")
jj commit -m "message"       # Shorthand: describe + new
jj edit <id>                 # Move working copy to different change
```

### History Manipulation

```bash
# Squash and move changes
jj squash                    # Move current changes into parent
jj squash -i                 # Interactive: select what to squash
jj move --from <id1> --to <id2>  # Move changes between any commits

# Split commits
jj split                     # Break current commit into multiple (interactive)
jj split -r <id>             # Split specific commit

# Rebase (always succeeds - conflicts become objects)
jj rebase -s <source> -d <dest>  # Rebase commit and descendants
jj rebase -b @ -d main          # Rebase current branch onto main

# Insert commits anywhere
jj new -A <id>               # Insert after (--insert-after)
jj new -B <id>               # Insert before (--insert-before)

# Remove commits
jj abandon                   # Discard commit, rebase children onto parent
```

### Git Interoperability

```bash
# Setup (in existing Git repo)
jj git init --colocate       # Creates .jj alongside .git; both work

# Remote operations
jj git fetch                 # Fetch from remotes
jj git push                  # Push tracked bookmarks
jj git push --allow-new      # Push newly created bookmarks

# IMPORTANT: No jj git pull - explicitly fetch then rebase
jj git fetch && jj rebase -b @ -d main
```

### Bookmark Management (Required for Pushing)

```bash
jj bookmark create <name>    # Create bookmark at @ (or -r <id>)
jj bookmark set <name>       # Move existing bookmark to @
jj bookmark list             # Show all bookmarks
jj bookmark track <name>@<remote>  # Start tracking remote bookmark
jj bookmark delete <name>    # Delete locally and on push
```

**Critical**: Bookmarks don't auto-advance. Before pushing:
```bash
jj bookmark set feature-x    # Move bookmark to current @
jj git push                  # Push the bookmark
```

### Undo and Recovery

```bash
jj op log                    # All operations (more comprehensive than git reflog)
jj undo                      # Undo last operation
jj op restore --operation <id>  # Restore to any previous state
jj evolog                    # Evolution of current change over time
```

## Revset Quick Reference

Revsets are a functional language for selecting commits.

### Basic Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `@` | Working copy | `jj log -r @` |
| `@-` | Parent of @ | `jj diff -r @-` |
| `@--` | Grandparent | `jj log -r @--` |
| `::x` | Ancestors of x | `jj log -r '::@'` |
| `x::` | Descendants of x | `jj log -r 'main::'` |
| `x..y` | Range (y not reachable from x) | `jj log -r 'main..@'` |
| `\|` | Union | `jj log -r 'a \| b'` |
| `&` | Intersection | `jj log -r 'mine() & main..'` |
| `~` | Difference | `jj log -r 'all() ~ trunk()'` |

### Key Functions

| Function | Returns |
|----------|---------|
| `trunk()` | Main branch (auto-detects main/master) |
| `bookmarks()` | All bookmarked commits |
| `remote_bookmarks()` | Remote bookmarks |
| `mine()` | Commits by current user |
| `heads(revset)` | Commits with no children |
| `roots(revset)` | Commits with no parents in set |
| `ancestors(revset)` | All ancestors |
| `descendants(revset)` | All descendants |

### Practical Revset Examples

```bash
# Work not yet pushed
jj log -r 'bookmarks() & ~remote_bookmarks()'

# My commits since branching from main
jj log -r 'mine() & main..@'

# Rebase all local branches onto updated main
jj rebase -s 'all:roots(trunk..@)' -d trunk

# Commits with conflicts
jj log -r 'conflict()'

# Empty commits (cleanup candidates)
jj log -r 'empty() & mine()'
```

## Common Workflows

### Starting New Feature

```bash
jj new -r main -m "feat: add feature X"   # Branch from main with message
# ... make changes ...
jj new                                     # Done with this, start next
```

### Iterative Development (Squash Workflow)

```bash
# Work in @, make small changes
jj describe -m "WIP"
# ... edit code ...
jj squash                    # Move changes to parent
# Repeat until done
jj describe -m "feat: final message"
```

### Rebasing onto Updated Main

```bash
jj git fetch
jj rebase -b @ -d main       # Rebase current branch onto main
# If conflicts, resolve with jj resolve or edit directly
jj bookmark set feature-x
jj git push
```

### Creating Pull Requests

```bash
# Ensure bookmark exists and is current
jj bookmark create pr-feature -r @  # Or: jj bookmark set pr-feature
jj git push --allow-new             # --allow-new for new bookmarks
# Create PR via gh or web interface
```

### Working with Conflicts

```bash
# Conflicts are committed, not blocking
jj rebase -s @ -d main       # May create conflicts
jj log                       # Shows conflict markers in graph
# Continue working if needed
jj resolve                   # Interactive resolution when ready
# Or edit conflict markers directly and jj describe
```

## Configuration Tips

### Essential Config (~/.jjconfig.toml)

```toml
[user]
name = "Your Name"
email = "your@email.com"

[ui]
default-command = "log"
diff-editor = ":builtin"    # Built-in TUI for split/squash -i

[revset-aliases]
'wip' = 'mine() & mutable() & ~empty()'
'stack' = 'trunk()..@'
```

### Useful Aliases

```toml
[aliases]
# Move nearest ancestor bookmark to current commit
tug = ['bookmark', 'move', '--from', 'heads(::@- & bookmarks())', '--to', '@']
```

## Common Pitfalls

**Bookmark not advancing**: Unlike Git branches, jj bookmarks don't auto-advance.
```bash
# Wrong assumption: bookmark follows after jj new
jj new
jj git push  # ERROR: bookmark still at old commit

# Correct: explicitly set before push
jj bookmark set <name>
jj git push
```

**Force push is normal**: jj rewrites history freely. Expect force pushes.

**No `jj git pull`**: Intentional design. Always:
```bash
jj git fetch
jj rebase -b @ -d main
```

## Progressive Context

- For advanced revsets and patterns: see `references/revsets.md`
- For stacked PR workflows: see `references/stacked-prs.md`
- For common workflow examples: see `examples/workflows.md`
