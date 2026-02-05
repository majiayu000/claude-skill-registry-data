---
name: sdd-update
description: Progress tracking for spec-driven development. Use to update task status, track progress, journal decisions, move specs between folders, and maintain spec files. Handles the administrative/clerical aspects of specification documents during development.
---

# Spec-Driven Development: Update Skill

## When to Use This Skill

Use `Skill(sdd-toolkit:sdd-update)` to:
- **Complete tasks** (atomically marks as completed AND creates journal entry using `complete-task`)
- Mark tasks as in_progress or blocked
- Document decisions and deviations in journal entries
- Add verification results to specs
- Move specs between lifecycle folders (e.g., pending => active, active => completed)
- Update spec metadata fields (progress tracking, status)

**Do NOT use for:**
- Creating specifications
- Finding what to work on next
- Writing code or running tests
- **Structural spec modifications** (use `Skill(sdd-toolkit:sdd-modify)` instead - see below)

## Core Philosophy

**Document Reality**: JSON spec files are living documents that evolve during implementation. This skill ensures the spec accurately reflects current progress, decisions, and status. All updates are made through CLI commands that handle validation, backups, and progress recalculation automatically.

## Reading Specifications (CRITICAL)

**When working with spec files, ALWAYS use `sdd` CLI commands:**
- ✅ **ALWAYS** use `sdd` commands to read/query spec files (e.g., `sdd update-status`, `sdd add-journal`, `sdd list-blockers`)
- ❌ **NEVER** use `Read()` tool on .json spec files - bypasses hooks and wastes context tokens (specs can be 50KB+)
- ❌ **NEVER** use Bash commands to read spec files (e.g., `cat`, `head`, `tail`, `grep`, `jq`)
- ❌ **NEVER** use command chaining to access specs (e.g., `sdd --version && cat specs/active/spec.json`)
- The `sdd` CLI provides efficient, structured access with proper parsing and validation
- Spec files are large and reading them directly wastes valuable context window space

## Skill Family

This skill is part of the **Spec-Driven Development** workflow:
- **sdd-plan** - Creates specifications → **sdd-plan-review** / **sdd-fidelity-review** - Reviews specs → **sdd-modify** - Applies review feedback → **sdd-next** - Finds next task → **Implementation** → **sdd-update** (this skill) - Updates progress

## Relationship to sdd-modify

**When to use sdd-update vs sdd-modify:**

| Operation | Use sdd-update | Use sdd-modify |
|-----------|---------------|----------------|
| Mark task completed | ✅ Yes | ❌ No |
| Update task status (in_progress, blocked) | ✅ Yes | ❌ No |
| Add journal entries | ✅ Yes | ❌ No |
| Move spec between folders | ✅ Yes | ❌ No |
| **Update task descriptions** | ❌ No | ✅ Yes |
| **Add/remove tasks** | ❌ No | ✅ Yes |
| **Add verification steps** | ❌ No | ✅ Yes |
| **Apply review feedback systematically** | ❌ No | ✅ Yes |
| **Bulk structural modifications** | ❌ No | ✅ Yes |

**Key Distinction:**
- **sdd-update** = Lightweight metadata updates (status, progress, journal entries)
- **sdd-modify** = Heavyweight structural changes (task descriptions, adding tasks/verifications, review feedback)

**Example - When to use sdd-modify:**

If you need to:
- Apply feedback from sdd-fidelity-review or sdd-plan-review
- Update multiple task descriptions for clarity
- Add verification steps discovered during implementation
- Make bulk modifications to spec structure

Then use: `Skill(sdd-toolkit:sdd-modify)`

See **Systematic Spec Modification** section below for details.

## Workflow 1: Starting a Task

Mark a task as in_progress when you begin work:

```bash
sdd update-status {spec-id} {task-id} in_progress
```

The CLI automatically records the start timestamp for tracking purposes.

## Workflow 2: Tracking Progress

### Add Journal Entries

Document decisions, deviations, or important notes:

