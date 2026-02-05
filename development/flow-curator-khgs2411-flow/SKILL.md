---
name: flow-curator
description: Manage backlog and archive completed work. Use for backlog operations, archiving phases, or keeping active plan focused. Curates plan organization.
---

# Flow Curator

Manage backlog, archive completed work, and keep the active plan focused. This skill handles plan organization and hygiene through backlog management and archiving operations.

## When to Use This Skill

Activate when the user wants plan organization:
- "Move this to backlog"
- "Add to backlog"
- "Show backlog"
- "View backlog"
- "Pull from backlog"
- "Bring back from backlog"
- "Archive completed work"
- "Archive this phase"
- "Split the plan"
- "Clean up completed tasks"

## Curation Philosophy

**Keep Active Plan Focused**: Only show work that's relevant now. Defer future work to backlog, archive completed work to history.

**Three Storage Areas**:
- **Active Plan** (`.flow/phase-N/`): Current and near-future work
- **Backlog** (`.flow/backlog/`): Deferred tasks (scope creep, future ideas, blocked work)
- **Archive** (`.flow/archive/`): Completed phases (history, reference)

## Backlog Management

### When to Backlog

**Move tasks to backlog when**:
- Scope creep: "That's a good idea, but not for V1"
- Blocked: "Can't work on this until X is done"
- Priorities shifted: "Let's focus on Y first"
- Future enhancement: "Nice-to-have, but not essential"
- Too many active tasks: "Plan is getting cluttered"

**DON'T backlog**:
- Tasks already IN PROGRESS (complete or cancel them)
- Tasks already COMPLETE (archive instead)
- Core V1 features (adjust scope instead)

### Backlog Structure

**Backlog task file** (`.flow/backlog/task-M.md`):
```markdown
# Task M: [Name]

**Original Phase**: Phase [N]
**Backlogged**: [DATE]
**Reason**: [Why deferred - scope creep, blocked, priority shift, etc.]

**Status**: 🔮 BACKLOG

---

## Task Overview

**Purpose**: [Why this task exists]

**Dependencies**: [What it requires]

---

## Action Items / Iterations

[Original task content preserved]

---

## Notes

**When to Pull Back**:
- [Condition that would make this task relevant again]
- [Example: "When API v2 is stable", "After V1 launch", "If user feedback requests this"]
```

### Backlog Operations

#### Add to Backlog

**Command**: `/flow-backlog-add`

**Process**:
1. Verify task is ⏳ PENDING (not IN PROGRESS or COMPLETE)
2. Prompt: "Why are you backlogging this task?" (capture reason)
3. Move `phase-N/task-M.md` to `.flow/backlog/task-M.md`
4. Add metadata header (original phase, date, reason)
5. Update DASHBOARD.md:
   - Remove from phase progress overview
   - Add to "Backlog" section
6. Renumber remaining tasks in phase if needed
7. Report what was backlogged

#### View Backlog

**Command**: `/flow-backlog-view`

**Process**:
1. List all files in `.flow/backlog/`
2. For each task, extract:
   - Task name
   - Original phase
   - Date backlogged
   - Reason
3. Sort by date backlogged (oldest first)
4. Format as table:
   ```
   | Task | Original Phase | Backlogged | Reason |
   |------|----------------|------------|--------|
   | Task 5: Admin Dashboard | Phase 2 | 2025-10-15 | Scope creep - V2 feature |
   | Task 8: Performance Tuning | Phase 3 | 2025-10-22 | Priority shift - focus on features first |
   ```
5. Suggest: "Use `/flow-backlog-pull [task-name]` to restore"

#### Pull from Backlog

**Command**: `/flow-backlog-pull`

**Process**:
1. Show backlog tasks (call view logic)
2. Prompt: "Which task to pull back?"
3. Prompt: "Which phase to add it to?" (default: current phase)
4. Move `.flow/backlog/task-M.md` to target phase
5. Renumber as needed (task-M becomes task-K in phase-N)
6. Remove metadata header
7. Update DASHBOARD.md:
   - Add to target phase progress overview
   - Remove from backlog section
8. Report: "Task restored to Phase N. Ready to start when priorities allow."

## Archive Management

### When to Archive

**Archive completed phases when**:
- Phase complete and verified
- Focus shifted to new phases
- DASHBOARD getting too large
- Want to keep history but reduce clutter

**Archiving preserves**:
- All task files
- All completion dates
- All notes and decisions
- Phase summary and goals

### Archive Operations

#### Archive Phase (Plan Split)

