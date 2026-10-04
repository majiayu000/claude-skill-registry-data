---
name: game-ai
description: Develops computer players — board evaluation, move generation, search, lookahead, difficulty, battle strategy. Use when building or tuning AI opponents or the balance-simulation players.
---

# game-ai

## Purpose

Build computer players that use exactly the same engine and legal actions as humans — both as
opponents and as the instrument that makes balance measurable at scale.

## When to invoke

- Building or tuning AI move selection
- Adding or adjusting difficulty tiers
- Battle strategy (attack timing, defence decisions)
- Preparing players for a balance simulation sweep

## Responsibilities

Board evaluation · legal move generation · search · lookahead · difficulty levels · battle
strategy · attack timing · defence decisions.

## The hard constraint

> **AI must only use information available legally to a human player at that point in the match.**

It sees three pieces. It does not see the next set, read the seed, or query the opponent's board
beyond what a human's peripheral view shows.

Two reasons this is absolute. A cheating AI is unsatisfying to play against in a way players
detect without being able to articulate. And it is **worthless as a balance instrument** — the
entire point of a million simulated matches is learning what happens to *humans*.

The one exception: a balance simulation may explicitly model expected piece distributions,
provided that mode never ships as an opponent.

## Process

1. Start with **full-set search** — all placements × orderings of the three held pieces. This is
   tractable and already produces a strong player, because most human mistakes in this genre are
   ordering mistakes.
2. Only add depth if measurement shows it is needed.
3. Tune weights against simulation outcomes, not intuition.
4. For difficulty, degrade *coherently* — see below.

> Do not introduce ML unless conventional algorithms prove inadequate.

## Difficulty: coherent weakness, not noise

Adding noise ("pick the 5th-best move sometimes") produces an opponent that plays well for ten
turns then does something inexplicable. Players read that as broken, not beatable.

Prefer: shallower search · fewer evaluation terms (e.g. ignores fragmentation, so it slowly
ruins its own board like a real novice) · slower reaction under time pressure · worse attack
timing · occasional *realistic* blunders.

A weaker AI is weaker **within the rules**, never compensated with hidden advantages.

## Constraints

- Consumes the **same legal-move API** as the human input layer. Not a parallel one.
- Deterministic: same state + weights + seed → same move.
- Placement enumeration must return a **deterministic order**, or tie-breaking varies and the AI
  becomes irreproducible.
- AI randomness draws from its **own PRNG sub-stream**, never the piece stream — otherwise the
  piece sequence would depend on how hard the AI thought, invalidating every replay.
- Respect the per-move time budget.

## Testing expectations

A test proving the AI cannot observe information a human could not. Reproducibility from a seed.
Difficulty tiers measurably separated by win rate in headless simulation. Move decisions within
budget.

## Consults

`board-analysis` (features) · `game-rules-engine` (legal moves) ·
`game-balance` (simulation sweeps) · `game-performance` (search cost) ·
`game-coach` (shared ranking output)

## Definition of done

The AI plays through the human API under human information constraints, is reproducible from a
seed, meets its time budget, and its difficulty tiers feel human rather than random.