```bash
# Document a decision
sdd add-journal {spec-id} --title "Decision Title" --content "Explanation of decision and rationale" --task-id {task-id} --entry-type decision

# Document a deviation from the plan
sdd add-journal {spec-id} --title "Deviation: Changed Approach" --content "Created separate service file instead of modifying existing. Improves separation of concerns." --task-id {task-id} --entry-type deviation

# Document task completion (use status_change, NOT completion)
sdd add-journal {spec-id} --title "Task Completed: Implement Auth" --content "Successfully implemented authentication with JWT tokens. All tests passing." --task-id {task-id} --entry-type status_change

# Document a note
sdd add-journal {spec-id} --title "Implementation Note" --content "Using Redis for session storage as discussed." --task-id {task-id} --entry-type note
```

**Entry types:** `decision`, `deviation`, `blocker`, `note`, `status_change`

## Workflow 3: Handling Blockers

### Mark Task as Blocked

When a task cannot proceed:

```bash
sdd mark-blocked {spec-id} {task-id} --reason "Description of blocker" --type {type} --ticket "TICKET-123"
```

**Blocker types:**
- `dependency` - Waiting on external dependency
- `technical` - Technical issue blocking progress
- `resource` - Resource unavailability
- `decision` - Awaiting architectural/product decision

### Unblock Task

When blocker is resolved:

```bash
sdd unblock-task {spec-id} {task-id} --resolution "Description of how it was resolved"
```

### List All Blockers

```bash
sdd list-blockers {spec-id}
```

## Workflow 4: Adding Verification Results

### Manual Verification Recording

Document verification results:

```bash
# Verification passed
sdd add-verification {spec-id} {verify-id} PASSED --command "npm test" --output "All tests passed" --notes "Optional notes"

# Verification failed
sdd add-verification {spec-id} {verify-id} FAILED --command "npm test" --output "3 tests failed" --issues "List of issues found"

# Partial success
sdd add-verification {spec-id} {verify-id} PARTIAL --notes "Most checks passed, minor issues remain"
```

### Automatic Verification Execution

If verification tasks have metadata specifying how to execute them, run automatically:

```bash
# Execute verification based on metadata
sdd execute-verify {spec-id} {verify-id}

# Execute and automatically record result
sdd execute-verify {spec-id} {verify-id} --record
```

**Requirements:** Verification task must have `skill` or `command` in its metadata.

### Verify on Task Completion

Automatically run verifications when marking a task complete:

```bash
sdd update-status {spec-id} {task-id} completed --verify
```

The `--verify` flag runs all associated verify tasks. If any fail, the task reverts to `in_progress`.

### Configurable Failure Handling

Verification tasks can specify custom failure behavior via `on_failure` metadata:

```json
{
  "verify-1-1": {
    "metadata": {
      "on_failure": {
        "consult": true,
        "revert_status": "in_progress",
        "max_retries": 2,
        "continue_on_failure": false
      }
    }
  }
}
```

**on_failure fields:**
- `consult` (boolean) - Recommend AI consultation for debugging
- `revert_status` (string) - Status to revert parent task to on failure
- `max_retries` (integer) - Number of automatic retry attempts (0-5)
- `continue_on_failure` (boolean) - Continue with other verifications if this fails

## Workflow 5: Completing Tasks

### Complete a Task (Recommended: Atomic Status + Journal)

When finishing a task, use `complete-task` to atomically mark it complete AND create a journal entry:

```bash
# Complete with automatic journal entry
sdd complete-task {spec-id} {task-id} --journal-content "Successfully implemented JWT authentication with token refresh. All tests passing including edge cases for expired tokens."

# Customize the journal entry
sdd complete-task {spec-id} {task-id} --journal-title "Task Completed: Authentication Implementation" --journal-content "Detailed description of what was accomplished..." --entry-type status_change

# Add a brief status note
sdd complete-task {spec-id} {task-id} --note "All tests passing" --journal-content "Implemented authentication successfully."
```

**What `complete-task` does automatically:**
1. Updates task status to `completed`
2. Records completion timestamp
3. Creates a journal entry documenting the completion
4. Clears the `needs_journaling` flag
5. Syncs metadata and recalculates progress
6. Automatically journals parent nodes (phases, groups) that auto-complete

**This is the recommended approach** because it ensures proper documentation of task completion.

#### Parent Node Journaling

When completing a task causes parent nodes (phases or task groups) to auto-complete, `complete-task` automatically creates journal entries for those parents:

