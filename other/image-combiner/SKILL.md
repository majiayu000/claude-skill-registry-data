---
name: image-combiner
description: Merge two to five supplied images into one newly generated, visually coherent image while preserving the requested subjects and reconciling scale, perspective, lighting, color, depth, and occlusion. Use when elements from separate photos should naturally coexist in one scene; do not use for side-by-side collages, poster layouts, background replacement only, local retouching, simple overlays, or pixel-exact compositing.
---

# Image Combiner

Create one unified image from multiple sources. Treat the capability as a multi-reference image model plus a compact role-aware Prompt, not a temporary combiner endpoint.

## Catalog

- Display name: Image Combiner
- Categories: Layout & Design
- Status: Ready
- Route label: Multi-reference image composition
- Tone: cyan
- Short description: Merge multiple images into one coherent scene.
## What this skill does

- Assigns a clear role to every source image before generation.
- Rebuilds the sources as one scene with consistent scale, perspective, lighting, color, depth, contact, and occlusion.
- Preserves only the explicitly requested identities, objects, materials, markings, or scene features.
- Rejects pasted-on, split-screen, collage, duplicated, or visibly disconnected results.

## How to use

Attach two or more images and say which subject, environment, pose, style, or detail each image contributes.

#### Put a subject into a scene

```text
Place the product from the first image naturally into the room from the second image.
```

#### Combine people or objects

```text
Combine these two subjects into one believable photo while preserving both appearances.
```

#### Mix subject and style references

```text
Create one image using the first image as the subject and the second as the visual style.
```

## Workflow

### 1. Assign source roles

Compile only execution-changing information:

```yaml
images: 2–5 by default
roles: subject | environment | identity | pose | object | wardrobe | style | composition
output_scene: what the one new image depicts
placement: where subjects belong and how they interact
preserve: source-specific identity, shape, material, color, markings, or geometry
adapt: scale, perspective, pose, crop, lighting, shadow, color, depth, and occlusion
ratio: supplied | environment-led | auto
```

Ask only when two plausible role assignments would produce different images. Never infer that every visible source element must survive; preserve what the user names and what is necessary to recognize the requested subject.

### 2. Select the model

- Apply the shared [model-selection policy](../../shared/model-selection.md). Prefer GPT Image 2 Medium when product, person, logo, or subject consistency is central; it is also mandatory for readable typography.
- Use `nano-banana-edit` with `nano2` for fast draft divergence, or `nano` (Nano Pro) for faster high-quality convergence/internal review when exact text is absent.
- Use Seedream only when demanding lighting/material rendering or Asian commercial aesthetics are explicit and the current adapter supports every reference. Reference count alone does not justify it.
- Use a specialized combiner or mixer endpoint only when its current API contract is verified and materially improves the requested merge. The endpoint is optional, not the Skill identity.
- Default to one `1K` result with `batchCount: 1`; use the environment's ratio when it provides the destination composition, otherwise `auto`.

### 3. Compile a short Prompt

Start from the cleaned WeShop baseline:

```text
Merge these two photos together naturally. Don't simply put element on the another image, try to generate a merged photo.
```

Replace generic references with indexed roles and submit compact natural prose:

```text
Create one coherent image. Use Image 1 for [subject] and Image 2 for [environment/style/pose]. Place [subject] [relationship and position]. Preserve [short source-specific locks]. Reconcile scale, perspective, lighting, color, depth, contact shadows, and occlusion so the result looks captured as one scene. No split screen, collage, duplicate subject, pasted edges, halo, or unrelated source elements.
```

Keep the submitted Prompt concise. Do not serialize the full role card or repeat preservation details.

### 4. Generate and accept

Upload every source, execute through WeShop OpenAPI, poll to terminal state, and read the returned image.

Accept only when:

1. Exactly one unified image is returned, not a grid, split screen, before/after, or collage.
2. Every requested source contribution appears once and remains recognisable at the promised preservation level.
3. Scale, perspective, horizon, light direction, color temperature, depth, contact shadows, and occlusion agree.
4. Edges are integrated without cutout halos, floating subjects, pasted rectangles, or mismatched sharpness.
5. Unrequested source backgrounds, duplicate subjects, text, logos, or unrelated elements are absent.

### 5. Retry one failed property

Retry once with a non-identical Prompt naming only the failure:

- subject drift: shorten the scene request and strengthen that source's identity or object lock;
- pasted appearance: emphasize contact, occlusion, reflected light, edge softness, and shared depth of field;
- wrong scale or position: specify one physical anchor and relative size;
- environment drift: make the environment image the composition anchor and restrict changes to the insertion zone;
- duplication: state the exact requested count and remove unnecessary source elements;
- style mismatch: choose one source as the color/light/material authority.

Change models only for a demonstrated reference-capacity or fidelity mismatch. Do not promise pixel-exact preservation from a generative merge; route such requests to deterministic compositing instead. Record model, optional agent, parameters, Prompt revision, execution ID, error, retryability, refund state, and failed acceptance item.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One merged image and a compact acceptance record
- Default quantity: 1 separate image
- Content per image: One coherent scene containing the requested contributions from two to five sources
- Default layout: Single scene using the environment source ratio or auto
- Video output: No
- Model policy: Route the best current multi-reference image editor; specialized combiner endpoints are optional
- Downstream use: Subject-in-scene composition, multi-subject photos, concept visualization, campaign source assembly, and creative reference synthesis
