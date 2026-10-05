---
name: merge-conflict-resolution
description: Detect, classify, and resolve git merge conflicts through structured analysis of conflict markers, per-file strategy selection, and post-resolution verification. Use when a branch has conflicts with its merge target, when rebasing onto an updated base, or when gh-merge detects an unmergeable PR.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
context: fork
agent: Explore
---

# Merge Conflict Resolution

Domain skill for detecting, classifying, and resolving git merge conflicts systematically.

## Iron Law

**NEVER silently drop changes.** Every conflict resolution must account for both sides. If lines from either side are excluded, the rationale must be documented. When in doubt, ask the user rather than guess.

## Conflict Detection

Detect conflicted files and their conflict types:

```bash
# List files with unmerged entries
git diff --name-only --diff-filter=U

# Full status with conflict markers
git status --porcelain
```

Classify each file by its porcelain status prefix.

## Conflict Type Classification

| Status | Type | Description |
|--------|------|-------------|
| UU | Content | Both sides modified the same file |
| AA | Add-add | Both sides added a file with the same name |
| UD | Delete-modify (ours deleted) | We deleted, they modified |
| DU | Delete-modify (theirs deleted) | They deleted, we modified |
| AU | Rename-related (add/unmerged) | Rename collision |
| UA | Rename-related (unmerged/add) | Rename collision |

## Conflict Complexity Classification

Assess each conflicted file's complexity before choosing a strategy:

| Complexity | Description | Example |
|------------|-------------|---------|
| Trivial | Non-overlapping changes in different sections | Import added at top + function added at bottom |
| Semantic | Changes to the same logical unit | Both sides modify the same function |
| Structural | File was refactored on one side | Moved code, renamed variables, changed structure |
| Delete-modify | One side deleted what the other modified | Feature removed vs feature enhanced |

## Resolution Strategies

| Strategy | When to Use | Risk | Autonomy |
|----------|-------------|------|----------|
| accept-ours | Their change is superseded by ours | Low | Auto for trivial |
| accept-theirs | Our change is superseded by theirs | Low | Auto for trivial |
| manual-merge | Both changes are needed | Medium | Show rationale |
| rebase | Clean linear history needed, few conflicts | Medium | Show rationale |

## Manual Merge Algorithm

For each conflict hunk in a file:

1. **Parse** — extract the ours block (`<<<<<<<` to `=======`) and theirs block (`=======` to `>>>>>>>`)
2. **Identify intent** — what was each side trying to accomplish?
3. **Classify compatibility**:
   - **Compatible**: both changes can coexist (e.g., different imports, non-overlapping logic) — combine both
   - **Competing**: changes are mutually exclusive (e.g., different implementations of the same function) — ask user
4. **Apply** — write the resolved content, removing all conflict markers
5. **Verify** — confirm no orphaned markers remain in the file

## Delete-Modify Protocol

When one side deletes a file (or section) that the other side modifies:

1. Show the user what was deleted and what was modified
2. Present options:
   - Keep the modified version
   - Accept the deletion
   - Keep modified version in a new location (if file was moved)
3. Wait for user decision — never auto-resolve delete-modify conflicts

## Post-Resolution Verification

After resolving all conflicts, run these checks in order:

### 1. Orphaned Marker Audit

```bash
# Must return zero results
grep -rn '^<<<<<<<\|^=======\|^>>>>>>>' . 2>/dev/null | grep -v '.git/' | grep -v 'node_modules/'
```

If any markers remain, resolution is incomplete. Fix before proceeding.

### 2. Stage and Complete

```bash
# Stage resolved files
git add <resolved-files>

# Complete the merge or rebase
git commit --no-edit   # or GIT_EDITOR=true git rebase --continue
```

### 3. Build and Test Verification

Run the project's quality commands (lint, test, typecheck) to verify the resolution didn't break anything. Use capability-discovery to find available commands.

### 4. Resolution Diff Display

Show a summary of what was resolved:

```bash
# Show what changed in the resolution
git diff HEAD~1 --stat
```

## Rationalization Prevention

Watch for these shortcuts that lead to incorrect resolutions:

| Rationalization | Correct Response |
|----------------|-----------------|
| "Just take ours for everything" | Analyze each conflict individually — theirs may contain important changes |
| "Too complex, just reset and start over" | Read both sides first — most conflicts are simpler than they appear |
| "Tests pass so the resolution is correct" | Review the diff too — passing tests don't guarantee semantic correctness |
| "This file isn't important" | Every file in the conflict list matters — verify or explicitly document why it's safe to skip |
| "Same change on both sides" | Verify they're truly identical — similar-looking changes may have subtle differences |

## Configuration

Read conflict resolution settings using the three-tier cascade:

```bash
# Read conflictResolution.autoResolveTrivial (local > project > user > default)
AUTO_RESOLVE=$(jq -r '.conflictResolution.autoResolveTrivial // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$AUTO_RESOLVE" ] && AUTO_RESOLVE=$(jq -r '.conflictResolution.autoResolveTrivial // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$AUTO_RESOLVE" ] && AUTO_RESOLVE=$(jq -r '.conflictResolution.autoResolveTrivial // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$AUTO_RESOLVE" ] && AUTO_RESOLVE="true"

# Read conflictResolution.maxConflictFiles
MAX_FILES=$(jq -r '.conflictResolution.maxConflictFiles // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$MAX_FILES" ] && MAX_FILES=$(jq -r '.conflictResolution.maxConflictFiles // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$MAX_FILES" ] && MAX_FILES=$(jq -r '.conflictResolution.maxConflictFiles // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$MAX_FILES" ] && MAX_FILES="20"
```

## Integration Points

This skill provides domain knowledge for:
- `gh-resolve` — conflict analysis, classification, resolution strategies, and verification (loaded as context)
- `gh-merge` — conflict detection triggers handoff to `gh-resolve`

The skill's content informs:
- Per-file resolution strategy selection
- User decision points (delete-modify, competing changes)
- Post-resolution quality verification

## Graceful Degradation

| Missing Capability | Fallback |
|-------------------|----------|
| No capability-discovery | Detect quality commands from tech stack indicators |
| No quality commands found | Skip build/test verification, warn user |
| AskUserQuestion unavailable | Default to manual-merge for all non-trivial conflicts |
| Config files missing | Use defaults (autoResolveTrivial: true, maxConflictFiles: 20) |