- **Automatic detection**: The system detects when all child tasks in a phase/group are completed
- **Automatic journaling**: Creates journal entries like "Phase Completed: Phase 1" for each auto-completed parent
- **No manual action needed**: You don't need to manually journal parent completions
- **Hierarchical**: Works for multiple levels (e.g., completing a task can journal both its group AND its phase)

Example output:
```bash
$ sdd complete-task my-spec-001 task-1-2 --journal-content "Completed final task"
✓ Task marked complete
✓ Journal entry added
✓ Auto-journaled 2 parent node(s): group-1, phase-1
```

### Alternative: Status-Only Update (Not Recommended for Completion)

If you need to mark a task completed without journaling (rare), use:

```bash
sdd update-status {spec-id} {task-id} completed --note "Brief completion note"
```

⚠️ **Warning:** This sets `needs_journaling=True` and requires a follow-up `add-journal` call. Use `complete-task` instead to avoid forgetting to journal.

### Complete a Spec

When all phases are verified and complete:

```bash
# Check if ready to complete
sdd check-complete {spec-id}

# Complete spec (updates metadata, regenerates docs, moves to completed/)
sdd complete-spec {spec-id}

# Skip documentation regeneration
sdd complete-spec {spec-id} --skip-doc-regen
```

## Workflow 6: Moving Specs Between Folders

### Activate from Backlog

Move a spec from pending/ to active/ when ready to start work:

```bash
sdd activate-spec {spec-id}
```

This updates metadata status to "active" and makes the spec visible to sdd-next.

### Move to Completed

Use `complete-spec` (see Workflow 5) to properly complete and move a spec.

### Archive Superseded Specs

Move specs that are no longer relevant:

```bash
sdd move-spec {spec-id} archived
```

## Fidelity Review Configuration

The optional pre-completion fidelity review behavior can be configured via `.claude/sdd_config.json`:

```json
{
  "fidelity_review": {
    "enabled": true,
    "on_task_complete": "prompt",
    "on_phase_complete": "always",
    "skip_categories": ["investigation", "research"],
    "min_task_complexity": "medium"
  }
}
```

**Configuration options:**

- `enabled` (boolean, default: `true`) - Master switch for fidelity review features
- `on_task_complete` (string, default: `"prompt"`) - When to offer fidelity review for task completion:
  - `"always"` - Automatically run fidelity review before marking any task complete
  - `"prompt"` - Ask user if they want to run fidelity review (recommended)
  - `"never"` - Skip automatic prompts, only use manual invocation or verification tasks

- `on_phase_complete` (string, default: `"always"`) - When to offer fidelity review for phase completion:
  - `"always"` - Automatically run phase-level fidelity review when all tasks in phase complete
  - `"prompt"` - Ask user if they want to run phase review
  - `"never"` - Skip automatic phase reviews

- `skip_categories` (array, default: `[]`) - Task categories that don't require fidelity review:
  - Common values: `["investigation", "research", "decision"]`
  - Tasks with these categories will skip automatic review prompts

- `min_task_complexity` (string, default: `"low"`) - Minimum task complexity for automatic review:
  - `"low"` - Review all tasks (most thorough)
  - `"medium"` - Only review medium/high complexity tasks
  - `"high"` - Only review high complexity tasks (least intrusive)

**When fidelity review is triggered:**

Based on configuration, when completing a task via `sdd-update`, the system will:

1. Check if task category is in `skip_categories` → skip if true
2. Check task complexity against `min_task_complexity` → skip if below threshold
3. Check `on_task_complete` setting:
   - `"always"` → Automatically invoke fidelity review subagent
   - `"prompt"` → Ask user: "Run fidelity review before completing?"
   - `"never"` → Skip (user can still manually invoke)

**Note:** Verification tasks with `verification_type: "fidelity"` always run regardless of configuration.

## Workflow 7: Git Commit Integration

When git integration is enabled (via `.claude/git_config.json`), the sdd-update skill can automatically create commits after task completion based on configured commit cadence preferences.

### Commit Cadence Configuration

The commit cadence determines when to offer automatic commits:

- **task**: Commit after each task completion (frequent commits, granular history)
- **phase**: Commit after each phase completion (fewer commits, milestone-based)
- **manual**: Never auto-commit (user manages commits manually)

