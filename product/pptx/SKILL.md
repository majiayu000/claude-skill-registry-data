---
name: pptx
description: Create, edit, read, and design PowerPoint presentations (.pptx). Use whenever a .pptx file is involved — creating slide decks, pitch decks, or stakeholder presentations; reading or extracting content from an existing .pptx; editing or updating slides; building from a template. Trigger on "deck", "slides", "presentation", "pitch deck", "PowerPoint", or any .pptx filename.
---

# PowerPoint Presentation (.pptx)

A `.pptx` file is a ZIP archive of XML files. You can create, edit, and read them programmatically. Choose the right approach for the task:

| Task | Approach |
|---|---|
| **Create** a new deck | `pptxgenjs` (Node) or `python-pptx` (Python) |
| **Edit** an existing deck | Unzip → edit slide XML → rezip |
| **Read** content from a deck | `markitdown deck.pptx` or unzip and parse XML |
| **Convert** to PDF | LibreOffice headless |

---

## Presentation Principles

- **Every slide has one job.** A slide that makes three points makes zero. Split ruthlessly.
- **Text-only slides are forgettable.** Every slide needs at least one visual element — chart, image, icon, data callout, or diagram.
- **The deck must work without the speaker.** Async decks (sent via email, read without a presenter) need more text and context than live-presentation decks.
- **Visual hierarchy over bullet points.** A large number + small label communicates faster than a sentence. A 2x2 grid communicates relationships better than a list.
- **Commit to a visual direction and hold it.** One font pair. One color palette. One layout style. Inconsistency signals lack of polish.
- **AI slop is obvious.** Cream backgrounds, accent stripes along card edges, Inter/Roboto with no rationale, blue CTA buttons, centered body text — these are trust killers. Avoid all of them.

---

## Step 0: Before Creating

Ask the user:

1. **What is the deck for?** (investor pitch, all-hands, client presentation, technical review, sales demo)
2. **Who is the audience?** (technical, executive, external client, general team)
3. **How many slides?** Or: what content needs to be covered?
4. **Brand constraints?** (specific colors, fonts, logo to include)
5. **Output format?** (.pptx to edit further, or PDF to send)
6. **Presenting live or sending async?** (changes text density and speaker notes needs)

---

## Creating with pptxgenjs (Node/TypeScript)

### Setup
```bash
# pptxgenjs is often pre-installed — try require first
node -e "require('pptxgenjs')" 2>/dev/null && echo "installed" || npm install pptxgenjs
```

### Basic Structure
```javascript
const pptx = require("pptxgenjs");
const pres = new pptx();

// ALWAYS set layout before adding slides
pres.layout = "LAYOUT_16x9"; // 10" × 5.625" — standard widescreen

// Define theme colors (never use # prefix, never 8-digit hex)
const COLORS = {
  primary:    "1E3A5F",  // Deep navy
  accent:     "2E86AB",  // Electric blue
  light:      "F8F9FA",  // Near white
  dark:       "212529",  // Near black
  muted:      "6C757D",  // Gray
};

// Title slide
const titleSlide = pres.addSlide();
titleSlide.background = { color: COLORS.primary };
titleSlide.addText("Your Presentation Title", {
  x: 0.5, y: 1.8, w: 9, h: 1.2,
  fontSize: 40, bold: true, color: "FFFFFF",
  align: "left",
});
titleSlide.addText("Subtitle or date", {
  x: 0.5, y: 3.0, w: 9, h: 0.5,
  fontSize: 18, color: "A8C6E8",
  align: "left",
});

await pres.writeFile({ fileName: "presentation.pptx" });
```

### Common Layout Patterns

#### Data callout slide (big numbers)
```javascript
const slide = pres.addSlide();
slide.addText("Key Metrics", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 28, bold: true, color: COLORS.dark
});

// Three metric blocks
const metrics = [
  { value: "810×", label: "Productivity increase" },
  { value: "40+",  label: "Features shipped" },
  { value: "3",    label: "Products launched" },
];

metrics.forEach((m, i) => {
  const x = 0.5 + i * 3.2;
  // Big number
  slide.addText(m.value, {
    x, y: 1.2, w: 2.8, h: 1.4,
    fontSize: 60, bold: true, color: COLORS.primary, align: "center"
  });
  // Label
  slide.addText(m.label, {
    x, y: 2.7, w: 2.8, h: 0.5,
    fontSize: 14, color: COLORS.muted, align: "center"
  });
});
```

#### Two-column slide
```javascript
const slide = pres.addSlide();
// Left column — text
slide.addText("Problem", {
  x: 0.5, y: 0.3, w: 4.2, h: 0.5,
  fontSize: 24, bold: true, color: COLORS.dark
});
slide.addText("The current checkout flow has a 23% drop-off rate on mobile...", {
  x: 0.5, y: 1.0, w: 4.2, h: 3.5,
  fontSize: 14, color: COLORS.dark, valign: "top"
});
// Right column — image or chart
slide.addImage({ path: "chart.png", x: 5.2, y: 0.5, w: 4.3, h: 4.5 });
```

