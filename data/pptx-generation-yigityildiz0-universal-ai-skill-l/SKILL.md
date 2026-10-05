---
name: pptx-generation
description: PowerPoint presentation generation expertise for creating, editing, and designing professional slide decks programmatically. Use when building presentation.
---

# PPTX Generation

Structured guidance for building systems that generate professional PowerPoint presentations programmatically. Covers library selection, slide layout design, chart integration, master slide management, template-based generation, batch processing, and quality assurance strategies for automated presentation pipelines.

## When to Use This Skill

Use this skill for:

- Building automated presentation generators from structured data
- Creating report decks (financial summaries, analytics dashboards, project status updates)
- Designing reusable slide templates with consistent corporate branding
- Adding charts, tables, and data visualizations to slides programmatically
- Populating existing PowerPoint templates with dynamic content
- Batch-generating personalized slide decks from datasets (mail merge pattern)
- Integrating presentation generation into CI/CD pipelines or reporting workflows
- Converting Markdown, JSON, or database records into formatted slide decks

**Trigger phrases**: "pptx", "PowerPoint generation", "slide deck", "presentation builder", "python-pptx", "PptxGenJS", "slide template", "chart slides", "automated reports", "batch presentations", "slide layouts", "master slides", "branding deck", "report generator", "slide automation"

## What This Skill Does

Provides presentation generation patterns including:

- **Library Selection**: Decision matrix for python-pptx, PptxGenJS, Apache POI, and LibreOffice approaches
- **Slide Design**: Layout patterns for title, content, two-column, section divider, and closing slides
- **Charts and Data**: Bar, line, pie, scatter, and combo charts with data-driven generation
- **Master Slides**: Theme management, color schemes, font families, and brand consistency
- **Templates**: Loading existing .pptx templates, populating placeholders, and extending layouts
- **Batch Generation**: Mail merge patterns, data-driven deck creation, and parallel processing
- **Quality Assurance**: Slide count verification, content extraction, visual validation, and file size optimization

## Instructions

### Step 1: Library Selection

Choose a PPTX generation library based on your runtime environment, feature requirements, and integration constraints. The following decision matrix compares the four primary options.

**Library Comparison Matrix**:

| Criteria | python-pptx | PptxGenJS | Apache POI | LibreOffice (CLI) |
|----------|-------------|-----------|------------|-------------------|
| Language | Python | JavaScript/TypeScript | Java/Kotlin | Any (CLI wrapper) |
| License | MIT | MIT | Apache 2.0 | MPL 2.0 |
| Template support | Full (load/modify .pptx) | Limited (no template loading) | Full (load/modify .pptx) | Full (via UNO API) |
| Chart support | Native (OOXML charts) | Built-in chart types | Native (OOXML charts) | Full (via template) |
| Table support | Full with merged cells | Full with styling | Full with merged cells | Full |
| Image support | PNG, JPEG, SVG (via EMF) | PNG, JPEG, SVG, GIF | PNG, JPEG, EMF, WMF | All formats |
| Master slides | Read and modify | Create from scratch only | Read and modify | Read and modify |
| File size | Small (efficient XML) | Small | Medium (Java overhead) | Depends on conversion |
| Dependencies | Pure Python | Zero dependencies (browser/Node) | JVM required | LibreOffice installation |
| Maturity | Stable, widely used | Active, growing | Very mature | Very mature |
| Best for | Backend report generation | Browser/Node slide builders | Enterprise Java stacks | Converting other formats |

**Decision Guide**:

- **Choose python-pptx** when you have a Python backend, need to load and modify existing templates, require native OOXML chart support, or are building data pipeline report generators
- **Choose PptxGenJS** when you need browser-side generation, are building a Node.js service, want zero-dependency simplicity, or need to generate slides from a web application
- **Choose Apache POI** when you are in a Java/Kotlin ecosystem, need enterprise-grade OOXML manipulation, or must integrate with existing Java reporting infrastructure
- **Choose LibreOffice CLI** when you need to convert other formats (HTML, Markdown, ODP) to PPTX, require a headless server-side converter, or need PDF export from slides

**Installation**:

```bash
# python-pptx (Python)
pip install python-pptx
# or with uv
uv pip install python-pptx

# PptxGenJS (Node.js)
npm install pptxgenjs
# or browser via CDN
# <script src="https://cdn.jsdelivr.net/npm/pptxgenjs/dist/pptxgenjs.bundle.js"></script>

# Apache POI (Maven)
# <dependency>
#   <groupId>org.apache.poi</groupId>
#   <artifactId>poi-ooxml</artifactId>
#   <version>5.2.5</version>
# </dependency>

# LibreOffice CLI (system package)
# apt install libreoffice-impress   # Debian/Ubuntu
# brew install --cask libreoffice   # macOS
```

### Step 2: Python python-pptx Fundamentals

python-pptx is the most popular Python library for creating and modifying PowerPoint files. It provides full access to the OOXML presentation model including slides, layouts, placeholders, shapes, text frames, tables, charts, and images.

**Core Object Model**:

```
Presentation
  -> SlideMasters[]
       -> SlideLayouts[]
  -> Slides[]
       -> Shapes[]
            -> TextFrame -> Paragraphs[] -> Runs[]
            -> Table -> Rows[] -> Cells[]
            -> Chart -> ChartData
            -> Picture
```

**Creating a Presentation from Scratch**:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def create_presentation() -> Presentation:
    """Create a new presentation with standard 16:9 dimensions."""
    prs = Presentation()
    # Set slide dimensions to 16:9 (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs
```

**Understanding Slide Layouts**:

Every presentation has a slide master that contains slide layouts. The default template provides these standard layouts:

```python
def list_available_layouts(prs: Presentation) -> list[dict]:
    """List all available slide layouts from the slide master."""
    layouts = []
    for idx, layout in enumerate(prs.slide_masters[0].slide_layouts):
        layouts.append({
            "index": idx,
            "name": layout.name,
            "placeholders": [
                {"idx": ph.placeholder_format.idx, "name": ph.name, "type": ph.placeholder_format.type}
                for ph in layout.placeholders
            ],
        })
    return layouts

