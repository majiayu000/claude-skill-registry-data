---
name: mbg-repo-analysis
description: Maps the Microelectronic Block Generator repository, traces the active execution path from a design script to the layout pipeline, separates active implementations from legacy code kept only for backward compatibility, and analyzes SPICE netlists (devices, nets, terminals, connectivity). Use before modifying or debugging any core module, or when asked what a design script actually calls. Do not use it to generate layout, run verification, or modify implementation — this skill is read-only.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-repo-analysis/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Repository Analysis

## Purpose

Give an agent a reliable, current picture of the codebase before it touches
anything: where the live execution path runs, which modules are legacy
compatibility shims, and how to read a SPICE netlist the way the pipeline
does. This skill only inspects; it never edits.

## When to Use

- Before modifying any file under
  `src/mbg/`.
- When asked "what actually runs when a design script executes" or "which
  module owns X".
- When you need to enumerate a netlist's devices, nets, or terminals before
  reasoning about placement or routing.
- When deciding whether a proposed change touches the active pipeline or a
  legacy fallback that other code still depends on.

## When Not to Use

- Generating a layout — use `mbg-spice-to-gds`.
- Running DRC/LVS/PEX — use `mbg-ic-verify`.
- Debugging a specific placement or routing failure once you already know
  which path is active — use `mbg-placement-debug` / `mbg-routing-debug`,
  which assume this skill's map as background.
- Making any code change — this skill is read-only by design; hand findings
  to whichever owner's skill covers the actual edit.

## Required Inputs

- Nothing is strictly required to use the "map the repo" portion.
- For netlist analysis: a SPICE subcircuit netlist string or path.

## Preconditions

- Read the actual files before asserting anything about them — module
  responsibilities and call graphs here can and do change; treat the
  summaries below as a starting map, not a substitute for grepping the
  current source.
- Core utilities live under
  `src/mbg/` (see `.ai/manifest.json`
  `project.core_utilities`).

## Workflow

### 1. Trace the active execution path

The live path, confirmed by what design scripts actually import and call
(e.g. `AI-Generated-Design-Result/*/run_layout.py`,
`designs/notebooks/chipathon2026-D/tests/test_all_designs.py`), is:

```
design script
  -> mbg.pipeline.spice_to_gds_with_checks(netlist)
       -> mbg.pipeline.spice_to_gds(netlist_input, ...)   # layout
       -> mbg.checks.run_drc / run_lvs / run_pex          # verification
```

`spice_to_gds_with_checks` is the one entry point design scripts are
expected to call — see `AGENTS.md`'s "Primary Pipeline API" section and
`mbg-spice-to-gds`.

### 2. Know there are two distinct pipeline flows — do not conflate them

`core/pipeline.py` defines **two** independent SPICE-to-GDS flows that look
similar but use different placement/routing engines underneath:

| Flow | Entry points | Placement | Routing | Used by the live design-script path? |
|---|---|---|---|---|
| **Legacy shape-router path** | `spice_to_gds`, `spice_to_gds_with_checks_legacy`, or `spice_to_gds_with_checks(..., legacy=True)` | `mbg.placement.placement()` | `mbg.routing.auto_router()` (fixed I/L/Z/U shape catalogue) | **No, not by default any more.** Reachable only via the explicit entry points at left. Kept working for reproducing archived runs. |
| **DesignContext path** | `spice_to_gds_with_checks` (**the default**), `spice_to_gds_ctx`, `spice_to_gds_with_checks_ctx` | `mbg.placement_engine.place_with_routability()` | `mbg.router.GridRouter` (A* grid maze router with rip-up/reroute and internal connectivity verification) | **Yes** — `spice_to_gds_with_checks` now delegates here, so this is what `tests/test_all_designs.py` and the design scripts exercise. Adds matching groups, symmetry constraints, `PinAccessPoint`, `RoutingFailure`, power rails and view emission. |

Both are live code — neither is dead — but they are **not interchangeable**
and a change to one does not automatically apply to the other. When asked
to fix "the placer" or "the router", first determine which of the two flows
the reporting design script actually used. Note the name no longer tells
you: `spice_to_gds_with_checks` means the **DesignContext** path unless the
call passed `legacy=True`. Archived runs in `AI-Generated-Design-Result/`
predate the switch and went through the legacy engine, so a bug described in
those logs may live in `mbg/routing.py`, not `mbg/router.py`.

### 3. Separate active from legacy code

`core/router.py` and `core/placement_engine.py` document their own relation
to the older modules directly in their module docstrings:

- `core/routing.py` implements a *shape* router (fixed I/L/Z/U wire
  patterns); `core/router.py`'s docstring states plainly that this is a
  different algorithm, not an edit to the old one, and that
  `routing.auto_router` can delegate to the new engine — but every legacy
  entry point in `routing.py` is kept working unchanged for existing
  scripts.
- `core/placement_engine.py`'s docstring states that the legacy
  `mbg.placement.placement()` entry point is untouched (aside from a
  device-width bug fix) so existing scripts keep working, while the new
  module adds matching/symmetry awareness, routing-channel reservation, and
  routability feedback.

Practical rule: do not assume a module is dead because a newer one exists
beside it. Confirm which design scripts / tests actually import which
entry point before treating either as removable.

### 4. Enumerate devices, nets, and terminals from a netlist

```python
from mbg.spice_parser import parse_netlist_with_pdk, build_design_context

config = parse_netlist_with_pdk(netlist_string, mode="analog")
# config["metadata"]["pdk"]        -> "gf180" or "sky130", auto-detected
#                                      from the .lib/.inc line
# config["components"]             -> list of dicts; one entry has
#                                      type == "subcircuit" (name + ports),
#                                      the rest have type == "device"
#                                      (name, model, nodes, parameters)

ctx = build_design_context(config, pdk=None)   # pdk optional for pure inspection
# ctx.devices        -> dict[name -> Device] (kind, terminals, width, length,
#                        fingers, multipliers, finger_width)
# ctx.nets           -> dict[name -> Net]     (terminals as (device, terminal)
#                        pairs, is_power/is_ground/is_critical/is_sensitive)
# ctx.matching_groups -> diff pairs, current mirrors, generic matched sets,
#                        inferred purely from netlist structure — nothing
#                        here invents geometry
```

`parse_netlist_with_pdk` auto-detects the PDK from `.LIB`/`.INC` lines
(`SKY130` -> `sky130`, `GF180` -> `gf180`) and accepts both `M1`-style and
`XM1`-style MOSFET instance names. `build_design_context` additionally
converts total SPICE device width into glayout's expected per-finger width
(`finger_width = width / (fingers * multipliers)`) — read
`core/spice_parser.py`'s `build_design_context` docstring before assuming
what it infers versus what it takes literally from the netlist.

## Outputs

- A description of which pipeline flow (legacy vs. DesignContext) a given
  design script or failure actually went through.
- A device/net/terminal inventory for a given netlist, with matching groups
  and power/ground nets identified.
- A statement of which module is authoritative for a given responsibility,
  with the specific file and, where useful, line reference that supports
  the claim.

## Failure Modes

- Asserting a call graph without having read the current source — the
  pipeline has two live flows that are easy to conflate; always confirm
  which one applies to the case at hand.
- Treating `core/placement.py` or `core/routing.py` as removable dead code
  without checking who still imports them.
- Assuming `parse_netlist_with_pdk` validates electrical correctness — it
  only parses syntax and structure; it does not simulate or verify the
  circuit.
- Reporting a "clean" netlist inventory without noting `mode` or PDK
  detection assumptions that shaped the parse.
