---
name: read-special-images
description: "Read and OCR long webpage screenshots, panoramas, high-resolution images, and dense documents when whole-image display makes task-relevant text or details unreadable or unreliable. Treat aspect ratio at least 4:1, a side over 4096 px, or area over 16 million pixels only as screening signals, never automatic tiling triggers. Keep any image unsplit when the requested content is already readable, including small ultra-wide images."
compatibility: opencode
---

# Read Special Images

## Goal

Recover task-relevant content lost to whole-image display scaling, especially in very long browser screenshots. Preserve reading order and state uncertainty instead of guessing. **Solve a readability problem, not an aspect-ratio problem.**

## Decision Rule: Screen, Then Assess Readability

Distinguish these two questions:

1. **Does the image match a geometry screening signal?** Check the original dimensions or trustworthy metadata. Flag longest side / shortest side **>= 4**, either side **> 4096 pixels**, or total pixels **> 16,000,000**. Equality counts only for the aspect-ratio threshold. Unusual or unknown dimensions reported by image guidance are also reasons to check, not reasons to tile.
2. **Does the task actually require preprocessing?** Assess whether the requested text, numbers, relationships, or fine structure can be read reliably in the available view. Tile or crop only when display scaling or density prevents reliable reading, or when the user explicitly requests tiles. Scaling by itself is not sufficient if the requested details remain readable.

**Never infer unreadability from dimensions alone.** A geometry hit means “check readability,” not “must preprocess.” Conversely, an ordinary-size image can need crops when its text is too dense.

| Observed state | Action |
| --- | --- |
| Requested content is clear, regardless of dimensions or ratio | Read the original view; do not create tiles. |
| Only a specific requested region is unclear | Inspect a focused crop at original resolution; avoid tiling unrelated regions. |
| Requested content across the image is unreadable after whole-image scaling | Create ordered, overlapping tiles and read them at a usable scale. |
| Readability is unknown | Assess the available preview first; if insufficient, inspect the original or a representative crop. Do not declare preprocessing necessary based only on geometry. |
| Content is already blurred, cut off, or missing in the original | Do not expect tiling to reconstruct it; report the limitation and request a better source when necessary. |

Judge readability against the **user's task**: a broad visual summary may not require tiny labels; exact transcription requires every relevant line and number to be legible. Do not call an image readable merely because its topic or layout is recognizable.

### Calibration Examples

| Example | Correct decision |
| --- | --- |
| 1620 × 232 image with a few clearly readable chat lines, approximately 7:1 | Matches the ratio signal, but needs no preprocessing. |
| 1440 × 20000 full-page browser screenshot whose body text becomes illegible in the whole-image view | Needs overlapping vertical tiles, or a focused crop if the task concerns only one section. |
| Very large image whose colors and broad layout are clear enough for the requested overview | Keep the whole-image view; size alone does not require tiles. |
| 1200 × 900 table with unreadable tiny figures | Crop or tile despite ordinary geometry. |

When asked whether an image “meets the conditions,” explicitly separate **geometry match** from **preprocessing need**. For example: “It matches the unusual-ratio screening signal, but the requested content is readable, so no preprocessing is needed.” If readability has not been assessed, say so.

## Workflow

1. Use the supplied preview if it is already readable. Do not reopen an attachment merely to repeat a sufficient inspection. Treat an unreadable whole-image preview as orientation/context only.
2. Identify the original local path when dimension inspection or cropping is needed. Prefer trustworthy `<image_metadata>` from the original image header. Do not mistake dimensions quoted inside a screenshot for that screenshot's own dimensions, or estimate original dimensions from its displayed size.
3. If dimensions are needed but unknown, inspect the original file. Resolve `scripts/slice_image.py` relative to the directory containing this `SKILL.md`; substitute actual paths and the available Python 3 interpreter in the commands below. Use `python3` on Linux/macOS or `py` on Windows when available. The script requires Pillow.

   ```bash
   python3 "<skill-dir>/scripts/slice_image.py" "<original-image-path>" --inspect-only
   ```

   Treat `screening_signals` in the result as geometric facts only. The script does not perform OCR or assess semantic readability; `preprocessing_required: null` means the decision is still unknown.
4. Assess task-relevant readability using the decision rule above. If readable, continue without tiles. If only one region is unclear, use the available crop capability on that region. If broad unreadability requires tiling, record the reason and run:

   ```bash
   python3 "<skill-dir>/scripts/slice_image.py" "<original-image-path>" --readability unreadable --output-dir "<tiles-directory>"
   ```

   By default, the script only inspects and never tiles based on geometry alone. `--readability readable` explicitly keeps the image unsplit. `--force` is an explicit tiling override for user-requested tiles or a confirmed need; never add it simply because a threshold matched. It cannot be combined with `--readability readable`.
5. Use `--mode vertical` for top-to-bottom screenshots, `--mode horizontal` for panoramas, or `--mode grid` when both dimensions need subdivision. Keep the default 12% overlap unless unusually tall lines or boundary objects need more. Reduce tile dimensions or switch to grid if a strip is still too wide or tall to read.
6. Read `manifest.json`, then view every listed tile in manifest order: top-to-bottom, left-to-right, or row-major as specified. Do not skip a tile because adjacent tiles look similar. If only a requested region was cropped, inspect all tiles of that region and do not claim coverage of the whole source.
7. Record extraction notes per tile before merging. Preserve headings, columns, numbered steps, and spatial relationships in source order. Save visual findings before further inspections as required by the active tools.
8. Reconcile boundaries using overlap: compare ending and starting lines/objects, retain one copy of repeated content, and repair a cut word or line only when another tile shows the complete version. Prefer the clearer view when OCR differs and flag unresolved conflicts. Never concatenate OCR fragments blindly.
9. Verify the merged result against several tiles, including an overlap boundary and the final tile. If a tile remains unreadable, try a smaller original-resolution crop or an available OCR capability; do not upscale and guess. If the original lacks recoverable detail, report only what is verified.

## Verification Checklist

- Confirm any reported dimensions and ratio came from the original file or trustworthy metadata.
- Separate screening signals from the actual preprocessing decision; never report geometry alone as proof of unreadability.
- Confirm readable images were kept unsplit even when unusually wide, tall, or large, unless the user explicitly requested tiles.
- Confirm any preprocessing addresses a concrete task-relevant readability problem or explicit tiling request.
- Confirm all relevant manifest tiles were viewed in order and overlap duplicates removed without dropping boundary text.
- Distinguish exact transcription from a summary; flag unreadable regions and unsupported reconstructions rather than inventing content.

## Bundled Script

`scripts/slice_image.py` reports geometric screening signals, accepts an explicit readability assessment, and creates deterministic overlapping tiles plus a reading-order manifest only when requested. It does not independently determine whether text is readable.
