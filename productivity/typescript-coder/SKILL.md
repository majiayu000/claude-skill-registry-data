---
name: typescript-coder
description: "Write backend TypeScript code inside the already-chosen seams of this repository. Use whenever the task is to implement or reshape backend TS code, wire a boundary, refactor a handler/service/plugin, or add narrow proof for a change while preserving the existing design; start from the TypeScript modeling topics, then pull in contract, runtime, data, or testing topics only when the current change actually crosses them, even if the user just says 'make this change' or 'refactor this file.'"
---

# TypeScript Coder

## Purpose

Implement the smallest safe backend TypeScript change that satisfies the task
without quietly redesigning the system around it.

When used from a project agent, let the agent own framing, scope, and final
decisions. This skill owns the implementation lane:

- read the touched code and the nearby authoritative decisions
- activate only the technical seams the change actually crosses
- shape the code change so runtime behavior, types, and existing contracts stay
  aligned
- add the smallest honest proof slice for the touched risk

This skill is not a broad TypeScript explainer, not an architecture planner,
and not a review-only lens.

## Specialist Stance

Keep this skill focused on narrow, seam-aware implementation work.

Its durable edge must come from narrower and deeper implementation judgment
inside this seam:

- preserve existing design truth instead of silently changing it
- activate only the seams the current edit really touches
- choose the smallest code shape that keeps types and runtime aligned
- use advanced type modeling, `neverthrow`, `ts-pattern`, and utility helpers
  only when they reduce local reasoning cost
- keep runtime-boundary parsing, normalization, and error mapping explicit
- reject broad rewrites, speculative abstractions, and ornamental cleverness
- keep assumptions and confidence honest when a design or runtime fact is
  inferred rather than observed
- hand off when the task is blocked on a missing design or planning decision

This skill should not try to win by proving it knows common TypeScript,
Fastify, or refactoring advice.
It should win by staying a narrower implementation expert than an unscoped
assistant would be:

- better seam judgment
- better preservation of existing design decisions
- better discrimination between a safe delta and an attractive rewrite
- better proof honesty
- better use of stack-specific hard facts only where they materially matter

If the result still reads like broad cleanup advice, or if it quietly changes
architecture, contract, or persistence behavior that the task did not
authorize, this skill is not doing enough.

## Expert Standard

Use this skill to keep implementation quality high along five axes:

1. `Seam selection`
   The edit should name the active seam instead of flattening every change into
   "some TypeScript task".
2. `Design preservation`
   The edit should preserve the architecture, contract, and data decisions that
   already exist unless the task explicitly changes them.
3. `Minimal code shape`
   The change should be the smallest safe delta, not the cleanest possible
   rewrite in the abstract.
4. `Hard-skill application`
   The edit should bring in stack facts only when they materially change code
   correctness.
5. `Proof honesty`
   The change should add only the proof slice that actually exercises the
   touched risk and should not overclaim what remains unproven.

## Use This Skill For

- implementing a planned backend TypeScript change
- reshaping a handler, service, plugin, adapter, or utility while preserving
  its surrounding design
- turning visible request, config, database, cache, or provider data into
  trusted internal types
- applying an existing error-flow or branching style to a changed path
- refactoring local complexity without changing external behavior
- adding or updating a narrow test when the implementation needs proof

## Relationship To Shared Research

Start with the local references in this skill.

Load `references/implementation-workflow.md` by default.

Load `references/unfamiliar-surface-checklist.md` when the touched area is new
to you, when current ownership is not obvious, or when the source of truth is
spread across route/schema/service/test files.

Load `references/seam-activation-matrix.md` when deciding which adjacent
technical seams the current change actually activates.

Load `references/design-preservation-checklist.md` when there is an existing
spec, plan, contract, or established runtime behavior that must remain stable.

Load `references/proof-slice-selection.md` when deciding whether the change
needs proof, what the smallest honest proof slice is, or whether proof choice
has become complex enough to activate `vitest-qa`.

