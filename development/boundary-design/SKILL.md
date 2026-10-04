---
name: boundary-design
shapes: [boundary-design]
description: >
  Draw the line where it costs least. Use for build-vs-buy calls, "where does this
  module/team/service boundary belong?", APIs and abstractions forcing users into
  implementation vocabulary, tools that should augment rather than automate,
  hardcoded decisions that belong at runtime, or information nobody can find.
---

# Boundary Design

**Problem shape:** something must be split, wrapped, or interfaced — a system
into modules, a workflow between human and tool, a product between build and
buy — and the current boundary leaks implementation detail, transaction cost,
or cognitive load across it.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [coase](../../agents/genius/coase.md) | build vs buy; team/service boundary placement — compare transaction costs across the boundary, not ideology |
| [hopper](../../agents/genius/hopper.md) | users forced to think in implementation vocabulary — build the translator; debugging under-invested; a tool defended out of familiarity |
| [engelbart](../../agents/genius/engelbart.md) | "automate this" proposed where augmenting the person is the real win; the team doesn't use its own tool; design for expert ceiling, not just novice floor |
| [kay](../../agents/genius/kay.md) | decisions hardcoded that could bind late; tight coupling via direct calls; users need to modify the system at runtime |
| [alexander](../../agents/genius/alexander.md) | decompose by misfit; the design needs a generative sequence of patterns rather than a top-down blueprint |
| [simon](../../agents/genius/simon.md) | the system should be nearly decomposable — strong interactions inside modules, weak between; hierarchy as the default shape |
| [liskov](../../agents/genius/liskov.md) | the boundary is an interface — write the behavioral contract so implementations are substitutable |
| [ranganathan](../../agents/genius/ranganathan.md) | information exists but nobody can find it — faceted classification and findability laws |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. Every proposed boundary states what crosses it, what it
   hides, and what it costs (Clean Architecture layer rules apply, §2.2).
4. Typical chain: coase places the boundary → simon shapes the decomposition →
   liskov contracts the interface. Run via
   `tools/genius-invoker.sh compose coase liskov -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The boundary is being drawn to match an org chart against the dependency
  evidence — surface the conflict instead of ratifying it.
- Fewer than three concrete uses exist for a proposed abstraction
  (coding-standards §3.3: premature abstraction is worse than duplication).
