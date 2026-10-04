---
name: design-an-interface
description: Generate multiple radically different interface designs before implementation. Use when designing an API, module boundary, command surface, data contract, or when the user says "design it twice".
---

# design-an-interface

Design an interface before building it. This skill adapts the "Design It Twice" practice from *A Philosophy of Software Design*: the first plausible interface is rarely the best one, so produce several different shapes, compare them, and synthesize a recommendation.

This is a design-only workflow. Do not edit implementation files, add tests, or scaffold code while using this skill unless the user explicitly starts a separate implementation task.

## When to use

- A user asks to design an API, module, CLI, protocol, data shape, hook, component props interface, or agent contract.
- A Beads issue or alignment document calls for interface design before coding.
- The current implementation path feels unclear because multiple public shapes could work.
- The user mentions "design it twice" or asks for alternatives/trade-offs.

## Context first

Before proposing designs, load the smallest useful set of harness context:

1. Read any task-specific alignment document in `.tmp/work/`.
2. Inspect the relevant Beads issue with `bd show <id>` and note acceptance criteria, parent context, blockers, and scope limits.
3. Read `knowledge/_shared.yaml` plus the relevant `knowledge/repos/<repo>.yaml` when the design touches a known repo.
4. Check existing patterns before inventing a new shape: nearby interfaces, exported types, commands, hooks, components, and prior plan artifacts.
5. If a contract file exists, treat it as authoritative. Do not rename exports, reorder parameters, or widen scope without calling out a deviation.

Ask clarifying questions only when a blocker prevents meaningful design work. Otherwise, state assumptions and continue.

## Workflow

### 1. Gather requirements

Identify:

- What problem the interface solves.
- Who the callers are: humans, scripts, tests, modules, subagents, external systems.
- The key operations and the minimum data each operation needs.
- Compatibility, performance, security, persistence, and rollout constraints.
- What complexity should be hidden inside versus exposed to callers.
- How success will be verified: tests, acceptance criteria, evaluator rubric, or manual review.

Use this prompt when requirements are missing:

```text
What does this interface need to let callers do, who will call it, and what should remain hidden behind the boundary?
```

### 2. Generate 3+ radically different designs

Create at least three alternatives with meaningfully different public shapes. Different names for the same method set do not count.

Use parallel subagents when they are available and appropriate for the environment. If subagents are unavailable, generate the alternatives yourself as separate passes and keep each pass anchored to a distinct design constraint.

Suggested constraints:

- Minimal surface: 1-3 operations, narrow caller choices.
- Flexible surface: composable primitives for many workflows.
- Common-case surface: optimized for the path most callers will use.
- Declarative surface: caller describes desired outcome, implementation chooses steps.
- Protocol/object surface: lifecycle, state, or streaming modeled explicitly.
- Existing-pattern surface: mirrors a local convention or well-known library.

Subagent prompt template:

```text
Design an interface for: <module or boundary>

Requirements:
<requirements and constraints>

Existing context:
<Beads issue, alignment scope, knowledge notes, relevant local patterns>

Design constraint for this pass:
<one distinct constraint>

Return:
1. Interface signature or command/data shape
2. Usage example from a realistic caller
3. Complexity hidden behind the interface
4. Trade-offs and failure modes
5. Verification implications

Do not implement the interface.
```

### 3. Present designs sequentially

Show each design on its own before comparing them so the user can absorb the shape.

For each design include:

- Interface signature, command surface, or data contract.
- A short realistic usage example.
- What the design hides internally.
- What the caller must understand.
- Trade-offs, including likely test and migration impact.

### 4. Compare in prose

Compare the alternatives using these criteria:

- **Interface simplicity**: fewer concepts, methods, parameters, and special cases.
- **General-purpose shape**: enough flexibility for likely future use without over-generalizing.
- **Implementation efficiency**: whether the shape permits efficient internals or forces awkward workarounds.
- **Depth**: a small interface hiding meaningful complexity is better than a broad shallow wrapper.
- **Ease of correct use vs misuse**: the best design nudges callers toward valid states and makes invalid states hard to express.

Use prose instead of a large table unless the user asks for a matrix. Highlight the points where designs diverge most.

### 5. Synthesize and stop

Recommend one design or a small synthesis of multiple designs. Explain why it fits the requirements and where it intentionally rejects other options.

End with:

- Recommended interface shape.
- Key trade-offs accepted.
- Open questions or risks.
- Verification plan for a future implementation task.

Stop at the design recommendation. If implementation should proceed, create or update Beads work separately and follow the normal coding workflow.

## Evaluation criteria

Good interface designs:

- Minimize caller-facing concepts without hiding necessary control.
- Make the common path obvious and the wrong path difficult.
- Keep stable contracts small while allowing internals to evolve.
- Reflect existing repo conventions unless there is a clear reason to diverge.
- Preserve acceptance criteria and contract requirements from Beads or alignment docs.

## Anti-patterns

- Producing three variants of the same design.
- Skipping Beads, alignment, knowledge, or existing-pattern context.
- Choosing the easiest implementation when the caller-facing shape is weaker.
- Treating comparison as a checklist instead of reasoning through trade-offs.
- Implementing, scaffolding, or changing production code during the design workflow.
