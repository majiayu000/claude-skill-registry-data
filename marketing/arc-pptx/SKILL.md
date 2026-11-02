---
name: arc-pptx
description: Create and edit PowerPoint PPTX decks using a real template, coherent slide design, source-backed charts, and slide geometry plus visual checks.
---

# PowerPoint presentations

Use the supplied deck, brand, or template when present. Read its slide size, layouts, typography, and existing content before changing it. For a connected Google Slides presentation, use the authorized Slides App when that is the requested destination. Do not replace an editable deck with screenshots when the user needs editable elements.

## Author a usable deck

Check Python and `python-pptx` on an authorized computer; use a task-local environment for missing packages. Obtain [scripts/inspect_pptx.py](scripts/inspect_pptx.py) using the resource tools. Load `Presentation(existing_path)` to preserve the real template or create a new `Presentation()` with an intentional slide size. Prefer the template's layouts and editable text, shapes, tables, and charts. Use actual supplied data for charts and record sources. Do not invent business metrics, quotations, or logos.

Choose slide structure around the audience and requested narrative. Keep one principal message per slide, use consistent margins and hierarchy, and split dense content before shrinking all text. Check that fonts cover the user's language. A large text box does not establish that text fits: consider its font size, margins, paragraphs, and line wrapping. Save a new `.pptx` unless an overwrite is intended.

## Check the actual slides

Run `python scripts/inspect_pptx.py OUTPUT.pptx`. Resolve unintended shapes outside the slide canvas and verify expected slide count and text. Intentional bleed shapes can be outside the canvas; inspect them rather than blindly moving everything. The inspector checks top-level geometry, not font rendering, nested shape overflow, or text fit.

When local PowerPoint or LibreOffice export is available, render every slide and inspect the images for clipping, overlaps, unreadable charts, and substituted fonts. A structurally valid PPTX is not proof of visual quality. If no renderer is available, state that limitation and do not claim every slide has been visually checked. Return the actual editable file path and checks performed.

Reference: https://python-pptx.readthedocs.io/en/latest/
