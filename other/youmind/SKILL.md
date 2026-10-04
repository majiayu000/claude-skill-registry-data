---
name: youmind
description: Use this skill to operate Youmind via HTTP APIs. Browser is only used for login bootstrap/refresh, while board/material/chat operations are API-only.
---

# Youmind API Skill

API-first Youmind operations for local AI agents.

## Core Rule

- Business operations are **API-only**.
- Browser automation is used **only** for authentication bootstrap/refresh.

## Authentication

```bash
python scripts/run.py auth_manager.py status
python scripts/run.py auth_manager.py validate
python scripts/run.py auth_manager.py setup
```

## Board APIs

```bash
# List boards
python scripts/run.py board_manager.py list

# Find boards by name/id keyword
python scripts/run.py board_manager.py find --query "roadmap"

# Get board detail
python scripts/run.py board_manager.py get --id <board-id>

# Create board
python scripts/run.py board_manager.py create --name "My Board"
python scripts/run.py board_manager.py create --name "My Board" --prompt "Initialize this board for AI coding agent research"
```

## Material APIs

```bash
# Add link to board
python scripts/run.py material_manager.py add-link --board-id <board-id> --url "https://example.com"

# Upload local file to board
python scripts/run.py material_manager.py upload-file --board-id <board-id> --file /path/to/file.pdf

# Get snips by IDs
python scripts/run.py material_manager.py get-snips --ids "<snip-id-1>,<snip-id-2>"

# List picks (if available)
python scripts/run.py material_manager.py list-picks --board-id <board-id>
```

## Chat APIs

```bash
# Create new chat with first message
python scripts/run.py chat_manager.py create --board-id <board-id> --message "Summarize key ideas"

# Send to existing chat
python scripts/run.py chat_manager.py send --board-id <board-id> --chat-id <chat-id> --message "Give next steps"

# Chat history/detail
python scripts/run.py chat_manager.py history --board-id <board-id>
python scripts/run.py chat_manager.py detail --chat-id <chat-id>
python scripts/run.py chat_manager.py detail-by-origin --board-id <board-id>

# Generation via chat
python scripts/run.py chat_manager.py generate-image --board-id <board-id> --prompt "Minimal blue AI poster"
python scripts/run.py chat_manager.py generate-slides --board-id <board-id> --prompt "6-page AI coding agent roadmap"
```

## Compatibility Wrapper

```bash
python scripts/run.py ask_question.py --board-id <board-id> --question "..."
python scripts/run.py ask_question.py --board-id <board-id> --chat-id <chat-id> --question "..."
```

## Data

Local auth state:

```text
data/
├── auth_info.json
└── browser_state/
    └── state.json
```

Do not commit `data/`.
