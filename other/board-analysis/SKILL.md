---
name: board-analysis
description: Owns board-quality algorithms — fragmentation, holes, connected regions, piece compatibility, flexibility, danger, clear potential. Shared infrastructure for AI, hints and post-match analysis.
---

# board-analysis

## Purpose

Answer "how good is this board?" with numbers. This becomes shared infrastructure for the AI,
hints, difficulty, post-match analysis and balancing — so a mistake here propagates to all of
them at once.

## When to invoke

- Adding or changing a board metric
- When the AI, coach or analysis needs a new signal
- Investigating why the AI plays badly, or why a hint looks wrong

## Responsibilities

Fragmentation · isolated holes · connected empty regions · largest open region · piece
compatibility · flexibility · danger · clear potential · future survivability · available 3×3
spaces · long horizontal and vertical runs · legal placement count.

## The metric that matters most

**Flexibility** — how many possible future pieces can this board still accommodate?

> A board with 30 empty cells can be considerably worse than one with 25 if those 30 are badly
> fragmented.

**Do not equate empty space with board quality.** Any metric that does will mislead the AI, the
hints and the coach simultaneously — and will do so confidently, which is worse than being
obviously wrong.

## Process

1. Define the metric precisely in prose, including its range and what "good" means.
2. Build hand-constructed boards with known-correct answers, including at least one where a
   board with *more* empty cells scores *worse*.
3. Implement, verify against the fixtures, then benchmark.
4. Document the definition — an undocumented metric will be misused by a later consumer.

## Constraints

- **Read-only.** Analysis never influences simulation, and nothing in `applyAction` may call it.
- Side-effect-free and allocation-light — this runs inside the AI's search loop, millions of
  times during a balance sweep.
- Integer-valued wherever it feeds anything hashed or compared for determinism.
- A metric with no consumer should not exist. Delete speculative ones.

## Testing expectations

Hand-constructed boards with expected values. Explicitly: a fragmented board with more empty
cells scores worse than a compact board with fewer. Benchmarked against the AI's per-move budget.
Proven side-effect-free.

## Consults

`game-rules-engine` (state access) · `game-ai` (consumer) · `game-coach` (consumer) ·
`game-performance` (search-loop cost)

## Definition of done

Each metric has a written definition, fixture-verified values, a real consumer, and a benchmark
showing it is affordable inside the search loop.