# Standard layout indices (default template):
# 0 = Title Slide (title + subtitle)
# 1 = Title and Content (title + body)
# 2 = Section Header
# 3 = Two Content (title + two body columns)
# 4 = Comparison (title + two columns with subtitles)
# 5 = Title Only
# 6 = Blank
# 7 = Content with Caption
# 8 = Picture with Caption
```

**Adding Slides with Text**:

```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def add_title_slide(
    prs: Presentation,
    title: str,
    subtitle: str,
) -> None:
    """Add a title slide (layout index 0) with title and subtitle."""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    slide.placeholders[0].text = title
    slide.placeholders[1].text = subtitle


def add_content_slide(
    prs: Presentation,
    title: str,
    body_text: str,
    bullet_points: list[str] | None = None,
) -> None:
    """Add a title-and-content slide (layout index 1) with formatted text."""
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    slide.placeholders[0].text = title

    # Set body content
    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()

    if body_text:
        paragraph = text_frame.paragraphs[0]
        paragraph.text = body_text
        paragraph.font.size = Pt(18)
        paragraph.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    if bullet_points:
        for point in bullet_points:
            paragraph = text_frame.add_paragraph()
            paragraph.text = point
            paragraph.level = 0
            paragraph.font.size = Pt(16)
            paragraph.space_after = Pt(6)
```

**Working with Text Frames and Runs**:

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def add_formatted_text(
    prs: Presentation,
    title: str,
    content_blocks: list[dict],
) -> None:
    """Add a slide with rich text formatting using runs.

    Each content_block: {"text": str, "bold": bool, "size": int, "color": str}
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only layout
    slide.placeholders[0].text = title

    # Add a text box for custom-positioned content
    from pptx.util import Inches
    left = Inches(1.0)
    top = Inches(2.0)
    width = Inches(11.0)
    height = Inches(4.5)
    text_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = text_box.text_frame
    text_frame.word_wrap = True

    for idx, block in enumerate(content_blocks):
        if idx == 0:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()

        run = paragraph.add_run()
        run.text = block["text"]
        run.font.size = Pt(block.get("size", 14))
        run.font.bold = block.get("bold", False)
        run.font.italic = block.get("italic", False)

        color_hex = block.get("color", "333333")
        run.font.color.rgb = RGBColor.from_string(color_hex)

    # Set paragraph alignment
    for paragraph in text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.LEFT
```

**Adding Images**:

```python
from pptx.util import Inches

def add_image_slide(
    prs: Presentation,
    title: str,
    image_path: str,
    left: float = 2.0,
    top: float = 2.0,
    width: float = 9.0,
) -> None:
    """Add a slide with a positioned image.

    The height is calculated automatically to maintain aspect ratio.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.placeholders[0].text = title

    slide.shapes.add_picture(
        image_path,
        left=Inches(left),
        top=Inches(top),
        width=Inches(width),
        # height omitted: auto-calculated from aspect ratio
    )
```

**Adding Tables**:

```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def add_table_slide(
    prs: Presentation,
    title: str,
    headers: list[str],
    rows: list[list[str]],
) -> None:
    """Add a slide with a formatted data table."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.placeholders[0].text = title

    row_count = len(rows) + 1  # +1 for header
    col_count = len(headers)
    left = Inches(1.0)
    top = Inches(2.0)
    width = Inches(11.0)
    height = Inches(0.5 * row_count)

    table_shape = slide.shapes.add_table(
        row_count, col_count, left, top, width, height,
    )
    table = table_shape.table

    # Style header row
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.bold = True
            paragraph.font.size = Pt(12)
            paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            paragraph.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x2E, 0x4A, 0x7A)

    # Populate data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(cell_value)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(11)
                paragraph.alignment = PP_ALIGN.LEFT

    # Set column widths proportionally
    total_width = Inches(11.0)
    col_width = int(total_width / col_count)
    for col_idx in range(col_count):
        table.columns[col_idx].width = col_width
```

**Saving the Presentation**:

```python
from pathlib import Path

def save_presentation(prs: Presentation, output_path: str | Path) -> Path:
    """Save presentation to disk and return the resolved path."""
    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))
    return output
```

### Step 3: JavaScript PptxGenJS

PptxGenJS is a zero-dependency JavaScript library that generates PPTX files in both browser and Node.js environments. It provides a fluent API for creating slides with text, images, charts, tables, and shapes.

**Creating a Presentation (Node.js)**:

```typescript
import PptxGenJS from "pptxgenjs";

interface SlideTheme {
  primaryColor: string;
  secondaryColor: string;
  fontFamily: string;
  titleSize: number;
  bodySize: number;
}

const DEFAULT_THEME: SlideTheme = {
  primaryColor: "2E4A7A",
  secondaryColor: "5B8DEF",
  fontFamily: "Segoe UI",
  titleSize: 28,
  bodySize: 14,
};

function createPresentation(theme: SlideTheme = DEFAULT_THEME): PptxGenJS {
  const pptx = new PptxGenJS();

  // Set presentation metadata
  pptx.author = "Automated Report Generator";
  pptx.company = "Your Company";
  pptx.subject = "Generated Presentation";

  // Set 16:9 layout
  pptx.layout = "LAYOUT_16x9";

  // Define reusable master slides
  pptx.defineSlideMaster({
    title: "TITLE_SLIDE",
    background: { color: theme.primaryColor },
    objects: [
      {
        placeholder: {
          options: {
            name: "title",
            type: "title",
            x: 1.0,
            y: 2.5,
            w: 11.0,
            h: 1.5,
            fontFace: theme.fontFamily,
            fontSize: 36,
            color: "FFFFFF",
            align: "center",
          },
          text: "",
        },
      },
      {
        placeholder: {
          options: {
            name: "subtitle",
            type: "body",
            x: 2.0,
            y: 4.2,
            w: 9.0,
            h: 1.0,
            fontFace: theme.fontFamily,
            fontSize: 18,
            color: "CCCCCC",
            align: "center",
          },
          text: "",
        },
      },
    ],
  });

  pptx.defineSlideMaster({
    title: "CONTENT_SLIDE",
    background: { color: "FFFFFF" },
    objects: [
      {
        rect: {
          x: 0,
          y: 0,
          w: "100%",
          h: 0.75,
          fill: { color: theme.primaryColor },
        },
      },
      {
        placeholder: {
          options: {
            name: "title",
            type: "title",
            x: 0.5,
            y: 0.1,
            w: 12.0,
            h: 0.55,
            fontFace: theme.fontFamily,
            fontSize: 22,
            color: "FFFFFF",
            bold: true,
          },
          text: "",
        },
      },
    ],
  });

  return pptx;
}
```