The cadence preference is configured project-wide in `.claude/git_config.json` and accessed via `get_git_setting('commit_cadence')`.

### Commit Workflow Steps

When completing a task and git integration is enabled, the workflow follows these steps:

**1. Check Commit Cadence**

First, confirm whether automatic commits are enabled for the current event type. `sdd-update` reads `.claude/git_config.json` at runtime, so you only need to inspect the configuration (for example: `sdd skills-dev start-helper session-summary . --json`) to see whether the cadence is set to `task`, `phase`, or `manual`.

**2. Check for Changes**

Before offering a commit, verify there are uncommitted changes:

```bash
# Check for changes (run in repo root directory)
git status --porcelain

# If output is empty, skip commit offer (nothing to commit)
# If output has content, proceed with commit workflow
```

**3. Generate Commit Message**

Create a structured commit message from task metadata using the pattern `{task-id}: {task-title}` (for example, `task-2-3: Implement JWT verification middleware`). The CLI applies this format automatically when generating commits.

**4. Preview and Stage Changes (Two-Step Workflow)**

The workflow now supports **agent-controlled file staging** with two approaches:

**Option A: Show Preview (Default - Recommended)**

When `file_staging.show_before_commit = true` (default), the agent sees uncommitted files and can selectively stage:

```bash
# Step 1: Preview uncommitted files (automatic via show_commit_preview_and_wait)
# Shows: modified, untracked, and staged files
sdd complete-task SPEC_ID TASK_ID

# Step 2: Agent stages only task-related files
git add specs/active/spec.json
git add src/feature/implementation.py
git add tests/test_feature.py
# (Deliberately skip unrelated files like debug scripts, personal notes)

# Step 3: Create commit with staged files only
sdd create-task-commit SPEC_ID TASK_ID
```

**Benefits:**
- ✅ Agent controls what files are committed
- ✅ Unrelated files protected from accidental commits
- ✅ Clean, focused task commits

**Option B: Auto-Stage All (Backward Compatible)**

When `file_staging.show_before_commit = false`, the old behavior is preserved:

```bash
# Automatically stages all files and commits (old behavior)
git add --all
git commit -m "{task-id}: {task-title}"
```

**Configuration:**

File staging behavior is controlled in `.claude/git_config.json`:

```json
{
  "enabled": true,
  "auto_commit": true,
  "commit_cadence": "task",
  "file_staging": {
    "show_before_commit": true  // false = auto-stage all (backward compatible)
  }
}
```

**Command Reference:**

```bash
# Complete task (shows preview if enabled)
sdd complete-task SPEC_ID TASK_ID

# Create commit from staged files
sdd create-task-commit SPEC_ID TASK_ID

# Example workflow:
sdd complete-task user-auth-001 task-1-2
# (Review preview, stage desired files)
git add specs/active/user-auth-001.json src/auth/service.py
sdd create-task-commit user-auth-001 task-1-2
```

**All git commands use `cwd=repo_root`** obtained from `find_git_root()` to ensure they run in the correct repository directory.

**5. Record Commit Metadata**

After successful commit, capture the commit SHA and update spec metadata:

