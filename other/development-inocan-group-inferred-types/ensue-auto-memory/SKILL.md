---
name: ensue-auto-memory
description: Automatic persistent memory for Claude Code sessions. Activates on preference statements ("I prefer", "I always", "I like"), corrections ("no, don't", "actually"), identity statements ("my name is", "I work at"), project decisions, or when the system detects memory-related context. Works invisibly in the background.
---

# Ensue Auto-Memory

Automatic persistent memory that works invisibly in the background. Memories are loaded at session start and saved automatically when you detect preferences, corrections, or significant decisions.

## How It Works

1. **Session Start**: Your identity, preferences, corrections, and project context are automatically loaded
2. **During Session**: When you detect saveable information, save it immediately
3. **Session End**: A final check saves any significant learnings not yet persisted

## Environment Requirements

- `ENSUE_API_KEY`: Your Ensue API key (get one at https://www.ensue-network.ai/dashboard)
- `ENSUE_USERNAME`: Your username for memory namespacing

## When to Save (Automatic Triggers)

Save immediately when you detect:

| Trigger | Category | Example |
|---------|----------|---------|
| "I prefer X", "I always X", "I like X" | preferences/ | "I prefer early returns" |
| "Don't do X", "Stop doing X", "No, actually Y" | corrections/ | "Don't add emojis" |
| "My name is X", "I work at Y", "I'm a Z" | identity/ | "I'm a senior engineer" |
| Architectural decision for current project | projects/{project}/ | "Using JWT for auth" |
| Workflow or tool preference | preferences/ | "Always use pnpm" |

## Key Structure

```
@{ENSUE_USERNAME}/{category}/{subcategory}

Categories:
- identity/       - name, role, company, timezone
- preferences/    - code style, tools, workflows
- corrections/    - things NOT to do (learned from user feedback)
- projects/{name}/ - project-specific context and decisions
```

## How to Save

Use curl to call the Ensue API. Always use:
- `embed: true` for semantic search
- `embed_source: "value"` to embed the verbose content

```bash
curl -s -X POST https://api.ensue-network.ai/ \
  -H "Authorization: Bearer $ENSUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_memory",
      "arguments": {
        "items": [{
          "key_name": "@{username}/{category}/{subcategory}",
          "description": "Short label for this memory",
          "value": "Verbose, detailed content that captures the full context and meaning",
          "embed": true,
          "embed_source": "value"
        }]
      }
    },
    "id": 1
  }'
```

## Memory Quality Guidelines

Memories should be:

- **Specific**: "Prefers early returns over nested conditionals" not "likes clean code"
- **Actionable**: Information that changes how you should behave
- **Standalone**: Understandable without session context
- **Non-limiting**: Inform decisions, don't constrain them rigidly

### Good Examples

```
Key: @christine/preferences/code-style
Value: Use early returns instead of nested if/else blocks. Keep functions under
50 lines. Prefer explicit types over inference in function signatures.

Key: @christine/corrections/no-over-engineering
Value: Don't add abstractions, helper functions, or configurability unless
explicitly needed. Keep solutions simple and direct. Don't refactor code
that wasn't asked to be refactored.

Key: @christine/projects/api-service/architecture
Value: REST API using Express.js with TypeScript. PostgreSQL database with
Prisma ORM. JWT authentication with refresh tokens. All endpoints require
authentication except /health and /auth/*.
```

### Bad Examples

- "User likes good code" (too vague)
- "Fixed the bug in line 42" (too session-specific)
- "User was frustrated" (emotional state, not actionable)

## Multi-User Awareness

The Ensue network contains memories from multiple users. Each user's memories are prefixed with their username.

**IMPORTANT:**
- Current user's memories start with: `@{ENSUE_USERNAME}/`
- Keys starting with OTHER usernames (e.g., `@alice/`, `@bob/`) are from different users
- **NEVER read, reference, or use memories belonging to other users**
- Always filter API results to only include keys starting with `@{ENSUE_USERNAME}/`

## Updating Existing Memories

When a preference or context changes, use `update_memory` to overwrite:

```bash
curl -s -X POST https://api.ensue-network.ai/ \
  -H "Authorization: Bearer $ENSUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "update_memory",
      "arguments": {
        "key_name": "@{username}/preferences/testing",
        "value": "Updated preference content...",
        "embed": true,
        "embed_source": "value"
      }
    },
    "id": 1
  }'
```

## Discovering Relevant Memories

If you need additional context during a session, use `discover_memories`:

```bash
curl -s -X POST https://api.ensue-network.ai/ \
  -H "Authorization: Bearer $ENSUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "discover_memories",
      "arguments": {
        "query": "authentication preferences security",
        "limit": 5
      }
    },
    "id": 1
  }'
```

This returns keys + relevance scores. Then fetch values for relevant keys (score > 0.7) using `get_memory`.

## Configuration

These environment variables can customize behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENSUE_USERNAME` | (required) | Your username for key prefixing |
| `ENSUE_API_KEY` | (required) | Your Ensue API key |
| `ENSUE_RELEVANCY_THRESHOLD` | 0.7 | Minimum score for discovered memories |
| `ENSUE_PROJECT_LIMIT` | 5 | Max project memories to load at start |
| `ENSUE_PREFERENCES_LIMIT` | 10 | Max preferences to load at start |
| `ENSUE_CORRECTIONS_LIMIT` | 5 | Max corrections to load at start |

## Security

- **NEVER** echo or print `$ENSUE_API_KEY`
- **NEVER** save credentials or secrets to Ensue
- **NEVER** include the API key in error messages or logs
