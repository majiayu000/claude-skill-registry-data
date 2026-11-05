---
name: feature-planner
version: 1.0.1
description: Upstream feature planning — requirement clarification, constraint discovery, design outline, vertical-slice task breakdown ordered by risk. Hands off to grill-with-docs and tdd. Use when starting new feature work from a vague request and no plan exists yet; if a plan or design already exists, use grill-with-docs to stress-test it instead.
---

# Feature Planner

The **first step** in the new-feature pipeline. Turns a vague request into a clarified requirement, a thought-through design, and an ordered list of vertical slices small enough to implement test-first. Hands off to [grill-with-docs](../grill-with-docs/SKILL.md) for stress-testing the plan, then to [tdd](../tdd/SKILL.md) for implementation.

## 1. When to invoke

- User says "I want to build X", "let's add a feature for Y", "I'm starting on Z".
- A request is vague enough that the right *shape* of the work isn't obvious.
- A task is large enough that "just start coding" would lead to mid-flight rework.
- The user explicitly asks for a plan, breakdown, or task list.

If the work fits in one commit and the shape is obvious, **skip planning** and go straight to TDD. Plans pay back when the work is non-trivial.

## 2. The flow

```
Request → Requirement → Constraints → Design outline → Vertical-slice tasks
   ↓          ↓             ↓              ↓                  ↓
"build X"  what + why   what's fixed   shape + risks    ordered, testable
```

Each step is a checkpoint with the user. Don't proceed to the next until the current one is confirmed.

## 3. Requirement clarification

Distill the request into a one-paragraph description of *what* must be true after the work ships, and *why* it's worth shipping. Two paragraphs at most.

Questions to ask before writing the requirement:

- **Who is the user?** A human? Another service? A scheduled job?
- **What outcome do they get?** Phrase as a present-tense fact: "the user can export their order history as CSV", not "we will build a CSV export feature".
- **What's the success criterion?** How does the user (and you) know it's done? A test that fails today and passes when complete.
- **What's explicitly out of scope?** Naming exclusions up front prevents scope creep mid-work.

**Anti-pattern:** writing a requirement that's actually a design ("we'll add a `/export` endpoint that streams CSV from `users.orders`"). That's the design step; the requirement is what the user gets, not how.

## 4. Constraint discovery

Constraints are everything the design must work *within*. Surface them now or they'll surprise you later.

Ask the user (and check the code):

