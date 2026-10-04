---
name: pptx
description: "Use this Canvas-owned clean-room skill whenever a PowerPoint `.pptx` deck is an input or output. Trigger for creating, editing, reviewing, repairing, templating, combining, splitting, rendering, or extracting slide decks, including pitch decks, reports, speaker notes, template-following, and Google Slides-targeted handoff."
license: "Canvas Notebook Sustainable Use License"
---

# PPTX Presentations

This skill covers editable PowerPoint-compatible presentation work in Canvas
Notebook. It is a clean-room Canvas skill; do not copy vendor skill material,
hidden prompts, or proprietary helper code into this folder.

## Core Contract

- Use `CANVAS_AGENT_TEMP_DIR` for scripts, working copies, exported PDFs,
  thumbnails, and QA images. Promote only the requested final deck to the
  workspace with `copy_path` or `move_path`.
- Deliver editable slides: use PowerPoint-native text, shapes, tables, charts,
  images, speaker notes, and layouts. Full-slide bitmaps are acceptable only
  when the user explicitly asks for image-only slides.
- Preserve source deck styling for targeted edits and template-following tasks.
- For new decks, choose a coherent visual system before building: type scale,
  palette, grid, slide rhythm, image treatment, chart style, and footer/page
  conventions.
- Keep scratch exports, thumbnails, notes, and QA images out of the final
  response unless requested.
- Use stable descriptive filenames and write final decks to the requested path
  or the workspace.

## Recommended Tools

- `python-pptx` for creating and editing many deck structures.
- `zipfile` plus `lxml` for narrow OOXML repairs that `python-pptx` cannot
  express.
- LibreOffice for deck-to-PDF visual checks. Before invoking it, read
  [references/headless-libreoffice.md](references/headless-libreoffice.md).
- Poppler tools for rendering exported PDFs to images.

## Workflow

1. Pick a mode: create, template-following, targeted edit, extract/review, or
   repair.
2. For existing decks, inspect slide count, dimensions, layouts, theme fonts,
   masters, images, charts, notes, and repeated brand elements before editing.
3. Build or edit with native objects. Avoid layout drift by using consistent
   coordinates, margins, and alignment rules.
4. Convert the scratch copy to PDF with headless LibreOffice, render every PDF
   page with Poppler, and inspect every slide for clipped text, overlap,
   illegible contrast, broken charts, missing images, and bad placeholder text.
5. Fix visible issues and render again. If rendering is unavailable, perform
   structural checks and disclose the limitation.

## Slide Quality Rules

- Start with the content structure, not decoration.
- Use fewer, clearer slide objects rather than dense unmanaged fragments.
- Keep titles short and scannable.
- Align objects to a consistent grid and keep repeated elements stable.
- Charts must include readable labels, units, and source notes when relevant.
- Speaker notes should be concise and tied to the visible slide.

## Final Checks

- Deck opens without repair warnings.
- Slide count, dimensions, order, and section flow match the request.
- No empty placeholders, internal notes, or unresolved TODOs remain.
- Visual QA has passed or any rendering limitation is clearly reported.
