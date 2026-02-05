---
name: sdd-modify
description: Apply spec modifications systematically. Use to apply review feedback, bulk modifications, or interactive spec updates with safety checks, validation, and rollback support.
---

# Spec-Driven Development: Modify Skill

## When to Use This Skill

Use `Skill(sdd-toolkit:sdd-modify)` to:
- **Apply review feedback systematically** - Parse and apply modifications from sdd-fidelity-review or sdd-plan-review outputs
- **Execute bulk modifications** - Apply multiple spec changes from JSON files with validation
- **Interactive spec updates** - Guided workflow for making structural changes to specifications
- **Parse review reports** - Convert review feedback to structured modification format
- **Preview modifications** - See what would change before applying (dry-run mode)

**Do NOT use for:**
- Simple task status updates (use `sdd-update` instead)
- Creating new specifications (use `sdd-plan` instead)
- Validation only (use `sdd-validate` instead)
- Finding next task to work on (use `sdd-next` instead)

## Core Philosophy

**Systematic Modification**: Spec modifications should be systematic, validated, and safe. This skill provides a guided workflow with previews, user approval, automatic backups, validation, and rollback support to ensure spec integrity.

**Feedback Loop Completion**: This skill closes the loop: Review → Parse → Modify → Validate → Re-review. It enables systematic application of review feedback without manual error-prone editing.

## Skill Family

This skill is part of the **Spec-Driven Development** workflow:
- **sdd-plan** - Creates specifications
- **sdd-fidelity-review** - Reviews implementation against spec
- **sdd-plan-review** - Multi-model spec review before implementation
- **sdd-modify** (this skill) - Applies modifications systematically
- **sdd-validate** - Validates spec structure
- **sdd-update** - Tracks task progress and metadata

## Relationship to sdd-update

**When to use sdd-modify vs sdd-update:**

| Operation | Use sdd-modify | Use sdd-update |
|-----------|---------------|---------------|
| Change task status (in_progress, blocked) | ❌ No | ✅ Yes |
| Mark task completed | ❌ No | ✅ Yes |
| Add journal entries | ❌ No | ✅ Yes |
| Update task descriptions | ✅ Yes | ❌ No |
| Add/remove tasks | ✅ Yes | ❌ No |
| Add verification steps | ✅ Yes | ❌ No |
| Apply review feedback | ✅ Yes | ❌ No |
| Bulk structural changes | ✅ Yes | ❌ No |
| Move spec between folders | ❌ No | ✅ Yes |
| Update spec metadata | ✅ Yes (structural) | ✅ Yes (progress) |

**Summary:**
- **sdd-update** = Task progress, status, journaling (lightweight metadata updates)
- **sdd-modify** = Structural changes, bulk modifications, review feedback (heavyweight spec restructuring)

## Reading Specifications (CRITICAL)

**When working with spec files, ALWAYS use `sdd` CLI commands:**
- ✅ **ALWAYS** use `sdd` commands to read/query spec files
- ❌ **NEVER** use `Read()` tool on .json spec files - bypasses hooks and wastes context tokens
- ❌ **NEVER** use Bash commands to read spec files (e.g., `cat`, `head`, `tail`, `grep`, `jq`)
- ❌ **NEVER** use Python to directly read/write spec JSON files (e.g., `python << EOF ... json.load()`, `open()`)
- ❌ **NEVER** bypass the Read() hook by using alternative file access methods
- The `sdd` CLI provides efficient, structured access with proper parsing and validation
- Spec files can be 50KB+ and reading them directly wastes valuable context window space

**To understand spec structure without reading the spec:**
- ✅ Get the schema: `sdd schema` - outputs the complete spec schema JSON
- This shows all required and optional fields, including metadata structure

**For simple metadata updates (like adding a title field):**
- ✅ Use: `sdd update-frontmatter <spec-id> <key> <value> [--dry-run]`
- Example: `sdd update-frontmatter my-spec-001 title "My Specification Title"`
- This is faster and safer than using `sdd apply-modifications` for single-field updates

## Command Execution Best Practices (CRITICAL)

**CRITICAL: Run sdd commands individually, never in loops or chains**

### DO: Individual Command Execution

Run each `sdd` command as a separate Bash tool call:

