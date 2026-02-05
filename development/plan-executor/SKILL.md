---
name: plan-executor
description: Execute and coordinate work on PLAN files with phased breakdown. Tracks progress via JSON state, coordinates worker sub-agents in worker mode, and manages commits. Use when user references a PLAN file or asks to continue/execute a plan.
---

# Plan Executor Skill

This skill executes and coordinates work on existing PLAN files. It handles progress tracking, worker coordination (in worker mode), commit management, and phase advancement.

## When to Use This Skill

Use this skill when:
- User references an existing PLAN file (e.g., `@PLAN-auth.md`)
- User asks to "continue the plan" or "execute the plan"
- User asks to "work on" or "resume" a project with a PLAN file
- User wants to see plan status or progress

Do NOT use this skill when:
- User wants to CREATE a new plan (use `plan-generator` skill instead)
- User wants to modify the plan structure (add/remove phases)

## CRITICAL RULES

**These rules MUST be followed at all times:**

### 1. ALWAYS Respect Execution Mode

The execution mode is defined in the JSON state block (`execution.mode`). **You MUST follow it:**

- **If `mode` is `"worker"`**: You are a COORDINATOR. Do NOT execute steps directly. Launch `plan-worker` sub-agents to do the work. NEVER perform implementation work yourself in worker mode.
- **If `mode` is `"direct"`**: Execute steps directly in the main session.

**On resume**: Re-read the JSON state and respect the mode. Do not switch modes.

### 2. ALWAYS Update State Immediately

State updates MUST happen in real-time, not batched:

- **BEFORE starting ANY step**: Run `scripts/plan-tool start <file> <step-id>`
- **IMMEDIATELY after completing a step**: Run `scripts/plan-tool complete <file> <step-id> --summary "..."`
- **Never skip state updates** - if the session is interrupted, state should reflect reality

This ensures that if execution is interrupted, the plan can resume from the correct point.

---

## Understanding Plan State

PLAN files contain a JSON state block at the end wrapped in HTML comment markers:

```
<!--PLAN-STATE
{
  "schema_version": "1.0",
  "execution": {
    "mode": "direct",           // or "worker"
    "auto_continue": false,     // auto-advance to next phase when current completes
    "commit_after_phase": false,
    "include_plan_in_commit": true
  },
  "current_phase": 0,           // -1 means all complete
  "phases": [
    {
      "id": 0,
      "name": "Setup",
      "steps": [
        { "id": "0.1", "status": "pending" },
        { "id": "0.2", "status": "completed", "summary": "..." }
      ]
    }
  ]
}
PLAN-STATE-->
```

### Step Status Values

- `pending` - Not started
- `in_progress` - Currently being worked on (only ONE at a time)
- `completed` - Finished successfully
- `blocked` - Cannot proceed (includes `blocker` field with reason)

### Initializing Plan State

When a PLAN file does not have a JSON state block, initialize it before starting execution:

```bash
scripts/plan-tool init <file> [--mode direct|worker] [--auto-continue] [--commit] [--no-plan-in-commit]
```

The `init` command parses the markdown headings to discover phases and steps, then generates the JSON state block at the end of the file.

**Options:**
- `--mode direct|worker`: Execution mode (default: direct)
- `--auto-continue`: Enable auto-advancement between phases
- `--commit`: Enable commits after each phase
- `--no-plan-in-commit`: Exclude PLAN file from commits

Example:
```bash
scripts/plan-tool init PLAN-auth.md --mode worker --auto-continue --commit --no-plan-in-commit
```

### Reading Plan State

When starting execution:
1. Read the entire PLAN file
2. Check if JSON state block exists (look for `<!--PLAN-STATE` marker)
3. **If no JSON state block exists**: Initialize it using `scripts/plan-tool init` with options based on the execution preferences in the Instructions section
4. Parse the JSON state block to understand:
   - Which execution mode is active (`direct` or `worker`)
   - Which phase is current (`current_phase`)
   - Which steps are `pending`, `in_progress`, `completed`, or `blocked`