**Adding Slides with Content**:

```typescript
function addTitleSlide(
  pptx: PptxGenJS,
  title: string,
  subtitle: string,
): void {
  const slide = pptx.addSlide({ masterName: "TITLE_SLIDE" });
  slide.addText(title, {
    placeholder: "title",
  });
  slide.addText(subtitle, {
    placeholder: "subtitle",
  });
}

function addContentSlide(
  pptx: PptxGenJS,
  title: string,
  bulletPoints: string[],
  theme: SlideTheme = DEFAULT_THEME,
): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  const textRows = bulletPoints.map((point) => ({
    text: point,
    options: {
      fontSize: theme.bodySize,
      fontFace: theme.fontFamily,
      color: "333333",
      bullet: { type: "bullet" as const },
      paraSpaceAfter: 6,
    },
  }));

  slide.addText(textRows, {
    x: 0.75,
    y: 1.2,
    w: 11.5,
    h: 5.5,
    valign: "top",
  });
}
```

**Adding Tables**:

```typescript
interface TableConfig {
  headers: string[];
  rows: string[][];
  theme?: SlideTheme;
}

function addTableSlide(
  pptx: PptxGenJS,
  title: string,
  config: TableConfig,
): void {
  const theme = config.theme ?? DEFAULT_THEME;
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  const headerRow: PptxGenJS.TableCell[] = config.headers.map((h) => ({
    text: h,
    options: {
      bold: true,
      color: "FFFFFF",
      fill: { color: theme.primaryColor },
      fontSize: 11,
      align: "center" as const,
    },
  }));

  const dataRows: PptxGenJS.TableCell[][] = config.rows.map((row) =>
    row.map((cell) => ({
      text: cell,
      options: {
        fontSize: 10,
        color: "333333",
        border: { type: "solid", pt: 0.5, color: "CCCCCC" },
      },
    })),
  );

  slide.addTable([headerRow, ...dataRows], {
    x: 0.5,
    y: 1.2,
    w: 12.0,
    colW: config.headers.map(() => 12.0 / config.headers.length),
    rowH: 0.4,
    autoPage: true,
    autoPageRepeatHeader: true,
  });
}
```

**Adding Images and Shapes**:

```typescript
import * as fs from "node:fs";
import * as path from "node:path";

function addImageSlide(
  pptx: PptxGenJS,
  title: string,
  imagePath: string,
): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  // Read image as base64 for Node.js
  const imageBuffer = fs.readFileSync(imagePath);
  const base64 = imageBuffer.toString("base64");
  const ext = path.extname(imagePath).slice(1).toLowerCase();

  slide.addImage({
    data: `image/${ext};base64,${base64}`,
    x: 2.0,
    y: 1.5,
    w: 9.0,
    h: 5.0,
    sizing: { type: "contain", w: 9.0, h: 5.0 },
  });
}

function addShapeSlide(pptx: PptxGenJS, title: string): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  // Add a rounded rectangle with text
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 3.0,
    y: 2.0,
    w: 7.0,
    h: 3.0,
    fill: { color: "E8F0FE" },
    line: { color: "2E4A7A", width: 2 },
    rectRadius: 0.2,
  });

  slide.addText("Key Insight", {
    x: 3.5,
    y: 3.0,
    w: 6.0,
    h: 1.0,
    fontSize: 24,
    color: "2E4A7A",
    align: "center",
    bold: true,
  });
}
```

**Saving (Node.js and Browser)**:

```typescript
// Node.js: save to file
async function saveToFile(
  pptx: PptxGenJS,
  outputPath: string,
): Promise<string> {
  await pptx.writeFile({ fileName: outputPath });
  return outputPath;
}

// Browser: trigger download
async function downloadInBrowser(
  pptx: PptxGenJS,
  fileName: string,
): Promise<void> {
  await pptx.writeFile({ fileName });
  // PptxGenJS handles the browser download automatically
}

// Get as base64 (for API responses)
async function toBase64(pptx: PptxGenJS): Promise<string> {
  const output = await pptx.write({ outputType: "base64" });
  return output as string;
}
```

### Step 4: Slide Design Patterns

Consistent slide design requires a defined system of layout types, spacing rules, and visual hierarchy. The following patterns cover the most common slide types needed in automated presentation generation.

**Slide Type Taxonomy**:

| Slide Type | Purpose | Layout | Key Elements |
|------------|---------|--------|-------------|
| Title Slide | Opening, section start | Full background color | Title (36pt), subtitle (18pt), logo |
| Content Slide | Body information | Header bar + white body | Title (22pt), bullets/text (14pt) |
| Two-Column | Comparison, dual info | Header bar + two panels | Title, left column, right column |
| Section Divider | Topic transition | Accent background | Section title (32pt), section number |
| Data Slide | Charts and tables | Header bar + data area | Title, chart/table, source note |
| Image Slide | Visuals, screenshots | Header bar + image area | Title, image (contain fit), caption |
| Key Takeaway | Emphasis, callout | Accent background | Icon, headline (28pt), supporting text |
| Closing Slide | End, contact info | Full background color | Thank you text, contact details, logo |

**Design System Constants** (python-pptx):

```python
from dataclasses import dataclass
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


@dataclass(frozen=True)
class DesignSystem:
    """Centralized design constants for consistent slide generation."""

    # Colors
    primary: RGBColor = RGBColor(0x2E, 0x4A, 0x7A)
    secondary: RGBColor = RGBColor(0x5B, 0x8D, 0xEF)
    accent: RGBColor = RGBColor(0xE8, 0x6C, 0x00)
    text_dark: RGBColor = RGBColor(0x33, 0x33, 0x33)
    text_light: RGBColor = RGBColor(0xFF, 0xFF, 0xFF)
    background_light: RGBColor = RGBColor(0xF5, 0xF7, 0xFA)
    border: RGBColor = RGBColor(0xDD, 0xDD, 0xDD)

    # Typography
    font_family: str = "Segoe UI"
    title_size: Pt = Pt(28)
    heading_size: Pt = Pt(22)
    body_size: Pt = Pt(14)
    caption_size: Pt = Pt(10)

    # Spacing (16:9 slide = 13.333 x 7.5 inches)
    margin_left: Inches = Inches(0.75)
    margin_top: Inches = Inches(1.0)
    content_width: Inches = Inches(11.83)
    content_height: Inches = Inches(5.75)
    header_height: Inches = Inches(0.75)
    footer_height: Inches = Inches(0.4)


DESIGN = DesignSystem()
```

