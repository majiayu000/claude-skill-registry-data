---
name: theorist-mode
description: |
  Activate theoretical foundations context for discussions about Grafema's
  formal underpinnings, multi-language strategy, cognitive science, and
  abstract architecture. Use when: (1) discussing formal languages, type
  theory, abstract interpretation, (2) planning multi-language support,
  (3) designing metrics or benchmarks, (4) reasoning about completeness
  and soundness of analysis, (5) positioning Grafema academically.
author: Vadim Reshetnikov + Claude Code
version: 1.0.0
date: 2026-03-03
tags: [research, theory, architecture, cognitive-science]
---

# Theorist Mode

## Activation

Load full theoretical context before discussing abstract/formal topics.

## Required Context — Read These Files First

1. `_ai/research/theoretical-foundations.md` — 5 abstraction levels, all theories, Cognitive Dimensions, evidence base, LLM benchmark design, academic partnership strategy
2. `_ai/research/declarative-semantic-rules.md` — semantic rules matrix, flow rules, completeness guarantees, prior art (Spoofax, CodeQL, Joern)

## Key Concepts Quick Reference

### The Five Levels

```
L5: Cognitive Model    → Cognitive Dimensions of Notations (Green & Petre)
L4: Paradigm           → Denotational Semantics
L3: Semantic Projections → Abstract Interpretation (Cousot & Cousot)
L2: Semantic Roles     → Operational Semantics
L1: AST Node Types     → Formal Grammars (Chomsky)
L0: Source Code
```

### Core Vocabulary

- **Semantic projection** — DFG, CFG, Scope etc. Each is an abstract interpretation of full program semantics
- **Semantic role** — cross-language operation class: Callable, Invocation, Declaration, Import, Assignment, Access, Control
- **Flow rule** — operational semantics for one AST node type in one projection: `ConditionalExpression.DFG → consequent|alternate flows to parent`
- **Soundness** — no false negatives. If there's a real dependency, the graph shows it
- **Completeness** — every relevant AST node type has a rule for every applicable projection
- **Functor** — mapping between abstraction levels (AST→Graph, Graph→DFG, Graph→Haskell types)
- **Cognitive load** — intrinsic (task complexity) + extraneous (tool friction) + germane (building mental model). Grafema reduces extraneous and pre-builds germane.

### Grafema's Theoretical Identity

**"Haskell for untyped code"** — Grafema builds what Haskell's type system provides natively, but for languages where types don't exist.

| Haskell | Grafema |
|---------|---------|
| Type signatures | Graph edges (RETURNS, THROWS, TRANSFORMS) |
| Exhaustiveness checking | Semantic rules matrix |
| Type class laws | Guarantees (`grafema check`) |
| Hoogle (search by type) | `find_nodes` (search by graph) |
| Compiler rejects inconsistencies | `grafema check` rejects broken guarantees |

### The Key Number

**Developers spend 58% of time on code comprehension.** A tool that speeds this up by 30% saves 17% of total developer time. For 50 developers = 8.5 FTE.

### Multi-Language Strategy

Best-in-class parser per language (NOT tree-sitter). AST = human understanding, CST = "code of code".

| Language | Parser | Complexity | MVP weeks |
|----------|--------|------------|-----------|
| JS/TS | Babel | Baseline | Done |
| Java | JavaParser | Low | 2-3 |
| Kotlin | kotlin-compiler (PSI) | Medium-Low | 3-4 |
| Swift | SwiftSyntax | Medium | 4-5 |
| Obj-C | libclang | High | 6-8 |

Order: Java first (simplest, reveals JS-coupling), then Kotlin → Swift → Obj-C.

### Completeness Chain

```
@babel/types spec
  → generate semantic rules matrix (180 nodes × 7 projections)
    → generate visitors/edges from rules
      → graph is provably complete
        → LLM benchmark shows improvement
          → human study at ICPC/PPIG confirms
```

## Discussion Guidelines

When in theorist mode:

1. **Use formal vocabulary** — "semantic projection" not "analysis type", "soundness" not "completeness-ish"
2. **Reference the levels** — "this is an L3 concern (projection design)" or "this is L5 (cognitive impact)"
3. **Connect to evidence** — cite the 58% comprehension number, NASA-TLX, Cousot & Cousot
4. **Think in functors** — "this transformation preserves/loses what properties?"
5. **Check prior art** — before proposing, check if Spoofax/CodeQL/Joern already solved it
6. **Measure** — every claim should have a measurable metric attached
