---
name: ln-1000-pipeline-orchestrator
description: "Meta-orchestrator (L0): reads kanban board, drives Stories through pipeline 300->310->400->500 in parallel via TeamCreate. Max 2 concurrent Stories. Auto squash-merge to develop on quality gate PASS."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Pipeline Orchestrator

Meta-orchestrator that reads the kanban board, builds a priority queue of Stories, and drives them through the full pipeline (task planning -> validation -> execution -> quality gate) using Claude Code Agent Teams for parallel Story processing.

## Purpose & Scope
- Parse kanban board and build Story priority queue
- Ask business questions in ONE batch before execution; make technical decisions autonomously
- Spawn per-story workers via TeamCreate (max 2 concurrent)
- Drive each Story through 4 stages: ln-300 -> ln-310 -> ln-400 -> ln-500
- Auto squash-merge to develop after quality gate PASS
- Handle failures, retries, and escalation to user

## Hierarchy

```
L0: ln-1000-pipeline-orchestrator (TeamCreate lead, delegate mode)
  +-- Story Workers (fresh per stage, shutdown after completion)
       |   All stages: Opus 4.6  |  Effort: Stage 0,3 = high | Stage 1,2 = medium
       +-- L1: ln-300 / ln-310 / ln-400 / ln-500 (invoked via Skill tool, as-is)
            +-- L2/L3: existing hierarchy unchanged
```

**Key principle:** ln-1000 does NOT modify existing skills. Workers invoke ln-300/ln-310/ln-400/ln-500 through Skill tool exactly as a human operator would.

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/storage_mode_detection.md` for Linear vs File mode detection and operations.

## When to Use
- Multiple Stories ready for processing across kanban board statuses
- Need end-to-end automation: task planning -> validation -> execution -> quality gate -> merge
- Want parallel Story processing with minimal manual intervention

## Pipeline: 4-Stage State Machine

**MANDATORY READ:** Load `references/pipeline_states.md` for transition rules and guards.

```
Backlog       --> Stage 0 (ln-300) --> Backlog      --> Stage 1 (ln-310) --> Todo
(no tasks)        create tasks         (tasks exist)      validate            |
                                                          | NO-GO             |
                                                          v                   v
                                                       [retry/ask]    Stage 2 (ln-400)
                                                                             |
                                                                             v
                                                                      To Review
                                                                             |
                                                                             v
                                                                      Stage 3 (ln-500)
                                                                       |          |
                                                                      PASS       FAIL
                                                                       |          v
                                                                     Done    To Rework -> Stage 2
                                                                   (merged)    (max 2 cycles)
```

| Stage | Skill | Input Status | Output Status |
|-------|-------|-------------|--------------|
| 0 | ln-300-task-coordinator | Backlog (no tasks) | Backlog (tasks created) |
| 1 | ln-310-story-validator | Backlog (tasks exist) | Todo |
| 2 | ln-400-story-executor | Todo / To Rework | To Review |
| 3 | ln-500-story-quality-gate | To Review | Done / To Rework |

## Team Lead Responsibilities

This skill runs as a **team lead** in delegate mode. The agent executing ln-1000 MUST NOT write code or invoke skills directly.

| Responsibility | Description |
|---------------|-------------|
| **Coordinate** | Assign stages to workers, process completion reports, advance pipeline |
| **Verify** | Re-read kanban after each stage, ASSERT expected state transitions |
| **Update** | Single writer to kanban_board.md — workers never edit the board |
| **Escalate** | Route failures to user when retry limits exceeded |
| **Merge to develop** | Squash-merge to develop after quality gate PASS (lead-only action) |
| **Shutdown** | Graceful worker shutdown, team cleanup |

**NEVER do as lead:** Invoke ln-300/ln-310/ln-400/ln-500 directly. Edit source code. Skip quality gate. Force-kill workers.

## Workflow

### Phase 0: Recovery Check

```
IF .pipeline/state.json exists AND complete == false:
  # Previous run interrupted — resume from saved state
  1. Read .pipeline/state.json → restore: story_state, worker_map,
     quality_cycles, validation_retries, crash_count, priority_queue_ids,
     story_results, infra_issues, worktree_map, depends_on
  2. Read .pipeline/checkpoint-*.json → validate story_state consistency
     (checkpoint.stage should match story_state[id])
  3. Re-read kanban board → rebuild priority_queue from priority_queue_ids
     (skip stories already DONE/PAUSED)
  4. Re-parse Story dependencies → rebuild depends_on (defense in depth)
  5. Read team config → verify worker_map members still exist
  6. Set suspicious_idle[*] = false (ephemeral, reset on recovery)
  7. For each story with story_state IN ("STAGE_0".."STAGE_3"):
     IF checkpoint.agentId exists → Task(resume: checkpoint.agentId)
     ELSE → respawn worker with checkpoint context (see checkpoint_format.md)
  8. Jump to Phase 4 event loop

IF .pipeline/state.json NOT exists OR complete == true:
  # Fresh start — proceed to Phase 1