**Two-Column Layout**:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def add_two_column_slide(
    prs: Presentation,
    title: str,
    left_title: str,
    left_points: list[str],
    right_title: str,
    right_points: list[str],
) -> None:
    """Add a two-column comparison slide with independent bullet lists."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.placeholders[0].text = title

    column_width = Inches(5.5)
    left_x = Inches(0.75)
    right_x = Inches(7.0)
    top_y = Inches(1.5)
    height = Inches(5.0)

    for col_x, col_title, points in [
        (left_x, left_title, left_points),
        (right_x, right_title, right_points),
    ]:
        text_box = slide.shapes.add_textbox(col_x, top_y, column_width, height)
        tf = text_box.text_frame
        tf.word_wrap = True

        # Column header
        p = tf.paragraphs[0]
        p.text = col_title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = DESIGN.primary
        p.space_after = Pt(12)

        # Bullet points
        for point in points:
            p = tf.add_paragraph()
            p.text = point
            p.font.size = Pt(13)
            p.font.color.rgb = DESIGN.text_dark
            p.level = 0
            p.space_after = Pt(6)
```

**Section Divider Slide**:

```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def add_section_divider(
    prs: Presentation,
    section_number: int,
    section_title: str,
) -> None:
    """Add a section divider slide with number and title on accent background."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Full-slide background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DESIGN.primary

    # Section number
    num_box = slide.shapes.add_textbox(
        Inches(1.0), Inches(2.0), Inches(11.0), Inches(1.5),
    )
    num_tf = num_box.text_frame
    num_tf.paragraphs[0].text = f"0{section_number}" if section_number < 10 else str(section_number)
    num_tf.paragraphs[0].font.size = Pt(60)
    num_tf.paragraphs[0].font.bold = True
    num_tf.paragraphs[0].font.color.rgb = DESIGN.secondary
    num_tf.paragraphs[0].alignment = PP_ALIGN.LEFT

    # Section title
    title_box = slide.shapes.add_textbox(
        Inches(1.0), Inches(3.5), Inches(11.0), Inches(1.5),
    )
    title_tf = title_box.text_frame
    title_tf.paragraphs[0].text = section_title
    title_tf.paragraphs[0].font.size = Pt(32)
    title_tf.paragraphs[0].font.color.rgb = DESIGN.text_light
    title_tf.paragraphs[0].alignment = PP_ALIGN.LEFT
```

**Closing Slide**:

```python
def add_closing_slide(
    prs: Presentation,
    title: str = "Thank You",
    contact_info: dict | None = None,
) -> None:
    """Add a closing slide with optional contact information."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DESIGN.primary

    # Main title
    title_box = slide.shapes.add_textbox(
        Inches(1.0), Inches(2.5), Inches(11.0), Inches(1.5),
    )
    tf = title_box.text_frame
    tf.paragraphs[0].text = title
    tf.paragraphs[0].font.size = Pt(36)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = DESIGN.text_light
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Contact details
    if contact_info:
        info_box = slide.shapes.add_textbox(
            Inches(3.0), Inches(4.5), Inches(7.0), Inches(2.0),
        )
        info_tf = info_box.text_frame
        for key, value in contact_info.items():
            p = info_tf.add_paragraph()
            run = p.add_run()
            run.text = f"{key}: {value}"
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
            p.alignment = PP_ALIGN.CENTER
            p.space_after = Pt(4)
```

### Step 5: Charts and Data Visualization

Both python-pptx and PptxGenJS support native OOXML chart generation. Charts are embedded directly in the PPTX file as editable objects that PowerPoint can re-render.

**Bar Chart (python-pptx)**:

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def add_bar_chart_slide(
    prs: Presentation,
    title: str,
    categories: list[str],
    series_data: dict[str, list[float]],
    chart_title: str = "",
) -> None:
    """Add a slide with a clustered bar chart.

    Args:
        prs: Target presentation.
        title: Slide title.
        categories: X-axis category labels.
        series_data: Mapping of series name to list of values.
        chart_title: Optional chart title displayed above the chart area.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.placeholders[0].text = title

    chart_data = CategoryChartData()
    chart_data.categories = categories
    for series_name, values in series_data.items():
        chart_data.add_series(series_name, values)

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1.0), Inches(1.5),
        Inches(11.0), Inches(5.5),
        chart_data,
    )
    chart = chart_shape.chart

    # Configure chart appearance
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False

    if chart_title:
        chart.has_title = True
        chart.chart_title.text_frame.paragraphs[0].text = chart_title
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(14)

    # Style the value axis
    value_axis = chart.value_axis
    value_axis.has_title = False
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)

    # Style the category axis
    category_axis = chart.category_axis
    category_axis.has_major_gridlines = False
    category_axis.tick_labels.font.size = Pt(10)

    # Apply colors to each series
    colors = ["2E4A7A", "5B8DEF", "E86C00", "2ECC71", "E74C3C"]
    plot = chart.plots[0]
    for idx, series in enumerate(plot.series):
        fill = series.format.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(colors[idx % len(colors)])
```

**Line Chart (python-pptx)**:

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_line_chart_slide(
    prs: Presentation,
    title: str,
    categories: list[str],
    series_data: dict[str, list[float]],
    smooth_lines: bool = False,
) -> None:
    """Add a slide with a line chart, optionally with smoothed lines."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.placeholders[0].text = title

    chart_data = CategoryChartData()
    chart_data.categories = categories
    for series_name, values in series_data.items():
        chart_data.add_series(series_name, values)

    chart_type = (
        XL_CHART_TYPE.LINE_MARKERS_STACKED
        if not smooth_lines
        else XL_CHART_TYPE.LINE
    )

    chart_shape = slide.shapes.add_chart(
        chart_type,
        Inches(1.0), Inches(1.5),
        Inches(11.0), Inches(5.5),
        chart_data,
    )
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM

    # Configure smooth lines if requested
    if smooth_lines:
        for series in chart.series:
            series.smooth = True
```

