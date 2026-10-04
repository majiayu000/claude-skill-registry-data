---
name: context-switch
description: "Switch between professional and personal contexts. Use when user mentions 'switch context', 'change context', '@teamname', or wants to see current context status."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Context Switch

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Switch between professional and personal contexts in the CTO system.

## Commands

- `/ctx` - Show current context and list available contexts
- `/ctx {name}` - Switch to a specific context
- `/ctx status` - Show status of all contexts

## Available Contexts

Contexts are defined in `pos.yaml`. Each context has shortcuts for quick switching.

| Shortcut | Context | Type |
|----------|---------|------|
| `@work`, `@company` | work | Employment |
| `@client-a` | client-a | Consulting |
| `@side-project` | side-project | Product |
| `@personal`, `@learn` | personal | Personal |

Customize the table above by editing `pos.yaml` to match your contexts.

## Process

### `/ctx` (no args) - Show Current Context

1. Read all context status files to find active session
2. Display current context info

```bash
# Read registry
cat pos.yaml

# Check each context's status.yaml for session_active
```

**Output format:**
```
## Current Context: {context_name}

**Role:** {role}
**Organization:** {organization}
**Session Active:** {yes/no}
**Current Task:** {task or "None"}

## Available Contexts
| Context | Type | Status |
|---------|------|--------|
| ... | ... | ... |

Switch with: /ctx {name}
```

### `/ctx {name}` - Switch Context

1. Validate context name exists in registry
2. Read target context's AGENTS.md and status.yaml
3. Display context info and set as active

**Steps:**
```bash
# 1. Read registry to validate context
cat pos.yaml

# 2. Determine context path from pos.yaml
# All contexts live under: contexts/{context}/

# 3. Read context files
cat {context_path}/AGENTS.md
cat {context_path}/status.yaml
```

**Output format:**
```
## Switched to: {context_name}

**Role:** {role}
**Organization:** {organization}
**Primary Agent:** {agent}

### Focus Areas
- {focus_area_1}
- {focus_area_2}

### Current Status
{status from status.yaml}

### Quick Commands
{commands from AGENTS.md}
```

### `/ctx status` - All Contexts Status

1. Read pos.yaml for all contexts
2. Read each context's status.yaml
3. Display unified status view

**Output format:**
```
## Context Status Overview

| Context | Type | Session | Current Task |
|---------|------|---------|--------------|
| work | Employment | - | - |
| client-a | Consulting | Active | Sprint 3 |
| personal | Personal | - | - |

Total contexts: {count}
Active sessions: {count}
```

## Context Paths

All contexts follow the same path pattern: `contexts/{context-id}/`

| Context | Path |
|---------|------|
| work | `contexts/work/` |
| client-a | `contexts/client-a/` |
| side-project | `contexts/side-project/` |
| personal | `contexts/personal/` |

## Shortcut Resolution

When user types `@work`, `@client-a`, etc., resolve using the shortcuts map in pos.yaml:

```yaml
shortcuts:
  "@work": work
  "@company": work
  "@client-a": client-a
  "@side-project": side-project
  "@personal": personal
  "@learn": personal
```

## Notes

- Context switch does NOT automatically start a session
- Use `/session start {context}` to start tracking time
- Shortcuts are defined in `pos.yaml` under each context's `shortcuts` field

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
