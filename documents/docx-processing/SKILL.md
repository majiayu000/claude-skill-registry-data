---
name: docx-processing
description: >
  Generate, parse, modify, and format Microsoft Word (.docx) documents
  programmatically. Use when creating styled corporate reports, extracting text
  and tables from Word documents with python-docx, manipulating document sections,
  headers, footers, and page breaks, replacing placeholders without losing formatting,
  or inspecting OpenXML structures and untrusted Word files. Do not use for legacy
  binary .doc files, PDFs, Google Docs, or for tracked-changes editing workflows that
  need Word's revision model (python-docx does not write tracked changes).
compatibility: >
  Agent Skills-compatible coding agents operating with python-docx (1.2.x checked in
  October 2026; Python 3.9+). LibreOffice (`soffice`) is optional for rendering a
  visual check.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "docx, word, office, python-docx, document-processing, formatting"
  topics: "office, documentation, devtools"
---

# Programmatic Microsoft Word (.docx) Processing

Microsoft Word documents (`.docx`) are zipped OpenXML packages containing structured XML parts representing document body, styles, headers, footers, relationships, and embedded media. This skill provides a complete, repeatable workflow for creating, reading, and modifying `.docx` files programmatically while preserving proper formatting, typographic hierarchy, and structural integrity.

Detailed reference guides:
- [OpenXML Structure & python-docx Internals](references/docx-structure.md)

---

## The 6-Step Document Engineering Workflow

1. **Inspect & Clarify Requirements**: Identify required margins, orientation (Portrait/Landscape), fonts, headers, footers, and branding color palettes.
2. **Select Tooling**: Use `python-docx` for Python workflows. Avoid shell tools that convert to plaintext and lose structure.
3. **Draft / Modify Document**: Build document linearly using semantic styles (`Heading 1`, `Heading 2`, `Normal`, `Table Grid`).
4. **Validate Document Structure**: Confirm that paragraph runs, table cells, and page breaks are valid OpenXML nodes without corruption.
5. **Inspect Content & Formatting**: Verify column widths, text wrapping, table alignments, and header/footer bindings.
6. **Deliver Genuine Output Artifact**: Ensure the final output is a genuine `.docx` file (never a renamed HTML or text file).

---

