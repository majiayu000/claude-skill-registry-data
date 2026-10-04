---
name: evo-pdf-field-inspector
description: Inspects PDF AcroForm fields - enumerates field names, types, values, and checkbox on-states. Essential for discovering exact internal field keys before filling.
---

# evo-pdf-field-inspector

Inspects a PDF form to enumerate all AcroForm field names, types (text, checkbox, radio),
current values, and checkbox appearance states.

## Key Functions

- `enumerate_pdf_fields(pdf_path)` - Returns dict of all fields with type, value, flags
- `classify_field_type(field_obj)` - Classifies pypdf Field into human-readable type
- `get_checkbox_on_states(pdf_path)` - Returns dict mapping checkbox field names to their on-state

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-field-inspector/scripts')
from utils import enumerate_pdf_fields, get_checkbox_on_states

fields = enumerate_pdf_fields('form.pdf')
checkbox_states = get_checkbox_on_states('form.pdf')
```

## SC-100 Field Name Pattern

Field names follow hierarchical pattern: `SC-100[0].PageN[0].Section.Field`
Checkbox on-states are typically `/1`, `/2`, etc. (NOT `/Yes`)
