---
name: gz-workflow
description: Namespace router → end-to-end workflow skills (design through release). Use to pick the next workflow stage before invoking the matched concrete skill directly.
category: agent-operations
lifecycle_state: active
disable-model-invocation: true
owner: gzkit-governance
last_reviewed: 2026-09-18
metadata:
  skill-version: "0.4.0"
model: haiku
---

# gz-workflow

| Intent | Skill |
|---|---|
| R&D run — "consider this for gzkit" (operator-invoked) | `gz-rnd` |
| design | `gz-design` |
| plan | `gz-plan` |
| implement | `gz-obpi-pipeline` |
| verify | `gz-implement` |
| justify | `gz-justify` |
| plan audit | `gz-plan-audit` |
| release | `gz-patch-release` (also routed by `gz-manage`) |

Invoke the matched skill directly. See `gz-how` for the flows and the full catalog.
