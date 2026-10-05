---
name: difficulty-and-balancing
description: Use when designing, tuning, or reviewing the difficulty or balance of any game system — encounter tuning, cost curves, dominant-strategy audits, dynamic difficulty adjustment (DDA), difficulty settings, and accessibility assists. Also use to diagnose "this is too hard/too easy", "everything feels overpowered", a degenerate meta, a missing difficulty curve, or an accessibility gap. Triggers on "balance", "balancing", "difficulty", "difficulty curve", "dynamic difficulty", "DDA", "dominant strategy", "overpowered", "underpowered", "too hard", "too easy", "cost curve", "power budget", "tuning", "accessibility difficulty", "difficulty settings", "assist mode", "rubber band", "flow channel", "tier list", "god tier", "broken build".
---

# Difficulty & Balancing

The discipline of ensuring no single option dominates and every player stays in the flow channel — made rigorous by encoding balance as testable invariants and verifying them through simulation, not intuition alone.

> **Tier:** universal craft (→ `gamestack-core`). Applies across all genres and multiplayer contexts. The encounter-difficulty application lives in `combat-design`; economy and loot power-budget live in `rpg-systems`.

## When to use this

- Auditing a system for dominant strategies (God-tier lock-in, degenerate meta, solved builds)
- Verifying cost-curve balance across a weapon, card, or unit roster
- Designing or tuning a difficulty curve — encounter sequence, wave rhythm, spike detection
- Specifying or auditing a DDA system (target metric, adjustment range, visibility decision)
- Designing difficulty settings and per-axis accessibility assists
- Building a pre-ship balance spreadsheet or instrumenting post-ship telemetry

## Scope

This skill owns **the balance and difficulty of game systems** — option viability, cost curves, difficulty curves, DDA, and accessibility. Adjacent concerns live in sibling skills:
- The "interesting decision / no dominant option" principle as a design foundation → `game-design-fundamentals` (this skill operationalizes that invariant)
- Encounter difficulty, enemy telegraphing, and encounter feel → `combat-design`
- Economy tuning, loot tables, and power-budget math → `rpg-systems`
- Macro difficulty pacing across a session arc → `pacing-and-the-player-journey`
- Procedural content gating and generation constraints → `procgen-review`
- Fairness and player expectations under permanent death → `permadeath-and-lethality`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: dominant strategies & degenerate cases; balance structures (symmetric/asymmetric/intransitive + cost-curve/power-budget); difficulty curves & DDA / hidden directors; difficulty settings & accessibility; metrics-driven balance (spreadsheets, simulation, telemetry). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as automated validators in a generation or build-gate loop.

## The one idea to anchor on

> **Balance exists to ensure no single option dominates — and this is the most machine-checkable discipline in game design.** Sid Meier's rule (GDC 2012): a choice with an obvious correct answer is not a decision. Encode the invariant ("no option's expected value exceeds all others in >80% of game states"), then simulate to enforce it. A human team can *feel* a broken meta; a headless generator cannot — it must measure it. Build the payoff matrix, run the dominance check, and gate every content ship on the result.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