```bash
# Get the commit SHA
git rev-parse HEAD

# Example output: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

### Error Handling

Git operations should be non-blocking - failures should not prevent task completion:

**Error handling principles:**

- Check `returncode` for all git commands
- Log warnings for failures but continue execution
- Git failures do NOT prevent task completion
- User can manually commit if automatic commit fails
- Provide clear error messages in logs for debugging

### Repository Root Detection

All git commands must run in the repository root directory:

- `sdd-update` automatically discovers the repo root (similar to running `git rev-parse --show-toplevel` from the spec directory).
- If no git repository is detected, the commit workflow is skipped and the task still completes.
- Manual workflows should `cd` to the project root (the directory containing `.git/`) before running git commands.

### Complete Example Workflow

1. Complete the task with `sdd complete-task SPEC_ID TASK_ID`.
2. If git integration is enabled and cadence matches the event, `sdd-update` checks for uncommitted changes.
3. Stage files either via the preview workflow (recommended) or `git add --all` when auto-staging is enabled.
4. Run `sdd create-task-commit SPEC_ID TASK_ID` to generate the commit; the command formats the message and records the SHA automatically.
5. If no changes are staged or the git command fails, the tool logs a warning and the task completion still succeeds.

### Configuration File

Git integration is configured via `.claude/git_config.json`:

```json
{
  "enabled": true,
  "auto_branch": true,
  "auto_commit": true,
  "auto_push": false,
  "auto_pr": false,
  "commit_cadence": "task"
}
```

**Settings:**
- `enabled`: Enable/disable all git integration
- `auto_commit`: Enable automatic commits (requires enabled: true)
- `commit_cadence`: When to commit - "task", "phase", or "manual"

See **Workflow 7: Git Commit Integration** in sdd-next SKILL.md for branch creation workflow details.

## Workflow 8: Git Push & PR Handoff

When a spec is completed, the workflow can automatically push commits to the remote repository. Pull request creation is handed off to the dedicated PR workflow.

### Push-Only Scope (PRs Deferred)

- `Skill(sdd-toolkit:sdd-update)` handles local commits and optional pushes during completion workflows, but it does **not** create pull requests.
- Pull requests are beyond the scope of your responsibilities.
- If push automation is disabled or fails, finish the spec update, run `git push -u origin <branch>` manually, and then involve the PR skill/agent.

## Common CLI Patterns

### Preview Changes

Use `--dry-run` to preview changes before applying:

```bash
sdd update-status {spec-id} {task-id} completed --dry-run
sdd mark-blocked {spec-id} {task-id} --reason "Test" --dry-run
```

### Query Spec State

```bash
# Get overall progress
sdd status-report {spec-id}

# List all phases with progress
sdd list-phases {spec-id}

# Find tasks by status
sdd query-tasks {spec-id} --status pending
sdd query-tasks {spec-id} --status blocked

# Find tasks by type
sdd query-tasks {spec-id} --type verify

# Get specific task details
sdd get-task {spec-id} {task-id}
```

### Update Metadata

```bash
# Update spec metadata fields
sdd update-frontmatter {spec-id} status "active"
sdd update-frontmatter {spec-id} owner "user@example.com"
sdd update-frontmatter {spec-id} priority "high"

# Sync metadata with hierarchy state
sdd sync-metadata {spec-id}
```

### Update Task Metadata

Update metadata fields for individual tasks using `update-task-metadata`:

```bash
# Update predefined metadata fields using individual flags
sdd update-task-metadata {spec-id} {task-id} --file-path "src/auth.py"
sdd update-task-metadata {spec-id} {task-id} --description "Updated task description"
sdd update-task-metadata {spec-id} {task-id} --task-category "implementation"
sdd update-task-metadata {spec-id} {task-id} --actual-hours 2.5

# Update custom metadata fields using JSON
sdd update-task-metadata {spec-id} {task-id} \
  --metadata '{"focus_areas": ["performance", "security"], "priority": "high"}'

# Combine individual flags with custom JSON (flags take precedence)
sdd update-task-metadata {spec-id} {task-id} \
  --file-path "src/middleware.py" \
  --metadata '{"focus_areas": ["authentication"], "complexity": "medium"}'

# Complex nested metadata structures
sdd update-task-metadata {spec-id} {task-id} \
  --metadata '{
    "focus_areas": ["error handling", "edge cases"],
    "blockers": ["clarification needed", "dependency X"],
    "implementation_notes": {
      "approach": "incremental",
      "testing_strategy": "unit + integration"
    }
  }'
```

**Available individual flags:**
- `--file-path` - File path associated with this task
- `--description` - Task description
- `--task-category` - Category (e.g., implementation, testing, documentation)
- `--actual-hours` - Actual hours spent on task
- `--status-note` - Status note or completion note
- `--verification-type` - Verification type (auto, manual, none)
- `--command` - Command executed

**Custom metadata with --metadata:**
- Accepts JSON object with any custom fields
- Useful for tracking focus areas, priorities, blockers, complexity, etc.
- Merges with individual flags (individual flags take precedence)
- Supports nested structures and arrays

**Common use cases:**
```bash
# Track focus areas for investigation tasks
sdd update-task-metadata {spec-id} task-1-1 \
  --metadata '{"focus_areas": ["code-doc structure", "skill patterns"]}'

