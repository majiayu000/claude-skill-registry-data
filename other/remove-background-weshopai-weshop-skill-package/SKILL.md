---
name: remove-background
description: Remove the background from one supplied image and return a true transparent PNG while preserving the complete foreground subject and clean alpha edges. Use for transparent product cutouts, people or pet cutouts, foreground extraction, background erasing, PNG isolation, compositing assets, and optional solid-color output; do not use for replacing a background with a generated scene, redesigning the subject, or ordinary white-background product photography.
---

# Remove Background

Extract one foreground subject without regenerating it. Treat transparency and edge cleanliness as hard acceptance requirements, not optional polish.

## Catalog

- Display name: Remove Background
- Kind: Atom
- Categories: Utility
- Status: Ready
- Featured: yes
- Route label: WeShop RemoveBG with alpha-edge QA
- Tone: mint
- Short description: Create a clean transparent PNG cutout.

## What this skill does

- Removes one image background with a dedicated segmentation endpoint.
- Returns a PNG containing a real alpha channel by default.
- Preserves foreground pixels, count, internal openings, fine edges, and original dimensions.
- Checks the cutout on black, white, and checkerboard backgrounds to expose dirty mask edges.
- Uses a supplied custom mask only when automatic subject segmentation fails.

## How to use

Provide one image and say what must remain.

#### Isolate a product

```text
Remove the background and return this bag as a transparent PNG.
```

#### Keep one selected subject

```text
Cut out only the chair on the right and keep its complete legs and openings.
```

#### Prepare a compositing asset

```text
Make this person a transparent cutout with clean hair edges.
```

## Workflow

### 1. Bind the foreground

Require one source image. Record the exact subject or connected subject group to preserve, foreground count, important internal holes, fine structures, semi-transparent materials, contact shadow policy, and requested output.

Default to transparent PNG. A solid `backgroundHex` is an optional delivery variant, not proof that background removal succeeded. Route generated scene replacement to the owning background-edit or product-scene Skill.

Read [references/routing-and-api.md](references/routing-and-api.md) before execution and [references/acceptance.md](references/acceptance.md) before accepting any result.

### 2. Select the mask route

- **Default:** query current `removeBG` agent info, resolve the background preset whose name is exactly `Transparent`, pass its returned ID as `backgroundId`, use `maskType: "autoSubjectSegment"`, and set `batchCount: 1`. The verified ID was `306` on 2026-08-19, but names are the durable contract and IDs may change.
- **User-supplied mask:** call `maskType: "custom"` with the real `customMaskUrl`.
- **Automatic mask failure:** do not switch to a generative image model. Obtain or construct one corrected custom mask and retry once.
- **Solid-color request:** first preserve the transparent master; use `backgroundHex` only for an additional flattened delivery when requested.

The endpoint exposes no Prompt field. Do not invent `textDescription`.

### 3. Execute once

Upload a local source when required, submit one run, and poll to terminal state. API `Success` is not visual acceptance.

Preserve source width and height. If the endpoint trims only a few outer transparent pixels, restore the original canvas with transparent padding and verified symmetric offsets; never resample the subject. Never crop, reconstruct, smooth, or recolor the foreground merely to hide a weak mask.

### 4. Verify true transparency

Run:

```text
python scripts/inspect_alpha.py RESULT.png --preview-dir QA
```

Reject the result when it lacks an alpha channel, has no fully transparent background pixels, is merely flattened onto white, or changes the source canvas size. Deliver the original transparent PNG; previews are QA derivatives only.

### 5. Inspect mask edges

Inspect the generated white, black, and checkerboard previews at 100% and enlarged edge crops when necessary.

Check:

- no white, dark, green, blue, or original-background halo;
- no missing fringe, hair, fur, lace, mesh, strap, antenna, handle, or thin product part;
- no opaque background islands or transparent holes inside solid material;
- preserve legitimate openings between handles, limbs, spokes, laces, or furniture legs;
- keep semi-transparent material as graded alpha when supported;
- keep or remove contact shadow only according to the bound policy.

Do not accept a binary-looking silhouette merely because the central subject remains recognizable.

### 6. Retry one failed property

- wrong foreground selection or missing connected part: correct one custom mask and retry once;
- dirty colored fringe: refine only the alpha/foreground edge with a non-generative matting or color-decontamination step when available;
- small mask islands: remove only verified disconnected background components;
- missing alpha: correct output parameters or file handling; do not convert a white JPEG to PNG and call it transparent;
- unresolved hair, fur, glass, smoke, veil, or motion blur: report the unsupported edge instead of regenerating the subject.

Never run a progressive model ladder or repeat an identical request.

## User-facing output

- Media type: One lossless transparent PNG
- Default quantity: 1 separate image
- Default route: `removeBG` v1.0 automatic subject segmentation with the live `Transparent` preset
- Required verification: Alpha-channel inspection plus black, white, and checkerboard edge previews
- Optional output: One additional solid-color composite when explicitly requested
- Downstream use: Product compositing, posters, banners, collages, packaging layouts, and scene placement