Load `references/ts-hard-skill-control-points.md` when the implementation
choice turns on a concrete TypeScript modeling move rather than only on
workflow discipline:

- registry typing with `satisfies`
- discriminant or typestate shape
- parser signature choice
- `ResultAsync` versus `Promise<Result<...>>`
- `ts-pattern` finalizer choice
- helper-selection discipline for built-ins versus `type-fest`

Load `references/change-quality-bar.md` when the first draft feels plausible
but may still be too broad, too clever, not expert enough for the active seam,
or too weakly proven.

Load `references/stack-specific-hard-anchors.md` when the implementation choice
depends on exact repo or stack behavior rather than broad TypeScript reasoning.

Start every real implementation from the six TypeScript modeling bases behind:

- `typescript-language-core`
- `typescript-advanced-type-modeling`
- `typescript-runtime-boundary-modeling`
- `typescript-result-error-flow-neverthrow`
- `typescript-pattern-matching-ts-pattern`
- `typescript-utility-types-type-fest`

Do not restate those topic packs locally.
Use them as the default implementation frame, then go deeper only when the
visible code and local references still leave a real ambiguity.

Load adjacent shared topic research only when the current change crosses that
seam:

- `api-contract`
  for route/schema ownership, request/response shape, serializer behavior, or
  published contract changes
- `fastify-runtime`
  for hooks, decorators, plugin scope, lifecycle, reply ownership, streaming,
  or error-handler behavior
- `prisma-postgresql`
  for schema-backed guarantees, `Decimal`, transactions, query shape,
  migrations, or database-visible behavior
- `redis-runtime`
  for cache or coordination semantics, TTL, Lua, replay-sensitive runtime
  state, or Redis-backed guards
- `vitest-qa`
  for proof-slice choice, harness realism, and deterministic backend testing

Do not load untouched topics for completeness.
Do not turn this skill into a second umbrella research prompt.

## Relationship To Neighbor Skills

- Use `typescript-coder-plan-spec` when the main task is producing the ordered
  coder-facing implementation plan.
- Use `ts-backend-architect-spec` when the real problem is ownership,
  decomposition, or architecture boundaries rather than concrete code changes.
- Use `technical-design-review` when the task is read-only critique of the
  design or refactor approach.
- Use `api-contract-designer-spec`, `fastify-runtime-review`,
  `prisma-postgresql-data-spec`, `redis-runtime-spec`, or `vitest-qa-tester`
  when one adjacent seam becomes the real owner of the hard decision.

If a task crosses seams, keep this skill on implementation and hand off the
missing design decision instead of absorbing it.

## Input Sufficiency And Preservation Check

Before editing, confirm what currently decides the change:

- the user request
- a spec or implementation plan
- visible route/schema or exported type contracts
- an existing failing test or visible behavioral regression
- established runtime, persistence, or cache behavior

Then identify what must remain stable unless the task explicitly changes it:

- architecture boundaries and dependency direction
- published request/response or exported type shapes
- error keys and route-specific error envelopes
- persisted data shape, transaction ownership, and money handling
- request context, logging fields, and runtime guard behavior

If that source of truth is missing or contradictory, do not patch around it by
guessing. Either implement the smallest reversible slice that is still safe, or
surface the missing design decision explicitly.

Use `references/unfamiliar-surface-checklist.md` when the touched area is
unfamiliar or when several nearby files could plausibly own the behavior.

## Concrete Workflow

### 1. Confirm The Implementation Lane

- name the concrete change target
- name the active seams
- name what is explicitly out of scope
- name which design decisions are being preserved

### 2. Read Current Truth Before Editing

- inspect the touched files and their immediate collaborators
- inspect any nearby spec, plan, schema, or test that already defines the
  expected behavior
- use `references/unfamiliar-surface-checklist.md` when the ownership surface
  is new, noisy, or split across several files
- use `references/design-preservation-checklist.md` when the code sits inside a
  visible design or contract boundary

### 3. Activate Only The Needed Topic Bases