# Document blockers and complexity
sdd update-task-metadata {spec-id} task-2-3 \
  --metadata '{"blockers": ["API design unclear"], "complexity": "high"}'

# Track implementation approach
sdd update-task-metadata {spec-id} task-3-2 \
  --metadata '{
    "approach": "refactor existing code",
    "estimated_subtasks": 4,
    "dependencies": ["task-3-1"]
  }'
```

### Validation

For comprehensive spec validation, use the sdd-validate subagent:

```
Task(
  subagent_type: "sdd-toolkit:sdd-validate-subagent",
  prompt: "Validate specs/active/{spec-id}.json",
  description: "Validate spec file"
)
```

For deep audits:

```bash
sdd audit-spec {spec-id}
```

## JSON Structure Reference

### Task Status Values

- `pending` - Not yet started
- `in_progress` - Currently being worked on
- `completed` - Successfully finished
- `blocked` - Cannot proceed due to dependencies or issues

### Journal Entry Structure

Journal entries are stored in a top-level `journal` array:

```json
{
  "journal": [
    {
      "timestamp": "2025-10-18T14:30:00Z",
      "entry_type": "decision",
      "title": "Brief title",
      "task_id": "task-1-2",
      "author": "claude-sonnet-4.5",
      "content": "Detailed explanation",
      "metadata": {}
    }
  ]
}
```

### Verification Result Structure

Stored in verification task metadata:

```json
{
  "verify-1-1": {
    "metadata": {
      "verification_result": {
        "date": "2025-10-18T16:45:00Z",
        "status": "PASSED",
        "output": "Command output",
        "notes": "Additional context"
      }
    }
  }
}
```

### Folder Structure

```
specs/
├── pending/      # Backlog - planned but not activated
├── active/       # Currently being implemented
├── completed/    # Finished and verified
└── archived/     # Old or superseded
```

## Best Practices

### When to Update

- **Update immediately** - Don't wait; update status as work happens
- **Be specific** - Vague notes aren't helpful later
- **Document WHY** - Always explain rationale, not just what changed

### Journaling

- **Link to evidence** - Reference tickets, PRs, discussions
- **Decision rationale** - Explain why decisions were made
- **Use bulk-journal** - Efficiently document multiple completed tasks

### Multi-Tool Coordination

- **Read before write** - Always load latest state before updating
- **Update your tasks only** - Don't modify other tools' work
- **Clear handoffs** - Add journal entry when passing work to another tool

### File Organization

- **Clean transitions** - Move specs promptly when status changes
- **Never rename specs** - Spec file names are based on spec_id
- **Backup before changes** - CLI handles automatic backups

## Troubleshooting

### Spec File Corruption

**Recovery:**
1. Check for backup: `specs/active/{spec-id}.json.backup`
2. If no backup, regenerate from original spec
3. Manually mark completed tasks based on journal entries
4. Validate repaired file

### Orphaned Tasks

**Resolution:**
1. If task in file but not in spec: Check if spec was updated; remove if confirmed deleted
2. If task in spec but not in file: Regenerate spec file using sdd-plan
3. Always preserve completed task history even if spec changed

### Merge Conflicts

**When:** Multiple tools update state simultaneously

**Resolution:**
1. Load both versions
2. Identify conflicting nodes
3. Choose most recent update (check timestamps)
4. Recalculate progress from leaf nodes up
5. Validate merged state

## Common Mistakes

### Using `--entry-type completion`

**Error:**
```bash
sdd add-journal: error: argument --entry-type: invalid choice: 'completion'
Exit code: 2
```

**Cause:** Confusing the `bulk-journal --template` option with `add-journal --entry-type`

**Fix:** Use `--entry-type status_change` instead:

```bash
# ❌ WRONG - "completion" is not a valid entry type
sdd add-journal {spec-id} --task-id {task-id} --entry-type completion --title "..." --content "..."

# ✅ CORRECT - Use "status_change" for task completion entries
sdd add-journal {spec-id} --task-id {task-id} --entry-type status_change --title "Task Completed" --content "..."

