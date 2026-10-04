---
name: session-management
description: "Start or end a work session for any context (teams or other contexts). Use when starting work, ending a session, or when user mentions 'start session', 'end session', 'begin work on', 'finish work on', 'session start', 'session end'."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Session Management

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Automate session start/end protocol for all contexts.

## Commands

- `/session start {context}` - Start a session
- `/session end [context]` - End current session with handoff notes
- `/session status` - Show session state across all contexts

## Context Path Resolution

| Context Type | Path Pattern |
|--------------|--------------|
| Contexts | `contexts/{context}/status.yaml` |

## `/session start {context}`

1. Register session: `./scripts/session-register.sh "claude-code" "{context}" "reasoning"`
2. Determine path: `contexts/{context}/`
3. Read `status.yaml` and context info (`AGENTS.md`)
4. Check `.handoff/sessions/` for conflicts
5. Update status.yaml:
   ```yaml
   session:
     active: true
     started: "{ISO timestamp}"
     task: null
   last_updated: "{timestamp}"
   ```
6. Display: context info, resume point, current status, pending items, blockers
7. Ask: "What would you like to work on this session?"

## `/session end [context]`

1. Scan status files for `session.active: true`; if multiple, ask which
2. Ask: accomplishments + blockers/notes for next session
3. Update status.yaml with `active: false`, `ended`, completed items, resume_point
4. Close session: `./scripts/session-close.sh "claude-code" "{summary}"`
   - Creates `.handoff/handoffs/{date}-claude-code.yaml`
   - Removes `.handoff/sessions/claude-code.yaml`
   - Re-syncs `.state/snapshot.yaml`
5. Enrich handoff record: completed, pending, blockers, files_modified, resume_point
6. Check `git status` — remind about uncommitted changes
7. Display handoff summary

## `/session status`

1. Scan: `contexts/*/status.yaml`
2. Check `session.active` field in each
3. Display unified table: context, type, current task, started/last updated

## Notes

- Context switch does NOT auto-start session — use `/session start`
- Keep `resume_point` detailed enough for another agent to continue
- Use ISO 8601 timestamps
- Commit changes before ending session

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