5. Check for any `blocked` steps that need resolution
6. Identify the next actionable step(s)

## Progress Tracking Commands

Use the `scripts/plan-tool` script (relative to this skill directory) to manage JSON state updates.

### Starting a Step

Before beginning work on a step:

```bash
scripts/plan-tool start <file> <step-id>
```

Example:
```bash
scripts/plan-tool start PLAN-auth.md 1.2
```

**Note:** Only ONE step can be `in_progress` at a time. Starting a new step automatically resets any previously in-progress step to `pending`.

### Completing a Step

After successfully finishing a step:

```bash
scripts/plan-tool complete <file> <step-id> [--summary "..."]
```

Example:
```bash
scripts/plan-tool complete PLAN-auth.md 1.2 --summary "Added JWT validation middleware with RS256 support"
```

**Auto-advancement:** If all steps in the current phase are completed and `auto_continue` is enabled, the phase automatically advances.

### Blocking a Step

When a step cannot proceed due to an issue:

```bash
scripts/plan-tool block <file> <step-id> --reason "..."
```

Example:
```bash
scripts/plan-tool block PLAN-auth.md 1.3 --reason "Redis not configured - refresh tokens need persistent storage"
```

### Unblocking a Step

To clear a blocked status after resolving the issue:

```bash
scripts/plan-tool unblock <file> <step-id>
```

### Advancing Phase

To manually advance to the next phase:

```bash
scripts/plan-tool next-phase <file> [--force]
```

Use `--force` to advance even if some steps are incomplete or blocked (not recommended).

## Direct Mode Execution

In direct mode, execute steps directly in the main Claude Code session.

### Execution Flow

1. **Identify next step**: Find the first `pending` step in the current phase
2. **Mark as in-progress**: Run `scripts/plan-tool start`
3. **Execute the step**: Perform all work described in the step
4. **Document completion**: Add notes under the step heading in markdown:
   ```markdown
   ### Step 1.2: Implement user validation
   Original step description...
   - **Completed:** Added email regex validation and password strength check
   - **Decision:** Used zxcvbn library for password scoring
   ```
5. **Update state**: Run `scripts/plan-tool complete` with a brief summary
6. **Repeat**: Continue with next pending step

### Stopping Conditions

Only stop when:
- An entire phase is complete AND `auto_continue` is disabled (ask user if they want to continue)
- An actual error or blocker occurs
- User explicitly requests to pause
- All phases are complete

**If `auto_continue` is enabled:** Do NOT stop between phases. Immediately proceed to the next phase.

### Adding Implementation Notes

After completing steps, add detailed notes to the **Notes & Decisions** section:

```markdown
## Notes & Decisions

### Phase 1: Core Implementation (Completed)
- Implemented JWT generation using RS256 algorithm
- Chose 15-minute expiry for access tokens based on security best practices
- Added refresh token rotation to prevent token reuse
```

## Worker Mode Execution

In worker mode, delegate step execution to `plan-worker` sub-agents. The main session acts as a coordinator.

### Coordinator Protocol

#### 1. Identify Next Work Batch

Parse the JSON state block to find steps with `"status": "pending"` in the current phase. Determine batch size by considering:

- **Step dependencies**: If step N+1 needs output from step N, batch them together
- **Complexity**: Steps involving multiple files, tests, or debugging -> smaller batches (1-2 steps)
- **Independence**: Simple, independent steps -> can batch more (3-5 steps)
- **Default**: 2-4 related steps per worker, or an entire phase if steps are simple

#### 2. Prepare Worker Context

Gather the information the worker needs:

- **Project goal**: 1-2 sentences from Project Overview
- **Specific steps**: Full descriptions from the plan
- **Relevant files**: List of files the worker will need to read or modify
- **Success criteria**: Derived from step descriptions
- **Inline examples**: Any relevant examples from the plan

#### 3. Mark Steps and Launch Worker

**BEFORE launching the worker**, mark all assigned steps as in-progress:

```bash
scripts/plan-tool start <file> <step-id>
```

