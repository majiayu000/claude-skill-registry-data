---
name: preserving-faces
description: Composable sub-Skill that compiles a face-locking ComfyUI prompt JSON by re-rendering the non-face region at very low denoise while leaving the face mask untouched. Use whenever the planner emits a step with goal=preserve_face, or whenever a previous step's output must keep the same face across a subsequent style transfer, inpaint, or background replacement.
v1_2_match:
  kinds: [comfyui_execute]
  capability: preserving-faces
v1_2_output: diff_patch
---

# preserving-faces

Composable sub-Skill. Given an image and a face mask, emits a prompt that
regenerates only the non-face region at low denoise, keeping the face
pixel-stable.

## When this Skill applies
- Planner step with `{goal:"preserve_face"}`.
- Or as a "seal" step after `transferring-styles` / `inpainting-regions`
  when identity drift is a risk.

## Intent overrides
| VIO | Node.input |
|---|---|
| `prompt` | `6.inputs.text` |
| `negative_prompt` | `7.inputs.text` |
| `inputs.image` | `10.inputs.image` |
| `inputs.mask` (face region) | `11.inputs.image` |
| `params.denoise` | `3.inputs.denoise` (default 0.25) |
| `params.*`, `model.checkpoint` | standard |

## Notes
`preserving-faces` is *composable*: its output can be piped directly into a
downstream step or used standalone. The downstream evaluator
`evaluating-identity-preservation` validates the result.