**Pie Chart (python-pptx)**:

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION

def add_pie_chart_slide(
    prs: Presentation,
    title: str,
    categories: list[str],
    values: list[float],
    show_percentages: bool = True,
) -> None:
    """Add a slide with a pie chart showing category distribution."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.placeholders[0].text = title

    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("Values", values)

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE,
        Inches(2.5), Inches(1.5),
        Inches(8.0), Inches(5.5),
        chart_data,
    )
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT

    # Configure data labels
    plot = chart.plots[0]
    data_labels = plot.data_labels
    data_labels.show_category_name = True
    data_labels.show_percentage = show_percentages
    data_labels.show_value = not show_percentages
    data_labels.font.size = Pt(10)
    data_labels.number_format = "0.0%" if show_percentages else "0"
```

**Charts in PptxGenJS**:

```typescript
function addBarChartSlide(
  pptx: PptxGenJS,
  title: string,
  chartData: { name: string; labels: string[]; values: number[] }[],
): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 0.75,
    y: 1.2,
    w: 11.5,
    h: 5.5,
    showLegend: true,
    legendPos: "b",
    showValue: false,
    catAxisOrientation: "minMax",
    valAxisOrientation: "minMax",
    chartColors: ["2E4A7A", "5B8DEF", "E86C00", "2ECC71"],
    valGridLine: { color: "DDDDDD", size: 0.5 },
  });
}

function addLineChartSlide(
  pptx: PptxGenJS,
  title: string,
  chartData: { name: string; labels: string[]; values: number[] }[],
): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  slide.addChart(pptx.ChartType.line, chartData, {
    x: 0.75,
    y: 1.2,
    w: 11.5,
    h: 5.5,
    showLegend: true,
    legendPos: "b",
    lineSmooth: true,
    lineSize: 2,
    showMarker: true,
    chartColors: ["2E4A7A", "5B8DEF", "E86C00"],
  });
}

function addPieChartSlide(
  pptx: PptxGenJS,
  title: string,
  chartData: { name: string; labels: string[]; values: number[] }[],
): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  slide.addChart(pptx.ChartType.pie, chartData, {
    x: 2.0,
    y: 1.2,
    w: 9.0,
    h: 5.5,
    showLegend: true,
    legendPos: "r",
    showPercent: true,
    showTitle: false,
    chartColors: ["2E4A7A", "5B8DEF", "E86C00", "2ECC71", "E74C3C", "9B59B6"],
  });
}
```

**Scatter Chart (python-pptx)**:

```python
from pptx.chart.data import XyChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_scatter_chart_slide(
    prs: Presentation,
    title: str,
    series_data: dict[str, list[tuple[float, float]]],
) -> None:
    """Add a slide with a scatter (XY) chart.

    Args:
        series_data: Mapping of series name to list of (x, y) tuples.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.placeholders[0].text = title

    chart_data = XyChartData()
    for series_name, points in series_data.items():
        series = chart_data.add_series(series_name)
        for x, y in points:
            series.add_data_point(x, y)

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.XY_SCATTER,
        Inches(1.0), Inches(1.5),
        Inches(11.0), Inches(5.5),
        chart_data,
    )
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
```

### Step 6: Advanced Features

**Master Slide Templates with python-pptx**:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
import copy


def create_branded_presentation(
    company_name: str,
    primary_color: str = "2E4A7A",
    logo_path: str | None = None,
) -> Presentation:
    """Create a presentation with custom branded master slides.

    Modifies the default slide master to apply corporate branding
    including colors, fonts, and an optional logo.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Access the slide master
    slide_master = prs.slide_masters[0]

    # Set the background color of the title layout
    title_layout = prs.slide_layouts[0]
    background = title_layout.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(primary_color)

    return prs
```

**Speaker Notes**:

```python
def add_slide_with_notes(
    prs: Presentation,
    title: str,
    content: str,
    speaker_notes: str,
) -> None:
    """Add a content slide with speaker notes for the presenter."""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.placeholders[0].text = title
    slide.placeholders[1].text = content

    # Add speaker notes
    notes_slide = slide.notes_slide
    notes_text_frame = notes_slide.notes_text_frame
    notes_text_frame.text = speaker_notes
```

**Adding Logos to Every Slide**:

```python
from pptx.util import Inches

def add_logo_to_all_slides(
    prs: Presentation,
    logo_path: str,
    width: float = 1.2,
    position: str = "bottom-right",
) -> None:
    """Add a logo image to every slide in the presentation.

    Position options: "top-left", "top-right", "bottom-left", "bottom-right".
    """
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    logo_width = Inches(width)

    positions = {
        "top-left": (Inches(0.3), Inches(0.2)),
        "top-right": (slide_width - logo_width - Inches(0.3), Inches(0.2)),
        "bottom-left": (Inches(0.3), slide_height - Inches(0.8)),
        "bottom-right": (slide_width - logo_width - Inches(0.3), slide_height - Inches(0.8)),
    }
    left, top = positions.get(position, positions["bottom-right"])

    for slide in prs.slides:
        slide.shapes.add_picture(logo_path, left, top, width=logo_width)
```

**Hyperlinks**:

```python
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

def add_hyperlink_text(
    prs: Presentation,
    title: str,
    links: list[dict],
) -> None:
    """Add a slide with clickable hyperlinks.

    Each link: {"text": str, "url": str, "description": str}
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.placeholders[0].text = title

    text_box = slide.shapes.add_textbox(
        Inches(1.0), Inches(2.0), Inches(11.0), Inches(4.5),
    )
    tf = text_box.text_frame
    tf.word_wrap = True

    for idx, link_info in enumerate(links):
        if idx == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        run = p.add_run()
        run.text = link_info["text"]
        run.font.size = Pt(16)
        run.font.color.rgb = DESIGN.secondary
        run.font.underline = True

        # Set the hyperlink via the OOXML run element
        r_element = run._r
        hlinkClick = parse_xml(
            f'<a:hlinkClick xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        )
        r_props = r_element.get_or_add_rPr()
        r_props.append(hlinkClick)

        # Add the relationship
        rel = slide.part.relate_to(
            link_info["url"],
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            is_external=True,
        )
        hlinkClick.set(qn("r:id"), rel.rId)

        if link_info.get("description"):
            desc_p = tf.add_paragraph()
            desc_p.text = f"  {link_info['description']}"
            desc_p.font.size = Pt(12)
            desc_p.font.color.rgb = DESIGN.text_dark
            desc_p.space_after = Pt(12)
```

