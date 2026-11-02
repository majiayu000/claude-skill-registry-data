---
name: image-studio
description: Draw original images with local Canvas/Python or seeded p5.js; use a user-hosted ComfyUI backend for photographic synthesis, retouching and upscaling.
priority: P1
category: media
status: builtin-guidance
---

# Image Studio

**Scope:** local code graphics and optional local ComfyUI.
**Community sources:** Canvas Design and Algorithmic Art by Anthropic, available as `community-canvas-design` and `community-algorithmic-art` in the Remote Arc Skills catalog.
**Model backend:** https://github.com/Comfy-Org/ComfyUI

## Choose the output workflow

For posters, covers, diagrams, editorial graphics, abstract art or generative patterns, use code graphics first: Canvas/Python for composed static work, or the packaged Algorithmic Art/p5.js workflow for seeded, interactive systems. These do not require an image model, GPU model download or paid image API. Read the selected skill and its resources, then create the actual local artifact.

For photographic synthesis, editing supplied photographs or model-based upscaling, check the user's local ComfyUI endpoint, compatible accelerator and existing model weights first. ComfyUI and weights are not bundled. Ask before downloading model weights or using a paid provider; there is no default GPU/cloud/API spending. Keep the endpoint on loopback and never expose it publicly without authentication. If no suitable backend exists, explain the missing dependency and do not claim a photograph was generated.

## Local code graphics

1. Confirm size, intended use, required text and whether the user wants a static image or an interactive generator.
2. Read Canvas Design or Algorithmic Art and the relevant resources. Materialize needed text resources in the authorized project folder. Use a local renderer; automatically prepare ordinary lightweight libraries within existing authorization.
3. Use local fonts. Canvas Design includes font license texts and a pinned font manifest, with optional binaries downloaded into the artifact workspace and checked against SHA-256. Never send a font binary through a UTF-8 text resource.
4. Keep algorithms seeded where applicable, expose meaningful parameters and make every visible control work. For offline viewers, embed or locally serve p5.js and fonts rather than relying on a CDN at viewing time.
5. Render an actual PNG/PDF, inspect it at useful resolution for clipping, text, composition and artifacts, and retain editable drawing code, seed and brief. Test export and same-seed reproduction for interactive art.
6. Describe code illustrations as code illustrations. Do not imply they were produced by a diffusion model or are photographs.

## Device and permission gates

Required authorization scopes: computer:read, computer:write. Execution uses existing device tools and current workspace permissions. Paid APIs, model weights and unrelated external side effects need their own authorization. This skill does not elevate Remote Arc Tool privileges or authorize hidden credentials.

## Preflight

A packaged Skill is guidance and resources, not proof of an installed engine. Check the chosen local renderer and fonts before relying on them. Avoid unnecessary model installation when code graphics satisfy the request.

## Evidence of completion

Report the actual file, dimensions, device and renderer; include editable source, seed when used and checks actually completed. Model-based work also identifies the backend and model. Distinguish rendering from visual verification and never imply execution succeeded from a plan alone.
