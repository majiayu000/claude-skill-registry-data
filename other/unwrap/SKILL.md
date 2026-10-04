---
name: unwrap
description: "Reads inbox task save-state files and resumes work autonomously — briefing + spawn. Trigger when the user invokes /unwrap [task-slug], says \"unwrap task\", \"pick up inbox task\", or \"continue task\". Similar to /pd-resume but for single inbox tasks: spawns a briefing subagent, collects the briefing, then spawns a task worker that starts the next action immediately. SSOT for task paths is ~/.claude/tasks/inbox/."
---

# Unwrap — Inbox Task Recall + Resume

Parses targets, spawns briefing subagents, collects briefings, spawns task workers.
All autonomous — no user interaction between briefing and execution.

## Step 1 — Parse Target

Accept an argument: `all` (resume all ongoing tasks) or a single task slug.

- `all` → resume every task in ~/.claude/tasks/inbox/ongoing/
- `[slug]` → resume only that task — spawn exactly one briefing + one worker

If slug is given but no matching folder exists in ongoing/, output:
```
TASK NOT FOUND: [slug]
Hint: Check ~/.claude/tasks/inbox/ongoing/ for the current task list.
```
Then stop.

## Step 2 — Spawn Briefing Subagent(s) in Parallel

Use the Agent tool to spawn general-purpose sonnet subagents. Spawn one per target simultaneously.

Subagent prompt per task:

"Read-only briefing for task '{slug}'. Do NOT write any files.

PERMISSIONS: read-only. No write/edit/create.

## Scope
- Task dir: ~/.claude/tasks/inbox/ongoing/{slug}/
- Session logs: ~/.claude/tasks/inbox/ongoing/{slug}/sessions/

FILES TO READ:
- ~/.claude/tasks/inbox/ongoing/{slug}/TASK.md
- Most recent session log in ~/.claude/tasks/inbox/ongoing/{slug}/sessions/
  — list sessions/ first to find the most recent file

OUTPUT FORMAT (write exactly this to /tmp/unwrap-{slug}.briefing):

UNWRAP — {slug}

Title: [from TASK.md]
Status: [from TASK.md]
Priority: [from TASK.md — high/medium/low]
Next: [specific next action — one sentence]
Blockers: [list one per line, or "none"]
Context: [what was happening — 1-2 sentences from session log or TASK.md]

--- Session History ---
[session date] — [1-line summary]
[...most recent 3 sessions...]

RULES:
- Read-only. Do NOT write or edit any files except /tmp/unwrap-{slug}.briefing.
- If a file doesn't exist, skip that field and note "N/A".
- Keep every field to 1-2 lines max.
- Be specific — "write unit tests for auth module" not "write tests".
- Write ONLY the briefing above to /tmp/unwrap-{slug}.briefing. Then stop."

subagent_type: general-purpose
model: sonnet

Wait for all briefing subagents to complete.

## Step 3 — Read Briefings

Read each `/tmp/unwrap-{slug}.briefing` file. Collect all.

## Step 4 — Spawn Task Worker(s) in Parallel

After all briefings are collected, read each `/tmp/unwrap-{slug}.briefing` file.
Then spawn one task worker per target simultaneously — briefing embedded directly
in the spawn prompt. Workers start immediately.

Task worker spawn prompt:

"You are resuming work on inbox task '{slug}'. Your briefing from the last session is
below. Read it carefully — this is your context. Start the stated 'Next' action immediately.

============================================
[READ /tmp/unwrap-{slug}.briefing — paste its full content here as the briefing]
============================================

## Task Scope (do not read — always embedded here)
- Task dir: ~/.claude/tasks/inbox/ongoing/{slug}/
- TASK.md: ~/.claude/tasks/inbox/ongoing/{slug}/TASK.md
- Sessions: ~/.claude/tasks/inbox/ongoing/{slug}/sessions/

## Task Protocol — NON-NEGOTIABLE

1. DECOMPOSE: Break every task into the smallest possible independent sub-tasks.
   Do not do any work yourself until sub-tasks are decomposed.

2. PARALLELIZE: In a SINGLE message, spawn one Agent per sub-task.
   All subagents must be launched simultaneously. Do not wait between spawns.

3. REPORT: After EACH subagent completes, send a SendMessage to "team-lead":
   - DONE: "{subtask-label}: DONE — [brief description]"
   - BLOCKED: "{subtask-label}: BLOCKED — [reason] — [workaround]"
   Report immediately on completion, not at the end of all work.

Agent template: general-purpose (task workers use Sonnet)

Start immediately on 'Next'. Do not re-read task docs unless the briefing says to.
When a task block is complete or you are blocked, run /wrap then stop.

subagent_type: general-purpose
model: sonnet

Wait for all task workers to report back.

## Step 5 — Output Summary

Read `/tmp/unwrap-{slug}.briefing` to extract Status, Priority, Next, and Blockers
for each task. Output:

```
UNWRAP — {n} task(s)

{slug} — [Status] [Priority] — spawned
  next: [Next from briefing]
  blockers: [Blockers from briefing]

[...one per task...]

All task workers running. Results arrive as each completes.
```

Then stop. No further narration.