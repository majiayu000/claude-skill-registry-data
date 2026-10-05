---
name: dircreative-update
description: Refresh model and prompt-pattern knowledge from official sources, GitHub prompt libraries, and internal QA.
---

# Update

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/sources/model-sources.yaml`
- `docs/film-preproduction/sources/prompt-sources.yaml`
- `docs/film-preproduction/research/model-adapter-notes.md`
- `docs/film-preproduction/research/image-prompt-style-system.md`
- `docs/film-preproduction/prompt-pattern-registry.json`

## Inputs

- source registry
- prompt registry
- QA observations

## Outputs

- source freshness report
- pattern candidate
- model adapter revision request
- deprecation note

## Rules

- Distinguish official facts from inferred behavior.
- Record source URL and verification date.
- Extract pattern mechanisms, not full copied prompts.
- Promote only after fixture QA improves.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record checked sources, stale entries, update decisions, and `next_recommended_skill: checkpoint`.
