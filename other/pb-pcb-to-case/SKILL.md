---
name: pb-pcb-to-case
description: >-
  From a KiCad board to a parametric enclosure that fits it: ERC and DRC
  clean, board dimensions extracted, an OpenSCAD case with your clearance,
  Gerbers exported, fab hand-off only after GO. Use for "PCB to enclosure",
  "case for this board", "KiCad to OpenSCAD case".
category: engineering-hardware
kind: playbook
trigger: ["PCB to enclosure", "case for this board", "KiCad to OpenSCAD case"]
inputs: [kicad_project, clearance_mm, mounting_style]
requires:
  skills: [godmode-hardware-pcb, "pcb-validation-dfm-signoff (external)", "pcb-constraint-definition (external)", "code-first-hardware-design (external)"]
  agents: []
  mcps: [kicad, openscad]
  store: []
go_points: [fab order]
outputs: ["hw/<project>/dims.json", "hw/<project>/case.scad", "hw/<project>/case.stl", "hw/<project>/gerbers/", "hw/<project>/fab.md", "production_artifacts/pb-pcb-to-case-<date>.md"]
verify: "run_drc zero errors; case inner dims >= board dims + clearance on every axis (recomputed from dims.json)"
difficulty: advanced
est_time: 1-3 h
---

# PCB to enclosure
What you get: a DRC-clean board and a parametric enclosure that fits it, with Gerbers ready for a fab order that you place after your GO.

## Inputs
- kicad_project — path to the KiCad project (`.kicad_pro`, `.kicad_pcb`, `.kicad_sch`)
- clearance_mm — gap between board and case wall on every axis
- mounting_style — for example standoffs, rails or snap-fit

## Steps
1. Preflight — `get_pcb_statistics` on `kicad`; `get_capabilities` on `openscad`; `test -f ~/.claude/skills/<name>/SKILL.md` for `pcb-validation-dfm-signoff`, `pcb-constraint-definition` and `code-first-hardware-design`. MCP tools may be deferred in the harness: try to load the tool once via the harness tool search before declaring it missing. MCP tool not loaded or call errors → stop with "Missing MCP: `<server>` (`<tool>` unavailable). Check `mcpServers.<server>` in your harness config." A skill file absent → stop with "Missing skill: <name> (installed locally only, not shipped by AOS). Install it and rerun." Write nothing except the run log on a stop — all probes answered
2. Ask — kicad_project, clearance_mm, mounting_style, project slug → run log and `hw/<project>/` — all answered, project files exist
3. pcb-validation-dfm-signoff + godmode-hardware-pcb — `run_erc` and `run_drc` (details via `get_erc_violations` and `get_drc_violations`) → violation list in the run log — zero errors; any error stops the run, the board is not edited by this playbook
4. pcb-constraint-definition — board outline, mounting holes and connector positions (`get_pcb_statistics`, `list_pcb_footprints`) → `hw/<project>/dims.json` (length, width, thickness, holes, connector edges, all in mm) — all values present; a missing value is asked of the human, never guessed
5. code-first-hardware-design + openscad — dims.json, clearance_mm, mounting_style → `case.scad` (parameters at the top, driven by dims.json), then `create_model_from_scad` (returns the `model_id`), then STL and a preview via `export_model` and `get_model_preview` with that `model_id` → `case.stl` — inner dims >= board dims + clearance_mm on every axis, recomputed from dims.json and logged — stops for approval
6. Gerbers — `export_gerber` → `hw/<project>/gerbers/` — files exist; `run_drc` again with zero errors on the exported state
7. [GO] fab hand-off — `hw/<project>/fab.md` with the Gerber list, board dimensions, layer count and case STL, shown in full. The run stops here until the human types GO. No fab ordering tool exists: the GO releases only the hand-off file and the order is placed manually by the human. — fab.md written

Run log: `production_artifacts/pb-pcb-to-case-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
