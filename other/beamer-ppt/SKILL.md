---
name: beamer-ppt
description: Create Beamer-style academic PPTX presentations using python-pptx. Produces publication-quality .pptx files with navy-blue Metropolis theme (16:9, frame title bars, progress bar) for conference talks, job market presentations, and seminar slides. Called by /present command.
---

# Beamer-ppt-Creator

## Purpose

This skill generates professional academic **PPTX** presentations that faithfully replicate the visual style of LaTeX Beamer (Metropolis theme). Output is a `.pptx` file that can be opened, edited, and presented directly in PowerPoint or LibreOffice Impress — no LaTeX installation required.

## When to Use

- Called by `/present` command to produce the final `slides/slides.pptx`
- Preparing conference, seminar, or job market slides
- Converting a completed economics paper into a slide deck

## Design Principles

- **One idea per slide** — split if content overflows
- **Minimum 20pt** for body text; 24pt for frame titles
- **Consistent palette** — navy blue primary, one accent color only
- **Figures over tables** — embed PNG images at ≥ 200 DPI
- **Last slide = Takeaways**, never "Questions?"

---

## Implementation

This skill executes Python code using `python-pptx`. Always install dependencies first:

```bash
pip install python-pptx pdf2image --break-system-packages
apt-get install -y poppler-utils 2>/dev/null || true
```

### Color Palettes by Theme

| Theme | Title Bar `bg` | Accent | Slide `bg` |
|-------|---------------|--------|-----------|
| **A. Metropolis** (default) | `RGB(0, 35, 82)` navy | `RGB(180, 30, 30)` red | `RGB(245, 245, 245)` light gray |
| **B. Minimal** (job market) | `RGB(0, 35, 82)` navy | `RGB(0, 35, 82)` navy | `RGB(255, 255, 255)` white |
| **C. Madrid** (traditional) | `RGB(31, 73, 125)` dark blue | `RGB(189, 152, 44)` gold | `RGB(255, 255, 255)` white |

### Core Helper Functions

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

# ── Presentation setup ───────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)   # 16:9 widescreen (Beamer aspectratio=169)
prs.slide_height = Inches(7.5)

# ── Color definitions (Metropolis theme) ─────────────────────────
NAVY  = RGBColor(0, 35, 82)
RED   = RGBColor(180, 30, 30)
LGRAY = RGBColor(245, 245, 245)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(30, 30, 30)
MGRAY = RGBColor(100, 100, 100)


