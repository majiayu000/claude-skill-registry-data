---
name: generating-images
description: Compiles a Visual Intent Object into a ComfyUI txt2img prompt JSON using a bundled SDXL or FLUX template. Use whenever the planner emits a step with goal=generate, or when an agent needs a one-step image-from-text pipeline.
v1_2_match:
  kinds: [comfyui_execute]
  capability: generating-images
v1_2_output: diff_patch
---

# generating-images

Template + patch Skill for text-to-image. No LLM emits graph JSON — `compile.py`
applies a flat override map from the Visual Intent Object onto a bundled
template and writes the result to stdout. Pipe into `comfyui-execution`'s
`submit_prompt.py`.

## When this Skill applies

- The planner produced a step with `{goal: "generate"}`.
- A caller wants a one-shot txt2img from a natural-language prompt.

## Templates

- `templates/txt2img-sdxl.json` — SDXL base, 1024², euler/normal, cfg 7.
- `templates/txt2img-flux.json` — FLUX.1-schnell variant.

Template selection: VIO `model.checkpoint` hint containing "flux" picks
`txt2img-flux.json`; otherwise `txt2img-sdxl.json`.

Provenance in `templates/PROVENANCE.md`.

## Intent overrides honored

| VIO field | Node.input |
|---|---|
| `prompt` | `6.inputs.text` |
| `negative_prompt` | `7.inputs.text` |
| `params.width` / `params.height` | `5.inputs.width` / `height` |
| `params.steps` | `3.inputs.steps` |
| `params.cfg` | `3.inputs.cfg` |
| `params.sampler_name` | `3.inputs.sampler_name` |
| `params.scheduler` | `3.inputs.scheduler` |
| `params.seed` | `3.inputs.seed` (-1 → random via time) |
| `model.checkpoint` | `4.inputs.ckpt_name` |

## Scripts

- `scripts/compile.py` — stdin: VIO JSON; stdout: prompt JSON. stdlib only.

## Errors

Bad VIO → `{"error":"...","code":"..."}` on stdout, exit 2.

## References

- `knowledge/workflows/ComfyUI_workflow.md` §3 (prompt JSON shape)
- `../planning-visual-tasks/reference/intent-schema.md`
