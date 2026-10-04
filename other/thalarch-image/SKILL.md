---
name: thalarch-image
description: >
  Routes and governs image-centric work across generation, editing, inspection,
  comparison, annotation, screenshots, branding, raster assets, vector assets,
  diagrams, infographics, mockups, and export validation. Use whenever an image
  is an input, output, reference, acceptance artifact, or major source of truth.
  Chooses the correct host-supported visual workflow before generation or editing begins.
---

# Thalarch Image

Images are first-class engineering artifacts. Treat them with the same discipline as code: define
the contract, choose the right production path, preserve invariants, and verify the actual output.

## 1. Classify the visual task

Choose one primary mode before acting:

- `inspect` — understand an existing image or screenshot;
- `generate` — create a new raster visual from text/references;
- `edit` — change a specific part of an existing image;
- `compose` — combine multiple source images;
- `vector` — logo, icon, diagram, or geometry that should remain code-native;
- `capture` — browser/app/system screenshot used as evidence;
- `compare` — before/after or reference-vs-output fidelity;
- `annotate` — callouts, arrows, labels, highlights;
- `optimize` — format, size, alpha, crop, compression, or export cleanup.

Do not route every visual task through generative image creation.

## 2. Discover visual capabilities

Before choosing a production path, inspect what the **current host/session** actually exposes:

- image generation/editing;
- image viewing/inspection;
- browser screenshot/recording;
- device/emulator capture;
- filesystem/code-native SVG or canvas creation;
- deterministic image-processing scripts.

A capability available in Antigravity is not automatically available in Codex or Claude Code, and
vice versa. Never fabricate a visual tool or subagent name.

If the acceptance criterion requires a capability that is unavailable, use the strongest safe
fallback and keep the affected claim `UNVERIFIED`.

## 3. Choose the production path

Prefer the most deterministic medium that fits the deliverable:

- **host-provided image generation/editing** for raster generation and semantic image edits when an
  actual compatible tool is available;
- **SVG / HTML / canvas / repository-native vector code** when exact geometry, typography,
  editability, or scalable logos/icons matter;
- **real browser screenshot tooling** for web UI evidence rather than recreating UI as generated art;
- **device/emulator capture** for mobile runtime evidence when available;
- **deterministic annotation/image-processing scripts** for callouts, dimensions, alpha, crops, and
  measurable comparisons.

A generated bitmap is not a substitute for an SVG when the product needs a real vector asset.

## 4. Visual acceptance contract

For meaningful image work establish the fields that matter:

- purpose / destination;
- asset type;
- target file format;
- target dimensions or aspect ratio;
- safe zones / crop behavior;
- background and transparency requirements;
- exact text, if any;
- subject and composition;
- style / medium;
- palette / brand constraints;
- reference images and each reference's role;
- invariants that must not change;
- forbidden/unwanted elements;
- required variants;
- verification evidence.

If a field does not matter, leave it unspecified instead of inventing decorative requirements.

## 5. Reference-image roles

Never assume every attached image is an edit target.

Label references explicitly:

- `edit target`;
- `style reference`;
- `composition reference`;
- `identity/character reference`;
- `brand/palette reference`;
- `content/source reference`;
- `comparison baseline`.

When several images are used, preserve their numbering and role in every generation/edit brief.

## 6. Exactness hierarchy

Some properties need different proof:

- **semantic appearance** → visual inspection;
- **exact wording** → read rendered text back;
- **pixel dimensions** → metadata probe;
- **transparency** → alpha-channel check;
- **before/after fidelity** → same-size comparison and visual diff;
- **brand palette** → source/design tokens plus rendered inspection;
- **layout geometry** → prefer vector/code-native production or deterministic overlays when
  precision matters.

Do not claim a visual property from the prompt alone.

## 7. Asset hygiene

- Use semantic filenames.
- Preserve source/reference files unless replacement was requested.
- Do not overwrite the only original during experimentation.
- Keep exploratory outputs out of production asset paths.
- Do not silently change format, crop, color profile, or transparency.
- Avoid embedding secrets, local paths, private metadata, or unrelated EXIF data.
- For repository assets, inspect file size and intended delivery cost.

## 8. Handoff by capability

For generation/editing, use `thalarch-imagegen` plus a real host-supported image capability.

For final inspection, before/after comparison, dimensions, alpha, text, annotations, or visual
evidence use `thalarch-visual-qa` and whatever actual image inspection/runtime tools exist.

For product UI combine with `thalarch-ui`, `thalarch-browser-qa`, and real browser/device evidence
when those capabilities are available.

Do not phrase an unavailable handoff as if it executed. Missing capability becomes explicit
`UNVERIFIED` evidence, not an invented specialist result.
