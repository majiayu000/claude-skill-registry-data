---
name: hzl
description: OpenClaw's persistent task database. Coordinate sub-agents, checkpoint progress, survive session boundaries.
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---

# HZL: Persistent task tracking for agents

HZL (https://github.com/tmchow/hzl) is a local-first task ledger (database-backed, optionally cloud-synced for backup) that an agent can use to:

- plan multi-step work into projects + tasks
- checkpoint progress (so work survives session boundaries)
- coordinate sub-agents or multiple coding tools with leases
- generate reliable status reports ("what's done vs what's left")

This skill teaches an agent how to use the `hzl` CLI.

## When to use HZL

**OpenClaw has NO native task tracking tools.** Unlike Claude Code (which has TodoWrite) or Codex (which has update_plan), OpenClaw relies on memory and markdown files for tracking work. This makes HZL especially valuable for OpenClaw.

**Use HZL by default for any non-trivial task tracking:**

- Multi-step projects with real sequencing (dependencies) and handoffs
- Work that may outlive this session or span multiple tools/agents
- Orchestration: delegating work to sub-agents and needing recovery if they crash
- Anything where "resume exactly where we left off" matters
- **Any work you want to persist beyond this session**
- **Any work that needs structure (nesting, dependencies, progress tracking)**
- **Any work that benefits from a durable record of decisions or ownership**

Multi-session or multi-agent work are common reasons to use HZL, not requirements.
Use HZL for single-session, single-agent work when the task is non-trivial.

**Why HZL is the right choice for OpenClaw:**

Without HZL, OpenClaw tracks tasks in-context (burns space, fragments during compaction) or in markdown files (requires manual management, no nesting/dependencies, no dashboard). HZL provides:

- Persistent storage that survives session boundaries
- Nesting (parent tasks + subtasks) and dependencies
- Web dashboard for human visibility (`hzl serve`)
- Leases for multi-agent coordination
- Checkpoints for progress recovery

**Only skip HZL for:**

- Truly trivial, one-step tasks you will complete immediately in this session
- Time-based reminders/alerts (use OpenClaw Cron instead)
- Longform notes or knowledge capture (use a notes or memory system)

**Rule of thumb:** If you feel tempted to make a multi-step plan or there is any chance you will not finish in this session, use HZL.

Example: "Investigate failing tests and fix root cause" -> use HZL because it likely involves multiple subtasks, even if you expect to finish within a session.

Personal tasks: HZL is not a polished human to-do app, but it is usable for personal task tracking, and it can also serve as a backend for a lightweight UI.

## Core concepts

- **Project**: stable container. For OpenClaw, use a single `openclaw` project—this keeps `hzl task next` simple. Check `hzl project list` before creating.
- **Task**: top-level work item. For multi-step requests, this becomes a parent task.
- **Subtask**: breakdown of a task into parts (`--parent <id>`). Max 1 level of nesting. Parent tasks are organizational containers—never returned by `hzl task next`.
- **Checkpoint**: short progress snapshot to support recovery
- **Lease**: time-limited claim (prevents orphaned work in multi-agent flows)

## ⚠️ DESTRUCTIVE COMMANDS — READ FIRST

The following commands **PERMANENTLY DELETE HZL DATA** and cannot be undone:

| Command | Effect |
|---------|--------|
| `hzl init --force` | **DELETES ALL DATA.** Prompts for confirmation. |
| `hzl init --force --yes` | **DELETES ALL DATA WITHOUT CONFIRMATION.** Extremely dangerous. |
| `hzl task prune ... --yes` | **PERMANENTLY DELETES** old done/archived tasks and their event history. |

**AI agents: NEVER run these commands unless the user EXPLICITLY asks you to delete data.**

- `hzl init --force` deletes the entire event database: all projects, tasks, checkpoints, and history
- `hzl task prune` deletes only tasks in terminal states (done/archived) older than the specified age
- There is NO undo. There is NO recovery without a backup.

## Anti-pattern: Project Sprawl

Use a single `openclaw` project. Requests and initiatives become **parent tasks**, not new projects.

**Wrong (creates sprawl):**
```bash
hzl project create "garage-sensors"
hzl project create "query-perf"
# Now you have to track which project to query
```

**Correct (single project, parent tasks):**
```bash
# Check for existing project first
hzl project list

# Use single openclaw project
hzl task add "Install garage sensors" -P openclaw
# → Created task abc123

hzl task add "Wire sensor to hub" --parent abc123
hzl task add "Configure alerts" --parent abc123

# hzl task next --project openclaw always works
```

Why this matters:
- Projects accumulate forever; you'll have dozens of abandoned one-off projects
- `hzl task next --project X` requires knowing which project to query
- With a single project, `hzl task next --project openclaw` always works

## Sizing Parent Tasks

HZL supports one level of nesting (parent → subtasks). Scope parent tasks to completable outcomes.

**The completability test:** "I finished [parent task]" should describe a real outcome.
- ✓ "Finished installing garage motion sensors"
- ✓ "Finished fixing query performance"
- ✗ "Finished home automation" (open-ended domain, never done)
- ✗ "Finished backend work" (if frontend still pending for feature to ship)

**Scope by problem, not technical layer.** A full-stack feature (frontend + backend + tests) is usually one parent if it ships together.

**Split into multiple parents when:**
- Parts deliver independent value (can ship separately)
- You're solving distinct problems that happen to be related

**Adding context:** Use `-d` for details, `-l` for reference docs:
```bash
hzl task add "Install garage sensors" -P openclaw \
  -d "Per linked spec. Mount sensors at 7ft height." \
  -l docs/sensor-spec.md,https://example.com/wiring-guide
```

**Don't duplicate specs into descriptions**—this creates drift. Reference docs instead.

**If no docs exist**, include enough detail for another agent to complete the task:
```bash
hzl task add "Configure motion alerts" -P openclaw -d "$(cat <<'EOF'
Trigger alert when motion detected between 10pm-6am.
Use Home Assistant automation. Notify via Pushover.
EOF
)"
```
Description supports markdown (16KB max).

## Core Workflows

**Setup:**
```bash
hzl project list                    # Always check first
hzl project create openclaw         # Only if needed
```

**Adding work:**
```bash
hzl task add "Feature X" -P openclaw -s ready         # Ready to claim
hzl task add "Subtask A" --parent <id>                # Subtask
hzl task add "Subtask B" --parent <id> --depends-on <subtask-a-id>  # With dependency
```

**Working on a task:**
```bash
hzl task next -P openclaw                # Next available task
hzl task next --parent <id>              # Next subtask of parent
hzl task next -P openclaw --claim        # Find and claim in one step
hzl task claim <id>                      # Claim specific task
hzl task checkpoint <id> "milestone X"   # Notable progress or before pausing
```

**Changing status:**
```bash
hzl task set-status <id> ready           # Make claimable (from backlog)
hzl task set-status <id> backlog         # Move back to planning
```
Statuses: `backlog` → `ready` → `in_progress` → `done` (or `blocked`)

**When blocked:**
```bash
hzl task block <id> --comment "Waiting for API keys from DevOps"
hzl task unblock <id>                    # When resolved
```

**Finishing work:**
```bash
hzl task comment <id> "Implemented X, tested Y"  # Optional: final notes
hzl task complete <id>

# After completing a subtask, check parent:
hzl task show <parent-id> --json         # Any subtasks left?
hzl task complete <parent-id>            # If all done, complete parent
```

**Troubleshooting:**
| Error | Fix |
|-------|-----|
| "not claimable (status: backlog)" | `hzl task set-status <id> ready` |
| "Cannot complete: status is X" | Claim first: `hzl task claim <id>` |

---

## Extended Reference (look up as needed — skip on first read)

```bash
# Setup
hzl init                                      # Initialize (safe, won't overwrite)
hzl init --reset-config                       # Reset config to default location
hzl status                                    # Database mode, paths, sync state
hzl doctor                                    # Health check for debugging

# Create with options
hzl task add "<title>" -P openclaw --priority 2 --tags backend,auth
hzl task add "<title>" -P openclaw --depends-on <other-id>
hzl task add "<title>" -P openclaw -s ready --assignee <name>         # Pre-assign owner
hzl task add "<title>" -P openclaw -s ready --assignee <name> --author <name>  # Optional delegation attribution
hzl task add "<title>" -P openclaw -s in_progress --assignee <name>  # Create and claim

# List and find
hzl task list -P openclaw --available        # Ready tasks with met dependencies
hzl task list -P openclaw --assignee <agent-id>  # Tasks currently assigned to a specific agent
hzl task list --parent <id>                  # Subtasks of a parent
hzl task list --root                         # Top-level tasks only

# Dependencies
hzl task add-dep <task-id> <depends-on-id>
hzl task remove-dep <task-id> <depends-on-id>

# Metadata and project changes
hzl task update <task-id> --priority 3 --author <name>   # Optional attribution
hzl task move <task-id> openclaw --author <name>         # Optional attribution (for project consolidation)
hzl validate                                 # Check for circular dependencies

# Web Dashboard
hzl serve                    # Start on port 3456 (network accessible)
hzl serve --host 127.0.0.1   # Restrict to localhost only
hzl serve --background       # Fork to background
hzl serve --status           # Check if running
hzl serve --stop             # Stop background server

# Multi-agent recovery
hzl task claim <id> --assignee <agent-id> --lease 30
hzl task stuck
hzl task steal <id> --if-expired --assignee <agent-id>
```

Tip: When a tool needs to parse output, prefer `--json`.

## Authorship tracking

HZL tracks authorship at two levels:

| Concept | What it tracks | Set by |
|---------|----------------|--------|
| **Assignee** | Who owns the task | `--assignee` on `claim` or `add` |
| **Event author** | Who performed an action | `--author` on mutating commands (except `claim`, which uses `--assignee`) |

`--author` is optional. Skip it when one orchestrator is tracking its own work or sub-agents do not expose stable identities. Use it when handoffs or accountability need explicit actor attribution.

The `--assignee` flag on `claim` and `add` sets task ownership. The `--author` flag records who performed each action:

Decision policy for OpenClaw agents:
1. Default: omit `--author`.
2. Add `--author` when actor != assignee (delegation/handoff/audit trail).
3. `task claim` has no `--author`; `--assignee` is recorded as event author.
4. `task steal` should use `--assignee` for new ownership; add `--author` only when actor differs from the assignee. (`--owner` is a deprecated alias.)
5. For `update`, `move`, `add-dep`, `remove-dep`, `checkpoint`, and `comment`, add `--author` only when attribution matters.

```bash
# Alice owns the task
hzl task claim 1 --assignee alice

# Clara assigns ownership to Kenji at creation time
hzl task add "Implement auth flow" -P openclaw -s ready --assignee kenji --author clara

# Bob adds a checkpoint (doesn't change ownership)
hzl task checkpoint 1 "Reviewed the code" --author bob

# Task is still assigned to Alice, but checkpoint was recorded by Bob

# Clara moves ownership to Kenji while keeping attribution
hzl task steal 1 --if-expired --assignee kenji --author clara
```

For AI agents that need session tracking, use `--agent-id` on claim:
```bash
hzl task claim 1 --assignee "Claude Code" --agent-id "session-abc123"
```

## Recommended patterns

### Start a multi-step project

1) Use the single `openclaw` project (create only if it doesn't exist).
2) Create a parent task for the initiative.
3) Decompose into subtasks with dependencies.
4) Validate.

