---
name: implement-content-data
description: "Use when generating ECS entity archetype definitions, component factory functions, and default value tables from game design specs. Triggers: 'implement content data', 'generate entity factories', 'content data structures', 'entity archetypes', 'game content wiring'."
---

# Implement Content Data

## 1. Overview

Generate per-domain content data files: entity archetype definitions, factory functions, and default value tables — one file per content domain (enemies, weapons, items, etc.). Engine-agnostic: reads platform from `rendering_target.md`.

## 2. Core Pattern

### 2.1. Read Configuration (MANDATORY)

1. Read `.game-dev-config.json` → extract `target_folder`, `specs_dir`
2. Read `{TARGET_FOLDER}/docs/rendering_target.md` → extract Platform, Engine, Language
3. If Engine ∉ {"Phaser 3", "Three.js"} → STOP, report unsupported
4. If Language ≠ "TypeScript" → STOP, report unsupported

### 2.2. Extract Content Domains

Read these specs in order:

| Spec File | Extract |
|---|---|
| `raw_rules.md` | Entity types mentioned (enemies, weapons, items, characters, collectibles, obstacles, projectiles) |
| `game_loop.md` | What entities participate in micro/macro loops |
| `ecs_spec.md` | Component definitions, archetype patterns, World API |
| `events_spec.md` | Events that spawn/destroy/modify entities |
| `system_roster.md` | Systems that process entity types |
| `visual_style.md` | Sprite dimensions, palette for visual defaults |

Build a **Content Domain Map**: each domain = { name, entity variants, required components, relevant events }.

### 2.3. Read Existing ECS Implementation

Read `{TARGET_FOLDER}/src/ecs/` to extract:
- Component class/interface names and field signatures
- World.createEntity() API shape
- Entity type alias
- Existing archetype patterns (if any)

Import paths MUST be derived from reading the actual ECS implementation.

### 2.4. Generate Per-Domain Files

For EACH content domain, create `{TARGET_FOLDER}/src/content/{domain}.ts`:

**Structure per file:**
1. **Imports** — Component types from `../ecs/`, Entity/World types
2. **Config interface** — `{Domain}Config` with required spawn parameters
3. **Default value table** — `const {DOMAIN}_DEFAULTS: Record<string, {Domain}Config>` mapping variant names to default configs
4. **Factory function** — `create{Domain}(world: World, config: {Domain}Config): Entity` that creates entity + adds components

**Engine-specific branching:**
- Phaser 3: asset keys use string identifiers (sprite sheet keys)
- Three.js: asset refs use file paths (model/texture URLs)
- Unsupported: generate `// TODO: Implement for {Engine}` placeholder

### 2.5. Domain-Specific Guidance

| Domain | Variants (from specs) | Key Components | Special Logic |
|---|---|---|---|
| Enemies | Read from raw_rules.md enemy definitions | Transform, Health, AI, Sprite, Collider | Difficulty scaling in defaults |
| Weapons | Read from raw_rules.md weapon/attack rules | Damage, Cooldown, Sprite, ProjectileEmitter | Range/type categories |
| Items | Read from raw_rules.md item/pickup rules | Transform, Sprite, Collider, Effect | Stack/unique flags |
| Characters | Read from raw_rules.md player/NPC definitions | Transform, Health, Sprite, Input/AI, Inventory | Player vs NPC config split |
| Levels | Read from raw_rules.md level/stage structure | TileMap, Bounds, SpawnPoints, Background | Wave/progression data |

Only generate domains that exist in the specs. Skip domains with no spec references.

### 2.6. Generate Barrel Export

Create `{TARGET_FOLDER}/src/content/index.ts` — re-export all domain files.

## 3. Output File Structure

```
{TARGET_FOLDER}/src/content/
├── enemies.ts          # Enemy archetypes + factories + defaults
├── weapons.ts          # Weapon archetypes + factories + defaults
├── items.ts            # Item archetypes + factories + defaults
├── characters.ts       # Character archetypes + factories + defaults
├── levels.ts           # Level data + spawn point definitions
└── index.ts            # Barrel export
```

Only files for domains found in specs. No empty placeholder files.

## 4. Validation Checklist

- [ ] `.game-dev-config.json` read for target_folder/specs_dir
- [ ] All entity types from `raw_rules.md` have corresponding domain file
- [ ] Each factory accepts `world: World` and typed config, returns Entity
- [ ] Component imports resolve to actual `src/ecs/` implementation paths
- [ ] Default value table covers all variants mentioned in specs
- [ ] All numeric values sourced from defaults table (zero hardcoded constants)
- [ ] Engine-specific asset references match rendering_target.md
- [ ] `index.ts` barrel re-exports all domain modules
- [ ] `npx tsc --noEmit` passes with no errors
- [ ] No game logic in factories — pure entity assembly only
- [ ] No circular imports between content/ and ecs/

## 5. Red Flags

| Signal | Action |
|---|---|
| `raw_rules.md` missing or lists no entities | STOP — cannot determine content domains |
| `ecs_spec.md` missing or no components defined | STOP — cannot map entities to components |
| Factory contains game logic (AI behavior, physics) | HALT — factories are pure assembly, move logic to systems |
| Component types mismatch `src/ecs/` implementation | HALT — re-read actual component signatures |
| Inventing components not in ecs_spec.md | HALT — only use defined components |
| Hardcoding engine-specific code without checking rendering_target.md | HALT — always branch on Engine |

## 6. Interaction Protocol

| Mistake | Correction |
|---|---|
| Pasting full code templates in the skill | Describe WHAT to generate, not HOW in code |
| Generating domains not in specs | Only create files for domains found in raw_rules.md |
| Importing components by guessed names | Read actual `src/ecs/` files for real import paths |
| Flat single-file output for all content | One file per domain for maintainability |
| Skipping default value tables | Every domain MUST have a defaults table with spec-derived values |
