---
name: dispatch
description: "Dispatch parallel Agent Teams teammates for beads tasks"
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

5. **Assign tasks** using TaskUpdate to set the owner of each task to the corresponding teammate name.

## Step 5: Post-Dispatch Summary

After all teammates are spawned, provide a summary:

```
Dispatch complete: N teammates spawned

Team: <team-name>
Teammates:
1. <name>: <task-id> — <title>
2. <name>: <task-id> — <title>
...

Each teammate runs in an isolated worktree (via isolation: "worktree") and will:
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
Plan-mode teammates will submit plans for your review.
When you receive a plan_approval_request, review the plan and respond:
- Approve: SendMessage type="plan_approval_response", approve=true
- Reject: SendMessage type="plan_approval_response", approve=false, content="<feedback>"
```

## Error Handling

- **No ready tasks**: Suggest running `/orient` first to identify work
- **Task doesn't exist**: Skip it, warn the user, continue with valid tasks
- **All tasks invalid**: Abort with clear error message
- **Teammate spawn fails**: Report the error, continue with remaining tasks

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
