---
name: kanban-lite
version: v0.0
description: Lightweight local kanban boards stored in SQLite — track tasks, view board state, create/update/move cards. Syncs across machines via git.
allowed-tools: Bash(node *)
---

# Kanban Lite — Local SQLite Board Management

Lightweight kanban boards stored in a local SQLite file. No external database — syncs across machines via git commits.

## Prerequisites

- Run `${CLAUDE_SKILL_DIR}/scripts/setup.sh` once to install dependencies

## Commands

Run commands via:
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs <command> [options]
```

### Sync

**Always sync before and after working with the board:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs sync
```
Pulls latest changes, then commits and pushes any local db changes.

### Read Operations

**List all boards:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs boards
```

**View a board (lists + cards):**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs board <board-id>
```

**Search cards across all boards:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs search --query "search term"
```

### Card Operations

**Create a card:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs create-card --board <board-id> --list <list-id> --name "Card title" [--description "Details"] [--due "2026-04-01"]
```

**Update a card:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs update-card --id <card-id> [--name "New name"] [--description "New desc"] [--done] [--due "2026-04-01"] [--starred]
```

**Mark a card done:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs done --id <card-id>
```

**Move a card to another list:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs move-card --id <card-id> --list <target-list-id>
```

### Board & List Operations

**Create a new board (with default lists: Backlog, In Progress, Done):**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs create-board --name "Board Name"
```

**Create a board with custom lists:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs create-board --name "Board Name" --lists "Todo,Doing,Review,Done"
```

**Add a list to a board:**
```bash
node ${CLAUDE_SKILL_DIR}/scripts/kanban.mjs create-list --board <board-id> --name "List Name"
```

## Output Format

All commands output JSON. Parse the output and present results in a human-readable format:
- For `boards`: show a table of board names and IDs
- For `board <id>`: show each list as a column header, with cards as bullet points underneath (include done status, due dates, starred)
- For mutations: confirm the action with the created/updated entity details

## Error Handling

If the output contains `{ "error": "..." }`, report the error message to the user. Common errors:
- `"Board not found"` → verify the board ID
- `"Card not found"` → verify the card ID

## Workflow Tips

When the user asks to "track tasks" or "manage my board":
1. Run `sync` to pull latest state
2. Run `boards` to show available boards
3. Then `board <id>` to show the selected board's state
4. Create/update/move cards as requested
5. After mutations, re-fetch the board to show updated state
6. Run `sync` to push changes for other machines
