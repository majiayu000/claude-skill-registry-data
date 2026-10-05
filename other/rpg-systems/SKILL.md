---
name: rpg-systems
description: Use when designing, tuning, or reviewing the core RPG systems triad — character progression (leveling, skills, attributes, classless vs. class), the economy (currencies, faucets/sinks, crafting materials), and loot & itemization (rarity tiers, drop rates, legendary/unique design). Also use to diagnose "leveling feels pointless", "the world scales with me", "players hoard their best items", "every legendary is just +stats", "the economy inflated", or "more loot but it means less". Triggers on "progression", "leveling", "level scaling", "skill system", "attributes", "economy", "currency", "gold sink", "faucet", "inflation", "loot", "itemization", "rarity", "drop rate", "legendary", "build-defining", "auction house", "hoarding".
---

# RPG Systems

The three interlocking number-systems that make an RPG feel like growth: **progression** (you get stronger), **economy** (you accumulate and spend), and **loot** (you find things worth finding). They fail together — level-scaling guts progression *and* devalues loot; a broken market guts the reward loop *and* the economy — so design and audit them as a triad.

## When to use this

- Designing progression: leveling, skill/attribute systems, classless vs. class, level scaling vs. zone gating
- Designing or balancing an economy: currencies, faucets/sinks, crafting materials, anti-hoarding
- Designing loot: rarity ladders, drop rates, legendary/unique identity, smart-loot biasing
- Diagnosing: "leveling feels pointless", "bandits in Daedric armor", "players never spend", "all legendaries are stat-sticks", "drowning in vendor trash"

## Scope

This skill owns the **RPG number-systems triad**. Adjacent concerns live in sibling skills, cross-linked from the guide:
- The "interesting decision" test, flow, reward schedules → `game-design-fundamentals`
- How loot/combat *feels* (impact, telegraphing, the rarity-effect ladder for finishers) → `combat-design`
- The single-save consequence model & meta-progression → `permadeath-and-lethality`
- Spatial gating, where a zone sits in the world → `open-world-design`
- Generating items/economy content within these constraints, and gating it → `procedural-generation`, `procgen-review`
- Systems that interact to produce emergence (currency-as-material chains) → `systemic-emergent-design`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in three sub-domains: progression (price advancement, don't scale the world), economy (faucets/sinks, desirable sinks, anti-hoarding under scarcity), and loot (rarity baseline, build-defining affixes, procedural breadth vs. hand-authored identity). Each rule carries an exemplar, source, **test-for** criterion, named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain, written to be enforced as automated gates in a generation loop.

## The one idea to anchor on

> **Build identity is preserved by opportunity cost, not by walls — and the path of least resistance must always be *playing the game*.** Every advancement should spend something finite; never scale the whole world to the player (the canonical trap — Oblivion's own designer called world-scaling "a mistake"); reserve the top loot tier for items that change *how you play*, not your numbers; and never let a market, an exploit, or a flood of drops outpace the kill → loot → upgrade loop.

> **Why this matters doubly for a generator:** an autonomous author will happily open uncontrolled faucets, mass-produce "uniques," or scale loot to the player — all locally reasonable, all globally corrosive. Hand-author the *invariants* (the spent resource, the zone level-bands, the finite-legendary manifest, the faucet/sink rates) as declared, inspectable, machine-testable contracts; let generation fill only the common→rare tiers inside them.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
