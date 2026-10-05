---
name: combat-design
description: Use when designing, tuning, or reviewing combat and game feel — juice/feedback budgets, hit-stop and impact, telegraphing and danger cues, enemy silhouettes and role-based rosters, multi-enemy readability, encounter pacing, and high-lethality (Souls-like) commitment/stamina/checkpoint loops. Also use to diagnose combat that feels floaty, noisy, unfair, swarmy, or like a memorization "knowledge check". Triggers on "combat design", "game feel", "juice", "hit-stop", "screen shake", "telegraph", "wind-up", "readability", "enemy design", "encounter design", "aggression", "gank", "stamina", "souls-like", "lethality", "this death felt cheap", "combat feels floaty".
---

# Combat Design & Game Feel

How to make combat that **feels** powerful and **reads** fairly — especially in a high-lethality game where an unreadable hit is a broken promise. Juice sells the hit; telegraphing keeps it fair; encounter structure keeps the fight legible; commitment + a generous retry loop make hard feel fair instead of cheap.

## When to use this

- Tuning game feel: juice budgets, hit-stop, screen shake, the impact bundle
- Authoring or auditing telegraphs and a game-wide danger-cue vocabulary
- Designing enemies (silhouettes, combat roles) and multi-enemy encounters
- Building a Souls-like lethality loop: commitment, stamina, comeback mechanics, checkpoints
- Diagnosing combat that feels floaty, noisy, unfair, swarmy, or memorization-gated

## Scope

This skill owns **moment-to-moment combat and its feel**. Adjacent concerns live in sibling skills, cross-linked from the guide:
- General game feel — input/latency, forgiveness windows, the full juice toolkit, the 12 animation principles, camera & UI feel → `game-feel-and-juice` (the universal foundation; **this skill applies it to hits, impacts, and telegraphing**)
- General reward/flow/difficulty theory and the "interesting decision" test → `game-design-fundamentals`
- The single-save consequence model & meta-progression → `permadeath-and-lethality`
- Loot/itemization that feeds builds, damage tiers as economy → `rpg-systems`
- Enemy placement in the world, sightlines to a fight → `open-world-design`
- Generating enemies/encounters within these constraints, and gating them → `procedural-generation`, `procgen-review`
- Multiplicative systems that make fights emergent → `systemic-emergent-design`
- Boss/quest framing → `narrative-and-quest-design`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in four sub-domains: combat juice (the inverted-U dose curve, **applied to hits** — general feel theory lives in `game-feel-and-juice`), readability/telegraphing (fairness as a contract), enemy & encounter design (silhouettes, roles, readable chaos), and Souls-like lethality (commitment, death-as-teacher, comeback, checkpoints). Each rule carries an exemplar, a source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as automated validators in a generation loop, not just read.

## The one idea to anchor on

> **In a lethal game, telegraphing is fairness, not decoration.** Every attack that can kill must be preceded by a readable, consistent wind-up whose salience scales with its damage ("relative damage must match perceived danger"). The general feel foundation this rests on — the inverted-U juice ceiling (Kao 2020), input response, and the animation-principle inversion (anticipation warns on enemies, lags on the player) — lives in `game-feel-and-juice`; this skill applies it to the specific case of hits and the fairness contract.

> **Why this matters doubly for a generator:** a human team feels an un-telegraphed kill or a juice-overloaded screen as "off." An autonomous generator does not. Hand-author the cue vocabulary, the damage→telegraph curve, the feedback table, and the stamina/checkpoint numbers as **inviolable contracts**, then let generation recombine vetted parts inside them — and run headless validators (telegraph checker, juice linter, fairness ghost-runner) before any content is committed.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
