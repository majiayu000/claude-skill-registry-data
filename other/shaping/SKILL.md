---
name: shaping
description: Shape Up methodology for product and feature development. Use when collaboratively shaping a solution — iterating on problem definition (requirements) and solution options (shapes), breadboarding systems into affordances and wiring, and slicing into vertical implementation increments. Triggers include "shape this feature", "breadboard the system", "let's shape", "slice this into increments", "fit check", "define requirements", or any product/feature scoping discussion using Shape Up methodology.
---

# Shaping & Breadboarding

Structured methodology for defining problems, exploring solutions, and planning implementation. Based on [Shape Up](https://basecamp.com/shapeup) adapted for working with an LLM.

Source: [rjs/shaping-skills](https://github.com/rjs/shaping-skills) by [@rjs](https://github.com/rjs) (Ryan Singer, author of [Shape Up](https://basecamp.com/shapeup))

## Two Skills in One

**Shaping** — Iterate on problem (requirements) and solution (shapes) before committing to implementation. Separates what you need from how you might build it, with fit checks to see what's solved and what isn't.

**Breadboarding** — Map a system into UI affordances, code affordances, and wiring. Shows what users can do and how it works underneath in one view. Good for slicing into vertical scopes.

## When to Use

- Exploring a new feature or product direction
- Comparing solution approaches before building
- Mapping an existing system to understand where changes land
- Breaking a selected solution into vertical implementation slices
- Any "should we build X or Y?" discussion

## Entry Points

- **Start from R (Requirements)** — Describe the problem, pain points, constraints. Build up requirements and let shapes emerge.
- **Start from S (Shapes)** — Sketch a solution already in mind. Capture it as a shape and extract requirements as you go.

No required order. R and S inform each other throughout.

## Core Notation

| Level | Notation | Meaning | Relationship |
|-------|----------|---------|--------------|
| Requirements | R0, R1, R2... | Problem constraints | Members of set R |
| Shapes | A, B, C... | Solution options | Pick one from S |
| Components | C1, C2, C3... | Parts of a shape | Combine within shape |
| Alternatives | C3-A, C3-B... | Approaches to a component | Pick one per component |

## Phases

```
Shaping → Slicing
```

- **Shaping**: Explore problem/solution space, select and detail a shape
- **Slicing**: Break down for implementation into vertical slices with demo-able UI

## Key Actions

- **Populate R** — Gather requirements as they emerge
- **Sketch a shape** — Propose a high-level approach
- **Detail** — Break shape into components or concrete affordances
- **Check fit** — Build decision matrix (R × S), binary ✅/❌ only
- **Breadboard** — Map to UI/Code affordances with wiring
- **Spike** — Investigate unknowns
- **Slice** — Break breadboarded shape into vertical increments

## Detailed Reference

For the complete methodology, notation rules, examples, and procedures:

- **Shaping reference**: See [references/shaping.md](references/shaping.md) — Full shaping methodology including fit checks, parts, spikes, documents, multi-level consistency
- **Breadboarding reference**: See [references/breadboarding.md](references/breadboarding.md) — Complete breadboarding procedure, affordance tables, places, wiring, Mermaid conventions, chunking, slicing

Load the relevant reference when entering that phase of work.

## Quick Reference: Fit Check Format

```markdown
| Req | Requirement | Status | A | B | C |
|-----|-------------|--------|---|---|---|
| R0 | Full requirement text | Core goal | ✅ | ✅ | ✅ |
| R1 | Full requirement text | Must-have | ✅ | ❌ | ✅ |
```

- Always show full requirement text, never abbreviate
- Binary only: ✅ or ❌. No ⚠️ in fit checks
- Explanations go in Notes section below the table

## Quick Reference: Affordance Tables

**UI Affordances**: `# | Place | Component | Affordance | Control | Wires Out | Returns To`
**Code Affordances**: Same columns
**Controls**: click, type, call, observe, write, render
**Wires Out** (solid →): Control flow — calls, triggers, writes
**Returns To** (dashed -.->): Data flow — return values, reads

## Quick Reference: Slicing

- Every slice must end in **demo-able UI**
- Max 9 slices
- Each slice demonstrates a mechanism working
- Format: `V1: Name` — affordances, demo statement
