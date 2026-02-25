---
name: dispatch
description: "Use when multiple tasks are ready and you want to assign them to parallel workers"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion, TeamCreate, TaskCreate, TaskUpdate, TaskList, SendMessage, Task
---

# Dispatch Teammates: $ARGUMENTS

You are an orchestrator dispatching parallel Agent Teams teammates for beads tasks.

## Parse Arguments

Arguments: `$ARGUMENTS`

Parse the following patterns:
- `--count N` — Auto-select N ready tasks from `bd ready`
- `--plan-first` — Force all teammates into plan approval mode
- `--no-plan` — Disable auto risk detection, all use bypassPermissions
- `--yes` — Skip dispatch confirmation (used by /auto-run for autonomous operation)
- `--model opus|sonnet` — Override model selection for all tasks
- `<task-id>` — Specific task to dispatch
- `<task-id>:"context"` — Task with custom context (e.g., `MoneyPrinter-ajq:"Use PriceCache"`)

If no arguments provided, default to `--count 3`.

## Step 1: Identify Tasks

**If `--count N` was specified (or defaulted):**

Run `bd ready` to get available tasks:
```bash
bd ready
```

Select the first N tasks that are:
- **Not epics** — Prefer concrete tasks (type: task, feature, bug) over epics
- **High priority first** — P0 > P1 > P2 > P3 > P4
- **Not already in_progress** — Only ready tasks

**If specific tasks were provided:**

Validate each task exists:
```bash
bd show <task-id>
```

## Step 2.5: Risk Assessment (Plan Mode Detection + Risk Tiers)

**Skip if `--no-plan` was specified.** If `--plan-first` was specified, mark ALL tasks `[PLAN]`.

### Risk Tier Configuration

First, check for a project-level review config:

```bash
cat .claude/review.json 2>/dev/null || cat .claude/risk-tiers.json 2>/dev/null || echo "No review config found"
```

**With review config:** Match task file paths (from `bd show` description or related files) against tier patterns. The highest matching tier determines the task's risk level:

| Risk Tier | Dispatch Mode |
|-----------|---------------|
| critical | `[PLAN]` |
| high | `[PLAN]` |
| medium | `[AUTO]` |
| low | `[AUTO]` |

**Without review config (keyword fallback):** For each task, check its title + description (from `bd show`) for high-risk keywords (case-insensitive):

- **Security**: `auth`, `authentication`, `authorization`, `encrypt`, `secret`, `password`, `token`, `credential`
- **Data**: `migration`, `migrate`, `schema change`, `drop table`, `delete data`
- **Financial**: `payment`, `billing`, `subscription`, `transaction`
- **Architectural**: `architecture`, `redesign`, `rewrite`, `refactor core`

Mark matching tasks `[PLAN]`, others `[AUTO]`.

## Step 2.6: Interface Detection (Peer Messaging)

For each pair of dispatched tasks, check if they share a dependency edge *within this dispatch batch*. Run `bd show <id>` for each task and check BLOCKS/BLOCKED BY fields. Only flag pairs where BOTH tasks are being dispatched together — external dependencies are irrelevant for peer messaging.

Build peer pairs: `[(task-A, task-B, "description of shared interface")]`

## Step 2.7: Model Selection

**If `--model` flag was specified:** Use that model for ALL tasks (overrides all other logic).

**With review config:**

| Risk Tier | Model |
|-----------|-------|
| critical | opus |
| high | opus |
| medium | sonnet |
| low | sonnet |

**Without review config (keyword fallback):**
- Keywords `architecture`, `security`, `auth`, `migration`, `rewrite`, `redesign` in task title/description → `opus`
- Everything else → `sonnet`

Display the model in the dispatch summary: `[AUTO/sonnet]` or `[PLAN/opus]`.

## Step 2: Generate Context

For each task without explicit context:

1. Read the task details from `bd show <task-id>`
2. Look for related patterns in the codebase:
   - Check if similar files exist that the worker should follow
   - Look for recently completed dependencies
3. Generate a brief (1-2 sentence) context that helps the teammate start faster

Example contexts:
- "Use sector_etfs.txt format from existing tickers/ directory"
- "Follow the pattern in backtesting/cache.py for data storage"
- "Depends on completed MoneyPrinter-xyz, can use its output"

## Step 3: Confirm Dispatch

Present a summary to the user:

```
Ready to dispatch N teammates:

1. <task-id> (P1 <type>) [PLAN/opus]: <title>
   Context: "<generated or provided context>"

2. <task-id> (P2 <type>) [AUTO/sonnet]: <title>
   Context: "<generated or provided context>"

...
```

The `[PLAN/AUTO]` tags indicate dispatch mode. The `[opus/sonnet]` tags indicate the model selection from Step 2.7.

