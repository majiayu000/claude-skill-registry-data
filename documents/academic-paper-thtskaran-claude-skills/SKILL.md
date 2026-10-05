---
name: academic-paper
description: >
  Write, format, and export professional academic research papers as publication-ready PDFs
  using reportlab. Use this skill whenever the user wants to write a research paper, preprint,
  white paper, literature review, position paper, or technical report — whether from scratch,
  from notes, or from an existing draft. Also trigger when the user asks to convert markdown/text
  into an academic PDF, needs SSRN/arXiv submission preparation, or wants tables, figures, and
  references formatted for publication. Trigger on: "write a paper", "preprint", "format as
  research paper", "turn my notes/draft into a paper", "academic PDF", "SSRN", "arXiv",
  "research report", "literature synthesis", "position paper", "white paper", "publish my research".
  Even if the user just provides a markdown file and says "make this a PDF", use this skill
  if the content is scholarly/research-oriented.
---

# Academic Paper Skill

Generate publication-ready academic research papers as professionally formatted PDFs.
This skill covers the full pipeline: gathering inputs → writing/rewriting → figure creation
→ PDF formatting with reportlab → submission preparation for SSRN/arXiv.

---

## Workflow Decision Tree

When the user triggers this skill, figure out where they are:

```
User has...             → Start at...
─────────────────────────────────────────────
A topic/idea only       → Stage 1 (Gather) → full pipeline
Bullet points/notes     → Stage 2 (Structure) → write → format
A markdown/text draft   → Stage 3 (Write/Rewrite) → format
A finished draft        → Stage 5 (Format as PDF)
A PDF, needs submission → Stage 6 (Submission Prep)
```

Always ask what they have and what they need. Don't assume full pipeline.

---

## Stage 1: Gather Inputs

Collect these before ANY writing:

**Required:**
- Author full name, email, affiliation (company name or "Independent Researcher" — both valid)
- Paper type: preprint, position paper, empirical study, literature synthesis, technical report
- Existing content: draft file, notes, or topic description
- Target venue: SSRN, arXiv, specific journal, or general

**Ask about:**
- Do they have citations/references already, or do we need to find them?
- Do they have figures/diagrams, or should we create them?
- Any page limits or formatting constraints from the venue?
- Any specific sections they want or don't want?

**If user provides a markdown/text draft:**
1. Read the entire draft before doing anything
2. Count all citations — you'll need to verify none get lost during rewriting
3. Map the section structure
4. Identify: What's the thesis? What evidence supports it? What's missing?

---

## Stage 2: Structure

### Standard Paper Architecture

```
Title + Abstract (≤300 words) + Keywords (8-12)
1. Introduction         → Hook → Gap → Thesis → Contribution list
2. Background/Related   → Only what the reader needs; argue, don't survey
3-5. Core sections      → The actual contribution (varies by paper type)
6. Discussion           → Implications, limitations, future work
7. Conclusion           → Mirror intro, restate contributions concretely
References              → Hanging indent, consistent format
Appendices (optional)   → Supporting tables, proofs, supplementary data
```

### Before Writing, Map the Argument

Do this explicitly — it prevents structural drift:

- **Thesis**: One sentence. The paper's central claim.
- **Evidence chain**: What supports it? Arrange in logical order.
- **Counterarguments**: What would a skeptic say? Plan where to address.
- **Novel contribution**: What is genuinely NEW here?
- **Reader**: Who is reading this, and what do they already know?

---

## Stage 3: Write or Rewrite

### Writing Principles

**1. Enter the reader's world first.**
Open with what the audience already knows and cares about — a concrete scenario, a surprising
finding, a known problem. Then introduce your contribution. Never lead with your own framework.

**2. Every section ARGUES, not just DESCRIBES.**
Bad section heading: "Related Work." Good: "Three Independently Studied Phenomena That Interact
as a System." Each section should advance a claim, not just organize information.

**3. Concrete before abstract.**
Give a specific example or scenario, then generalize. The reader should visualize before you name.

**4. Every data point gets a "so what" sentence.**
Never drop a statistic bare. After every cited finding, one sentence interpreting what it means
for YOUR argument. Example: "Retrieval drops to 29.8% at 32K tokens (Modarressi et al., 2025).
A user asking 'remember what I said about feeling worthless?' is making exactly this kind of
semantic retrieval request — and the model is likely to fail."

