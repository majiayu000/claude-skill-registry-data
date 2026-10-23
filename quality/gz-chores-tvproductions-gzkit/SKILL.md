---
name: gz-chores
description: Namespace router → maintenance and code-quality chore skills. Use to pick the chore intent before invoking the matched concrete skill directly.
category: agent-operations
lifecycle_state: active
disable-model-invocation: true
owner: gzkit-governance
last_reviewed: 2026-09-18
metadata:
  skill-version: "0.2.0"
model: haiku
---

# gz-chores

| Intent | Skill |
|---|---|
| chore runner | `gz-chore-runner` |
| deps upgrade | `gz-deps-upgrade` |
| foundation triage | `gz-foundation-triage` |
| pythonic detect | `gz-pythonic-pattern-detect` |
| pythonic apply | `gz-pythonic-pattern-apply` |
| config check | `gz-check-config-paths` |
| cli audit | `gz-cli-audit` |

Invoke the matched skill directly. See `gz-how` for the flows and the full catalog.