```

### Phase 1: Discovery & Kanban Parsing

**MANDATORY READ:** Load `references/kanban_parser.md` for parsing patterns.

1. Auto-discover `docs/tasks/kanban_board.md` (or Linear API via storage mode detection)
2. Parse all status sections: Backlog, Todo, In Progress, To Review, To Rework
3. Extract Story list with: ID, title, status, Epic name, task presence
4. Build priority queue:
   ```
   Priority: To Review > To Rework > In Progress > Todo > Backlog
   ```
5. Filter: skip Stories in Done, Postponed, Canceled
6. Detect task presence per Story:
   - Has `_(tasks not created yet)_` → **no tasks** → Stage 0
   - Has task lines (4-space indent) → **tasks exist** → Stage 1+
7. Extract dependencies per Story (see `references/kanban_parser.md` Dependency Extraction):
   - Read each Story file → parse `## Dependencies / ### Depends On` section
   - Build `depends_on[storyId] = [prerequisite IDs]`
   - Prerequisites already Done → satisfied, ignore. Not found → WARN, treat as none
   - Circular dependencies → ESCALATE to user
8. Show pipeline plan to user:
   ```
   Pipeline Plan:
   | # | Story | Status | Stage | Deps | Action |
   |---|-------|--------|-------|------|--------|
   | 1 | PROJ-42 | To Review | 3 | — | Quality gate |
   | 2 | PROJ-38 | To Rework | 2 | — | Re-execute with fix tasks |
   | 3 | PROJ-45 | Todo | 2 | PROJ-42 | Execute (after PROJ-42) |
   | 4 | PROJ-50 | Backlog | 1 | — | Validate |
   | 5 | PROJ-55 | Backlog | 0 | PROJ-50 | Create tasks (after PROJ-50) |
   ```

### Phase 2: Pre-flight Questions (ONE batch)

1. Load Story descriptions (metadata only) for top stories in pipeline scope
2. Scan for business ambiguities — questions where:
   - Answer cannot be found in codebase, docs, or standards
   - Answer requires business/product decision (payment provider, auth flow, UI preference)
3. Collect ALL business questions into single AskUserQuestion:
   ```
   "Before starting pipeline:
    Story PROJ-42: Which payment provider? (Stripe/PayPal/both)
    Story PROJ-45: Auth flow — JWT or session-based?"
   ```
4. Technical questions — resolve autonomously:
   - Library versions: MCP Ref / Context7
   - Architecture patterns: project docs + CLAUDE.md
   - Standards compliance: ln-310 Phase 2 handles this
5. Store answers in shared context (pass to workers via spawn prompt)

**Skip Phase 2** if no business questions found. Proceed directly to Phase 3.

### Phase 3: Team Setup

**MANDATORY READ:** Load `references/settings_template.json` for required permissions and hooks.

#### 3.1 Pre-flight: Settings Verification

Verify `.claude/settings.local.json` in target project:
- `defaultMode` = `"bypassPermissions"` (required for workers)
- `hooks.Stop` registered → `pipeline-keepalive.sh`
- `hooks.TeammateIdle` registered → `worker-keepalive.sh`

If missing or incomplete → copy from `references/settings_template.json` and install hook scripts via Bash `cp` (NOT Write tool — Write produces CRLF on Windows, breaking `#!/bin/bash` shebang):
```
mkdir -p .claude/hooks
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/pipeline-keepalive.sh .claude/hooks/pipeline-keepalive.sh
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/worker-keepalive.sh  .claude/hooks/worker-keepalive.sh
```

**Hook troubleshooting:** If hooks fail with "No such file or directory":
1. Verify hook commands use `bash .claude/hooks/script.sh` (relative path, no env vars — `$CLAUDE_PROJECT_DIR` is NOT available in hook shell context)
2. Verify `.claude/hooks/*.sh` files exist and have `#!/bin/bash` shebang
3. On Windows: ensure LF line endings in .sh files (see hook installation above — use Bash `cp`, not Write tool)

#### 3.2 Initialize Pipeline State

```
Write .pipeline/state.json (full schema — see checkpoint_format.md):
  { "complete": false, "active_workers": 0, "stories_remaining": N, "last_check": <now>,
    "story_state": {}, "worker_map": {}, "quality_cycles": {}, "validation_retries": {},
    "crash_count": {}, "priority_queue_ids": [<all story IDs>],
    "worktree_map": {}, "depends_on": {}, "story_results": {}, "infra_issues": [] }
Write .pipeline/lead-session.id with current session_id   # Stop hook uses this to only keep lead alive
```

#### 3.3 Create Team & Spawn Workers

**Worktrees:** Created lazily in Phase 4 spawn loop — only when a 2nd worker starts (parallel mode). Solo worker runs in project CWD.

**Model routing:** All stages use `model: "opus"`. Effort routing via prompt: `effort_for_stage(0) = "high"`, `effort_for_stage(1) = "medium"`, `effort_for_stage(2) = "medium"`, `effort_for_stage(3) = "high"`. Crash recovery = `"high"`. Thinking mode: always enabled (adaptive).

