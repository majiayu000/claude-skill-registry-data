---
name: pb-image-to-3d
description: >-
  Turn one reference image into a cleaned, scaled 3D asset: your own
  image-to-3D ComfyUI workflow makes the mesh, Blender decimates it to a poly
  budget, fixes scale, origin and material, and exports a .glb. Use for
  "image to 3D", "make a 3D model from this picture", "photo to glb".
category: media-eventtech
kind: playbook
trigger: ["image to 3D", "3D model from this picture", "photo to glb"]
inputs: [image, comfy_workflow, poly_budget, project]
requires:
  skills: [bdb-blender-mcp, godmode-3d-creation]
  agents: []
  mcps: [comfyui-mcp, bdb_blender_mcp]
  store: []
go_points: []
outputs: ["renders/<project>/asset.glb", "renders/<project>/preview.png", "production_artifacts/pb-image-to-3d-<date>.md"]
verify: "asset.glb exists; Blender reports face count <= budget and non-zero dimensions"
difficulty: advanced
est_time: 30-90 min
---

# Image to 3D asset
What you get: a cleaned, scaled `.glb` from one reference image, with a preview you approved.

## Inputs
- image — the reference image path
- comfy_workflow — path to a ComfyUI API-format workflow JSON that contains the image-to-3D nodes; required, never invented (no TripoSR or TRELLIS server ships with AOS)
- poly_budget — maximum face count
- project — a slug for `renders/<project>/`

## Steps
1. Preflight — one probe per server, before any file is written: `check_comfyui_health` on `comfyui-mcp`; `get_scene_info` on `bdb_blender_mcp`. MCP tools may be deferred in the harness: try to load the tool once via the harness tool search before declaring it missing. Tool not loaded, call errors, or ComfyUI `status` is not `"online"` → stop with "Missing MCP: `<server>` (`<tool>` unavailable). Start <ComfyUI|Blender and click Connect to Claude in the BlenderMCP sidebar tab> and check `mcpServers.<server>` in your harness config." and write nothing except the run log — both probes answered
2. Ask — image, comfy_workflow path, poly_budget, project slug, target size in metres → run log and `renders/<project>/` — all answered, image and workflow files exist
3. ComfyUI — the workflow file's text with the image filled in as the JSON string for `queue_prompt` → `get_history <prompt_id>` status success → `get_output_media_info` path of the mesh file — a mesh file exists; `local_path` is only set when `COMFYUI_DIR` is set, so if `local_path` is empty or `exists_locally` is false, stop with a clear message and import nothing
4. Blender (bdb-blender-mcp, godmode-3d-creation) — mesh file → via `execute_blender_code`: import, Decimate modifier down to poly_budget, scale to the target size, origin to base centre, one material, and report face count and dimensions; `get_scene_info` as the cross-check — face count <= poly_budget and non-zero dimensions; save the Blender project first, since scripted code can crash the session
5. Preview — a viewport render saved to `renders/<project>/preview.png` via `execute_blender_code` — file exists — stops for approval (taste review); changes loop back to step 4
6. Export — `execute_blender_code` runs the glTF binary export → `renders/<project>/asset.glb` — file exists and is larger than 0 bytes; re-import the file or read the exported object stats and log face count and dimensions again

Run log: `production_artifacts/pb-image-to-3d-<date>.md` in the start directory, never committed

Rules
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR APPROVAL: <step>` at each stop.
- This playbook has no GO step: it writes only under `renders/<project>/` and publishes nothing.
