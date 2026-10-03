---
name: html2pptx
description: Convert local HTML/WebDeck slide presentations into editable PowerPoint PPTX files. Use when the user provides an .html/.htm deck and wants editable text, shapes, SVG, and ECharts content instead of a screenshot-only export.
---

# html2pptx

This is the Claude Code / opencode project-skill entry point for this repository.

The implementation lives in the shared skill folder:

- `skills/html2pptx/SKILL.md`
- `skills/html2pptx/scripts/html2pptx.py`
- `skills/html2pptx/scripts/html_dom_to_editable_svg.js`
- `skills/html2pptx/scripts/svg_to_pptx/`

Run the converter from the repository root:

```bash
python skills/html2pptx/scripts/html2pptx.py input.html -o output.pptx
```

If Chrome or Chromium is not auto-detected:

```bash
python skills/html2pptx/scripts/html2pptx.py input.html -o output.pptx \
  --chrome "/path/to/Google Chrome or Chromium"
```

`--chrome-path` is also accepted as an alias. On Windows:

```bash
python skills/html2pptx/scripts/html2pptx.py examples/basic-deck.html -o basic-deck.pptx \
  --chrome-path "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

For debugging bad pages:

```bash
python skills/html2pptx/scripts/html2pptx.py input.html -o output.pptx \
  --workdir /tmp/html2pptx-debug --keep-workdir
```

Inspect `svg_output/NN_slide.svg`.

Good fit:

- Fixed 16:9 HTML/WebDeck slides.
- Plain single-page HTML that should be auto-wrapped into one 1280x720 slide.
- DOM text, CSS boxes, lines, SVG diagrams, and ECharts charts that should remain editable.
- Decks where PowerPoint editability matters more than screenshot-perfect rendering.

Current converter strengths:

- ECharts instances are forced or rebuilt with SVG renderer where possible.
- Uniform rounded CSS borders are preserved as editable stroked rounded rectangles.
- Inline SVG children inside text nodes are extracted instead of being swallowed by text conversion.
- Common Font Awesome Free solid `<i class="fa-...">` icons are inlined as SVG paths before extraction.

Known limits:

- Long webpages are clipped to the slide viewport.
- Full HTML documents nested inside a slide may need preprocessing.
- CSS pseudo-elements, filters, shadows, complex masks, and external icon fonts may degrade.