- **Performance** — latency budgets, throughput, payload size limits.
- **Compatibility** — clients on old versions, public API stability, backwards-compatible DB migrations.
- **Security & compliance** — auth requirements, audit trails, PII handling, regulatory rules.
- **Cost** — anything that bills per call (cloud APIs, LLM tokens, queue messages).
- **Existing architecture** — what does this feature have to fit into? Read [CONTEXT.md](../grill-with-docs/CONTEXT.md) for the domain language, check `docs/adr/` for prior decisions ([improve-codebase-architecture §1](../../refactoring/improve-codebase-architecture/SKILL.md#1-glossary)).
- **Team & timeline** — who owns the work, what's the deadline, what's the cost of being late.

Record constraints in the plan, even if they're "no constraint" — explicit nothing beats implicit nothing.

## 5. Design outline

A design outline is **not** a design document. It's a short description of:

- **The shape** — where the new code lives (which module, which layer, which bounded context). Use the vocabulary from [hexagonal-arch](../../design/hexagonal-arch/SKILL.md) and [ddd-architect](../../design/ddd-architect/SKILL.md).
- **The seams** — what new interfaces are introduced, what existing seams are crossed. One new port? One new adapter? An aggregate gains a method?
- **The risks** — the parts you're least sure about. Name them. The first slice in the breakdown will tackle the highest-risk one.
- **The alternatives considered** — what other shapes were possible, and why this one wins. Even a one-line "considered X, picked Y because Z" prevents the next person from re-litigating the choice.

Skip patterns reflexively. The design isn't "Repository + Strategy + Decorator"; it's "the order intake module gains a `cancel()` method, which raises an `OrderCancelled` domain event, which the shipping module consumes." Pattern names are reached for *if and when* they earn it ([design-patterns §5](../../refactoring/design-patterns/SKILL.md#5-decision-rules)).

## 6. Task breakdown — vertical slices ordered by risk

The critical step. Per [tdd's anti-horizontal-slicing rule](../tdd/SKILL.md#anti-pattern-horizontal-slices), break the work into **vertical slices**: each slice delivers one observable behavior end-to-end.

Slice properties:

- **Independently testable.** Each slice can be merged on its own without breaking what already exists.
- **Small.** A slice should fit in one TDD red-green-refactor loop. If it takes a day, it's too big — split.
- **Ordered by risk, not by layer.** The first slice tackles the *most uncertain* part of the design — proving the riskiest assumption first. If the riskiest part can't be made to work, you want to know on day one, not at integration.
- **Ends in a real assertion.** Each slice's success criterion is a test that fails before the slice starts and passes when it's done.

**Wrong (horizontal slicing — common, painful):**

1. Add the database migration.
2. Add the repository code.
3. Add the service code.
4. Add the HTTP handler.
5. Add the tests.

**Right (vertical slicing):**

1. **Tracer bullet:** a stub endpoint returns a hardcoded response; one test passes end-to-end (proves the wire works).
2. **Riskiest assumption:** a single happy-path slice runs the real logic, hits the real DB, returns real data; one test.
3. **Edge case A** — one more test, the smallest amount of code to make it pass.
4. **Edge case B** — same.
5. **N. Refactor the now-duplicated bits** as the third occurrence appears ([logic-cleaner §6](../../refactoring/logic-cleaner/SKILL.md#6-duplication-rule-of-three)).

## 7. Output — the plan deliverable

A plan is a short markdown document or a structured message the user can react to. Shape:

```
# Plan: <feature name>

## Requirement
<one paragraph: who + outcome + success criterion + out-of-scope>

## Constraints
- <constraint or "no constraint">
- ...

## Design outline
- Shape: <module/layer/context>
- New seams: <port, adapter, aggregate method>
- Risks: <ordered, highest first>
- Alternatives: <"considered X, picked Y because Z" — one line each>

## Tasks (vertical slices, in order)
1. <tracer bullet — establishes the wire>
2. <riskiest assumption — proves the design>
3. <edge cases — one per slice>
4. ...
N. <refactor / cleanup as duplication accumulates>
```

Keep it tight. A plan that's longer than the code it describes is over-planning.

## 8. Hand-off

The plan is the input to the next pipeline step:

- **[grill-with-docs](../grill-with-docs/SKILL.md)** — stress-test each decision in the plan with questions. The grilling loop will surface gaps in constraints or risks that weren't obvious during planning.
- **[ddd-architect](../../design/ddd-architect/SKILL.md)** — if the feature shapes the domain (new aggregate, new value object, new domain event), apply DDD discipline now.
- **[hexagonal-arch](../../design/hexagonal-arch/SKILL.md)** — confirm port placement and dependency direction before the first slice.
- **[tdd](../tdd/SKILL.md)** — implement each slice in red-green-refactor; never write all tests first.

When the plan changes mid-implementation (and it will), **re-plan the remaining slices, don't continue with stale ones**. Sunk cost on a slice list is real but tiny compared to the cost of building the wrong thing.

## 9. When NOT to plan

Planning earns its place when the work is non-trivial and the shape isn't obvious. Skip it for:

- **Trivial changes** — a typo fix, a one-line config tweak, a bug fix with a known root cause.
- **Exploratory spikes** — when you're learning whether a thing is possible. Spike, learn, discard, *then* plan the real implementation.
- **Bug fixes with reproductions** — go straight to a failing test, then fix.
- **Pure refactors** — those go through [code-design-refactor](../../refactoring/code-design-refactor/SKILL.md) or [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md).

Forcing a plan onto trivial work makes the planning process feel like ceremony and erodes trust in it. Save plans for when they pay back.

## 10. Cross-skill ties

- [grill-with-docs](../grill-with-docs/SKILL.md) — next step in the pipeline; stress-tests the plan.
- [ddd-architect](../../design/ddd-architect/SKILL.md) — domain-shaping decisions belong here, not in the requirement.
- [hexagonal-arch](../../design/hexagonal-arch/SKILL.md) — seam decisions in the design outline.
- [tdd](../tdd/SKILL.md) — vertical-slice principle inherited from here; implementation follows.
- [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md) — alternative entry point for *refactor* work (not new features); reads the codebase first.
- [logic-cleaner](../../refactoring/logic-cleaner/SKILL.md) — rule-of-three justifies waiting on the refactor slice until duplication is real.