**If `--yes` was specified:**
Skip the AskUserQuestion confirmation and proceed directly to Step 4.

**Otherwise, use AskUserQuestion to confirm:**

Ask: "Confirm dispatch of N teammates?"
- Options: "Yes, dispatch" / "No, cancel"
- multiSelect: false

**Wait for explicit user confirmation before proceeding.**

If user selects "No, cancel", abort dispatch.

## Step 4: Create Team and Spawn Teammates

1. **Create the team** using TeamCreate with a descriptive name based on the project/tasks.

2. **Create tasks** in the Agent Teams task list using TaskCreate — one per beads task. Include in each task description:
   - The beads task ID
   - Task title and description from `bd show`
   - The generated context
   - Clear instruction: "Run `/start-task <task-id>` to begin. Run `/finish-task <task-id>` when done."

3. **Set up dependencies** between tasks using TaskUpdate if the beads tasks have dependencies.

4. **Spawn teammates** using the Task tool with `team_name` parameter and `isolation: "worktree"` — one per task. Each teammate should be a `general-purpose` subagent type. Give each teammate a descriptive name based on the task (e.g., the task short ID).

   **Mode selection:**
   - `[AUTO]` tasks: spawn with `mode: "bypassPermissions"` (default behavior)
   - `[PLAN]` tasks: spawn with `mode: "plan"`

   **Model selection:** Pass `model: "<selected>"` from Step 2.7 in the Task tool call (e.g., `model: "opus"` or `model: "sonnet"`).

   **Spawn prompt for `[AUTO]` tasks:**
   ```
   You are a worker on team "<team-name>". Your task:

   <task title and description from bd show>

   Context: <generated context>

   Instructions:
   1. Run `/start-task <task-id>` to claim the task and verify your environment
      (You're already in an isolated worktree with .env files set up)
   2. Implement the task according to the acceptance criteria
   3. Run `/finish-task <task-id>` when tests pass and implementation is complete
   4. Report back to the team lead when done
   ```

   **Spawn prompt for `[PLAN]` tasks:**
   ```
   You are a worker on team "<team-name>" spawned in PLAN MODE. Your task:

   <task title and description from bd show>

   Context: <generated context>

   Instructions:
   1. Run `/start-task <task-id>` to claim the task and gather context
      (You're already in an isolated worktree with .env files set up)
   2. Create a detailed implementation plan
   3. Call ExitPlanMode to submit your plan for lead approval
   3a. IMMEDIATELY after ExitPlanMode, send a direct message to the team lead
       using SendMessage type="message":
       "PLAN APPROVAL NEEDED for <task-id>. I've submitted my plan via
       ExitPlanMode. Please review and respond with:
       SendMessage type='plan_approval_response', request_id='<from the request>',
       recipient='<my name>', approve=true/false.
       I am blocked until you respond."
   4. WAIT — the lead will review and approve/reject your plan
   5. After approval, implement the task
   6. Run `/finish-task <task-id>` when tests pass and implementation is complete
   7. Report back to the team lead when done
   ```

   **Peer coordination (if peer pairs detected in Step 2.6):**
   For tasks with peers, append to the spawn prompt:
   ```
   Peer coordination:
   Your teammate "<peer-name>" is working on <peer-task-id> (<brief desc>).
   Your tasks share a dependency. If you make decisions about shared interfaces
   (API contracts, data schemas, file formats), message <peer-name> using
   SendMessage to agree before implementing.
   ```

   **After spawning all teammates but before assigning tasks:**
   If any `[PLAN]` teammates were spawned:
     Do not consider dispatch complete until you have handled all plan approval
     requests. Remain attentive to incoming messages from plan-mode teammates.

5. **Assign tasks** using TaskUpdate to set the owner of each task to the corresponding teammate name.

## Step 4.5: Verify Worktree Isolation

After spawning and assigning all teammates, verify that worktree isolation actually succeeded. This is critical — `isolation: "worktree"` can fail silently, leaving workers running in the main repo.

### 4.5.1: Wait for initialization

```bash
sleep 10
```

Workers need time to register in the team config. If the team was just created, give the system 10 seconds to stabilize.

### 4.5.2: Check team config

```bash
cat ~/.claude/teams/<team-name>/config.json
```

For each spawned worker in the `members` array (skip the team-lead entry), check:
- **`cwd` field**: Must contain `.claude/worktrees/` — NOT the main repo root path

Determine the main repo path for comparison:
```bash
git rev-parse --show-toplevel
```

Build two lists:
- **Isolated workers**: `cwd` is under `.claude/worktrees/`
- **Non-isolated workers**: `cwd` matches the main repo root

**If team config is missing or has no worker members after 10s**, wait another 10 seconds and re-check. If still missing, treat as total failure.

