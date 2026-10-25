---
name: photoshop-raster-to-layered-psb
description: Convert one or more flat raster images into original-size editable Photoshop PSD or PSB files with auditable semantic layers, repaired backgrounds, extracted editable text, local font-library matching, and print-ready JPEG copies. Use for AI拆图、地图或版式图分层、图例蒙版移除补全、文字转真实Photoshop文字层、或批量JPG到可编辑PSB。Do not use for a simple one-layer photo retouch.
---

# 位图拆层生成可编辑 PSB

Produce a usable editing master, not a stack of visually similar opaque images. Preserve the source, isolate inferred content, and state what remains uncertain.

## Scope and pilot

- Inventory the actual files first. Treat every source image as an independent document even when they share one folder.
- Freeze source dimensions, resolution, color mode, file hash, output path, and no-overwrite boundary before processing.
- For a homogeneous batch, complete one representative image through save, reopen, text editability, clean-background, and print-JPEG acceptance before applying the recipe to the remaining files.
- Preserve accepted files. A second pass handles only failed images or layers; a shared workflow defect returns to the pilot instead of replaying the whole batch.

## Layering contract

- Reuse exact source pixels wherever the source contains them. Prefer a native duplicate of the source with a user mask over a round-trip through PNG for original-pixel layers.
- Put generated occlusion repair in a separate layer named as AI completion and explicitly mark it as non-survey or non-source evidence where relevant.
- Keep a hidden, locked original reference and a visible locked calibration layer that reproduces the untouched source by default.
- Upper elements such as project masks, boundaries, symbols, title blocks, legends, north arrows, and scale bars must be independently switchable when the source supports a meaningful split.
- Read [the layer and acceptance contract](references/layer-contract.md) before assembling a production PSD or PSB.

## Editable text

- OCR alone is not text reconstruction. Detect line polygons, per-character boxes, text, and OCR confidence.
- Scan the local font library before choosing fonts. Render each supported candidate, compare glyph masks to the source crop, apply semantic filtering to exclude symbol-font coincidences, and retain the first candidate, runner-up, error, and confidence gap.
- Only after choosing the relative best font, estimate point size from pixel height and document DPI, horizontal scale from glyph width, tracking from the remaining line width and character centers, weight from a real font face when possible, and color from the foreground cluster.
- Write real Photoshop point-text layers. Keep OCR confidence separate from font-fit confidence and label low-confidence results for correction.
- Calibrate against Photoshop-rendered layer bounds, because Pillow or another renderer does not share Photoshop font metrics.
- Read [the text reconstruction procedure](references/text-reconstruction.md) whenever the requested output includes editable text.

## Model boundary

- Image-generation or image-to-image models may separate semantics and repair backgrounds hidden by text, legends, masks, or symbols.
- Their output remains raster. They do not establish the original font metadata and cannot replace OCR, local font matching, or Photoshop TextItem creation.
- Use local inference for sensitive plans and maps by default. Uploading a source or crop to an external model requires authorization for that concrete image and destination.

## Deliverables and acceptance

- Use PSD only within its limits; use PSB for large dimensions or files. Save and reopen the mother file.
- Verify source hash unchanged, original dimensions and DPI preserved, required groups and masks present, editable text layers remain text layers, default view matches the source, and the clean view has no holes or obvious removed-element remnants.
- If a reduced-size print copy is requested, reduce JPEG storage size rather than pixel dimensions. Record JPEG quality, chroma subsampling, actual bytes, dimensions, DPI, and hash.
- Deliver a compact text/font-fit manifest and final receipt. Never describe an inferred font as the exact original when the source was a flat raster.
