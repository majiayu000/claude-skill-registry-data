---
name: docs-lint-link-check
description: Validate documentation quality gates (local links, required files, stale markers, and mirror drift).
owner_agent: workflow-agent
---

# docs:lint-link-check

Use this skill whenever docs integrity or governance drift must be verified.

## Checks

- Local markdown/txt link validity (no broken local targets)
- Required project files from `content/*/project.config.json`
- Stale date/version markers for workspace status docs
- `.cursor` vs `.antigravity` mirror drift checks

## Implementation

- Primary command: `python3 .ai/scripts/docs_quality_gate.py`
- Optional strict run: `python3 .ai/scripts/docs_quality_gate.py --max-age-days 60`

## Boundaries

- Owns docs-quality verification only.
- Does not schedule recurring execution (handled by `workspace:audit-orchestrator`).
- Does not edit content unless explicitly requested.

## Trigger Phrases

- "lint docs"
- "check links"
- "validate docs quality gates"
- "check docs drift"
