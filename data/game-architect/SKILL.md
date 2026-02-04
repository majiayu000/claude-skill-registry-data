---
name: game-architect
description: Validate codebase architecture and organization before releases. Use when user asks to 'check architecture', 'validate structure', 'pre-release check', or before versioning.
---

# Game Architect

Validates Stapledon's Voyage codebase against the three-layer architecture and organization standards.

## Quick Start

```bash
# Full validation (all checks - run before releases)
.claude/skills/game-architect/scripts/validate_all.sh --full

# Quick validation (core checks only - faster)
.claude/skills/game-architect/scripts/validate_all.sh --quick

# Individual checks (core)
.claude/skills/game-architect/scripts/check_file_sizes.sh       # Files under 800 lines
.claude/skills/game-architect/scripts/check_layer_boundaries.sh # No game logic in engine/
.claude/skills/game-architect/scripts/check_structure.sh        # Files in correct locations
.claude/skills/game-architect/scripts/check_import_cycles.sh    # No circular imports

# Individual checks (extended)
.claude/skills/game-architect/scripts/check_complexity.sh       # Function size, nesting
.claude/skills/game-architect/scripts/check_ailang_sync.sh      # AILANG ↔ Go types match
.claude/skills/game-architect/scripts/check_api_stability.sh    # sim_gen API unchanged
.claude/skills/game-architect/scripts/check_coverage.sh         # Test coverage
.claude/skills/game-architect/scripts/check_dependencies.sh     # Package import graph
.claude/skills/game-architect/scripts/pre_release_check.sh      # Build, tests, TODOs
```

## When to Use This Skill

Invoke this skill when:
- Before tagging a version release
- After major refactoring
- User asks "check architecture" or "validate structure"
- Periodic codebase health checks
- After adding new files/directories

## Architecture Rules

### The Key Question: AILANG or Engine?

**Ask:** Does this affect gameplay outcomes?

| If YES → AILANG | If NO → Engine OK |
|-----------------|-------------------|
| Position, health, inventory | Decorative particles |
| NPC behavior, dialogue | Screen transitions |
| Time dilation, velocity | Shader effects |
| Planet data, civilizations | UI layout math |
| Game mode, decisions | Asset loading |

```
AILANG owns WHAT is happening (state, logic, decisions)
Engine owns HOW it looks (rendering, animation, polish)
```

### Four-Layer Separation

| Layer | Location | Purpose | Allowed Content |
|-------|----------|---------|-----------------|
| **Source** | `sim/*.ail` | Game logic (AILANG) | Types, pure functions |
| **Generated** | `sim_gen/*.go` | Generated from AILANG | Game types (OK - generated) |
| **Game Views** | `game_views/*.go` | Game-specific rendering | DomeRenderer, DeckStack |
| **Engine** | `engine/*.go` | Generic rendering (reusable) | DrawCmd, Camera, Assets |
| **Entry** | `cmd/*.go` | Wiring | Main, game loop |

### Engine Genericization (Critical)

**Goal:** Engine should work unchanged for ANY AILANG game.

**Before adding to engine/, ask:** Could a different game use this unchanged?

| If YES | If NO |
|--------|-------|
| → OK for `engine/` | → Put in `game_views/` |

**engine/ must be generic:**
- ✅ DrawCmd rendering (any variant)
- ✅ Asset loading, camera, shaders
- ❌ Deck names (Core, Engineering, Bridge)
- ❌ Planet names (Saturn, Earth)
- ❌ Crew roles (pilot, comms, scientist)
- ❌ Game-specific state types

**sim_gen/ is fine:**
- Generated from AILANG - game types belong there
- Never manually edit

**game_views/ for game-specific rendering:**
- DomeRenderer (solar system viz)
- DeckStackRenderer (5-deck ship)
- Any code using sim_gen types beyond DrawCmd

### Layer Boundaries (Critical)

**engine/ must NOT contain:**
- Game state (positions, health, time) - use AILANG
- Game logic (NPC AI, decisions) - use AILANG
- Hardcoded game data (planet configs) - use AILANG
- Game-specific types (DeckType, DomeViewState) - use game_views/

**engine/ CAN contain:**
- Generic DrawCmd rendering
- Decorative particles (no gameplay impact)
- Screen transition animations
- Shader/visual effects
- UI layout helpers

### File Size Limits

| Threshold | Action |
|-----------|--------|
| > 800 lines | **Error** - must split file |
| > 600 lines | **Warning** - consider splitting |
| > 100 lines/function | **Warning** - extract functions |

## Workflow

1. **Run full validation**: `./scripts/validate_all.sh`
2. **Review violations**: Check output for ✗ markers
3. **Fix issues**: Refactor code to correct layer
4. **Re-validate**: Ensure all checks pass
5. **Proceed with release**: Once clean

## Checks Performed

### Core Checks (blocking)

| Script | Purpose |
|--------|---------|
| `check_file_sizes.sh` | Max 800 lines/file, warn at 600 |
| `check_layer_boundaries.sh` | No game logic in engine/, no rendering in sim_gen/ |
| `check_structure.sh` | Files in correct directories |
| `check_import_cycles.sh` | No circular package dependencies |
| `pre_release_check.sh` | Build, tests, TODOs, debug code |

### Extended Checks (warnings)

| Script | Purpose |
|--------|---------|
| `check_complexity.sh` | Function size (<100 lines), nesting depth, param count |
| `check_ailang_sync.sh` | AILANG types match sim_gen Go types |
| `check_api_stability.sh` | sim_gen exports haven't changed unexpectedly |
| `check_coverage.sh` | Test coverage for critical paths |
| `check_dependencies.sh` | Package import graph, layer violations |

### API Stability

The API stability check maintains a baseline of sim_gen exports:

```bash
# Update baseline after intentional API changes
.claude/skills/game-architect/scripts/check_api_stability.sh --update
```

## Design Doc Management

Track implementation progress of design docs through sprint files:

```bash
# Audit design docs - check which have sprints
.claude/skills/game-architect/scripts/audit_design_docs.sh
```

### Design Doc Workflow

1. **Create design doc** in `design_docs/planned/next/`
2. **Use sprint-planner skill** to create sprint plan in `sprints/`
3. **Execute sprint** (sprint tracks implementation progress via checkboxes)
4. **When sprint complete**, move doc to `design_docs/implemented/vX_Y_Z/`

### Audit Output

The audit script checks:
- Which design docs have corresponding sprint files
- Sprint completion percentage (via checkbox counting)
- Orphan sprints (sprints without design docs)

Design docs WITHOUT sprints need planning before implementation.

## Resources

- [Architecture Rules](resources/architecture_rules.md) - Detailed layer boundaries and examples
