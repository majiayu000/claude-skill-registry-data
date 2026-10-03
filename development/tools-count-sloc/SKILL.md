---
name: tools-count-sloc
description: Present a summary of the code base including lines of source code and complexity metrics.
allowed-tools: Bash(*)
argument-hint: "[path]  (default: repo root)"
---

Count lines of source code and present complexity metrics for the codebase.

## Input

Optional argument: a subdirectory to scope the analysis (e.g. `components/dispatcher/v0`). Defaults to the repository root.

## Steps

1. Determine the target directory:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
if [[ -n "$ARGUMENTS" ]]; then
    TARGET="$REPO_ROOT/$ARGUMENTS"
    if [[ ! -d "$TARGET" ]]; then
        echo "Error: directory not found: $TARGET" >&2
        exit 1
    fi
else
    TARGET="$REPO_ROOT"
fi
```

2. Ensure `tokei` is installed (it's a fast, accurate SLOC counter written in Rust):

```bash
if ! command -v tokei &>/dev/null; then
    echo "Installing tokei..."
    cargo install tokei --quiet
fi
```

3. Run tokei for the SLOC summary, excluding build artifacts and vendored dependencies:

```bash
tokei "$TARGET" --exclude deps/spdk-build --exclude target --sort code
```

4. Run the complexity analysis script to produce per-component metrics:

```bash
SCRIPT="$(git rev-parse --show-toplevel)/.claude/skills/tools-count-sloc/complexity.sh"
bash "$SCRIPT" "$TARGET"
```

5. Present the results to the user in a clear summary with:
   - Total lines of code (by language)
   - Breakdown by component/directory
   - Complexity indicators (files with highest function counts, deepest nesting)
   - Comparison of code vs tests vs comments ratios

6. Write out the presented results to SUMMARY.md file. Interactively allow user to specify a different directory.
