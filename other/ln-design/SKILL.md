---
name: ln-design
description: "Explore radically different module shapes before committing to one. Use when choosing an API surface, deciding what a module hides vs exposes, or when the user says 'design it twice'."
argument-hint: "[module or API boundary to explore]"
---

# Ln Design

Apply Ousterhout's "Design It Twice": generate **3+ radically different module shapes**, compare on depth, and synthesize. The goal is deep modules — small interfaces hiding significant complexity. Do not implement; this is purely about the shape of the seam.

Use `ln-design` as the deepening pathway from `ln-review`: when review surfaces a shallow module or weak seam, explore alternative deepened module shapes here before routing to `ln-scope` or `ln-refactor`.

## Input

The module or API boundary: $ARGUMENTS

## Procedure

### 1. Gather requirements

Understand the problem, the callers, the key operations, constraints, and — crucially — what complexity should be hidden inside vs exposed. If this design follows an `ln-review` deepening candidate, start from that candidate's files, problem, possible direction, and benefits. Skip steps you already know the answer to.

Read `memory/SPEC.md` first when it exists. Use its lexicon for domain terms and respect its live assumptions, decisions, and invariants. Read `memory/PLAN.md` when the seam touches active or near-horizon work.

### 2. Generate designs (parallel sub-agents)

Spawn 3+ sub-agents simultaneously. Each must produce a **radically different** shape — enforce this by assigning divergent constraints:

- "Minimize method count — aim for 1–3 methods max"
- "Maximize flexibility — support many use cases"
- "Optimize for the most common case"
- "Take inspiration from [specific paradigm or library]"

Each agent returns: **interface** (types, methods, params, invariants, ordering constraints, error modes, required configuration, and performance characteristics), **usage example**, **what it hides**, **seam / adapter strategy** where relevant, and **trade-offs**.

### 3. Present and compare

Show each design sequentially, then compare in prose on:

- **Depth** (Ousterhout's depth test): small interface hiding significant complexity (good) vs large interface with thin implementation (bad)
- **Locality**: whether change, bugs, knowledge, and verification concentrate behind the seam
- **Leverage**: what callers get per fact they must learn about the interface
- **Ease of correct use** vs ease of misuse
- **General-purpose vs specialized**: flexibility vs focus
- **Implementation efficiency**: does the shape allow efficient internals?

Highlight where designs diverge most.

### 4. Synthesize

The best design often combines insights from multiple options. Ask which shape best fits the primary use case and whether elements from other designs are worth incorporating.

## Output

Present the recommended module shape with rationale. If `memory/SPEC.md` exists, ensure names align with its lexicon.

Do not invent a standalone design document unless the user explicitly asks for one. Durable design choices reconcile back into `memory/SPEC.md` and `memory/PLAN.md`.

## Routing

After choosing a design, present these options to the user (use `tool-ask-question`):

| #   | Label         | Target     | Why                                      |
| --- | ------------- | ---------- | ---------------------------------------- |
| 1   | Scope a slice | `ln-scope` | Design is chosen, define the first slice |
| 2   | Write a spec  | `ln-spec`  | Module needs a full spec before slicing  |
| 3   | Grill it more | `ln-grill` | Design choice raised new questions       |

Recommended: **1**

---
*Adapted from [mattpocock/skills/design-an-interface](https://github.com/mattpocock/skills/tree/main/design-an-interface).*
