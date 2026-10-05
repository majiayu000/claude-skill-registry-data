---
name: dashboard-snapshot
description: Assemble a dashboard-ready snapshot from the canonical state.
---

# dashboard-snapshot

Goal:

- Assemble a dashboard-ready snapshot from the canonical state.

Inputs:

- `CoScientistState`
- `run_id`
- `updated_at`

Outputs:

- `dashboard/SNAPSHOT.json`

Context Loading:

- Read `skills/shared-references/artifact-contract.md` so the dashboard artifact stays downstream of canonical run artifacts.
- Read `packages/dashboard_contracts/snapshot_projection.py` before rebuilding `dashboard/SNAPSHOT.json`.
- Read `packages/dashboard_contracts/dashboard.py` when the dashboard-facing snapshot field layout needs to be checked.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- The canonical shared builder surface is `from tools import build_dashboard_snapshot`.
- The underlying implementation lives in `packages/dashboard_contracts/snapshot_projection.py`.
- The snapshot builder is a pure projection shared by API reads and artifact writes.
- The dashboard layer must remain downstream of canonical state and artifact contracts and must not invent new pipeline semantics.

Execution Steps:

1. Open `skills/shared-references/artifact-contract.md`, then read `packages/dashboard_contracts/snapshot_projection.py`.
2. Load the canonical run state and routing artifacts required to build the dashboard projection.
3. Call the canonical snapshot builder and write `dashboard/SNAPSHOT.json`.
4. Keep the emitted snapshot aligned with the dashboard-facing contract models.

Completion Rule:

- This skill is complete only when `dashboard/SNAPSHOT.json` has been rebuilt from canonical state through the shared deterministic builder surface.
