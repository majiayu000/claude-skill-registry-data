---
name: backlog-resume
description: Check for in-progress work on session start. Use when beginning a new session in a project with backlog.org. Triggers automatically at session start or when user says "what was I working on?", "resume", "continue", or "where did I leave off?". Surfaces WIP tasks and handoff notes to enable seamless session continuity.
---

# Backlog Resume

This skill checks for in-progress work when starting a new session, implementing the "hook pattern" from gastown - if there's work on your hook, you should run it.

## When to Offer This Workflow

**Trigger conditions:**
- Starting a new session in a project with `backlog.org`
- User asks "what was I working on?", "resume", "continue"
- User says "where did I leave off?"

**Initial check:**
Read `backlog.org` and look for WIP tasks in the Active section.

## Workflow

### 1. Check for WIP Tasks

Read `* Current WIP` > `** Active` section in backlog.org.

Look for tasks with state `WIP` (work in progress).

### 2. Surface Handoff Notes

For each WIP task found:
- Read the `:HANDOFF:` property
- Read recent progress notes (entries starting with `[YYYY-MM-DD]`)

### 3. Present Resume Option

If WIP task(s) found, display:

```
## Work in Progress

Found active work from previous session:

### [TASK-ID] Task Title

**Handoff notes:**
> <content of :HANDOFF: property>

**Recent progress:**
> <last progress note>

Continue working on this task?
```

### 4. If No WIP Tasks

Check if there are TODO tasks in Active section:

```
## Ready to Start

No work in progress. Active queue:

1. [TASK-ID-1] Task title
2. [TASK-ID-2] Task title

Start one of these tasks?
```

### 5. Handle Response

- If user wants to continue: Run `/task-start <task-id>`
- If user wants different task: Queue or start the requested task
- If user declines: Proceed with whatever they want to do

## Example

```
User: <starts session>

Claude: "Checking backlog.org for in-progress work...

## Work in Progress

Found active work from previous session:

### [DAB-005-01] Implement handoff notes

**Handoff notes:**
> Stuck on property format. Check org-mode docs for multi-line properties.

**Recent progress:**
> [2026-01-03] Started implementation. Template updated.

Continue working on this task?"
```

## Related Commands

| Command | When to use |
|---------|-------------|
| `/task-start <id>` | Resume the WIP task |
| `/task-queue <id>` | Add a new task to Active |
| `/task-hold <id> <reason>` | If task is blocked |