```bash
# Check if project exists first
hzl project list
# Create only if needed
hzl project create openclaw

# Parent task for the initiative
hzl task add "Implement auth system" -P openclaw --priority 3
# → abc123

# Subtasks with sequencing
hzl task add "Clarify requirements + acceptance criteria" --parent abc123 --priority 5
hzl task add "Design API + data model" --parent abc123 --priority 4 --depends-on <reqs-id>
hzl task add "Implement endpoints" --parent abc123 --priority 3 --depends-on <design-id>
hzl task add "Write tests" --parent abc123 --priority 2 --depends-on <impl-id>
hzl task add "Docs + rollout plan" --parent abc123 --priority 1 --depends-on <tests-id>

hzl validate
```

### Resume from a previous session

This is THE core use case for OpenClaw agents — you wake up fresh and need to pick up where the last session left off.

```bash
# 1. Check what's in progress or stuck
hzl task list -P openclaw --available     # What's ready to work?
hzl task list -P openclaw --assignee orchestrator  # What is already assigned to me?
hzl task stuck                            # Any expired leases from crashed sessions?

# 2. If there are stuck tasks, review their checkpoints before stealing
hzl task show <stuck-id> --json           # Read last checkpoint to understand state

# 3. Steal the expired task and continue
hzl task steal <stuck-id> --if-expired --assignee orchestrator

# 4. Read the last checkpoint to know exactly where to resume
hzl task show <stuck-id> --json | jq '.checkpoints[-1]'

# 5. Continue working, checkpoint your progress
hzl task checkpoint <stuck-id> "Resumed from previous session. Continuing from: <last checkpoint>"
```

