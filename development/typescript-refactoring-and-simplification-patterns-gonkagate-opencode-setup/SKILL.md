---
name: typescript-refactoring-and-simplification-patterns
description: Simplify and safely refactor existing TypeScript backend code without changing external behavior. Use whenever the task is about reducing local reasoning cost, untangling large handlers, replacing flag or stringly-typed flows with explicit data, moving parsing/validation/narrowing to boundaries, shrinking helper or type indirection, deleting leaky abstractions or dead code, or making an existing TS service easier to change safely, even if the user frames it as "clean this up", "make this less clever", "reduce TS complexity", or "refactor this without changing behavior."
---

# TypeScript Refactoring And Simplification Patterns

## Purpose

Use this skill to simplify existing TypeScript backend code so the next change
is safer and easier, without changing external behavior unless that behavior
change is explicitly separated and named.

This skill owns:

- behavior-preserving refactors on existing code
- smaller local reasoning and clearer readability payoff
- choosing the smallest reversible move that removes accidental complexity
- boundary normalization from untrusted inputs into trusted internal shapes
- control-flow simplification, hidden-state removal, and data-shape clarity
- deleting or shrinking leaky abstractions, dead surface, and needless type
  cleverness

It does not own architecture rewrites, greenfield type modeling, framework
migration, or product behavior changes hidden inside a "cleanup" diff.

## Specialist Stance

Do not spend time restating the common refactor catalog.

Use this as a narrow expert lens for behavior-preserving simplification.

This skill should improve the answer by forcing sharper judgment:

- name the preserved behavior before proposing moves
- separate what is visible in code, tests, config, or call sites from what is
  only inferred
- identify the dominant complexity source before suggesting a rewrite
- choose the smallest reversible move that removes that complexity
- explain the readability payoff in local-reasoning terms, not aesthetic terms
- name the concrete TS or Node technical anchor when the recommendation depends
  on one
- prefer deletion, boundary normalization, and explicit shapes over extra
  helper layers or type machinery
- make assumptions, confidence, and proof obligations explicit
- reject cleanup whose main payoff is "looks cleaner" or "more advanced TS"

If a generic refactoring answer could match that precision and discipline
without this skill, the skill is not doing enough work.

## Differentiation Contract

This skill should beat a generic refactoring answer, not just a generic
cleanup checklist.

Its value is not "more refactoring facts."

Its value is that it reliably makes the answer:

- narrower about seam ownership
- more explicit about what behavior is being preserved
- more honest about observed evidence versus assumption
- more discriminating between the best move and the tempting wrong move
- more explicit about why the chosen move improves local reasoning
- stricter about proof strength versus diff size

If the answer still looks like "here are some solid refactor ideas," the skill
has probably failed.

The answer should instead feel like it came from a specialist who knows exactly
why one move wins here, what makes it safe enough, and why the nearby
alternatives lose.

## Quality Bar

Reject generic refactor-checklist prose.

A good answer from this skill must:

- classify the main problem as one of:
  - `data-shape complexity`
  - `control-flow sprawl`
  - `type or helper complexity`
  - `abstraction leakage`
  - `dead surface`
  - `behavior-risk gap`
- name the external behavior being preserved
- say which claims come from observed code, observed tests, observed config, or
  explicit assumptions
- choose one minimal move or one tight sequence of minimal moves before
  mentioning broader alternatives
- explain why that move improves local reasoning more than the tempting nearby
  alternative
- state the concrete readability payoff:
  - fewer hidden modes
  - fewer branches to hold in mind
  - fewer places where the invariant is reconstructed
  - fewer layers that must be understood together
- surface at least one seam-specific distinction a generic refactoring answer
  would likely leave implicit
- name the exact compiler flag, runtime constraint, or language mechanic when
  the recommendation depends on one
- lower confidence when behavior, tests, runtime assumptions, or effective
  compiler settings are unknown
- reject advice whose real effect is style churn, DRY-for-its-own-sake, or
  cleverness migration
- fail the answer if removing the skill would leave the recommendation
  materially unchanged

If the answer could come from a generic "clean code" article, it is not yet
good enough.

## Scope

- simplifying existing TS backend code while preserving behavior
- `Extract Function`, `Split Phase`, `Remove Flag Argument`,
  `Remove Control Flag`, `Remove Dead Code`, and `Remove Middle Man`
- moving parse, validate, and narrow work to the boundary
- replacing boolean or stringly flows with explicit shapes
- shrinking unnecessary `as`, helper types, deep intersections, or inferred
  complexity when that improves readability
- using mechanical codemods for large repetitive changes when the transform is
  truly behavior-preserving and reviewable

## Relationship To Neighbor Skills

- Use `ts-backend-architect-spec` when the primary win comes from changing
  module, service, or ownership boundaries rather than simplifying existing
  local code.
- Use `typescript-language-core` when the main problem is strict-mode language
  truth, narrowing semantics, or compiler behavior rather than refactor shape.
- Use `typescript-advanced-type-modeling` when the real task is designing a
  richer type model, not reducing existing complexity.
- Use `typescript-runtime-boundary-modeling` when boundary architecture or
  validation strategy is the main question rather than local normalization.
- Use `typescript-public-api-design` when exported surface ergonomics or API
  evolution dominates.

If the task crosses seams, keep this skill focused on simplification and safe
refactor sequencing and hand off the rest explicitly.

## Relationship To Shared Research

Start with the local references in this skill.

Load `references/core-model.md` by default.

Load `references/behavior-preservation-and-proof.md` for every non-trivial
refactor, and immediately when current behavior, side effects, error order, or
async sequencing are part of the risk.

