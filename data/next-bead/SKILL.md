---
name: next-bead
description: Find and safely claim the next Beads task with conflict checking. Use when looking for work, when finishing a task and need the next one, when the user mentions "next task" or "what should I work on", or when coordinating with other agents on task ownership.
---

# Next Bead — Orchestrator

Find available work. Verify no conflicts. Claim safely. Announce.

> **Pattern:** This skill uses the orchestrator-subagent pattern. Each phase runs in a fresh context for thorough conflict checking. See `docs/guides/ORCHESTRATOR_SUBAGENT_PATTERN.md`.

## When This Applies

| Signal | Action |
|--------|--------|
| User says "next task" or "what's next" | Run discovery + claim |
| Just finished a task | Close out, then discover |
| User says "/next-bead" | Run full protocol |
| Looking for work | Run discovery |

---

## Tool Reference

### Agent Mail (MCP)
| Tool | Purpose |
|------|---------|
| `fetch_inbox(agent_name)` | Check for messages before claiming |
| `file_reservation_paths(paths, exclusive)` | Reserve files before editing |
| `release_file_reservations(agent_name)` | Release files after closing |
| `send_message(to, subject, body_md, thread_id)` | Announce [CLAIMED]/[CLOSED] |

### Bash Commands
| Command | Purpose |
|---------|---------|
| `bd list --status in_progress --json` | Check for current work |
| `bd ready --json` | List available tasks |
| `bd-claim <id> --paths "..."` | **PREFERRED:** Atomic claim + reserve |
| `bd update <id> --status in_progress --assignee NAME` | Manual claim (use bd-claim instead) |
| `bd close <id> --reason "..."` | Close completed bead |
| `bv --robot-triage` | Get recommendations |
| `bv --robot-next` | Get single best task |
| `bv --robot-plan` | Get execution order |
| `cm context "task description" --json` | Get patterns before starting |
| `pytest` | Run tests before closing |
| `ubs --staged` | Security scan (MANDATORY) |

### Message Subjects
| Pattern | When |
|---------|------|
| `[CLAIMED] bd-XXX - Title` | After claiming task |
| `[CLOSED] bd-XXX - Title` | After closing task |

### Close Order
1. Run tests + `ubs --staged`
2. Commit with `.beads/issues.jsonl`
3. Close sub-beads FIRST (`bd close <id>.1`)
4. Close parent LAST (`bd close <id>`)
5. Release file reservations
6. Send [CLOSED] announcement

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEXT-BEAD ORCHESTRATOR                        │
│  - Creates session: sessions/next-bead-{timestamp}/              │
│  - Manages TodoWrite state                                       │
│  - Spawns subagents with minimal context                         │
│  - Passes verified task to claim phase                           │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Closeout     │  │    Discover     │  │     Verify      │
│  agents/        │  │  agents/        │  │  agents/        │
│  closeout.md    │  │  discover.md    │  │  verify.md      │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
    01_closeout.md       02_discovery.md      03_verification.md
         │                    │                    │
         │ reservations       │ ready_tasks        │ can_claim
         │ released           │ bv_recommendation  │ verified_task
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │     Claim       │ → Task claimed
                    │  agents/        │
                    │  claim.md       │
                    └────────┬────────┘
                             │
                        04_claim.md
```

## Subagents

| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | `agents/closeout.md` | agent_name | beads_closed, reservations_released |
| 2 | `agents/discover.md` | agent_name | ready_tasks, bv_recommendation |
| 3 | `agents/verify.md` | target_task, active_agents | can_claim, verified_task |
| 4 | `agents/claim.md` | verified_task | task_claimed, files_reserved |

---

## Execution Flow

### 1. Setup (Orchestrator)

```markdown
1. Create session directory:
   mkdir -p sessions/next-bead-{timestamp}

2. Initialize TodoWrite with phases:
   - [ ] Phase 1: Closeout
   - [ ] Phase 2: Discover
   - [ ] Phase 3: Verify
   - [ ] Phase 4: Claim

3. Gather inputs:
   - project_path: Absolute path to project
   - agent_name: Current agent name