```bash
# Parse review report
sdd parse-review my-spec-001 --review reports/review.md --output suggestions.json

# Preview modifications
sdd apply-modifications my-spec-001 --from suggestions.json --dry-run

# Apply modifications
sdd apply-modifications my-spec-001 --from suggestions.json
```

### DON'T: Loops, Chains, or Compound Commands

**Never use bash loops:**
```bash
# ❌ WRONG - Do not use loops
for spec in specs/*.json; do
  sdd apply-modifications $(basename $spec .json) --from mods.json
done
```

**Never chain commands:**
```bash
# ❌ WRONG - Do not chain commands
sdd parse-review my-spec-001 --review review.md && sdd apply-modifications my-spec-001 --from suggestions.json
```

**Never use compound commands:**
```bash
# ❌ WRONG - Do not combine with other commands
echo "Parsing review..." && sdd parse-review my-spec-001 --review review.md
```

**Never use semicolons:**
```bash
# ❌ WRONG - Do not use semicolons
sdd parse-review spec-1 --review r1.md; sdd parse-review spec-2 --review r2.md
```

### Why Individual Execution Matters

1. **Transaction Safety** - Each modification operation is a transaction with automatic rollback
2. **Error Handling** - Easier to identify which operation failed
3. **Rollback Boundaries** - Clear transaction boundaries prevent partial modifications
4. **Permission Clarity** - User can approve/deny each operation separately
5. **Progress Visibility** - User sees each step complete
6. **Debugging** - Easier to trace issues to specific operations
7. **Idempotency** - Safe to retry individual failed operations

### Correct Pattern: Sequential Individual Calls

**For multiple specs:**
```bash
# ✅ CORRECT - Individual calls
sdd apply-modifications spec-1 --from mods.json
# Wait for completion, check result

sdd apply-modifications spec-2 --from mods.json
# Wait for completion, check result

sdd apply-modifications spec-3 --from mods.json
# Wait for completion, check result
```

**For workflow steps:**
```bash
# ✅ CORRECT - Sequential individual operations
sdd parse-review my-spec-001 --review reports/review.md --output suggestions.json
# Wait, parse results

sdd apply-modifications my-spec-001 --from suggestions.json --dry-run
# Wait, review preview

sdd apply-modifications my-spec-001 --from suggestions.json
# Wait, verify completion
```

## Workflow 1: Apply Review Feedback

Complete workflow for applying feedback from sdd-fidelity-review or sdd-plan-review.

### Step 1: Generate Review Report

First, run a review to identify issues:

```bash
# Run fidelity review
Skill(sdd-toolkit:sdd-fidelity-review) "Review implementation for spec my-spec-001"

# This generates: reports/my-spec-001-fidelity-review.md
```

### Step 2: Parse Review Report

Convert review feedback to structured modifications:

```bash
sdd parse-review my-spec-001 --review reports/my-spec-001-fidelity-review.md --output suggestions.json
```

**Output:**
```
✓ Parsed 5 modifications from review report
✓ Saved to suggestions.json

Modifications by type:
  - update_task: 3
  - add_verification: 2

Confidence scores:
  - High confidence: 4 modifications
  - Medium confidence: 1 modification
  - Low confidence: 0 modifications
```

### Step 3: Preview Modifications

See what would change before applying:

```bash
sdd apply-modifications my-spec-001 --from suggestions.json --dry-run
```

**Output:**
```
📋 Modification Preview (Dry-Run)

Tasks to Update:
  task-2-1: "Implement auth"
    → "Implement OAuth 2.0 authentication with PKCE flow"

  task-2-2: "Add login endpoint"
    → "Add /auth/login endpoint with rate limiting"

  task-3-1: "Write tests"
    → "Write comprehensive tests covering edge cases and error handling"

Verification Steps to Add:
  task-2-1 verify-2-1-3: "Verify token expiration handling"
  task-2-2 verify-2-2-4: "Verify rate limiting with concurrent requests"

Impact Summary:
  - 3 tasks will be updated
  - 2 verification steps will be added
  - 2 phases affected
  - 0 tasks will be added
  - 0 tasks will be removed

No validation errors predicted.
```

### Step 4: Apply Modifications

Apply the changes with automatic backup and validation:

```bash
sdd apply-modifications my-spec-001 --from suggestions.json
```

