---
name: visio-image-rebuilder
description: Rebuild or restyle editable Microsoft Visio diagrams from reference images and existing .vsdx files, then export deliverables as .vsdx, PNG, SVG, PDF, or PPTX. Use when the user asks Codex to open Visio, recreate a diagram from a PNG/JPG/screenshot/reference image, match a scientific model figure, batch-create Chinese technical-bid flowcharts, continue drawing another similar flowchart, update colors/typography/layout in a .vsdx, calibrate panel coordinates to avoid shifted or overlapping submodules, or make publication/presentation outputs while preserving Visio native editable shapes rather than embedding the reference image as a flat picture. For Chinese technical-bid flowcharts, default to the user's standard SimSun/宋体 12 pt technical-bid style and ask whether to use that default or reproduce the original image style when the two conflict.
---

# Visio Image Rebuilder

## Core Rule

Recreate the reference as editable Visio content. Do not satisfy a rebuild request by inserting the whole reference image into the page. Embedding the reference image is only allowed as a temporary locked tracing layer if it is removed or hidden before delivery and the final `.vsdx` remains native shapes, text, connectors, and groups.

Treat `.vsdx` as the source of truth. Export PNG, SVG, PDF, or PPTX only when the user asks for those formats or when a visual preview is needed for verification. For fast Chinese technical-bid flowchart work, the default deliverable is the saved `.vsdx` only.

## Windows PowerShell And CJK Text

When generating PowerShell automation scripts on Windows, keep the script body ASCII-only whenever practical. Raw Chinese string literals in `.ps1` files can be mis-decoded by Windows PowerShell and may surface as parse errors or apparent Visio COM hangs.

For Chinese labels, build strings from escaped Unicode instead of embedding raw CJK text:

```powershell
function UE([string]$text) {
    return [regex]::Replace($text, '\\u([0-9A-Fa-f]{4})', {
        param($m)
        return [string]([char][Convert]::ToInt32($m.Groups[1].Value, 16))
    })
}

$label = UE '\u8fdb\u5ea6\u7ba1\u63a7'
```

If a rebuild fails early, inspect the PowerShell parser output before assuming Visio COM is stuck.

## Chinese Technical-Bid Flowchart Mode

Use this mode for repeated Chinese engineering, tender, bid, QA/QC, supervision, procurement, schedule, or change-management flowcharts, especially when the user says "continue drawing this one" or provides several screenshots in sequence.

- Reuse the previous flowchart style unless the user gives a new style.
- Default to fast VSDX-only delivery: save exactly the final `.vsdx`, run package inspection when practical, and do not create backup files or preview images unless the user explicitly asks or visual verification is needed.
- Use simple sequential names such as `1.vsdx`, `2.vsdx`, `3.vsdx`, or the user's requested base name.
- When using sequential names, choose the next unused `.vsdx` name in the output directory. Do not overwrite an existing `.vsdx` unless the user explicitly asks to overwrite or provides that exact target path.
- Use batch mode when the user provides several screenshots, says "continue drawing", or asks to process a series: create one `.vsdx` per reference with the same style profile and sequential names, without PNG/SVG/PDF/PPTX by default.
- Keep generated task scripts ASCII-only and encode Chinese labels with `UE` or explicit Unicode code points.
- Default technical-bid style: SimSun/宋体 font, 12 pt, not bold; straight-corner rectangle process boxes; box fill `RGB(198,216,240)`; box border `RGB(0,176,240)` at 1 pt; connector color `RGB(0,170,240)` at 1 pt; Visio end arrow type `5` (`05`), medium end arrow size `2`; arrow line weight 1 pt.
- Default page limit for Visio flowcharts: do not exceed `165mm x 235mm` (`6.49in x 9.25in`). Either portrait or landscape is acceptable when the larger dimension stays within 235 mm and the smaller dimension stays within 165 mm.
- When the reference image's visible style conflicts with the default technical-bid style, ask before drawing: "按默认技术标设置走，还是按原图样式复刻？" If the user chooses default, preserve the reference's hierarchy, labels, and connector topology but use the default style instead of the screenshot colors, fonts, rounded corners, or arrow styling. If the user chooses original, reproduce the reference image style as closely as practical while keeping editability and page-size constraints.

