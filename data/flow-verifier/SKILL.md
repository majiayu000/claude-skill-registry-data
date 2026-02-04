---
name: flow-verifier
description: Verify plan consistency, generate summaries, maintain plan health. Use for review, verification, summaries, or plan maintenance. Mostly read-only with maintenance operations.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Flow Verifier

Verify plan consistency, generate summaries, and maintain plan health. This skill combines read-only inspection (verify, review) with maintenance operations (summarize, compact, rollback).

## When to Use This Skill

Activate when the user wants verification:
- "Review the plan"
- "Verify the status"
- "Check if we're done"
- "Is the implementation complete?"
- "Validate the structure"
- "Are there any issues?"
- "Check for inconsistencies"
- "Verify all tasks are tracked"

## Review Philosophy

**Read-Only Inspection**: This Skill observes and reports, never modifies.

**What We Check**:
- Status markers match actual state
- No phantom tasks (DASHBOARD promises what doesn't exist)
- Brainstorming complete before implementation starts
- Task structure follows Flow rules
- Action items are all checked off when complete
- File references are valid

**Tools Available**: `Read`, `Grep`, `Glob` (read-only tools only)

## Review Checklist

### 1. Status Marker Consistency

**Check**: Do status markers reflect actual state?

**How to verify**:
```bash
# Find all IN PROGRESS items
grep -r "🚧 IN PROGRESS" .flow/

# Find all COMPLETE items
grep -r "✅ COMPLETE" .flow/

# Find all PENDING items
grep -r "⏳ PENDING" .flow/
```

**Common issues**:
- Task marked 🚧 IN PROGRESS but all iterations are ✅ COMPLETE
- Iteration marked ⏳ PENDING but has implementation section
- Multiple items marked 🚧 IN PROGRESS (should only be one active)

**Example problem**:
```markdown
### 🚧 Iteration 2: Error Handling

**Status**: ✅ COMPLETE (2025-10-30)  ← MISMATCH!
```

**Report**:
```
❌ Status Marker Mismatch
- Iteration 2 header shows 🚧 IN PROGRESS
- Implementation section shows ✅ COMPLETE
- Action: Update header to match implementation status
```

### 2. Phantom Task Detection

**Check**: Does every task listed in DASHBOARD.md have a corresponding file?

**How to verify**:
```bash
# List all tasks mentioned in DASHBOARD
grep "Task [0-9]" .flow/DASHBOARD.md

# Check if task files exist
ls .flow/phase-*/task-*.md
```

**Common issues**:
- DASHBOARD lists "Task 5" but `.flow/phase-2/task-5.md` doesn't exist
- Task file references non-existent iterations

**Example problem**:
```markdown
DASHBOARD.md:
- 🚧 **Task 3**: API Integration (2/4 iterations)

But: .flow/phase-2/task-3.md doesn't exist
```

**Report**:
```
❌ Phantom Task Detected
- DASHBOARD.md references Task 3: API Integration
- File .flow/phase-2/task-3.md does not exist
- Action: Create task file or remove from DASHBOARD
```

### 3. Implementation Gate Verification

**Check**: Is implementation starting before brainstorming is complete?

**How to verify**:
```bash
# Check if iteration has brainstorming
grep -A 20 "## Brainstorming" task-file.md

# Check brainstorming status
grep "Brainstorming.*Status.*COMPLETE" task-file.md

# Check if implementation started
grep "## Implementation" task-file.md
```

**Gate Rule**: If iteration has brainstorming, it must be ✅ COMPLETE before implementation starts.

**Example problem**:
```markdown
## Brainstorming
**Status**: 🚧 IN PROGRESS

## Implementation
**Status**: 🚧 IN PROGRESS  ← GATE VIOLATION!
```

**Report**:
```
❌ Implementation Gate Violation
- Iteration 2 has brainstorming IN PROGRESS
- Implementation section already started
- Action: Complete brainstorming before implementing
```

### 4. Task Structure Validation

**Check**: Does task follow the Golden Rule (Standalone XOR Iterations)?

**Golden Rule**: Tasks have EITHER:
- Direct action items (standalone task)
- OR iterations with action items in each iteration
- NEVER both

**How to verify**:
```bash
# Check if task has direct action items
grep -A 5 "## Action Items" task-file.md

# Check if task has iterations
grep "### " task-file.md | grep "Iteration"
```

**Example problem**:
```markdown
# Task 3: API Integration

## Action Items
- [ ] Create StripeClient
- [ ] Add error handling

## Iterations

### Iteration 1: Setup
...
```

**Report**:
```
❌ Task Structure Violation (Golden Rule)
- Task 3 has both direct action items AND iterations
- Golden Rule: Tasks must be EITHER standalone OR have iterations, never both
- Action: Move action items into iterations or remove iterations
```

### 5. Action Item Completion Check

**Check**: Are all action items checked off when iteration is marked complete?

**How to verify**:
```bash
# Find iteration marked COMPLETE
grep -B 2 "Status.*COMPLETE" task-file.md

# Check for unchecked action items in that iteration
grep -A 30 "### ✅ Iteration" task-file.md | grep "\[ \]"
```

**Example problem**:
```markdown
### ✅ Iteration 2: Error Handling
**Status**: ✅ COMPLETE

#### Action Items
- [x] Create ErrorMapper
- [ ] Add tests  ← UNCHECKED!
- [x] Integrate with client
```

**Report**:
```
❌ Incomplete Action Items
- Iteration 2 marked ✅ COMPLETE
- But action item "Add tests" is unchecked
- Action: Either complete the item or mark iteration as IN PROGRESS
```

### 6. File Reference Validation

**Check**: Do all file references point to existing files?

**How to verify**:
```bash
# Find file references in task files
grep -r "\`.*\.ts\`" .flow/ | grep -v "example"

# Check if referenced files exist
ls path/to/file.ts
```

**Example problem**:
```markdown
**Files Modified**:
- src/payment/StripeClient.ts
- src/payment/DoesNotExist.ts  ← FILE DOESN'T EXIST!
```

**Report**:
```
⚠️ Invalid File Reference
- Iteration 2 references src/payment/DoesNotExist.ts
- File does not exist in repository
- Action: Verify file path or remove invalid reference
```

## Status Markers Reference

### Valid Status Markers

**Task/Iteration Status**:
- ✅ `COMPLETE` - Work finished and verified
- 🚧 `IN PROGRESS` - Currently working on this
- ⏳ `PENDING` - Not started yet
- 🎨 `READY` - Ready to implement (brainstorming complete)
- ❌ `CANCELLED` - Work abandoned
- 🔮 `DEFERRED` - Moved to future version

**Phase Status**:
- ✅ `COMPLETE` - All tasks in phase done
- 🚧 `IN PROGRESS` - Currently working in this phase
- ⏳ `PENDING` - Phase not started

### Status Marker Lifecycle

**Iteration Lifecycle**:
```
⏳ PENDING
  ↓ (brainstorming started)
🚧 IN PROGRESS (brainstorming)
  ↓ (brainstorming complete, ready to implement)
🎨 READY
  ↓ (/flow-implement-start)
🚧 IN PROGRESS (implementing)
  ↓ (/flow-implement-complete)
✅ COMPLETE
```

**Common Mistakes**:
- ❌ Skipping 🎨 READY (going from brainstorming to implementation without marking ready)
- ❌ Multiple items marked 🚧 IN PROGRESS (should only be one active)
- ❌ Marking ✅ COMPLETE with unchecked action items
- ❌ Using ⏳ PENDING after implementation started

## Common Review Patterns

### Pattern 1: Full Plan Review

**When**: User asks "review the entire plan"

**Steps**:
1. Read DASHBOARD.md to understand structure
2. For each phase:
   - Verify phase status matches task statuses
   - Check all tasks listed have files
3. For each task:
   - Verify task status matches iteration statuses
   - Check structure (standalone XOR iterations)
4. For each iteration:
   - Verify status marker consistency
   - Check action items if marked complete
5. Report all findings

**Output format**:
```markdown
## Plan Review Results

**Summary**: 15 items checked, 2 issues found

### ✅ Passing Checks (13)
- All phase statuses consistent
- No phantom tasks detected
- Task structure valid
- ...

### ❌ Issues Found (2)

#### Issue 1: Status Marker Mismatch
- **Location**: Phase 2, Task 3, Iteration 2
- **Problem**: Header shows 🚧 but implementation shows ✅
- **Action**: Update header to ✅ COMPLETE

#### Issue 2: Unchecked Action Items
- **Location**: Phase 2, Task 4, Iteration 1
- **Problem**: Iteration marked complete but 1 action item unchecked
- **Action**: Complete action item or mark iteration IN PROGRESS
```

### Pattern 2: Task-Specific Review

**When**: User asks "review Task 3"

**Steps**:
1. Read task file
2. Check task status consistency
3. Verify structure (standalone XOR iterations)
4. For each iteration:
   - Status marker consistency
   - Action item completion
   - Implementation gate (brainstorming before implementation)
5. Report findings

### Pattern 3: Status Audit

**When**: User asks "check all status markers"

**Steps**:
1. Grep for all status markers
2. For each marker:
   - Verify it's in valid lifecycle position
   - Check consistency with surrounding content
3. Check for multiple IN PROGRESS items (should be max 1)
4. Report findings

## Review Commands

### Check for Phantom Tasks

```bash
# List tasks from DASHBOARD
grep -E "Task [0-9]" .flow/DASHBOARD.md

# List actual task files
ls .flow/phase-*/task-*.md

# Compare (manual check)
```

### Find Incomplete Work

```bash
# Find all IN PROGRESS items
grep -r "🚧 IN PROGRESS" .flow/

# Find unchecked action items
grep -r "\[ \]" .flow/phase-*/*.md
```

### Verify Implementation Gates

```bash
# Find iterations with brainstorming
grep -r "## Brainstorming" .flow/phase-*/

# Check if brainstorming is complete
grep -A 2 "## Brainstorming" .flow/phase-*/*.md | grep "Status"
```

### Validate Task Structure

```bash
# Check for direct action items in tasks
grep -A 5 "## Action Items" .flow/phase-*/task-*.md

# Check for iterations
grep "### " .flow/phase-*/task-*.md | grep -i iteration
```

## Summary Generation

**Command**: `/flow-summarize`

**Purpose**: Generate comprehensive summary of project status

### When to Summarize

- Project milestone reached
- Preparing status report
- End of sprint/phase
- Before stakeholder meeting
- User asks "summarize the project"

### Summary Template

```markdown
# Project Summary

**Generated**: [DATE]
**Project**: [PROJECT_NAME from PLAN.md]
**Version**: [VERSION from PLAN.md]

## Overview

**Goal**: [Project goal from PLAN.md]
**Status**: [Overall status - % complete]
**Current Work**: Phase [N], Task [M], Iteration [K]

## Phase Progress

### Phase 1: [Name] ✅ COMPLETE
**Duration**: [Start date] - [End date]
**Goal**: [Phase goal]
**Completed Tasks**: [X/X]

Key deliverables:
- [Task 1: Name] - [Brief outcome]
- [Task 2: Name] - [Brief outcome]

### Phase 2: [Name] 🚧 IN PROGRESS
**Duration**: [Start date] - present
**Goal**: [Phase goal]
**Completed Tasks**: [X/Y]

Completed:
- [Task 1: Name] - [Brief outcome]

In Progress:
- [Task 2: Name] - [Current iteration]

Pending:
- [Task 3: Name] - [Purpose]

## Key Decisions

[Extract from PLAN.md Key Decisions section]

## Next Steps

1. [Immediate next action]
2. [Upcoming milestone]
3. [Blockers if any]
```

### Summary Generation Process

1. Read DASHBOARD.md for current status
2. Read all task files for completion details
3. Read PLAN.md for project context
4. Generate summary using template
5. Return formatted markdown

## Plan Maintenance

### Compact Operation

**Command**: `/flow-compact`

**Purpose**: Remove clutter from old completed work

**When to Compact**:
- DASHBOARD.md getting too large (>500 lines)
- Many completed iterations with excessive notes
- Old completed phases cluttering active plan

**What Gets Compacted**:
- Completed iterations older than 30 days:
  - Remove implementation notes (keep summary)
  - Remove detailed action items (keep count)
  - Keep completion date and key outcomes
- Completed phases:
  - Collapse task details (keep titles and status)
  - Keep phase summary and goals achieved

**What's Preserved**:
- All status markers
- Completion dates
- Task/iteration names
- Key outcomes
- Current work (last 30 days)

**Process**:
1. Create backup in `.flow/.backups/`
2. Identify items to compact
3. Remove excessive detail
4. Verify plan still valid
5. Report what was compacted

### Rollback Operation

**Command**: `/flow-rollback`

**Purpose**: Undo last change if something went wrong

**When to Rollback**:
- Accidental deletion of important content
- Bad compact operation
- Incorrect status updates
- User regrets last change

**Rollback Process**:
1. List available backups in `.flow/.backups/`
2. Show timestamp and change description
3. User selects backup to restore
4. Restore selected files
5. Report what was rolled back

**Backup Strategy**:
- Auto-backup before compact
- Auto-backup before plan-split
- Keep last 10 backups
- Backups include timestamp and change type

## Interaction with Other Flow Skills

**Planning Stage** (flow-planner Skill):
- Planner creates structure
- Verifier validates structure

**Implementation Stage** (flow-builder Skill):
- Builder executes work
- Verifier checks completion

**Design Stage** (flow-designer Skill):
- Designer documents decisions
- Verifier checks references are valid

**Verify Stage** (This Skill):
- Inspect plan consistency ← YOU ARE HERE
- Generate summaries ← YOU ARE HERE
- Maintain plan health ← YOU ARE HERE

## Reporting Guidelines

### Report Format

**Use this structure for review findings**:

```markdown
## Review Results

**Scope**: [What was reviewed]
**Date**: [Review date]
**Status**: [✅ All Clear | ⚠️ Issues Found]

### Summary
- X checks performed
- Y issues found
- Z warnings

### ✅ Passing Checks
- [List what's working correctly]

### ❌ Issues Found
- [List problems discovered]

### ⚠️ Warnings
- [List potential concerns]

### 📋 Recommendations
- [Suggested actions to fix issues]
```

### Severity Levels

**❌ Critical**: Must fix before proceeding
- Phantom tasks (DASHBOARD promises don't exist)
- Implementation started before brainstorming complete
- Task structure violates Golden Rule

**⚠️ Warning**: Should fix soon
- Status marker inconsistency (cosmetic)
- Unchecked action items with work complete
- Minor file reference issues

**ℹ️ Info**: Nice to fix
- Formatting inconsistencies
- Missing optional documentation

## Examples

### Example 1: Full Plan Review

```
User: "Review the entire plan"

AI Process:
1. Read DASHBOARD.md to understand structure (3 phases, 8 tasks total)
2. Check each phase for status consistency
3. Verify all task files exist
4. Check task structure (standalone XOR iterations)
5. Verify status markers match implementation
6. Check action item completion

AI Response:
"## Plan Review Results

**Summary**: 15 checks performed, 2 issues found

### ✅ Passing Checks (13)
- All phase statuses consistent with task statuses
- No phantom tasks detected (all DASHBOARD tasks have files)
- Task structure valid (no mixing of action items and iterations)
- All completed iterations have checked action items
- File references valid

### ❌ Issues Found (2)

#### Issue 1: Status Marker Mismatch
- **Location**: Phase 2, Task 3, Iteration 2
- **Problem**: Header shows 🚧 IN PROGRESS but status line shows ✅ COMPLETE (2025-10-30)
- **Severity**: ⚠️ Warning (cosmetic issue)
- **Action**: Update header to `### ✅ Iteration 2: Error Handling`

#### Issue 2: Implementation Gate Violation
- **Location**: Phase 2, Task 4, Iteration 1
- **Problem**: Brainstorming status is 🚧 IN PROGRESS but Implementation section exists
- **Severity**: ❌ Critical (violates gate rule)
- **Action**: Complete brainstorming before continuing implementation"
```

### Example 2: Generating Summary

```
User: "Summarize the project status"

AI Process:
1. Read DASHBOARD.md for current work and progress
2. Read PLAN.md for project context
3. Read all task files for completion details
4. Generate formatted summary

AI Response:
"# Project Summary

**Generated**: 2025-11-02
**Project**: Flow Framework Agent Skills
**Version**: 1.0.0

## Overview

**Goal**: Refactor 8 workflow stage-based agent skills from 28 slash commands
**Status**: 57% complete (4/7 iterations in current task)
**Current Work**: Phase 3, Task 4, Iteration 5

## Phase Progress

### Phase 1: Foundation ✅ COMPLETE
**Duration**: Oct 15 - Oct 22
**Goal**: Set up project structure
**Completed Tasks**: 2/2

Key deliverables:
- Task 1: Project Setup - Framework structure established
- Task 2: Documentation - Architecture spec complete

### Phase 2: Initial Skills 🚧 IN PROGRESS
**Duration**: Oct 23 - present
**Goal**: Build core workflow skills
**Completed Tasks**: 2/4

Completed:
- Task 1: flow-initializer - Project initialization complete
- Task 2: flow-planner - Planning workflows done

In Progress:
- Task 4: Stage-Based Skills - Building flow-designer + flow-builder (Iteration 5 of 7)

Pending:
- Task 5: Verification Skills - Not started

## Key Decisions

- Progressive disclosure strategy: SKILL.md (400-500 lines) + supporting files
- 8 workflow stage-based skills absorb all 28 commands
- Dashboard-first navigation pattern throughout

## Next Steps

1. Complete Iteration 5 (flow-completer + flow-navigator)
2. Begin Iteration 6 (flow-verifier + flow-curator)
3. Final verification and integration testing"
```

### Example 3: Compact Operation

```
User: "The DASHBOARD is getting too long, can you clean it up?"

AI Process:
1. Read DASHBOARD.md (780 lines)
2. Identify completed items older than 30 days (Phase 1 completed Oct 22)
3. Create backup before compacting

AI Response:
"I'll compact old completed work to reduce clutter.

**Before Compacting**:
- Created backup: .flow/.backups/2025-11-02-143022-pre-compact.zip
- Current DASHBOARD.md: 780 lines
- Identified items to compact: Phase 1 (completed 11 days ago)

**What Will Be Compacted**:
- Phase 1, Task 1: Remove 45 lines of implementation notes (keep summary)
- Phase 1, Task 2: Remove 38 lines of detailed action items (keep count)
- Preserve all status markers and completion dates

**After Compacting**:
- New DASHBOARD.md: ~520 lines (33% reduction)
- All important info preserved
- Backup available for rollback if needed

Proceed with compact operation?"
```

### Example 4: Rollback Operation

```
User: "Oh no, I accidentally deleted important content. Can you undo that?"

AI Process:
1. List backups in .flow/.backups/
2. Show recent backups with timestamps

AI Response:
"Available backups:

1. 2025-11-02 14:30:22 - Pre-compact (DASHBOARD.md, 780 lines)
2. 2025-11-01 16:45:10 - Pre-plan-split (3 phase files archived)
3. 2025-10-31 09:20:15 - Manual backup (full project)

Which backup would you like to restore?

User: "Restore backup 1"

AI Process:
1. Restore DASHBOARD.md from backup 1
2. Verify restored file
3. Report what was rolled back

AI Response:
"✅ Rollback complete!

**Restored**:
- .flow/DASHBOARD.md (from 2025-11-02 14:30:22 backup)
- File size: 780 lines
- All content restored to pre-compact state

**What Changed**:
- Phase 1 details restored (83 lines of implementation notes)
- Detailed action items restored
- Current file backed up to .flow/.backups/2025-11-02-145530-pre-rollback.zip (just in case)

Your content is back!"
```

## References

- **Status Markers**: DEVELOPMENT_FRAMEWORK.md lines 1872-1968
- **Task Structure Rules**: DEVELOPMENT_FRAMEWORK.md lines 238-566
- **Implementation Gates**: DEVELOPMENT_FRAMEWORK.md lines 1798-1836
- **Slash Commands**: `/flow-verify-plan`, `/flow-summarize`, `/flow-compact`, `/flow-rollback`

## Key Reminders

**Before reviewing**:
- [ ] Understand what user wants reviewed (full plan, specific task, status audit)
- [ ] Use read-only tools (Grep, Read, Glob)
- [ ] Never modify files during review

**During review**:
- [ ] Check status marker consistency
- [ ] Verify no phantom tasks
- [ ] Validate implementation gates
- [ ] Check task structure (Golden Rule)
- [ ] Verify action item completion

**After review**:
- [ ] Report findings in structured format
- [ ] Prioritize issues by severity
- [ ] Suggest specific actions to fix
- [ ] Don't modify files - let user or other Skills handle fixes
