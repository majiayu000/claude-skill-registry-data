---
name: diff
description: Analyze branch diff against merge-base — stat overview, full diff, file list, commit list, or branch overlap check. Always uses merge-base to exclude main's forward progress.
---

# Diff Skill

Analyze the current branch's diff against its merge-base with main.

## Usage

```
/diff             # Stat overview (default)
/diff full        # Full patch output
/diff files       # List changed files only
/diff commits     # List commits on this branch
/diff overlap feature/other-branch  # Check for file overlap with another branch
```

## ⚠️ Critical: Always Use Merge-Base

```bash
# CORRECT — only shows YOUR changes
git diff $(git merge-base main HEAD)..HEAD

# WRONG — includes main's forward progress as noise
git diff main
```

## Instructions

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `stat` or (empty) | `git --no-pager diff $(git merge-base main HEAD)..HEAD --stat` |
| `full` | `git --no-pager diff $(git merge-base main HEAD)..HEAD \| head -200` |
| `files` | `git --no-pager diff $(git merge-base main HEAD)..HEAD --name-only` |
| `commits` | `git --no-pager log $(git merge-base main HEAD)..HEAD --oneline` |
| `overlap <branch>` | Cross-branch file overlap check (see below) |

### Cross-Branch Overlap Check:
```bash
BRANCH_A_FILES=$(git --no-pager diff $(git merge-base main HEAD)..HEAD --name-only)
BRANCH_B_FILES=$(git --no-pager diff $(git merge-base main <other-branch>)..<other-branch> --name-only)
# Show files that appear in both
comm -12 <(echo "$BRANCH_A_FILES" | sort) <(echo "$BRANCH_B_FILES" | sort)
```

## Report Format

For stat/default mode, report:
1. Files changed (count)
2. Lines added / removed
3. Any files that look unexpectedly large (>200 lines changed)
4. Any test files missing for changed source files
