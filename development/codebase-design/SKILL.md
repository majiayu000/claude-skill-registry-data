---
name: codebase-design
category: codebase-build
description: Shared vocabulary and principles for designing deep modules — a lot of behaviour behind a small interface, placed at a clean seam. Use when designing or improving a module's interface, deciding where a seam goes, making code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
codex-short-description: "Deep-module design vocabulary: interfaces, seams, adapters, depth"
related-skills:
  - codebase-improve-architecture
  - codebase-plan-refactor
  - tdd
loop-eligible: false
compatibility: claude-code codex opencode
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

This skill is **reference, not a procedure** — it holds the vocabulary that `codebase-improve-architecture`, `codebase-plan-refactor`, and `tdd` all speak. Read it when you need the definitions; those skills carry the process.

## Stopping rule

A reference has no checkpoints, no one-question-at-a-time gate, and no stopping condition of its own — so an agent pointed at it and told to "go" will improvise a process out of the most action-shaped content it can find (usually the parallel design pass in `INTERFACE-DESIGN.md`) and run a long way before asking anything.

When this skill is invoked on its own: state the vocabulary that bears on the question, answer the design question asked, and stop. Reading files, surveying the codebase, and proposing refactors are **not** this skill's work.

- Don't know *which* module to redesign yet? That's `codebase-improve-architecture` — the survey that finds candidates.
- Want the design argued with rather than named? That's `grill-with-docs` or `grill-me`.
- Have a concrete behaviour to build? That's `tdd`.

Run one of those as the driver and let this skill sit underneath it as vocabulary.

## Glossary

Use these terms exactly — don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

**Module**
Anything with an interface and an implementation. Deliberately scale-agnostic — applies equally to a function, class, package, or tier-spanning slice.
_Avoid_: unit, component, service.

**Interface**
Everything a caller must know to use the module correctly. Includes the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.
_Avoid_: API, signature (too narrow — those refer only to the type-level surface).

**Implementation**
What's inside a module — its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**
Leverage at the interface — the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface. A module is **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(from Michael Feathers)_
A place where you can alter behaviour without editing in that place. The *location* at which a module's interface lives. Choosing where to put the seam is its own design decision, distinct from what goes behind it.
_Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**
A concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage**
What callers get from depth. More capability per unit of interface they have to learn. One implementation pays back across N call sites and M tests.

**Locality**
What maintainers get from depth. Change, bugs, knowledge, and verification concentrate at one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```text
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│ Deep Implementation │  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```text
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, the module wasn't hiding anything (it was a pass-through). If complexity reappears across N callers, the module was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Designing for testability

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods means fewer tests; fewer params means simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- **Deepening a cluster given its dependencies** — [DEEPENING.md](DEEPENING.md): dependency categories, seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces** — [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md): design the interface several radically different ways in parallel, then compare on depth, locality, and seam placement.
- **Naming the modules after the domain** — the [domain-modeling](../domain-modeling/) skill owns `CONTEXT.md` and the ADR discipline. A deepened module should be named in the project's ubiquitous language, not invented vocabulary.

## Delegation Map

| User need | Delegate via | Notes |
| :--- | :--- | :--- |
| Find *which* modules to deepen across a codebase | Invoke `codebase-improve-architecture` | This skill supplies its vocabulary; that skill supplies the scan and the grilling loop |
| Turn an agreed deepening into ordered commits | Invoke `codebase-plan-refactor` | Plan first, then implement in tiny steps |
| Put behaviour tests at the new interface | Invoke `tdd` | The interface is the test surface — test through it, not past it |
| The new module needs a domain-accurate name | Invoke `domain-modeling` | Resolve the term, write it to `CONTEXT.md`, then name the module after it |

**Loop eligibility:** false — reference vocabulary, consulted on demand.

> **Host portability:** this skill is pure reference — no host-specific tools. See [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/codebase-design.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
