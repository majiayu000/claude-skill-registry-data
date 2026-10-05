---
name: jj
description: Jujutsu (jj) — Git-compatible VCS with automatic change tracking, conflict-aware rebasing, and revset algebra
version: 1.0.0
trit: +1
role: PLUS
color: "#7B5EA7"
source: brew install jujutsu
---

# jj

Git-compatible next-generation VCS with first-class conflicts, anonymous branches, and operation log undo.

**Trit**: +1 (PLUS) — Generator role: creates new changes fluidly without staging friction

---

## Overview

Jujutsu (jj) wraps or replaces Git with a superior mental model:
- **No staging area** — working copy is always a commit, auto-snapshotted
- **First-class conflicts** — conflicts are values in the tree, not blockers
- **Operation log** — every repo mutation is logged and undoable (`jj undo`)
- **Revsets** — algebraic revision language for selecting/filtering commits
- **Colocated mode** — works on existing `.git` repos alongside `git` CLI

---

## Installation

```bash
# macOS
brew install jujutsu

# Nix
nix profile install nixpkgs#jujutsu

# Cargo
cargo install --locked jj-cli

# flox
flox install jujutsu
```

---

## Setup

```bash
jj config set --user user.name "Your Name"
jj config set --user user.email "you@example.com"

# Initialize in existing git repo (colocated)
jj git init --colocate

# Clone from remote
jj git clone <url>
```

---

## Core Workflow

```bash
# Working copy is always @ (current change)
jj status              # what's changed in @
jj diff                # show diff of @
jj log                 # commit graph with change + commit IDs

# Describe current change
jj describe -m "Add feature"   # alias: jj desc

# Finish current change, start new empty one
jj new                 # start fresh on top of @
jj new -m "next task"  # with message
jj commit -m "msg"     # describe @ then create new on top (like git commit)

# Navigate
jj prev                # move to parent
jj next                # move to child
jj edit <change-id>    # switch to editing a specific change
```

---

## Bookmarks (Branches)

```bash
# Create bookmark at current change
jj bookmark create <name>
jj bookmark set -r @ <name>    # point bookmark to @

# List bookmarks
jj bookmark list

# Track remote bookmark
jj bookmark track main@origin

# Delete
jj bookmark delete <name>
```

---

## Rewriting History

```bash
# Squash @ into parent
jj squash

# Squash into specific change
jj squash --into <change-id>

# Split current change into multiple
jj split

# Edit an earlier change (auto-rebases descendants)
jj edit <change-id>

# Rebase onto another change
jj rebase -d main

# Absorb — auto-distribute hunks to matching earlier commits
jj absorb

# Abandon (discard) a change
jj abandon <change-id>
```

---

## Git Interop

```bash
# Fetch from remote
jj git fetch

# Push bookmark to remote
jj git push -b <bookmark> --allow-new

# Push change by ID (auto-creates bookmark)
jj git push --change <change-id>

# Import/export between jj and git views
jj git import
jj git export
```

---

## Revsets

Algebraic expressions for selecting revisions:

```bash
@              # current working copy
@-             # parent of @
main           # bookmark named "main"
mine()         # changes authored by you
bookmarks()    # all bookmarked changes
trunk()        # main trunk bookmark

# Composition
@::            # @ and all descendants
..@            # all ancestors of @
main..@        # changes between main and @
bookmarks() & ~remote_bookmarks()  # local-only bookmarks

# Use in commands
jj log -r 'mine() & ~main'
jj rebase -d 'trunk()'
```

---

## Conflicts

Jujutsu treats conflicts as first-class tree values:

```bash
# Conflicts don't block work — they're recorded in the commit
jj status                   # shows conflicted files
jj resolve <file>           # open merge tool
jj resolve --list           # list conflicted files

# Rebase through conflicts, resolve later
jj rebase -d main           # may create conflict commit
jj edit <conflicted>        # go fix it
# ... resolve files ...
jj squash                   # clean up
```

---

## Operations & Undo

```bash
jj undo                     # undo last operation
jj op log                   # show all operations
jj op restore <op-id>       # restore to specific operation
```

---

## Workspaces

```bash
jj workspace add ../ws2     # create additional workspace
jj workspace list
jj workspace update-stale   # sync after external changes
```

---

## Useful Aliases

Add to `~/.config/jj/config.toml`:

```toml
[aliases]
fetch = ["git", "fetch"]
push = ["git", "push", "--allow-new"]
tug = ["bookmark", "move", "--from", "heads(::@- & bookmarks())", "--to", "@-"]
mine = ["bookmark", "list", "-r", "mine()"]
```

---

## GitHub Workflow

```bash
# Start feature from trunk
jj new main -m "Add widget"
# ... make changes ...
jj bookmark create -r @ feature-widget
jj git push -b feature-widget --allow-new
# → create PR on GitHub

# Address review feedback
jj edit <change-id>          # go back to the change
# ... fix ...
jj new                       # back to tip
jj git push -b feature-widget

# Sync with upstream
jj git fetch
jj rebase -d main
```

---

## GH CLI Integration

For non-colocated repos, set `GIT_DIR`:

```bash
export GIT_DIR=$PWD/.jj/repo/store/git
gh pr list   # now works in jj repos
```

Or via `.envrc` with direnv:
```bash
export GIT_DIR=$PWD/.jj/repo/store/git
```

---

## Triadic Composition

```
jj (+1)  +  pijul (-1)  +  gh (0)  = 0 ✓
Generator   Validator     Coordinator
```

jj generates new changes fluidly, pijul validates patch-theoretic correctness, gh coordinates with GitHub remotes.

---

## References

- [Jujutsu Docs](https://docs.jj-vcs.dev/latest/)
- [CLI Reference](https://docs.jj-vcs.dev/latest/cli-reference/)
- [GitHub Workflow](https://docs.jj-vcs.dev/latest/github/)
- [Steve Klabnik's Tutorial](https://steveklabnik.github.io/jujutsu-tutorial/)
- [Jujutsu for Everyone](https://jj-for-everyone.github.io/)
- [pijul skill](../pijul/SKILL.md)
- [gh skill](../gh/SKILL.md)
