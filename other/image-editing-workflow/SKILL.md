---
name: image-editing-workflow
description: "Apply a source-preserving workflow to plan, execute, and verify image edits with the active host's approved image-editing capability. Use when the user asks for this workflow or needs an additional edit-validation pass; never switch providers or upload images automatically. Turkish triggers: görseli düzenle, arka plan veya kıyafet değiştir, rötuş ve varyasyon, kimliği koru."
license: MIT
---

# Portable Image Editing

## 1. Inspect

View the source at adequate resolution. Record dimensions, color profile, alpha, orientation, compression, visible text, protected identity/features, and likely privacy/copyright concerns. Keep the original untouched.

## 2. Define the edit contract

State:

- what must change;
- what must remain identical;
- edit region or mask;
- output size/aspect/format/transparency;
- realism/style and lighting perspective;
- text spelling/language if applicable;
- acceptance criteria and allowed variation.

For people, explicitly preserve identity, anatomy, skin texture, age cues, pose, and expression unless the request changes them. Avoid inferring or altering sensitive traits.

## 3. Choose an available path

Use an image-edit tool already exposed by the active host, an installed local workflow, or a provider the user already authorized. Do not choose a provider/model, spend credits, install a CLI, or upload a private image merely because a reusable skill names one. If no suitable capability exists, produce the edit plan/prompt and clearly state the missing tool.

Use masks for localized changes. Prefer one controlled edit over broad regeneration when preservation matters. For text replacement, specify exact text, location, alignment, type character, and unchanged surroundings.

## 4. Iterate conservatively

Change one major factor per iteration. Keep source, mask, prompt/parameters, seed when available, and outputs. Do not repeatedly regenerate after the acceptance criteria are met.

## 5. Verify

Compare source and output at full image and 100% crops. Check protected regions, seams, edges, hands/faces, reflections, shadows, geometry, repeated textures, text accuracy, color profile, alpha, dimensions, and compression. Ensure removed content is not visibly retained when the request requires removal.

Report tool/path used, edit contract, output file, checks performed, deliberate deviations, and whether the image left the local machine.
