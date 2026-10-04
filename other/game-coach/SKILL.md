---
name: game-coach
description: Converts board and match analysis into useful player feedback — mistakes, excellent moves, alternatives, turning points. Use when building post-game analysis, hints, or any explanatory text.
---

# game-coach

## Purpose

Turn deterministic engine output into something a player learns from. Very few puzzle games can
tell you *why* you lost; done well, this is a substantial differentiator.

## When to invoke

- Post-match analysis
- Hints and tutorials
- Critical-turn detection
- Any player-facing explanation of gameplay

## Responsibilities

Identify mistakes · identify excellent moves · compare alternative moves · detect turning
points · produce post-game recommendations.

## The line that must not be crossed

```
engine → metrics → structured findings → language
```

A finding is **data**:

```json
{ "type": "isolated_region", "turn": 71, "cells": 2, "blocked_pieces": 3 }
```

The language layer renders that as a sentence. It **never** inspects the board, never judges
legality, and never generates a finding of its own.

> **Never invent analysis.** All explanations must be grounded in deterministic engine output.

### Why this is absolute

An LLM asked to "look at this board and give advice" produces fluent, confident, occasionally
wrong advice. Players will believe it. In a game whose entire premise is that skill is legible
and rewarded, teaching people the wrong lesson is a product failure, not a cosmetic one.

The engine already knows the true answer. The language layer's only job is to say it well.

## Process

1. Identify the finding from engine data — never from a vibe about the board.
2. Verify it is genuinely notable. Flagging every suboptimal move is noise; players stop reading.
3. Render it, with the specific numbers included. "You created an isolated 1×2 region which
   blocked three later pieces" teaches; "that was a weak move" does not.
4. Confirm it traces back to its finding.

## Constraints

- Every sentence traces to a specific structured finding. A test enforces this.
- Gameplay evaluation stays deterministic; the language layer is a pure renderer.
- Analysis is **optional and never blocks the rematch** — the rematch impulse is strongest
  immediately after a loss and must not be delayed by a wall of text.
- Degrades gracefully: without the language layer, findings render as plain templates.
- Be specific and kind. The player just lost.

## Testing expectations

A test verifying the language layer cannot produce a claim without a backing finding. Critical
turns matching human judgement on manual review. Graceful degradation with the language layer
unavailable.

## Consults

`board-analysis` (metrics) · `game-ai` (move ranking) · `replay-debugger` (reconstruction) ·
`game-ux` (readability, and how much is too much)

## Definition of done

Every claim is grounded in engine output, the analysis is genuinely useful rather than
exhaustive, and it never stands between a player and the rematch button.
