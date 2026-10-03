---
name: ppt-generation
description: "Generate PPTX presentations from slide plan + content."
allowed-tools:
  - bash
  - write_file
  - read_file
  - present_files
enabled: true
related-skills: [deep-research, chart-visualization]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# PPT Generation

## Overview

Generate professional PowerPoint presentations. Plan the structure with a
consistent visual style, generate slide content, and compose into a PPTX file.

> **Poirot note:** The original deer-flow skill uses AI image-generation per
  slide. Poirot may not have image-generation available. This version generates
  text-based slides with `python-pptx`. Install: `pip install python-pptx`.

## When to Use

- User requests to generate, create, or make presentations (PPT/PPTX)
- User wants slides for a topic with structured content
- User needs a visual presentation from research findings

## Presentation Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **dark-premium** | Black bg, luminous accents, luxury aesthetic | Executive presentations |
| **gradient-modern** | Bold mesh gradients, contemporary typography | Startups, brand launches |
| **minimal-swiss** | Grid-based, bold negative space, timeless | Consulting, architecture |
| **keynote** | Apple-inspired, bold typography, dramatic imagery | Keynotes, product reveals |
| **editorial** | Magazine-quality layouts, sophisticated typography | Annual reports, thought leadership |

## Workflow

### Step 1: Understand Requirements

- Topic/subject
- Number of slides (default: 5-10)
- Style: dark-premium / gradient-modern / minimal-swiss / keynote / editorial
- Aspect ratio: 16:9 (standard) or 4:3
- Content outline: key points per slide

### Step 2: Research (if needed)

Use `deep-research` skill to gather content for the presentation.

### Step 3: Create Presentation Plan

```json
{
  "title": "Presentation Title",
  "style": "dark-premium",
  "slides": [
    {"number": 1, "type": "title", "title": "...", "subtitle": "..."},
    {"number": 2, "type": "content", "title": "...", "bullets": ["...", "..."]},
    {"number": 3, "type": "chart", "title": "...", "data": {...}},
    {"number": 4, "type": "section", "title": "..."},
    {"number": 5, "type": "content", "title": "...", "bullets": ["...", "..."]},
    {"number": 6, "type": "closing", "title": "Thank You", "subtitle": "..."}
  ]
}
```

### Step 4: Generate PPTX

```bash
python3 -c "
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)

# Style: dark-premium
BG_COLOR = RGBColor(0x0A, 0x0A, 0x0A)
TEXT_COLOR = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT_COLOR = RGBColor(0x00, 0xD9, 0xFF)

def add_slide(prs, layout_idx=6):  # 6 = blank
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR
    return slide

def add_text(slide, text, left, top, width, height, size=24, color=TEXT_COLOR, bold=False):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    return txBox

# Slide 1: Title
slide = add_slide(prs)
add_text(slide, 'Presentation Title', 1, 2, 11, 2, size=44, bold=True)
add_text(slide, 'Subtitle', 1, 4, 11, 1, size=24, color=ACCENT_COLOR)

# Slide 2: Content with bullets
slide = add_slide(prs)
add_text(slide, 'Key Points', 1, 0.5, 11, 1, size=36, bold=True)
for i, bullet in enumerate(['Point one', 'Point two', 'Point three']):
    add_text(slide, f'• {bullet}', 1, 2 + i*0.8, 11, 0.7, size=24)

# Slide 3: Section divider
slide = add_slide(prs)
add_text(slide, 'Section Title', 1, 3, 11, 1.5, size=40, bold=True, color=ACCENT_COLOR)

# Save
prs.save('.poirot/outputs/presentation.pptx')
print('Saved to .poirot/outputs/presentation.pptx')
"
```

### Step 5: Present

```
present_files([".poirot/outputs/presentation.pptx"])
```

## Slide Types

| Type | Content | Layout |
|------|---------|--------|
| **title** | Title + subtitle | Centered, large font |
| **content** | Title + bullets | Left-aligned, 3-5 bullets |
| **section** | Section title only | Centered, accent color |
| **chart** | Title + chart image | Chart from `chart-visualization` skill |
| **quote** | Large quote + attribution | Centered, italic |
| **closing** | Thank you + contact | Centered |

## Pitfalls

- **Too much text per slide**: max 5-6 bullets, max 2 lines each. Slides are
  visual aids, not documents.
- **Font sizes too small**: title ≥36pt, body ≥24pt. If text doesn't fit,
  split into more slides.
- **Inconsistent style**: all slides must use the same color palette, font
  sizes, and layout patterns.
- **No visual hierarchy**: title > section headers > bullets > footnotes.
  Use size + weight + color to establish hierarchy.
- **python-pptx not installed**: `pip install python-pptx` first.
- **Image slides**: if you need chart images, generate them first with the
  `chart-visualization` skill, then embed as `slide.shapes.add_picture()`.
