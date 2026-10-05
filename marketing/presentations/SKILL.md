---
name: presentations
description: Use when creating or editing slide decks (.pptx). Covers slide structure, using layouts and templates correctly, charts and images, speaker notes, and building a deck that communicates rather than decorates.
metadata:
  category: documents
  version: 1.0.0
  tags: [pptx, powerpoint, slides, presentations, templates]
---

# Presentations

## Purpose

Build slide decks programmatically, using the template's layouts rather than positioning text boxes by hand — and with a structure that carries an argument rather than a list of topics.

## When to Use

- Generating a deck from data or a document.
- Editing an existing `.pptx`.
- Extracting content or speaker notes from a deck.
- Applying a corporate template to generated content.

## Capabilities

- Slide generation using template layouts and placeholders.
- Charts, tables, and images with correct positioning.
- Speaker notes.
- Content extraction from existing decks.
- Template application and brand compliance.

## Inputs

- The content and the argument it should make.
- The template, if there is a house style.
- The audience and the setting — read in a room, or sent as a document.

## Outputs

- A `.pptx` using the template's layouts, not free-floating text boxes.
- One idea per slide.
- Speaker notes carrying the detail that does not belong on the slide.

## Workflow

1. **Write the argument before the slides** — What is the conclusion, and what supports it? A deck assembled from available material rather than toward a point is a document with page breaks.
2. **Use the template's layouts** — Each layout has placeholders. Filling a placeholder inherits the template's fonts, sizes, and positions. Adding a free-floating text box does not, and it will look wrong on a projector.
3. **One idea per slide** — The slide title should state the point, not the topic. "Revenue grew 40% on enterprise expansion" is a title; "Revenue" is a label.
4. **Put the detail in the notes** — The slide carries the point; the speaker or the notes carry the argument. A slide with eight bullet points will be read instead of listened to.
5. **Verify it renders** — Open it. Text that overflows its placeholder is invisible in the XML and obvious on screen.

## Best Practices

- Use placeholders, not text boxes. A deck built from free-positioned text boxes ignores the template entirely, and it will be visibly off-brand.
- The title of a slide should be a claim. If every title is a noun, the deck has no argument.
- Text overflowing a placeholder does not error — it is silently clipped or shrunk. Check the rendered output, always.
- Images must maintain their aspect ratio. Setting both width and height distorts them, and it looks amateurish.
- A chart built in PowerPoint is editable and rescales; a chart pasted as an image does not. Prefer native charts for anything that may need revision.
- Speaker notes are where the detail goes. They are also what makes the deck useful to someone who was not in the room.

## Examples

**Building on a template's layouts:**

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation("templates/corporate.pptx")   # inherit the house style

# Layouts come from the template. Inspect them rather than guessing indices.
# for i, layout in enumerate(prs.slide_layouts):
#     print(i, layout.name)
# 0 Title Slide | 1 Title and Content | 5 Title Only | 6 Blank

title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = "Q2 Operations Review"
title_slide.placeholders[1].text = "Platform Team | July 2026"

# A slide whose title is a claim, not a label.
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Availability met target every month; two incidents exceeded RTO"

body = slide.placeholders[1].text_frame
body.text = "99.94% availability against a 99.9% target"

for point in [
    "Two incidents exceeded the 30-minute recovery objective",
    "Both traced to the same cause: no automated rollback on the pricing service",
    "Automated rollback ships this quarter",
]:
    p = body.add_paragraph()
    p.text = point
    p.level = 1

# The detail lives in the notes, not on the slide.
slide.notes_slide.notes_text_frame.text = (
    "The 99.94% figure is the weighted average across all three regions. "
    "eu-west-1 was 99.87% in May, below target, driven entirely by the "
    "14 May incident. Without automated rollback, mean recovery time is "
    "41 minutes against a 30-minute objective — the incidents were not "
    "unusually severe, the recovery was unusually manual."
)

prs.save("output/q2-review.pptx")
```

**A native chart rather than a pasted image:**

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Incident count fell 40% after the rollback change"

chart_data = CategoryChartData()
chart_data.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
chart_data.add_series("Incidents", (12, 14, 11, 8, 7, 7))

slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(1.8), Inches(8), Inches(4.5),
    chart_data,
)
# Editable in PowerPoint, rescales with the slide, and readable on a projector.
```

## Notes

- The layout indices in a template are not standardized. Print the layout names before using them, or you will place a title into a picture placeholder.
- Text that overflows a placeholder is the most common defect in a generated deck, and it is invisible until the file is opened. Budget the text length, or enable autofit.
- If the deck will be sent rather than presented, the slides must carry more of the argument — but the answer is usually a document, not a denser deck.
