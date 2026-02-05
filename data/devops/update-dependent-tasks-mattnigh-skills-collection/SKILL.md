---
name: update-dependent-tasks
description: Automatically unblock tasks when dependencies are satisfied
allowed-tools: Bash, Read, Edit
---

# Update Dependent Tasks Skill

**Purpose**: Automatically update BLOCKED tasks to READY when all their dependencies are satisfied, preventing tasks from remaining unnecessarily blocked.

**Performance**: Automates dependency management, prevents stale BLOCKED tasks, improves workflow visibility

## When to Use This Skill

### ✅ Use update-dependent-tasks When:

- After completing and archiving a task
- After updating changelog.md with completed task
- In COMPLETE → CLEANUP transition
- Want to unblock dependent tasks automatically

### ❌ Do NOT Use When:

- Task not yet completed
- Task not yet in changelog.md
- No tasks have dependencies
- Not using dependency tracking in todo.md

## What This Skill Does

### 1. Finds BLOCKED Tasks

```bash
# Searches todo.md for:
- [ ] **BLOCKED:** `task-name`
  - **Dependencies**: A0, A1, A2
```

### 2. Checks Dependencies

```bash
# For each dependency:
- Checks if dependency in changelog.md
- If in changelog: Dependency satisfied ✅
- If not in changelog: Dependency pending ❌
```

### 3. Updates Task Status

```bash
# If ALL dependencies satisfied:
BEFORE: - [ ] **BLOCKED:** `task-name`
AFTER:  - [ ] **READY:** `task-name`
```

### 4. Updates Dependency List

```bash
# Marks which dependencies complete:
BEFORE: - **Dependencies**: A0, A1, A2
AFTER:  - **Dependencies**: A0 ✅ COMPLETE, A1 ✅ COMPLETE, A2 ✅ COMPLETE
```

### 5. Reports Changes

```markdown
## Dependency Update Results

### Unblocked Tasks:
- `implement-line-length-formatter` (dependencies: A0 ✅, A1 ✅)
- `implement-import-organization` (dependencies: A0 ✅, A1 ✅)

### Still Blocked Tasks:
- `implement-advanced-formatter` (waiting for: A3)
```

## Usage

### Basic Update

```bash
# After completing task A1
COMPLETED_TASK="implement-index-overlay-parser"

/workspace/main/.claude/scripts/update-dependent-tasks.sh \
  --completed-task "$COMPLETED_TASK"
```

### Update All Dependencies

```bash
# Check all BLOCKED tasks, update any now ready
/workspace/main/.claude/scripts/update-dependent-tasks.sh \
  --check-all true
```

## Dependency Tracking Format

### Todo.md Entry Format

```markdown
- [ ] **BLOCKED:** `implement-line-length-formatter`
  - **Dependencies**: A0 (styler-formatter-api module), A1 (parser for AST)
  - **Description**: Format line length according to rules
```

**Components**:
- **Status**: `BLOCKED` (will change to `READY` when satisfied)
- **Task name**: Backtick-wrapped identifier
- **Dependencies**: Comma-separated list of task identifiers
- **Description**: Optional task description

### Dependency Specification

```markdown
Dependencies: A0, A1, A2
Dependencies: implement-api, implement-tests
Dependencies: A0 (module setup), A1 (parser core)
```

**Formats**:
- Short identifiers: `A0, A1, A2`
- Full task names: `implement-api, implement-tests`
- With descriptions: `A0 (module setup), A1 (parser core)`

## Workflow Integration

### Complete → Cleanup Flow

```markdown
COMPLETE state
  ↓
Merge task to main
  ↓
Update todo.md (mark complete)
  ↓
Update changelog.md (add entry)
  ↓
[update-dependent-tasks skill] ← THIS SKILL
  ↓
Find BLOCKED tasks
  ↓
Check if dependencies satisfied
  ↓
Update BLOCKED → READY if satisfied
  ↓
Commit updated todo.md
  ↓
Continue with cleanup
```

## Example Scenario

### Initial State

**todo.md**:
```markdown
- [ ] **BLOCKED:** `implement-line-length-formatter`
  - **Dependencies**: A0 (styler-formatter-api module), A1 (parser for AST)
  - **Description**: Format line length according to rules

- [ ] **BLOCKED:** `implement-import-organization`
  - **Dependencies**: A0 (styler-formatter-api module), A1 (parser for AST)
  - **Description**: Organize imports according to rules

- [ ] **BLOCKED:** `implement-advanced-formatter`
  - **Dependencies**: A1 (parser for AST), A3 (semantic analyzer)
  - **Description**: Advanced formatting with semantic analysis
```

**changelog.md**:
```markdown
## [2025-11-01] - A0-styler-formatter-api
- Created formatter API module
- Defined FormattingRule interface

## [2025-11-10] - A1-implement-index-overlay-parser
- Implemented parser with index overlay
- Added AST generation
```

### After Running Skill

**Completed Task**: A1 (implement-index-overlay-parser)

**Analysis**:
1. `implement-line-length-formatter`: Needs A0 ✅, A1 ✅ → UNBLOCK
2. `implement-import-organization`: Needs A0 ✅, A1 ✅ → UNBLOCK
3. `implement-advanced-formatter`: Needs A1 ✅, A3 ❌ → STAY BLOCKED

**Updated todo.md**:
```markdown
- [ ] **READY:** `implement-line-length-formatter`
  - **Dependencies**: A0 ✅ COMPLETE, A1 ✅ COMPLETE
  - **Description**: Format line length according to rules

- [ ] **READY:** `implement-import-organization`
  - **Dependencies**: A0 ✅ COMPLETE, A1 ✅ COMPLETE
  - **Description**: Organize imports according to rules

- [ ] **BLOCKED:** `implement-advanced-formatter`
  - **Dependencies**: A1 ✅ COMPLETE, A3 (semantic analyzer)
  - **Description**: Advanced formatting with semantic analysis
```

