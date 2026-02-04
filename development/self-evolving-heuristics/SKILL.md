---
name: self-evolving-heuristics
description: Analyze the codebase to find hard-coded thresholds, defaults, and timing constants, then convert them into self-evolving heuristics backed by a persistent registry that updates on each execution. Use when asked to replace fixed decision logic with adaptive parameters, build a heuristic registry, or generate a patch plan for heuristic rewrites.
---

# Self Evolving Heuristics

## Overview

Identify static decision points in the codebase and rewrite them as registry-backed heuristics that evolve via runtime observations.

## Workflow

1. Scan for bottlenecks
   - `python scripts/scan_bottlenecks.py --root . --output runs/heuristics_bottlenecks.json`
2. Build the heuristic registry
   - `python scripts/build_registry.py --input runs/heuristics_bottlenecks.json --output memory/agent_state_v1/heuristics.json`
3. Install the registry module for runtime use
   - `python scripts/install_registry.py --repo .`
4. Emit a patch plan
   - `python scripts/emit_patch_plan.py --input runs/heuristics_bottlenecks.json --output runs/heuristics_patch_plan.md`
5. Apply the plan manually
   - Replace constants with `heuristics_registry.get_value("key", default=<literal>)`.
   - Add `heuristics_registry.observe("key", observed_value)` after each execution to evolve the value.

## Update Pattern

```python
from core.sovereignty_v2 import heuristics_registry

threshold = heuristics_registry.get_value("core_worker.cpu_threshold", default=0.85)
if cpu_usage > threshold:
    ...
heuristics_registry.observe("core_worker.cpu_threshold", cpu_usage)
```

## Notes

- Keep bounds conservative and only update from reliable signals.
- Re-run the scan after patching to confirm remaining constants are intentional.

