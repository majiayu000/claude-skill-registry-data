---
name: game-design-fundamentals
description: The foundational design discipline — the spine the rest of the pack cross-links to. Use when judging whether a mechanic is fun, auditing a system for balance, designing difficulty/flow, setting reward schedules, checking player motivation, or diagnosing "my choices don't matter" / "this is grindy" / "this difficulty spike feels cheap". Covers interesting decisions (Sid Meier), flow & difficulty curves, intrinsic/extrinsic motivation (Self-Determination Theory), feedback & agency, and choice architecture. Triggers on "is this fun", "interesting decision", "dominant strategy", "balance this", "difficulty curve", "flow", "reward schedule", "player motivation", "fake choice", "analysis paralysis", "one more turn".
---

# Game-Design Fundamentals

The bedrock principles every other skill in the pack assumes. If a design decision feels wrong and you're not sure why, the answer is usually here.

## When to use this

- Deciding whether a mechanic, system, or choice is actually *fun* (not just functional)
- Balancing — hunting dominant strategies, no-brainer options, difficulty spikes
- Designing difficulty/flow, reward schedules, or progression
- Diagnosing player complaints: "my choices don't matter", "it's grindy", "that death was cheap", "I'm overwhelmed"

## Scope

This is the **spine**. Sibling skills specialize it and link back here:
- Spatial reward cadence & exploration pull → `open-world-design`
- Perceptual uniqueness / the oatmeal problem → `procedural-generation`, `procgen-review`
- Telegraphing & fair lethality → `combat-design`, `permadeath-and-lethality`
- Loot dominance & economy balance → `rpg-systems`
- Real vs. fake branching → `narrative-and-quest-design`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*: interesting decisions, flow & difficulty, motivation (SDT), feedback & agency, choice architecture. Each principle carries exemplars, sources, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by topic. These are written to be enforced as automated invariants in a generation loop, not just read.

## The one idea to anchor on

> **A game is a series of *interesting* decisions** (Sid Meier). A decision is interesting only when it has believed, persistent consequences, is made with enough information, carries a real trade-off, and **has no dominant option**. The single highest-leverage audit you can run: scan every system for a strictly-best strategy and delete it.

> **Why this matters doubly for a generator:** a human team has a "this feels off" reflex that catches a broken economy or a cheap death late. An autonomous agent has none. So treat each principle here as an **enforced automated invariant**, not advice.

Start with `GUIDE.md`.
