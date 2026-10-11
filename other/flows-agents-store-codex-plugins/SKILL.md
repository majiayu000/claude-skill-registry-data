---
name: flows
description: 'Find main user flows (entry points → services → DB) and visualize them Arguments: (no arguments — auto-discovers flows).'
---

# Discover and Visualize User Flows

Find the main user flows in the project and generate visual diagrams for each.

## Instructions

1. Read the primary skill:
   - `${CLAUDE_PLUGIN_ROOT}/skills/codemap-explain/SKILL.md` — for understanding and tracing flows

2. Ensure output directories exist: `docs/codemap/diagrams/` — create if missing.

3. Launch the **architect-explainer** agent with a prompt to:
   - Discover all route definitions / API endpoints / CLI commands
   - Group them into logical user flows (auth, CRUD, key features)
   - For each major flow (max 5-6): trace the call chain, identify decision points, note DB operations
   - Generate a flowchart diagram for each flow via the codemap-diagram skill
   - Save diagrams to `docs/codemap/diagrams/flow-{name}.drawio`
   - Write `docs/codemap/FLOWS.md` with flow descriptions and diagram links