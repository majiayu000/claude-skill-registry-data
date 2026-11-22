---
name: semantic-growth-seed
description: "Use when a task needs Functional Semantic Growth: review abstraction, clarify vague requirements, bootstrap semantic docs, map model to code, create FormularDefTree/, write Quint-style semantic kernels, find the best existing abstraction, and bridge model to code with scenarios, typed IR, validation, and review."
---

# Semantic Growth Seed

`semantic-growth-seed` helps a project grow its own `FormularDefTree/`.

## Root Rule

```text
Evidence first, not implementation authority.
Design D comes from parent contract, user goal, or scenarios.
Implementation I comes from the observed snapshot.
Gap(D, I) is allowed and must be explicit.
Validate proportionally to risk.
Keep project facts in FormularDefTree/.
Prefer unambiguous formulars over prose.
```

Core gaps:

```text
G1 Reality Gap:      user intent <-> real-world need
G2 Understanding Gap: user expression -> agent model
G3 Realization Gap:   agent model -> implementation / behavior
```

Loop:

```text
Evidence -> Candidate Need/Model -> Scenario -> User Judgment -> Refine -> Realize -> Observe -> Evidence
```

User expression is lossy, partial, and context-dependent evidence. Infer the
latent need, then validate it with user-checkable scenarios before treating it
as a model constraint.

## Trigger

```text
existing project/module -> legacy_as_is
ambiguous intent        -> scenario_oracle
need better abstraction -> model_abstraction
concept changed         -> semantic_change
model-to-code risk      -> model_to_code
tree layout/template     -> storage_schema
```

If more than one applies, start from the earliest gap:

```text
real-world need -> user language -> agent model -> code implementation
```

## Quick Procedure

```text
1. Classify the task into one trigger.
2. Read references/tree.yml, then only references/nodes/<trigger>/node.md.
3. If project `FormularDefTree/tree.yml` exists, read only relevant project nodes.
4. Check the tree repository snapshot metadata before trusting implementation evidence.
5. Produce the minimal artifact for that trigger.
6. Validate against the trigger node's Output Format, Procedure, and Invariants; record conclusions in task notes or project tree.
```

## Tree Rule

Read the skill reference node first. Then, if project `FormularDefTree/tree.yml`
exists, read/update only relevant project nodes.

The project tree is `FormularDefTree/`.

If no project tree exists, create a project tree only
when the user goal needs persistent semantic docs or the trigger is
`legacy_as_is` / `storage_schema`. Otherwise record conclusions in task notes.

For tree initialization, use `assets/FormularDefTree-template/` as the starter layout.

## Compositional Tree Rule

```text
Each node is a self-contained local formular.
Parent node: motivation, scope, invariants, and allowed refinement space.
Child node: local model for the smallest relevant module/feature.
Child must state Parent Contract and Refinement To Parent.
Validate locally first; escalate only when parent invariants break.
```

## Formular Rule

For nontrivial modules, a node should be a comparable pair of formulars, not a
module prose summary:

```text
Design Formular D:
  abstract input/state/event -> abstract state/output/error

Implementation Formular I:
  concrete input/state/event -> concrete state/output/error

Refinement Map alpha/beta:
  alpha(concrete_state/input/event) = abstract_state/input/event
  beta(concrete_output/error) = abstract_output/error
  beta_result(concrete_state/output/error) = abstract_state/output/error

Obligation:
  beta_result(I(x, s, e)) refines D(alpha(x), alpha(s), alpha(e))
```

`Design Formular` captures intended semantics from the parent contract, current
spec, or user-approved target. `Implementation Formular` captures the current
observed code behavior at the recorded repository snapshot. If no target exists
yet, record only the observed implementation formular and mark the design formular
as unknown or candidate.

`Design Formular` may be cleaner, stronger, or different from current
implementation. Implementation mechanisms must not appear in `Design Formular`
unless required by the parent contract or user-approved target. If a design
mentions a helper, file, class, staging trick, or current call sequence, justify
why that term is semantic; otherwise move it to `Implementation Formular` or
`Gap(D, I)`.

Use prose only to explain the formular, not to replace it.

## Quint-Style Kernel Rule

Before writing Design/Implementation Formulars for a nontrivial node, model the
node as a small language or semantic system using Quint-style state-machine
notation. The default artifact is a Markdown `quint-pseudo` block, not a real
`.qnt` file.

Unless explicitly labeled otherwise, the kernel is the Design kernel. An
implementation-specific kernel must be labeled as such, and any mismatch belongs
in `Gap(D, I)`.

