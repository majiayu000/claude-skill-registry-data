---
name: cad-modeling-fusion
description: Generate parametric CAD model specifications and Autodesk Fusion Python scripts from natural-language 3D modeling requests. Use when the user asks to create, automate, modify, export, or validate CAD models for Fusion, FreeCAD, OpenSCAD, STEP, STL, OBJ, or 3D printing.
---

# CAD Modeling Fusion Skill

Use this skill when a user wants a parametric CAD model, a validated CAD model specification, generated Autodesk Fusion Python code, fallback FreeCAD/OpenSCAD code, or export guidance for STEP/STL/OBJ/F3D workflows.

Do not use this skill for pure mesh sculpting, animation, rendering-only scenes, destructive edits to user CAD files, or executing untrusted generated code without explicit confirmation.

## Workflow

1. Parse the request into a `ModelSpec` JSON object.
2. Ask clarifying questions only when critical dimensions, units, or manufacturing requirements are missing and cannot be inferred.
3. Validate the spec with `scripts/validate_spec.py` or `cad_skill.validators`.
4. Choose a backend: `fusion` first, `freecad` when Fusion is unavailable, and `openscad` for simple CSG previews.
5. Generate code with `scripts/generate_model.py`.
6. Save generated files under `outputs/<model_name>/`.
7. If execution is requested, run the script in the CAD tool or use the optional Computer Use plan from `cad_skill.computer_use_adapter`.
8. Report files created, assumptions, validation issues, run instructions, and known limitations.

## Safety

- Prefer official scripting APIs over GUI automation.
- Never overwrite, delete, or move user files unless explicitly requested.
- Keep generated scripts in a dedicated output directory.
- Validate units, dimensions, wall thickness, backend feature support, and export requests before generation.
- Treat Computer Use as optional and platform-specific.

## Scripts

- Generate code: `python scripts/generate_model.py --spec assets/examples/mounting_bracket/example.spec.json --backend fusion --out outputs/mounting_bracket`
- Generate all examples: `python scripts/generate_all_examples.py --backend all --overwrite`
- Validate only: `python scripts/validate_spec.py assets/examples/phone_stand/example.spec.json --strict`
- Preview plan: `python scripts/render_preview.py --spec assets/examples/simple_gear/example.spec.json --backend openscad`
- Fusion run plan: `python scripts/run_fusion_script.py outputs/mounting_bracket/mounting_bracket_fusion.py`

## Retrieval Map

Load the narrowest relevant reference first:

- Enclosure-like objects: `references/cad_modeling_patterns.md` -> Rectangular Enclosure, Lid + Enclosure, Rounded Container, Snap-Fit Enclosure; examples `assets/examples/pcb_enclosure/`, `assets/examples/storage_bin/`.
- Brackets, mounts, and fixtures: `references/cad_modeling_patterns.md` -> Mounting Bracket, Rib Reinforcement, Boss Feature, Camera/Servo Side-Ear Mount; examples `assets/examples/mounting_bracket/`, `assets/examples/servo_mount/`, `assets/examples/camera_mount/`.
- Rotational parts, pulleys, shafts, bearings, and gears: `references/cad_modeling_patterns.md` -> Gear-Like Wheel, Pulley With Flanges, Bearing Seat, Shaft Adapter, Parametric Knob; examples `assets/examples/simple_gear/`, `assets/examples/pulley/`, `assets/examples/bearing_mount/`, `assets/examples/shaft_coupler/`.
- Laboratory and scientific fixtures: `references/cad_modeling_patterns.md` -> Laboratory Rack, Tube Holder, Optical Mount, Lens Retainer Ring, Sample Stage Grid; examples `assets/examples/optical_mount/`, `assets/examples/lens_holder/`, `assets/examples/sample_stage/`, `assets/examples/test_tube_rack/`, `assets/examples/microscope_adapter/`.
- Consumer and utility parts: `references/cad_modeling_patterns.md` -> Phone Stand, Hook, Cable Clip, Storage Tray; examples `assets/examples/phone_stand/`, `assets/examples/cable_clip/`, `assets/examples/wall_hook/`, `assets/examples/storage_bin/`.
- Fusion API implementation: `references/fusion_api_recipes.md`; quick overview `references/fusion_api_notes.md`.
- Manufacturing checks: `references/manufacturing_rules.md` and `references/geometry_validation_rules.md`.
- Example selection: `assets/examples/README.md` and `references/examples.md`.

## References

- `references/model_spec_schema.md` defines the full `ModelSpec` format.
- `references/cad_modeling_patterns.md` is the reusable CAD pattern cookbook.
- `references/fusion_api_recipes.md` contains Fusion API implementation recipes.
- `references/fusion_api_notes.md` summarizes Fusion API orientation.
- `references/manufacturing_rules.md` gives process-specific design rules.
- `references/geometry_validation_rules.md` defines validation and manufacturability checks.
- `references/computer_use_workflow.md` covers optional GUI automation.
- `references/examples.md` explains the bundled example specs.
- `references/repository_review.md` tracks knowledge-base quality and follow-up recommendations.

The backend generators cover common primitive, boolean, hole, fillet, chamfer, shell, pattern, and export workflows, and emit explicit warnings for unsupported or approximate features.
