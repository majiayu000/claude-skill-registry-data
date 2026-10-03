---
name: html2pptx
description: Convert HTML/WebDeck slide presentations into editable PowerPoint PPTX files using a browser-rendered DOM-to-SVG pipeline and native DrawingML conversion. Use when Codex needs to export .html/.htm slide decks, WebDeck documents, ECharts-heavy decks, or DOM/CSS presentations to editable .pptx while preserving text, shapes, SVG primitives, and chart vectors better than screenshot-based export.
---

# HTML2PPTX

Use this skill to convert browser-rendered HTML slide decks into editable PPTX.
The bundled pipeline is:

1. `html_dom_to_editable_svg.js`: launch Chromium, render the deck, extract DOM/CSS/SVG/ECharts into editable SVG primitives.
2. `svg_to_pptx`: convert SVG primitives to native PowerPoint DrawingML shapes.
3. `html2pptx.py`: wrapper CLI that runs both steps and validates the generated PPTX structure.

## Quick Start

Run the wrapper script from this skill folder:

```bash
python scripts/html2pptx.py input.html -o output.pptx
```

If Chromium is not discoverable or browser launch fails, pass an executable:

```bash
python scripts/html2pptx.py input.html -o output.pptx \
  --chrome "/path/to/Google Chrome or Chromium"
```

`--chrome-path` is also accepted as an alias. On Windows, prefer:

```bash
python scripts/html2pptx.py examples/basic-deck.html -o basic-deck.pptx \
  --chrome-path "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

Keep intermediate SVG files for debugging:

```bash
python scripts/html2pptx.py input.html -o output.pptx \
  --workdir /tmp/html2pptx-debug --keep-workdir
```

## Recommended Workflow

1. Confirm the input is an HTML slide deck, usually containing `.deck-slide`, `.deck-stage`, `.deck-page`, or similar fixed-size slide containers. Plain single-page HTML is also supported and will be wrapped as one 1280x720 slide automatically.
2. Run `scripts/html2pptx.py`.
3. Inspect the command summary:
   - `pictures=0` is ideal for fully editable output.
   - A large `shapes` count means the deck was converted as native shapes/text.
4. If specific pages look wrong, rerun with `--keep-workdir` and inspect `svg_output/NN_slide.svg`.
5. For malformed source decks, read `references/troubleshooting.md`.

## Output Expectations

The generated PPTX is editable, not pixel-perfect. It preserves:

- Text as editable text boxes where possible.
- Rectangles, lines, circles, paths, and many SVG primitives as editable shapes.
- Rounded boxes with uniform CSS borders as editable rounded rectangles.
- ECharts charts as vector SVG primitives when the chart can render or be rebuilt in SVG mode.
- Common Font Awesome Free solid `<i class="fa-...">` icons as editable SVG paths through an offline subset.
- Speaker notes generated from slide text.

Known limitations:

- Full HTML documents nested inside each slide may still require preprocessing.
- Long scroll-page layouts are clipped to the 1280x720 slide viewport.
- CSS pseudo-elements, filters, shadows, complex masks, unsupported external icon fonts, and advanced gradients may degrade.
- The pipeline requires local Chromium/Chrome and Node.js.

## Cross-Agent Usage

- Codex: invoke this skill as `$html2pptx`, then run `scripts/html2pptx.py`.
- Claude Code: read this `SKILL.md`, then call the same wrapper script.
- opencode: use the wrapper script directly, or follow the repo-level `AGENTS.md` if present.

For project setup and multilingual documentation, use the repository README files outside the skill folder.
