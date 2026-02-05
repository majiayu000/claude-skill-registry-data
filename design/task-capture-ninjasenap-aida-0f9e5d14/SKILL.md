---
name: task-capture
description: Quick, structured task capture with automatic processing. Use when user wants to capture a task, add a todo, or remember something. Auto-triggers on phrases like "I need to...", "remind me to...", "add task", "new todo", "capture this", "jag måste...", "lägg till uppgift", "fånga detta".
allowed-tools: Bash, Read
---

# Skill: task-capture

## Purpose

Provides minimal-friction task capture that processes natural language input into structured tasks. Focuses on SPEED over perfectionism - get it captured, refine later if needed.

## Trigger Conditions

- **Slash command:** `/capture [text]`
- **Natural phrases:** ["I need to...", "remind me to...", "add task", "new todo", "capture this", "jag måste...", "lägg till uppgift", "fånga detta", "kom ihåg att...", "todo:", "task:"]
- **Auto-trigger:** When user expresses something they need to do

## Required Context (gather BEFORE starting workflow)

1. Active roles via `roles getActiveRoles` → returns Role[] for role inference
2. Active projects via `projects getActiveProjects` → returns Project[] for project linking (optional)

**How to gather context:**
```bash
# Get active roles (for role inference/selection)
bun run src/aida-cli.ts roles getActiveRoles

# Get active projects (optional, for project association)
bun run src/aida-cli.ts projects getActiveProjects
```

## Workflow Steps

### Step 1: Parse Input

See [PARSING-RULES.md](PARSING-RULES.md) for detailed parsing rules.

- **Action:** Extract task title, deadline hints, role hints, project hints, energy hints, priority hints
- **Output to user:** None (internal processing)
- **Wait for:** Continue immediately

### Step 2: Infer Role

See [ROLE-INFERENCE.md](ROLE-INFERENCE.md) for detailed inference rules.

- **Action:** Match keywords, project context, or conversation context to determine role
- **Output to user:** If ambiguous, ask "Vilken roll gäller detta?" with role options
- **Wait for:** User selects role (only if ambiguous)

### Step 3: Check for Duplicates (Optional)

- **Action:** Search existing tasks via `tasks searchTasks "[parsed title]"`
- **Output to user:** If similar task found, warn: "Det finns redan en liknande uppgift: [title]. Vill du lägga till ändå?"
- **Wait for:** User confirms or cancels

### Step 4: Create Task

- **Action:** Create task via `tasks createTask {...}`
- **CLI call:**
  ```bash
  bun run src/aida-cli.ts tasks createTask '{
    "title": "[parsed title]",
    "role_id": [inferred/selected role id],
    "deadline": "[parsed date or null]",
    "priority": [0-3, default 0],
    "energy_requirement": "[low/medium/high or null]",
    "project_id": [associated project or null]
  }'
  ```
- **Output to user:** None yet
- **Wait for:** Continue immediately

### Step 5: Create Journal Entry

- **Action:** Log capture via `journal createEntry {...}`
- **CLI call:**
  ```bash
  bun run src/aida-cli.ts journal createEntry '{
    "entry_type": "task",
    "content": "Fångade: [task title]",
    "related_task_id": [created task id]
  }'
  ```
- **Output to user:** None yet
- **Wait for:** Continue immediately

### Step 6: Confirm & Suggest Next Step

- **Output to user:**
  ```
  ✅ Fångat: "[task title]"
     Roll: [role name]
     [Deadline: datum] (if set)

  Vill du göra något mer med den? (annars är den sparad i captured-status)
  ```
- **Optional follow-ups:**
  - "Vill du sätta en deadline?"
  - "Ska vi aktivera den nu?" (triggers task-activation)
  - "Finns det fler saker att fånga?"
- **Wait for:** User input (optional)

## Output Format

- **Language:** Swedish (default)
- **Style:** Quick confirmation, minimal text
- **Confirmation:** Always show captured task with role and deadline (if set)

**Example output:**
```
✅ Fångat: "Ringa tandläkaren"
   Roll: Förälder

Sparad! Något mer?
```

**Example with deadline:**
```
✅ Fångat: "Skicka rapporten till chefen"
   Roll: Systemutvecklare
   Deadline: 2025-12-20

Sparad med deadline! 📅
```

## Error Handling

- **If `roles getActiveRoles` returns empty:** Show error "Inga roller finns. Du behöver skapa roller först via profile-management."
- **If role inference fails and no clarification:** Use first active role as default and inform user "Sparad i [role name]. Om det är fel roll kan du ändra senare."
- **If `tasks createTask` fails:** Show error message with details, ask user if they want to retry
- **If `journal createEntry` fails:** Task is still created, just log warning to console and continue
- **If duplicate task found:** Warn user and ask for confirmation before proceeding
- **If project not found:** Ignore project_id and create task without project association

## Anti-patterns

- **NEVER create task without role_id** - always infer or ask for role
- **NEVER use non-existent project_id** - validate project exists before associating
- **NEVER over-ask** - infer as much as possible, only ask if truly ambiguous
- **NEVER force all fields** - capture with minimal info, user can refine later
- **NEVER modify existing tasks** - only create new ones
- **NEVER change task status** - tasks are created with status='captured'
- **NEVER use direct SQL** - always use aida-cli.ts
- **NEVER run query modules directly** (e.g., `bun run src/database/queries/tasks.ts`)

## Tool Contract

**Allowed CLI Operations:**
- **tasks:** createTask, searchTasks (duplicate check)
- **roles:** getActiveRoles, getRoleById (READ ONLY)
- **projects:** searchProjects, getActiveProjects (READ ONLY)
- **journal:** createEntry (type: task)

**Forbidden Operations:**
- Updating existing tasks
- Changing task status
- Deleting tasks
- Any profile operations
- Any plan operations

**Default Task Values:**
- status: `captured`
- priority: inferred or null
- energy_requirement: inferred or null

**File Access:**
- **No file reads needed**
- **No file writes** - All operations via CLI

## Supporting Documentation

- [PARSING-RULES.md](PARSING-RULES.md) - How to parse natural language input
- [ROLE-INFERENCE.md](ROLE-INFERENCE.md) - Rules for inferring roles
- [QUICK-CAPTURE.md](QUICK-CAPTURE.md) - Minimal-friction capture flow

## Design Principles

1. **Speed over perfection** - Capture now, refine later
2. **Minimal questions** - Infer as much as possible
3. **Non-blocking** - Don't force user to fill in all fields
4. **Confirm, don't interrogate** - Show what was captured, offer to adjust
