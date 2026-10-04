---
name: markdown-to-pdf
description: >-
  Convert Markdown (.md) files to a polished PDF with ALL images preserved and scaled to the
  page. Use whenever the user asks to "save this markdown as a PDF", "convert README.md to
  pdf", "export the .md as a pdf", "turn these notes/docs into a PDF", or wants a PDF
  deliverable of any GitHub-flavored Markdown document (README, design doc, report, notes) —
  especially when it contains images or diagrams (remote or local), tables, code blocks, or a
  linked table of contents. Pipeline: pandoc (GFM → standalone HTML with embedded resources) →
  headless Chrome print-to-pdf with a GitHub-like print stylesheet → pypdf verification that
  every referenced image is embedded. Do NOT use for .tex → PDF (use a LaTeX toolchain) or for
  .docx work (use word-docx / tex2docx).
metadata:
  author: Claude Code
  date: 2026-06-11
  version: 1.1.0
---

# Markdown → PDF (pandoc + headless Chrome)

## Problem

Converting Markdown to PDF through pandoc's default LaTeX route breaks on
real-world GitHub-flavored documents: Unicode box-drawing characters in code
blocks (`├──`) crash pdflatex, wide GFM tables overflow the page, remote
images need manual download, and the output looks nothing like the rendered
Markdown the author reviewed. Naive HTML routes drop images or paste them at
native resolution so they spill off the page.

## Context / Trigger Conditions

- User asks to save/convert/export a `.md` file as PDF.
- The document carries images (hosted PNGs, local figures), GFM tables,
  fenced code blocks, blockquotes, or `#`-anchor TOC links.
- Requirements like "all images must be preserved" or "scaled appropriately".

## Solution

Render the Markdown to HTML exactly as a browser would, then print it.

**One command (preferred):**

```
python ~/.claude/skills/markdown-to-pdf/scripts/md2pdf.py <input.md> [-o out.pdf]
```

The script: (1) runs pandoc `-f gfm -t html5 --standalone --embed-resources`
with `assets/print.css`, executed from the Markdown's own directory so
relative image paths resolve, and with remote images fetched and inlined as
data URIs; (2) prints with headless Chrome (Edge/Chromium fallback) using
`--no-pdf-header-footer --virtual-time-budget=30000`; (3) verifies with pypdf
that the embedded raster-image count is at least the number of image
references in the source, printing each image's page and dimensions. Exit
code 2 flags a missing-image warning.

**Manual equivalent** (what the script automates):

```bash
pandoc input.md -f gfm -t html5 -s --embed-resources -c print.css \
    --metadata pagetitle="input" -o /tmp/input.html
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless \
    --disable-gpu --no-pdf-header-footer --virtual-time-budget=30000 \
    --print-to-pdf="out.pdf" "file:///tmp/input.html"
```

**Why this works for images.** The stylesheet constrains every image with
`max-width: 100%; max-height: 240mm; width/height: auto; break-inside: avoid`,
so each image scales to the printable width, a very tall diagram still fits a
single page, aspect ratio is preserved, and no image is split across a page
break. `--virtual-time-budget` makes Chrome wait for image loading before
printing; `--embed-resources` makes the HTML self-contained so nothing
depends on the network at print time.

## Verification

1. The script's pypdf pass: page count, plus one line per embedded image with
   its page number and pixel dimensions; compare against the source's image
   count.
2. Visual spot-check: the Read tool renders PDF pages as images — read the
   pages the verifier listed and confirm each diagram is legible and fits the
   page.

## Example

`style-emulation/README.md` (~800 lines: 4 hosted PNG diagrams up to
1410×2998 px, two request/command tables, a box-drawing module map, a linked
TOC) → 19-page, 1.35 MB PDF; all 4 images embedded on pages 6/7/9/10, each
scaled to one page; tables bordered with zebra striping; code blocks styled;
TOC links live.

## Notes

- **Page-break trade-off:** `break-inside: avoid` keeps images whole, so an
  image that does not fit the space left on a page pushes to the next page,
  leaving white space behind. Acceptable for reports; mention it to the user.
- **TOC anchors:** pandoc's GFM reader auto-generates GitHub-style heading
  ids, so existing `(#section-name)` links keep working in the PDF.
- **SVG images** may be drawn as vector art rather than raster XObjects; the
  pypdf count then under-reports and the warning is a false positive — check
  visually.
- **Same image referenced twice** can be embedded once; the `embedded <
  referenced` check is a heuristic, not an exact equality test.
- **Wide code blocks** are handled by `white-space: pre-wrap` (wrap, never
  clip); long table cells wrap inside bordered cells at 8.5pt.
- **Paper/margins** live in `assets/print.css` (`@page { size: A4; margin:
  16mm 15mm; }`); pass `--css <file>` for a per-job override (e.g. letter,
  landscape).
- **`--no-embed`** reverts to link-only HTML with Chrome fetching images at
  print time — useful if pandoc cannot reach a host that Chrome can.
- If headless Chrome ever hangs on a remote-image page, raise `--budget`.
- **Locked targets (cloud sync / open viewers):** Chrome can fail to
  overwrite a PDF in a Dropbox/OneDrive-synced folder — or one open in
  Acrobat — while still exiting 0, silently leaving the stale file in place
  (the byte-identical output size is the tell). The script therefore prints
  to its temp dir and moves the result over the target with retries; if the
  target stays locked (e.g. the user has the old PDF open), it saves to
  `<name>.new.pdf` and says so. The pypdf verification step is what catches
  this class of failure — keep it on.

## Related skills

- `pdf` — probing, extracting, manipulating existing PDFs (and reportlab
  generation from scratch). Markdown sources route here instead.
- `tex2docx`, `manuscript-editing-template-latex` — LaTeX/docx conversion
  pipelines; use those for `.tex`/`.docx`, not this skill.

## References

- pandoc manual, `--embed-resources` / GFM reader: https://pandoc.org/MANUAL.html
- Chrome headless print-to-pdf flags: https://developer.chrome.com/docs/chromium/headless