def add_bg(slide, prs, color):
    """Full-slide background rectangle."""
    shape = slide.shapes.add_shape(
        1, 0, 0, prs.slide_width, prs.slide_height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_frame_title(slide, prs, text, bg=NAVY, fg=WHITE):
    """Navy title bar (1.1 in tall) — mimics Beamer \\frametitle."""
    bar = slide.shapes.add_shape(
        1, 0, 0, prs.slide_width, Inches(1.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = bg
    bar.line.fill.background()
    tf = bar.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.3)
    tf.margin_top  = Inches(0.22)
    p = tf.paragraphs[0]
    p.text = text
    p.font.bold  = True
    p.font.size  = Pt(24)
    p.font.color.rgb = fg
    p.alignment  = PP_ALIGN.LEFT


def add_progress_bar(slide, prs, current, total, color=NAVY):
    """Metropolis-style thin progress bar at bottom."""
    h   = Inches(0.055)
    top = prs.slide_height - h
    # Gray track
    track = slide.shapes.add_shape(
        1, 0, top, prs.slide_width, h)
    track.fill.solid()
    track.fill.fore_color.rgb = RGBColor(200, 200, 200)
    track.line.fill.background()
    # Filled portion
    filled_w = int(prs.slide_width * current / max(total, 1))
    if filled_w > 0:
        bar = slide.shapes.add_shape(1, 0, top, filled_w, h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()


def add_speaker_notes(slide, notes_text):
    """Add speaker notes to a slide."""
    slide.notes_slide.notes_text_frame.text = notes_text
```

### Slide Factory Functions

```python
# ── 1. Title slide ───────────────────────────────────────────────
def make_title_slide(prs, title, subtitle, author, institute, date_line):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs, NAVY)

    def _tb(left, top, w, h):
        tb = slide.shapes.add_textbox(
            Inches(left), Inches(top), Inches(w), Inches(h))
        tb.text_frame.word_wrap = True
        return tb.text_frame

    # Paper title
    tf = _tb(1, 1.7, 11.33, 2.0)
    p = tf.paragraphs[0]
    p.text = title; p.font.bold = True
    p.font.size = Pt(34); p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle; p2.font.size = Pt(20)
        p2.font.color.rgb = LGRAY; p2.alignment = PP_ALIGN.CENTER

    # Author + institute
    tf2 = _tb(1, 4.3, 11.33, 1.4)
    p3 = tf2.paragraphs[0]
    p3.text = author; p3.font.size = Pt(18)
    p3.font.color.rgb = WHITE; p3.alignment = PP_ALIGN.CENTER
    p4 = tf2.add_paragraph()
    p4.text = institute; p4.font.size = Pt(15)
    p4.font.color.rgb = LGRAY; p4.alignment = PP_ALIGN.CENTER

    # Date / conference
    tf3 = _tb(1, 6.1, 11.33, 0.8)
    p5 = tf3.paragraphs[0]
    p5.text = date_line; p5.font.size = Pt(13)
    p5.font.color.rgb = LGRAY; p5.alignment = PP_ALIGN.CENTER
    return slide


# ── 2. Content slide (bullet list) ──────────────────────────────
def make_content_slide(prs, title, bullets,
                       current=None, total=None, bg=LGRAY):
    """
    bullets: list of (indent_level, text) tuples.
    indent_level 0 = top-level bullet, 1 = sub-bullet.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs, bg)
    add_frame_title(slide, prs, title)

    tb = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.3), Inches(12.33), Inches(5.8))
    tf = tb.text_frame; tf.word_wrap = True
    for i, (lvl, text) in enumerate(bullets):
        p = tf.paragraphs[i] if i == 0 else tf.add_paragraph()
        p.text = text; p.level = lvl
        p.font.size = Pt(20 if lvl == 0 else 17)
        p.font.color.rgb = BLACK
        p.space_before = Pt(8 if lvl == 0 else 4)

    if current and total:
        add_progress_bar(slide, prs, current, total)
    return slide


# ── 3. Figure slide ──────────────────────────────────────────────
def make_figure_slide(prs, title, img_path, caption="",
                      current=None, total=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs, LGRAY)
    add_frame_title(slide, prs, title)

    slide.shapes.add_picture(
        img_path,
        left=Inches(1.17), top=Inches(1.3),
        width=Inches(11.0), height=Inches(5.2))

    if caption:
        cap = slide.shapes.add_textbox(
            Inches(0.5), Inches(6.6), Inches(12.33), Inches(0.7))
        cap.text_frame.paragraphs[0].text = caption
        cap.text_frame.paragraphs[0].font.size = Pt(11)
        cap.text_frame.paragraphs[0].font.color.rgb = MGRAY

    if current and total:
        add_progress_bar(slide, prs, current, total)
    return slide


# ── 4. Regression table slide ────────────────────────────────────
def make_table_slide(prs, title, headers, rows,
                     footnote="", highlight_last_col=True,
                     current=None, total=None):
    """
    headers: list of str (first col is row label).
    rows:    list of lists of str.
    Last column is treated as the preferred specification (bolded).
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs, LGRAY)
    add_frame_title(slide, prs, title)

    nc = len(headers); nr = len(rows) + 1
    tbl = slide.shapes.add_table(
        nr, nc,
        Inches(0.5), Inches(1.4),
        Inches(12.33), Inches(4.5)).table

    # Header row — navy background, white bold text
    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = h
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.size = Pt(14)
        c.text_frame.paragraphs[0].font.color.rgb = WHITE
        c.fill.solid(); c.fill.fore_color.rgb = NAVY

    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            c.text = str(val)
            c.text_frame.paragraphs[0].font.size = Pt(13)
            if highlight_last_col and j == nc - 1:
                c.text_frame.paragraphs[0].font.bold = True

    if footnote:
        fn = slide.shapes.add_textbox(
            Inches(0.5), Inches(6.0), Inches(12.33), Inches(1.2))
        fn.text_frame.paragraphs[0].text = footnote
        fn.text_frame.paragraphs[0].font.size = Pt(10)
        fn.text_frame.paragraphs[0].font.color.rgb = MGRAY

    if current and total:
        add_progress_bar(slide, prs, current, total)
    return slide


# ── 5. Two-column slide ──────────────────────────────────────────
def make_two_col_slide(prs, title, left_bullets, right_bullets,
                       current=None, total=None):
    """Two-column layout (e.g. Robustness slide)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs, LGRAY)
    add_frame_title(slide, prs, title)

    for col_bullets, left_offset in [(left_bullets, 0.4),
                                      (right_bullets, 6.9)]:
        tb = slide.shapes.add_textbox(
            Inches(left_offset), Inches(1.35),
            Inches(5.8), Inches(5.8))
        tf = tb.text_frame; tf.word_wrap = True
        for i, (lvl, text) in enumerate(col_bullets):
            p = tf.paragraphs[i] if i == 0 else tf.add_paragraph()
            p.text = text; p.level = lvl
            p.font.size = Pt(18 if lvl == 0 else 15)
            p.font.color.rgb = BLACK
            p.space_before = Pt(6 if lvl == 0 else 3)

    if current and total:
        add_progress_bar(slide, prs, current, total)
    return slide
```

### PDF → PNG Conversion (for figures from /plot)

```python
import subprocess

def pdf_to_png(pdf_path, dpi=200):
    """Convert PDF figure to PNG for embedding in PPTX."""
    png_base = pdf_path.replace(".pdf", "")
    try:
        subprocess.run(
            ["pdftoppm", "-r", str(dpi), "-png", "-singlefile",
             pdf_path, png_base],
            check=True, capture_output=True)
        return png_base + ".png"
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: pdf2image
        from pdf2image import convert_from_path
        imgs = convert_from_path(pdf_path, dpi=dpi)
        png_path = png_base + ".png"
        imgs[0].save(png_path, "PNG")
        return png_path
```

### Save, Export PDF & Verify

```python
import subprocess

def save_and_verify(prs, output_path, export_pdf=True):
    """Save PPTX, optionally export PDF via LibreOffice, then verify."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)

    # ── Verify PPTX ──────────────────────────────────────────────
    check = Presentation(output_path)
    n = len(check.slides)
    assert n > 0, "PPTX is empty — check slide generation."
    print(f"✅ PPTX saved : {output_path}")
    print(f"   {n} slides | {os.path.getsize(output_path) // 1024} KB")

    # ── Export PDF ───────────────────────────────────────────────
    pdf_path = None
    if export_pdf:
        pdf_path = _pptx_to_pdf(output_path)

    return output_path, pdf_path


def _pptx_to_pdf(pptx_path):
    """Convert PPTX → PDF using LibreOffice headless."""
    out_dir = os.path.dirname(pptx_path)
    try:
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf",
             "--outdir", out_dir, pptx_path],
            capture_output=True, text=True, timeout=120
        )
        pdf_path = pptx_path.replace(".pptx", ".pdf")
        if os.path.exists(pdf_path):
            print(f"✅ PDF exported: {pdf_path}")
            print(f"   {os.path.getsize(pdf_path) // 1024} KB")
            return pdf_path
        else:
            print(f"⚠️  LibreOffice conversion failed: {result.stderr.strip()}")
            print("   → Open slides.pptx in PowerPoint and export manually.")
            return None
    except FileNotFoundError:
        print("⚠️  LibreOffice not found. Install with:")
        print("   apt-get install -y libreoffice   # Ubuntu/Debian")
        print("   brew install --cask libreoffice  # macOS")
        print("   → You can also export PDF from PowerPoint / LibreOffice Impress.")
        return None
    except subprocess.TimeoutExpired:
        print("⚠️  LibreOffice timed out. Try running manually:")
        print(f"   libreoffice --headless --convert-to pdf {pptx_path}")
        return None
