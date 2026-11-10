---
name: wargame-domain
description: Iron Pipeline's domain language and core model — hexes, units, stacks, ZOC, supply lines, depots, trucks, MP/fuel/ammo — plus the Command/GameState conventions and pillars. Load before writing specs, Sim code, or domain reviews.
---
# Iron Pipeline domain

## Pillars (from docs/gdd.md)
Logistics tension · Big maps · Readable tactics · Distinct factions. Every spec names the pillar it serves.

## Glossary — use these words, in code and specs
| Term | Meaning |
|---|---|
| **hex** | one map cell; `HexCoord(q, r)` axial, cube `s = -q-r`; pointy-top in presentation only |
| **terrain** | per-hex type with movement cost (MP) and defense modifier; from `content/terrain/` |
| **unit** | a company/battalion-scale piece with a type from `content/units/`, a faction, strength, MP, fuel, ammo |
| **stack** | the units on one hex; stacking limit is content data |
| **MP** (movement points) | per-turn movement budget; terrain cost is deducted per hex entered |
| **fuel** | consumed per hex moved; at 0 the unit cannot move (it can still fight) |
| **ammo** | consumed per attack; at 0 the unit cannot attack (it can still defend, at a penalty) |
| **supply** | abstract resource delivered to units; v0 = fuel + ammo refills |
| **depot** | a fixed supply source on a hex |
| **truck** | a unit that carries supply from a depot to units in range |
| **supply line** | (later spec) traced path of friendly-controlled hexes from a depot; cut = no delivery |
| **ZOC** (zone of control) | the six hexes around a combat unit; entering one ends movement; from spec 0009 |
| **turn / phase** | one full round of all factions; each faction's turn has phases (supply → movement → combat → end) |
| **faction** | a side with an `ai_profile` from `content/factions/` |
| **scenario** | map + start positions + victory conditions from `content/scenarios/` |

## Core model conventions
- `GameState` is the whole world. It is treated as immutable: `Rules.Apply(state, command) → (newState, events)`.
- `Command` is a serializable record (`MoveCommand`, `AttackCommand`, `EndPhaseCommand`, …) carrying only ids and coordinates — never object references.
- `Event`s describe what happened for the presentation layer and the log (`UnitMoved`, `CombatResolved`, `UnitOutOfFuel`). Presentation reacts to events; it never recomputes rules.
- Queries (`Reachable(unitId)`, `CanAttack(a, b)`) are pure functions on state and are what the UI uses for highlighting.
- All balance numbers come from `content/`; code holds no constants beyond structural ones.

## Non-goals right now
Real-time, multiplayer, diplomacy, tech trees, fog of war before v1 decides.
