---
name: wsc-world-state
description: Initialize and manage WSC world state. Use when creating a new world, loading world state, advancing simulation ticks, or checking world status.
allowed-tools: Read, Write, Bash, Glob
---

# WSC World State Management

Manage world instances including creation, switching, tick advancement, and status checking.

## Architecture

WSC separates **scenarios** (templates) from **worlds** (runtime instances):

```
src/
├── scenarios/              # Scenario TEMPLATES (read-only)
│   ├── scenarios.json      # Available scenarios
│   ├── vega_conflict/      # Sci-fi scenario
│   │   ├── scenario.json
│   │   ├── entities/
│   │   ├── locations/
│   │   └── rules/
│   └── shattered_realms/   # Fantasy scenario
│       └── ...
└── worlds/                 # RUNTIME instances (mutable)
    ├── worlds.json         # Registry of world instances
    ├── vega_conflict_001/  # First Vega playthrough
    │   ├── state.json
    │   ├── chronicle.ndjson
    │   ├── entities/
    │   └── locations/
    └── shattered_realms_001/
        └── ...
```

## Commands

### Create New World

```bash
# Create from default scenario
npx tsx .claude/skills/wsc-world-state/scripts/init.ts

# Create from specific scenario
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --scenario shattered_realms

# Create with custom name
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --scenario vega_conflict --name "My Campaign"

# Create with specific ID
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --scenario vega_conflict --id my_vega_game

# Create empty world
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --empty
```

### List Available

```bash
# List scenarios (templates)
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --list

# List world instances (saves)
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --list-worlds
```

### Switch Worlds

```bash
# Switch to a different world instance
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --switch vega_conflict_002
```

### Delete World

```bash
# Delete a world instance
npx tsx .claude/skills/wsc-world-state/scripts/init.ts --delete vega_conflict_001
```

### Check World Status

```bash
npx tsx .claude/skills/wsc-world-state/scripts/status.ts
```

Shows:
- Active world ID
- Current tick
- Entity counts by type
- Recent events
- World settings

### Advance Tick

```bash
# Advance by 1 tick
npx tsx .claude/skills/wsc-world-state/scripts/tick.ts

# Advance by N ticks
npx tsx .claude/skills/wsc-world-state/scripts/tick.ts --count 5

# Advance to specific tick
npx tsx .claude/skills/wsc-world-state/scripts/tick.ts --to 1050
```

## World Instance Structure

Each world instance contains:

```
worlds/{world_id}/
├── state.json          # World metadata (tick, settings)
├── chronicle.ndjson    # Append-only event log
├── entities/           # Current entity states
│   ├── polity.*.json
│   ├── agent.*.json
│   └── ...
└── locations/          # Location map files
    ├── world.*.json
    ├── region.*.json
    └── locale.*.json
```

## State File Format

```json
{
  "tick": 1000,
  "last_event_id": 10500,
  "active_scenario": "vega_conflict",
  "drill_down_opportunities": [],
  "active_conflicts": [],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T12:30:00Z",
  "settings": {
    "name": "The Vega Conflict",
    "genre": "sci-fi"
  }
}
```

## Worlds Registry Format

The `worlds/worlds.json` file tracks all instances:

```json
{
  "active_world": "vega_conflict_001",
  "worlds": {
    "vega_conflict_001": {
      "scenario": "vega_conflict",
      "name": "The Vega Conflict",
      "created_at": "2024-01-15T10:00:00Z",
      "last_played": "2024-01-15T12:30:00Z"
    },
    "shattered_realms_001": {
      "scenario": "shattered_realms",
      "name": "The Shattered Realms",
      "created_at": "2024-01-16T08:00:00Z",
      "last_played": "2024-01-16T09:00:00Z"
    }
  }
}
```

## Tick Semantics

The `tick` value represents world time. Its meaning depends on the genre:

| Genre | Tick Unit | Example |
|-------|-----------|---------|
| Galactic | Days | tick 1000 = Day 1000 |
| Continental | Seasons | tick 100 = 25th year |
| City | Weeks | tick 52 = 1 year |
| Scene | Minutes | tick 60 = 1 hour |

## Integration with Agents

Agents read world state to understand context and emit events that modify it:

1. Orchestrator reads `state.json` to get current tick and active world
2. Orchestrator queries entities relevant to current lens
3. Agent simulates and emits events
4. Events are applied via `wsc-effects` skill
5. Tick advances

## File Locations

All paths automatically resolve to the active world:

- **Active world**: `src/worlds/{active_world}/`
- **World state**: `src/worlds/{active_world}/state.json`
- **Entities**: `src/worlds/{active_world}/entities/`
- **Locations**: `src/worlds/{active_world}/locations/`
- **Chronicle**: `src/worlds/{active_world}/chronicle.ndjson`
- **Scenarios**: `src/scenarios/`
