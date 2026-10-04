---
name: mike-model
version: 0.2.0
description: Inspect a MIKE+ .sqlite model via the mike-plus MCP server — active simulation/scenario/model type, unit system, the list of simulation setups and scenarios, element counts — and switch the active scenario. Use when an agent needs to understand a MIKE+ model before running or editing it, or must run a scenario prepared in the GUI. Requires MIKE+ installed + a license.
---

# MIKE+ Model

Opens a MIKE+ `.sqlite` and reports its high-level structure (via mikeplus).

## When to use
First step on any unfamiliar model: find the active simulation (what `mike_run` would run), the available simulation setups and scenarios, the model type, and the network size. Then, if the goal names a scenario that already exists, activate it.

## Tools
- **`mike_model_info`** — `{sqlite}` → `{active_simulation, active_scenario, active_model, unit_system, simulations[], scenarios[], counts{nodes,links,catchments}}`. Read-only. For MIKE 1D models (`CS_MIKE1D`) the setups/counts come from `msm_Project` / `msm_Node` / `msm_Link`; for MIKE+ SWMM models (`CS_SWMM`, e.g. after `mike_import_swmm`) from `mss_Project` / `mss_Node` / `mss_Link`.
- **`mike_set_scenario`** — `{sqlite, scenario}` → activates an EXISTING scenario (name from `scenarios[]`), verifies by re-opening the database, and reports per alternative group whether the scenario has its own alternative (`own_alternatives_in`) or shares Base (`shares_base_alternatives_in`). Mutates the model's active state: use a copy.

## Conventions
- Requires MIKE+ + license (it opens the model through mikeplus).
- Read-only, but still prefer a copy when a run/edit will follow.
- The `simulations` list are `msm_Project` (or `mss_Project`) setup ids — pass one as `mike_run`'s `simulation` to run a non-active setup.
- Scenarios are for **running** what the modeller prepared in the GUI. They are not the way to make a what-if variant from an agent: `mike_set_scenario` does not create scenarios, and edits made under a scenario either leak into Base (shared alternatives) or are refused (own alternatives): see `mike-compare` and use model copies.

## Orchestration
```
mike_model_info  -> choose simulation / scenario  -> (mike_set_scenario)  -> mike_run  -> mike-results / mike-plot
```