1. Ensure `develop` branch exists:
   ```
   IF `develop` branch not found locally or on origin:
     git branch develop master        # Create from master
     git push -u origin develop
   git checkout develop               # Start pipeline from develop
   ```

2. Create team:
   ```
   TeamCreate(team_name: "pipeline-{YYYY-MM-DD}")
   ```

Workers are spawned by Phase 4 spawn loop on first heartbeat — NOT here. This avoids duplicate spawn logic.

### Phase 4: Execution Loop

**MANDATORY READ:** Load `references/message_protocol.md` for exact message formats and parsing regex.
**MANDATORY READ:** Load `references/worker_health_contract.md` for crash detection and respawn rules.

**Lead operates in delegate mode — coordination only, no code writing.**

**MANDATORY READ:** Load `references/checkpoint_format.md` for checkpoint schema and resume protocol.

#### Communication Rules

```
FORBIDDEN PATTERNS (lead and workers):
- Reading ~/.claude/teams/*/inboxes/*.json directly
- Bash sleep loops for polling messages
- Parsing internal JSON formats (permission_request, idle_notification)
- Any filesystem access to ~/.claude/ internal structures

CORRECT PATTERNS:
- Messages arrive automatically as conversation turns (TeammateIdle notifications)
- Use SendMessage(type: "message") for all communication
- Use SendMessage(type: "shutdown_request") for shutdown
- Lead processes messages in event-driven style (ON ... handlers below)
```

