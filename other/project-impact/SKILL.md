---
name: project-impact
description: Calculate which story-film artifacts become stale after a story, screenplay, canon, reference, shot, dialogue, or production change, then preserve unaffected approved work.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Project Impact

## Workflow

1. Read the core contract and dependency rules.
2. Read `00_project/dependencies.json` and current state.
3. Identify the changed artifact key or stable ID.
4. Traverse only downstream dependency edges in the same or affected scope.
5. Mark affected artifacts stale. Preserve unrelated approved artifacts.
6. Write a short impact report naming changed input, invalidated outputs, preserved outputs, and required validation boundaries.
7. Run `scripts/project_status.py` when available to support hash-based change detection.

## Done

The project has an explicit minimal rebuild set and no stale artifact is still presented as approved.
