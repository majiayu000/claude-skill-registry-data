---
name: transferring-styles
description: Compiles a Visual Intent Object into a ComfyUI img2img style-transfer prompt JSON by patching a low-denoise image-to-image template with the caller's style prompt. Use whenever the planner emits a step with goal=transfer_style, or when the user wants to apply a specific style to an existing image without changing its composition.
v1_2_match:
  kinds: [comfyui_execute]
  capability: transferring-styles
v1_2_output: diff_patch
---

# transferring-styles

Template+patch Skill for img2img style transfer.

## When this Skill applies
- Planner step with `{goal:"transfer_style"}`.
- Optional `preserve:["face"]` constraint — the Skill does not enforce it
  (downstream `preserving-faces` does), but this Skill lowers `denoise` to
  0.45 when the constraint is present.

## Intent overrides
| VIO | Node.input |
|---|---|
| `prompt` | `6.inputs.text` |
| `negative_prompt` | `7.inputs.text` |
| `inputs.image` | `10.inputs.image` |
| `params.denoise` | `3.inputs.denoise` (default 0.55, 0.45 when preserving face) |
| `params.steps`/`cfg`/`sampler_name`/`scheduler`/`seed` | standard |
| `model.checkpoint` | `4.inputs.ckpt_name` |
