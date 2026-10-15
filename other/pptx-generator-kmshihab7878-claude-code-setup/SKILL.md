---
name: pptx-generator
description: Generate professional PowerPoint presentations from structured content. Slide layouts, themes, charts, tables, speaker notes. Uses python-pptx. Use when creating presentations, pitch decks, reports as slides, or converting content to PPTX format.
version: "1.0.0"
category: documents
---

# PowerPoint Generator

Generate professional PPTX files using `python-pptx`.

## Rules (Mandatory)

1. **Every presentation MUST have**: title slide, agenda/outline, content slides, summary/next-steps slide
2. **No wall-of-text slides** — max 6 bullet points per slide, max 8 words per bullet
3. **Every data claim gets a chart or table** — never present numbers as plain text
4. **Speaker notes on every slide** — full context the presenter needs
5. **Consistent theme** — colors, fonts, and spacing uniform throughout
6. **File output** — always save to a concrete path and confirm it exists

## Slide Types

| Type | When | Layout |
|------|------|--------|
| Title | Opening | Large title + subtitle + date |
| Section | Chapter break | Section title + brief description |
| Content | Key points | Title + bullets (max 6) |
| Two-Column | Comparison | Title + left/right content |
| Chart | Data | Title + chart (bar/line/pie) + caption |
| Table | Structured data | Title + table + footnote |
| Image | Visual | Title + placeholder for image path |
| Quote | Testimonial | Large quote + attribution |
| Summary | Closing | Key takeaways + next steps |

## python-pptx Patterns

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9 widescreen
prs.slide_height = Inches(7.5)

# Add slide
slide_layout = prs.slide_layouts[1]  # Title + Content
slide = prs.slides.add_slide(slide_layout)
slide.shapes.title.text = "Slide Title"

# Add chart
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (1.2, 1.5, 1.8, 2.3))
slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)

# Speaker notes
slide.notes_slide.notes_text_frame.text = "Full context here"

prs.save("output.pptx")
```

## Workflow

1. **Structure** — outline slides with types and key content
2. **Theme** — set colors, fonts, slide dimensions (default 16:9)
3. **Build** — create slides programmatically
4. **Charts/Tables** — add data visualizations
5. **Notes** — add speaker notes to every slide
6. **Save** — write to file, verify it exists

## Install

```bash
pip install python-pptx
```