## 1. Creating a Styled Word Document with `python-docx`

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def generate_report(output_path: str):
    doc = Document()

    # Configure Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Header & Footer
    header = doc.sections[0].header
    header_p = header.paragraphs[0]
    header_p.text = "Confidential - Internal Engineering Review"
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    footer = doc.sections[0].footer
    footer_p = footer.paragraphs[0]
    footer_p.text = "Acme Corp © 2026"
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Document Title (Heading 0 / Title)
    title = doc.add_heading("Architecture Assessment Report", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Lead Paragraph with styled runs
    lead = doc.add_paragraph()
    run_bold = lead.add_run("Executive Summary: ")
    run_bold.bold = True
    lead.add_run(
        "This document details the transition from monolithic storage to "
        "distributed object stores across all production regions."
    )

    # Section Heading
    doc.add_heading("1. Throughput Benchmarks", level=1)

    # Adding a Structured Table
    data = [
        ["Service Tier", "Requests / Sec", "p99 Latency (ms)", "Status"],
        ["Database Layer", "14,500", "4.2", "OPTIMAL"],
        ["API Gateway", "52,000", "12.8", "OPTIMAL"],
        ["Async Queue", "8,200", "45.0", "ATTENTION"],
    ]

    table = doc.add_table(rows=len(data), cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            # Format header row
            if r_idx == 0:
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Add Page Break before next major chapter
    doc.add_page_break()

    doc.add_heading("2. Migration Timeline", level=1)
    p2 = doc.add_paragraph("Target completion is Q4 2026.")

    # Save artifact
    doc.save(output_path)
    print(f"Document saved successfully: {output_path}")

if __name__ == "__main__":
    generate_report("architecture_review.docx")
```

---

## 2. Reading and Modifying Existing `.docx` Files

```python
from docx import Document

def replace_in_paragraph(paragraph, placeholder: str, value: str) -> bool:
    """Replace placeholder text across runs, keeping the first touched run's formatting."""
    runs = paragraph.runs
    start = "".join(r.text for r in runs).find(placeholder)
    if start == -1:
        return False
    end = start + len(placeholder)
    pos = 0
    first = True
    for run in runs:
        r_start, r_end = pos, pos + len(run.text)
        pos = r_end
        if r_end <= start or r_start >= end:
            continue
        before = run.text[: max(start - r_start, 0)]
        after = run.text[min(end - r_start, len(run.text)):]
        run.text = before + (value if first else "") + after
        first = False
    return True


def inspect_and_update_docx(file_path: str, target_author: str):
    doc = Document(file_path)

    # Extract all text paragraphs
    full_text = [p.text for p in doc.paragraphs if p.text.strip()]
    print(f"Total paragraphs: {len(full_text)}")

    # Modify placeholder text in place, keeping run formatting (see helper below)
    for p in doc.paragraphs:
        replace_in_paragraph(p, "{{AUTHOR}}", target_author)

    # Read tables
    for t_idx, table in enumerate(doc.tables):
        print(f"Table {t_idx}: {len(table.rows)} rows x {len(table.columns)} cols")

    # Save to new file (never overwrite input directly)
    doc.save("updated_document.docx")
```

---

Word often splits a placeholder such as `{{AUTHOR}}` across several runs, so `paragraph.text = ...` or a naive per-run search either misses it or flattens the formatting. The helper above handles that case. Placeholders can also live in tables (`table.cell(r, c).paragraphs`), headers/footers (`section.header.paragraphs`), text boxes, and content controls, which `doc.paragraphs` does not reach; check each location you expect.

## 3. Untrusted Word Files and Sensitive Content

- A `.docx` is a ZIP: cap size and the number/size of entries before opening to avoid zip bombs, and process in a sandbox for files from strangers.
- `.docm` and `.dotm` can contain macros. Do not convert, enable, or run macros; reject them unless the task explicitly requires them.
- Inspect `word/_rels/document.xml.rels` and `settings.xml` for external targets (`TargetMode="External"`, remote templates via `attachedTemplate`): these can make Word fetch remote content on open. Do not fetch them on your own initiative.
- Documents carry metadata (author, last-modified-by, comments, revision history, hidden text, embedded files). Inspect `doc.core_properties` and the package before sharing outside the organization.
- Never place secrets in templates; generated documents are easily forwarded.

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Writing HTML and saving with `.docx` extension | Microsoft Word reports corrupt file error on open | Generate genuine OpenXML zip package via `python-docx` |
| Overwriting source file while open in Word | Permission denied crash (`EBUSY` / `PermissionError`) | Write to separate destination file |
| Manual spacing with multiple empty paragraphs | Inconsistent layout across different page sizes and printers | Use `paragraph.paragraph_format.space_after = Pt(12)` |
| Hardcoding non-standard fonts | Missing font falls back to a substitute on the recipient machine | Use widely available fonts or state the dependency |
| `paragraph.text = new` on formatted text | Removes all run formatting in that paragraph | Edit runs, or use the run-aware helper |
| Expecting a table of contents to fill itself | python-docx cannot compute page numbers; TOC fields update only in Word | Insert a TOC field and tell the user to update fields, or generate it with Word/LibreOffice |
| Relying on `doc.paragraphs` for all text | Misses tables, headers, footers, text boxes | Iterate each container explicitly |
| Treating "no exception on save" as correct | Layout problems appear only on render | Convert to PDF and look at pages |

---

## 5. Troubleshooting

| Symptom | Likely cause | Action |
| :--- | :--- | :--- |
| `KeyError: "no style with name 'X'"` | Style absent in the template | Use built-in names (`Normal`, `Heading 1`, `Table Grid` exist in the default template) or define the style |
| `BadZipFile` / "File is not a zip file" | Legacy `.doc`, HTML renamed, or truncated file | Check magic bytes (`PK`); convert legacy files with LibreOffice first |
| Word shows "unreadable content" | Invalid XML edits via lxml, duplicate ids, or a mislabeled file | Reopen with python-docx; rebuild from a known-good template; avoid manual XML unless necessary |
| Images missing or wrong size | Width not set or image blocked | `add_picture(path, width=Inches(5))` and check the file type |
| Spacing differs between Word and LibreOffice | Style defaults and font substitution | Set explicit paragraph formats and fonts, then compare renders |

Visual check (optional, requires LibreOffice): `soffice --headless --convert-to pdf --outdir out_dir report.docx`, then rasterize a page with `pdftoppm -png -r 80 -f 1 -l 1 out_dir/report.pdf out_dir/page`.

Comments are supported in python-docx 1.2 (`doc.add_comment(runs, text=..., author=...)`); tracked insertions and deletions are not, so edit those with raw XML only when required and say so.

## 6. Verification Checklist

- [ ] Output is a genuine `.docx` zip package (verified via `zipfile.is_zipfile(path)`).
- [ ] Heading hierarchy follows H1 -> H2 -> H3 without skipping.
- [ ] Tables have proper borders, cell padding, and header row formatting.
- [ ] Document margins, headers, and footers are consistently configured.
- [ ] File opens in Word or LibreOffice Writer without repair warnings.