**Report**:
```
=== DEPENDENCY UPDATE RESULTS ===

Unblocked Tasks: 2
- implement-line-length-formatter (A0, A1 complete)
- implement-import-organization (A0, A1 complete)

Still Blocked Tasks: 1
- implement-advanced-formatter (waiting for: A3)

Updated todo.md with changes.
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "Dependent tasks updated successfully",
  "completed_task": "A1-implement-index-overlay-parser",
  "checked_tasks": 3,
  "unblocked_tasks": [
    {
      "task_name": "implement-line-length-formatter",
      "dependencies": ["A0", "A1"],
      "all_satisfied": true,
      "new_status": "READY"
    },
    {
      "task_name": "implement-import-organization",
      "dependencies": ["A0", "A1"],
      "all_satisfied": true,
      "new_status": "READY"
    }
  ],
  "still_blocked_tasks": [
    {
      "task_name": "implement-advanced-formatter",
      "dependencies": ["A1", "A3"],
      "satisfied": ["A1"],
      "pending": ["A3"],
      "status": "BLOCKED"
    }
  ],
  "todo_md_updated": true,
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Safety Features

### Validation

- ✅ Verifies todo.md exists and readable
- ✅ Validates changelog.md exists
- ✅ Checks dependency format correct
- ✅ Confirms all dependencies specified

### Conservative Updates

- ✅ Only updates when ALL dependencies satisfied
- ✅ Preserves task order in todo.md
- ✅ Maintains task descriptions
- ✅ Keeps formatting intact

### Atomic Changes

- ✅ Edits todo.md atomically
- ✅ Commits changes separately
- ✅ Rollback on error
- ✅ Preserves backup if update fails

## Related Skills

- **archive-task**: Adds task to changelog (prerequisite)
- **task-cleanup**: Runs after dependency updates

## Troubleshooting

### Error: "Dependency not found in changelog"

```bash
# Dependency listed but not in changelog.md
# Possible causes:
1. Task completed but not archived
2. Dependency identifier mismatch
3. Changelog.md not up to date

# Fix:
1. Check if task actually complete
2. Verify dependency identifier matches changelog entry
3. Run archive-task if missing
```

### Error: "Invalid dependency format"

```bash
# Dependency list format incorrect
# Expected: "Dependencies: A0, A1, A2"
# Found: "Depends on: A0 and A1"

# Fix: Update todo.md to use standard format
- **Dependencies**: A0, A1, A2
```

### Task Not Unblocked

```bash
# Task expected to unblock but didn't
# Check:
1. All dependencies in changelog?
   grep "A0\|A1\|A2" changelog.md

2. Dependency list complete?
   grep -A 2 "BLOCKED.*task-name" todo.md

3. Task status correct?
   grep "task-name" todo.md

# If all dependencies satisfied, manually update:
sed -i 's/BLOCKED:/READY:/' todo.md
```

## Common Patterns

### Pattern 1: Linear Dependencies

```markdown
A0 → A1 → A2 → A3

After A1 completes:
- A2 unblocked (depends only on A1)
- A3 remains blocked (depends on A2)
```

### Pattern 2: Fan-Out Dependencies

```markdown
      A0
    /  |  \
  B1  B2  B3

After A0 completes:
- B1, B2, B3 all unblocked (all depend only on A0)
```

### Pattern 3: Fan-In Dependencies

```markdown
  A1   A2   A3
    \  |  /
      B0

After A1 and A2 complete:
- B0 remains blocked (still waiting for A3)

After A3 completes:
- B0 unblocked (all dependencies satisfied)
```

### Pattern 4: Diamond Dependencies

```markdown
      A0
     /  \
   A1    A2
     \  /
      B0

After A0 completes:
- A1, A2 unblocked

After A1 completes:
- B0 remains blocked (waiting for A2)

After A2 completes:
- B0 unblocked (both A1 and A2 complete)
```

## Best Practices

### Clear Dependency Identifiers

```markdown
✅ GOOD: Unique, consistent
- Dependencies: A0, A1, A2
- Dependencies: implement-api, implement-tests

❌ BAD: Ambiguous, inconsistent
- Dependencies: the API thing, parser
```

### Minimal Dependencies

```markdown
✅ GOOD: Only true dependencies
Dependencies: A0 (API interface needed)

❌ BAD: Nice-to-have
Dependencies: A0 (API), B5 (would be nice to have)
```

### Keep Dependencies Updated

```bash
# After completing task, check for dependents
./update-dependent-tasks.sh --check-all

# After updating todo.md structure, verify dependencies
grep -A 2 "BLOCKED:" todo.md
```

## Implementation Notes

The update-dependent-tasks script performs:

1. **Discovery Phase**
   - Read todo.md
   - Find all BLOCKED tasks
   - Extract dependency lists
   - Parse dependency identifiers

2. **Validation Phase**
   - Read changelog.md
   - Extract completed task identifiers
   - Build set of satisfied dependencies

3. **Analysis Phase**
   - For each BLOCKED task:
     - Get dependency list
     - Check each dependency against changelog
     - Determine if all satisfied

4. **Update Phase**
   - For tasks with all dependencies satisfied:
     - Update BLOCKED → READY
     - Mark dependencies as ✅ COMPLETE
     - Preserve task structure

5. **Commit Phase**
   - Write updated todo.md
   - Verify changes applied
   - Commit changes
   - Report results

6. **Reporting Phase**
   - List unblocked tasks
   - List still-blocked tasks
   - Show pending dependencies
   - Return JSON summary
