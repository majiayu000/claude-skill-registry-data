---
name: pptx
description: Use when creating, editing, or reading PowerPoint files.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [powerpoint, presentations, slides, pptx]
---

# PPTX Creation, Editing, and Analysis

A `.pptx` file is a ZIP archive of XML files. Choose your approach by task:

| Task | Approach |
|------|----------|
| **Create** a new deck | Write a `pptxgenjs` script |
| **Edit** an existing deck | unzip → edit XML → zip |
| **Read** content | `markitdown deck.pptx` |

## Creating with pptxgenjs

`pptxgenjs` is preinstalled — write the script and `require('pptxgenjs')` directly.

### Critical Gotchas

- Set `pres.layout` **before** adding slides. Default is `LAYOUT_16x9` = 10" × 5.625"
- Hex colors: never `#`, never 8 digits. Use `"FF0000"` format
- pptxgenjs mutates option objects in place — build fresh objects per call
- Shadow `offset` must be ≥ 0 — negative offsets corrupt the file
- `letterSpacing` is ignored; use `charSpacing` instead
- Lists: `bullet: true` on each item, `breakLine: true` on all but last
- Speaker notes go in `slide.addNotes("...")` (plain text)
- After `writeFile()`, run validation: `python scripts/office/validate.py deck.pptx`

```javascript
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const slide = pres.addSlide();
slide.addText('Hello World', {
  x: 0.5, y: 0.5, w: 9, h: 1,
  fontSize: 44, bold: true,
  color: '141413',
  fontFace: 'Poppins',
});

pres.writeFile({ fileName: 'output.pptx' });
```

## Editing Existing Decks

```bash
# Unpack
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx

# Duplicate a slide
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml

# Reorder/delete slides = edit <p:sldIdLst> in ppt/presentation.xml

# Clean orphans after deletion
python scripts/clean.py unpacked/

# Repack
(cd unpacked && rm -f ../out.pptx && zip -Xr ../out.pptx .)

# Validate
python scripts/office/validate.py out.pptx --original deck.pptx
```

## Design Ideas

- Pick a bold, content-informed color palette
- One color dominates (60-70%), with 1-2 supporting tones and one accent
- Dark/light contrast for sandwich structure
- Commit to a visual motif — repeat it across every slide
- Every slide needs a visual element (image, chart, icon, shape)

### Typography Safe Fonts
Arial, Calibri, Cambria, Times New Roman, Courier New

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt |

## Common Pitfalls

- ❌ **Hex colors with `#` prefix** — Corrupts the file
- ❌ **Sharing option objects across add* calls** — pptxgenjs mutates in place
- ❌ **Text-only slides** — Every slide needs a visual element
- ❌ **Accent lines under titles** — Hallmark of AI-generated slides
- ❌ **Aptos font** — Not available in all environments

## Verification Checklist

- [ ] `python scripts/office/validate.py output.pptx` passes
- [ ] No placeholder text remains (grep for xxx, lorem, ipsum, TODO)
- [ ] Visual QA: no text overflow, no overlapping elements
- [ ] Charts render correctly with proper axis configuration
- [ ] Speaker notes are plain text (not text boxes)
- [ ] Colors use proper hex format (no `#`, no 8-digit)
