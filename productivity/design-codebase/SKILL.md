---
name: design-codebase
description: Use when the user asks to make or compare a codebase architecture decision involving module boundaries, ownership, interfaces, seams, adapters, domain language, or a throwaway prototype that answers a design question. Also use during implementation only when a non-obvious architecture, ownership, interface, or dependency-boundary decision blocks the next safe edit; a testability concern qualifies only when it demonstrates that kind of boundary pressure. Do not use for ordinary code explanation, straightforward implementation, general test design, flaky tests, mocks, regression coverage, or implementation of an already selected design.
---

# Design Codebase

Use architecture language to improve leverage, locality, and testability without turning ordinary implementation into a design ceremony.

## First Decision

- If the user asks for a small bug fix or ordinary implementation and existing patterns make the next safe edit clear, stay in the lightweight development flow.
- If an implementation depends on a non-obvious architecture, ownership, interface, or dependency-boundary decision that existing patterns cannot safely settle, use this workflow to resolve that decision.
- If the user asks where an interface or seam should live, inspect the directly affected callers, dependencies, tests, and constraints first. If material evidence for the decision is unavailable or cannot be inspected, name the missing evidence and request only the minimum input needed; do not present generic architecture guidance as an established project conclusion.
- If a testability concern is primarily about test level, fixtures, mocks, timing, regression signal, or acceptance proof, use `test-strategy` when it is installed, available, and applicable; otherwise preserve the host's existing testing method. If it exposes an unresolved ownership, dependency, interface, or architecture boundary, resolve that design question here first, then hand any remaining test-design decision to `test-strategy` when it is installed, available, and applicable; otherwise preserve the host's existing testing method.
- If the user asks to improve architecture, identify the actual design pressure before choosing lenses such as shallow modules or leakage across seams.
- If runnable feedback is the fastest way to settle a design question, read [prototypes.md](references/prototypes.md) and apply its automatic-local versus approval-required gate.
- If broad planning is the real task, use `plan-work` only when it is installed, available, and applicable; otherwise preserve the host's existing planning method.
- When a request includes both an unresolved architecture boundary and rollout concerns such as migration, compatibility, sequencing, or scope, resolve the architecture boundary first, then plan the work that depends on that decision.

## Design Runbook

When this skill is active, drive the design pass in this order:

1. Read the directly affected callers, dependencies, tests, operational constraints, and any directly relevant docs before proposing structure. If material evidence is unavailable or cannot be inspected, stop project-specific recommendation, identify the missing evidence, and request only what is needed to continue. Stop broadening the design read once the decision can be made safely.
2. State the exact design decision and goal in one sentence.
3. Derive only the criteria that matter for this decision, such as compatibility, locality, operational simplicity, performance, ownership, failure isolation, testability, migration cost, and reversibility.
4. Identify the current design pressure without assuming it is a seam, adapter, or module-depth problem.
5. Compare the smallest useful set of materially distinct options against the derived criteria when the answer is non-obvious.
6. Recommend one option that best fits the current project and change pressure, then call out migration impact, verification approach, and what should stay out of scope.

## Vocabulary

Use these terms consistently:

- **Module**: anything with an interface and implementation.
- **Interface**: everything callers must know to use the module correctly, including invariants, ordering, errors, configuration, and performance.
- **Implementation**: what lives behind the interface.
- **Seam**: the place where behavior can vary without editing callers.
- **Adapter**: a concrete implementation that satisfies an interface at a seam.
- **Depth**: leverage at the interface; deep modules hide useful behavior behind a small surface.
- **Locality**: changes, bugs, and tests concentrate in one place.

## Design Checks

- Existing project architecture and explicit user constraints outrank the vocabulary and heuristics in this skill.
- Treat deep-module, seam, adapter, and interface-leakage checks as lenses only when caller complexity, duplicated coordination, or a real dependency boundary demonstrates that pressure.
- Introduce an interface, adapter, or seam only when demonstrated variation, ownership, testability, operational isolation, or an external dependency boundary justifies it; do not add one merely because this skill is active. Adapter count alone does not determine whether a seam is real.

Use these checks to support the runbook rather than replace it:

- Deletion test: if deleting the module makes complexity vanish, it was probably shallow. If complexity spreads across callers, it was earning its interface.
- Interface test surface: callers and tests should cross the same seam.
- Dependency fit: pure or local-substitutable dependencies can usually sit behind the module; remote or external dependencies may need ports/adapters.
- Scope fit: improve the architecture needed for the current goal; avoid unrelated broad refactors.

## References

- Read [deep-modules.md](references/deep-modules.md) when caller complexity, duplicated coordination, or interface leakage may indicate a shallow module.
- Read [deepening.md](references/deepening.md) when consolidating shallow modules or deciding where a demonstrated seam belongs.
- Read [api-and-interface-design.md](references/api-and-interface-design.md) when a consumer-visible API, service boundary, or interface contract needs explicit input/output, error, boundary-validation, or compatibility criteria.
- Read [design-it-twice.md](references/design-it-twice.md) when the decision is non-obvious enough to compare materially distinct interface options.
- Read [domain-modeling.md](references/domain-modeling.md) when the architecture decision depends on domain terminology, glossary work, or recording an ADR.
- Read [prototypes.md](references/prototypes.md) only when runnable feedback is the fastest discriminating method for the active design question.

## Exit To Implementation

- When a request includes implementation, treat design as a transient internal phase: once the design choice is settled, exit to implementation automatically unless user-only input, an irreversible trade-off, or a scope change remains.
- When the user asks only to design, do not implement until they ask.
- Do not keep comparing architecture alternatives during implementation unless the selected design becomes concretely invalid.
- Verify the implementation against the settled interface and invariants rather than reopening the design discussion.

## Boundaries

Do not automatically create glossary files, domain-context files, ADRs, architecture reports, HTML files, subagent workflows, or broad refactors. Follow [prototypes.md](references/prototypes.md) for the only automatic-prototype exception.

Only create durable design artifacts when the user asks, or when a hard-to-reverse and surprising trade-off has been explicitly chosen and the user agrees it should be recorded.
