---
name: crew-config
description: Manages CodeCrew configuration. Allows users to customize default mode, model tiers, agent activation, token budgets, and auto-index settings without editing JSON files.
---

# Crew Config - User Configuration Manager

Reads and writes `.claude/crew-config.json` to customize CodeCrew behavior.

## When to Activate

- User runs `/crew config show|set|reset`
- Other skills check for config overrides at startup

## Config File

**Location**: `.claude/crew-config.json` (created on first `set` command)

**Default values** (used when file doesn't exist):
```json
{
  "defaultMode": "full",
  "modelOverrides": {},
  "agentOverrides": {},
  "tokenBudgets": {
    "opus": 3000,
    "sonnet": 2000,
    "sonnet-planner": 2500,
    "haiku": 800
  },
  "autoIndex": true,
  "historyLimit": 50
}
```

## Subcommands

### `show` — Display Current Configuration

1. Read `.claude/crew-config.json` (if exists, otherwise show defaults)
2. Display:

```
Config: Mode={full|lite} | Auto-Index={on|off} | History={count}
Budgets: Opus {t}tk/{s}sk | Sonnet {t}tk/{s}sk | Sonnet-planner {t}tk/{s}sk | Haiku {t}tk/{s}sk
Model overrides: {none | list}
Agent overrides: {none | list}
```

### `set <key> <value>` — Update a Setting

Supported keys:

| Key | Values | Example |
|-----|--------|---------|
| `mode` | `full`, `lite` | `/crew config set mode lite` |
| `auto-index` | `true`, `false` | `/crew config set auto-index false` |
| `history-limit` | number | `/crew config set history-limit 100` |
| `agent.<name>.model` | `opus`, `sonnet`, `haiku` | `/crew config set agent.senior-dev.model opus` |
| `agent.<name>.active` | `true`, `false` | `/crew config set agent.security-analyst.active true` |
| `budget.<tier>` | number (tokens) | `/crew config set budget.sonnet 2500` |

Process:
1. Read existing `.claude/crew-config.json` (or start with defaults)
2. Validate the key and value
3. Apply the change
4. Write back to `.claude/crew-config.json`
5. Confirm: `"Set {key} = {value}"`

**Validation rules:**
- `mode`: must be `full` or `lite`
- `agent.<name>.model`: agent must exist in crew-team.json
- `budget.<tier>`: must be a positive number, max 5000
- Warn if user sets a Haiku agent to Opus (expensive, possible but discouraged)

### `reset` — Restore Defaults

1. Delete `.claude/crew-config.json`
2. Confirm: `"Configuration reset to defaults"`

## Integration with Other Skills

Other skills should check for config overrides at startup:

```
1. Check if .claude/crew-config.json exists
2. If yes, read it and apply overrides:
   - task-router / lite-router: check defaultMode to decide which router to use
   - skill-injector: check tokenBudgets for custom limits
   - execution-orchestrator: check autoIndex, modelOverrides
3. If no, use built-in defaults
```

This check adds ~50 tokens per skill invocation but enables full user customization.
