---
name: design-an-interface
description: "Invoked helper skill for unresolved module boundaries, usually called from /write-a-prd. Use to compare multiple interface shapes for a module or component when caller ergonomics and surface area are still unclear. Not for API contract review or already-settled designs."
sources:
  primary:
    - "A Philosophy of Software Design — John Ousterhout"
  secondary:
    - "Designing Web APIs — Jin, Sahni, Shevat"
---

# Design an Interface

Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best. Generate multiple radically different designs, then compare.

## Invocation Position

This is an invoked helper skill. It normally runs from `/write-a-prd` when a module boundary is still unresolved, and it can also support refactor or architecture work when interface tradeoffs are the main uncertainty.

Use it when the open question is the shape of a module interface: method count, surface area, depth, caller ergonomics, or evolvability.

Do not use it when the real uncertainty is the API contract itself — that belongs in `/api-design-review` — or when the work is already clear enough to keep shaping or implementing without a design fork.

## Workflow

### 1. Gather Requirements

Before designing, understand:

- [ ] What problem does this module solve?
- [ ] Who are the callers? (other modules, external users, tests)
- [ ] What are the key operations?
- [ ] Any constraints? (performance, compatibility, existing patterns)
- [ ] What should be hidden inside vs exposed?

Ask: "What does this module need to do? Who will use it?"

### 2. Generate Designs (Parallel Sub-Agents)

Spawn 3+ sub-agents simultaneously using Task tool. Each must produce a **radically different** approach.

```
Prompt template for each sub-agent:

Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [assign a different constraint to each agent]
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from [specific paradigm/library]"

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

### 3. Present Designs

Show each design with:

1. **Interface signature** - types, methods, params
2. **Usage examples** - how callers actually use it in practice
3. **What it hides** - complexity kept internal

Present designs sequentially so user can absorb each approach before comparison.

### 4. Compare Designs

After showing all designs, compare them on:

- **Interface simplicity**: fewer methods, simpler params
- **General-purpose vs specialized**: flexibility vs focus
- **Implementation efficiency**: does shape allow efficient internals?
- **Depth**: small interface hiding significant complexity (good) vs large interface with thin implementation (bad)
- **Ease of correct use** vs **ease of misuse**
- **Evolvability**: can the interface change without breaking consumers, and are error contracts or versioning needs already visible?

Discuss trade-offs in prose, not tables. Highlight where designs diverge most.

### 5. Synthesize

Often the best design combines insights from multiple options. Ask one question at a time:

1. "Which design best fits your primary use case?"
2. "Any elements from other designs worth incorporating?"

## Evaluation Criteria

From "A Philosophy of Software Design":

**Interface simplicity**: Fewer methods, simpler params = easier to learn and use correctly.

**General-purpose**: Can handle future use cases without changes. But beware over-generalization.

**Implementation efficiency**: Does interface shape allow efficient implementation? Or force awkward internals?

**Depth**: Small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (avoid).

**Evolvability**: Prefer interfaces that can absorb likely future change without forcing broad consumer breakage. If failure modes or versioning pressure are already obvious, evaluate them as part of the design rather than as an afterthought.

## Anti-Patterns

- Don't let sub-agents produce similar designs - enforce radical difference
- Don't skip comparison - the value is in contrast
- Don't implement - this is purely about interface shape
- Don't evaluate based on implementation effort

## Handoff

- **Expected input:** a concrete module problem with multiple plausible interface shapes
- **Produces:** contrasted interface options plus a recommendation or synthesis direction
- **Usually invoked by:** `/write-a-prd`, or occasionally refactor and architecture side-route skills
- **Returns control to:** the calling skill so shaping, refactor planning, or implementation can continue with a chosen interface
