---
name: git-diff
description: Display git changes in GitHub-style unified diff format with colored terminal output. Shows both staged (--cached) and unstaged changes with two-column line numbers, red/green highlighting, and chunk markers. Use when reviewing code changes, preparing commits, or comparing file modifications. Triggers on "git diff", "show changes", "what changed", or "review diff".
allowed-tools: Bash, Read
---

# git-diff

Display git changes in GitHub-style unified diff format.

## Execution

Run the Python script to display formatted diff:

```bash
python3 scripts/github_diff.py [optional-path]
```

## Output Format

- **File headers**: Dark background with filepath
- **Line numbers**: Two columns (old | new)
- **Deletions**: Red background with `-` marker
- **Additions**: Green background with `+` marker
- **Context**: Neutral with both line numbers
- **Chunk markers**: Cyan `@@ -n,m +n,m @@` headers

## Sections

1. **Staged Changes** (`git diff --cached`) - shown first if present
2. **Unstaged Changes** (`git diff`) - working directory modifications

## Examples

```bash
# Show all changes
python3 scripts/github_diff.py

# Filter by path
python3 scripts/github_diff.py src/components/
```

## Requirements

- Python 3.6+
- Git installed and in PATH
- Terminal with ANSI color support