**If no stuck tasks:** just use `hzl task next -P openclaw --claim` to grab the next available work.

### Work a task with checkpoints

Checkpoint at notable milestones or before pausing work. A checkpoint should be short and operational:
- what you accomplished
- what's next (if continuing)

**When to checkpoint (for AI agents):**
- Before any tool call that might fail (API calls, deploys, installs)
- Before spawning a sub-agent (in case it crashes)
- Before a session might compact (long-running work)
- After completing a meaningful unit of work
- Before pausing or handing off to another agent

**Rule of thumb:** If the session died right now, could another agent resume from your last checkpoint? If not, checkpoint now.

```bash
hzl task claim <id> --assignee orchestrator
# ...do work...
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh." --progress 50
# ...more work...
hzl task checkpoint <id> "Added token refresh. Testing complete." --progress 100
hzl task complete <id>
```

You can also set progress without a checkpoint:
```bash
hzl task progress <id> 75
```

### Handle blocked tasks

When stuck on external dependencies, mark the task as blocked:

```bash
hzl task claim <id> --assignee orchestrator
hzl task checkpoint <id> "Implemented login flow. Blocked: need API key for staging."
hzl task block <id> --comment "Blocked: waiting for staging API key from DevOps"

# Later, when unblocked:
hzl task unblock <id> --comment "Unblocked: received API key from DevOps"
hzl task checkpoint <id> "Got API key, resuming work"
hzl task complete <id>
```