**5. Transitions advance the argument.**
Kill "Additionally", "Furthermore", "Moreover" as paragraph openers. Each transition should
show logical progression: "This creates a problem that..." / "That finding has a direct
corollary..." / "The mechanism just described operates differently when..."

**6. Introduction and conclusion bookend.**
Open with a scenario → return to it in the conclusion with resolution.

**7. Write for the skeptical expert.**
Smart, busy, looking for reasons to stop reading. Front-load importance. Cut ruthlessly.

### Rewriting an Existing Draft — THE RULES

These are non-negotiable when polishing someone's draft:

1. **Preserve ALL citations verbatim.** Never change, remove, or invent citations. After
   rewriting, diff-check: count refs in original vs. output. Must match.
2. **Preserve ALL data points exactly.** Numbers, percentages, dates — untouched.
3. **Preserve the author's core argument.** Improve the vehicle, don't change the destination.
4. **Convert bullet/numbered lists to flowing prose** in the body. Lists only in appendices.
5. **Strengthen the opening** — add a narrative hook if missing.
6. **Add interpretive "so what" sentences** after key findings.
7. **Sharpen transitions** between paragraphs and sections.
8. **Trim redundancy.** If two sentences say the same thing, keep the stronger one.
9. **Check for orphan claims** — assertions without supporting evidence or citations.

---

## Stage 4: Figures

### Creating SVG Diagrams

For flowcharts, system diagrams, conceptual figures — build them as SVG:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 950"
     width="680" height="950" font-family="Georgia, 'Times New Roman', serif">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
    <filter id="shadow" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="1" dy="1" stdDeviation="2" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- ALWAYS include a white background rect -->
  <rect width="680" height="950" fill="white"/>

  <!-- Then your diagram elements... -->
</svg>
```

**Visual design rules:**
- ALWAYS set explicit white background — SVGs default to transparent which renders as BLACK in PDFs
- Muted professional palette:
  - Pink endpoints/warnings: `fill="#ffcdd2" stroke="#e57373"`
  - Blue processes: `fill="#c5cae9" stroke="#7986cb"`
  - Green outcomes: `fill="#c8e6c9" stroke="#66bb6a"`
  - Neutral steps: `fill="#fafafa" stroke="#aaa"` or `fill="#fff" stroke="#999"`
- Subtle drop shadows via SVG `<filter>` (not CSS)
- Arrow markers (`<marker>`) for flow direction
- Dashed strokes (`stroke-dasharray="8,5"`) for feedback loops
- Font: Georgia or Times New Roman, 11-13px
- Box labels: 3-6 words max. If longer, split across two `<text>` lines
- Rounded rects (`rx="4"`) look more professional than sharp corners
- Add annotations for loop labels using rotated text

**Converting SVG → high-res PNG for PDF embedding:**
```bash
pip install cairosvg --break-system-packages -q
```
```python
import cairosvg
cairosvg.svg2png(url='/home/claude/figure.svg', write_to='/home/claude/figure.png', scale=3)
```
Always 3× scale. This produces a crisp image even at print resolution.

### Handling User-Provided Images with Dark/Transparent Backgrounds

This is a common gotcha — transparent PNGs render with BLACK backgrounds in PDFs.

**Safe approach** — replace only exact-black pixels (preserves dark text):
```python
from PIL import Image
import numpy as np

img = Image.open('figure.png')
arr = np.array(img).copy()
mask = (arr[:,:,0] <= 2) & (arr[:,:,1] <= 2) & (arr[:,:,2] <= 2)
arr[mask] = [255, 255, 255]
Image.fromarray(arr).save('figure_white.png')
```

**NEVER use:**
- Flood-fill with high thresholds (destroys anti-aliased text)
- Blanket replacement of all dark pixels (destroys text strokes)
- `Image.convert('RGBA')` + alpha compositing if the image is already RGB with no alpha channel

The threshold ≤ 2 works because flat backgrounds use exact (0,0,0) or (1,1,1), while text
anti-aliasing uses slightly higher values (3-30+).

---

## Stage 5: Format as PDF with Reportlab

### Install Dependencies
```bash
pip install reportlab Pillow cairosvg --break-system-packages -q
```

### Architecture: Use BaseDocTemplate, Not SimpleDocTemplate

SimpleDocTemplate doesn't support different headers per page. Use BaseDocTemplate
with two PageTemplates: `first` (title page, no running header) and `later`
(running header with short title + date).

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate

PAGE_W, PAGE_H = letter
MARGIN = 1 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

doc = BaseDocTemplate(OUTPUT_PATH, pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=0.85*inch, bottomMargin=0.75*inch,
    title=PAPER_TITLE, author=AUTHOR_NAME)

frame = Frame(doc.leftMargin, doc.bottomMargin,
    CONTENT_W, PAGE_H - doc.topMargin - doc.bottomMargin, id='main')

doc.addPageTemplates([
    PageTemplate(id='first', frames=[frame], onPage=first_page_header),
    PageTemplate(id='later', frames=[frame], onPage=later_pages_header),
])
```