**Output:**
```
✓ Backup created: specs/.backups/my-spec-001-20251106-143022.json
✓ Applied 5 modifications
✓ Validation passed
✓ Spec updated successfully

Changes:
  - Updated 3 task descriptions
  - Added 2 verification steps

Next steps:
  - Review updated spec: sdd context show my-spec-001
  - Continue implementation with updated guidance
  - Run fidelity review again to confirm issues resolved
```

### Step 5: Verify Results

Optionally, run fidelity review again to confirm issues are resolved:

```bash
Skill(sdd-toolkit:sdd-fidelity-review) "Re-review spec my-spec-001 after modifications"
```

## Workflow 2: Bulk Modifications from JSON

Apply pre-defined modifications from a JSON file.

### Step 1: Create Modification File

Create a JSON file with desired modifications:

```json
{
  "modifications": [
    {
      "operation": "update_task",
      "task_id": "task-2-1",
      "updates": {
        "description": "Implement OAuth 2.0 authentication with PKCE flow and refresh tokens",
        "task_category": "implementation",
        "file_path": "app/services/auth_service.py"
      }
    },
    {
      "operation": "add_verification",
      "task_id": "task-2-1",
      "verify_id": "verify-2-1-4",
      "description": "Verify refresh token rotation works correctly",
      "command": "pytest tests/test_auth.py::test_refresh_token_rotation -v",
      "verification_type": "automated"
    },
    {
      "operation": "update_metadata",
      "task_id": "task-2-2",
      "metadata": {
        "estimated_hours": 3,
        "priority": "high"
      }
    }
  ]
}
```

**Save as:** `my-modifications.json`

### Step 2: Validate Modification Structure

Check that the modification file is valid:

```bash
sdd validate-modifications my-modifications.json
```

**Output:**
```
✓ Modification file is valid
✓ All task references exist in spec
✓ All required fields present
✓ No schema violations

Ready to apply 3 modifications.
```

### Step 3: Preview Impact

Run dry-run to see what would change:

```bash
sdd apply-modifications my-spec-001 --from my-modifications.json --dry-run
```

### Step 4: Apply with Validation

Apply the modifications:

```bash
sdd apply-modifications my-spec-001 --from my-modifications.json
```

**Output shows:**
- Backup location
- Number of modifications applied
- Validation results
- Changes summary

## Workflow 3: Interactive Guided Modification

Use the skill for step-by-step guided modifications (NOT YET IMPLEMENTED - FUTURE ENHANCEMENT).

```bash
Skill(sdd-toolkit:sdd-modify) "Guide me through updating spec my-spec-001"
```

**Future workflow:**
1. Skill asks what type of modification you want to make
2. Provides options: Update task, Add task, Add verification, etc.
3. Prompts for required information
4. Shows preview of change
5. Asks for confirmation
6. Applies modification
7. Validates result
8. Offers to make more changes or finish

**Current Status:** Interactive mode is planned for Phase 2. For now, use Workflows 1 or 2.

## CLI Commands Reference

### Parse Review Report

Convert review feedback to structured modification JSON:

```bash
sdd parse-review <spec-id> --review <review-report.md> --output <suggestions.json>
```

**Options:**
- `--review` - Path to review report (markdown from sdd-fidelity-review or sdd-plan-review)
- `--output` - Where to save parsed modifications JSON (optional, defaults to `{spec-id}-suggestions.json`)

**Example:**
```bash
sdd parse-review my-spec-001 \
  --review reports/my-spec-001-review.md \
  --output suggestions.json
```

### Apply Modifications

Apply modifications to a spec with validation and backup:

```bash
sdd apply-modifications <spec-id> --from <modifications.json> [--dry-run] [--no-validate]
```

**Options:**
- `--from` - Path to modifications JSON file (required)
- `--dry-run` - Preview changes without applying (optional)
- `--no-validate` - Skip validation after applying (NOT RECOMMENDED)

**Examples:**
```bash
# Preview modifications
sdd apply-modifications my-spec-001 --from suggestions.json --dry-run

# Apply modifications with validation
sdd apply-modifications my-spec-001 --from suggestions.json

# Apply without validation (dangerous, not recommended)
sdd apply-modifications my-spec-001 --from suggestions.json --no-validate
```

