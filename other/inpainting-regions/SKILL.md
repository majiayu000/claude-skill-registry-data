---
name: inpainting-regions
description: Compiles a Visual Intent Object into a ComfyUI inpaint prompt JSON using an SDXL LoadImage+VAEEncode+SetLatentNoiseMask template. Use whenever the planner emits a step with goal=inpaint, or when the user wants to edit a region of an existing image defined by a mask.
v1_2_match:
  kinds: [comfyui_execute]
  capability: inpainting-regions
v1_2_output: diff_patch
---

# inpainting-regions

Template+patch Skill for masked inpainting.

## When this Skill applies
- Planner step with `{goal:"inpaint"}`.
- Caller has an input image and a mask PNG.

## Intent overrides
| VIO | Node.input |
|---|---|
| `prompt` | `6.inputs.text` |
| `negative_prompt` | `7.inputs.text` |
| `inputs.image` | `10.inputs.image` |
| `inputs.mask` | `11.inputs.image` |
| `params.steps`/`cfg`/`sampler_name`/`scheduler`/`seed` | `3.inputs.*` |
| `params.denoise` | `3.inputs.denoise` |
| `model.checkpoint` | `4.inputs.ckpt_name` |

## Scripts
- `scripts/compile.py` — VIO → inpaint prompt JSON.
