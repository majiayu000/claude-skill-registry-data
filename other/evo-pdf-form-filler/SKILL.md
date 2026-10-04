---
name: evo-pdf-form-filler
description: Fills PDF AcroForm fields (text and checkboxes) using pypdf, sets NeedAppearances flag, and writes the output PDF. Handles checkbox state detection and proper value updates.
---

# evo-pdf-form-filler

Fills a PDF AcroForm with provided data (text fields, checkboxes), sets the
/NeedAppearances flag, and writes the output PDF.

## Key Functions

- `fill_pdf_form(input_pdf, output_pdf, text_fields, checkbox_fields)` - Main entry point
- `set_need_appearances(writer)` - Sets /NeedAppearances on AcroForm root
- `fill_text_field(writer, field_name, value)` - Fill a single text field
- `fill_checkbox_field(writer, field_name, on_state)` - Check a single checkbox

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-form-filler/scripts')
from utils import fill_pdf_form

text_fields = {
    'SC-100[0].Page2[0].List1[0].Item1[0].PlaintiffName1[0]': 'Jane Smith',
    'SC-100[0].Page2[0].List3[0].PlaintiffClaimAmount1[0]': '5000',
}
checkbox_fields = {
    'SC-100[0].Page3[0].List5[0].Lia[0].Checkbox5cb[0]': '/1',
}
fill_pdf_form('blank.pdf', 'filled.pdf', text_fields, checkbox_fields)
```

## SC-100 Checkbox Notes

- Checkbox on-states are typically '/1', '/2', etc. (NOT '/Yes')
- Must match the non-Off key from the checkbox's /AP/N dictionary
- Use evo-pdf-field-inspector's get_checkbox_on_states() to discover correct values