### Validate Modifications

Check modification file structure before applying:

```bash
sdd validate-modifications <modifications.json>
```

**Example:**
```bash
sdd validate-modifications suggestions.json
```

## Modification JSON Schema

Modification files use this structure:

```json
{
  "modifications": [
    {
      "operation": "update_task",
      "task_id": "task-2-1",
      "field": "description",
      "value": "New task description"
    },
    {
      "operation": "add_verification",
      "task_id": "task-2-1",
      "verify_id": "verify-2-1-4",
      "description": "Verification description",
      "command": "optional command to run"
    },
    {
      "operation": "update_metadata",
      "task_id": "task-2-1",
      "field": "actual_hours",
      "value": 4.5
    }
  ]
}
```

### Supported Operations

#### High-Level Task-Centric Operations (Recommended)

**1. update_task** - Modify multiple task fields in one operation

```json
{
  "operation": "update_task",
  "task_id": "task-2-1",
  "updates": {
    "title": "Updated title",
    "description": "Updated description",
    "file_path": "app/services/auth.py",
    "task_category": "implementation"
  }
}
```

**Updatable fields:**
- `title` - Task title
- `description` - Task description
- `task_category` - Task category (implementation, test, documentation, etc.)
- `skill` - Skill to use for this task
- `command` - Command to run for this task
- `file_path` - Related file path
- `status_note` - Note about current status
- `status` - Task status (pending, in_progress, completed, blocked)

**Notes:**
- Can update multiple fields in single operation
- Unknown fields are rejected with clear error
- Validates task exists and is correct type

**2. add_verification** - Add verification step to task

```json
{
  "operation": "add_verification",
  "task_id": "task-2-1",
  "verify_id": "verify-2-1-4",
  "description": "Verify X works correctly",
  "command": "pytest tests/test_x.py -v",
  "verification_type": "automated"
}
```

**Required fields:**
- `task_id` - Parent task
- `verify_id` - Unique verification ID (must follow pattern verify-X-Y-Z)
- `description` - What to verify

**Optional fields:**
- `command` - Command to run for verification
- `verification_type` - Type of verification ("manual" or "automated", defaults to "manual")

**Notes:**
- Auto-generates boilerplate (type, status, dependencies)
- Validates parent task exists
- Prevents duplicate verify_id

**3. update_metadata** - Update task metadata fields

```json
{
  "operation": "update_metadata",
  "task_id": "task-2-1",
  "metadata": {
    "details": "Detailed implementation notes",
    "estimated_hours": 4,
    "priority": "high",
    "complexity": "medium"
  }
}
```

**Common metadata fields:**
- `details` - Detailed implementation notes
- `estimated_hours` - Estimated time
- `actual_hours` - Actual time spent
- `priority` - Task priority (high, medium, low)
- `complexity` - Task complexity (high, medium, low)
- Any custom fields your workflow needs