```

### 2. Phase 1: Closeout

**Spawn:** `agents/closeout.md`

**Input:**
```json
{
  "project_path": "/abs/path/to/project",
  "session_dir": "sessions/next-bead-{timestamp}",
  "agent_name": "BlueLake"
}
```

**Output:**
```json
{
  "had_in_progress": true,
  "beads_closed": ["bd-123", "bd-123.1"],
  "reservations_released": true
}
```

### 3. Phase 2: Discover

**Spawn:** `agents/discover.md`

**Input:**
```json
{
  "project_path": "/abs/path/to/project",
  "session_dir": "sessions/next-bead-{timestamp}",
  "agent_name": "BlueLake"
}
```

**Output:**
```json
{
  "ready_tasks": ["bd-125", "bd-126", "bd-127"],
  "bv_recommendation": "bd-125",
  "active_agents": ["GreenCastle"]
}
```

### 4. Phase 3: Verify

**Spawn:** `agents/verify.md`

**Input:**
```json
{
  "project_path": "/abs/path/to/project",
  "session_dir": "sessions/next-bead-{timestamp}",
  "agent_name": "BlueLake",
  "target_task": {"id": "bd-125", "files": ["src/auth/**"]},
  "active_agents": ["GreenCastle"]
}
```

**Output:**
```json
{
  "can_claim": true,
  "verified_task": "bd-125",
  "blocking_reason": null
}
```

### 5. Phase 4: Claim

**Spawn:** `agents/claim.md`

**Input:**
```json
{
  "project_path": "/abs/path/to/project",
  "session_dir": "sessions/next-bead-{timestamp}",
  "agent_name": "BlueLake",
  "task_to_claim": {"id": "bd-125", "title": "JWT validation"},
  "active_agents": ["GreenCastle"]
}
```

**Output:**
```json
{
  "task_claimed": "bd-125",
  "files_reserved": ["src/auth/**"],
  "announcement_sent": true
}
```

### 6. Finalize (Orchestrator)

1. Update TodoWrite (all phases complete)
2. Present summary to user
3. Begin work on claimed task

---

## Templates

Located in `.claude/templates/beads/`:
- `verification.md` — Pre-claim checklist
- `claimed.md` — Claim announcement format
- `closed.md` — Completion announcement format
- `next-bead-output.md` — Output summary format

---

## Philosophy

**Parallel agents must coordinate.** Before claiming:
1. Know what's truly available
2. Check what other agents are doing
3. Verify no file conflicts
4. Communicate intent

---

## 1. Close Out Previous Work

Check for in-progress work:
```bash
bd list --status in_progress --json
```

If yes:
1. Run tests + `ubs --staged`
2. Commit/push (include `.beads/issues.jsonl`)
3. Close sub-beads first, then parent:
   ```bash
   bd close <id>.1 --reason "Completed: [summary]"
   bd close <id> --reason "Completed: [summary]"
   ```
4. Release reservations:
   ```python
   release_file_reservations(project_key=PROJECT_PATH, agent_name=YOUR_NAME)
   ```
5. Send `[CLOSED]` announcement (use template)

---

## 2. Discover

**Recommendations:**
```bash
bv --robot-triage
bv --robot-plan
```

**Ready tasks:**
```bash
bd ready --json
```

**Active agents:**
```python
ReadMcpResourceTool(server="mcp-agent-mail", uri="resource://agents/PROJECT_PATH")
```

**Already claimed:**
```bash
bd list --status in_progress --json
```

**Your inbox:**
```python
fetch_inbox(project_key=PROJECT_PATH, agent_name=YOUR_NAME, include_bodies=true, limit=10)
```

Address urgent messages before claiming new work.

---

## 3. Verify

All must pass before claiming:

- [ ] Task status is `ready`
- [ ] No other agent has claimed it
- [ ] Required files not reserved by others
- [ ] Dependencies satisfied
- [ ] No blocking inbox messages

**If ANY fails → pick different task or coordinate first.**

If uncertain, ask:
```python
send_message(
  project_key=PROJECT_PATH,
  sender_name=YOUR_NAME,
  to=[OTHER_AGENTS],
  subject="Claiming task: <task-id>?",
  body_md="Planning to pick up **<task-id>**. Files: `app/...`. Conflicts?",
  importance="normal"
)
```

---

## 4. Claim

**PREFERRED: Use bd-claim for atomic claim + reserve:**

```bash
bd-claim <id> --paths "app/path/**,tests/**"
```

This atomically validates, reserves, and claims in one command with automatic rollback on failure.

**For sub-beads, claim each:**
```bash
bd-claim <id>.1 --paths "app/path/**"
bd-claim <id>.2 --paths "tests/**"
```

**ALTERNATIVE: Manual steps (use bd-claim instead):**

```bash
bd update <id> --status in_progress --assignee YOUR_NAME
bd update <id>.1 --status in_progress --assignee YOUR_NAME
bd update <id>.2 --status in_progress --assignee YOUR_NAME
```

```python
file_reservation_paths(
  project_key=PROJECT_PATH,
  agent_name=YOUR_NAME,
  paths=["app/path/**", "tests/**"],
  ttl_seconds=3600,
  exclusive=true,
  reason="<task-id>: description"
)
```

**Announce (MANDATORY):**
```python
send_message(
  project_key=PROJECT_PATH,
  sender_name=YOUR_NAME,
  to=[ALL_AGENTS],
  subject="[CLAIMED] <task-id> - <title>",
  body_md=<use claimed template>,
  importance="normal",
  thread_id="<task-id>"
)
```

---

## 5. Get Context Before Working

After claiming, get patterns and anti-patterns:
```bash
cm context "<task-title>" --json
```

This returns:
- **Relevant rules** from past sessions
- **Anti-patterns** to avoid
- **Historical context** about similar work

---

## Quick Reference

```bash
# Recommended next
bv --robot-triage
bv --robot-next          # Single best task

# Ready tasks
bd ready --json

# Claimed tasks
bd list --status in_progress --json

# Claim (PREFERRED: atomic claim + reserve)
bd-claim <id> --paths "src/**/*.py"

# Manual claim (use bd-claim instead)
bd update <id> --status in_progress --assignee YOUR_NAME

# Close (sub-beads first)
bd close <id>.1 --reason "Completed: ..."
bd close <id> --reason "Completed: ..."
```

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Skip file reservation checks | Merge conflicts |
| Claim only parent, not sub-beads | Other agents grab sub-beads |
| Skip `[CLAIMED]` announcement | Duplicate work |
| Skip `[CLOSED]` announcement | Stale state |
| Hoard tasks | Claim one, finish it, then next |
| Ignore inbox | Miss coordination messages |

---

## See Also

- `bead-workflow/` — Full bead lifecycle details
- `prime/` — Session startup
- `.claude/templates/beads/` — Message templates
