---
name: game-core-loop
description: Use only for video game projects; analyze moment-to-moment, session, progression, and retention loops
type: analysis
version: v0.2
required_conventions: [alignment-page]
context_intake: artifact_only
visual_tier: visual
---

# Game Core Loop

## Alignment-YAML Routing

While an alignment page is in `review`, the only next action is section-feedback YAML or final compiled YAML from the bottom compile controls. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Invoke as `$game-core-loop`.

Break the game into repeatable loops.

## Output

Write or update `research/game-core-loop.md` with the 10-second interaction loop, 1-minute action loop, 5-minute session loop, 30-minute progression loop, multi-day retention loop, reward cadence, and novelty sources.

## Next-Step Routing

After writing the artifact, recommend the next contextual game-pack skill in the final response as `Recommended next skill: <command>`.

Default recommendation: `$game-prototype-test`.

If prototype, playtest, or market evidence invalidates an upstream assumption, route back to the earliest affected artifact (`$game-audience`, `$game-fantasy`, `$game-genre-map`, or `$game-comparables`) and explain the evidence. Otherwise, follow the default game sequence:

`$game-audience` -> `$game-fantasy` -> `$game-genre-map` -> `$game-comparables` -> `$game-core-loop` -> `$game-prototype-test` -> `$game-playtest-metrics` -> `$game-store-page-test` -> `$game-launch` -> `$game-roadmap`

If the next artifact already exists and is current, recommend `$game-workflow` to identify the first missing or stale game-pack artifact.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/game-core-loop-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

