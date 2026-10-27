---
name: thai-docx
description: |
  สร้างไฟล์ Word (.docx) ที่ภาษาไทยเขียนเต็มบรรทัดไม่ตัดบรรทัดก่อนเวลา ใช้ skill นี้ทุกครั้งที่ต้องสร้างเอกสาร Word ที่มีเนื้อหาภาษาไทย ไม่ว่าจะเป็นรายงาน บทความ เอกสารวิชาการ บันทึกข้อความ หรือเอกสารทั่วไป ใช้ได้กับข้อความภาษาไทยล้วนและไทย-อังกฤษผสม
  Trigger เมื่อ: ผู้ใช้ต้องการสร้าง Word ที่มีภาษาไทย, "ทำ docx ภาษาไทย", "สร้างเอกสาร Word", "ข้อความไทยไม่เต็มบรรทัด", "ข้อความตัดบรรทัดผิด", "Thai text line break", "สร้างรายงาน", "เขียนเอกสาร"
  ใช้ skill นี้แทน docx skill ปกติเมื่อเอกสารมีภาษาไทย เพราะ docx-js (JavaScript) ไม่จัดการ Thai line breaking ได้ดี
---

# Thai DOCX — Word documents with proper Thai line breaking

## Problem

Thai has no spaces between words. Word doesn't know where to break lines, so it breaks too early → short lines, wasted space on the right margin. English text is unaffected since Word breaks at spaces.

## Solution

Insert **Zero-Width Space (U+200B)** between Thai words before writing to docx. ZWS is invisible and zero-width but tells Word "you can break here." More break points → smarter wrapping → text fills lines fully.

## Setup

```bash
pip install pythainlp python-docx --break-system-packages
```

## Usage

The script at `scripts/thai_docx.py` provides two functions:

### `insert_zwsp(text)` — add ZWS between Thai words

Only processes Thai character runs. English, numbers, URLs stay untouched.

```python
from thai_docx import insert_zwsp
processed = insert_zwsp("สวัสดีครับผมชื่อสมชาย")
# → "สวัสดี\u200bครับ\u200bผม\u200bชื่อ\u200bสมชาย"
```

### `create_docx(paragraphs, output_path, ...)` — build the Word file

```python
from thai_docx import create_docx

paragraphs = [
    {"text": "Main heading", "type": "heading1"},
    {"text": "Body paragraph with Thai text...", "type": "body"},
    {"text": "Subheading", "type": "heading2"},
    {"text": "Another paragraph...", "type": "body"},
]

create_docx(
    paragraphs,
    "output.docx",
    font_name="TH Sarabun New",  # default
    font_size=14,                 # pt, default 14
    page_size="A4",               # "A4" or "Letter"
    line_spacing=1.5,             # default 1.5
    margins={"top": 2.54, "bottom": 2.54, "left": 2.54, "right": 2.54},  # cm
)
```

Paragraph types: `body`, `heading1`, `heading2`, `heading3`.

## Critical rules

- **Always use python-docx (Python), never docx-js (JavaScript)** for Thai documents
- **Always use LEFT alignment** — JUSTIFIED stretches spaces grotesquely, THAI_DISTRIBUTE stretches characters
- `insert_zwsp()` is called automatically inside `create_docx()` — no need to call it separately
- ZWS is invisible, zero-width, doesn't change text appearance — just enables line breaking

## CLI

```bash
python scripts/thai_docx.py input.txt -o output.docx --font "TH Sarabun New" --size 14
```

Blank lines in input.txt separate paragraphs. Lines starting with numbers (e.g. "15.5.2 ...") become headings automatically.
