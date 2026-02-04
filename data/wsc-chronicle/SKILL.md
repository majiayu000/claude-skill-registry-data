---
name: wsc-chronicle
description: Emit and query WSC chronicle events. Use when recording world events, checking event history, tracing causality chains, or finding events by type, location, or participants.
allowed-tools: Read, Write, Bash, Glob
---

# WSC Chronicle Management

The chronicle is an append-only event log that records everything that happens in the world. Events are stored in NDJSON format (one JSON object per line).

## Event Structure

```json
{
  "id": "evt_10001",
  "t_world": 1042,
  "t_scale": "galactic",
  "t_local": 8.0,
  "t_parent": null,
  "t_depth": 0,
  "t_stream": "02:14:33",
  "type": "battle.resolved",
  "where": "region.vega",
  "who": ["force.7th_fleet", "force.raiders"],
  "data": { /* event-specific payload */ },
  "causes": ["evt_10000"],
  "source": "lens.galactic",
  "confidence": 0.95,
  "importance": 0.8,
  "narrative_summary": "Human-readable description..."
}
```

## Hierarchical Time System

Events use hierarchical time to support recursive drill-downs across simulation scales:

| Field | Description |
|-------|-------------|
| `t_world` | Parent tick at the top simulation level (integer) |
| `t_scale` | Which simulation scale generated this event: `galactic`, `continental`, `city`, `scene`, `action` |
| `t_local` | Local time within the current scale's context (optional) |
| `t_parent` | Event ID that triggered this drill-down (for sub-scale events) |
| `t_depth` | Nesting depth: 0 = top level, 1 = first drill-down, 2 = drill-down within drill-down, etc. |

### Example Flow

1. **Galactic tick 1000**: galactic-4x creates opportunity `evt_10500`
2. **Scene drill-down**: party-rpg resolves scene, emits `evt_10501`:
   ```json
   { "t_world": 1000, "t_scale": "scene", "t_local": 15.5, "t_parent": "evt_10500", "t_depth": 1 }
   ```
3. **Action drill-down**: action-sim resolves combat within scene, emits `evt_10502`:
   ```json
   { "t_world": 1000, "t_scale": "action", "t_local": 47.2, "t_parent": "evt_10501", "t_depth": 2 }
   ```

## Event Types

| Family | Types | Description |
|--------|-------|-------------|
| **Governance** | `treaty.signed`, `control.changed`, `election.held` | Political events |
| **Economy** | `shortage.started`, `route.established`, `trade.completed` | Economic events |
| **Conflict** | `conflict.started`, `battle.resolved`, `asset.captured` | Military events |
| **Discovery** | `anomaly.discovered`, `artifact.recovered` | Exploration events |
| **Character** | `agent.promoted`, `agent.killed`, `agent.defected` | Character events |
| **Settlement** | `infrastructure.completed`, `unrest.spike` | City/locale events |
| **Scene** | `dialogue.occurred`, `skill_check.attempted`, `secret.revealed` | RPG events |
| **Opportunity** | `opportunity.created`, `opportunity.resolved` | Drill-down hooks |

## Commands

### Emit an Event

```bash
# Top-level galactic event
npx tsx .claude/skills/wsc-chronicle/scripts/emit.ts \
  --type battle.resolved \
  --where region.vega \
  --who force.7th_fleet,force.raiders \
  --data '{"outcome": "raider_victory"}' \
  --scale galactic \
  --importance 0.8 \
  --summary "Raiders ambushed the 7th Fleet..."

# Scene drill-down event
npx tsx .claude/skills/wsc-chronicle/scripts/emit.ts \
  --type dialogue.occurred \
  --where locale.port_nexus \
  --who agent.reva,agent.zara \
  --scale scene \
  --parent evt_10500 \
  --t-local 15.5 \
  --depth 1 \
  --importance 0.5

# Action drill-down within scene
npx tsx .claude/skills/wsc-chronicle/scripts/emit.ts \
  --type combat.round \
  --where locale.port_nexus \
  --who agent.reva,agent.assassin \
  --scale action \
  --parent evt_10501 \
  --t-local 47.2 \
  --depth 2 \
  --importance 0.6
```

### Query Events

```bash
# Recent events
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --last 10

# By type
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --type battle.resolved

# By location
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --where region.vega

# By participant
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --who agent.captain_reva

# By importance threshold
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --min-importance 0.7

# Time range
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --after 1040 --before 1050
```

### Query by Scale

```bash
# Only top-level galactic events
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --scale galactic

# Only scene-level events
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --scale scene

# Events drilled down from a specific event
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --parent evt_10500

# Only top-level events (depth 0)
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --depth 0

# Show event tree (event and all descendants)
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --tree evt_10500
```

### Trace Causality

```bash
# Find what caused an event
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --causes-of evt_10492

# Find what an event caused
npx tsx .claude/skills/wsc-chronicle/scripts/query.ts --caused-by evt_10311
```

## Importance Scores

Events carry an `importance` score (0-1) used for artifact generation:

| Score | Meaning | Examples |
|-------|---------|----------|
| 0.9+ | Major turning point | War declared, leader killed |
| 0.7-0.9 | Significant | Battle won, alliance formed |
| 0.5-0.7 | Notable | Skirmish, trade deal |
| 0.3-0.5 | Minor | Patrol, routine event |
| <0.3 | Background | Ambient events |

## File Location

- **Chronicle**: `src/worlds/{active_world}/chronicle.ndjson`
- **Example events**: `src/examples/events/`
