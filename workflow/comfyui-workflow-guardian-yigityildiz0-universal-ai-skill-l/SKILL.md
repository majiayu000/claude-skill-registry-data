---
name: comfyui-workflow-guardian
description: "Automatically audit, repair, refactor, and stabilize an existing ComfyUI workflow or Windows runtime when the user shares workflow JSON, an error/screenshot, or reports startup/queue failure, `Failed to fetch`, missing nodes/models, broken links, overlap, identity drift, LoRA/model-order problems, VRAM/speed instability, or wants to integrate identity/refiner/post-processing modules without breaking the primary workflow. Validate before and after, preserve backups and working branches, and prefer one evidence-based change at a time. Use comfyui-workflow to design a new pipeline from scratch. Turkish triggers: ComfyUI workflow düzelt, JSON veya node hatası, VRAM/kimlik/bağlantı sorunu, güvenli onarım."
---

# ComfyUI Workflow Guardian

Use this skill to work on ComfyUI like an infrastructure and workflow engineer, not like an improvising prompt tweaker.

## Core Rules

- Back up the target workflow before editing it.
- Change only the workflow the user explicitly names. Do not sync other workflows unless asked.
- Inspect runtime failures before editing the workflow. A dead backend is not a workflow bug.
- Prefer one precise change over many speculative changes.
- Keep optional modules behind switches so they do not add cost when disabled.
- Preserve working post-processing sections unless the user explicitly wants them changed.
- Prefer validated architecture rules over folklore or one-off community claims.

## Workflow

### 1. Classify the task

Classify the request before touching files:

- **Runtime failure**: startup crash, queue crash, `Failed to fetch`, access violation, provider error
- **Structure failure**: broken links, missing files, overlapping nodes/groups, unreadable layout
- **Quality failure**: identity drift, anatomy defects, artifacts, color shifts, over-smoothing
- **Performance failure**: generation too slow, unnecessary modules active, too many second-pass steps
- **Architecture change**: adding or comparing LoRAs, identity modules, refiners, control branches

### 2. Read the right reference file

- Read [references/runtime-profile.md](references/runtime-profile.md) first when machine-specific paths, hardware, models, launchers, or workflow locations matter.
- Read [references/runtime-performance.md](references/runtime-performance.md) for crashes, access violations, performance regressions, or backend instability.
- Read [references/identity-modules.md](references/identity-modules.md) for BFS, PuLID, LanPaint-style face transfer, or identity-preservation tasks.
- Read [references/workflow-editing-checklist.md](references/workflow-editing-checklist.md) before editing workflow JSON.
- Read [references/provenance-and-recovery.md](references/provenance-and-recovery.md) for API-format validation, output provenance, missing-model checks, and timeout recovery.

### 3. Validate before editing

Run the bundled checker on the target workflow:

```powershell
python scripts/check_comfyui_workflow.py "<WORKFLOW_PATH>" --comfy-root "<COMFYUI_ROOT>"
```

Use it before and after edits. Treat these as hard failures until explained:

- missing node references
- missing model or LoRA files
- overlapping nodes
- overlapping groups

### 4. Apply architecture rules

Follow these stable ordering rules unless source documentation for a specific module contradicts them:

- Put the **base model loader** first.
- Put **general LoRAs that shape the base image** before the main sampler.
- Put **identity model layers** after the general LoRA chain when they modify the final model directly.
- Put **second-pass face-transfer or inpainting systems** after the base image is generated.
- Put **detail or sharpening passes** after identity transfer, not before.
- Keep **manual size overrides, CFG, and quality toggles** in a compact quick-access area, but leave original nodes in place if the workflow already depends on them.

### 5. Change conservatively

- Tighten one branch at a time.
- If a post-pass copies unwanted props, hands, or expressions, reduce what that pass is allowed to transfer instead of raising its strength blindly.
- If identity is weak, test the identity modules separately before combining them.
- If performance is poor, reduce second-pass cost before degrading the main generation stage.
- Do not switch models, precision modes, or providers without evidence that the current setting is the cause.

### 6. Validate after editing

After edits:

- run the workflow checker again
- confirm the target files exist on disk
- confirm the launcher and runtime still start
- confirm the active workflow still loads cleanly
- summarize only the actual changes, default values, and residual risks

## Operating Defaults

Use these defaults when the user does not specify otherwise:

- Keep the user's main workflow as the only edit target.
- Keep runtime changes conservative and stability-first unless the user prioritizes speed or another objective.
- Treat second-pass identity transfer as optional and isolated.
- Favor clean, non-overlapping layout and short notes over decorative complexity.
- Favor explicit validation over guesswork.

## Output Requirements

When finishing a task with this skill:

- name the exact files changed
- name the critical node or runtime settings changed
- state what was validated
- state what remains uncertain
