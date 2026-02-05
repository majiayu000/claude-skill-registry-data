---
name: mem-persist
description: Saves Claude Code or Codex CLI conversation threads to Nowledge Mem knowledge base via HTTP API. Use when user requests to save, persist, or backup the current session or conversation thread.
---

# Save Conversation to Nowledge Mem

Persists the current conversation thread to a remote Nowledge Mem server.

## Usage

**IMPORTANT**: Always set `PROJECT_PATH` to the actual project directory (from `<env>` block's working directory), not the skill's directory.

```bash
# Save current session
PROJECT_PATH=/path/to/project uv run python -m mem_persist save

# With custom title
PROJECT_PATH=/path/to/project uv run python -m mem_persist save --title "Feature X implementation"

# Force specific source (skip auto-detect)
PROJECT_PATH=/path/to/project uv run python -m mem_persist save --source codex
```

## Troubleshooting

```bash
PROJECT_PATH=/path/to/project uv run python -m mem_persist diagnose
```

## Configuration

Environment variables (optional):
- `MEM_API_URL` - API endpoint (default: `http://localhost:14243`)
- `MEM_AUTH_TOKEN` - Bearer token (default: `helloworld`)
- `MEM_SESSION_SOURCE` - `auto`/`claude`/`codex` (default: `auto`)

For detailed configuration and `.env` file setup, see [README.md](./README.md).
