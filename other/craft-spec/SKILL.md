---
name: craft-spec
description: From business need to code, in order. Eleven steps, two gates.
---

# Skill: Craft Spec

> "Specification work cannot be removed. Only moved."

Moved up front, into artifacts that outlive the session, it costs less than discovered in production.
Evans' aggregates, Meyer's contracts, Cockburn's ports — sequenced. **The order is the
contribution.**

## The Boundary

**This governs code that *decides*. It does not govern code that *depicts*.**

It applies wherever there is a decision spine — state that must not be corrupted, guarded by
transitions. That includes transactional domain logic **and state-machine UI**: a wizard is a state
machine wearing CSS.

It **idles** on projections — reports, transforms, rendering — where verification is golden examples
plus algebraic properties. It can host those; it cannot derive them. Read the boundary before you
start, not at step 9.

## Prerequisite

**Inside a convened panel, steps 4 and 10 may not be run by whoever did the work. No exception.**
Self-assessment of this kind runs near 29% accuracy, applied at the moment of maximum authorial
investment. `panel:adversary` judges gate 1; `panel:newcomer` judges gate 2.

**Walking this alone is a different thing, and legitimate** — the eleven steps are worth following
without a panel. There the gates degrade to self-checks: gate 1 by writing client code from three
callers, gate 2 cold after a deliberate gap. Record the weakening — `craft-charter`, *When Gates Are
Weakened*.

But a solo walk is **not a panel run**, and must not be recorded as one. Law 1 admits no degradation
inside a panel.

## The Walk

The numbering is the **order the artifacts depend on each other**, not an execution sequence.
See [re-entry](re-entry.md).

| # | Step | Act | Done when |
|---|------|-----|-----------|
| 0 | Domain knowledge | Indicative facts that hold whether or not you build anything | Every term used in a need is grounded in one |
| 1 | Needs | What must become true, stated so it could be false | Every term is an environment phenomenon, and *why* bottoms out at money, risk, time, or obligation |
| 2 | Invariants | Negate each need; derive the obstacles | Each has a consistency boundary, and transactional-vs-eventual is decided |
| 3 | Ports | Driving and driven | Two to four. Fifteen means adapters wearing port costumes |
| 4 | **Gate 1** | Signature draft, empty bodies | A non-author judge approves the shape |
| 5 | Contracts | Classify each: precondition, postcondition, class invariant, constraint | Every invariant has a terminus |
| 6 | Assertions | Derive from the contracts and the input partition | Every contract has at least one test |
| 7 | Primitives | Make illegal states unconstructable | Assertion count **dropped** |
| 8 | Adapters | Wire the ports. Hooks at ports only | A different client could consume this unchanged |
| 9 | Bodies | Implement | Every gate exits 0 |
| 10 | **Gate 2** | Cold read | Someone who wasn't here can rebuild the theory |

**Blame assignment is why step 5 has four termini, not one.** A precondition violation is the
caller's bug, a postcondition the supplier's, an invariant the class's. Collapse them and a failing
contract is merely red instead of diagnostic. The fourth — a **constraint** enforced below the code,
a unique index or a serialisable transaction — is where concurrency properties live, and no draft
can show it.

## Deeper

| | |
|---|---|
| [gates](gates.md) | how the draft comes to exist, and what each gate judges |
| [re-entry](re-entry.md) | discovery runs upward, and what re-opens |

## The Anti-Patterns

| Don't | Do | Why |
|-------|----|-----|
| One `ensure` per test | One contract, ≥1 test | Boundary values are one dataset, not three tests |
| A primitive that adds assertions | Delete assertions | If count rises, it is a wrapper |
| Test a rule at three altitudes | Lowest one still about behaviour | Triplication reads as thoroughness |
| Enumerate ports as technologies | Enumerate intents | HTTP is an adapter, not a port |