**Comment best practices:** Include context about the action, not just the state:
- Good: "Blocked: waiting for API keys from infra team"
- Good: "Unblocked: keys received, resuming work"
- Bad: "waiting for API keys" (missing action context)

Blocked tasks stay visible in the dashboard (Blocked column) and keep their assignee, but don't appear in `--available` lists.

### Coordinate sub-agents with leases

Use leases when delegating, so you can detect abandoned work and recover.

```bash
hzl task add "Implement REST endpoints" -P myapp-auth --priority 3 --json
hzl task claim <id> --assignee subagent-claude-code --lease 30
```

Delegate with explicit instructions:
- claim the task (with their assignee id)
- checkpoint progress as they go
- complete when done

Monitor:
```bash
hzl task show <id> --json
hzl task stuck
hzl task steal <id> --if-expired --assignee orchestrator
```

### Break down work with subtasks

Use parent/subtask hierarchy to organize complex work:

```bash
# Create parent task
hzl task add "Implement vacation booking" -P portland-trip --priority 2
# → abc123

# Create subtasks (project inherited automatically)
hzl task add "Research flights" --parent abc123
hzl task add "Book hotel" --parent abc123 --depends-on <flights-id>
hzl task add "Plan activities" --parent abc123

# View breakdown
hzl task show abc123

# Work through subtasks
hzl task next --parent abc123
```

**Important:** `hzl task next` only returns leaf tasks (tasks without children). Parent tasks are organizational containers—they are never returned as "next available work."

**Finishing subtasks:** After completing each subtask, check if the parent has remaining work:
```bash
hzl task complete <subtask-id>

# Check parent status
hzl task show abc123 --json         # Any subtasks left?
hzl task complete abc123            # If all done, complete parent
```

## Web Dashboard

HZL includes a built-in Kanban dashboard for monitoring task state. The dashboard shows tasks in columns (Backlog → Blocked → Ready → In Progress → Done), with filtering by date and project.
Click any task card to open details with comments, checkpoints, and a per-task Activity tab (event history with actor attribution).

### Setting up the dashboard (recommended for OpenClaw)

For always-on access on your OpenClaw box, set up as a systemd service (Linux only):

```bash
# Check if service already exists before overwriting
systemctl --user status hzl-web 2>/dev/null && echo "Service already exists — skip setup" && exit 0

# Create the systemd user directory if needed
mkdir -p ~/.config/systemd/user

# Generate and install the service file
hzl serve --print-systemd > ~/.config/systemd/user/hzl-web.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now hzl-web

# IMPORTANT: Enable lingering so the service runs even when logged out
loginctl enable-linger $USER

# Verify it's running
systemctl --user status hzl-web
```

The dashboard will be available at `http://<your-box>:3456` (accessible over Tailscale).

To use a different port:
```bash
hzl serve --port 8080 --print-systemd > ~/.config/systemd/user/hzl-web.service
```

**macOS note:** systemd is Linux-only. On macOS, use `hzl serve --background` or create a launchd plist manually.

### Quick commands

```bash
hzl serve                    # Start in foreground (port 3456)
hzl serve --background       # Fork to background process
hzl serve --status           # Check if background server is running
hzl serve --stop             # Stop background server
hzl serve --host 127.0.0.1   # Restrict to localhost only
```

Use `--background` for temporary sessions. Use systemd for always-on access.

## Best Practices

1. **Always use `--json`** for programmatic output
2. **Checkpoint at milestones** or before pausing work
3. **Check for comments** before completing tasks
4. **Use a single `openclaw` project** for all work
5. **Use dependencies** to express sequencing, not priority
6. **Use leases** for long-running work to enable stuck detection
7. **Review checkpoints** before stealing stuck tasks

## What HZL Does Not Do

HZL is deliberately limited:

- **No orchestration** - Does not spawn agents or assign work
- **No task decomposition** - Does not break down tasks automatically
- **No smart scheduling** - Uses simple priority + FIFO ordering

These are features for your orchestration layer, not for the task tracker.

## OpenClaw-specific notes

- Run `hzl ...` via the Exec tool.
- OpenClaw skill gating checks `requires.bins` on the host at skill load time. If sandboxing is enabled, the binary must also exist inside the sandbox container too. Install it via `agents.defaults.sandbox.docker.setupCommand` (or use a custom image).
- If multiple agents share the same HZL database, use distinct `--assignee` ids (for example: `orchestrator`, `subagent-claude`, `subagent-gemini`) and rely on leases to avoid collisions.