After the title block in the story, insert: `story.append(NextPageTemplate('later'))`

### Page Callbacks

```python
from reportlab.lib.colors import HexColor

LIGHT_GRAY_TEXT = HexColor("#999999")
RULE_COLOR = HexColor("#c5cae9")

def first_page_header(canvas, doc):
    """First page: centered page number only."""
    canvas.saveState()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(LIGHT_GRAY_TEXT)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch, str(canvas.getPageNumber()))
    canvas.restoreState()

def later_pages_header(canvas, doc):
    """Pages 2+: running header + page number."""
    canvas.saveState()
    pg = canvas.getPageNumber()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(LIGHT_GRAY_TEXT)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch, str(pg))
    canvas.setFont('Times-Italic', 7.5)
    canvas.drawString(MARGIN, PAGE_H - 0.6*inch, SHORT_TITLE)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.6*inch, f"Preprint — {DATE}")
    canvas.setStrokeColor(RULE_COLOR)
    canvas.setLineWidth(0.3)
    canvas.line(MARGIN, PAGE_H - 0.65*inch, PAGE_W - MARGIN, PAGE_H - 0.65*inch)
    canvas.restoreState()
```

### Style Definitions

Define ALL styles up front. Key styles needed:

| Style Name | Font | Size | Leading | Alignment | Purpose |
|---|---|---|---|---|---|
| PaperTitle | Times-Bold | 16pt | 20pt | CENTER | Main title |
| PrePrintNotice | Times-Italic | 8pt | 10pt | CENTER | "Preprint — Not Yet Peer-Reviewed" |
| AuthorName | Times-Bold | 11pt | 14pt | CENTER | Author name |
| AuthorAffil | Times-Roman | 9.5pt | 12pt | CENTER | Affiliation, email, date |
| AbstractHeading | Times-Bold | 10pt | 13pt | CENTER | "Abstract" label |
| AbstractBody | Times-Italic | 9.5pt | 13pt | JUSTIFY | Abstract text, 24pt L/R indent |
| Keywords | Times-Roman | 9pt | 12pt | JUSTIFY | Keywords line, 24pt L/R indent |
| SectionHeading | Times-Bold | 13pt | 16pt | LEFT | "1. Introduction" |
| SubsectionHeading | Times-Bold | 11pt | 14pt | LEFT | "2.1 Subsection" |
| SubsubHeading | Times-BoldItalic | 10.5pt | 13pt | LEFT | "2.1.1 Detail" |
| Body | Times-Roman | 10pt | 13.5pt | JUSTIFY | Main body text |
| FigCaption | Times-Roman | 9pt | 12pt | CENTER | Figure captions |
| TableNote | Times-Italic | 8.5pt | 11pt | LEFT | Table captions/notes |
| Equation | Times-Roman | 10pt | 14pt | CENTER | Displayed equations |
| Reference | Times-Roman | 8.5pt | 11pt | JUSTIFY | Reference entries |

Reference style needs hanging indent: `leftIndent=18, firstLineIndent=-18`

### Title Block Assembly

```python
story = []
story.append(Spacer(1, 0.1*inch))
story.append(p("Preprint — Not Yet Peer-Reviewed", 'PrePrintNotice'))
story.append(Spacer(1, 0.15*inch))
story.append(p(PAPER_TITLE, 'PaperTitle'))
story.append(Spacer(1, 0.15*inch))
story.append(p(AUTHOR_NAME, 'AuthorName'))
story.append(p(AUTHOR_AFFIL, 'AuthorAffil'))
story.append(p(AUTHOR_EMAIL, 'AuthorAffil'))
story.append(Spacer(1, 0.05*inch))
story.append(p(PAPER_DATE, 'AuthorAffil'))
story.append(Spacer(1, 0.2*inch))
story.append(hr())  # HRFlowable
story.append(p("Abstract", 'AbstractHeading'))
# Abstract paragraphs...
story.append(p("<b>Keywords:</b> keyword1, keyword2, ...", 'Keywords'))
story.append(hr())
story.append(NextPageTemplate('later'))
```

