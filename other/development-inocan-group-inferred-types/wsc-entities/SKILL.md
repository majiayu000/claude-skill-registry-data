---
name: wsc-entities
description: Create, validate, and query WSC world entities (polities, agents, regions, forces, locales, holdings). Use when working with entity JSON files, checking entity consistency, or finding entities by type, tag, or relationship.
allowed-tools: Read, Write, Bash, Glob
---

# WSC Entity Management

Manage entities in the World State Chronicler. Entities are JSON files representing game world objects like factions, characters, locations, and assets.

## Entity Types

| Type | Description | ID Format |
|------|-------------|-----------|
| `polity` | Faction, nation, guild | `polity.slug` |
| `region` | Star system, province | `region.slug` |
| `presence` | Polity-region relationship | `presence.polity.region` |
| `force` | Fleet, army, warband | `force.slug` |
| `locale` | Station, city, dungeon | `locale.slug` |
| `feature` | Planet, terrain, anomaly | `feature.slug` |
| `link` | Route, jump lane, portal | `link.a.b` |
| `site` | District, zone within locale | `site.locale.slug` |
| `agent` | Character, hero, leader | `agent.slug` |
| `holding` | Asset, artifact, ship | `holding.slug` |

## Commands

### Validate an Entity

```bash
npx tsx .claude/skills/wsc-entities/scripts/validate.ts <entity-file-or-id>
```

Validates entity JSON against the schema. Reports errors and warnings.

### Query Entities

```bash
# By type
npx tsx .claude/skills/wsc-entities/scripts/query.ts --type agent

# By tag
npx tsx .claude/skills/wsc-entities/scripts/query.ts --tag veteran

# By affiliation/belongs-to
npx tsx .claude/skills/wsc-entities/scripts/query.ts --belongs-to polity.hegemony

# By location
npx tsx .claude/skills/wsc-entities/scripts/query.ts --location region.vega

# Combined filters
npx tsx .claude/skills/wsc-entities/scripts/query.ts --type force --belongs-to polity.free_traders
```

### Create Entity Template

```bash
npx tsx .claude/skills/wsc-entities/scripts/create.ts <type> <slug> [--name "Display Name"]
```

Creates a new entity JSON file from template.

### List All Entities

```bash
npx tsx .claude/skills/wsc-entities/scripts/query.ts --list
```

## Entity Structure

All entities share this base structure:

```json
{
  "id": "type.slug",
  "type": "entity_type",
  "name": "Display Name",
  "tags": ["tag1", "tag2"],
  "attrs": { /* type-specific */ },
  "ai": { /* optional LLM integration */ }
}
```

### AI Block (for characters and factions)

```json
{
  "ai": {
    "persona": "Character identity description",
    "voice": {
      "tone": "weary | formal | aggressive",
      "vocabulary": ["preferred", "terms"],
      "speech_patterns": "Quirks and patterns"
    },
    "goals": ["objective_1", "objective_2"],
    "memory": ["evt_id_1", "evt_id_2"],
    "secrets": ["hidden fact 1"],
    "emotional_state": {
      "mood": "guarded",
      "stress": 0.6
    },
    "skills": {
      "combat": 0.8,
      "negotiation": 0.6
    }
  }
}
```

## File Locations

- **Live world**: `src/world/entities/`
- **Examples**: `src/examples/entities/`

## Examples

See [examples documentation](../../../src/examples/README.md) for complete entity examples.
