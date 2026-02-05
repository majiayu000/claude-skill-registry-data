---
name: validate-git-safety
description: Validate git operations won't affect version branches or cause data loss
allowed-tools: Bash, Read
---

# Validate Git Safety Skill

**Purpose**: Validate git history-rewriting operations won't affect version branches or cause unintended data loss.

**Performance**: Prevents catastrophic history rewrites, protects version branches

## When to Use This Skill

### ✅ Use validate-git-safety When:

- Before `git filter-branch` command
- Before `git rebase` with `--all` or `--branches`
- Before any history-rewriting operation
- Considering operation that might affect multiple branches
- **Before any non-atomic git operation in `/workspace/main`**

### ❌ Do NOT Use When:

- Simple branch operations (checkout, create)
- Operations explicitly targeting single branch
- Read-only git operations (log, diff, status)
- Fast-forward merge in main worktree (atomic, safe)

## What This Skill Does

### 1. Identifies Version Branches

```bash
# Find all version branches (v1, v13, v21, etc.)
git branch | grep -E "^  v[0-9]+$"
```

### 2. Analyzes Command Impact

```bash
# Check if command affects multiple branches
if [[ "$COMMAND" == *"--all"* ]] || [[ "$COMMAND" == *"--branches"* ]]; then
  # DANGER: Will affect version branches
fi
```

### 3. Validates Target Branch

```bash
# If command targets specific branch, verify not version branch
TARGET_BRANCH=$(extract_target_from_command "$COMMAND")
if [[ "$TARGET_BRANCH" =~ ^v[0-9]+$ ]]; then
  # DANGER: Targeting version branch directly
fi
```

### 4. Blocks or Warns

```bash
# For dangerous operations:
echo "❌ BLOCKED: Operation would affect version branches"
exit 2

# For potentially dangerous:
echo "⚠️  WARNING: Verify this won't affect version branches"
echo "Protected branches: v1, v13, v14, v15, v18, v19, v20, v21"
```

## Protected Branch Patterns

### Version Branches

**Pattern**: `v[0-9]+`

**Examples**:
- `v1` - Version 1 marker
- `v13` - Version 13 marker
- `v21` - Current version marker

**Protection**: NEVER delete, modify, or rewrite history

### Temporary Branches (Safe to Delete)

**Patterns**:
- Task branches: `implement-*`, `fix-*`, `add-*`
- Backup branches: `backup-before-*-20251111*`
- Agent branches: `*-architect`, `*-tester`, `*-formatter`

**Lifecycle**: Delete after merge to main

## Dangerous Command Patterns

### ❌ NEVER Use These

```bash
# Affects ALL branches including version branches
git filter-branch --all ...
git filter-branch --branches ...

# Direct manipulation of version branch
git filter-branch v21 ...
git rebase --onto ... v21

# Forced history rewrite without backup
git reset --hard HEAD~10  # On version branch
```

### ✅ SAFE Alternatives

```bash
# Target specific non-version branch
git filter-branch main ...
git filter-branch my-feature-branch ...

# Rebase feature branch only
git rebase main  # While on feature branch

# Update version branch pointer (not history)
git branch -f v21 <new-commit>
```

## Usage

### Validate Before Filter-Branch

```bash
# Before running git filter-branch
COMMAND="git filter-branch --tree-filter 'rm -f secrets.txt' HEAD"

/workspace/main/.claude/scripts/validate-git-safety.sh \
  --command "$COMMAND"

# If validation passes, safe to execute
# If validation fails, command blocked
```

### Validate Before Branch Delete

```bash
# Before deleting branches
BRANCHES="v21 backup-123 my-feature"

/workspace/main/.claude/scripts/validate-git-safety.sh \
  --operation "delete" \
  --branches "$BRANCHES"

# Will identify v21 as protected, block deletion
```

### Check Current Repository State

```bash
# List all protected branches
/workspace/main/.claude/scripts/validate-git-safety.sh \
  --check-protected

# Output:
# Protected version branches:
# - v1
# - v13
# - v21
```

## Safety Rules

### Main Worktree Protection {#main-worktree-protection}

**⚠️ CRITICAL**: `/workspace/main` is shared infrastructure across concurrent Claude instances.

**Allowed in Main Worktree (Atomic Only)**:
- ✅ `git merge --ff-only {branch}` (fast-forward merge)
- ✅ Read-only: `git log`, `git status`, `git diff`, `git show`
- ✅ `git worktree remove` (after cd to main)

**❌ FORBIDDEN in Main Worktree**:
- ❌ `git cherry-pick` (multi-step, can leave conflicts)
- ❌ `git rebase` (multi-step, can leave conflicts)
- ❌ Conflict resolution (non-atomic, blocks all instances)
- ❌ `git reset` on main (can lose commits for all instances)
- ❌ `git commit` for new work (main should only receive merges)

**Correct Pattern**:
```bash
# 1. Stay in task worktree for all git operations
cd /workspace/tasks/{task}/code
git fetch /workspace/main refs/heads/main:refs/remotes/origin/main
git rebase origin/main  # Conflicts resolved HERE
./mvnw verify

# 2. Only touch main for atomic fast-forward merge
cd /workspace/main
git merge --ff-only {task-branch}
```