## Workflow

1. Inspect inputs.
   - Confirm paths for the target `.vsdx`, reference image, requested output formats, and output directory.
   - If the target `.vsdx` does not exist and the task is a rebuild from an image, create a blank Visio document first, then back it up before drawing.
   - Export the current Visio page to PNG before editing when a target file already exists.
   - Inspect the `.vsdx` package for pages, media entries, and shape counts.
   - For new fast technical-bid flowchart rebuilds, do not create a separate backup file; the expected output is only the final `.vsdx`.
   - For edits to an existing user-provided `.vsdx`, create a backup only when the user requests it or when overwriting would risk losing unrelated work.
   - If Visio is already open, close only the target document or ask before terminating a stuck process.

2. Decode the reference image.
   - Identify page orientation, panel boundaries, module colors, captions, text hierarchy, arrows, dashed lines, and repeated motifs.
   - Build an object inventory: containers, titles, process boxes, icons, charts, graphs, equations, connectors, captions.
   - Calibrate the canvas first, then calibrate each major panel or subpanel with explicit top-left bounds or four corner points.
   - Draw panel internals in panel-local normalized coordinates whenever the figure has dense multi-panel content.
   - Decide whether the task is a full rebuild, color/style transfer, local edit, or export-only job.
   - For dense scientific figures, first create a coarse panel map, then draw panel internals. Do not start with small decorative details.

3. Prefer Visio automation for native edits.
   - Use COM automation on Windows when Visio is installed.
   - Use `DrawRectangle`, `DrawOval`, `DrawLine`, `Page.Import` only for small source assets, and shape cells such as `FillForegnd`, `LineColor`, `LineWeight`, `Char.Size`, `Char.Color`, `Rounding`.
   - Use explicit coordinates and IDs for fragile edits.
   - Keep grouped structure meaningful: major panels, submodules, repeated blocks, legends.
   - For nested modules, use helpers such as `RectRel`, `TextRel`, `LineRel`, and `OvalRel` so child shapes are constrained by their calibrated parent panel.

4. Use package XML edits only for narrow, deterministic changes.
   - XML patching is appropriate for recoloring existing shapes, replacing font tables, or changing known cell values.
   - Preserve Visio XML ordering: shape-level `Cell` nodes should be before `Section`, `Text`, or child `Shapes`.
   - Avoid rebuilding complex geometry by raw XML unless COM automation is unavailable.

5. Export requested formats from the verified Visio source.
   - Do not generate PNG/SVG/PDF/PPTX by default. In fast technical-bid flowchart mode, omit `-PreviewPath` and `-ExportFormats` unless the user asks for previews or secondary formats.
   - Use `scripts/visio_page_tools.ps1` for export-only jobs.
   - Use `scripts/visio_rebuild_scaffold.ps1` with `-ExportFormats` for rebuilds that should immediately create deliverables.
   - Prefer SVG for vector web/manuscript handoff, PDF for review/print, and PPTX for presentation decks.
   - For PPTX, use PowerPoint COM when available; the generated slide contains the Visio page render, usually inserted from SVG.

6. Verify without overtrusting a single signal.
   - For high-fidelity scientific or publication figures, export at least one preview after editing when possible.
   - For fast VSDX-only Chinese technical-bid flowcharts, package inspection plus checking the saved `.vsdx` exists is sufficient unless the user requests a preview.
   - Inspect the `.vsdx` package to confirm that no full-size reference PNG/JPG was left in `visio/media`.
   - Check shape count and representative text labels.
   - Check that major panels do not overlap and that child shapes stay within their intended panel bounds.
   - Check every requested output file exists and is non-empty.
   - If Visio automation hangs, stop safely, close the document if possible, and report whether the file was actually modified.

## Implementation Pattern

For full rebuilds, generate a script that:

- Opens the target `.vsdx` with Visio COM.
- Creates a blank `.vsdx` first when the target file does not exist.
- Skips backup creation by default for new fast technical-bid flowcharts so the output directory contains only the final `.vsdx`.
- Uses `-CreateBackup` only when a backup is requested or needed for an existing file overwrite.
- Clears or duplicates the page depending on user preference.
- Sets page size to match the reference aspect ratio while staying within the technical-bid maximum page box when that mode applies.
- Draws native shapes in top-left reference coordinates converted to Visio coordinates.
- Defines calibrated panel bounds for complex regions and uses panel-local coordinates for their internals.
- Adds reusable helpers for rectangles, text boxes, ovals, lines, arrows, mini charts, graph nodes, and image-like stacks.
- Saves the document and exports requested formats.
- Runs Visio hidden or in the background by default; make it visible only when visual interactive debugging is needed.
- After export, list or inspect the actual output directory so the final response names files that really exist.

Start from `scripts/visio_rebuild_scaffold.ps1` when building a full reconstruction script. Copy it into the workspace and customize the `Draw-ReferenceFigure` function rather than editing the skill copy.

For style transfer, generate a script that:

- Reads existing shape IDs, text, approximate geometry, fill, and line colors.
- Maps known modules to target palettes by text and group context.
- Applies fills, borders, text colors, line patterns, and font changes to existing shapes.
- Avoids repositioning unless the user asks for layout changes.
- Exports only after the `.vsdx` has been saved and inspected.

For export-only requests, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_page_tools.ps1 `
  -VsdxPath "C:\path\figure.vsdx" `
  -ExportFormats svg,pdf,pptx `
  -OutputDir "C:\path\exports" `
  -InspectPackage
```

For rebuild plus multi-format export, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_rebuild_scaffold.ps1 `
  -VsdxPath "C:\path\figure.vsdx" `
  -PageW 16 `
  -PageH 9 `
  -RefW 1600 `
  -RefH 900 `
  -PreviewPath "C:\path\exports\figure.png" `
  -ExportFormats svg,pdf,pptx `
  -OutputDir "C:\path\exports"
```

For fast Chinese technical-bid flowchart rebuilds, save `.vsdx` only by omitting `-PreviewPath` and `-ExportFormats`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_rebuild_scaffold.ps1 `
  -VsdxPath "C:\path\outputs\1.vsdx" `
  -PageW 9.25 `
  -PageH 6.49 `
  -RefW 640 `
  -RefH 400
```

## Safety Checklist

- Do not create backup or preview files for new fast technical-bid flowcharts unless the user asks for them; for existing user files, avoid destructive overwrites and use `-CreateBackup` when preservation matters.
- Close any open Visio document that locks the target file before direct package edits.
- Never delete or revert unrelated user files.
- If a previous attempt embedded the reference image, restore from backup or remove the image shape before continuing.
- Tell the user clearly whether the final file is native editable shapes or a flat embedded image.
- Tell the user when PPTX export is a rendered slide rather than native PowerPoint shapes.
- For Windows PowerShell scripts, keep CJK labels encoded with Unicode escapes or code points to avoid mojibake and parser failures.

## Acceptance Criteria

A Visio rebuild is acceptable only when:

- Main panel positions, flow direction, captions, and module hierarchy match the reference at first glance.
- Major panels are aligned to calibrated bounds, with no obvious submodule drift, collision, or cross-panel overlap.
- Text remains editable and uses the requested font; use Times New Roman for manuscript figures and SimSun for the default Chinese technical-bid profile.
- Repeated motifs are represented with reusable native shapes rather than pasted raster crops.
- The final `.vsdx` package has no full-page raster reference image in `visio/media`.
- Requested PNG/SVG/PDF/PPTX deliverables, if any, were exported from the saved `.vsdx` and are non-empty.
- Package inspection or direct existence checks were performed, with package inspection alone acceptable for VSDX-only fast flowchart mode.
- For batch flowchart work, the response uses verified file names from the output directory, not assumed names from script parameters.

## Useful Resource

Use `scripts/visio_page_tools.ps1` for common inspection, backup, preview export, multi-format export, and package checks. Use `scripts/visio_export_formats.ps1` when a custom task script needs reusable export helpers. Use `scripts/visio_rebuild_scaffold.ps1` as the starting point for native-shape drawing scripts; it includes both global top-left helpers and panel-local calibrated helpers. Read `references/rebuild-guidelines.md` when a task requires a full figure reconstruction or careful one-to-one scientific diagram matching.