**Animations and Transitions (PptxGenJS)**:

```typescript
function addAnimatedSlide(pptx: PptxGenJS, title: string): void {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.addText(title, { placeholder: "title" });

  // Add slide transition
  slide.transition = {
    type: "fade",
    speed: 1.0,  // seconds
  };

  // Animate text elements
  const points = ["First point", "Second point", "Third point"];
  points.forEach((point, idx) => {
    slide.addText(point, {
      x: 1.0,
      y: 1.5 + idx * 0.8,
      w: 11.0,
      h: 0.6,
      fontSize: 18,
      color: "333333",
      bullet: { type: "bullet" },
    });
  });

  // Note: PptxGenJS supports slide transitions but has limited
  // shape-level animation support. For complex animations,
  // use a template-based approach (see Step 7).
}
```

### Step 7: Template-Based Generation

Template-based generation loads an existing .pptx file (designed in PowerPoint or Google Slides) and populates it with dynamic data. This approach separates design from code and is ideal for branded report generation.

**Loading and Inspecting a Template** (python-pptx):

```python
from pptx import Presentation
from pptx.util import Inches


def inspect_template(template_path: str) -> dict:
    """Inspect a template to discover its layouts and placeholders.

    Run this first when working with a new template to understand
    which placeholder indices and names are available.
    """
    prs = Presentation(template_path)
    template_info = {
        "slide_width": str(prs.slide_width),
        "slide_height": str(prs.slide_height),
        "slide_count": len(prs.slides),
        "layouts": [],
    }

    for layout_idx, layout in enumerate(prs.slide_layouts):
        layout_info = {
            "index": layout_idx,
            "name": layout.name,
            "placeholders": [],
        }
        for ph in layout.placeholders:
            layout_info["placeholders"].append({
                "idx": ph.placeholder_format.idx,
                "name": ph.name,
                "type": str(ph.placeholder_format.type),
                "left": str(ph.left),
                "top": str(ph.top),
                "width": str(ph.width),
                "height": str(ph.height),
            })
        template_info["layouts"].append(layout_info)

    return template_info


def load_template(template_path: str) -> Presentation:
    """Load an existing .pptx template for population."""
    return Presentation(template_path)
```

**Populating Template Placeholders**:

```python
from pptx import Presentation
from pptx.util import Pt


def populate_template_slide(
    prs: Presentation,
    layout_index: int,
    placeholder_data: dict[int, str],
) -> None:
    """Add a new slide from a template layout and fill its placeholders.

    Args:
        prs: Presentation loaded from template.
        layout_index: Index of the slide layout to use.
        placeholder_data: Mapping of placeholder index to text content.
    """
    layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(layout)

    for ph_idx, text in placeholder_data.items():
        if ph_idx in [ph.placeholder_format.idx for ph in slide.placeholders]:
            slide.placeholders[ph_idx].text = text


def populate_with_formatting(
    prs: Presentation,
    layout_index: int,
    placeholder_content: dict[int, list[dict]],
) -> None:
    """Populate placeholders with formatted text runs.

    Each entry in placeholder_content maps a placeholder index to a list of
    run descriptors: {"text": str, "bold": bool, "size": int, "color": str}.
    """
    layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(layout)

    for ph_idx, runs in placeholder_content.items():
        if ph_idx not in [ph.placeholder_format.idx for ph in slide.placeholders]:
            continue

        text_frame = slide.placeholders[ph_idx].text_frame
        text_frame.clear()

        for run_idx, run_data in enumerate(runs):
            if run_idx == 0:
                paragraph = text_frame.paragraphs[0]
            else:
                paragraph = text_frame.add_paragraph()

            run = paragraph.add_run()
            run.text = run_data["text"]
            run.font.size = Pt(run_data.get("size", 14))
            run.font.bold = run_data.get("bold", False)
            if "color" in run_data:
                from pptx.dml.color import RGBColor
                run.font.color.rgb = RGBColor.from_string(run_data["color"])
```

**Batch Generation from Data (Mail Merge Pattern)**:

```python
from pathlib import Path
from pptx import Presentation
import json


def batch_generate_decks(
    template_path: str,
    data_records: list[dict],
    output_dir: str,
    filename_field: str = "name",
) -> list[Path]:
    """Generate one presentation per data record using a shared template.

    This implements a mail merge pattern where each record produces
    a complete deck with its own data.

    Args:
        template_path: Path to the .pptx template.
        data_records: List of dicts, each containing fields for one deck.
        output_dir: Directory to write generated files.
        filename_field: Key in each record to use for the output filename.

    Returns:
        List of paths to generated files.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    generated_files: list[Path] = []

    for record in data_records:
        prs = Presentation(template_path)

        # Remove template example slides (keep only layouts)
        while len(prs.slides) > 0:
            rId = prs.slides._sldIdLst[0].get("r:id")
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[0]

        # Build slides from record data
        _build_deck_from_record(prs, record)

        # Save with sanitized filename
        safe_name = "".join(
            c if c.isalnum() or c in "-_ " else "" for c in record.get(filename_field, "output")
        ).strip()
        file_path = output / f"{safe_name}.pptx"
        prs.save(str(file_path))
        generated_files.append(file_path)

    return generated_files


def _build_deck_from_record(prs: Presentation, record: dict) -> None:
    """Build slides for a single record. Customize per template structure."""
    # Title slide (layout 0)
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.placeholders[0].text = record.get("title", "Untitled")
    slide.placeholders[1].text = record.get("subtitle", "")

    # Content slides (layout 1)
    for section in record.get("sections", []):
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.placeholders[0].text = section.get("heading", "")
        slide.placeholders[1].text = section.get("body", "")
```

**Data-Driven Generation from JSON**:

