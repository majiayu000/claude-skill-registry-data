---
name: delegate
description: |
  Snapshots the full current context — open file, conversation history, project memory files,
  decisions made, and what's left — then hands the task off to a specialized subagent (preferred)
  or general-purpose subagent (fallback) that drives to completion autonomously. Use when you need
  to offload work without losing context, when a task spans files or domains that don't fit a
  focused specialist, or when you want a subagent to own a task end-to-end while you stay free to
  work on other things. Also useful for keeping the main context window clean during long multi-step
  sessions. The subagent receives a structured briefing and works independently — no further
  prompting required. Check Agency catalog for named specialists first.
triggers:
  - /delegate
  - delegate this task
  - finish this for me
  - hand off to subagent
aliases: []
scope: global
dept: [all]
team: ["-"]
priority: implementation
author: skill-seekers
provenance: skill-seekers
last_updated: "2026-04-10"
trust_level: agent-authored
---

# delegate

Delegates the current task to a `general-purpose` subagent with enough context to complete it independently. Unlike a focused specialist, this subagent has full tool access and drives the task to completion — no further prompting needed.

## When to Use

- You want a subagent to own a task end-to-end
- You need to offload work without losing context
- A focused skill agent isn't the right tool shape — the task spans files, tools, or domains

## Workflow

### Step 1 — Detect the Task File

The user has a file open in the IDE. Read it first — it's the anchor for context.

**Read the file from `ide_opened_file`** (already provided in the prompt as a system-reminder). Extract:
- The file path
- Any relevant content (look for task descriptions, TODOs, comments about what needs doing)

### Step 2 — Find Project Memory

Determine the project directory. Common patterns:
- `~/.claude/agents/{slug}/` — Agent/PD project
- Current working directory or parent `CLAUDE.md`

Read the following files if they exist (in order of priority):

```
memory/next-session.md      ← session-start briefing, carries forward context
memory/decisions.md        ← decisions made so far
memory/heartbeat.md        ← recent status / what's been worked on
memory/state.md            ← machine-readable state snapshot
memory/TODOS.md            ← outstanding tasks
CLAUDE.md                  ← project-level instructions and constraints
PROJECT.md                ← project overview and goals
```

### Step 3 — Synthesize the Briefing

Construct a briefing block that answers:

```
## Task
[What needs to be done — one sentence, then expanded]

## What's Been Done
[Decisions made, code written, files modified — be specific with paths]

## What's Left
[Outstanding tasks, TODOs, open questions]

## Context & Constraints
- Working file: [path]
- Project: [name/slug]
- Any constraints from CLAUDE.md or decisions.md
- Any relevant file paths the subagent needs to look at

## Verify Before Claiming Done
[The standard this task must meet — e.g., tests pass, builds, user confirms]
```

**Be specific.** "The app needs auth" is vague. "Add JWT session middleware to the /api/auth route using the existing AuthService — see src/auth/middleware.ts as a reference" is actionable.

If no project memory files exist, fall back to a brief summary based on the conversation history up to this point. State what's clear and what the subagent should infer.

### Step 4 — Spawn the Subagent

Use the `Agent` tool — check Agency catalog first. If a named specialist fits the task domain, use it. If not, use `subagent_type: general-purpose` (this skill's purpose is end-to-end delegation, which general-purpose is suited for).

```json
{
  "description": "Complete: [1-line task summary]",
  "name": "[short-slug-for-task]",
  "prompt": "[full briefing block from Step 3]",
  "subagent_type": "[named specialist — check Agency catalog first; general-purpose if no match]"
}
```

Use `run_in_background: true` for long-running tasks, `false` (default) for tasks that return a result to report back.

### Step 5 — Report

Report back to the user:
- What the subagent is doing
- Its name (for reference if the user wants to message it directly)
- That it will drive to completion independently

## Briefing Quality Checklist

- [ ] Working file path included
- [ ] Task goal is explicit and unambiguous
- [ ] What's been done is specific (file paths, not just "work in progress")
- [ ] What's left is a clear list, not vague
- [ ] Any constraints from CLAUDE.md are called out
- [ ] Verification criteria are stated

## Edge Cases

| Situation | Behavior |
|---|---|
| No memory files exist | Synthesize from conversation history; note uncertainty |
| ide_opened_file is blank/unclear | Infer task from conversation; note assumption |
| Task is trivial (1-2 steps) | Still delegate — use brief briefing, keeps context clean |
| Subagent spawn fails | Report error; suggest running task directly |
| User interrupts | No special handling — subagent continues in background |

## Notes

- The subagent does **not** report back to you automatically — it completes and the user sees the result.
- If you need to send a message to the running subagent, use `SendMessage({to: "[name]"})`.
- For running background tasks, you will be notified when it completes.
- Do NOT send a shutdown message to the subagent unless the user explicitly requests it.
