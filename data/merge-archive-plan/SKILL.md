---
name: merge-archive-plan
description: Archive completed implementation plans after PR merge. Use when a plan's implementation has been merged to main, or after plan-execute completes on main branch.
license: MIT
metadata:
  author: agent-kit
  version: "1.0.0"
---

# Merge and Archive Plan

Archive completed implementation plans with full metadata after successful merge to main.

## Purpose

Maintain a clean, organized plan history by:
- Moving completed plans to `docs/plans/archive/`
- Adding comprehensive archive metadata
- Preserving execution history and lessons learned
- Keeping active plans directory focused

## When to Use

- After a plan's implementation PR is merged to main
- When plan-execute completes successfully (with confirmation if on main)
- Manual cleanup of completed plans

## Trigger Behavior

### Automatic Invocation (from plan-execute)

If invoked automatically after plan-execute completes:

1. **Check current branch**
2. **If on feature branch/worktree:** Skip - wait for PR merge
3. **If on main branch:** Prompt user for confirmation

```
Plan execution complete on main branch.

Would you like to archive this plan now?
- The plan will be moved to docs/plans/archive/
- Archive metadata will be added

[Yes] [No, I'll do it later]
```

### Slash Command Invocation

If invoked via `/ak-merge-archive-plan`:
- Proceed directly without double-confirmation
- User explicitly requested archiving

## Archive Workflow

### Step 1: Identify the Plan

**If plan path provided:** Use directly.

**If no path:**
1. Check conversation context for recently executed plan
2. List completed plans in `docs/plans/`
3. Ask user which plan to archive

### Step 2: Verify Merge Status

Before archiving, verify the implementation is merged:

```bash
# Check if on main branch
git branch --show-current

# If on feature branch, check if merged to main
git log main --oneline | grep -q "{plan-related-commit}"
```

**If not merged:**
```
⚠️ Plan implementation doesn't appear to be merged to main yet.

Current branch: feature/0042_user-auth
Merge status: Not merged

Options:
1. Archive anyway (not recommended)
2. Wait for merge
3. Check a different plan

How would you like to proceed?
```

### Step 3: Gather Archive Metadata

Collect comprehensive information:

```bash
# Get PR information (if available)
gh pr list --state merged --search "{plan-name}" --json number,title,url,mergedAt

# Get commits from implementation
git log --oneline main~{N}..main --grep="{plan-name}"

# Get files changed
git diff --stat {first-commit}^..{last-commit}
```

### Step 4: Update Plan with Archive Header

**Use the Edit tool** to prepend the archive metadata block at the top of the plan file. Do NOT create a new file - edit the existing plan in place.

See [assets/archive-header-template.md](assets/archive-header-template.md) for the full template.

### Step 5: Move to Archive with git mv

**Use `git mv` to move the plan** - this preserves git history and stages the change in one step.

```bash
# Ensure archive directory exists
mkdir -p docs/plans/archive/

# Move the plan using git mv (preserves history)
git mv docs/plans/{NNNN}_{name}.md docs/plans/archive/

# Move any subplans
git mv docs/plans/{NNNN}A_*.md docs/plans/archive/ 2>/dev/null || true
git mv docs/plans/{NNNN}B_*.md docs/plans/archive/ 2>/dev/null || true
```

**Example:**
```bash
mkdir -p docs/plans/archive/
git mv docs/plans/0001_bootstrap.md docs/plans/archive/
```

### Step 6: Commit Archive

```bash
git add docs/plans/archive/{plan-files}
git add docs/plans/  # To capture the removal
git commit -m "docs(plans): archive {NNNN}_{name}

- Moved to docs/plans/archive/
- Added archive metadata
- PR: {PR URL}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 7: Report

```markdown
## Plan Archived: {plan-name}

**Status:** ✅ Archived successfully

| Detail | Value |
|--------|-------|
| Plan | `{NNNN}_{name}.md` |
| New Location | `docs/plans/archive/` |
| PR | [{PR title}]({URL}) |
| Commits | {N} |
| Files Changed | {N} |

Subplans also archived:
- `{NNNN}A_{subplan}.md`
- `{NNNN}B_{subplan}.md`
```

## Archive Directory Structure

```
docs/plans/
├── 0043_current-feature.md     # Active plans
├── 0044_upcoming-work.md
└── archive/                     # Completed plans
    ├── 0001_bootstrap.md
    ├── 0002_cli-core.md
    ├── 0040_old-feature.md
    ├── 0041_another-done.md
    └── 0042_user-auth.md
```

## Metadata Template

See [assets/archive-header-template.md](assets/archive-header-template.md) for the full archive header format.

## Edge Cases

### Plan with No PR

If implementation was done directly on main without a PR:

```markdown
## Archive Information

| Field | Value |
|-------|-------|
| Archived | {date} |
| PR | N/A (direct to main) |
| Commits | {N} commits |
```

### Partial Implementation

If plan was only partially completed:

```markdown
---
archived: true
archived_date: {date}
partial: true
---

## Archive Information

**Note:** This plan was partially implemented. See Lessons Learned for details.

### Completed
- Phase 1: Database Schema ✅
- Phase 2: API Endpoints ✅

### Not Completed
- Phase 3: Frontend (deferred to plan 0050)
- Phase 4: Integration Tests (covered by 0050)
```

### Abandoned Plan

For plans that were abandoned:

```markdown
---
archived: true
archived_date: {date}
status: ABANDONED
---

## Archive Information

**Status:** ABANDONED

**Reason:** {Why the plan was abandoned}

**Disposition:**
- Requirements changed
- Superseded by plan {NNNN}
- No longer needed
```

## Examples

### Example: Archive after PR merge

```
User: Archive the user-auth plan, the PR just merged

Claude: [Checks git status]
[Finds merged PR via gh cli]
[Gathers commit history]

Archiving plan 0042_user-auth...

[Updates plan with archive header]
[Moves to docs/plans/archive/]
[Commits changes]

## Plan Archived: 0042_user-auth

✅ Archived successfully

| Detail | Value |
|--------|-------|
| Plan | `0042_user-auth.md` |
| PR | [feat: add user authentication](#123) |
| Commits | 8 |
| Files Changed | 12 |
```

### Example: Auto-invocation on main

```
[plan-execute completes on main branch]

Claude: Plan execution complete on main branch.

Would you like to archive this plan now?
- The plan will be moved to docs/plans/archive/
- Archive metadata will be added

User: Yes

Claude: [Proceeds with archiving]
```

## Related Skills

- `plan-execute` - May invoke this skill after completion
- `create-plan` - Creates plans this skill archives
- `review-plan` - Reviews plans before execution
