---
name: milestone-complete
description: "Update all core documentation files after completing a milestone. Use when marking any M#.#.# as COMPLETE. Ensures documentation stays synchronized. TRIGGER when the user says \"milestone done\", \"mark milestone complete\", \"finish milestone\", \"this is done\", \"wrap up this milestone\", \"close out milestone\", \"mark it complete\", or any indication that a milestone has been completed."
argument-hint: <PREFIX-#.#>
---

# Milestone Completion Documentation

**Milestone to complete**: $ARGUMENTS

## Step 0: Detect Identifier Format

Accepts both legacy M-format (`M7.7`, `M9.16`) and new OpenSpec change-ids (`architecture-compliance-sweep`). Normalize via:
```bash
bash .claude/skills/_shared/milestone-format.sh "$ARGUMENTS"
```

All subsequent references to the identifier use it as-is. File name patterns substitute `<identifier>` — e.g., `docs/next-prompt-M9.16.md` for legacy, or `docs/next-prompt-architecture-compliance-sweep.md` for new-style (if such per-milestone file exists — OpenSpec changes generally don't use per-milestone next-prompt files; the change directory under `openspec/changes/` is the source of truth).

## Current State

- Branch: !`git branch --show-current`
- Uncommitted changes: !`git status --short`

## Files to Update

### 1. `docs/current-story.md` (source of truth for status)
- Move milestone from Active to Recently Completed table
- Add actual hours spent
- Update "Last Updated" date to today
- Update priority queue (remove completed, add next)

### 2. Branch-specific next-prompt file
- If `docs/next-prompt-<identifier>.md` exists for this milestone, move it to `docs/archive/` (rename to `next-prompt-<identifier>.md` stays as-is — the archive path is sufficient historical marker) for reference, or delete it
- If the file contains guidance for other sub-tasks still in progress, only remove the completed section
- OpenSpec changes (new work) generally do not use per-milestone next-prompt files — the `openspec/changes/<change-id>/` directory holds the proposal/design/tasks, and archival happens via `/opsx:archive`. If completing an OpenSpec change, prefer `/opsx:archive <change-id>` after this skill runs.

### 3. `docs/next-prompt.md` (hub/index)
- **Remove** the pointer to the completed milestone from the Active Milestones section
- If there's a next milestone in the priority queue, add guidance for it (or note it as planned)

### 4. `docs/requirements.md`
- Mark related requirements as COMPLETE (only if new requirements were fulfilled)

### 5. `docs/project-index.md`
- Add milestone to completed section with key achievements
- Update recent activity section
- Verify all links are correct

### 6. `docs/insights-log.md`
Ask the user if there are any unlogged insights from this milestone. If yes, invoke `/log-insight` via an Agent (background) to handle it. This delegates to the canonical skill so format stays consistent.

### 7. `docs/development-journal.md`
Invoke `/dev-journal` via an Agent (background) to write the milestone completion narrative. Pass context: milestone completed, what was accomplished, key decisions. Include the **Retro** section (see below).

## Cleanup

- Update the branch-keyed status file to reflect completion (do not delete — the file is the record of what this branch *was*; deleting it causes the status line to fall back to branch-name parsing and lose the focus label):

```bash
bash .claude/skills/_shared/status-line.sh write "[<identifier>] COMPLETE — awaiting merge"
```

If the PR has merged and the branch has been deleted locally, the status file becomes orphaned (harmless) and can be removed at leisure. For active branches kept around post-merge, leave the status file in place.

## Retrospective (mandatory)

Add to the journal entry:

```markdown
**Retro**:
- Estimate vs actual: [Xh estimated, Yh actual]
- What surprised you: [unexpected complexity, discovery, or outcome]
- Process improvement: [what would help next time]
```

## Verification

After updating:
- [ ] `current-story.md` has milestone in Recently Completed table
- [ ] Branch-specific next-prompt file deleted (or cleaned up)
- [ ] Pointer removed from `docs/next-prompt.md` Active Milestones section
- [ ] Planning Accuracy table updated in current-story.md
- [ ] Actual hours recorded
- [ ] Journal has retro section
- [ ] Any unlogged insights captured
- [ ] OpenSpec change archived (if applicable)