Run this for EACH step being assigned to the worker.

Then launch the `plan-worker` sub-agent with this prompt structure:

```
**Project:** [Project name from plan]

**Goal:** [Brief goal from Project Overview section]

**Your Assignment:**
Execute the following steps from Phase N:
- Step N.X: [full description]
- Step N.Y: [full description]
- Step N.Z: [full description]

**Context Files to Read:**
- [path/to/file1] - [why it's relevant]
- [path/to/file2] - [why it's relevant]

**Success Criteria:**
- [Specific criterion derived from steps]
- [Another criterion]

**Constraints:**
- [Any project-specific constraints]
- [Technology requirements]

When done, provide your structured summary.
```

#### 4. Process Worker Results

When the worker returns its summary:

**For COMPLETED steps:**
```bash
scripts/plan-tool complete <file> <step-id> --summary "Summary from worker"
```

Add inline notes under the step heading:
```markdown
### Step N.X: [description]
Original step description...
- **Completed:** [1-2 sentence summary of what was done]
- **Decision:** [any notable decision, if applicable]
```

**For BLOCKED steps:**
```bash
scripts/plan-tool block <file> <step-id> --reason "Blocker description from worker"
```

Add blocker details under the step heading:
```markdown
### Step N.X: [description]
Original step description...
- **Blocked:** [description of the blocker]
```

Then report to user and ask how to proceed.

**Update Notes & Decisions section** with worker findings for the appropriate phase.

#### 5. Continue or Pause

- If more pending steps remain in the phase, launch another worker
- If phase is complete:
  - Create git commit if `commit_after_phase` is enabled
  - **If `auto_continue` is enabled**: Immediately proceed to the next phase
  - **If `auto_continue` is disabled**: Ask user if they want to continue
- If all phases are complete, report completion to user
- If blocker hit, wait for user guidance

## Phase Completion Handling

### Creating Commits

If `commit_after_phase` is enabled:

1. Stage all modified files from the phase
2. Check `include_plan_in_commit` setting:
   - If `true`: Include the PLAN file in the commit
   - If `false`: Keep PLAN file unstaged
3. Create commit with message describing the phase work

Example commit message:
```
feat(auth): Phase 1 - Implement JWT token generation

- Added generateToken() function with RS256 signing
- Created token validation middleware
- Implemented refresh token rotation
```

### Advancing to Next Phase

After a phase completes:

1. If `auto_continue` is enabled:
   - Log phase completion
   - Immediately begin work on next phase
   - Continue until all phases complete or a blocker occurs

2. If `auto_continue` is disabled:
   - Report phase completion to user
   - Ask: "Phase N is complete. Would you like to continue to Phase N+1?"
   - Wait for user confirmation before proceeding

### All Phases Complete

When `current_phase` becomes `-1`:
1. Report completion to user
2. Review the Completion Checklist in the PLAN file
3. Verify all items are satisfied
4. Suggest any final cleanup or documentation tasks

## Error Handling


### Handling Blocked Steps

When a step is blocked:

1. Run `scripts/plan-tool block` to mark it in the JSON state
2. Stop launching workers for steps that depend on the blocked step
3. Report to user with:
   - The step that is blocked
   - The reason for the blocker
   - Options to resolve:
     - Add a prerequisite step to fix the blocker
     - Skip the step (unblock then complete with note)
     - Provide guidance for another attempt

### Partial Completion

When a worker completes some but not all assigned steps:

1. Run `scripts/plan-tool complete` for each finished step
2. For incomplete steps:
   - Leave as `pending` if work can continue
   - Mark as `blocked` if there's an issue
3. Decide whether to:
   - Launch a new worker for remaining steps
   - Report to user if there's an issue

### Invalid State Recovery

If the JSON state becomes corrupted:

1. Attempt to parse and identify the issue
2. If recoverable, fix the JSON and continue
3. If not recoverable, report to user:
   - "The plan state appears corrupted. Would you like me to re-initialize it from the markdown headings?"
   - Use `scripts/plan-tool init` to rebuild state if user confirms

