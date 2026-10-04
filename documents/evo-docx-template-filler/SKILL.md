---
name: evo-docx-template-filler
description: >
  A utility module for filling Word document templates (.docx) with data from JSON files.
  Handles split-run-aware text replacement to preserve formatting, traverses all document
  containers (body, tables, nested tables, headers, footers, text boxes), and processes
  conditional IF/END_IF blocks by keeping or removing content based on data values.
---

# evo-docx-template-filler

Fill Word (.docx) templates with data from JSON, preserving formatting and handling conditionals.

## Key Capabilities

1. **Split-run-aware replacement**: Handles OOXML split runs where placeholders like `{{NAME}}` are fragmented across multiple XML runs
2. **Comprehensive container traversal**: Body paragraphs, tables (nested), headers (default/first/even), footers, text boxes
3. **Conditional blocks**: `{{IF_KEY}}...{{END_IF_KEY}}` - keeps content when condition is true (removes markers), removes entire block when false
4. **Format preservation**: Replaces text at run level, never overwrites paragraph.text
5. **Safe deletion**: Prevents OOXML corruption by not removing the last paragraph in table cells

## Usage

```python
import sys
sys.path.insert(0, "/app/environment/skills/evo-docx-template-filler/scripts")
from utils import (
    load_json_data,
    iter_all_paragraphs,
    replace_text_in_paragraph,
    process_conditional_blocks,
    delete_paragraph,
    apply_template_data
)

# One-liner to fill a template:
apply_template_data("template.docx", "data.json", "output.docx")

# Or step by step:
from docx import Document
import json

doc = Document("template.docx")
data = load_json_data("data.json")
process_conditional_blocks(doc, data)
for para in iter_all_paragraphs(doc):
    for key, value in data.items():
        if not key.startswith("IF_"):
            replace_text_in_paragraph(para, "{{" + key + "}}", str(value))
doc.save("output.docx")
```

## Functions

- `load_json_data(filepath)` - Load JSON data file
- `iter_all_paragraphs(doc)` - Generator yielding all paragraphs from body, tables, headers, footers, text boxes
- `replace_text_in_paragraph(paragraph, search_text, replace_text)` - Split-run-aware text replacement
- `process_conditional_blocks(doc, data)` - Handle IF/END_IF blocks (inline and multi-paragraph)
- `delete_paragraph(paragraph)` - Safe paragraph deletion with table cell protection
- `apply_template_data(template_path, json_path, output_path)` - Main orchestration function

## Conditional Logic

Condition evaluation for `{{IF_KEY}}`:
1. Check `IF_KEY` in data (bool or yes/true/1)
2. Check `KEY_PACKAGE` in data (e.g., RELOCATION -> RELOCATION_PACKAGE)
3. Check `KEY` directly in data

When condition is true: content is kept, `{{IF_KEY}}` and `{{END_IF_KEY}}` markers are removed.
When condition is false: entire block (markers + content) is deleted.