### 4.5.3: Corroborate with git worktree list

```bash
git worktree list
```

Cross-reference: each isolated worker's `cwd` should appear as a worktree entry. Log any discrepancies but trust the team config `cwd` as the primary signal (a fast-completing worker's worktree may have been cleaned up already).

### 4.5.4: Handle failures

**If ALL workers are properly isolated** → proceed to Step 5.

**If ANY workers failed isolation:**

1. **Shut down non-isolated workers immediately** — they are sharing the main repo:
   ```
   For each non-isolated worker:
     SendMessage type="shutdown_request" recipient="<worker-name>"
       content="Worktree isolation failed — you are running in the main repo, not an isolated worktree. Shutting down to prevent conflicts."
   ```

2. **Check main repo state:**
   ```bash
   git status
   git branch --show-current
   ```
   If the main repo has modifications or is on the wrong branch, report this to the user. Do NOT auto-clean — the user decides.

3. **Report clearly:**
   ```
   WARNING: Worktree isolation failed for N of M workers.

   Isolated (OK):
   - <name>: <task-id> — running in <cwd path>

   Failed (shut down):
   - <name>: <task-id> — was running in main repo (no worktree created)

   Main repo status: <clean/dirty> on branch <branch-name>
   Failed workers have been sent shutdown requests.
   ```

4. **If `--yes` was specified (auto-run mode):**
   - Do NOT prompt the user.
   - Unassign failed workers' tasks: `TaskUpdate` with owner set to empty string for each.
   - Log the failure. Failed tasks remain open in beads and return to `bd ready` for next dispatch.
   - Continue to Step 5 with only the isolated workers.

5. **If `--yes` was NOT specified (interactive mode):**
   - Use `AskUserQuestion`: "N workers failed worktree isolation and were shut down. Their tasks remain open. What should we do?"
     - Option 1: "Re-dispatch failed tasks" — run `/dispatch <failed-task-ids>` again
     - Option 2: "Continue with isolated workers only"
     - Option 3: "Abort entire dispatch" — shutdown ALL workers, exit

## Step 5: Post-Dispatch Summary

After all teammates are spawned, provide a summary:

```
Dispatch complete: N teammates spawned

Team: <team-name>
Teammates:
1. <name>: <task-id> — <title>
2. <name>: <task-id> — <title>
...

**If all workers verified isolated (Step 4.5 passed):**
All teammates verified running in isolated worktrees.

**If any workers failed isolation (from Step 4.5):**
WARNING: N of M workers failed worktree isolation.
Failed workers were shut down. Their tasks remain open for re-dispatch.
Failed tasks: <task-id-1>, <task-id-2>, ...
Only N workers are active.

Each active teammate will:
1. Run /start-task to claim the task and verify environment
2. Implement the task
3. Run /finish-task when tests pass

Use Shift+Up/Down to switch between teammates (in-process mode).
The team lead will receive notifications as teammates complete work.

IMPORTANT: Before ending this session, run /reconcile-summary to sync
all teammate work back to beads.
```

**If plan-mode teammates were spawned, add:**

```
CRITICAL — Plan-mode teammates are NOW WAITING for your approval.
Handle plan approvals BEFORE doing anything else.

When you receive a plan approval message from a teammate:
1. Review the plan in the plan_approval_request message
2. Call SendMessage with these EXACT parameters:
   - type: "plan_approval_response"
   - request_id: "<the request_id from the plan_approval_request JSON>"
   - recipient: "<teammate name>"
   - approve: true (or false with content: "<feedback>")
3. Do NOT respond with a plain text message — you MUST use the SendMessage tool

If multiple PLAN teammates were spawned, you will receive multiple
plan_approval_requests. Handle EACH one individually with its own request_id.
```

## Error Handling

- **No ready tasks**: Suggest running `/orient` first to identify work
- **Task doesn't exist**: Skip it, warn the user, continue with valid tasks
- **All tasks invalid**: Abort with clear error message
- **Teammate spawn fails**: Report the error, continue with remaining tasks
- **Worktree isolation fails**: Shut down non-isolated workers (SendMessage shutdown_request), report failure, continue with isolated workers only. Tasks for failed workers remain open in beads. In `--yes` mode (auto-run), unassign and let next dispatch cycle retry. In interactive mode, offer re-dispatch, continue, or abort.

## Examples

**Auto-select 3 tasks (default):**
```
/dispatch
```

**Auto-select specific count:**
```
/dispatch --count 5
```

**Specific tasks:**
```
/dispatch MoneyPrinter-ajq MoneyPrinter-4b3
```

**With custom context:**
```
/dispatch MoneyPrinter-ajq:"Use existing ticker format"
```

**Force all tasks to use Opus:**
```
/dispatch --count 3 --model opus
```
