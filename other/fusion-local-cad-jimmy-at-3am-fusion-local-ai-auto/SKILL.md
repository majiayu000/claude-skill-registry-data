---
name: fusion-local-cad
description: Inspect and modify local Autodesk Fusion desktop CAD through its installed API, with exact geometry checks, parameter edits, planar-face cuts, and local export/reopen verification. Use for this project's offline CAD workflow and its required validation before CAM.
---

Use the project root `AGENTS.md` and `SETUP.md`. The skill supplies procedure; the running Fusion add-in supplies execution. Do not equate installing a skill with connecting Fusion.

Call `py -3 scripts/cad_client.py ping` to verify the loaded bridge. Call `inspect` only after the bridge has created/imported a local document. Use `self_test` for the parameter workflow and `geometry_test` for the complete scratch geometry chain. `open_local` imports a workspace `.f3d`/STEP into a new document; never attach the bridge to an arbitrary active document. Requests enforce Fusion Work Offline mode. Require `ok: true` and inspect the returned postconditions before reporting success.

For edits, inspect first and use the returned document session ID and revision with `set_parameter`. Supply an explicit expression such as `8 mm`. The bridge checkpoints and exports locally; it does not save to Autodesk cloud. Supported feature creation is `cut_hole` on a uniquely resolved planar face of a root solid. Supply `body` (the inspected body name), model-space `center_mm`, unit `outward_normal`, `diameter_mm` and `depth_mm`, plus session/revision. The center must lie on the bounded face. The implementation transforms model to sketch coordinates, identifies the circular profile by loop count/area, and cuts inward. Do not select the first sketch profile: face sketches can auto-project the whole face boundary. Add other features or assembly edits only with separate installed-API verification and acceptance cases.

Interpret measurements using their stated units. Inspection enumerates root bodies and occurrence bodies, with occurrence paths and transforms. Face normals are local samples, not a full description of curved surfaces; use surface type and evaluators for detailed geometry. A sample face point is not necessarily its centroid. Respect output truncation.

After a change, compare required dimensions and topology, timeline health and native reimport. Evaluate viewport images with `view_image`. For complex geometry, inspect multiple views and sections in addition to numerical measurements. Do not infer overlap from zero minimum distance alone; touching and volumetric interference require distinct checks.

Exported `top` and `front` images follow the user's Fusion view-cube preference, not an assumed world-Z convention. Numerical coordinate frames are authoritative. The verified geometry fixture is a 40 x 30 mm plate with a 2 mm hole through its 30 mm span: its solid volume is `40*30*thickness - 30*pi mm^3`.

Finish create/import, inspection, checkpoint, edit, recomputation, geometric checks, image review, native/STEP export, native reopen and a second edit before CAM. See `STATUS.md` for the passed bridge acceptance scope. Use `fusion-local-cam` for subsequent CAM work. Do not switch documents or edit CAD while a CAM generation job is running.

Inspect `artifacts/<request-id>/result.json` after a client timeout. The bridge expires queued requests before execution, but a request already running can finish after the client stops waiting. Do not resend mutations blindly.

API references: [units](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm), [main-thread events](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Threading_UM.htm). Installed definitions are beneath the running Fusion executable's `Api/Python/packages/adsk/` folder. Do not pip-install an unrelated `adsk` package.
