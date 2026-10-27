---
name: worktree-status
description: Show all active git worktrees with branch name, dirty/clean status, and last commit. Use after /worktree to check state across all parallel branches.
---

# Worktree Status Skill

Show all active git worktrees with their branch, dirty/clean status, and last commit.

## Usage

```
/worktree-status              # Show all worktrees
/worktree-status verbose      # Include last 3 commits per worktree
```

## Implementation

Execute this script:

```bash
#!/bin/bash
set -euo pipefail

VERBOSE=false
if [[ "${ARGUMENTS:-}" == *"verbose"* ]]; then
  VERBOSE=true
fi

GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"
if [ -z "$GIT_COMMON_DIR" ]; then
  echo "Not in a git repository"
  exit 1
fi

echo "Git Worktrees"
echo "============="
echo ""

COUNT=0
while IFS= read -r line; do
  if [[ "$line" =~ ^([^[:space:]]+)[[:space:]]+([0-9a-f]+)[[:space:]]+\[(.+)\]$ ]]; then
    WT_PATH="${BASH_REMATCH[1]}"
    WT_COMMIT="${BASH_REMATCH[2]}"
    WT_BRANCH="${BASH_REMATCH[3]}"

    if git -C "$WT_PATH" diff --quiet 2>/dev/null && git -C "$WT_PATH" diff --cached --quiet 2>/dev/null; then
      STATUS="clean"
    else
      CHANGED=$(git -C "$WT_PATH" status --short 2>/dev/null | wc -l | xargs)
      STATUS="dirty ($CHANGED files)"
    fi

    SHORT_HASH="${WT_COMMIT:0:7}"

    echo "  Branch: $WT_BRANCH"
    echo "  Path:   $WT_PATH"
    echo "  Status: $STATUS"
    echo "  Commit: $SHORT_HASH"

    if [ "$VERBOSE" = true ]; then
      echo "  Recent commits:"
      git --no-pager -C "$WT_PATH" log --oneline -3 2>/dev/null | sed 's/^/    /' || true
    fi

    echo ""
    COUNT=$((COUNT + 1))
  fi
done < <(git worktree list 2>/dev/null)

echo "Total: $COUNT worktree(s)"
echo ""
echo "Create:  \/worktree <branch>"
echo "Cleanup: \/clean-worktrees"
```

## Integration

Related skills:
- `/worktree` — create/manage worktrees
- `/clean-worktrees` — remove merged worktrees
