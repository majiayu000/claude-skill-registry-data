---
name: word-documents
description: Use when creating, reading, or editing Word documents (.docx). Covers document generation with styles and structure, extracting content, find-and-replace, tracked changes, and templates.
metadata:
  category: documents
  version: 1.0.0
  tags: [docx, word, documents, templates, reports]
---

# Word Documents

## Purpose

Produce and manipulate `.docx` files programmatically, with real styles and structure rather than a wall of manually formatted paragraphs.

## When to Use

- Generating a report, memo, letter, or contract as a Word document.
- Extracting text, tables, or comments from an existing `.docx`.
- Performing find-and-replace across a document while preserving formatting.
- Filling a template with data.
- Working with tracked changes or comments.

## Capabilities

- Document generation with headings, tables, images, headers, and footers.
- Style application and modification.
- Content extraction, including tables and embedded objects.
- Find-and-replace preserving runs and formatting.
- Template filling.
- Tracked changes and comments.

## Inputs

- The content and its structure.
- A template or style reference, if the output must match a house style.
- The source document, when reading or editing.

## Outputs

- A valid `.docx` with a proper style hierarchy.
- Extracted content in a structured form.
- An edited document that preserves the formatting it should preserve.

## Workflow

1. **Use styles, never direct formatting** — A heading is `Heading 1`, not 18pt bold. Styles produce a navigable document, a working table of contents, and a document that can be restyled in one operation.
2. **Start from a template when the house style matters** — Load the organization's `.dotx` or a reference `.docx` and write into its styles rather than recreating them.
3. **Structure before content** — Headings, then the body. The outline is what makes a long document usable.
4. **Preserve formatting when editing** — A naive find-and-replace on the XML destroys runs. Replace within runs, and handle text split across runs.
5. **Verify the output** — Open it. A `.docx` that a library writes without error can still be malformed in ways Word will complain about.

## Best Practices

- Direct formatting (bold, a font size, a colour applied by hand) makes a document unmaintainable. Every visual property should come from a style.
- Text in Word is stored in runs, and a single sentence is frequently split across several. A replace that only handles single-run text will silently miss matches where formatting changes mid-word.
- Tables need a table style, or they render with no borders and are unreadable when printed.
- Images need explicit dimensions. Without them, Word inserts at native resolution, which is usually enormous.
- A table of contents field must be marked for update, and Word will prompt the user on open. This is expected behavior, not a bug.
- For a document that will be edited by humans, keep the structure simple. Deeply nested tables and text boxes are fragile.

## Examples

**Generating a structured document:**

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Start from the house template so styles already exist and match.
doc = Document("templates/report-template.docx")

doc.add_heading("Quarterly Operations Review", level=0)   # Title style

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Q2 2026")
run.italic = True

doc.add_heading("Summary", level=1)
doc.add_paragraph(
    "Availability met the 99.9% target in each month of the quarter. "
    "Two incidents exceeded the 30-minute recovery objective; both are covered below."
)

doc.add_heading("Incidents", level=1)

table = doc.add_table(rows=1, cols=4)
table.style = "Light Grid Accent 1"          # a real table style, not hand-drawn borders

for cell, heading in zip(table.rows[0].cells, ["Date", "Duration", "Impact", "Cause"]):
    cell.paragraphs[0].add_run(heading).bold = True

for incident in incidents:
    row = table.add_row().cells
    row[0].text = incident.date.isoformat()
    row[1].text = f"{incident.minutes} min"
    row[2].text = incident.impact
    row[3].text = incident.cause

doc.add_page_break()
doc.save("output/q2-review.docx")
```

**Find-and-replace that survives split runs:**

```python
def replace_text(paragraph, old: str, new: str) -> None:
    """Word splits text across runs at formatting boundaries. A naive
    run-by-run replace misses any match that spans a boundary — which is
    most of them, in a real document."""
    full_text = "".join(run.text for run in paragraph.runs)
    if old not in full_text:
        return

    replaced = full_text.replace(old, new)

    # Write the result into the first run and clear the rest, preserving the
    # first run's formatting for the whole paragraph.
    paragraph.runs[0].text = replaced
    for run in paragraph.runs[1:]:
        run.text = ""
```

## Notes

- The split-run problem is the most common source of "my find-and-replace only worked sometimes". A placeholder like `{{name}}` is frequently stored as `{{`, `nam`, `e}}` across three runs because of an autocorrect or a spellcheck boundary.
- `.dotx` templates preserve styles, headers, footers, and page setup. Loading one is nearly always better than building a document's styling from scratch.
- If the output will be converted to PDF, verify the conversion — fonts that are not embedded will be substituted, and the layout will shift.
