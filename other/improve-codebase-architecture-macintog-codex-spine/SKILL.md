---
name: improve-codebase-architecture
description: Find evidence-backed simplification, module deepening, terminology, and semantic-symmetry opportunities in a codebase. Use for architecture or refactoring audits, unnecessary architectural complexity, tightly coupled or shallow modules, weak test seams, scattered domain concepts, overloaded names, or sibling workflows whose ownership and transitions drift unexpectedly. Do not use for a narrow fix or an implementation whose architecture is already selected.
---

# Improve Codebase Architecture

Adapted for Codex from Matt Pocock's `improve-codebase-architecture`,
`domain-modeling`, and `codebase-design` skill packets, reviewed at commit
`885e2ca4d842d139e9aef4e48d366c63cb1b8013`.

Use this skill to reduce the effort of using, changing, and diagnosing a codebase. First establish what behavior is needed; then consider removing unnecessary mechanisms or deepening modules that still earn their keep. Fewer files, lines, or entry points alone do not establish an improvement.

## When To Use This Skill

- The user asks to improve architecture, find refactoring opportunities, simplify an overcomplicated design, consolidate modules, or make a codebase easier to test.
- Understanding a concept requires bouncing through many shallow modules.
- Extracted helpers exist mainly for testability, but bugs still live in caller choreography.
- Tightly coupled modules leak details across their seams.
- The repo is hard for agents to navigate because important concepts do not line up with code structure.

## When Not To Use This Skill

- The task is a narrow bug fix, review, or feature request where architecture is not the blocker.
- A repo-local architecture doc, ADR, or skill already gives a stronger task-specific route.
- The user asked for implementation and the architecture direction is already clear.

## Vocabulary

Use these words consistently in architecture suggestions. Full definitions are in [LANGUAGE.md](LANGUAGE.md).

- **Module**: anything with an interface and an implementation.
- **Interface**: everything a caller must know to use the module correctly: types, invariants, ordering, errors, configuration, and performance shape.
- **Implementation**: the code inside a module.
- **Depth**: how much useful behavior sits behind an interface.
- **Seam**: where an interface lives; a place behavior can change without editing in place.
- **Adapter**: a concrete thing satisfying an interface at a seam.
- **Payoff**: what callers and maintainers get from depth.
- **Locality**: how much related behavior can be understood or changed in one place.

## Workflow

1. Bind the review to the selected scope and required behavior.
   - Prefer `PROJECT_CONTINUITY.md`, `CHECKPOINT.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `docs/architecture*`, and repo-local agent docs when they exist.
   - Do not flag missing context or ADR files as a problem.
   - If the repo has a structured code-navigation lane such as `jcode`, use it for symbol, file-outline, and call-site discovery.
   - Identify the need behind the mechanism before optimizing it. Use current callers, requirements, history, and operational evidence to distinguish a necessary constraint from an obsolete assumption. Do not silently relax an explicit user requirement; flag a consequential unresolved choice.
   - Establish the relevant behavior baseline: normal outcomes, failure and recovery paths, and performance or operational constraints that the proposed change could affect. Missing evidence limits the recommendation.
   - Build a small term map from product language to types, state, logs, and user-visible behavior. Flag one concept with several names and one overloaded name used for several concepts.

2. Explore architecture friction.
   - Look for places where one product concept is scattered across many modules.
   - Identify shallow modules whose interface is nearly as complex as their implementation.
   - Apply the deletion test from [LANGUAGE.md](LANGUAGE.md): consider removing the need or mechanism before reorganizing it. Trace the remaining responsibility through callers, configuration, operations, and module internals; a smaller interface can relocate complexity without eliminating it.
   - Compare the current design with the smallest plausible simplification. Deepening can be worthwhile when it contains necessary complexity, but account for added internal state, coupling, and diagnostic burden.
   - Notice where tests cross past the interface into implementation details.
   - Compare sibling modes, states, or pipelines for semantic symmetry. Parallel concepts should use parallel names, owners, transitions, and proof; preserve an asymmetry when domain evidence shows that the concepts genuinely differ.

3. Present candidates.
   - Present only evidence-backed opportunities. Identify the affected code, demonstrated friction, proposed change, and relevant proof; scale detail to the decision.
   - Describe a concrete before/after use, change, or diagnosis that becomes easier. Explain which responsibilities disappear, which move, and what remains necessary; connect locality, depth, or test improvements to that observable payoff.
   - Retain the current design when its burden is justified or the change costs more than it helps. Report insufficient evidence when a material uncertainty prevents judgment; do not manufacture a candidate or a metric.
   - Use project vocabulary for product concepts and this skill's vocabulary for architecture.
   - Name terminology or symmetry evidence only when it changes ownership, interface shape, or verification; do not turn naming consistency into cosmetic churn.
   - If a candidate contradicts an ADR, mention it only when the friction is strong enough to justify reopening that decision.

4. Choose the next action.
   - If the user asked for an audit or exploration, stop with findings and recommendations; selection of a candidate for implementation requires user authority.
   - If the user already authorized audit and in-scope fixes, complete that finite outcome without requiring selection again. Do not turn residual findings into successor work.
   - If the user asked to implement an already chosen direction, continue with the smallest owned change and verify it.
   - If a new module name introduces a durable domain term, update the repo's domain vocabulary only when the repo already has such a surface or the user asks for one.

5. Design the interface when needed.
   - Use [DEEPENING.md](DEEPENING.md) to classify dependencies and testing strategy.
   - Use [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md) when the user wants alternative interface shapes.
   - Verify the affected behavior against the baseline, including relevant failure, recovery, and performance cases. Keep tests at the module interface once the deepened module exists; delete old shallow tests only when replacement coverage proves the same behavior. Preserve diagnostic visibility needed to operate and debug it.

## Output Shape

For an architecture audit with actionable candidates, this is an optional compact shape:

```markdown
1. Candidate name
   Files: ...
   Problem: ...
   Solution: ...
   Benefits: ...
   Proof to gather before editing: ...
```

For implementation, explain the selected simplification or seam and its validation, then patch within scope. A successful review may conclude that no change is warranted.
