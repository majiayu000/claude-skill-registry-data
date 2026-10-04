---
name: marp
description: "Creates professional slide decks from Markdown using Marp (marp.app), outputting to HTML, PDF, PPTX, and image formats. Supports built-in themes (default, gaia, uncover), custom CSS overrides, speaker notes, per-slide directives, chart blocks, and math/KaTeX rendering. Trigger when the user says create a presentation, make slides, build a deck, or convert markdown to PDF/PPTX. Also activates for Marp theme setup, speaker notes in slides, and automated presentation builds via CLI or CI. Best for speakers, founders, and engineers who want to write slides in Markdown without fighting a GUI, and want outputs that work in any browser or presentation tool. Also for: automated doc-to-slides pipelines, pitch deck generation, and technical speaker decks with code highlighting."
---

# Marp — Markdown Presentation Ecosystem

Marp converts Markdown into professional HTML, PDF, PPTX, and image slides via
[Marp CLI](https://github.com/marp-team/marp-cli). No proprietary formats, no GUI.

---

## When to Activate

- "create a presentation", "make slides", "build a deck", "pitch deck"
- "convert markdown to slides", "markdown to PDF"
- "speaker notes", "presenter notes in slides"
- "set up Marp", "Marp theme", "Marp project"
- Any task where the output is a `.pptx`, `.pdf`, or HTML slide deck

---

## Workflow

### Step 1 — Ensure Marp CLI Is Installed

```bash
which marp || npx @marp-team/marp-cli@latest --version
```

If not present, install it:
```bash
npm install --save-dev @marp-team/marp-cli   # project
npm install -g @marp-team/marp-cli           # global
```

Or run via `npx` (no install required):
```bash
npx @marp-team/marp-cli@latest [command]
```

---

### Step 2 — Create or Review the Markdown Source

Create `slides.md` (or any `.md` file). Key conventions:

```markdown
---
marp: true
theme: default
paginate: true
---

# Slide 1 Title

Content here.

---

# Slide 2 Title

- Bullet point
- Another point

<!-- speaker notes: only visible in presenter mode -->

---

## Even-Level Headings Start New Slides (H2 = new slide)
### H3 is a Section Label (no slide break)
```

#### Core Front Matter Options

```yaml
---
marp: true              # enable Marp processing
theme: default          # built-in: default, gaia, uncover
paginate: true          # show page numbers
backgroundColor: #1e1e1e # dark background
header: "Title"         # persistent header
footer: "© 2026"        # persistent footer
---

# Or override per-slide with directives:
<!-- _color: white -->
<!-- _backgroundColor: #000 -->
<!-- _class: lead -->
```

#### Slide Separators

| Syntax | Effect |
|--------|--------|
| `---` on its own line | Hard slide break |
| `--` on its own line | Soft break (same section) |
| `<!-- fit -->` | Auto-fit text to slide |

#### Speaker Notes

```markdown
<!-- speaker notes:
This is hidden in slides but shown in presenter mode.
- Sub-points work too.
-->
```

#### Charts & Code (Marp Core Features)

````markdown
```chart
type: bar
data:
  labels: [Q1, Q2, Q3, Q4]
  datasets:
    - label: Revenue
      data: [12, 19, 15, 28]
```
{type=bar}
```
````

---

### Step 3 — Choose Output Format & Run

```bash
# HTML (default, opens in browser)
marp slides.md

# PDF (requires Chrome/Edge/Firefox)
marp slides.md --pdf

# PowerPoint
marp slides.md --pptx

# PNG images (one per slide)
marp slides.md --images png

# JPEG images
marp slides.md --images jpeg

# Output to specific path
marp slides.md -o dist/slides.html

# Watch mode (auto-reconvert on save)
marp slides.md -w

# HTTP server (on-demand conversion, ?pdf, ?pptx, ?png in query string)
marp slides.md -s
PORT=8080 marp slides.md -s

# Preview window (desktop only)
marp slides.md -p

# Batch: entire directory
marp --input-dir ./slides/ -o ./dist/
```

#### Useful Flags

```bash
--pdf-notes           # include speaker notes in PDF
--pdf-outlines        # add PDF bookmarks
--pptx-editable       # editable PPTX (requires LibreOffice)
--image-scale 2       # scale factor for image export
--allow-local-files   # embed local images (HTML only)
--browser chrome      # force specific browser for PDF/image export
```

---

### Step 4 — Verify Output

- **HTML**: open the `.html` file in a browser, test keyboard navigation (arrows, Space)
- **PDF**: open and check pagination, fonts, image quality
- **PPTX**: open in PowerPoint/Keynote/Google Slides
- **Images**: check resolution, especially for `--image-scale 2`

---

### Step 5 — Automation (Optional)

For CI/CD or project integration:

```json
// package.json scripts
{
  "scripts": {
    "slides:html": "marp src/slides.md -o public/slides.html",
    "slides:pdf": "marp src/slides.md --pdf",
    "slides:watch": "marp src/slides.md -w"
  }
}
```

Or use the `--server` mode to serve presentations from a docs site:
```bash
PORT=4321 marp docs/slides/ -s
# Access at http://localhost:4321/slides.md?pdf
```

---

## Marp Core Built-in Themes

| Theme | Best For |
|-------|----------|
| `default` | Clean, minimal, all-purpose |
| `gaia` | Modern with a sidebar, section headers |
| `uncover` | Full-bleed image backgrounds |
| Custom theme | CSS custom properties — see `marp-core` docs |

### Customizing Themes

Override via `style` block or custom CSS:

```markdown
---
marp: true
style: |
  section {
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
  }
  h1 { color: #58a6ff; }
  footer { color: #8b949e; }
---
```

---

## Project Structure Recommendation

```
project/
├── slides/
│   ├── cover.md        # Title slide
│   ├── agenda.md       # Overview
│   ├── content-1.md   # Section 1
│   ├── content-2.md   # Section 2
│   └── qa.md          # Closing slide
├── src/
│   └── presentation.md  # Combined deck (use !include directives)
├── public/
│   └── presentation.html
└── dist/
    ├── presentation.pdf
    └── presentation.pptx
```

Combine multiple files:
```markdown
<!-- $slide: cover.md -->
<!-- $slide: agenda.md -->
<!-- !include slides/content-1.md -->
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "marp: command not found" | Use `npx @marp-team/marp-cli@latest` or install globally |
| PDF export fails | Install Chrome/Edge/Firefox; use `--browser chrome` |
| Images not found | Use absolute paths or `--allow-local-files` for HTML |
| PPTX not editable | Re-export with `--pptx-editable` (requires LibreOffice) |
| Fonts look wrong | Bundle fonts or use web-safe fonts in CSS |
| Server mode 404 | Ensure `index.md` or `slides.md` exists in served dir |

---

## Key Marpit/Marp Markdown Extensions

| Extension | Example |
|-----------|---------|
| Directives (global) | `<!-- theme: gaia -->` |
| Directives (per-slide) | `<!-- _class: lead -->` |
| Built-in filters | `<!-- fit -->`, `<!-- _color: red -->` |
| Code blocks | Fenced code with language and Marp extensions |
| Charts (core) | `` ```chart `` blocks |
| Math | `` ```math `` blocks via KaTeX |

---

## See also

- `deck-narrative` — co-load for the deck's ARGUMENT (action titles, Minto
  top-down sequencing, one-message-per-slide, table-vs-chart selection,
  decision-slide construction) before Marp lays out the visuals. If
  exporting `--pptx`, run `deck-narrative/scripts/audit_deck.py` on the
  output before shipping — it mechanically catches system-font leaks
  (Rule 9) and other file-level defects a rendered preview can't show.