```
# --- INITIALIZATION ---
active_workers = 0                    # Current worker count (invariant: <= 2)
quality_cycles = {}                   # {storyId: count} — FAIL→retry counter, limit 2
validation_retries = {}               # {storyId: count} — NO-GO retry counter, limit 1
crash_count = {}                      # {storyId: count} — crash respawn counter, limit 1
suspicious_idle = {}                  # {storyId: bool} — crash detection flag
story_state = {}                      # {storyId: "STAGE_0"|"STAGE_1"|"STAGE_2"|"STAGE_3"|"DONE"|"PAUSED"}
worker_map = {}                       # {storyId: worker_name}
depends_on = {}                       # {storyId: [prerequisite IDs]} — from Phase 1 step 7
worktree_map = {}                     # {storyId: worktree_dir | null} — tracks which stories use worktrees
story_results = {}                    # {storyId: {stage0: "...", stage1: "...", ...}} — for pipeline report
infra_issues = []                     # [{phase, type, message}] — infrastructure problems for report

# Initialize counters for all queued stories
FOR EACH story IN priority_queue:
  quality_cycles[story.id] = 0
  validation_retries[story.id] = 0
  crash_count[story.id] = 0
  suspicious_idle[story.id] = false
  story_state[story.id] = "QUEUED"

# --- EVENT LOOP (driven by Stop hook heartbeat) ---
# HOW THIS WORKS:
# 1. Lead's turn ends → Stop event fires
# 2. pipeline-keepalive.sh reads .pipeline/state.json → complete=false → exit 2
# 3. stderr "HEARTBEAT: N workers, M stories..." → new agentic loop iteration
# 4. Any queued worker messages (SendMessage) delivered in this cycle
# 5. Lead processes messages via ON handlers below
# 6. Lead's turn ends → Go to step 1
#
# The Stop hook IS the event loop driver. Each heartbeat = one iteration.
# Lead MUST NOT say "waiting for messages" and stop — the heartbeat keeps it alive.
# If no worker messages arrived: output brief status, let turn end → next heartbeat.
#
# FRESH WORKER PER STAGE: Each stage transition = shutdown old worker + spawn new one.
# active_workers stays same (net-zero). Only DONE/PAUSED/ERROR decrement active_workers.

WHILE ANY story_state[id] NOT IN ("DONE", "PAUSED"):

  # 1. Spawn workers for queued stories (respecting concurrency + dependency limits)
  WHILE active_workers < 2 AND priority_queue NOT EMPTY:
    story = priority_queue.peek()            # Don't pop yet — may be blocked

    # Dependency guard: all prerequisites must be DONE
    blocked_deps = [d for d in depends_on[story.id] if story_state[d] != "DONE"]
    IF blocked_deps NOT EMPTY:
      priority_queue.skip(story.id)          # Move to next candidate
      CONTINUE                               # Try next story in queue
    priority_queue.pop()                     # Safe to start

    target_stage = determine_stage(story)    # See pipeline_states.md guards
    worker_name = "story-{story.id}-s{target_stage}"

    # Conditional worktree: only when parallel (another worker already active)
    IF active_workers >= 1:
      worktree_dir = ".worktrees/story-{story.id}"
      git worktree add {worktree_dir} develop
    ELSE:
      worktree_dir = null                    # Solo mode — work in project CWD

    worktree_map[story.id] = worktree_dir
    Task(name: worker_name, team_name: "pipeline-{date}",
         model: "opus", mode: "bypassPermissions",
         subagent_type: "general-purpose",
         prompt: worker_prompt(story, target_stage, business_answers, worktree_dir))
    worker_map[story.id] = worker_name
    story_state[story.id] = "STAGE_{target_stage}"
    active_workers++
    Write .pipeline/worker-{worker_name}-active.flag     # For TeammateIdle hook
    Update .pipeline/state.json: active_workers, last_check
    SendMessage(recipient: worker_name,
                content: "Execute Stage {target_stage} for {story.id}",
                summary: "Stage {target_stage} assignment")

  # 1b. Deadlock detection: all remaining stories blocked on non-DONE dependencies
  IF active_workers == 0 AND priority_queue NOT EMPTY:
    unblockable = [s for s in priority_queue if ANY d in depends_on[s.id]: story_state[d] == "DONE"]
    IF unblockable EMPTY:
      FOR EACH s IN priority_queue: story_state[s.id] = "PAUSED"
      ESCALATE: "Deadlocked: remaining stories depend on PAUSED/incomplete stories: {ids}"

  # 2. Process worker messages (delivered by heartbeat cycle)
  #    Messages from workers arrive as conversation context in each heartbeat iteration.
  #    Match against ON handlers below. If no match → ON NO NEW MESSAGES at bottom.
  #
  # SENDER VALIDATION: Before processing ANY completion message, verify sender:
  #   VERIFY message.sender == worker_map[id]
  #   IF mismatch: LOG "Ignoring stale message from {sender} for {id}"; SKIP handler
  #   This prevents old/dead workers from corrupting pipeline state.
  #
  # STATE GUARD: Before processing ANY stage completion, verify story is in expected state:
  #   Stage 0 COMPLETE → story_state[id] must be "STAGE_0"
  #   Stage 1 COMPLETE → story_state[id] must be "STAGE_1"
  #   Stage 2 COMPLETE → story_state[id] must be "STAGE_2"
  #   Stage 3 COMPLETE → story_state[id] must be "STAGE_3"
  #   IF mismatch: LOG "Duplicate/stale message for {id} (state={story_state[id]})"; SKIP handler
  #   This prevents double-spawn when same completion message is delivered across heartbeats.

  ON "Stage 0 COMPLETE for {id}. {N} tasks created. Plan score: {score}/4.":
    Re-read kanban board
    ASSERT tasks exist under Story {id}         # Guard: verify ln-300 output
    IF tasks missing: story_state[id] = "PAUSED"; ESCALATE; CONTINUE
    story_state[id] = "STAGE_1"
    # Shutdown old worker, spawn fresh for Stage 1
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    next_worker = "story-{id}-s1"
    Task(name: next_worker, team_name: "pipeline-{date}",
         model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",
         prompt: worker_prompt(story, 1, business_answers, worktree_map[id]))
    worker_map[id] = next_worker
    Write .pipeline/worker-{next_worker}-active.flag
    story_results[id].stage0 = "{N} tasks, {score}/4"

  ON "Stage 0 ERROR for {id}: {details}":
    story_state[id] = "PAUSED"
    active_workers--
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    ESCALATE to user: "Cannot create tasks for Story {id}: {details}"
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    story_results[id].stage0 = "ERROR: {details}"
    Append story report section to docs/tasks/reports/pipeline-{date}.md (PAUSED)

  ON "Stage 1 COMPLETE for {id}. Verdict: GO. Readiness: {score}.":
    Re-read kanban board
    ASSERT Story {id} status = Todo              # Guard: verify ln-310 output
    story_state[id] = "STAGE_2"
    # Shutdown old worker, spawn fresh for Stage 2
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    next_worker = "story-{id}-s2"
    Task(name: next_worker, team_name: "pipeline-{date}",
         model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",      # Stage 2 medium effort
         prompt: worker_prompt(story, 2, business_answers, worktree_map[id]))
    worker_map[id] = next_worker
    Write .pipeline/worker-{next_worker}-active.flag
    story_results[id].stage1 = "GO, {score}"

  ON "Stage 1 COMPLETE for {id}. Verdict: NO-GO. Readiness: {score}. Reason: {reason}":
    validation_retries[id]++
    IF validation_retries[id] <= 1:
      # Shutdown old worker, spawn fresh for Stage 1 retry
      Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
      SendMessage(type: "shutdown_request", recipient: worker_map[id])
      next_worker = "story-{id}-s1-retry"
      Task(name: next_worker, team_name: "pipeline-{date}",
           model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",    # Stage 1 = review
           prompt: worker_prompt(story, 1, business_answers, worktree_map[id]))
      worker_map[id] = next_worker
      Write .pipeline/worker-{next_worker}-active.flag
    ELSE:
      story_state[id] = "PAUSED"
      active_workers--
      Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
      ESCALATE to user: "Story {id} failed validation twice: {reason}"
      SendMessage(type: "shutdown_request", recipient: worker_map[id])
      story_results[id].stage1 = "NO-GO, {score}, {reason} (retries exhausted)"
      Append story report section to docs/tasks/reports/pipeline-{date}.md (PAUSED)

  ON "Stage 2 ERROR for {id}: {details}":
    story_state[id] = "PAUSED"
    active_workers--
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    ESCALATE to user: "Story {id} execution failed: {details}"
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    story_results[id].stage2 = "ERROR: {details}"
    Append story report section to docs/tasks/reports/pipeline-{date}.md (PAUSED)

  ON "Stage 2 COMPLETE for {id}. All tasks Done. Story set to To Review.":
    Re-read kanban board
    ASSERT Story {id} status = To Review         # Guard: verify ln-400 output
    story_state[id] = "STAGE_3"
    # Shutdown old worker, spawn fresh for Stage 3
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    next_worker = "story-{id}-s3"
    Task(name: next_worker, team_name: "pipeline-{date}",
         model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",      # Stage 3 = QA
         prompt: worker_prompt(story, 3, business_answers, worktree_map[id]))
    worker_map[id] = next_worker
    Write .pipeline/worker-{next_worker}-active.flag
    story_results[id].stage2 = "Done"

  ON "Stage 3 COMPLETE for {id}. Verdict: PASS|CONCERNS|WAIVED. Quality Score: {score}/100.":
    story_state[id] = "DONE"
    active_workers--
    Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
    Update .pipeline/state.json: active_workers, stories_remaining, last_check
    Squash merge (see Phase 4a below)
    Update kanban: Story → Done
    SendMessage(type: "shutdown_request", recipient: worker_map[id])
    story_results[id].stage3 = "{verdict} {score}/100"

  ON "Stage 3 COMPLETE for {id}. Verdict: FAIL. Quality Score: {score}/100. Issues: {issues}":
    quality_cycles[id]++
    IF quality_cycles[id] < 2:
      story_state[id] = "STAGE_2"
      # Shutdown old worker, spawn fresh for Stage 2 re-entry (fix tasks)
      Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
      SendMessage(type: "shutdown_request", recipient: worker_map[id])
      next_worker = "story-{id}-s2-fix{quality_cycles[id]}"
      Task(name: next_worker, team_name: "pipeline-{date}",
           model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",    # Stage 2 medium effort (fix)
           prompt: worker_prompt(story, 2, business_answers, worktree_map[id]))
      worker_map[id] = next_worker
      Write .pipeline/worker-{next_worker}-active.flag
    ELSE:
      story_state[id] = "PAUSED"
      active_workers--
      Bash: rm -f .pipeline/worker-{worker_map[id]}-active.flag .pipeline/worker-{worker_map[id]}-done.flag
      ESCALATE to user: "Story {id} failed quality gate {quality_cycles[id]} times"
      SendMessage(type: "shutdown_request", recipient: worker_map[id])
      story_results[id].stage3 = "FAIL {score}/100 (cycles exhausted)"
      Append story report section to docs/tasks/reports/pipeline-{date}.md (PAUSED)

  ON worker TeammateIdle WITHOUT prior completion message for {id}:
    # Crash detection: 3-step protocol (see worker_health_contract.md)
    # Step 1: Flag suspicious
    suspicious_idle[id] = true
    # Step 2: Probe
    SendMessage(recipient: worker_map[id],
                content: "Status check: are you still working on Stage {N} for {id}?",
                summary: "{id} health check")
    # Step 3: Evaluate
    ON worker responds with parseable status:
      suspicious_idle[id] = false           # False alarm, continue
    ON TeammateIdle again WITHOUT response:
      crash_count[id]++
      IF crash_count[id] <= 1:
        active_workers--
        # Resume protocol (see checkpoint_format.md):
        checkpoint = read(".pipeline/checkpoint-{id}.json")
        IF checkpoint.agentId exists:
          Task(resume: checkpoint.agentId)          # Try 1: full context resume
        ELSE:
          new_prompt = worker_prompt(story, checkpoint.stage, business_answers, worktree_map[id]) + CHECKPOINT_RESUME block
          Task(name: "story-{id}-s{checkpoint.stage}-retry", team_name: "pipeline-{date}",
               model: "opus", mode: "bypassPermissions", subagent_type: "general-purpose",
               prompt: new_prompt)                  # Try 2: Opus for crash recovery/troubleshooting
        worker_map[id] = new_worker_name
        active_workers++
      ELSE:
        story_state[id] = "PAUSED"
        active_workers--
        ESCALATE: "Story {id} worker crashed twice at Stage {N}"

  # 3. Heartbeat handler — persist ALL state on every cycle
  ON HEARTBEAT (Stop hook stderr: "HEARTBEAT: N workers, M stories..."):
    Write .pipeline/state.json with ALL state variables:
      complete, active_workers, stories_remaining, last_check=now,
      story_state, worker_map, quality_cycles, validation_retries,
      crash_count, priority_queue_ids, story_results, infra_issues,
      worktree_map, depends_on
    # Full state write enables Phase 0 recovery if lead crashes between heartbeats

  ON NO NEW MESSAGES (heartbeat cycle with no worker updates):
    # Brief status with checkpoint progress — do NOT say "waiting" and stop.
    FOR EACH active story in story_state (STAGE_0..STAGE_3):
      checkpoint = read(".pipeline/checkpoint-{id}.json") if exists
      progress = "{len(checkpoint.tasksCompleted)}/{len(checkpoint.tasksCompleted)+len(checkpoint.tasksRemaining)}" if checkpoint else "—"
      # Collect per-story progress
    Output: "Heartbeat: {active_workers} workers, {stories_remaining} remaining. Progress: {id}={progress}, ..."
    # Turn ends → Stop hook fires → next heartbeat cycle
```

