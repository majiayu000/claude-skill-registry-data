---
name: photo-to-cute-3d-toy
description: Create cute 3D toy assets from photo-reference manifests. Use when Codex needs to turn scene photos into 2D toy concept prompts, choose a photo-to-3D route, produce or plan GLB assets for Three.js, or maintain a repeatable personal-gift/toy-character generation workflow.
---

# Photo To Cute 3D Toy

## Purpose

Turn a scene manifest into a repeatable pipeline:

1. map photos to roles such as `face`, `outfit`, `pose`, `mood`, and `mainPhoto`;
2. write a 2D cute-toy concept prompt pack;
3. choose a 3D generation route;
4. deliver frontend-ready concept images and GLB assets without leaking privacy, IP, or unsupported completion claims.

## Workflow

1. Read the project scene manifest first. If none exists, create one from `references/manifest.md`.
2. Inspect the referenced photos and state the role of each photo before generating anything.
3. Write a prompt pack using `references/prompting.md`.
4. Choose a route using `references/routes.md`.
5. Deliver assets using `references/delivery.md`.
6. Validate outputs. If a concept image or GLB was not actually generated, say so plainly and provide the next command/service step.

## Required Boundaries

- Use original style language such as `soft plush`, `blind-box proportions`, `designer collectible toy`, or `cute stylized figurine`; do not name or imitate protected toy IPs.
- Do not use celebrity likenesses, artist names, brand logos, readable protected marks, or copyrighted stage text in generated assets.
- Treat private photos as sensitive. If an external service is used, report the exact service/model and which input images were uploaded.
- Do not download large model weights, install CUDA stacks, or run long local jobs without explicit user approval.
- Do not claim a `GLB` is complete unless a real file exists and passes at least a basic GLB/GLTF validation.
- Do not modify the frontend unless the user explicitly assigns frontend integration. Hand off paths and manifest fields instead.

## Scripts

Use `scripts/build_prompt_pack.py` to validate one scene and emit a Markdown prompt pack:

```powershell
python scripts/build_prompt_pack.py `
  --manifest .\toy-scenes.manifest.json `
  --project-root . `
  --scene sence5 `
  --out .\sence5-prompt-pack.md
```

The script only uses the manifest and filesystem checks. It does not upload photos or call AI services.

## References

- Manifest schema and example: `references/manifest.md`
- 2D concept prompt templates: `references/prompting.md`
- 3D route selection: `references/routes.md`
- Frontend delivery and validation: `references/delivery.md`
