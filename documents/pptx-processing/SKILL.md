---
name: pptx-processing
description: >
  Generate, edit, and inspect modern PowerPoint (.pptx) presentation decks
  programmatically using python-pptx. Use when building executive slide decks,
  enforcing 16:9 widescreen layouts, adding structured tables and callout shapes,
  configuring speaker notes, or verifying typography and visual slide balance.
compatibility: >
  Agent Skills-compatible coding agents operating with Python presentation
  manipulation libraries (python-pptx).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "pptx, powerpoint, python-pptx, slides, presentations, office"
  topics: "office, documentation, devtools"
---

# Programmatic PowerPoint (.pptx) Processing

Microsoft PowerPoint files (`.pptx`) are OpenXML slide presentation packages. Generating professional presentations programmatically requires establishing consistent master layouts, adhering to modern 16:9 widescreen ratios, controlling typographic hierarchy, positioning shapes using precise coordinate metrics, and embedding speaker notes.

Detailed reference guides:
- [python-pptx Layouts, Shapes & Tables Guide](references/python-pptx-guide.md)

---

## The 6-Step Presentation Engineering Workflow

1. **Inspect Requirements**: Define slide count, aspect ratio (16:9 Widescreen vs 4:3 Standard), master color palette, and corporate typography.
2. **Select Tooling**: Use `python-pptx` in Python for reliable OpenXML deck generation.
3. **Establish Layout Template**: Set 16:9 dimensions (`Inches(13.333)` x `Inches(7.5)`) and choose standard slide layouts from the master.
4. **Build Slides with Restraint**: Limit each slide to one core message, high-contrast headings, concise bullet points, and clean structured tables.
5. **Attach Speaker Notes & Accessibility**: Add presenter notes to slides to explain background context; set descriptive titles for screen readers.
6. **Save & Validate Visual Balance**: Save to `.pptx` and verify margins, text wrapping, and alignment.

---

## 1. Generating a Widescreen Deck with `python-pptx`

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def generate_deck(output_path: str):
    prs = Presentation()

    # 1. Configure 16:9 Modern Widescreen Dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Blank layout index is typically 6 in standard templates
    blank_layout = prs.slide_layouts[6]

    # --- Slide 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)

    # Title Box
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.0))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "Cloud Infrastructure Modernization"
    p1.font.name = "Helvetica"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Deep Slate

    # Subtitle
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Q4 Strategic Roadmap & Execution Timeline"
    p1_sub.font.size = Pt(20)
    p1_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69) # Slate

    # Speaker notes for Slide 1
    slide1.notes_slide.notes_text_frame.text = (
        "Welcome attendees. Highlight that this session covers the multi-region migration timeline."
    )

    # --- Slide 2: Metrics Table & Key Takeaways ---
    slide2 = prs.slides.add_slide(blank_layout)

    # Slide Header
    header_box = slide2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf2 = header_box.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "Key Performance Indicators"
    p2.font.size = Pt(32)
    p2.font.bold = True

    # Structured Table (4 rows x 3 columns)
    rows, cols = 4, 3
    left, top, width, height = Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.2)
    table_shape = slide2.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(4.333)
    table.columns[1].width = Inches(3.5)
    table.columns[2].width = Inches(3.5)

    headers = ["Metric", "Q3 Baseline", "Target Q4"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data = [
        ["API p99 Latency", "120 ms", "< 25 ms"],
        ["Availability SLA", "99.9%", "99.99%"],
        ["Compute Cost / User", "$0.042", "$0.028"],
    ]

    for r_idx, row in enumerate(data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.text_frame.paragraphs[0].font.size = Pt(14)

    prs.save(output_path)
    print(f"Presentation saved successfully: {output_path}")

if __name__ == "__main__":
    generate_deck("strategic_roadmap.pptx")
```

---

## 2. Common Mistakes and Anti-Patterns

| Anti-Pattern | Visual / Technical Risk | Correct Practice |
| :--- | :--- | :--- |
| Defaulting to 4:3 square slides | Pillarboxed black bars on modern monitors | Set explicit 16:9 widescreen dimensions (`13.333 x 7.5` in) |
| Wall of tiny text (font < 14pt) | Unreadable during presentations | Use 28-36pt for headings, 16-20pt for body text |
| Overflowing text boxes | Text cuts off or overlaps other shapes | Always set `text_frame.word_wrap = True` and test dimensions |
| Inconsistent margin alignment across slides | Jarring visual jumps when advancing slides | Use standardized left margin (`Inches(1.0)`) across all slides |

---

## 3. Verification Checklist

- [ ] Presentation aspect ratio configured as 16:9 Widescreen.
- [ ] Heading font sizes >= 28pt; body font sizes >= 16pt.
- [ ] Word wrapping explicitly enabled on text frames.
- [ ] Speaker notes added to key slides.
- [ ] Validated with `zipfile.is_zipfile(path)` and verified visual hierarchy.