**`determine_stage(story)` routing:** See `references/pipeline_states.md` Stage-to-Status Mapping table.

#### Phase 4a: Git Flow & Squash Merge

After Stage 3 PASS for each Story. All git commands use `git -C {dir}` where `dir = worktree_map[id] || "."`.

```
dir = worktree_map[id] || "."

# 1. Sync with develop (pull latest changes)
git -C {dir} fetch origin develop
git -C {dir} rebase origin/develop
IF rebase conflict:
  git -C {dir} rebase --abort
  git -C {dir} merge origin/develop    # Fallback to merge
  IF merge conflict:
    ESCALATE to user: "Merge conflict in Story {id}. Manual resolution required."
    story_state[id] = "PAUSED"
    CONTINUE                           # Skip merge, move to next story

# 2. Squash merge into develop
git -C {dir} checkout develop
git -C {dir} merge --squash feature/{id}-{slug}
git -C {dir} commit -m "{storyId}: {Story Title}"
git -C {dir} push origin develop

# 3. Cleanup worktree (if exists)
IF worktree_map[id]:
  git worktree remove .worktrees/story-{id} --force
  worktree_map[id] = null
ELSE:
  # Solo mode — already on develop after checkout above

# 4. Re-read SKILL.md (context refresh after merge cycle)
**MANDATORY READ:** Reload this SKILL.md to refresh pipeline context after develop push.

# 5. Append story report section
Append to docs/tasks/reports/pipeline-{date}.md:
  ### {storyId}: {storyTitle} — DONE
  | Stage | Result | Details |
  |-------|--------|---------|
  | 0 | {story_results[id].stage0 or "skip"} | |
  | 1 | {story_results[id].stage1 or "skip"} | retries: {validation_retries[id]} |
  | 2 | {story_results[id].stage2 or "skip"} | rework cycles: {quality_cycles[id]} |
  | 3 | {story_results[id].stage3 or "skip"} | crashes: {crash_count[id]} |
  **Branch:** feature/{id}-{slug}
  **Problems:** {list from counters, or "None"}

# 6. Verify kanban + Linear sync
Re-read kanban board → ASSERT Story {id} is in Done section
IF storage_mode == "linear":
  Read Linear issue via MCP → ASSERT status matches kanban (Done/Completed)
  IF mismatch: Update Linear status to match kanban
  VERIFY assignee, labels
IF mismatch found: LOG warning but do NOT block pipeline
```

