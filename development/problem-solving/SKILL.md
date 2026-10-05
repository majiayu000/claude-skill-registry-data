---
name: mk:problem-solving
version: 1.0.0
description: |
  Use when stuck on approach (not debugging). Strategic unsticking via 7 non-default techniques:
  simplification cascades, collision-zone thinking, meta-pattern recognition, inversion, scale game,
  first principles, via negativa. Triggers on complexity spiraling, innovation block, recurring
  patterns across domains, forced-assumption solutions, scale uncertainty, told-it's-impossible,
  or bloated systems needing subtraction. For evidence-based root-cause debugging, use
  mk:sequential-thinking instead.
allowed-tools:
  - Read
  - Grep
  - Glob
source:
  - local
  - cc-thinking-skills
keywords:
  - problem-solving
  - first-principles
  - reasoning-framework
  - approach-design
  - decomposition
  - analytical-thinking
when_to_use: Use when applying first-principles reasoning to a complex problem. General-purpose problem decomposition.
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Problem-Solving — Strategic Unsticking

Seven techniques for non-debugging stuck-ness. Each targets a specific failure mode of default thinking.

## When to Use

**NOT this skill if:** you want open solution exploration before any plan exists — use `mk:brainstorming`. **NOT this skill if:** you want to re-examine an existing output or verdict — use `mk:elicit`.

Match symptom to technique. Load the reference only after matching.

| Stuck symptom                                         | Technique                | Reference                                |
| ----------------------------------------------------- | ------------------------ | ---------------------------------------- |
| Same thing implemented 5+ ways, growing special cases | Simplification Cascades  | `references/simplification-cascades.md`  |
| Conventional solutions inadequate, need breakthrough  | Collision-Zone Thinking  | `references/collision-zone-thinking.md`  |
| Same issue across domains, reinventing wheels         | Meta-Pattern Recognition | `references/meta-pattern-recognition.md` |
| Solution feels forced, "must be done this way"        | Inversion Exercise       | `references/inversion-exercise.md`       |
| "Should scale fine" — no idea where limits are        | Scale Game               | `references/scale-game.md`               |
| Told it's "impossible" / reasoning by analogy         | First Principles         | `references/first-principles.md`         |
| Bloated system, remove > add, simplify by subtraction | Via Negativa             | `references/via-negativa.md`             |
| Unsure which applies                                  | Dispatch flowchart       | `references/when-stuck.md`               |

## Do NOT use for

- **Anything broken / needing a fix** — use `mk:fix` (top-level orchestrator; invokes scout + investigate + sequential-thinking, adds regression tests, writes to memory).
- **Pure diagnostic reasoning without fix intent** — use `mk:sequential-thinking` directly (evidence-based hypothesis testing).
- **Trivial fixes** — typo, rename, single-file change with obvious cause.
- **Known-options trade-off** — use `mk:party` (multi-agent deliberation) or `mk:brainstorming` (solution alternatives).

The line: problem-solving is for being stuck on _approach_. Sequential-thinking is for being stuck on _cause_. `mk:fix` is for anything broken that needs fixing.

## The Seven Techniques

### 1. Simplification Cascades

Find one insight that eliminates multiple components. "Everything is a special case of X."

- **Win shape:** 10× (things deleted), not 10% (things optimized).
- **Red flag:** "Just need to add one more case..." repeating forever.

### 2. Collision-Zone Thinking

Force unrelated domains together. "What if we treated X like Y?"

- **Win shape:** Emergent properties from metaphor (services like circuits → circuit breakers, fuses).
- **Red flag:** "I've tried everything in this domain."

### 3. Meta-Pattern Recognition

Pattern in 3+ domains → likely universal. Extract, abstract, reuse.

- **Win shape:** Caching (CPU / DB / HTTP / DNS / CDN / LLM) collapses to one abstract "store frequently-accessed data closer."
- **Red flag:** "This problem is unique" — it probably isn't.

### 4. Inversion Exercise

Flip the core assumption. "What if the opposite were true?"

- **Win shape:** Valid inversion reveals context-dependence (strategic slowness → debounce, rate-limit, lazy-load).
- **Red flag:** "There's only one way to do this."

### 5. Scale Game

Test at extremes (1000× bigger / smaller). Extremes expose what normal scales hide.

- **Win shape:** Production readiness validated before production.
- **Red flag:** "Should scale fine" without evidence.

### 6. First Principles

Strip to fundamental truths. Rebuild from verified basics. Escape reasoning by analogy.

- **Win shape:** SpaceX-style 10× cost reduction by questioning "because that's the industry price."
- **Red flag:** Everyone accepts a constraint without evidence.

### 7. Via Negativa

Improve by removing, not adding. Subtraction is more robust than addition.

- **Win shape:** Remove a retry-with-backoff wrapper → surfaces the real intermittent bug → obvious fix.
- **Red flag:** "Adding X to fix the problem caused by adding Y."

## Process

1. Match symptom → pick technique (use `when-stuck.md` if unsure).
2. Load the one relevant reference. Do not preload others.
3. Apply. Document what worked and what did not.
4. Combine only if the first pass does not resolve.

## Combining Techniques

Use only when one pass fails. Keep the log.

- **Simplification + Meta-Pattern** — find pattern across domains, then collapse instances.
- **Collision + Inversion** — force the metaphor, then invert its assumptions.
- **Scale + Via Negativa** — extremes reveal what to cut.
- **First Principles + Inversion** — rebuild from zero, then flip the rebuild.

## Gotchas

- **Tool-stacking** — running 3 techniques before finishing one. One at a time. Finish or discard before adding.
- **Debugging misroute** — "my code is broken" is not problem-solving territory. Route to `mk:sequential-thinking`.
- **Premature abstraction** — collapsing 2 instances. Meta-pattern rule requires 3+ domains.
- **Metaphor over-fit** (collision) — every metaphor breaks. Document where it breaks, do not hide it.
- **Invalid inversion** — "trust all user input" is a security hole, not a context-dependent inversion. Test: does it work in _any_ real context?
- **Scale-game theater** — thinking about 1000× without running the numbers. Estimate concretely or it's vibes.
- **First-principles tourism** — listing assumptions without challenging them. Must ask _why_ each one is assumed.
- **Via-negativa overkill** — removing something users rely on. Confirm usage via telemetry before stripping.
- **Sunk-cost clinging** — refusing to accept a technique gave nothing. Move on. Log the null result.

## Workflow Integration

```
user stuck on approach
   ├→ match symptom → apply ONE technique → resolved ✓
   ├→ not resolved → try a combination (see above)
   ├→ actually stuck on cause → route to mk:sequential-thinking
   └→ actually a multi-perspective trade-off → route to mk:party
```

## References

Load only what you need. Before emitting any Mermaid block, Read `.claude/skills/preview/references/mermaid-essentials.md`.

- `references/when-stuck.md` — dispatch flowchart (start here if symptom unclear)
- `references/simplification-cascades.md`
- `references/collision-zone-thinking.md`
- `references/meta-pattern-recognition.md`
- `references/inversion-exercise.md`
- `references/scale-game.md`
- `references/first-principles.md`
- `references/via-negativa.md`
