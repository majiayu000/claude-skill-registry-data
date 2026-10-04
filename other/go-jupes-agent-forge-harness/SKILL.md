---
name: go
description: Classify a task and route it to the right workflow (fix / feature / epic). Use when the user runs /go or wants the adaptive workflow router.
---

# /go — Adaptive Workflow Router

Single entry point for all development work. Classifies scope and routes to the right workflow.

## Usage
```
/go                          # Pick highest-priority ready task
/go T-42                     # Work on specific task
/go EPIC-7                   # Run epic workflow
/go fix login redirect bug   # Describe work in free text
/go path/to/spec.md          # Read spec file, materialize Beads tasks
/go --epic <description>     # Force epic workflow
```

---

## Input Handling

### Empty input
```bash
bd ready
```
Pick the first unblocked, unclaimed task. If none: report "No ready work. Check `bd ready` or create new tasks."

### Task/Epic ID (e.g., `T-42`, `EPIC-7`)
```bash
bd show <id>
```
Fetch details, then classify scope and route to workflow.

### File path
Read the file as a spec. Materialize Beads tasks from it (see Spec Materialization below), then route.

### Free text
Use the description directly. Classify scope, create a Beads task if needed, then route.

### `--epic` flag
Force epic workflow regardless of scope classification.

---

## Scope Classification

Evaluate the task to determine which workflow to use:

| Tier | Criteria | Routes To |
|------|----------|-----------|
| **Fix** | Single task, ≤3 files touched, clear scope, no new architecture | `workflows/fix.md` |
| **Feature** | Single task, >3 files OR needs a plan OR new system/component | `workflows/feature.md` |
| **Epic** | Epic ID, `--epic` flag, or multiple tasks from spec | `workflows/epic.md` |

**When in doubt about Fix vs Feature**: check whether a plan would help. If yes → Feature.

---

## Spec Materialization

When input is a file path, parse the spec and create Beads tasks:

1. Read the file
2. Identify distinct work items (look for headers, numbered lists, bullet points with verbs)
3. For each item:
   ```bash
   bd create \
     --type <bug|feature|task|chore> \
     --title "<derived title>" \
     --repo <repo from spec or ask> \
     --priority <value> \
     --acceptance "<acceptance criterion if identifiable>"
   ```
   Set **`<value>`** using `.claude/skills/beads-priority-assignment/SKILL.md`.
4. If items have clear dependencies (item B requires item A), add them:
   ```bash
   bd dep add <B-id> --requires <A-id>
   ```
5. If there are 3+ related items: create an epic to group them
   ```bash
   bd create --type epic --title "<overall goal>" --priority <value>
   ```
   Epic **`<value>`**: same skill — reflect overall urgency of the group.
6. Report what was created, then route

---

## PR Stack Detection

Before routing, check for PR stacks (existing open PRs for the repo):

```bash
gh pr list --state open --json number,title,baseRefName,headRefName
```

If the current branch is part of a stack (a PR whose base is another feature branch):
- Note the stack structure
- When shipping later, use the correct base branch for the PR, not `main`

---

## Routing

After classification, invoke the appropriate workflow:

```
→ Fix:     Follow .claude/workflows/fix.md
→ Feature: Follow .claude/workflows/feature.md
→ Epic:    Follow .claude/workflows/epic.md
           (Adopt the Lead Agent role from .claude/agents/lead.md)
```

Announce routing decision before starting:
```
Routing to: [Fix/Feature/Epic] workflow
Task: <id> — <title>
Reason: <1 sentence why this tier>
```

---

## Error Handling

- **Task not found**: `bd show <id>` returns empty → check ID, suggest `bd ready`
- **Ambiguous spec**: >10 items from a single spec → ask user to confirm before materializing
- **No git repo**: abort with instructions to `git init`
- **Beads unreachable** (`bd` errors / Dolt server down): **STOP — do not proceed without Beads.** Run `bd dolt start` and retry; Beads tracking is mandatory for tracked work. (The SessionStart hook normally auto-starts the server.) Only if `bd` is genuinely not installed should you tell the user to install it before continuing.