#### Critical gotchas
```javascript
// ❌ WRONG — # prefix corrupts the file
color: "#FF0000"

// ✅ CORRECT — 6 hex chars, no #
color: "FF0000"

// ❌ WRONG — sharing option objects causes corruption
const shadow = { type: "outer", blur: 3, offset: 2, color: "000000" };
slide1.addShape(pptx.ShapeType.rect, { shadow }); // mutates shadow object
slide2.addShape(pptx.ShapeType.rect, { shadow }); // now uses corrupted values

// ✅ CORRECT — fresh object per call
const makeShadow = () => ({ type: "outer", blur: 3, offset: 2, color: "000000" });
slide1.addShape(pptx.ShapeType.rect, { shadow: makeShadow() });
slide2.addShape(pptx.ShapeType.rect, { shadow: makeShadow() });

// ❌ WRONG — shadow offset must be >= 0
shadow: { offset: -2 }  // corrupts file

// ✅ CORRECT
shadow: { offset: 2 }
```

---

## Creating with python-pptx

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# Add a slide using blank layout
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Add title text box
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.add_paragraph()
p.text = "Slide Title"
p.font.bold = True
p.font.size = Pt(36)
p.font.color.rgb = RGBColor(0x1E, 0x3A, 0x5F)
p.alignment = PP_ALIGN.LEFT

prs.save("presentation.pptx")
```

---

## Editing an Existing Deck

```bash
# Unzip to inspect/edit
mkdir deck_unpacked && cp deck.pptx deck.zip
unzip deck.zip -d deck_unpacked/

# Slides are at: deck_unpacked/ppt/slides/slide1.xml, slide2.xml, etc.
# Edit XML directly for text replacement, color changes, etc.

# Repack
cd deck_unpacked && zip -r ../deck_edited.pptx . && cd ..
```

For simple text replacement across all slides:
```python
from pptx import Presentation

prs = Presentation("template.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    run.text = run.text.replace("{{COMPANY}}", "Acme Corp")
prs.save("output.pptx")
```

---

## Reading / Extracting Content

```bash
# Extract all text, slide by slide
markitdown deck.pptx

# Check for placeholder text (leftover template text)
markitdown deck.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert"
```

```python
from pptx import Presentation

prs = Presentation("deck.pptx")
for i, slide in enumerate(prs.slides, 1):
    print(f"\n--- Slide {i} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text_frame.text)
```

---

## Design Standards

### Color palettes (use one, stay consistent)

| Palette | Primary | Accent | Background |
|---|---|---|---|
| Midnight Executive | `1E2761` | `CADCFC` | `FFFFFF` |
| Forest & Moss | `2C5F2D` | `97BC62` | `F5F5F5` |
| Coral Energy | `F96167` | `F9E795` | `2F3C7E` |
| Charcoal Minimal | `36454F` | `F2F2F2` | `212121` |
| Teal Trust | `028090` | `00A896` | `FFFFFF` |

### Typography
| Element | Size | Weight |
|---|---|---|
| Slide title | 36–44pt | Bold |
| Section header | 20–24pt | Bold |
| Body text | 14–16pt | Regular |
| Captions / labels | 10–12pt | Regular |

**Safe fonts** (render correctly in both PowerPoint and LibreOffice):
Arial, Calibri, Cambria, Times New Roman, Courier New

### What to never do
- ❌ Accent lines or stripes under titles (AI slop signature)
- ❌ Decorative color bars spanning slide width
- ❌ Centered body text (left-align everything except titles)
- ❌ Cream/beige background when not specified — use white
- ❌ Text-only slides — always add a visual element
- ❌ Same layout repeated on every slide
- ❌ `#` prefix in color values (pptxgenjs)
- ❌ Shared option objects across add calls (pptxgenjs)

---

## QA Before Delivering

```bash
# 1. Content check — read all text
markitdown output.pptx

# 2. Check for leftover placeholder text
markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|TODO|\[insert"

# 3. Convert to PDF for visual check
libreoffice --headless --convert-to pdf output.pptx

# 4. Visual inspection checklist:
```

Visual QA checklist (check every slide):
- [ ] No text overflowing its box or the slide edge
- [ ] No overlapping elements
- [ ] Minimum 0.5" margin from all slide edges
- [ ] Consistent gaps between content blocks (0.3" or 0.5" — pick one)
- [ ] No low-contrast text (light on light, dark on dark)
- [ ] No leftover template placeholder text
- [ ] Speaker notes added for any slide that needs explanation

---

## Definition of Done — PPTX

- [ ] Deck purpose, audience, and slide count confirmed before starting
- [ ] Layout set before first slide added (`pres.layout = "LAYOUT_16x9"`)
- [ ] Color palette defined — no `#` prefix, no 8-digit hex
- [ ] One font pair used consistently throughout
- [ ] Every slide has at least one visual element (no text-only slides)
- [ ] No accent stripes, decorative bars, or cream backgrounds
- [ ] No AI slop patterns (see list above)
- [ ] Content QA run: `markitdown output.pptx`
- [ ] Placeholder text check: no leftover `lorem`, `TODO`, `[insert]`
- [ ] Visual QA: every slide inspected for overflow, overlap, contrast
- [ ] Speaker notes added where needed
- [ ] File opens without errors in PowerPoint / LibreOffice
