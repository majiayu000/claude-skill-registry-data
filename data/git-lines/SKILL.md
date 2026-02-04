---
name: git-lines
description: Stages specific lines from git diffs when hunk-level staging is too coarse. Use when a file contains multiple unrelated changes that need separate semantic commits, split commits, partial staging, or cherry-picking specific lines. Requires git-lines tool on PATH.
---

# Line-Level Git Staging

## Requirements

The `git-lines` tool must be installed and on PATH:
```bash
git-lines --version    # verify installation
```

> **Important**: Use normal git for viewing changes, staging whole files, and committing. Only use git-lines for the specific task of staging individual lines.

## Workflow

```
git diff                        # review changes (normal git)
↓ decide: "need to split this file"
git lines diff config.rs        # get line numbers
git lines stage config.rs:10    # stage first change
git commit -m "feat: first change"
git lines stage config.rs:25    # stage second change
git commit -m "fix: second change"
```

## Commands

Can be invoked as `git-lines` or `git lines` (if on PATH).

**View line numbers** (only when you intend to stage):
```bash
git lines diff              # all changed files
git lines diff file.rs      # specific file
```

Example output:
```
file.rs:
  +10:	  new_function();

  -25:	  old_code();
  +26:	  replacement_code();

  +40:	  another_addition();
```

**Stage specific lines**:
```bash
git lines stage file.rs:10         # single addition
git lines stage file.rs:-25        # single deletion
git lines stage file.rs:-25,26     # replacement (delete old, add new)
git lines stage file.rs:10..20     # range of additions
git lines stage file.rs:10,15,-20  # multiple (mixed)
git lines stage a.rs:5 b.rs:10     # multiple files
git lines stage -q file.rs:10      # quiet mode (no output)
```

After staging, shows what was staged:
```
Staged:
file.rs:
  -25:	  old_code();
  +25:	  replacement_code();
```

Use `--quiet` / `-q` to suppress this output.

## Line Numbers Stay Stable

Line numbers always refer to working tree positions, which don't change until you edit the file. You can run multiple `git lines stage` commands using line numbers from the same initial `git lines diff` output.