### Tables — THE #1 FORMATTING BUG

**ALWAYS wrap cell content in Paragraph objects.** Raw strings WILL overflow their columns
and overlap adjacent cells. This is guaranteed to happen with any cell longer than ~15 chars.

```python
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor, white

cell_style = ParagraphStyle('Cell', fontName='Times-Roman',
    fontSize=9, leading=12, alignment=TA_LEFT)
header_style = ParagraphStyle('CellH', fontName='Times-Bold',
    fontSize=9, leading=12, alignment=TA_LEFT)

# Build data as Paragraph objects
data = [
    [Paragraph(f'<b>{h}</b>', header_style) for h in headers],
]
for row in rows:
    data.append([Paragraph(str(cell), cell_style) for cell in row])

table = Table(data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor("#e8eaf6")),   # header bg
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.4, HexColor("#c5cae9")),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#fafafa")]),
]))
```

**Column width strategy**: Distribute `CONTENT_W` (6.5 inches) across columns. Give
wider columns to text-heavy cells. Example for a 3-column table with model names,
descriptions, and numbers: `[1.5*inch, 3.5*inch, 1.5*inch]`.

### Equations

reportlab CANNOT render LaTeX. Use these approaches:

```python
# Inline: use <sub> and <super> tags
Paragraph("R(n) ≈ R<sub>0</sub> · e<super>−α·n/n<sub>eff</sub></super>", eq_style)

# Unicode math symbols that work in Times-Roman:
# ≈ ≤ ≥ ∝ ∞ α β γ δ ε θ λ μ σ · × ± ∑ √ ∂ ∫ → ← ↔ ≠ ∈
# Em dash: \u2014   En dash: \u2013   Minus: \u2212   Multiply: \u00d7
```

If the paper needs complex multi-line equations (integrals, matrices, aligned systems),
tell the user: "For proper equation typesetting, I recommend converting to LaTeX and
compiling with pdflatex. reportlab is better for papers with minimal math."

### Figures

```python
from PIL import Image as PILImage
from reportlab.platypus import Image, Spacer

img = PILImage.open(img_path)
w_px, h_px = img.size
aspect = h_px / w_px

fig_w = 4.5 * inch
fig_h = fig_w * aspect
if fig_h > 7.0 * inch:        # cap to fit on one page
    fig_h = 7.0 * inch
    fig_w = fig_h / aspect

story.append(Spacer(1, 6))
story.append(Image(img_path, width=fig_w, height=fig_h, hAlign='CENTER'))
story.append(Paragraph("<b>Figure 1.</b> Caption text here.", fig_caption_style))
```

### Horizontal Rules

```python
from reportlab.platypus import HRFlowable

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR,
                      spaceBefore=8, spaceAfter=8)
```

### Building and Delivering

```python
doc.build(story)
print(f"PDF generated: {OUTPUT_PATH}")

# Copy to outputs and present
import shutil
shutil.copy(OUTPUT_PATH, '/mnt/user-data/outputs/paper-title.pdf')
# Then use present_files tool
```

---

## Stage 6: Submission Preparation

### SSRN (Zero Friction — Recommended for Independent Researchers)

**Required for submission form:**
1. **Title** — must match PDF title exactly
2. **Authors** — name, email, affiliation. No institutional email required.
3. **Abstract** — plain text only. Strip all markdown formatting (`**bold**` → bold text, etc.)
4. **Keywords** — 8-12 terms, comma-separated
5. **PDF upload** — the formatted paper
6. **eJournal classifications** — browse the tree and checkbox relevant ones
7. **Paper type** — select "Working Paper" for preprints
8. **Availability** — set to "Publicly Available" (CRITICAL: private papers don't appear in
   SSRN search or eJournal distributions)

**eJournal selection strategy:**
Select MULTIPLE classifications for cross-disciplinary visibility:
- One PRIMARY journal where the core contribution lives
- 2-3 SECONDARY journals based on who else should read this
- Think about the READER, not just the TOPIC

Example SSRN networks and journals:
- **CompSciRN**: Artificial Intelligence, Human-Computer Interaction, Cybersecurity
- **PsychRN**: Cognitive Psychology, Developmental Psychology
- **LawRN**: Science & Technology Law, Regulation of AI
- **HealthRN**: Mental Health, Public Health

