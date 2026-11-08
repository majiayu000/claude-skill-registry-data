---
name: html-to-press-pdf
description: Use when converting a Claude-designed (or any HTML/CSS) magazine, zine, booklet, or multi-page document into a crystal-clean, print-ready PDF for a print shop like Mixam — especially when Chrome's print-to-PDF adds whitespace margins, shrinks/scales content, or the layout relies on CSS transform:scale artboards. Covers full-bleed, exact trim size, DPI, and print-shop upload settings.
compatibility: >-
  Node with puppeteer-core and Python with img2pdf. Loads the user's own design URL in local Chrome.
---

# HTML → Press-Ready PDF

## Overview

Claude-designed print HTML lays each page out as a fixed-px "artboard" (e.g. 670×870) scaled up to the trim+bleed page with `transform: scale(...)` on a wrapper div (`.pp`, `.sheet`, etc.). Chrome's `--print-to-pdf` and even puppeteer `page.pdf()` **mis-paint scaled content during pagination** — the print compositor fits each page using the *pre-transform* layout box, so the artwork squashes into the top-left corner and the rest of the page is dead whitespace. This looks like a "margin" bug but is actually a scale bug.

**Core principle:** Don't print transformed HTML to PDF. **Screenshot each rendered page element** (post-transform pixels are correct) at high DPI, then **assemble lossless into a PDF with exact page boxes.** Photos in these designs are raster anyway, so 384 DPI raster is print-indistinguishable from vector and sidesteps the bug entirely.

## When to use

- Output has white margins / content shrunk to a corner after Chrome print-to-PDF
- HTML uses `transform: scale()` on page wrappers (grep the source for `transform:scale`)
- A print shop (Mixam, Mixbook, Lulu, local) needs full-bleed PDF at exact trim
- Source is a hosted Claude `claudeusercontent.com` design URL with relative `../images/` assets

**Don't use for** vector-only / text documents with no transform tricks — plain `page.pdf({preferCSSPageSize:true})` is fine there and keeps text vector.

## The pipeline

```bash
# 0. Find Chrome + read the design's @page size and scale mechanism
grep -n '@page\|transform:scale\|class="sheet"\|<img' design.html

# 1. Screenshot every page element at high DPI (loads live URL so images/fonts resolve)
cd <skill>/scripts && npm i puppeteer-core@23   # first run only
node shoot.js "<LIVE_HTML_URL>" /tmp/sheets 384 ".sheet"
#                                          ^DPI  ^page-element selector
#   384 default, 480 for extra crispness. Match source photo res; 300 is the floor.

# 2. Assemble lossless PDF with exact trim+bleed page boxes
python3 scripts/assemble_pdf.py /tmp/sheets /tmp/out.pdf 384
#   Pass the SAME DPI as step 1, or page boxes mis-size.
```

`shoot.js` waits for `document.fonts.ready` + all images decoded, hides `.toolbar/.hint`, and reports broken images. `assemble_pdf.py` uses `img2pdf` (no recompression) with `get_fixed_dpi_layout_fun` so page box = `pixels / dpi` inches exactly.

## Verify before delivering (always)

```bash
python3 scripts/verify_pdf.py /tmp/out.pdf
```
Confirms: page count, **every page identical exact in/pt size**, and content **bleeds 0→~100%** (no whitespace). If a page covers only ~66%, the transform bug is back — you printed instead of screenshotting.

## Print-shop settings (Mixam defaults)

- **Page size in HTML** = trim + 0.125" bleed all sides. E.g. trim 8.375×10.875 → `@page { size: 8.625in 11.125in; margin:0 }`. Order at the **trim** size; bleed is already included.
- **No crop/registration marks** — Mixam wants bleed only.
- **Page count:** saddle-stitch ÷4, perfect-bound ÷2. Perfect-bound often wants the cover as a separate file.
- **Color:** deliver **sRGB**; Mixam auto-converts to CMYK (safest for dark/moody covers — CMYK conversion muddies deep blacks). Only make a CMYK PDF/X if their preflight demands it (needs Ghostscript; expect color shift).
- **Size:** 150–200 MB is fine to upload. To shrink, re-embed photos as quality-95 JPEG.

## Common mistakes

| Mistake | Fix |
|---|---|
| Chrome `--print-to-pdf` → whitespace margins | It's the transform bug. Screenshot pages instead. |
| Downloaded HTML, images 404 | `../images/` are relative — render the **live URL**, don't save HTML locally. |
| Different DPI in step 1 vs 2 | Page boxes mis-size (e.g. 82.8in). Pass the same DPI to both. |
| Pillow `.save(...pdf)` for assembly | Pillow recompresses to JPEG (lossy). Use `img2pdf` (lossless). |
| Added extra bleed in print-shop order | Bleed is already in the page size. Order at trim. |
| Assumed it worked | Always run `verify_pdf.py` — check coverage hits ~100%, not 66%. |