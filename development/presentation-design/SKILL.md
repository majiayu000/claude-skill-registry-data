---
name: presentation-design
description: Techniques and code examples for creating professional slide decks and presentations. Use this skill to structure narratives, apply design principles, and automate slide generation.
license: MIT
metadata:
  category: documents
---
# Presentation Design Guide

## Overview

This skill offers guidance on crafting compelling presentations, from storyboarding to slide aesthetics, and includes code snippets for generating slides programmatically.

## Storytelling Principles

- **Structure**: Use a clear beginning, middle, and end. Start with a hook, explain the problem, present the solution, and conclude with a call to action.
- **Simplicity**: Limit each slide to one idea. Avoid clutter and excessive text.
- **Visuals**: Use images, diagrams, and charts to reinforce key points.

## Design Guidelines

- **Consistency**: Maintain consistent fonts, colors, and alignment.
- **Contrast**: Ensure text contrasts with backgrounds for readability.
- **Hierarchy**: Use headings and varying font sizes to guide the viewer's eye.
- **White space**: Leave space around elements to avoid overcrowding.

## Creating Slides with python-pptx

Install the library:

```bash
pip install python-pptx
```

### Basic Slide

```python
from pptx import Presentation

prs = Presentation()
slide_layout = prs.slide_layouts[0]  # Title slide
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "My Presentation"
subtitle.text = "An overview of our project"

prs.save("presentation.pptx")
```

### Adding Charts

```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

chart_data = ChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Sales', (10, 15, 12, 18))

slide_layout = prs.slide_layouts[5]  # Title and content
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
title.text = "Quarterly Sales"

# Add chart
x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(4.5)
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
).chart

prs.save("presentation_with_chart.pptx")
```

## Tips for Effective Slides

- Use high-quality images and icons (unsplash.com, fontawesome).
- Limit bullet points; use visuals to illustrate data.
- Use speaker notes to expand on slide content.
- Practice delivering your slides to refine timing and transitions.

## Additional Resources

- *Presentation Zen* by Garr Reynolds.
- Nancy Duarte’s Resonate framework.
- python-pptx documentation.