**JEL codes** (optional but helps discoverability):
Common ones for AI papers: O33 (Tech Change), L86 (Info/Internet Services),
K32 (Environmental/Health/Safety Law), I31 (Wellbeing)

**Processing time**: Officially ≤3 business days. Realistically 2-5 days.
~30% of submissions get desk-rejected (not for quality — formatting/metadata issues).
Clean PDF + complete metadata = faster approval.

**SSRN retains no copyright.** Authors keep full rights. Non-exclusive revocable license only.

### arXiv

**Key requirements:**
- Endorsement required for first-time submitters in most categories
- Find endorsers among researchers you cite — cold-email with your SSRN preprint link
- Publish on SSRN first, pursue arXiv endorsement in parallel
- Submit PDF or LaTeX source (LaTeX preferred for proper math rendering)

**Relevant categories for AI/ML papers:**
- `cs.AI` — Artificial Intelligence
- `cs.CL` — Computation and Language (NLP/LLM papers)
- `cs.HC` — Human-Computer Interaction
- `cs.CY` — Computers and Society (safety, ethics, policy)
- `cs.LG` — Machine Learning

**Strategy for independent researchers:**
Publish SSRN first → get a DOI and download traction → use this to approach
arXiv endorsers. Having a live, citable preprint makes endorsement requests
more credible than cold-emailing with an unpublished manuscript.

### AI Disclosure Statement

All major publishers (Elsevier, Springer Nature, Wiley, Taylor & Francis, SAGE) permit
AI tools for editorial refinement. AI cannot be listed as author. Recommended wording:

> "The author used [Tool Name] ([Company]) for editorial refinement and prose revision
> of this manuscript. All research synthesis, analysis, argumentation, and conclusions
> are the author's own."

Place in an "Acknowledgments" section before References.

---

## Quality Checklist — Run Before Delivery

```
[ ] Title on PDF matches submission metadata exactly
[ ] Citation count: original draft refs == final PDF refs (diff-check if rewritten)
[ ] All data points (numbers, %, dates) unchanged from source
[ ] Tables: open PDF and visually inspect every table for text overflow
[ ] Figures: white backgrounds, captions present, readable at print size
[ ] Page numbers on every page
[ ] Running headers on pages 2+
[ ] References: consistent format, hanging indent, no broken entries
[ ] Abstract ≤ 300 words
[ ] Keywords present (8-12 terms)
[ ] No orphan headings (heading at page bottom, body on next page)
[ ] PDF metadata: title + author set in document properties
[ ] No "Amy AI", product names, or internal project refs (if paper is venue-agnostic)
```

---

## File Locations

| What | Where |
|---|---|
| Working directory | `/home/claude/` |
| User uploads | `/mnt/user-data/uploads/` |
| Final deliverables | `/mnt/user-data/outputs/` |
| Skill scripts | Bundled in `scripts/` alongside this SKILL.md |

Always `present_files` the final PDF + any SVG figures.

---

## Common Pitfalls (Learned the Hard Way)

1. **Table text overflow** — The #1 bug. ALWAYS use `Paragraph()` in cells. Never raw strings.
2. **Transparent/dark PNG backgrounds** — Render as black in PDF. Replace exact-black pixels
   (≤2,2,2) with white. Don't flood-fill aggressively — it destroys text.
3. **SVG without explicit white background** — Transparent SVG backgrounds also render black
   in PDF. Always include `<rect fill="white"/>` as the first element.
4. **Lost citations during rewrite** — Count references before and after. Must match exactly.
5. **Unicode subscripts in reportlab** — Characters like ₀₁₂ render as BLACK BOXES in
   Times-Roman. Use `<sub>` and `<super>` XML tags in Paragraph objects instead.
6. **Figure too tall for page** — Always cap height at ~7 inches and maintain aspect ratio.
7. **SimpleDocTemplate** — Can't do different headers per page. Use BaseDocTemplate with
   PageTemplate(id='first') and PageTemplate(id='later').
8. **Equations** — reportlab can't do LaTeX math. Use Unicode + sub/super tags for simple
   equations. For complex math, recommend the LaTeX pipeline instead.
9. **SSRN abstract formatting** — Plain text only. Strip all markdown/HTML before pasting.
10. **Orphan headings** — Check final PDF visually. Use `KeepTogether()` or `KeepWithNext()`
    if a heading lands at the bottom of a page with its body on the next.
