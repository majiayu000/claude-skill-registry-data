---
name: architect
description: Re-derive the simplest, cleanest architecture from first principles. Enforces minimal code, composition, single source of truth, deep modules, clear abstractions, clean interfaces, functional core, state machines for lifecycle, ports/adapters, typed recovery, no silent fallbacks, Effect primitives in Effect-owned code, and game-theoretic incentive compatibility. Output uses ASCII diagrams and code contracts, never mermaid, and fits one to two screens. Hands off to /review.
---

# /architect

Before rendering user-facing output, read `../_shared/plain-output.md` and `../_shared/ascii-diagrams.md`.

Re-derive the architecture from the problem, constraints, values, non-goals, codebase reality, and incentive structure.

Do not anchor on the user's initial solution sketch unless it survives first-principles scrutiny and game-theoretic pressure.

This is an architecture skill, not an implementation skill. Produce the architecture that should exist before GitHub issues are written.

## Preconditions

- `/interview` should have produced a locked core shape, or the current conversation must contain equivalent clarity:
  - problem
  - root cause
  - affected users/systems
  - constraints
  - non-goals
  - architectural values
  - game board
  - desired equilibrium
  - rough solution direction
  - review criteria
- If the core shape is missing, do not design. Tell the user to run `/interview` first and stop.
- If `/scout` has not run, perform a scout-equivalent grounding pass before designing.

## Core thesis

A good architecture is a mechanism. It should make:

- the correct action cheap
- the dangerous action impossible or loud
- the ambiguous action reviewable
- the repeated future action sustainable
- the local incentive aligned with global code health

## Shared contracts

Before grounding or spawning subagents, read `../_shared/subagents.md`, `../_shared/evidence-quality.md`, and `../_shared/grounding.md`.

`/architect` owns the final design. Subagents may gather evidence, propose alternatives, or critique a draft, but they do not decide the architecture.

## Principle spine

The full principle spine lives in `./PRINCIPLES.md`. Walk it during the derivation; cite a violation only when it is an explicit, justified trade-off.

Quick spine:

- **First principles.** Start from invariants. Separate facts from assumptions. Name primitive concepts. Derive before choosing.
- **Game-theoretic.** Design the mechanism. Good move easy, bad move loud. Account for players, incentives, information asymmetry, repeated-game durability, principal-agent safety, adversarial input.
- **Simplicity.** Minimal code. KISS. YAGNI. Complexity is a budget.
- **Modularity.** Deep modules, narrow interfaces, information hiding, separation of concerns, don't complect. Name what it is, not what wraps it.
- **Composition.** Compose, don't inherit. Program to contracts. Restrained Open/Closed.
- **I/O direction.** Ports and adapters. Dependencies point inward. Layer discipline. No circular dependencies.
- **Functional core.** Pure decisions in the core, effects at the shell. Data over behavior at boundaries. Single source of truth.
- **State & lifecycle.** Make invalid states unrepresentable. State machines only where lifecycle is real. Domain invariants at boundaries.
- **Effects & errors.** Effect-first in Effect-owned code. Typed errors. **No silent fallbacks.** Idempotency for retriable side effects. Failure modes are architecture.
- **Quality.** Performance budget, reliability story, least privilege, observability, testability, migration safety, explicit non-goals.

## Process

0. **Check context.** If `/interview` did not lock the core shape, stop and ask the user to run it. If `/scout` did not run, perform scout-equivalent grounding now.

1. **Ground before designing.** Read repo code/tests; use `rg`, ast-grep, symbol/type search; inspect existing conventions; inspect `node_modules` or installed package source when library behavior matters; use official docs, `shelf`, `context7`, `gh_grep`, and `exa` when relevant. If the codebase can answer a question, do not ask the user.

2. **Restate the problem from first principles.** One sentence. No solution-assuming phrasing.

