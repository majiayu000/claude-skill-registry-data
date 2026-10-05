---
name: exam-time-machine-bulk-gen
description: Bulk-generate Office deliverables (docx/xlsx/pdf) via python-docx + openpyxl + LibreOffice headless when user is out of time on an exam. Linux-friendly. Use when user asks to bulk-generate or has <30 min left.
---

# Bulk Office Generation Under Time Pressure

## Trigger
User has <30 min on a multi-task Office exam and wants you to do everything.
Original folder structure already exists. Source files available.

## The ladder
1. Default: estimate score gain/loss, just batch-execute
2. python-docx + openpyxl for Word/Excel (zero Office install)
3. LibreOffice headless for PDF conversion
4. Access on Linux = SQL scripts only - tell user to paste into Access GUI
5. VBA macros = .bas source file + empty .docm/.xlsm container
6. PivotTable/Forms = approximate only

## Concrete recipe (proven in ITAS2 exam)

### Word docs (python-docx)
```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def insert_field(paragraph, field_code, placeholder="Update field"):
    """Insert TOC/INDEX/XE field codes for Word"""
    run = paragraph.add_run()
    for tag, attrs, text in [
        ('w:fldChar', {'w:fldCharType': 'begin'}, None),
        ('w:instrText', {'xml:space': 'preserve'}, field_code),
        ('w:fldChar', {'w:fldCharType': 'separate'}, None),
        ('w:t', None, placeholder),
        ('w:fldChar', {'w:fldCharType': 'end'}, None),
    ]:
        el = OxmlElement(tag)
        if attrs:
            for k, v in attrs.items(): el.set(qn(k), v)
        if text: el.text = text
        run._r.append(el)

def add_page_break(paragraph):
    run = paragraph.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)

def set_two_columns(section):
    sectPr = section._sectPr
    cols = OxmlElement('w:cols')
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '720')
    sectPr.append(cols)
```

### Excel (openpyxl)
```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.formatting.rule import CellIsRule

ws.oddHeader.center.text = "Title"
ws.oddFooter.center.text = "Name | TaskXX | Date"
ws.conditional_formatting.add('H4:H100',
    CellIsRule(operator='equal', formula=['"Re-order"'],
               fill=PatternFill('solid', fgColor='FFFF0000'),
               font=Font(color='FFFFFFFF', bold=True)))
ws['B7'] = "=VLOOKUP(A7, Reference!A:E, 5, FALSE)"
```

### Bulk PDF convert
```python
import subprocess
for f in files:
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf',
                   '--outdir', dst_dir, f], timeout=60)
```

### Access on Linux
Write `.sql` files. User pastes into Access SQL view (1 min each).

## Critical pitfalls
- `shutil.copy` fails on NTFS when dest exists (mode-copy PermissionError). Use `shutil.copyfile()`
- Reserved words like Line/User/Order wrap in [Premium_Line] in SQL
- Multiple INSERT in one Access query: run separately
- python-docx 2-column layout needs manual OXML (cols element)
- openpyxl cannot write VBA: ship .bas + empty .docm/.xlsm
- soffice cannot read .accdb (no Jet driver) - Access GUI only

## Output structure
```
output_dir/
├── Task_XX_Name/
│   ├── main_file.docx
│   └── main_file.pdf
├── _CHECKLIST.txt
└── _SQL_SCRIPTS/
```

## Communication cadence (ponytail)
- Show score estimate, not 50-line plan
- Done beats here is the analysis
- Skip Access details unless user asks