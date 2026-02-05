---
name: runtime-diagnostics
description: Run local system diagnostics and model benchmarks across CPU, memory, GPU, NPU, Docker, and Kubernetes; use when asked to benchmark, health-check, or collect environment diagnostics, and store a summary in memory.
---

# Runtime Diagnostics

Use this skill to collect a consistent diagnostics snapshot with timeouts and safe fallbacks.

## Workflow

1) Run the diagnostics script:

```bash
python skills/automation/runtime-diagnostics/scripts/diagnostics.py --runs 1
```

2) If Docker or CIM access fails, rerun with elevated permissions.
3) Share the JSON output summary and note any failures/timeouts.
4) The script stores a semantic memory entry with the full context.

## Notes

- The script times out Kubernetes queries; it will record errors instead of hanging.
- If sentence-transformers or embedding backends are missing, the benchmark can still run.
- Use `--runs 3` for a deeper model benchmark (slower).