**Command**: `/flow-plan-split`

**Purpose**: Move completed phases to archive, renumber active phases

**Process**:
1. List all ✅ COMPLETE phases
2. Confirm: "Archive Phase N: [Name]?"
3. Create backup in `.flow/.backups/`
4. Create `.flow/archive/` if doesn't exist
5. Move `phase-N/` to `.flow/archive/phase-N/`
6. Update DASHBOARD.md:
   - Move phase to "Archived Phases" section
   - Preserve completion date and summary
7. Renumber remaining active phases:
   - If phase-1 and phase-2 archived, phase-3 becomes phase-1
   - Update all DASHBOARD references
   - Update "Current Work" pointer if needed
8. Report:
   ```
   ✅ Archive Complete!

   Archived:
   - Phase 1: Foundation (Oct 15 - Oct 22)
   - Phase 2: Core Features (Oct 23 - Nov 05)

   Active Phases Renumbered:
   - Phase 3 → Phase 1: Testing & Polish
   - Phase 4 → Phase 2: Deployment

   Backup: .flow/.backups/2025-11-02-pre-split.zip

   Current work now: Phase 1 (formerly Phase 3), Task 2
   ```

### Archive Structure

**Archive directory**:
```
.flow/archive/
├── phase-1/
│   ├── task-1.md
│   ├── task-2.md
│   └── task-3.md
├── phase-2/
│   ├── task-1.md
│   └── task-2.md
└── ARCHIVE_INDEX.md
```

**ARCHIVE_INDEX.md** (auto-generated):
```markdown
# Archive Index

## Phase 1: Foundation ✅ COMPLETE
**Duration**: Oct 15 - Oct 22 (7 days)
**Goal**: Set up project structure
**Tasks**: 3/3 complete

### Deliverables
- Project structure defined
- Development framework established
- Initial documentation complete

---

## Phase 2: Core Features ✅ COMPLETE
**Duration**: Oct 23 - Nov 05 (13 days)
**Goal**: Implement core workflows
**Tasks**: 4/4 complete

### Deliverables
- User authentication working
- API endpoints functional
- Data persistence implemented
- Error handling in place
```

## Best Practices

**DO**:
- ✅ Backlog tasks before they clutter active plan
- ✅ Capture reason when backlogging (why deferred)
- ✅ Archive completed phases to maintain focus
- ✅ Create backups before plan-split
- ✅ Renumber phases/tasks after backlog/archive operations

**DON'T**:
- ❌ Backlog tasks that are IN PROGRESS (complete them first)
- ❌ Archive phases that aren't fully COMPLETE
- ❌ Lose context when backlogging (capture "when to pull back")
- ❌ Skip backups before destructive operations
- ❌ Forget to update DASHBOARD after backlog/archive

## Backlog vs Cancel vs Defer

**When to use each**:

**Backlog** (🔮 BACKLOG):
- Task is good idea, just not now
- Might come back later
- Actively manage in backlog
- Example: "Admin dashboard - defer to V2"

**Cancel** (❌ CANCELLED):
- Task no longer needed
- Won't come back
- Don't track anymore
- Example: "Duplicate of Task 5, cancelled"

**Defer** (🔮 DEFERRED):
- Iteration within task deferred
- Task continues, some work deferred
- Mark specific iterations
- Example: "Iteration 4: Optimizations - defer to V2"

## Examples

### Example 1: Moving Task to Backlog

```
User: "Let's move the Admin Dashboard task to backlog - it's not needed for V1"

AI Process:
1. Find "Admin Dashboard" task (Phase 2, Task 5)
2. Verify status is ⏳ PENDING (yes)
3. Prompt for reason

AI Response:
"Moving Task 5: Admin Dashboard to backlog.

**Task Details**:
- Current location: Phase 2, Task 5
- Status: ⏳ PENDING (not started)
- Purpose: Admin panel for user management

**Backlog Reason**: V1 scope reduction - admin features defer to V2

**What Happens**:
1. Move to .flow/backlog/task-5-admin-dashboard.md
2. Add metadata (original: Phase 2, reason: scope reduction)
3. Update DASHBOARD.md (remove from Phase 2)
4. Renumber remaining tasks (Task 6 becomes Task 5)

Proceed?"

User: "Yes"

AI Response:
"✅ Task backlogged!

**Backlog Summary**:
- Task 5: Admin Dashboard → .flow/backlog/
- Phase 2 now has 4 tasks (down from 5)
- Task 6 renumbered to Task 5
- Can restore later with `/flow-backlog-pull`"
```