```python
from pathlib import Path
from pptx import Presentation
import json


def generate_from_json(
    json_path: str,
    template_path: str | None = None,
    output_path: str = "output.pptx",
) -> Path:
    """Generate a presentation from a JSON specification.

    JSON schema:
    {
      "metadata": {"title": str, "author": str},
      "theme": {"primary_color": str, "font": str},
      "slides": [
        {
          "type": "title|content|two_column|chart|table|image",
          "title": str,
          "content": {...type-specific fields...}
        }
      ]
    }
    """
    with open(json_path) as f:
        spec = json.load(f)

    prs = Presentation(template_path) if template_path else Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for slide_spec in spec.get("slides", []):
        slide_type = slide_spec.get("type", "content")

        if slide_type == "title":
            add_title_slide(
                prs,
                slide_spec.get("title", ""),
                slide_spec.get("content", {}).get("subtitle", ""),
            )
        elif slide_type == "content":
            add_content_slide(
                prs,
                slide_spec.get("title", ""),
                slide_spec.get("content", {}).get("body", ""),
                slide_spec.get("content", {}).get("bullets", []),
            )
        elif slide_type == "two_column":
            content = slide_spec.get("content", {})
            add_two_column_slide(
                prs,
                slide_spec.get("title", ""),
                content.get("left_title", ""),
                content.get("left_points", []),
                content.get("right_title", ""),
                content.get("right_points", []),
            )
        elif slide_type == "chart":
            content = slide_spec.get("content", {})
            chart_type = content.get("chart_type", "bar")
            if chart_type == "bar":
                add_bar_chart_slide(
                    prs,
                    slide_spec.get("title", ""),
                    content.get("categories", []),
                    content.get("series", {}),
                )
            elif chart_type == "pie":
                add_pie_chart_slide(
                    prs,
                    slide_spec.get("title", ""),
                    content.get("categories", []),
                    content.get("values", []),
                )
        elif slide_type == "table":
            content = slide_spec.get("content", {})
            add_table_slide(
                prs,
                slide_spec.get("title", ""),
                content.get("headers", []),
                content.get("rows", []),
            )

    output = Path(output_path)
    prs.save(str(output))
    return output
```

**Example JSON Specification**:

```json
{
  "metadata": {
    "title": "Q4 Performance Report",
    "author": "Analytics Team"
  },
  "slides": [
    {
      "type": "title",
      "title": "Q4 2025 Performance Report",
      "content": { "subtitle": "Analytics Team | January 2026" }
    },
    {
      "type": "content",
      "title": "Executive Summary",
      "content": {
        "bullets": [
          "Revenue grew 23% year-over-year to $4.2M",
          "Customer acquisition cost decreased by 15%",
          "Net promoter score improved from 42 to 58",
          "Three new enterprise clients onboarded"
        ]
      }
    },
    {
      "type": "chart",
      "title": "Revenue by Quarter",
      "content": {
        "chart_type": "bar",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {
          "2024": [2800000, 3100000, 3400000, 3600000],
          "2025": [3200000, 3500000, 3900000, 4200000]
        }
      }
    },
    {
      "type": "table",
      "title": "Regional Performance",
      "content": {
        "headers": ["Region", "Revenue", "Growth", "Clients"],
        "rows": [
          ["North America", "$2.1M", "+18%", "45"],
          ["Europe", "$1.2M", "+28%", "32"],
          ["Asia Pacific", "$0.9M", "+35%", "21"]
        ]
      }
    }
  ]
}
```

### Step 8: Testing and Quality Assurance

Automated presentation generation requires validation at multiple levels: structural correctness, content accuracy, visual consistency, and file integrity.

**Slide Count and Structure Verification**:

```python
from pptx import Presentation
from pathlib import Path


def verify_presentation_structure(
    pptx_path: str,
    expected_slide_count: int | None = None,
    expected_titles: list[str] | None = None,
) -> dict:
    """Verify the structural integrity of a generated presentation.

    Returns a dict with verification results and any issues found.
    """
    prs = Presentation(pptx_path)
    issues: list[str] = []
    results = {
        "file_path": pptx_path,
        "file_size_bytes": Path(pptx_path).stat().st_size,
        "slide_count": len(prs.slides),
        "issues": issues,
    }

    # Verify slide count
    if expected_slide_count is not None and len(prs.slides) != expected_slide_count:
        issues.append(
            f"Expected {expected_slide_count} slides, got {len(prs.slides)}"
        )

    # Verify slide titles
    actual_titles = []
    for idx, slide in enumerate(prs.slides):
        title_shape = slide.shapes.title
        title_text = title_shape.text if title_shape else ""
        actual_titles.append(title_text)

        if not title_text:
            issues.append(f"Slide {idx + 1} has no title")

    results["titles"] = actual_titles

    if expected_titles:
        for idx, expected in enumerate(expected_titles):
            if idx >= len(actual_titles):
                issues.append(f"Missing slide {idx + 1}: expected title '{expected}'")
            elif actual_titles[idx] != expected:
                issues.append(
                    f"Slide {idx + 1} title mismatch: "
                    f"expected '{expected}', got '{actual_titles[idx]}'"
                )

    results["valid"] = len(issues) == 0
    return results
```

**Content Extraction for Assertions**:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def extract_all_text(pptx_path: str) -> list[dict]:
    """Extract all text content from every slide for validation.

    Returns a list of dicts, one per slide, with all text content.
    """
    prs = Presentation(pptx_path)
    slides_content = []

    for slide_idx, slide in enumerate(prs.slides):
        slide_data = {
            "slide_number": slide_idx + 1,
            "title": "",
            "text_blocks": [],
            "tables": [],
            "notes": "",
        }

        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if shape == slide.shapes.title:
                    slide_data["title"] = text
                elif text:
                    slide_data["text_blocks"].append(text)

            if shape.has_table:
                table_data = []
                for row in shape.table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                slide_data["tables"].append(table_data)

        # Extract speaker notes
        if slide.has_notes_slide:
            notes_frame = slide.notes_slide.notes_text_frame
            slide_data["notes"] = notes_frame.text.strip()

        slides_content.append(slide_data)

    return slides_content


def extract_images(pptx_path: str) -> list[dict]:
    """Extract image metadata from the presentation."""
    prs = Presentation(pptx_path)
    images = []

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                images.append({
                    "slide_number": slide_idx + 1,
                    "name": shape.name,
                    "width": shape.width,
                    "height": shape.height,
                    "content_type": shape.image.content_type,
                    "size_bytes": len(shape.image.blob),
                })

    return images
