---
name: cross-handoff
description: "Create and manage cross-agent handoff records. Use when handing off work to another agent/model, creating task records, or when user mentions 'handoff', 'hand off', 'pass to another agent', 'create handoff'."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Cross-Agent Handoff

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Manage file-based handoffs between AI agents.

## Commands

- `/handoff create {team} {description}` - Create a handoff record
- `/handoff resume {handoff-id}` - Resume work from a handoff
- `/handoff list` - List pending handoffs
- `/handoff close {handoff-id}` - Complete a handoff

## File Locations

- Queue: `/.handoff/queue.yaml`
- Sessions: `/.handoff/sessions/`
- Handoffs: `/.handoff/handoffs/`

## `/handoff create {team} {description}`

1. **Gather:** summary of work, current state, next steps, blockers, files modified
2. **Create** `.handoff/handoffs/{date}-{team}-{id}.yaml`:
   ```yaml
   handoff_id: "2026-01-12-{team}-001"
   created_at: "{timestamp}"
   created_by: "claude-opus"
   team: {team}
   project: {project}
   task_type: bug-fix | feature | refactor | research
   title: "{short description}"
   description: |
     {detailed description}
   completed:
     - "{things done}"
   files_modified:
     - path: "{file}"
       changes: "{what changed}"
   current_state: |
     {where work stands}
   next_steps:
     - "{what to do next}"
   blockers:
     - "{any blocking issues}"
   context:
     relevant_files: [...]
     key_decisions: |
       {important decisions}
     gotchas: |
       {things to watch out for}
   required_capability: basic | standard | advanced | reasoning
   ```
3. **Optionally update** `/.handoff/queue.yaml` status
4. **Output** confirmation with ID, file path, next steps

## `/handoff resume {handoff-id}`

1. Read `.handoff/handoffs/{handoff-id}.yaml`
2. Load all `files_modified` and `context.relevant_files`
3. Display: previous work, current state, tasks, blockers, key context

## `/handoff list`

Scan `.handoff/handoffs/*.yaml`, display summary table (ID, team, title, created, capability).

## `/handoff close {handoff-id}`

Add `closed_at`, `closed_by`, `resolution` to handoff file. Optionally move to `archive/`.

## Capability Levels

| Level | Models | Suitable Tasks |
|-------|--------|----------------|
| basic | Haiku, Flash | Status, docs, formatting |
| standard | Sonnet, GPT-4o | Bug fixes, features |
| advanced | Sonnet+ | Architecture, refactoring |
| reasoning | Opus, o3 | Planning, root cause analysis |

Full SOP: `docs/system/sops/cross-agent-handoff.md`

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