3. **Define the game board.** Players, incentives, information asymmetries, bad local moves, global costs, desired equilibrium, adversarial moves, repeated-game risks.

4. **List constraints.** User, codebase, quality, compatibility, migration, non-negotiable architectural constraints.

5. **Name the core trade-off.** `I am trading X for Y.`

6. **Derive the minimal architecture.** Start from invariants and pure core. Push state, I/O, lifecycle, framework details, retries, logging, and wiring outward. Add ports only for real I/O or volatility. Add abstractions only when they hide something real. Add state machines only for lifecycle.

7. **Draw the architecture with ASCII.** Module/flow diagram. Add an ASCII state diagram only when lifecycle exists. Both follow `../_shared/ascii-diagrams.md`. **No mermaid.**

8. **Show one or two typed code contracts.** Public interface, command shape, or state union — at the contract level, not the implementation. A code example beats three paragraphs describing the same shape.

9. **Specify modules tersely.** For each module: responsibility, interface signature, what it hides, dependency category (`pure-core`, `in-process`, `local-substitutable`, `ports-and-adapters`, `true-external`), state ownership, error model, incentive effect, test strategy. One row per module in a table. Skip rows that don't change the decision.

10. **Run the principle and game-theory fit checks.** Name only the high-risk principles and how the design satisfies or deliberately violates them. Skip principles that are not at risk.

11. **State quality attributes** that bind the design: performance, reliability/failure modes, security/least privilege, observability, testability, migration/compatibility.

12. **Self-review.** When subagents are available, spawn bounded critics for the highest-risk lenses (boundary ownership, lifecycle/state, failure/concurrency, security/authority, simplicity/deep modules, Effect discipline, code grounding). Revise the draft before output. If subagents are unavailable, run the lenses locally and say so.

13. **State explicit non-goals.**

If you cannot ground a decision, stop and ground it. Do not guess.

## Output

Use Plain Senior output. One to two screens. **ASCII diagrams only.** A code example is required.

````markdown
## Decision
<one sentence naming the architecture>

## Problem
<what is true now, what must remain true, what should become true — three short paragraphs>

## Why
- Grounding: <repo or doc facts that shaped the design>
- Trade-off: I am trading <X> for <Y>.
- Mechanism: <how the good move becomes cheap and the bad move loud>

## Design

<One to two paragraphs. Name modules only when they change the decision.>

```
<ASCII module/flow diagram — see ../_shared/ascii-diagrams.md>
```

<If lifecycle exists, add a second ASCII state diagram.>

```ts
// Public contract — types and signatures only.
export type <Name> = {
  readonly <method>: (<input>) => <Effect.Effect<Output, Error>>
}
```

## Modules

| Name | Responsibility | Interface | Hides | Dependency | Incentive |
|---|---|---|---|---|---|
| `<Name>` | <one sentence> | `<signature>` | <impl detail> | <category> | <how this makes correct use easy or misuse loud> |

## Proof
- Invariants protected: <one line each>
- Failure modes: <one line each>
- Observability: <one line>
- Tests: <one line>

## Risk
- <remaining risk or explicit trade-off>

## Next
Run `/review` to pressure-test it before opening an issue.
````

Then end with exactly this line and stop:

> Architecture proposed. Run `/review` to pressure-test it before opening an issue.

## Hard rules for output

- **No mermaid.** ASCII diagrams only. Width under 80 chars. Max 3 levels of nesting.
- **At least one code contract.** Types and signatures, not implementation. Will Larson: "specific creates alignment; generic creates the illusion of alignment."
- **One to two screens total.** If it doesn't fit, the problem isn't decomposed enough.
- **No walls of text.** One idea per paragraph. Bullets when they help scanning.
- **Cut everything that doesn't change the decision.** Modules table rows, fit-check items, quality attributes — drop anything generic.
- **No "alternatives considered" section.** That belongs in `/scout` or `/review` notes.
- **End with the exact handoff line.** No trailing summary.
