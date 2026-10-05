---
name: level-design
description: Use when designing, generating, or reviewing the craft of an individual level, zone, or encounter — layout, wayfinding, structural type, lock-and-key gating, antepieces, arena design, in-level pacing, and the greybox process. Also use to diagnose levels where players get lost, challenge feels unfair, pacing drags, or teaching moments land flat. Triggers on "level design", "level layout", "greybox", "blockout", "wayfinding", "sightlines", "lock and key", "arena design", "encounter design", "the level feels confusing", "players get lost", "chokepoint", "flanking route", "intensity curve", "antepiece", "teach the mechanic", "critical path", "leading lines", "weenie", "breadcrumbs", "level feels boring", "players don't know where to go".
---

# Level Design

How to craft a level — or generate one — that guides players through space so they always know where to go and why, teaches through the environment instead of a tutorial pop-up, paces intensity as a rhythm of peaks and valleys, and validates all of it in blockmesh before a single art asset is committed.

> **Tier:** universal craft (→ `gamestack-core`). Applies to every genre that has levels, rooms, or encounters. The macro/world spatial layer lives in `open-world-design`; this skill owns the *level/encounter* craft.

## When to use this

- Laying out a level or zone — structure type, critical path, arenas, shortcuts
- Designing or auditing wayfinding (players getting lost or marker-following)
- Authoring antepieces and teaching sequences for new mechanics
- Designing or diagnosing encounter/arena propositions
- Plotting and tuning in-level intensity curves
- Specifying a blockmesh-first process a generator can follow

## Scope

This skill owns the **level/encounter** spatial craft layer. Adjacent concerns live in sibling skills:
- The *macro/world* spatial layer (terrain, biomes, world-map layout, exploration pull) → `open-world-design`
- *What* to generate and how to validate generated content → `procedural-generation`, `procgen-review`
- Combat-specific feel (hit-stop, telegraphing, enemy feel) within arenas → `combat-design`
- In-level pacing as part of a session-wide arc → `pacing-and-the-player-journey`
- Signposting, landmarks, signal color, silhouette → `art-direction-and-readability`
- Teaching through space as part of the onboarding arc → `onboarding-and-teaching`
- General reward/flow/motivation theory → `game-design-fundamentals`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in six sub-domains: guidance language (critical path, breadcrumbing, leading lines, weenies, light/color, affordances); structure & gating (structural types, lock-and-key, interconnection/shortcuts, Metroidvania loop); teaching through space (antepiece, intro→develop→twist→conclude, the gym); encounter/arena design (arena proposition, cover, chokepoints, flanking, verticality); in-level pacing (intensity curve, rest beats, reward placement); and the greybox process (blockmesh, metrics, playtest iteration). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The one idea to anchor on

> **Guide the player through the space itself — not the HUD.** Landmarks, light, leading lines, and affordances must tell the player where to go and what to do before a minimap arrow ever has to try. If a player is watching a minimap instead of the horizon, the level has become an obstacle between them and a waypoint.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
