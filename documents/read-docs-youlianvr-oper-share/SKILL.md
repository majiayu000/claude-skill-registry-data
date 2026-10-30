---
name: read-docs
description: Reading .doc/.docx files via python-docx.
---

# Skill: read-docs

Reading .doc/.docx files via python-docx.

## Installed

- **python-docx 1.2.0** — primary library
- Ready scripts in `scripts/check_docx.py` and `scripts/extract_docx.py`

## Quick start

### Simple text extraction

```python
from docx import Document

doc = Document("path/to/file.docx")
for p in doc.paragraphs:
    if p.text.strip():
        print(p.text)
```

### Document structure (styles, headings)

```python
from docx import Document

doc = Document("file.docx")

# Style statistics
styles = {}
for p in doc.paragraphs:
    s = p.style.name
    styles[s] = styles.get(s, 0) + 1

print("Styles:", styles)

# Headings only
for p in doc.paragraphs:
    if p.style.name.startswith("Heading"):
        print(f"[{p.style.name}] {p.text}")
```

### Tables

```python
doc = Document("file.docx")
for table in doc.tables:
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        print(" | ".join(cells))
```

### Formatting info

```python
doc = Document("file.docx")
for p in doc.paragraphs[:10]:  # first 10 paragraphs
    align = str(p.alignment) if p.alignment else "None"
    fonts = set()
    for run in p.runs:
        if run.font.name:
            fonts.add(run.font.name)
    print(f"align={align} fonts={fonts} | {p.text[:80]}")
```

### Text extraction with page breaks

```python
doc = Document("file.docx")
for i, p in enumerate(doc.paragraphs):
    if p.paragraph_format.page_break_before:
        print(f"\n--- PAGE BREAK ---\n")
    print(p.text)
```

## Ready scripts

### `scripts/extract_docx.py`

Extracts clean text from .docx to stdout.

```bash
python scripts/extract_docx.py
```

**Note:** Pass the .docx path as an argument: `python scripts/extract_docx.py file.docx` — for other files, change the path in the code.

### `scripts/check_docx.py`

Analyzes document structure: paragraphs, styles, headings, fonts, page breaks.

```bash
python scripts/check_docx.py
```

Also accepts a path argument: `python scripts/check_docx.py file.docx`.

## When to use what

| Task | Tool |
|------|------|
| Quick text extraction | `extract_docx.py` (or one-liner: `python -c "from docx import Document; d=Document('file.docx'); [print(p.text) for p in d.paragraphs if p.text.strip()]"`) |
| Study document structure | `check_docx.py` (styles, headings, fonts) |
| Tables, complex formatting | Custom python-docx script |
| Embed in another agent | Import `docx.Document` directly in code |

## Important notes

- **Encoding:** `python-docx` works with UTF-8, but if output goes to Windows cmd, set:
  ```python
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
  ```
- **Images:** `python-docx` does NOT extract images from .docx. Only text, tables, formatting.
- **Large files:** Reading the entire document into memory — for files >50MB may be slow.
- **.doc (old format):** `python-docx` does NOT read old .doc files (Word 97—2003). Use `python-docx2txt` or convert via LibreOffice.
- **Lists:** Numbered and bulleted lists are read as regular paragraphs (without nesting info).
- **Headers/footers:** Read via `doc.sections[0].header.paragraphs` and `.footer.paragraphs`.

## Installation (if needed on another machine)

```bash
pip install python-docx
```

---

*Created: 2026-06-19.*
