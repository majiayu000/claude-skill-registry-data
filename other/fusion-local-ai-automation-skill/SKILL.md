---
name: fusion-local-ai-automation-skill
description: Automate offline mechanical CAD and validated CAM work in Autodesk Fusion desktop through a local file bridge. Use for geometry inspection, parameter edits, planar-face cuts, local exports, face-milling setup changes, and toolpath regeneration on Windows; complete CAD validation before CAM.
---

Read `AGENTS.md` and `SETUP.md` before operating Fusion. This skill is self-contained: its Fusion add-in is under `fusion-addin/LocalCADBridge`, and its local client is `scripts/cad_client.py`. The bridge uses the installed `adsk.core`, `adsk.fusion`, and `adsk.cam` modules inside Fusion. The external Python client only exchanges request/result files with that add-in.

Keep Fusion in Work Offline mode. Operate only on a new document or a workspace-local `.f3d`/STEP file imported by the bridge into a new unsaved document. Never adopt an arbitrary active document, call Fusion cloud/data APIs, use cloud project identifiers, or invoke document save/saveAs. Preserve inputs and write checkpoints, exports, reports, and images under `artifacts/`.

For CAD, follow `skills/fusion-local-cad/SKILL.md`. Complete its full import/create, inspect, checkpoint, mutate, recompute, measure, image, native/STEP export, native reopen, persistence, second-edit, and rollback gate before working on CAM for that part.

For CAM after the CAD gate, follow `skills/fusion-local-cam/SKILL.md`. The verified strategy is face milling with an installed local sample tool. Treat sample feeds, spindle speeds, stock, and timing inputs only as software-test values. Do not claim machine simulation, collision clearance, post selection, NC output, or physical-machine readiness without separate implementation and validation.

Use fresh session and revision identifiers for every mutation. Serialize requests. A timeout does not cancel a request or generation job; inspect the original result or poll the original job ID before deciding whether to retry. Require explicit geometry and toolpath postconditions rather than relying on screenshots or a single API status flag.

The supported test chain and public installation instructions are in `SETUP.md`. `STATUS.md` records the scope actually validated against desktop Fusion. Extend CAD features or CAM strategies only with a bounded acceptance case and update the stated scope after it passes.
