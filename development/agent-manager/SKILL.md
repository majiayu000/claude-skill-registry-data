---
name: agent_manager
description: Automatically manage agent lifecycle, proposals, and registry.
---

## Purpose
Maintain an auto-managed registry of agents and keep their scopes current.

## Steps
1. Discover all `AGENTS.md` and `AGENTS.override.md` files.
2. Update `.agent-docs/memory/AGENTS_REGISTRY.md` and `.agent-docs/memory/AGENTS_REGISTRY.json`.
3. Compare coverage with `.agent-docs/memory/INDEX.md` and architecture maps.
4. Propose missing agents in `.agent-docs/memory/AGENT_PROPOSALS.md`.
5. Explain each proposal objective and ask for approval before scaffolding.
6. Detect drift by comparing scope file timestamps to agent instructions.
7. Mark `needs_update`, `stale`, or `retire_candidate` in the registry.
8. For approved proposals, scaffold new agent instructions from
   `.agent-docs/agents/AGENT_TEMPLATE.md`.
9. Record actions in the Action Log.
10. Use the agent management checklist for completeness.

## Guardrails
- Use the merge protocol for updates.
- Do not modify fixed agents; only propose changes.