```

---

## Slide Structure by Presentation Type

| Slide Section | 15-min conf (≤15) | 45-min seminar (≤30) | Job market (≤20) |
|---------------|:-----------------:|:--------------------:|:----------------:|
| Title | 1 | 1 | 1 |
| Motivation | 1–2 | 2–3 | 2–3 |
| This Paper | 1 | 1 | 1 |
| Related Lit | — | 1–2 | 1–2 |
| Data | 1 | 2 | 2 |
| Identification | 2 | 3–4 | 3 |
| Main Results | 3 | 5–7 | 4–5 |
| Robustness | 1 | 2–3 | 2 |
| Heterogeneity | — | 2–3 | 1–2 |
| Takeaways | 1 | 1 | 1 |

---

## Best Practices

1. **One message per slide** — split if content overflows
2. **Use figures over tables** — embed PNG at ≥ 200 DPI
3. **Bold the preferred specification** column in regression tables
4. **Add speaker notes** to every key slide via `add_speaker_notes()`
5. **Prepare appendix slides** for anticipated Q&A
6. **Timing**: budget 1.5 min/slide; final slide must be Takeaways

## Common Pitfalls

- ❌ Too much text (max 5 bullets per slide, max 10 words per bullet)
- ❌ Tables with more than 4 columns
- ❌ Ending with "Thank you / Questions?" — use Takeaways instead
- ❌ Embedding low-resolution images (< 150 DPI looks blurry on projectors)
- ❌ Skipping the "This Paper" preview slide
