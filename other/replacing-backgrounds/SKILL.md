---
name: replacing-backgrounds
description: Compiles a Visual Intent Object into a ComfyUI background-replacement prompt JSON by driving the inpaint template with a background mask. Use whenever the planner emits a step with goal=replace_background, or when the user wants to swap the backdrop of an image while keeping the subject.
v1_2_match:
  kinds: [comfyui_execute]
  capability: replacing-backgrounds
v1_2_output: diff_patch
---

# replacing-backgrounds

Template+patch Skill for background swap. Uses the inpaint mechanism with a
background-region mask and high denoise.

## When this Skill applies
- Planner step with `{goal:"replace_background"}`.
- The caller must supply a mask PNG covering the background (the region to
  regenerate). If no mask is provided, the caller should first run a matting
  step.

## Intent overrides
| VIO | Node.input |
|---|---|
| `prompt` (new bg description) | `6.inputs.text` |
| `negative_prompt` (subject keywords to protect) | `7.inputs.text` |
| `inputs.image` | `10.inputs.image` |
| `inputs.mask` | `11.inputs.image` |
| `params.*`, `model.checkpoint` | standard |

## Scripts
- `scripts/compile.py` — VIO → prompt JSON.
