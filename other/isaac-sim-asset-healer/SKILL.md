---
name: isaac-sim-asset-healer
description: Use when creating, reviewing, or repairing Isaac Sim 5.1 scene-generation Python for GUI Script Editor workflows, especially from floor-plan images or local USD/USDC asset inventories. The skill forbids direct MCP script execution and produces English-only code snippets that clean old prims, validate assets, preserve navigation clearance, and apply collision APIs.
---

# Isaac Sim Asset Healer

## Purpose

Generate reliable Isaac Sim 5.1 Python for two safe offline execution modes:

- GUI Script Editor snippets that the user can paste into Isaac Sim.
- Standalone `SimulationApp` runners executed with the Isaac Sim Python interpreter.

The generated code must build or repair a scene without relying on MCP `execute_script` transport.

## Required Inputs

- Floor-plan image, coordinate data, or a precise verbal layout.
- Scale source, such as a dimension label, grid size, or user-confirmed meters-per-cell value.
- Local asset directory when USD/USDC assets are requested.

If the request lacks both visual layout and coordinate data, ask for a top-down screenshot or a dimensioned sketch before generating code.

## Hard Rules

- Do not call Isaac Sim MCP `execute_script` to create the scene.
- Generated Python code must use ASCII-only comments, strings, variable names, and print output.
- Prefer standalone `SimulationApp({"headless": False})` when the user wants Isaac Sim to open and build the scene automatically.
- Prefer Script Editor snippets when Isaac Sim is already open and the user wants to paste code manually.
- Never invent local asset filenames.
- Check real local inventory before referencing USD or USDC files.
- Use bundle-safe paths for packaged assets: `os.path.join(asset_root, folder_name, folder_name)`.
- Delete the target root prim before rebuilding it.
- Keep `(0, 0, 0)` clear for robot spawning with at least `1.5m` radius.
- Keep doorways and node transitions clear with at least `1.5m` radius.
- Keep furniture separated enough for robot navigation.
- Keep furniture inside wall bounds.
- Build outer walls from the actual footprint, not a simplified rectangle.
- Build doorway walls with exactly two full-height wall pieces and no header.
- Use data tables as source of truth for walls, doors, slabs, windows, and placements.
- Apply `UsdPhysics.CollisionAPI` to generated obstacles and referenced mesh assets.

## Workflow

1. Calibrate scale.
2. Extract topology as nodes, edges, corners, walls, doors, floor slabs, windows, and optional furniture zones.
3. Validate geometry: axis alignment, duplicate walls, door gaps, floor continuity, and navigation clearance.
4. Generate a Script Editor snippet with self-contained data tables and helper functions.
5. Include a concise validation report before or after the code.

For standalone mode, wrap the same generated scene builder with:

- `from isaacsim import SimulationApp`
- `simulation_app = SimulationApp({"headless": False})`
- normal Isaac Sim imports after `SimulationApp` starts
- an update loop using `while simulation_app.is_running(): simulation_app.update()`

## Output Shape

When generating a scene, return:

- `Corner Points Table`
- `Wall Segments Table`
- `Doorway Table`
- `Floor Slabs Table`
- Script Editor Python snippet
- Optional standalone `SimulationApp` runner
- Validation notes

## Implementation Preference

Use `UsdGeom.Cube` with translate and scale for primitive geometry. This is more stable in Isaac Sim 5.1 than `FixedCuboid` in environments where type conversion errors occur.

Use `FixedCuboid(..., color=np.array(...))` only when the target environment is known to support it.

Run standalone scripts with the Isaac Sim Python executable, for example:

```bash
/home/iy/miniconda3/envs/isaacsim-5.1/bin/python /tmp/generated_scene.py
```
