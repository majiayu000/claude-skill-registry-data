---
name: update_architecture
description: Refresh architecture maps after structural changes.
---

## Purpose
Keep architecture indexes and maps aligned with code changes.

## Steps
1. Identify affected entrypoints, components, and flows.
2. Update `.agent-docs/architecture/overview.md` baseline truth.
3. Refresh interaction and flow maps for impacted areas.
4. Update component profiles if interfaces or boundaries changed.
5. Refresh `ARCHITECTURE.md` and `.agent-docs/architecture.md` indexes.
6. Record gaps and confidence levels.
7. Log notable changes in ADRs and Action Log.

## Guardrails
- Keep `ARCHITECTURE.md` index-only.
- Use the architecture mapping checklist for completeness.
