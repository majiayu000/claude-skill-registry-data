---
name: architect
description: "Design typed Luau ownership, module boundaries, remotes, state, persistence, and lifecycle before broad or load-bearing Roblox changes. Use for $architect or when skipping design could lock in the wrong shape."
---

# Architect for Roblox

Design before implementation. This is a design gate, not a reason to expand scope. Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md) first. Repository instructions and the current source outrank this skill. Use the contract's Repository mode or Studio fallback mode; never use Roblox Studio MCP playtest controls.

Before delegating or using optional capabilities, read [the runtime contract](../david-mode/references/agent-runtime.md). It owns eligibility, model selection, limits, and fallback.

The selected high-capability parent owns the design, dependency order, and difficult implementation. Delegate source inventories, bounded evidence gathering, routine modules under settled interfaces, and fixtures through the runtime worker policy. Inspect worker artifacts and resolve their questions before accepting a design or implementation unit.

## Choose the depth

Classify the change before doing deep work:

- **Local:** one clear owner, one module, no public/shared API, remote, server-owned state, persistence, replication, lifecycle, or authored-asset boundary. Produce a compact sketch. Skip `$arena`, `$how`, and `$why` unless evidence is missing.
- **Integrated:** crosses two or more modules or services, or changes a public/shared API, remote contract, server-owned state, persistence, replication, lifecycle ownership, or authored assets. Run Ground and Sketch before implementation.
- **Load-bearing:** adds a migration, monetization or purchase path, consequential RNG, security boundary, physics/network ownership, broad refactor, or an irreversible contract. Use Integrated depth, compare whole-shape alternatives, and consider `$arena` or `$interrogate` only when the ambiguity or risk justifies the cost.

## Start

Keep a compact phase checklist so work does not silently skip a design step:

1. Ground
2. Sketch
3. Agree (opt-in)
4. Implement
5. Scrap (only if the shape fails)

Each phase ends only when its completion criterion is met.

## Phase A: Ground the problem

Build an evidence-backed model of every system the change touches.

1. Read applicable repository guidance and design documents. Locate the relevant source, project mappings, tests, remotes, tags, attributes, and authored Instance dependencies.
2. For Integrated or Load-bearing work, run `$how` over the existing subsystem. Run `$why` only when existing ownership or layering rationale is a constraint, contested, or otherwise not recoverable from current code and documents.
3. Trace the caller's request through server authority, validation, mutation, replication, presentation, persistence, retry, cleanup, and failure. Classify each value as persisted, server-runtime, replicated, or client-local state.
4. Use Studio context only when source and repository guidance cannot establish a necessary Instance path, attribute, tag, attachment, constraint, or placement fact. Reuse David Mode's Studio preflight; do not repeat it just to check connectivity.
5. Record evidence paths, assumptions, unresolved product decisions, and the boundary that makes the design load-bearing.

**Ground is complete when:** the entry point, authoritative owner, state lifecycle, trust boundaries, dependencies, and material risks are named with evidence, and any unresolved decision is explicit.

## Phase B: Sketch

Start with the caller's intended usage. Derive the shape from that usage rather than inventing layers first.

1. Write the smallest caller-facing usage example, then the typed Luau state and result shapes, exported function signatures, module map, remote payloads, and authored-Instance contract. Use object-like module shapes only when the codebase already uses them.
2. Assign one owner to every mutation and name the lifecycle for connections, tasks, instances, caches, rounds, characters, players, and servers. Mark persisted, server-runtime, replicated, and client-local data separately.
3. Trace one complete request, including validation, authoritative mutation, replication, presentation, cleanup, retry, and failure. State invariants and make illegal states hard to construct.
4. State mobile CPU/memory, replication, remote-frequency, physics, render, and instance-volume costs. Prefer event-driven and bounded work; name what must be measured rather than guessing.
5. For a Load-bearing or genuinely ambiguous decision, produce at least two structurally distinct candidates. Compare them on ownership clarity, interface depth, security, lifecycle behavior, performance, migration cost, and implementation risk. Compare whole shapes, not point fixes inside one shape. Read [`references/design-red-flags.md`](references/design-red-flags.md) while screening candidates.
6. Use `$arena` only when the user requests a candidate comparison and independent evidence or bounded prototypes can justify the cost. Permission for routine workers is not a request for parallel planning. The parent defines the alternatives and retains the design decision. If it runs, read [`references/runner-prompt.md`](references/runner-prompt.md), require each candidate's rationale from [`references/rationale-template.md`](references/rationale-template.md), and record the synthesis, grafts, rejections, dropouts, and verification. Never run it for a Local change.
7. Prefer the viable design that hides more complexity behind the smallest stable public surface. Recommend one and state the tradeoff; do not enumerate alternatives that do not change a load-bearing decision.