**Reference**: [task-protocol-operations.md § Main Worktree Safety Policy](../../docs/project/task-protocol-operations.md#main-worktree-safety-policy)

### Version Branch Protection

**NEVER**:
- ❌ Delete version branches
- ❌ Rewrite history of version branches
- ❌ Force push to version branches
- ❌ Use `--all` or `--branches` with history rewriting

**ALWAYS**:
- ✅ Move version branch pointer forward: `git branch -f v21 <commit>`
- ✅ Create new version branches: `git branch v22 <commit>`
- ✅ Target specific non-version branch
- ✅ Create backup before history operations

### Pre-Operation Checklist

Before ANY history-rewriting operation:

1. ✅ List all branches: `git branch -a`
2. ✅ Identify version branches: `git branch | grep -E "^  v[0-9]+"`
3. ✅ Verify command targets specific branch (not --all)
4. ✅ Create backup: `git branch backup-before-op-$(date +%Y%m%d-%H%M%S)`
5. ✅ Run validation: `validate-git-safety.sh`
6. ✅ Execute operation
7. ✅ Verify version branches unchanged
8. ✅ Cleanup backup

## Workflow Integration

### Safe History Rewrite Workflow

```markdown
1. ✅ Identify operation needed (filter-branch, rebase, etc.)
2. ✅ Invoke validate-git-safety skill
3. ✅ Skill checks for version branch impact
4. ✅ If SAFE: Proceed with operation
5. ✅ If UNSAFE: Modify command to target specific branch
6. ✅ Re-validate modified command
7. ✅ Execute when safe
```

## Output Format

Script returns JSON:

```json
{
  "status": "safe",
  "message": "Operation safe to execute",
  "command": "git filter-branch main",
  "protected_branches": ["v1", "v13", "v21"],
  "target_branches": ["main"],
  "affected_version_branches": [],
  "warnings": [],
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

**Or for dangerous operation**:

```json
{
  "status": "blocked",
  "message": "Operation would affect version branches",
  "command": "git filter-branch --all",
  "protected_branches": ["v1", "v13", "v21"],
  "target_branches": ["all"],
  "affected_version_branches": ["v1", "v13", "v21"],
  "error": "Cannot use --all with filter-branch (affects version branches)",
  "suggestion": "Target specific branch: git filter-branch main",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Related

- **CLAUDE.md § Git History Rewriting Safety**: Complete safety procedures
- **docs/project/git-workflow.md**: Git workflows and safety guidelines
- **git-squash skill**: Uses validation before squashing
- **git-rebase skill**: Uses validation before rebasing

## Troubleshooting

### Validation Blocks Safe Operation

```bash
# If validation incorrectly blocks:
# 1. Check command syntax
# 2. Verify target branch is not version branch
# 3. Remove --all or --branches flags
# 4. Specify exact branch name

# Example fix:
# ❌ BLOCKED: git filter-branch --all
# ✅ SAFE: git filter-branch main
```

### Version Branch Accidentally Modified

```bash
# If version branch history was modified:

# 1. Check reflog for original position
git reflog show v21

# 2. Reset to original commit
git branch -f v21 v21@{1}

# 3. Verify restored
git log v21 -5 --oneline
```

### Need to Update Version Branch

```bash
# To update version branch pointer (NOT rewrite history):

# ✅ CORRECT: Move pointer forward
git branch -f v21 main

# ❌ WRONG: Rewrite history
git filter-branch v21 ...
```

## Common Patterns

### Pattern 1: Safe Filter-Branch

```bash
# Always target specific branch
git filter-branch --tree-filter 'rm secrets.txt' main
# NOT: git filter-branch --tree-filter 'rm secrets.txt' --all
```

### Pattern 2: Version Branch Update

```bash
# Move pointer, don't rewrite
git branch -f v21 new-commit
# NOT: git reset --hard on v21 branch
```

### Pattern 3: Pre-Delete Validation

```bash
# Before deleting branches, check pattern
BRANCH="v21"
if [[ "$BRANCH" =~ ^v[0-9]+$ ]]; then
  echo "Cannot delete version branch"
  exit 1
fi
```

## Implementation Notes

The validate-git-safety script performs:

1. **Discovery Phase**
   - List all branches
   - Identify version branches (v[0-9]+)
   - Identify temporary branches

2. **Analysis Phase**
   - Parse command for dangerous flags
   - Extract target branches
   - Check for version branch impact

3. **Validation Phase**
   - Check if version branches affected
   - Validate target branch safety
   - Assess risk level (safe/warning/blocked)

4. **Reporting Phase**
   - Return status (safe/warning/blocked)
   - List affected version branches
   - Suggest safe alternatives if blocked
   - Provide remediation steps

5. **Enforcement Phase**
   - Block (exit 2) if dangerous
   - Warn (exit 0 + warning) if risky
   - Allow (exit 0) if safe