### Phase 5: Cleanup & Self-Verification

```
# 0. Signal pipeline complete (allows Stop hook to pass)
Write .pipeline/state.json: { "complete": true, ... }

# 1. Wait for all active workers to complete
ASSERT active_workers == 0

# 2. Self-verify against Definition of Done
verification = {
  kanban_parsed:    priority_queue was built          # Phase 1 ✓
  questions_asked:  business_answers stored OR none   # Phase 2 ✓
  team_created:     team exists                       # Phase 3 ✓
  all_processed:    ALL story_state[id] IN ("DONE", "PAUSED")  # Phase 4 ✓
  merged_develop:   EVERY "DONE" story squash-merged to develop  # Phase 4a ✓
  linear_synced:    IF storage_mode == "linear": ALL "DONE" stories match Linear status  # Phase 4a.6 ✓
  on_develop:       Current branch is develop              # Phase 5 ✓
}
IF ANY verification == false: WARN user with details

# 3. Finalize pipeline report
Prepend summary header to docs/tasks/reports/pipeline-{date}.md:
  # Pipeline Report — {date}
  | Metric | Value |
  |--------|-------|
  | Stories processed | {total} |
  | Completed (DONE) | {count where story_state == "DONE"} |
  | Paused (needs intervention) | {count where story_state == "PAUSED"} |
  | Total quality rework cycles | {sum of quality_cycles} |
  | Total validation retries | {sum of validation_retries} |
  | Total crash recoveries | {sum of crash_count} |
  | Infrastructure issues | {len(infra_issues)} |

# 3a. Collect infrastructure issues
# Analyze entire pipeline session for non-fatal problems:
# hook/settings failures, git conflicts, worktree errors, merge issues,
# Linear sync mismatches, worker crashes, permission errors, any unexpected fallbacks.
# Populate infra_issues = [{phase, type, message}] from session context.

Append Infrastructure Issues section:
  ## Infrastructure Issues
  IF infra_issues NOT EMPTY:
    | # | Phase | Type | Details |
    |---|-------|------|---------|
    FOR EACH issue IN infra_issues:
      | {N} | {issue.phase} | {issue.type} | {issue.message} |
  ELSE:
    _No infrastructure issues._

Append Operational Recommendations section (auto-generated from counters):
  ## Operational Recommendations
  - IF any quality_cycles > 0: "Story {id} needed {N} quality cycles. Improve task specs or acceptance criteria."
  - IF any validation_retries > 0: "Story {id} failed validation. Review Story/Task structure."
  - IF any crash_count > 0: "Worker crashed {N} times for {id}. Check for context-heavy operations."
  - IF any PAUSED: "Stories {ids} require manual intervention."
  - IF any Linear sync mismatches: "Linear/kanban sync issues detected for {ids}. Verify statuses manually."
  - IF any infra_issues with type "hook": "Hook configuration errors. Verify settings.local.json and .claude/hooks/."
  - IF any infra_issues with type "git": "Git conflicts encountered. Rebase feature branches more frequently."
  - IF any infra_issues with type "worktree": "Worktree failures. Check disk space and existing worktree state."
  - IF all DONE with 0 retries AND no infra_issues: "Clean run — no issues detected."

Append Process Improvement section (auto-generated from pipeline analysis):
  ## Process Improvement Suggestions
  Analyze pipeline session and generate suggestions in 4 categories:

  ### Efficiency (reduce time/steps)
  - IF any story went through all 4 stages (0→1→2→3): "Consider skipping Stage 0/1 for stories with pre-validated tasks (resume from Stage 2)."
  - IF multiple stories produced similar Stage 0 output: "Stories {ids} had similar task plans. Consider task templates to skip planning."
  - IF Stage 2 was bottleneck (longest stage across stories): "Execution dominated pipeline time. Split large stories for better parallelism."

  ### Cost (reduce token usage)
  - IF any crash_count > 0: "Crashes waste full stage token budget. Reduce context-heavy operations or add intermediate checkpoints."
  - IF quality_cycles > 0: "Rework cycles multiply cost — Stage 2+3 repeated {N} times. Invest in better task specs upfront (ln-300)."
  - IF validation_retries > 0: "Validation retry = wasted Stage 0+1. Improve story templates or run ln-310 earlier."
  - General: "Review worker prompt sizes. Shorter focused prompts reduce per-spawn token cost."

  ### Quality (improve output)
  - IF any Stage 3 verdict was CONCERNS: "Story {id} passed with concerns. Tighter AC or stricter test coverage may prevent debt."
  - IF any Stage 3 score < 80: "Low quality ({score}/100) for {id}. Consider: more specific AC, ln-002 research before coding, stricter ln-402 review."
  - IF agent reviews (ln-512) found issues not caught by ln-402: "External agents caught missed issues. Consider running agent review earlier."
  - IF all scores > 90: "High quality scores. Current process works well — maintain."

  ### Process Architecture (structural improvements)
  - IF pipeline ran > 5 stories: "Large batch. Consider increasing max_workers or grouping into sub-batches."
  - IF any PAUSED: "PAUSED stories indicate systematic issues. Analyze: task spec quality? Missing context? Unclear AC?"
  - IF depends_on blocked stories for extended periods: "Dependency chains caused idle workers. Reorder stories to minimize blocking."
  - General: "Compare metrics across runs to track trends: quality_score, avg cycles per story, crash rate."

# 4. Show pipeline summary to user
```
Pipeline Complete:
| Story | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Merged | Final State |
|-------|---------|---------|---------|---------|--------|------------|
| PROJ-42 | skip | skip | skip | PASS 92 | yes | DONE |
| PROJ-55 | 5 tasks | GO | Done | PASS 85 | yes | DONE |
| PROJ-60 | skip | NO-GO | — | — | — | PAUSED |