**Notes:**
- Merges with existing metadata (doesn't replace)
- Can update multiple metadata fields at once
- Works on any node type (task, subtask, verify, phase)

**4. batch_update** - Apply same change to multiple nodes

```json
{
  "operation": "batch_update",
  "node_ids": ["task-1-1", "task-1-2", "task-1-3"],
  "field": "metadata",
  "value": {"priority": "high"}
}
```

**Required fields:**
- `node_ids` - List of node IDs to update
- `field` - Field name to update
- `value` - Value to set for all nodes

**Notes:**
- Useful for bulk operations (e.g., set priority for all tasks in phase)
- Partial success possible (reports which nodes succeeded/failed)
- Works with any updatable field including metadata

#### Low-Level Node Operations (Advanced)

For direct node manipulation, use these operations:

**5. add_node** - Add any node type (task, subtask, verify, phase, group)

```json
{
  "operation": "add_node",
  "parent_id": "phase-2",
  "node_data": {
    "node_id": "task-2-5",
    "type": "task",
    "title": "New task",
    "description": "Task description",
    "status": "pending",
    "metadata": {},
    "dependencies": {"blocks": [], "blocked_by": [], "depends": []}
  }
}
```

**6. remove_node** - Remove node (optionally with descendants)

```json
{
  "operation": "remove_node",
  "node_id": "task-2-5",
  "cascade": true
}
```

**7. update_node_field** - Update single field on any node

```json
{
  "operation": "update_node_field",
  "node_id": "task-2-1",
  "field": "description",
  "value": "Updated description"
}
```

**8. move_node** - Move node to different parent

```json
{
  "operation": "move_node",
  "node_id": "task-1-3",
  "new_parent_id": "phase-2",
  "position": 0
}
```

#### Future Operations (Not Yet Implemented)

**9. reorder_tasks** - Change task order within phase (PLANNED)

```json
{
  "operation": "reorder_tasks",
  "phase_id": "phase-2",
  "new_order": ["task-2-2", "task-2-1", "task-2-3"]
}
```

## Safety Features

### 1. Automatic Backup

Every apply operation creates a backup before making changes:

```
specs/.backups/my-spec-001-20251106-143022.json
```

Backups include:
- Full spec content at time of modification
- Timestamp in filename
- Preserved indefinitely (manual cleanup required)

**Restoring from backup:**
```bash
cp specs/.backups/my-spec-001-20251106-143022.json specs/active/my-spec-001.json
```

### 2. Transaction Rollback

If validation fails after applying modifications:
1. All changes are automatically rolled back
2. Spec restored to pre-modification state
3. Backup preserved for manual inspection
4. Clear error message indicates rollback occurred

**Example rollback scenario:**
```
✗ Validation failed after applying modifications
✓ Rolled back all changes
✓ Spec restored to original state
✓ Backup preserved: specs/.backups/my-spec-001-20251106-143022.json

Validation errors:
  - Task task-2-3 missing required field: description
  - Invalid phase_id reference in task task-3-1

Suggestions:
  - Review modification file for invalid task references
  - Ensure all required fields are included
  - Run sdd-validate on modification file before applying
```

### 3. Validation After Apply

After every modification (unless `--no-validate` used):
1. Full spec validation runs
2. Checks schema compliance
3. Validates references (phase_id, task_id, etc.)
4. Ensures required fields present
5. Reports any issues found

**If validation passes:**
- Changes committed
- Success message shown
- Ready to continue

**If validation fails:**
- Automatic rollback triggered
- Error messages explain what's wrong
- Suggestions for fixing provided

### 4. Idempotency

Modifications are designed to be idempotent:
- Applying same modification twice is safe
- Second application results in "no changes" not error
- Safe to retry failed operations

**Example:**
```bash
# First application
sdd apply-modifications my-spec-001 --from mods.json
# Output: ✓ Applied 5 modifications

# Second application (same file)
sdd apply-modifications my-spec-001 --from mods.json
# Output: ✓ No changes needed (all modifications already applied)
```

### 5. Preview Before Apply

Always preview with `--dry-run` before applying significant changes:

```bash
# Preview first
sdd apply-modifications my-spec-001 --from mods.json --dry-run

# Review output, then apply if looks correct
sdd apply-modifications my-spec-001 --from mods.json
```

## Integration with Review Skills

### sdd-fidelity-review Integration

**Complete closed-loop workflow:**

```bash
# 1. Run fidelity review
Skill(sdd-toolkit:sdd-fidelity-review) "Review spec my-spec-001"
# → Generates: reports/my-spec-001-fidelity-review.md

# 2. Parse review to extract fixes
sdd parse-review my-spec-001 --review reports/my-spec-001-fidelity-review.md

# 3. Preview modifications
sdd apply-modifications my-spec-001 --from my-spec-001-suggestions.json --dry-run

# 4. Apply modifications
sdd apply-modifications my-spec-001 --from my-spec-001-suggestions.json

# 5. Re-review to confirm fixes
Skill(sdd-toolkit:sdd-fidelity-review) "Re-review spec my-spec-001"
# → Should show issues resolved
```

### sdd-plan-review Integration

**Apply consensus recommendations:**

```bash
# 1. Run multi-model plan review
Skill(sdd-toolkit:sdd-plan-review) "Review spec my-spec-001"
# → Generates consensus recommendations

# 2. Extract high-confidence recommendations
# (Manual step or automated filter for consensus items)

# 3. Apply consensus improvements
sdd apply-modifications my-spec-001 --from consensus-improvements.json
```

## Error Handling

### Common Error Scenarios

**1. Spec Not Found**

```
✗ Error: Spec 'my-spec-001' not found

Searched locations:
  - specs/active/my-spec-001.json
  - specs/pending/my-spec-001.json
  - specs/completed/my-spec-001.json

Suggestions:
  - Verify spec ID is correct
  - Check that spec exists in specs/ folder
  - Use full path if spec is in non-standard location
```

**2. Invalid Modification File**

```
✗ Error: Modification file invalid

Validation errors:
  - Line 5: Missing required field 'operation'
  - Line 12: Invalid task_id format 'task2' (expected 'task-2-X')
  - Line 18: Unknown operation 'delete_task' (supported: update_task, add_verification, update_metadata)

Suggestions:
  - Review modification schema documentation
  - Use sdd parse-review to generate valid modification files
  - Validate modification file structure before applying
```

**3. Task Reference Error**

```
✗ Error: Task not found in spec

Cannot modify task-5-3: Task does not exist in spec my-spec-001

Available tasks in spec:
  - task-1-1 through task-1-3 (Phase 1)
  - task-2-1 through task-2-4 (Phase 2)
  - task-3-1 through task-3-2 (Phase 3)

Suggestions:
  - Verify task_id exists in spec
  - Use sdd context show my-spec-001 to see all task IDs
  - Check for typos in task_id
```

**4. Validation Failure After Apply**

```
✗ Error: Validation failed after applying modifications
✓ All changes rolled back
✓ Spec restored to original state

Validation errors:
  - Task task-2-3: Missing required field 'description'
  - Task task-3-1: Invalid phase_id reference 'phase-5' (phase doesn't exist)

Modifications attempted: 5
Backup location: specs/.backups/my-spec-001-20251106-143022.json

Suggestions:
  - Review modification file for completeness
  - Ensure all required fields included in update operations
  - Verify phase references are correct
  - Fix issues and retry
```

### Rollback Communication

When rollback occurs:
1. **Clear indication** - "All changes rolled back"
2. **Reason explained** - Shows validation errors that triggered rollback
3. **Backup location** - Shows where backup is preserved
4. **Actionable suggestions** - Tells you how to fix the issue

## Best Practices

### 1. Always Preview First

Run `--dry-run` before applying significant changes:

```bash
# Preview
sdd apply-modifications my-spec-001 --from mods.json --dry-run

# Review output carefully

# Apply if preview looks correct
sdd apply-modifications my-spec-001 --from mods.json
```

### 2. Start with Small Batches

When making many changes:
- Apply in small batches (5-10 modifications at a time)
- Validate after each batch
- Easier to identify and fix issues

```bash
# Split modifications into batches
sdd apply-modifications my-spec-001 --from batch1.json
sdd apply-modifications my-spec-001 --from batch2.json
sdd apply-modifications my-spec-001 --from batch3.json
```

### 3. Preserve Backups

Keep backups until changes are verified:
- Don't delete backups immediately
- Wait until implementation complete
- Use for comparison or rollback if needed

```bash
# Compare current spec to backup
diff specs/active/my-spec-001.json specs/.backups/my-spec-001-20251106-143022.json
```

### 4. Validate Modification Files

Before applying, validate the modification file structure:

```bash
# Validate first
sdd validate-modifications my-modifications.json

# Then apply
sdd apply-modifications my-spec-001 --from my-modifications.json
```

### 5. Document Major Changes

After significant modifications, add journal entry via sdd-update:

```bash
sdd add-journal my-spec-001 \
  --title "Spec Updated from Fidelity Review" \
  --content "Applied 5 modifications based on fidelity review feedback. Updated task descriptions for clarity and added verification steps." \
  --entry-type note
```

### 6. Use Parse-Review for Review Feedback

Don't manually create modification files from review reports:
- Use `sdd parse-review` to automatically extract modifications
- Reduces errors
- Faster
- More reliable

```bash
# ✓ Good
sdd parse-review my-spec-001 --review reports/review.md

# ✗ Bad
# Manually transcribing review feedback into JSON
```

### 7. Re-Review After Modifications

After applying review feedback, run review again to confirm:

```bash
# Apply modifications
sdd apply-modifications my-spec-001 --from suggestions.json

# Re-review to confirm issues resolved
Skill(sdd-toolkit:sdd-fidelity-review) "Re-review spec my-spec-001"
```

### 8. Handle Rollbacks Gracefully

If rollback occurs:
1. Read the error messages carefully
2. Fix issues in modification file
3. Preview again with `--dry-run`
4. Retry application

```bash
# Failed with rollback
sdd apply-modifications my-spec-001 --from mods.json
# ✗ Rolled back due to validation errors

# Fix mods.json based on error messages

# Preview to verify fix
sdd apply-modifications my-spec-001 --from mods.json --dry-run

# Retry
sdd apply-modifications my-spec-001 --from mods.json
```

## Limitations

### Current Limitations

1. **No interactive guided mode** - Interactive workflow is planned for Phase 2
2. **No task reordering** - Cannot change task order within phases yet (use move_node as workaround)
3. **Limited phase operations** - Can add/remove phases with low-level operations, but no high-level convenience operations
4. **Single spec at a time** - No batch operations across multiple specs
5. **Manual batch creation** - No automated batching or dependency resolution for complex multi-spec workflows

### Future Enhancements (Phase 2)

- **Interactive modification builder** - Guided prompts for building modifications
- **Modification templates** - Common patterns as reusable templates
- **Diff visualization** - Better visual diff output with highlighting
- **Undo/redo support** - History of modifications with rollback to any point
- **Automated batching** - Smart grouping of related modifications
- **Multi-spec operations** - Apply same modification to multiple specs
- **Phase operations** - Add, remove, reorder phases
- **Task operations** - Add, remove, reorder tasks
- **Dependency tracking** - Handle task dependencies during modifications

## Troubleshooting

### Issue: Parse-review finds no modifications

**Problem:**
```
sdd parse-review my-spec-001 --review reports/review.md
✗ No modifications found in review report
```

**Solutions:**
1. Check review report format - Should contain clear modification language
2. Ensure review was generated by sdd-fidelity-review or sdd-plan-review
3. Look for patterns like "update task X to Y", "add verification step"
4. Manual modification file creation may be needed for non-standard formats

### Issue: Task ID not found

**Problem:**
```
✗ Error: Task task-5-3 not found in spec
```

**Solutions:**
1. List all task IDs: `sdd context show my-spec-001`
2. Check for typos in task_id
3. Verify task exists in current spec version
4. Ensure you're modifying the correct spec

### Issue: Validation fails after apply

**Problem:**
```
✗ Validation failed after applying modifications
✓ Rolled back all changes
```

**Solutions:**
1. Read validation error messages carefully
2. Check that all required fields are included in modifications
3. Verify all references (phase_id, task_id) are valid
4. Fix issues in modification file
5. Preview with --dry-run before retrying
6. Apply in smaller batches to isolate problematic modifications

### Issue: Modifications applied but no visible changes

**Problem:**
```
✓ Applied 5 modifications
# But spec looks unchanged
```

**Solutions:**
1. Check if modifications were already applied (idempotency)
2. Verify modification file targets correct fields
3. Compare with backup: `diff specs/active/spec.json specs/.backups/spec-backup.json`
4. Review modification values - may be identical to existing values

### Issue: Cannot find backup file

**Problem:**
Need to rollback but backup file missing

**Solutions:**
1. Check `.backups/` folder in specs directory
2. Backups use timestamp: `{spec-id}-{YYYYMMDD-HHMMSS}.json`
3. If backup missing, check git history for previous version
4. Use `git log specs/active/{spec-id}.json` to see commits

## Examples Directory

See `skills/sdd-modify/examples/` for detailed walkthroughs:

- **apply-review.md** - Complete workflow for applying fidelity review feedback
- **bulk-modify.md** - Bulk modifications from JSON file
- **interactive.md** - Interactive guided modification (future)

## Summary

The sdd-modify skill provides systematic, safe spec modification:
- ✅ **Safe** - Automatic backup, validation, and rollback
- ✅ **Systematic** - Parse review feedback automatically
- ✅ **Validated** - Full validation after every apply
- ✅ **Transparent** - Clear previews and error messages
- ✅ **Integrated** - Works seamlessly with review workflows

**Key Workflow:**
```
Review → Parse → Preview → Apply → Validate → Re-review
```

For simple task status updates and journaling, use `Skill(sdd-toolkit:sdd-update)` instead.
