---
name: performance-analyzer
description: >-
  Read-only performance analysis for Blunder Engine hot paths. Use with Task
  tool for parallel review of viewport, render, or UI bottlenecks. Reports
  bottlenecks with severity and suggested fix order.
---

# Performance analyzer (read-only)

Run as a **parallel subagent** (Cursor Task tool, `subagent_type: explore`, `readonly: true`).

## Scope

- Viewport / render pipeline (`RenderSystem`, readback, Slint present)
- Per-frame allocations and redundant work
- GPU/CPU sync stalls (fences, readback, full-window composite)

Do **not** edit files. Read and report only.

## Process

1. Read `docs/agents/render-pipeline.md` and trace the reported hot path.
2. Grep/read key files under `engine/src/runtime/function/render/` and `.../ui/`.
3. Identify:
   - Work done every frame vs only on dirty/resize
   - Full-screen vs partial updates
   - CPU-GPU stalls and copies
   - Redundant Slint or Vulkan passes
4. Rank findings by **impact** (high / medium / low) and **effort** (small / medium / large).

## Output format

```markdown
## Performance findings

### High impact
- [finding] — file:line — suggested fix

### Medium impact
- ...

### Low impact / nice-to-have
- ...

## Recommended order
1. ...
2. ...

## Risks
- Invariants that must not break (Z-up, offscreen path, Slint fork)
```

## Pair with

- `viewport-perf` skill for viewport-specific context
- `blunder-engine` skill for project invariants