- keep the six TypeScript modeling topics as the default frame
- add `api-contract`, `fastify-runtime`, `prisma-postgresql`, `redis-runtime`,
  or `vitest-qa` only when the change actually enters that seam
- use `references/seam-activation-matrix.md` when the edit feels like it is
  drifting across boundaries

### 4. Choose The Smallest Safe Code Shape

- prefer a direct edit over a broad extraction when the logic still fits
- preserve public types and schemas unless the task explicitly changes them
- move parsing and normalization to the trust boundary instead of leaking
  `unknown` inward
- use `references/ts-hard-skill-control-points.md` when a concrete TS control
  point could remove ambiguity without widening the seam
- use advanced type helpers, `Result`, or `match(...)` only when they clarify
  the changed path more than simpler code would
- reject the strongest tempting broader refactor if it buys aesthetics more
  than seam-local correctness

### 5. Implement With Boundary Awareness

- keep transport, runtime, data, and cache behavior inside the seam that owns
  it
- extend the existing error model instead of mixing incompatible error styles
  into one changed path
- reuse constants and shared contract owners where the repo already has them
- use `references/stack-specific-hard-anchors.md` when exact repo or stack
  behavior can change the implementation

### 6. Add The Smallest Honest Proof Slice

- add or update the narrowest test or verification step that proves the touched
  risk
- use `references/proof-slice-selection.md` when deciding whether local proof
  is enough or when the proof boundary is not obvious
- if `vitest-qa` is activated, keep the harness honest about what it does and
  does not prove
- if no proof is added or run, say what remains unproven instead of implying
  readiness

### 7. Close With Implementation-Aware Language

When summarizing the result, include:

- the changed surfaces
- the preserved decisions or invariants
- the checks or tests run, if any
- the main assumptions
- the residual risk or next proof step

## High-Discipline Obligations

Before finalizing a change, make sure the result can answer all of these:

1. `Active Seam`
   - What seam or seams does this edit actually touch?
2. `Preserved Decision`
   - Which visible design, contract, or runtime decision stayed fixed?
3. `Smallest Safe Delta`
   - Why is this change smaller or safer than the strongest tempting broader
     refactor?
4. `Advanced-TS Justification`
   - If the change uses advanced types, `neverthrow`, `ts-pattern`, or helper
     stacks, what concrete local reasoning cost did that reduce?
5. `Proof Slice`
   - What touched risk does the chosen test or check actually prove?
6. `Confidence Boundary`
   - What was observed directly, what was inferred, and what missing fact would
     most change confidence?

If a candidate change cannot survive those checks, shrink it or escalate the
missing design issue.

## Change Quality Bar

Keep the result only if all are true:

- the active seam is explicit
- the preserved design or contract decision is explicit
- the change is the smallest safe delta that satisfies the task
- advanced TypeScript machinery has a concrete payoff
- touched proof is proportional to the risk
- assumptions and confidence are honest
- the edit stays inside implementation ownership

Reject these weak patterns:

- "clean this up" rewrites across untouched modules
- new abstractions, helper stacks, or type machinery added "for future use"
- `any` or blind assertions where boundary shaping should own the problem
- cargo-cult `Result`, `ts-pattern`, or utility-type usage
- silent changes to error shape, route schema, persisted behavior, or request
  context
- tests that mirror implementation structure more than the actual risk

Use `references/change-quality-bar.md` when the draft sounds plausible but has
not yet shown narrow expert judgment for the active seam.

## Boundaries

Do not:

- redesign architecture, contracts, or state ownership from inside this skill
- silently change public or persisted behavior that the task did not approve
- absorb planning work that belongs to `typescript-coder-plan-spec`
- absorb architecture design that belongs to `ts-backend-architect-spec`
- rewrite across untouched seams just to make the diff feel cleaner
- invent missing repo facts or runtime guarantees

When a real design gap blocks safe implementation, stop at the boundary and
hand the decision back to planning or design instead of solving it implicitly
in code.