# ✅ ALTERNATIVE - Use bulk-journal with completion template
sdd bulk-journal {spec-id} --template completion
```

**Why this happens:** The `bulk-journal` command has a `--template` parameter that accepts `completion` as a value for batch journaling. However, `add-journal` has an `--entry-type` parameter with different valid values. These are two separate parameters for different purposes:
- `bulk-journal --template completion` - Batch journal multiple completed tasks using a template
- `add-journal --entry-type status_change` - Add individual journal entry about task status changes

### Reading Spec Files Directly

**Error:** Using Read tool, cat, grep, or jq on spec files

**Fix:** Always use `sdd` CLI commands:

```bash
# ❌ WRONG - Wastes context tokens and bypasses validation
Read("specs/active/my-spec.json")
cat specs/active/my-spec.json

# ✅ CORRECT - Use sdd CLI for structured access
sdd status-report {spec-id}
sdd get-task {spec-id} {task-id}
sdd query-tasks {spec-id} --status pending
```

## Command Reference

### Status Management
- `update-status` - Change task status
- `mark-blocked` - Mark task as blocked with reason
- `unblock-task` - Unblock a task with resolution

### Documentation
- `add-journal` - Add journal entry to spec
- `bulk-journal` - Add entries for multiple completed tasks
- `check-journaling` - Detect tasks without journal entries
- `add-verification` - Document verification results
- `execute-verify` - Run verification task automatically

### Lifecycle
- `activate-spec` - Move spec from pending/ to active/
- `move-spec` - Move spec between folders
- `complete-spec` - Mark complete and move to completed/

### Query & Reporting
- `status-report` - Get progress and status summary
- `query-tasks` - Filter tasks by status, type, or parent
- `get-task` - Get detailed task information
- `list-phases` - List all phases with progress
- `list-blockers` - List all blocked tasks
- `check-complete` - Verify if spec/phase is ready to complete

### Metadata
- `update-task-metadata` - Update task metadata fields (individual flags or JSON)
- `update-frontmatter` - Update spec metadata fields
- `sync-metadata` - Synchronize metadata with hierarchy

### Validation
- `validate-spec` - Check spec file consistency
- `audit-spec` - Deep audit of spec file integrity

### Common Flags
- `--dry-run` - Preview changes without saving
- `--verify` - Auto-run verify tasks on completion

## Systematic Spec Modification

For **structural modifications** to specs (not progress tracking), use `Skill(sdd-toolkit:sdd-modify)`.

### What is Systematic Spec Modification?

Systematic modification applies structured changes to specs with:
- Automatic backup before changes
- Validation after changes
- Transaction support with rollback
- Preview before applying (dry-run mode)

### Common Use Cases

**1. Apply Review Feedback**

After running sdd-fidelity-review or sdd-plan-review:

```bash
# Parse review feedback into structured modifications
sdd parse-review my-spec-001 --review reports/review.md --output suggestions.json

# Preview modifications
sdd apply-modifications my-spec-001 --from suggestions.json --dry-run

# Apply modifications
sdd apply-modifications my-spec-001 --from suggestions.json
```

**2. Bulk Modifications**

Apply multiple structural changes at once:

```bash
# Create modifications.json with desired changes
# (update task descriptions, add verifications, correct metadata)

# Apply bulk modifications
sdd apply-modifications my-spec-001 --from modifications.json
```

**3. Update Task Descriptions**

Make task descriptions more specific based on implementation learnings:

```json
{
  "modifications": [
    {
      "operation": "update_task",
      "task_id": "task-2-1",
      "field": "description",
      "value": "Implement OAuth 2.0 authentication with PKCE flow and JWT tokens"
    }
  ]
}
```

### When to Use sdd-modify

Use `Skill(sdd-toolkit:sdd-modify)` when you need to:
- Apply review feedback from sdd-fidelity-review or sdd-plan-review
- Update task descriptions for clarity (beyond just journaling)
- Add verification steps discovered during implementation
- Make multiple structural changes at once
- Ensure changes are validated and safely applied

### See Also

- **Skill(sdd-toolkit:sdd-modify)** - Full documentation on systematic spec modification
- **skills/sdd-modify/examples/** - Detailed workflow examples
- **sdd parse-review --help** - Parse review reports into modification format
- **sdd apply-modifications --help** - Apply modifications with validation