Use real executable Quint only when the user explicitly asks for a `.qnt`
model, model checking, or executable formal validation. Do not create `.qnt`
files or run Quint merely because a node is complex.

Every `quint-pseudo` kernel must be state-machine shaped:

```quint-pseudo
module <node_name> {
  type Evidence = ...
  type Event = ...
  type State = ...
  type Effect = ...
  type Error = ...
  type Obs = ...

  pure def obs(s: State): Obs = ...

  action step(s: State, e: Event):
    Either[(State, Effect), Error] = ...

  pure def inv(s: State): bool = ...

  // Optional named actions may refine step:
  action <name>(s: State, args...):
    Either[(State, Effect), Error] = ...
}
```

The kernel must make these parts explicit:

```text
Evidence:
  input alphabet, grammar, event shape, trace, or evidence accepted by the node.

Event:
  the typed event(s) that drive the state machine.

State:
  the smallest abstract state and values needed to explain behavior.

Effect:
  externally relevant side effects or publications.

Error:
  failed transition result and whether state is unchanged, invalidated,
  committed, or recoverable.

Observation:
  obs : State -> Observable.

Transition:
  step : State x Event -> State' x Effect | Error.

Invariants:
  equations or predicates preserved by valid transitions.

Equivalence / Refinement:
  what counts as same behavior, stronger behavior, or invalid behavior.

Counterexample Shape:
  smallest trace, state, or relation instance that would falsify the node.
```

This is a writing discipline, not extra ceremony. It keeps the node closer to
Quint/TLA-style operational semantics, algebraic data types, equations, and
refinement maps than to module/class prose. Prose may explain motivation,
scope, and interpretation, but prose must not define transition semantics when
they can be expressed by the kernel.

## Precision Rule

Prefer compact unambiguous forms:

```text
function signatures
state variables
event alphabets
transition tables
relations
invariants
pre/postconditions
refinement equations
```

Use prose to state motivation, scope, and interpretation. Do not let prose
stand in for the actual formular when the behavior can be expressed as a
function, relation, state machine, or table.

## Snapshot Rule

Every project `FormularDefTree/` must say which repository snapshot its current
implementation formulars describe. Default to one tree-level snapshot; do not
duplicate commit metadata in every node.

```text
tree.yml:
  repositories:
    <repo-id>:
      path: <relative-or-absolute-path>
      commit: <git sha or unknown>
      branch: <branch or unknown>
      dirty: true|false|unknown
      captured_at: <YYYY-MM-DD HH:MM TZ>
```

Each node that maps to code should list only its snapshot scope:

```text
snapshot_scope:
  repo: <repo-id>
  paths:
    - <code-or-doc-path>
  status: current|needs_catchup|stale|unknown
```

Node-level commit metadata is only needed for an explicit exception, such as a
node describing a different repository, a vendored dependency snapshot, or a
historical comparison. When code changes materially, update the tree-level
snapshot and either update affected implementation formulars or mark affected
nodes `needs_catchup`.

Do not use stale implementation formulars to make correctness claims.

## Tool Rule

```text
Agent owns the abstraction. Tools only check local hard cases after a candidate model exists.
Each node chooses the lightest sufficient validation and records the reason.
Validation modes:
  none/examples/review: simple local definitions.
  property tests: generated boundary inputs and implementation conformance.
  harness: code behavior must refine the model.
Formal tools:
  Alloy: finite relational structure, ownership, uniqueness, and coverage.
  Quint: state transitions, traces, replay, recovery, and temporal invariants.
Do not run formal tools when scenarios and review are enough.
Do not create real `.qnt` files or run Quint unless the user explicitly asks
for executable Quint modeling or validation. Default to `quint-pseudo` kernels
inside Markdown.
```

## Node Rule

```text
Motivation
-> Snapshot Scope
-> Parent Contract
-> Quint-Style Kernel
-> Design Formular
-> Implementation Formular
-> Refinement Map
-> Gap(D, I) / Known Non-Refinements / Debt
-> Validation
-> Evolution Log
```

## Artifact Rule

```text
existing code -> Implementation Formular + tree snapshot + node snapshot scope
unclear intent -> 2-4 scenarios
weak abstraction -> Quint-Style Kernel + Design Formular + selected kernel
model-to-code risk -> Refinement Map + bridge spec + typed IR + tests/harness/review
tree layout/template -> initialize/update from assets/FormularDefTree-template/
```

If discussing only, record conclusions in task notes or the project tree.
