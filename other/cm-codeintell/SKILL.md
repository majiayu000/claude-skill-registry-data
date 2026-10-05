---
name: cm-codeintell
description: Unified code intelligence — routes to Skeleton Index, CodeGraph, Architecture Diagram, or Smart Context Builder based on task shape. Loads deep refs on demand.
token_budget: 1500
token_core: 520
token_refs:
  layer-0-skeleton: 820
  layer-1-codegraph: 980
  layer-2-architecture: 620
  layer-3-context-builder: 760
  integration-workflows: 520
compressed: true
deprecated: false
---

# Code Intelligence — Structural Understanding for AI Agents

## TL;DR
- **Use to** index a codebase for fast structural understanding
- **Layers**: skeleton, code graph, architecture diagram, smart context
- **Default**: start from the lightest useful layer
- **Next**: `cm-planning`, `cm-debugging`, or `cm-execution`

> Stop scanning. Start querying. Load only the layer the task actually needs.

## When to Use
- Understanding a medium or large codebase
- Tracing callers, callees, or impact before edits
- Building focused context for planning, debugging, or execution
- Auto-triggering structural understanding during project setup

## Choose a Layer

```
Need instant codebase orientation with zero extra setup?
└─ YES → Layer 0: Skeleton Index

Need symbol search, callers/callees, or impact analysis?
└─ YES → Layer 1: Code Graph

Need a visual system / module map?
└─ YES → Layer 2: Architecture Diagram

Need a focused context packet for another skill or agent?
└─ YES → Layer 3: Smart Context Builder
```

| Layer | Summary | Load |
|---|---|---|
| 0 | Grep-based skeleton index for instant orientation | `references/layer-0-skeleton.md` |
| 1 | AST graph and symbol-query workflow | `references/layer-1-codegraph.md` |
| 2 | Mermaid architecture generation | `references/layer-2-architecture.md` |
| 3 | Synthesized focused context for downstream work | `references/layer-3-context-builder.md` |

## Conditional References
- Load only the target layer reference for the current task.
- Load `references/integration-workflows.md` only when wiring `cm-codeintell` into `cm-start`, `cm-planning`, `cm-debugging`, or `cm-execution`.

## Integration
| Skill | How `cm-codeintell` helps |
|---|---|
| `cm-start` | bootstrap structural context early |
| `cm-planning` | impact analysis and component boundaries |
| `cm-debugging` | trace callers, callees, and failure paths |
| `cm-execution` | pre-flight context for focused implementation |

## Rules
- Start from the lightest layer that answers the question.
- Prefer Layer 0 when simple orientation is enough.
- Regenerate or refresh indexes after major structural changes.
- Do not pay for deep graph or context synthesis unless the task needs it.

## The Bottom Line
**Pick the cheapest layer that answers the question, then load deeper only when needed.**