Load `references/hard-technical-anchors.md` when the answer depends on
TypeScript or Node mechanics such as strictness flags, index or optional
semantics, `satisfies` versus `as`, interface versus intersections, Node
type-stripping limits, `node:test`, or codemod safety.

Load `references/high-payoff-moves.md` when choosing among specific refactor
moves.

Load `references/failure-modes.md` when a draft answer may be drifting toward
behavior change, cleverness migration, or seam creep.

Load `references/unfamiliar-codebase-checklist.md` when auditing an unfamiliar
repository or prioritizing where simplification should start.

Load `references/reasoning-pressure-test.md` when the first answer sounds
plausible but generic, when several refactor paths seem defensible, or when you
need to prove the answer is actually stronger than generic refactoring
guidance.

Load
`../_shared-hyperresearch/deep-researches/typescript-refactoring-and-simplification-patterns.md`
only when:

- the codebase is unfamiliar and the local references are not enough
- the answer depends on version-sensitive TS or Node behavior
- the recommendation needs deeper nuance around boundary narrowing, helper
  complexity, or preparatory refactoring
- the task is large enough that the deeper investigation map materially lowers
  risk
- the hard technical anchors are not enough and deeper source-ladder detail is
  needed

Version anchor: TypeScript 5.9 backend code. If the repository depends on
different effective compiler settings or different runtime assumptions, say so
explicitly.

## Input Sufficiency And Confidence

Before answering, identify the missing facts that matter:

- do you have real code or only a problem description?
- do you know current behavior from tests, contract, call sites, or only from
  inferred intent?
- do you know the effective `tsconfig`, or only a guess?
- is the user asking for a concrete refactor, an audit, or just the next safe
  step?

If the repository is available, inspect real code, tests, and config instead
of assuming them.

If preserved behavior is not directly observable, say whether you are
preserving:

- tests
- visible current outputs and side effects
- described intent only

Lower confidence when the preserved behavior is inferred, not observed.

Use `references/behavior-preservation-and-proof.md` when the key uncertainty is
not "which move is elegant?" but "what exactly is safe to preserve and how do
we prove it?"

## Workflow

### 1. Confirm Topic Fit

- make sure the task is existing-code simplification, not architecture rewrite
  or disguised behavior change
- if the real win is outside this seam, hand off explicitly

### 2. Anchor Preserved Behavior

- name the contract you are protecting:
  - outputs
  - side-effect order
  - error behavior
  - important async sequencing when relevant
- say what evidence supports that contract and what remains assumption
- if that evidence is weak, add the smallest proof seam before recommending a
  broader cleanup

### 3. Find The Dominant Complexity Source

Pick the main source of accidental complexity before choosing a move:

- `data shape`
- `control flow`
- `type or helper complexity`
- `abstraction leakage`
- `dead surface`

Do not solve three kinds of complexity at once unless one small move genuinely
shrinks all three.

### 4. Choose The Smallest Winning Move

Prefer, in order:

1. delete dead surface
2. normalize a boundary
3. split phases or extract a local function
4. make hidden states explicit in data
5. remove a leaky or wrong abstraction
6. only then add a new abstraction or helper shape

Keep the move reversible and low-diff whenever possible.

### 5. Compare Against The Tempting Alternative

Force at least one "why not" comparison:

- why not a broader rewrite?
- why not another helper layer?
- why not deeper type machinery?
- why not silence the issue with `as`?
- why not flip a compiler flag immediately?

Accept the move only after explaining why the chosen change improves local
reasoning more directly than the nearby alternative.

### 6. Sequence Safely

- add characterization tests or equivalent proof when current behavior is
  uncertain
- introduce the new shape in parallel when needed
- migrate call sites in small steps
- delete the old path only after the new path is proven

Separate pure refactoring from any real behavior change in both planning and
communication.

### 7. State Payoff, Proof, And Confidence

Close with:

- what became easier to reason about
- what behavior proof is carrying the change
- what result would show the refactor was not actually safe
- what assumptions remain
- your confidence level and why

## Reasoning Obligations

Do not finalize a recommendation until you can answer these explicitly:

1. What behavior is being preserved?
2. What evidence makes that behavior real rather than guessed?
3. What is the dominant accidental-complexity source?
4. What is the smallest move that attacks it?
5. Why does that move beat the most tempting nearby alternative?
6. What concrete readability payoff appears afterward?
7. What could still make this unsafe?

If these answers are missing, the recommendation is probably directionally
right but not yet expert enough.

## Failure Smells

Treat these as red flags:

- behavior drift hidden inside a "rename" or extraction
- reordering side effects or errors in async flows without naming it
- replacing runtime mess with compile-time cleverness
- using `as` to make the compiler quiet instead of simplifying the code
- deleting `undefined` from types without boundary normalization
- adding helpers that reduce text duplication but not reasoning cost
- mixing many unrelated cleanups into one diff
- recommending a big rewrite when one local move would remove the pain sooner

## Deliverable Shape

When giving guidance, structure the answer around these anchors:

- `Preserved Behavior`
- `Behavior Evidence`
- `Observed Complexity`
- `Recommended Minimal Move`
- `Why This Wins`
- `Safety / Proof`
- `Assumptions And Confidence`

If the user asks for implementation steps, add:

- `Incremental Sequence`
- `Rollback Or Stop Signal`

## Escalate When

Escalate instead of pretending certainty when:

- preserved behavior is unclear and there is no safe seam for a small proof
- the real win requires module or service-boundary redesign
- concurrency, transactions, or external side effects make behavior
  preservation ambiguous
- the change depends on a broad config flip with unclear fallout
- multiple valid paths remain and the choice depends on product or ownership
  trade-offs rather than simplification alone