Report saved: docs/tasks/reports/pipeline-{date}.md
```
# 5. Shutdown remaining workers (if any still active)
FOR EACH worker_name IN worker_map.values():
  SendMessage(type: "shutdown_request", recipient: worker_name)

# 6. Cleanup team
TeamDelete

# 7. Remove remaining worktrees (PAUSED stories not cleaned by Phase 4a)
IF .worktrees/ directory exists:
  FOR EACH story in worktree_map WHERE worktree_dir != null:
    git worktree remove {worktree_dir} --force
  rm -rf .worktrees/

# 8. Ensure on develop branch
git checkout develop

# 9. Remove pipeline state files
Delete .pipeline/ directory

# 10. Report results and report location to user
```

## Kanban as Single Source of Truth

- **Lead = single writer** to kanban_board.md. Workers report results via SendMessage; lead updates the board
- **Re-read board** after each stage completion for fresh state
- **Update algorithm:** Follow `shared/references/kanban_update_algorithm.md` for Epic grouping and indentation

## Error Handling

| Situation | Detection | Action |
|-----------|----------|--------|
| ln-300 task creation fails | Worker reports error | Escalate to user: "Cannot create tasks for Story {id}" |
| ln-310 NO-GO (Score <5) | Worker reports NO-GO | Retry once (ln-310 auto-fixes). If still NO-GO -> ask user |
| Task in To Rework 3+ times | Worker reports rework loop | Escalate: "Task X reworked 3 times, need input" |
| ln-500 FAIL | Worker reports FAIL verdict | Fix tasks auto-created by ln-500. Stage 2 re-entry. Max 2 quality cycles |
| Worker crash | TeammateIdle without completion msg | Re-spawn worker, resume from last stage |
| All Stories blocked | Empty actionable queue | Report to user, cleanup team |
| Business question mid-execution | Worker encounters ambiguity | Worker -> lead -> user -> lead -> worker (message chain) |
| Merge conflict | git merge --squash fails | Escalate to user, Story PAUSED, manual resolution required |

