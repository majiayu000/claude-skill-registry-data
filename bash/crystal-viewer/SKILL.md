---
name: crystal-viewer
description: Generate an interactive 3D HTML crystal structure viewer from a CIF file (URL or local path). Uses 3Dmol.js — no Python dependencies needed. Features rotate/zoom/pan controls, Jmol color scheme, ball-and-stick/sphere/stick/wire style toggle, unit cell wireframe, background toggle, and an info panel showing formula, space group, and cell parameters.
---

# Crystal Viewer

Converts a CIF file (local path or URL) into a single HTML file with a fully interactive 3D crystal structure viewer powered by **3Dmol.js**.

**No Python dependencies required** — the script uses only the standard library.

## When to Use

- User provides a CIF link (URL) or path and wants to visualize it
- User asks to "show", "visualize", "render", or "view" a crystal structure
- User wants a rotatable 3D browser view of a material

## Quick Start

```bash
# No pip install needed!

# From a URL
python scripts/cif_to_html.py https://example.com/structure.cif

# From a local file
python scripts/cif_to_html.py structure.cif

# Custom output name
python scripts/cif_to_html.py structure.cif -o viewer.html
```

Then open the generated HTML in any modern browser (internet required for the 3Dmol.js CDN).

## Features

| Feature | Details |
|---------|---------|
| 3D controls | Drag rotate · Scroll zoom · Shift+drag pan |
| Rendering | 3Dmol.js with Jmol element colors |
| Style toggle | Ball & Stick · Space Filling · Stick · Wire |
| Unit cell | Toggleable wireframe overlay |
| Background | Dark / light toggle |
| Info panel | Formula, space group, a/b/c/α/β/γ |
| No deps | Pure Python stdlib — no pymatgen, numpy, etc. |

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `input` | required | CIF URL or local file path |
| `-o OUTPUT` | `<stem>_crystal.html` | Output HTML path |

## Implementation Notes

- CIF content is embedded as a JSON string directly in the HTML
- 3Dmol.js (`https://3Dmol.org/build/3Dmol-min.js`) handles all parsing, symmetry expansion, and rendering
- CIF header is parsed with regex to extract formula, space group, and cell parameters for the info panel
- The generated HTML requires an internet connection to load 3Dmol.js from CDN

## Example Workflow

When a user says "可视化这个 CIF 文件 https://…/structure.cif":

```bash
python scripts/cif_to_html.py https://…/structure.cif
# → structure_crystal.html
```
Return a link that opens the generated viewer in a new tab, for example:

```html
<a href="/viewer/structure_crystal.html" target="_blank" rel="noopener noreferrer">打开结构</a>
```

Replace `structure_crystal.html` with the actual generated HTML filename or viewer path.