**Sketch is complete when:** another engineer can implement the requested behavior without inventing ownership, types, module boundaries, remote contracts, lifecycle rules, persistence behavior, or verification steps.

## Phase C: Agree (opt-in)

Default: continue directly to implementation when the request includes implementation. For a design-only request, return the design package and stop.

Pause only when the invoker explicitly asks for a checkpoint, such as `$architect with checkpoint` or "stop and show me before implementing." Surface the usage, chosen shape, rejected alternatives, risks, and checks; do not ask for sign-off by default.

Use `$interrogate` only for a contested or high-risk design, or when the user explicitly requests adversarial review. It is a review gate, not a default second opinion. If the user rejects the shape, treat that feedback as Ground evidence and re-ground before sketching again.

## Phase D: Implement against the sketch

Implement only when the request authorizes implementation. Treat the chosen sketch as the contract.

- Build the smallest complete vertical slice in independently verifiable units.
- Surface deviations immediately. A new parameter, owner, escape hatch, cast, optional field, or cross-boundary shortcut means the sketch may be wrong, the requirement may be missing, or the implementation may be overreaching.
- Run the narrowest relevant local checks after each unit, then the repository's authoritative checks. For Rojo projects, run `rojo build`; it validates assembly and serialization, not Luau runtime behavior.
- Use Repository mode when local source and Rojo/project sync are available. When that source path is unavailable, Studio fallback mode may make scoped non-playtest MCP edits to scripts and authored Instances. Inspect before mutating and report exact Studio paths. The user performs Studio playtesting; give them an exact scenario instead of starting, stopping, or controlling a test session.

**Implementation is complete when:** the requested behavior is implemented against the chosen ownership and type contract, each unit has a check, the relevant local verification passes, and remaining user-run Studio validation is concrete.

## Phase E: Scrap when the architecture is wrong

Treat repeated friction as a redesign signal, not a reason to bolt on another exception. Tells include:

- the same ownership workaround appearing in unrelated modules;
- client-supplied values becoming authority through repeated exceptions;
- remotes, services, or callers reaching through an abstraction's internals;
- types needing `any`, casts, escape hatches, or optional fields that are always set;
- cleanup, reconnect, round-reset, or migration branches multiplying around one shape;
- two or more independent implementation deviations with the same cause.

When the pattern appears:

1. Re-run `$how` over what was built and capture the implementation lessons.
2. Redesign from the new constraints as day-one assumptions. `$why` is useful only when the existing rationale still matters.
3. Subtract before adding. The replacement sketch must first become smaller or clearer before it grows.
4. Return to Phase B. Use `$arena` only if its gate is met; never average incompatible candidates.

## Outputs

Return one concise design package, with the caller's usage first:

- scope and depth classification;
- state shapes and invariants;
- ownership and lifecycle map;
- typed Luau signatures and module boundaries;
- remote, replication, persistence, and authored-Instance contracts;
- request/failure path and performance/security costs;
- chosen shape, meaningful alternatives, and rationale;
- implementation order, local checks, and the user's exact Studio test.

For a Local change, keep this to the smallest useful sketch. For Integrated or Load-bearing work, include the full package. Do not create production stub files merely to hold a sketch, and do not implement a design-only request.
