---
name: architecture
description: "Find deepening opportunities, design an interface two ways, or plan a behavior-preserving refactor."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills improve-codebase-architecture (+ HTML-REPORT.md), codebase-design (+ DEEPENING.md, DESIGN-IT-TWICE.md), design-an-interface, request-refactor-plan; MCT (local) skills/refactor-safely; cursor/plugins pstack 0.15.25 architect (+ references/design-red-flags.md, rationale-template.md, runner-prompt.md), principle-minimize-reader-load, principle-migrate-callers-then-delete-legacy-apis"
---

# Architecture

Make code easier to change and test by deepening modules: more behavior behind a smaller interface, at a seam where something actually varies. Read `references/vocabulary.md` before the first suggestion and use its terms exactly (module, interface, implementation, depth, seam, adapter, leverage, locality); drifting into "service", "API" or "boundary" blurs what you mean. Domain names come from `CONTEXT.md`. ADRs in `docs/adr/` are settled; reopen one only when the friction is real, and name it ("contradicts ADR-0007, worth reopening because …").

| Ask | Branch |
|---|---|
| "improve the architecture", "where's the friction", code hard to test or navigate | 1. Find deepening opportunities |
| A chosen module or a new interface; "design it twice" | 2. Design the interface twice |
| "plan this refactor", a restructure that must keep behavior | 3. Plan a behavior-preserving refactor |

## 1. Find deepening opportunities

1. **Explore.** Read `CONTEXT.md` and the ADRs for the area, then walk the code (subagents for bulk reading). Note where you feel friction, using the red flags in `references/vocabulary.md`: one concept spread across many small modules, interfaces nearly as large as their implementations, pass-through layers, one internal decision known in several modules, two ways to do one task, logic extracted for testability while the bugs live in how it's called, code untested because its interface makes testing hard.
2. **Deletion test** each suspect. Delete it in your head: if the complexity vanishes, it was a pass-through, so collapse it. If the complexity reappears across N callers, it earns its keep.
3. **Reader-load test.** A new reader should answer "where does X come from?" and "what can change X?" in under 30 seconds.
4. **Present three to six candidates**, strongest first. Each: files; problem (one sentence); the deepening (one sentence); wins in locality, leverage and test terms; dependency category; strength `Strong`, `Worth exploring` or `Speculative`; any ADR conflict. Chat by default. If the user wants visuals, write a self-contained HTML report with before/after diagrams to `${TMPDIR:-/tmp}/architecture-review-<timestamp>.html` and give the path. Leave interfaces for branch 2.
5. **Ask which to explore.** Grill the pick with the `grill` skill: constraints, what sits behind the seam, which tests survive. Keep new terms in `CONTEXT.md` through the `domain` skill. If the user rejects a candidate for a load-bearing reason, offer an ADR so future reviews don't suggest it again.

Done when: the user has a ranked list and has picked one candidate or declined them all.

## 2. Design the interface twice

Your first design is rarely the best; contrast is how you find a better one.

1. **Frame.** Problem, callers, key operations, constraints, what must stay hidden, dependency category. Write the caller's usage first: two or three realistic call sites. The types serve the usage, never the reverse. Show the frame to the user and keep going.
2. **Generate at least two, default three, radically different designs**, in parallel subagents. Each brief carries the file paths, the vocabulary, the `CONTEXT.md` terms, and one constraint: minimal (one to three entry points); maximally flexible; the common case trivial; ports and adapters across the seam. Each returns: the interface (types, invariants, ordering, error modes), a usage example, what it hides, its adapters, and its trade-offs. Without subagents, write them one after another, each from its own constraint.
3. **Screen** every design against the red flags in `references/vocabulary.md`.
4. **Compare in prose** on depth, locality, seam placement, and ease of correct use against ease of misuse. Implementation effort is not a criterion.
5. **Recommend** one design or a hybrid, opinionated, with at least one rejected alternative and why it lost. One adapter means a hypothetical seam; add a port only when a second adapter (usually the test one) exists.

Done when: one interface is chosen, its usage example is written, and each loser's reason is recorded.

## 3. Plan a behavior-preserving refactor

1. **Pin the behavior that must not change**: the interface, outputs, side effects, UI, stored data, error modes. Check the user's claims about the current code before planning on them.
2. **Find the checks that prove it.** Where coverage is thin, the plan's first step is characterization tests at the interface, through the `tdd` skill.
3. **Fix the scope**: what changes, and what explicitly stays. Unrelated cleanup is its own change.
4. **Order tiny steps**, each leaving the program working. Prefactor first: make the change easy, then make the easy change. For a new internal API with no external users: add it, migrate callers in batches, then delete the old API and its tests in the same wave, with no compatibility shim. Replace tests, don't layer them: new tests at the deepened interface; delete tests that pinned the old shallow internals.
5. **Write it with the `plan` skill**, using `references/refactor-plan.md` for the sections. Every step ends with the check that shows behavior held.
6. **While executing**, read each step's diff for accidental interface, UI or data-flow changes. If the same workaround appears twice, the target shape is wrong: stop and return to branch 2.

Done when: every step has a check that proves behavior held, and deleting the old path is a step in the plan, not a follow-up.
