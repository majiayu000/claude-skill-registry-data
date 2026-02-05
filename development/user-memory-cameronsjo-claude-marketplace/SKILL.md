---
name: User Memory
description: Long-term user profile memory that persists across Claude Code sessions
when_to_use: Automatic - runs via hooks, no manual invocation needed
version: 4.0.0
---

# User Memory

Persistent user profile memory for Claude Code. Two implementations - pick your flavor:

| Mode | Deps | Features | Best for |
|------|------|----------|----------|
| **minimal/** | jq only | Hook extraction | Lightweight, portable |
| **mcp/** | Node + MCP SDK | Hooks + real-time tools | Full control |

## Quick Start

### Option A: Minimal (Shell-only)

```bash
# Add to ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/minimal/session-start.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/minimal/stop-memory.sh"
      }]
    }]
  }
}
```

Done. No npm install needed.

### Option B: MCP Server (Full)

```bash
cd ~/.claude/skills/user-memory/mcp
npm install
```

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/mcp/src/hooks/session-start.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/mcp/src/hooks/stop-memory.sh"
      }]
    }]
  },
  "mcpServers": {
    "user-memory": {
      "command": "npx",
      "args": ["tsx", "~/.claude/skills/user-memory/mcp/src/mcp-server.ts"]
    }
  }
}
```

---

## How It Works

```
SessionStart hook
    ↓
    Loads ~/.claude/user-memory/profile.json
    ↓
    Injects into session context

Stop hook (after every Claude response)
    ↓
    Reads conversation transcript
    ↓
    Extracts preferences via pattern matching
    ↓
    Deduplicates (skips already-processed turns)
    ↓
    Merges into profile.json

[MCP only] Claude can also call:
    Profile tools:
    - get_user_profile
    - update_user_profile
    - remove_preference
    - clear_user_profile
    - get_changelog
    - get_preference_metadata
    - run_decay

    Session continuity tools:
    - get_session_context
    - update_task
    - log_decision
    - add_session_context
    - set_session_summary
    - get_full_context
```

## What Gets Stored

| Category | Trigger phrases |
|----------|-----------------|
| Tech stack | "I prefer Bun", "I'm switching to FastAPI" |
| Editor | "I use neovim", "My editor is VS Code" |
| Tone | "Be more direct", "I prefer concise" |
| Role | "I'm a backend engineer" |
| Languages | "I work mostly in TypeScript" |

## Storage

```
~/.claude/user-memory/
├── profile.json         # Your preferences
├── profile-meta.json    # Confidence/decay tracking (MCP only)
├── changelog.jsonl      # Audit trail (auto-pruned)
├── .processed_turns     # Dedup tracker
└── sessions/            # Session continuity (MCP only)
    ├── session-abc123.json
    └── ...
```

Override location: `USER_MEMORY_DIR=/custom/path`

## Changelog (Audit Trail)

Every profile change is logged to `changelog.jsonl`:

```jsonl
{"timestamp":"2025-01-15T10:30:00Z","session_id":"abc123","action":"extract","source":"minimal/hook","changes":{"codePreferences":{"preferredStacks":["Bun"]}}}
{"timestamp":"2025-01-15T11:00:00Z","action":"update","source":"mcp/tool","changes":{"tools":{"editor":"neovim"}}}
{"timestamp":"2025-01-16T09:00:00Z","action":"clear","source":"mcp/tool","changes":{"userId":"default"}}
```

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 when change occurred |
| `session_id` | Session that triggered the change (hooks only) |
| `action` | `extract`, `update`, `clear`, `remove`, `decay` |
| `source` | `minimal/hook`, `mcp/hook`, `mcp/tool`, `system` |
| `changes` | What was added/modified |
| `removed` | Paths that were removed (for remove/decay actions) |

**MCP only:** Use `get_changelog` tool to query the log.

**Auto-pruning:** Changelog keeps last 1000 entries and removes entries older than 90 days.

## Session Continuity (MCP only)

Track task progress and decisions across sessions. Resume where you left off.

### Storage

```
~/.claude/user-memory/sessions/
├── session-abc123.json    # Session with tasks, decisions, context
├── session-def456.json
└── ...
```

### Tools

| Tool | Purpose |
|------|---------|
| `get_session_context` | Get resume context from previous sessions |
| `update_task` | Track task progress (pending/in_progress/blocked/completed) |
| `log_decision` | Record important decisions with rationale |
| `add_session_context` | Store context notes for future sessions |
| `set_session_summary` | Set summary shown at next session start |
| `get_full_context` | Get full context prompt (profile + session resume) |

### Auto-pruning

Sessions older than 30 days are automatically removed.

## Negation Handling

The extraction system understands when you want to **remove** preferences:

| Phrase | Effect |
|--------|--------|
| "I no longer use Webpack" | Removes Webpack from stacks |
| "I stopped using React" | Removes React from stacks |
| "Forget that I prefer tabs" | Removes that preference |
| "I switched away from npm" | Removes npm from tools |

Negation patterns have higher priority than positive patterns, so "I prefer Bun over npm" will add Bun and remove npm atomically.

## Decay & Confidence (MCP only)

Preferences decay over time if not reinforced. This prevents stale preferences from persisting forever.

### How it works

1. Each preference has a **confidence score** (0.0 - 1.0)
2. Confidence decays exponentially: `confidence * 0.5^(days / 30)`
3. When confidence drops below 0.1, preference is auto-removed
4. Mentioning a preference again **reinforces** it (+0.3 confidence)

### Example timeline

| Day | Event | Confidence |
|-----|-------|------------|
| 0 | "I prefer Bun" | 1.00 |
| 30 | No mention (decay) | 0.50 |
| 60 | No mention (decay) | 0.25 |
| 75 | "I'm using Bun" (reinforce) | 0.55 |
| 90 | No mention (decay) | 0.39 |

### MCP tools for decay

| Tool | Purpose |
|------|---------|
| `get_preference_metadata` | View confidence scores, days until decay |
| `run_decay` | Manually trigger decay cycle |
| `remove_preference` | Explicitly remove preferences |

### Auto-decay on SessionStart

When using MCP mode, decay is automatically checked at session start:
- Only runs if 24+ hours since last decay
- Removes preferences below confidence threshold
- Prunes old changelog entries
- Zero latency impact (runs async)

## Profile Schema

```typescript
interface UserProfile {
  userId: string;
  schemaVersion: 1;
  lastUpdated: string;

  bio?: string;
  work?: {
    role?: string;
    focusAreas?: string[];
    languages?: string[];
  };
  codePreferences?: {
    tone?: "direct" | "neutral" | "friendly";
    detailLevel?: "high" | "medium" | "low";
    avoidExamples?: string[];
    preferredStacks?: string[];
  };
  tools?: {
    editor?: string;
    infra?: string[];
  };
  interests?: string[];
  custom?: Record<string, unknown>;
}
```

## Swizzling

Switch modes anytime - both use the same `profile.json`:

```bash
# Switch from minimal → mcp
# Just update hooks paths in settings.json and add mcpServers

# Switch from mcp → minimal
# Remove mcpServers, update hook paths
```

## Architecture Notes

**Why Stop hook instead of SessionEnd?**
SessionEnd doesn't fire on Ctrl+C, terminal close, or crashes. Stop hook runs after every response - bulletproof.

**Why heuristic extraction?**
- Zero latency
- No API cost
- Deterministic
- MCP tools available for edge cases (mcp/ only)

**Minimal vs MCP trade-offs:**

| | Minimal | MCP |
|-|---------|-----|
| Dependencies | jq | Node, tsx, MCP SDK |
| Real-time updates | No | Yes (tool calls) |
| Cross-tool access | No | Yes |
| Pattern coverage | Basic | Extended |
| Portability | High | Medium |

## Directory Structure

```
skills/user-memory/
├── SKILL.md
├── minimal/              # Zero-dep shell scripts
│   ├── session-start.sh
│   └── stop-memory.sh
└── mcp/                  # Full TypeScript MCP
    ├── package.json
    ├── tsconfig.json
    └── src/
        ├── types.ts          # Type definitions
        ├── store.ts          # Profile storage + decay
        ├── context.ts        # Context injection builder
        ├── session.ts        # Session continuity
        ├── prompt.ts         # System prompt builder
        ├── extract-memory.ts # Pattern extraction
        ├── decay-check.ts    # Auto-decay on session start
        ├── mcp-server.ts     # MCP server (13 tools)
        └── hooks/
            ├── session-start.sh
            └── stop-memory.sh
```
