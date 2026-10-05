---
name: ai-image-video-studio
description: "AI image/video: ComfyUI workflows and fixes (FLUX, SDXL, Wan, LoRA), product photos, image edits, video QA. ComfyUI workflow yap, node eksik, görseli düzenle."
---

# AI Image & Video Studio

## Choose the module

| Need | Module |
|---|---|
| New ComfyUI workflow or capability (FLUX, SDXL, SD3, Wan, Hunyuan, LTXV, Mochi, Cosmos, LoRA, ControlNet, IPAdapter, PuLID, inpaint, upscale, txt2vid, img2vid) | `comfyui-workflow` |
| Existing ComfyUI JSON, runtime/startup error, missing nodes/models, `Failed to fetch`, VRAM/speed, identity drift, adding a module without breaking the main flow | `comfyui-workflow-guardian` |
| AI product photos, packshots, lifestyle scenes, e-commerce image sets | `product-photography` |
| Edit an existing image while preserving identity and details | `image-editing-workflow` |
| Check a rendered video or export (resolution, fps, audio, subtitles, frames) | `video-delivery-qa` |

Banners, brand identity and social graphics → the separate ui-ux-pro-max family skills (`banner-design`, `brand`, `design`).

## Shared rules

- Use the ComfyUI MCP or local API tools when connected; otherwise produce files the user can load.
- Start from a validated template; output valid JSON; list exact models and custom nodes with sources.
- Back up before editing a working workflow; prefer the smallest fix; never delete user models or outputs.
- Preserve faces, logos, text and product details exactly; never upload personal images to a new provider without consent.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `comfyui-workflow` | Automatically design or substantially modify a ComfyUI workflow when the user wants a new image/video pipeline or capability for FLUX, SDXL, SD3, Wan, Hunyuan, LTXV, Moc… | [MODULE.md](modules/comfyui-workflow/MODULE.md) |
| `comfyui-workflow-guardian` | Automatically audit, repair, refactor, and stabilize an existing ComfyUI workflow or Windows runtime when the user shares workflow JSON, an error/screenshot, or reports … | [MODULE.md](modules/comfyui-workflow-guardian/MODULE.md) |
| `product-photography` | Plan, generate, edit, or review AI product photography for e-commerce, packaging, ads, catalogs, and product launches. | [MODULE.md](modules/product-photography/MODULE.md) |
| `image-editing-workflow` | Apply a source-preserving workflow to plan, execute, and verify image edits with the active host's approved image-editing capability. | [MODULE.md](modules/image-editing-workflow/MODULE.md) |
| `video-delivery-qa` | Inspect, validate, and prepare video deliverables for export or handoff using available local tools such as ffprobe, frame sampling, waveform/audio inspection, captions,… | [MODULE.md](modules/video-delivery-qa/MODULE.md) |

Supporting files (open only when the module points to them):

- `comfyui-workflow-guardian`: [identity-modules.md](modules/comfyui-workflow-guardian/references/identity-modules.md), [provenance-and-recovery.md](modules/comfyui-workflow-guardian/references/provenance-and-recovery.md), [runtime-performance.md](modules/comfyui-workflow-guardian/references/runtime-performance.md), [runtime-profile.md](modules/comfyui-workflow-guardian/references/runtime-profile.md), [source-notes.md](modules/comfyui-workflow-guardian/references/source-notes.md), [workflow-editing-checklist.md](modules/comfyui-workflow-guardian/references/workflow-editing-checklist.md); scripts: `modules/comfyui-workflow-guardian/scripts/check_comfyui_workflow.py`