```

**Pytest Test Suite**:

```python
import pytest
from pathlib import Path
from pptx import Presentation

# Assume your generator module is importable
# from my_generator import generate_report_deck


@pytest.fixture
def sample_presentation(tmp_path: Path) -> Path:
    """Generate a sample presentation for testing."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Add test slides
    add_title_slide(prs, "Test Report", "Generated by pytest")
    add_content_slide(prs, "Summary", "", ["Point 1", "Point 2"])
    add_table_slide(prs, "Data", ["Col A", "Col B"], [["1", "2"], ["3", "4"]])

    output = tmp_path / "test_output.pptx"
    prs.save(str(output))
    return output


class TestPresentationStructure:
    """Tests for presentation structural correctness."""

    def test_slide_count(self, sample_presentation: Path) -> None:
        result = verify_presentation_structure(
            str(sample_presentation), expected_slide_count=3,
        )
        assert result["valid"], f"Issues: {result['issues']}"

    def test_slide_titles_present(self, sample_presentation: Path) -> None:
        result = verify_presentation_structure(str(sample_presentation))
        assert all(title for title in result["titles"]), "Some slides missing titles"

    def test_expected_titles(self, sample_presentation: Path) -> None:
        result = verify_presentation_structure(
            str(sample_presentation),
            expected_titles=["Test Report", "Summary", "Data"],
        )
        assert result["valid"], f"Title mismatches: {result['issues']}"


class TestContentExtraction:
    """Tests for content accuracy in generated slides."""

    def test_bullet_points_present(self, sample_presentation: Path) -> None:
        content = extract_all_text(str(sample_presentation))
        summary_slide = content[1]  # Second slide
        all_text = " ".join(summary_slide["text_blocks"])
        assert "Point 1" in all_text
        assert "Point 2" in all_text

    def test_table_data_correct(self, sample_presentation: Path) -> None:
        content = extract_all_text(str(sample_presentation))
        data_slide = content[2]  # Third slide
        assert len(data_slide["tables"]) == 1
        table = data_slide["tables"][0]
        assert table[0] == ["Col A", "Col B"]  # Header row
        assert table[1] == ["1", "2"]  # First data row


class TestFileIntegrity:
    """Tests for file-level quality checks."""

    def test_file_not_empty(self, sample_presentation: Path) -> None:
        assert sample_presentation.stat().st_size > 0

    def test_file_opens_without_error(self, sample_presentation: Path) -> None:
        prs = Presentation(str(sample_presentation))
        assert prs is not None

    def test_file_size_reasonable(self, sample_presentation: Path) -> None:
        size_mb = sample_presentation.stat().st_size / (1024 * 1024)
        assert size_mb < 50, f"File too large: {size_mb:.1f} MB"

    @pytest.mark.parametrize("max_size_mb", [10, 25, 50])
    def test_file_size_thresholds(
        self, sample_presentation: Path, max_size_mb: int,
    ) -> None:
        size_mb = sample_presentation.stat().st_size / (1024 * 1024)
        assert size_mb < max_size_mb
```

**File Size Optimization**:

```python
from pptx import Presentation
from pathlib import Path
from PIL import Image
import io


def optimize_images_in_presentation(
    input_path: str,
    output_path: str,
    max_dimension: int = 1920,
    jpeg_quality: int = 85,
) -> dict:
    """Optimize images in a presentation to reduce file size.

    Resizes images larger than max_dimension and recompresses JPEGs.
    Returns optimization statistics.
    """
    prs = Presentation(input_path)
    original_size = Path(input_path).stat().st_size
    images_optimized = 0

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.shape_type != MSO_SHAPE_TYPE.PICTURE:
                continue

            image_blob = shape.image.blob
            content_type = shape.image.content_type

            if content_type not in ("image/jpeg", "image/png"):
                continue

            img = Image.open(io.BytesIO(image_blob))
            w, h = img.size

            # Skip if already small enough
            if max(w, h) <= max_dimension:
                continue

            # Resize maintaining aspect ratio
            if w > h:
                new_w = max_dimension
                new_h = int(h * max_dimension / w)
            else:
                new_h = max_dimension
                new_w = int(w * max_dimension / h)

            img = img.resize((new_w, new_h), Image.LANCZOS)

            # Recompress
            buffer = io.BytesIO()
            if content_type == "image/jpeg":
                img.save(buffer, format="JPEG", quality=jpeg_quality, optimize=True)
            else:
                img.save(buffer, format="PNG", optimize=True)

            # Replace the image blob in the presentation
            shape.image._blob = buffer.getvalue()
            images_optimized += 1

    prs.save(output_path)
    new_size = Path(output_path).stat().st_size

    return {
        "original_size_bytes": original_size,
        "optimized_size_bytes": new_size,
        "reduction_percent": round((1 - new_size / original_size) * 100, 1),
        "images_optimized": images_optimized,
    }
```

**Visual Validation (Convert to Images for Comparison)**:

```python
import subprocess
from pathlib import Path


def export_slides_as_images(
    pptx_path: str,
    output_dir: str,
    format: str = "png",
) -> list[Path]:
    """Export each slide as an image using LibreOffice for visual validation.

    Requires LibreOffice installed and accessible via command line.
    Useful for visual regression testing in CI pipelines.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    # Convert PPTX to individual images via LibreOffice
    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to", format,
            "--outdir", str(output),
            pptx_path,
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed: {result.stderr}"
        )

    # Collect generated images
    return sorted(output.glob(f"*.{format}"))
```

**Key Quality Assurance Principles**:

- Always verify slide count matches the expected number of data items
- Extract and assert text content rather than relying on visual inspection
- Test table dimensions (row count, column count) match input data
- Verify chart data by re-reading the chart XML when possible
- Keep file sizes under control by optimizing images before embedding
- Use LibreOffice headless conversion for visual regression testing in CI
- Test with both minimal and maximal data to catch overflow and layout issues
- Validate that speaker notes are populated when expected
- Check that hyperlinks resolve to valid URLs
- Run generation tests with `tmp_path` fixtures to avoid polluting the working directory