### Example 2: Viewing Backlog

```
User: "Show me the backlog"

AI Process:
1. List files in .flow/backlog/
2. Extract metadata from each
3. Format as table

AI Response:
"## Backlog Contents

**Total Backlogged**: 3 tasks

| Task | Original Phase | Backlogged | Reason |
|------|----------------|------------|--------|
| Admin Dashboard | Phase 2 | 2025-10-15 | Scope reduction - V2 feature |
| Performance Tuning | Phase 3 | 2025-10-22 | Priority shift - focus on core features |
| Advanced Analytics | Phase 3 | 2025-10-28 | Blocked - need more data first |

**When to Pull Back**:
- Admin Dashboard: After V1 launch with user feedback
- Performance Tuning: After core features stable
- Advanced Analytics: When data collection implemented

Use `/flow-backlog-pull [task-name]` to restore any task."
```

### Example 3: Archiving Completed Phase

```
User: "Archive Phase 1 - it's been complete for weeks"

AI Process:
1. Verify Phase 1 is ✅ COMPLETE (yes)
2. Check all tasks complete (3/3 ✅)
3. Create backup before archiving

AI Response:
"Archiving Phase 1: Foundation

**Phase Summary**:
- Duration: Oct 15 - Oct 22 (7 days)
- Tasks: 3/3 complete
- Goal: Set up project structure ✅

**What Will Happen**:
1. Create backup: .flow/.backups/2025-11-02-pre-split.zip
2. Move phase-1/ → .flow/archive/phase-1/
3. Update DASHBOARD.md (move to Archived Phases)
4. Renumber remaining phases:
   - Phase 2 → Phase 1 (Core Features 🚧 IN PROGRESS)
   - Phase 3 → Phase 2 (Testing ⏳ PENDING)
5. Update current work pointer (Phase 2 Task 3 → Phase 1 Task 3)

**Benefit**: Active plan focuses on current work, DASHBOARD more concise

Proceed?"

User: "Yes"

AI Response:
"✅ Archive complete!

**Archived**:
- Phase 1: Foundation (7 days, 3 tasks) → .flow/archive/phase-1/

**Active Phases Renumbered**:
- Phase 2 → Phase 1: Core Features (currently Phase 1, Task 3)
- Phase 3 → Phase 2: Testing

**DASHBOARD Updated**:
- Current work: Phase 1, Task 3 (formerly Phase 2, Task 3)
- Active plan now 2 phases (down from 3)
- Backup available: .flow/.backups/2025-11-02-152030-pre-split.zip

Archive preserved all task files and notes for future reference."
```

### Example 4: Pulling Task from Backlog

```
User: "Priorities changed - let's pull back the Admin Dashboard task"

AI Process:
1. Find Admin Dashboard in backlog
2. Show task details
3. Prompt for target phase

AI Response:
"Pulling task from backlog: Admin Dashboard

**Original Info**:
- Backlogged: 2025-10-15
- Reason: Scope reduction - V2 feature
- Original Phase: Phase 2

**Current Phases**:
1. Phase 1: Core Features (4 tasks, 🚧 IN PROGRESS)
2. Phase 2: Testing (2 tasks, ⏳ PENDING)

Which phase should Admin Dashboard join?"

User: "Phase 2"

AI Process:
1. Move backlog/task-5-admin-dashboard.md → phase-2/task-3.md
2. Remove metadata header
3. Update DASHBOARD.md

AI Response:
"✅ Task restored from backlog!

**Restored Task**:
- Admin Dashboard → Phase 2, Task 3
- Removed backlog metadata
- Status: ⏳ PENDING (ready to start)

**Updated DASHBOARD**:
- Phase 2 now has 3 tasks (up from 2)
- Backlog now has 2 tasks (down from 3)

Use `/flow-task-start` when ready to begin work."
```

## Interaction with Other Flow Skills

**Planning Stage** (flow-planner Skill):
- Planner creates tasks
- Curator manages backlog

**Verify Stage** (flow-verifier Skill):
- Verifier checks plan health
- Curator maintains plan focus

**Curate Stage** (This Skill):
- Manage backlog ← YOU ARE HERE
- Archive completed work ← YOU ARE HERE

## References

- **Backlog Management**: DEVELOPMENT_FRAMEWORK.md (backlog patterns)
- **Archive Strategy**: DEVELOPMENT_FRAMEWORK.md (plan splitting)
- **Slash Commands**: `/flow-backlog-add`, `/flow-backlog-view`, `/flow-backlog-pull`, `/flow-plan-split`
