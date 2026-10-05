---
name: comfyui-workflow
description: Generate and debug ComfyUI workflow JSON files for FLUX, SDXL, SD3, Wan2.2, img2img, txt2img, txt2vid, img2vid, LoRA, ControlNet, IPAdapter, inpaint, and.
---

# ComfyUI Workflow

Use this skill when the user wants to create, modify, compare, or troubleshoot a ComfyUI workflow.

## Goals

- Generate valid ComfyUI workflow JSON files
- Start from the closest template in `templates/` whenever possible
- Use `references/` to check node names, inputs, outputs, defaults, and constraints
- Keep explanations short and practical
- Prefer working solutions over theory

## What to gather first

Before generating a workflow, identify:

1. Task type  
   - txt2img
   - img2img
   - txt2vid
   - img2vid
   - inpaint
   - upscale
   - control workflow
   - identity-preserving edit

2. Model family  
   - FLUX
   - SDXL
   - SD3
   - Wan 2.2
   - HunyuanVideo
   - LTXV
   - Mochi
   - Cosmos
   - other

3. Key settings  
   - resolution
   - steps
   - CFG
   - sampler
   - seed behavior

4. Optional modules  
   - LoRA
   - ControlNet
   - IPAdapter
   - PuLID
   - upscaler
   - face/detail nodes

5. Prompt inputs  
   - positive prompt
   - negative prompt
   - trigger words if a LoRA is used

If the user is vague, suggest a sane default configuration.

## Workflow generation rules

- Use the closest file in `templates/` as the base whenever possible
- Adapt the template instead of building everything from zero unless necessary
- Output valid ComfyUI LiteGraph UI JSON
- Include a short explanation of the pipeline
- List required custom nodes
- List required model files
- Mention likely missing dependencies if relevant

## Debugging rules

When the user shares a broken workflow, console error, or screenshot, troubleshoot in this order:

1. Missing model files
2. Missing custom nodes
3. Wrong node connections
4. Wrong widget values
5. Incompatible model family
6. VAE / text encoder mismatch
7. LoRA placement or wrong trigger usage
8. ControlNet / IPAdapter / PuLID integration mistakes
9. Unsupported or outdated node names
10. Resolution / VRAM / precision issues

## FLUX-specific checks

For FLUX workflows, always verify:

- correct model loader path
- text encoder setup
- VAE compatibility
- LoRA attachment points
- filename consistency
- sampler path
- output node presence

## Output style

- Be concise
- Give the final workflow first if the request is clear
- Then list required models and custom nodes
- If debugging, first state the most likely cause
- Then give the fastest fix
- Then give the clean long-term fix

## Examples

- Generate a FLUX txt2img workflow with LoRA support
- Build a Wan 2.2 img2vid workflow with camera control
- Debug this ComfyUI workflow JSON
- Add PuLID and identity-preserving editing to this FLUX workflow
- Compare two workflows and explain which one is more stable
