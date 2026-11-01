---
name: academic-poster
description: Create and review academic research posters (conference, demo, or symposium posters) from a manuscript, figures, and screenshots, delivered as an editable PowerPoint (.pptx) plus a print-ready PDF. Use when the user asks to make, design, draft, revise, or critique a research poster or any part of one (its section plan, text, layout, conclusion headline, or banner wording), turns a paper into a poster, or mentions poster size (A0, 48x36 in), a poster board, or a poster session.
---

# Academic Poster

Build the poster around the scientific contribution; design makes that contribution easier to understand and never replaces its explanation. The full guidance (narrative, structure, writing, hierarchy, figures, scenarios, style, conclusion, QC) is in [references/guidelines.md](references/guidelines.md). Read it at the start of every poster task.

The user builds posters in **PowerPoint**. Deliver an editable `.pptx` and a PDF exported from it. Do not propose LaTeX (tikzposter, beamerposter), Canva, or HTML unless the user asks. Use the `pptx` skill for the mechanics (pptxgenjs for a new poster, its editing workflow for an existing template or previous poster).

## Workflow

Work content first. Do not build a layout and then pour text into it.

1. **Gather inputs.** Manuscript (authoritative for every fact), figures, screenshots, previous posters, logos, and the venue's poster requirements (size, orientation, poster ID, branding). If the size is unknown, ask; do not guess silently. When inputs are missing, ask for them and, in the same reply, sketch a provisional section plan from what the user already said (for parallel scenarios, show their shared sub-parts).
2. **Draft the narrative as text** (markdown, in chat or a scratch file): background and gap, approach, architecture explanation, results or scenarios, and a two-level conclusion (one-sentence headline plus a short supporting paragraph). Pick the one takeaway. Mark what is implemented, evaluated, demonstrated, or future work, and keep claims inside that. Write real explanatory paragraphs: do not reduce sections to keyword bullets or a word cap to make the poster look sparse, and push back when the user asks for that.
3. **Plan the hierarchy.** A few main sections (typically 3 to 5). Decide which get large figures, which get tables, which get prose. Group tables beside the diagram they explain. Give parallel scenarios a parallel structure and one accent colour each.
4. **Get the user's sign-off** on the text and the section plan before building the PPTX. Poster text is the expensive part to redo.
5. **Build the PPTX** (see PowerPoint specifics below).
6. **Render and inspect** at full-poster scale (balance, reading order, alignment) and at print scale (crop regions at 100% to check body text, table labels, diagram annotations, screenshot detail). Fix and re-render. Never ship the first layout.
7. **Re-read the text** for accuracy, repetition, and unsupported claims, then run the checklist in section 12 of the guidelines.

## PowerPoint specifics

**Slide size first.** Set the slide to the print size before placing anything (pptxgenjs: `pres.defineLayout({ name: 'POSTER', width: W, height: H })` in inches, then `pres.layout = 'POSTER'`). PowerPoint caps slides at 56 x 56 in. For larger posters (e.g. 72 x 36 in), build at exact half scale (36 x 18 in), halve every font size, and tell the user to print at 200%.

| Format | Inches (W x H) |
|---|---|
| A0 portrait | 33.11 x 46.81 |
| A0 landscape | 46.81 x 33.11 |
| A1 portrait | 23.39 x 33.11 |
| US 48 x 36 landscape | 48 x 36 |
| US 36 x 48 portrait | 36 x 48 |

**Type sizes at full A0 / 48 x 36 scale** (scale proportionally for other sizes):

| Element | Size (pt) |
|---|---|
| Title | 80 to 110, bold |
| Authors / affiliations | 36 to 48 |
| Section headings | 48 to 60, bold |
| Subheadings | 36 to 44, bold |
| Body text | 28 to 36 (never under 24) |
| Table text, captions | 24 to 28 |
| Conclusion headline | 54 to 72, bold |

One sans-serif family throughout (e.g. Calibri, Arial, Source Sans). Left-align body text; do not justify.

**Editable vs embedded.**
- Editable PPTX objects: title, authors, affiliations, headings, body paragraphs, tables (native PowerPoint tables), captions, labels, header and footer bars, panel backgrounds, simple arrow workflows.
- Embedded images: architecture diagrams, maps, software screenshots, plots. Prefer the original vector (SVG, or EMF from the source); otherwise use PNG at 150 to 300 DPI at printed size (an image printed 15 in wide needs about 2250 to 4500 px). Preserve aspect ratio. Do not redraw a supplied diagram with approximate shapes unless asked.

**Layout grid.** Fix outer margins (about 1 in at A0), a column grid (2 to 4 columns), and a single gutter value (about 0.6 to 0.8 in) and reuse them everywhere. Compute positions from these constants in the build script instead of hand-placing coordinates.

**Header and conclusion.** Full-width header band with title, authors, affiliations, contact, logos, and poster ID. Full-width contrasting conclusion band near the bottom with the headline and supporting paragraph.

**Text fit.** PowerPoint does not shrink text reliably on export. Size boxes to their content and verify in the render that no text clips or overflows; shorten text or enlarge the box, do not drop below the minimum size.

## Rendering and export

The user's machine has Microsoft PowerPoint (no LibreOffice), so export through PowerPoint itself for exact fonts and layout. Scripts are in this skill's `scripts/` folder:

```bash
# PDF via PowerPoint COM (writes poster.pdf next to the pptx; close the file in PowerPoint first)
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/export_pdf.ps1 poster.pptx

# Full-poster preview (PyMuPDF, available in the base conda env)
python scripts/preview.py poster.pdf --dpi 20

# Print-scale crop: X Y W H in inches from the top-left, at 100 dpi
python scripts/preview.py poster.pdf --dpi 100 --crop 0 0 12 6
```

View the PNGs with the Read tool. Check several crops (header, a body paragraph, each table, each figure's annotations).

## Deliverables

- `poster.pptx` (editable)
- `poster.pdf` (print-ready, matches the PPTX)
- a full-poster PNG preview
- a short note listing anything unresolved: missing logos, low-resolution images, claims that need the author's confirmation, venue requirements not yet known

## User style rules that apply to poster text

Concise academic prose, no em dashes, no defensive "X, not Y" phrasing. Follow any project memory about terminology and figure text style (e.g. large bold-keyed fonts, no "·" separators).