## Critical Rules

1. **Max 2 concurrent Stories.** Never spawn more than 2 story-workers simultaneously
2. **Delegate mode.** Lead coordinates only — never invoke ln-310/ln-400/ln-500 directly. Workers do all execution
3. **Skills as-is.** Never modify or bypass existing skill logic. Workers call `Skill("ln-310-story-validator", args)` exactly as documented
4. **Single kanban writer.** Only lead updates kanban_board.md. Workers report via SendMessage
5. **Quality cycle limit.** Max 2 quality FAILs per Story (1 retry cycle). After 2nd FAIL, escalate to user
6. **Squash per Story.** Each Story that passes quality gate gets squash-merged to develop separately. No batch merges
7. **Re-read kanban.** After every stage completion, re-read board for fresh state. Never cache
8. **Graceful shutdown.** Always shutdown workers via shutdown_request. Never force-kill

## Anti-Patterns
- Running ln-300/ln-310/ln-400/ln-500 directly from lead instead of delegating to workers
- Spawning >2 workers simultaneously
- Updating kanban from worker (only lead updates)
- Skipping quality gate after execution
- Merging to develop before quality gate PASS
- Caching kanban state instead of re-reading
- Reading `~/.claude/teams/*/inboxes/*.json` directly (messages arrive automatically)
- Using `sleep` + filesystem polling for message checking
- Parsing internal Claude Code JSON formats (permission_request, idle_notification)
- Reusing same worker across stages (context exhaustion — spawn fresh worker per stage)
- Processing messages without verifying sender matches worker_map (stale message confusion from old/dead workers)

## Plan Mode Support

When invoked in Plan Mode, generate execution plan without creating team:

1. Parse kanban board (Phase 1)
2. Build priority queue
3. Show pipeline plan table (which Stories, which stages)
4. Write plan to plan file, call ExitPlanMode

**Plan Output Format:**
```
## Pipeline Plan for {date}

| # | Story | Status | Stage | Skill | Expected Outcome |
|---|-------|--------|-------|-------|-----------------|
| 1 | {ID}: {Title} | To Review | 3 | ln-500 | Done + PR |
| 2 | {ID}: {Title} | Todo | 2 | ln-400 | To Review |

### Execution Sequence
1. TeamCreate("pipeline-{date}")
2. Spawn story-worker for {Story-1} -> Stage 3 (ln-500)
3. Spawn story-worker for {Story-2} -> Stage 2 (ln-400)
4. Wait for completions, advance stages, squash-merge to develop
5. Cleanup
```

## Definition of Done (self-verified in Phase 5)

| # | Criterion | Verified By |
|---|-----------|-------------|
| 1 | Kanban board parsed, priority queue built | `priority_queue` was populated |
| 2 | Business questions asked in single batch (or none found) | `business_answers` stored OR skip |
| 3 | Team created, workers spawned (max 2 concurrent) | `active_workers` never exceeded 2 |
| 4 | ALL Stories processed: state = DONE or PAUSED | `ALL story_state[id] IN ("DONE", "PAUSED")` |
| 5 | Every DONE Story squash-merged into develop | Feature branches merged, on develop branch |
| 6 | Pipeline summary shown to user | Phase 5 table output |
| 8 | Team cleaned up (workers shutdown, TeamDelete) | `active_workers == 0`, TeamDelete called |

## Reference Files
- **Message protocol:** `references/message_protocol.md`
- **Worker health:** `references/worker_health_contract.md`
- **Checkpoint format:** `references/checkpoint_format.md`
- **Settings template:** `references/settings_template.json`
- **Hooks:** `references/hooks/pipeline-keepalive.sh`, `references/hooks/worker-keepalive.sh`
- **Kanban parsing:** `references/kanban_parser.md`
- **Pipeline states:** `references/pipeline_states.md`
- **Worker prompts:** `references/worker_prompts.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Storage mode detection:** `shared/references/storage_mode_detection.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Skills invoked:** `../ln-300-task-coordinator/SKILL.md`, `../ln-310-story-validator/SKILL.md`, `../ln-400-story-executor/SKILL.md`, `../ln-500-story-quality-gate/SKILL.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-13
