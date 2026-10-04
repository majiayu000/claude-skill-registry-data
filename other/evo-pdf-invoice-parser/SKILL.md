---
name: evo-pdf-invoice-parser
description: Extracts text from each page of a PDF invoice file using pdfplumber and parses structured fields (vendor name, IBAN, PO number, invoice amount) using regex.
---

# evo-pdf-invoice-parser

Extracts invoice data from PDF files. One invoice per page.

## Key Functions

- `extract_all_invoices(pdf_path)` - Returns list of dicts with page_number and parsed fields
- `extract_invoice_fields_from_text(text)` - Parse all fields from page text
- `extract_vendor_name(text)` - Extract vendor name after "From:"
- `extract_iban(text)` - Extract IBAN after "Payment IBAN:"
- `extract_invoice_amount(text)` - Extract total amount
- `extract_po_number(text)` - Extract PO number

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-invoice-parser/scripts')
from utils import extract_all_invoices

invoices = extract_all_invoices('/root/invoices.pdf')
for inv in invoices:
    print(inv['invoice_page_number'], inv['vendor_name'], inv['invoice_amount'])
```
