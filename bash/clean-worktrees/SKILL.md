---
name: clean-worktrees
description: Remove all git worktrees for merged branches. Accepts --dry-run to preview. Use after merging PRs or for weekly maintenance.
---

# Clean Worktrees Skill

Automatically remove all worktrees for branches merged into the default branch (`main` or `master`). No interaction required.

## Usage

```
/clean-worktrees              # Remove all merged worktrees
/clean-worktrees --dry-run    # Preview what would be deleted
```

## Implementation

Execute this script:

```bash
#!/bin/bash
set -euo pipefail

DRY_RUN=false
if [[ "${ARGUMENTS:-}" == *"--dry-run"* ]]; then
  DRY_RUN=true
fi

DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|.*/||' || \
                 git branch --list main master 2>/dev/null | head -1 | xargs || \
                 echo "main")

echo "Cleaning Worktrees"
echo "=================="
echo "Default branch: $DEFAULT_BRANCH"
echo ""

echo "1. Pruning stale git references..."
PRUNED=$(git worktree prune -v 2>&1)
[ -n "$PRUNED" ] && echo "$PRUNED" || echo "No stale references found"
echo ""

echo "2. Finding merged worktrees..."
MERGED_COUNT=0
MERGED_BRANCHES=()
CURRENT_DIR="$(pwd)"

while IFS= read -r line; do
  path=$(echo "$line" | awk '{print $1}')
  branch=$(echo "$line" | grep -oE '\[.*\]' | tr -d '[]' || true)
  [ -z "$branch" ] && continue
  [ "$branch" = "master" ] && continue
  [ "$branch" = "main" ] && continue
  [ "$path" = "$CURRENT_DIR" ] && continue
  if git branch --merged "$DEFAULT_BRANCH" 2>/dev/null | grep -q "^[* ] ${branch}$"; then
    MERGED_COUNT=$((MERGED_COUNT + 1))
    MERGED_BRANCHES+=("$branch|$path")
    echo "  - $branch (merged)"
  fi
done < <(git worktree list)

if [ $MERGED_COUNT -eq 0 ]; then
  echo "No merged worktrees found"
  git worktree list
  exit 0
fi

echo "Found $MERGED_COUNT merged worktree(s)"

if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN — Would delete:"
  for item in "${MERGED_BRANCHES[@]}"; do
    branch=$(echo "$item" | cut -d'|' -f1)
    path=$(echo "$item" | cut -d'|' -f2)
    echo "  - $branch ($path)"
  done
  echo "Run without --dry-run to actually delete"
  exit 0
fi

echo "3. Removing merged worktrees..."
REMOVED_COUNT=0
for item in "${MERGED_BRANCHES[@]}"; do
  branch=$(echo "$item" | cut -d'|' -f1)
  path=$(echo "$item" | cut -d'|' -f2)
  echo "Removing: $branch"
  git worktree remove "$path" 2>/dev/null || { rm -rf "$path" 2>/dev/null; git worktree prune 2>/dev/null; }
  git branch -d "$branch" 2>/dev/null || true
  REMOVED_COUNT=$((REMOVED_COUNT + 1))
done

echo ""
echo "Removed: $REMOVED_COUNT worktree(s)"
git worktree list
```

## Safety Features

- Only removes branches merged into `main`/`master`
- Auto-detects default branch via `git symbolic-ref`
- Never removes `main` or `master`
- Never removes the current working directory
- Dry-run mode to preview before deletion

## When to Use

- After merging PRs
- Weekly maintenance
- Before creating new worktrees: `/clean-worktrees --dry-run` first
