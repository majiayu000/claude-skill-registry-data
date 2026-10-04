---
name: evo-receipt-parse-export
description: Parses OCR text from receipts to extract dates and total amounts using keyword-priority matching and regex, writes results to Excel.
---

# evo-receipt-parse-export

Parses OCR text from receipts to extract dates and total amounts using prioritized keyword matching with exclusion rules, then writes structured results to Excel.

## Key Functions

- `extract_date(ocr_text)` - Extract date from OCR text, returns ISO format (YYYY-MM-DD) or None
- `extract_total_amount(ocr_text)` - Extract total amount using keyword priority, returns string with 2 decimals or None
- `parse_receipt_text(ocr_text)` - Returns dict with date and total_amount
- `write_results_to_excel(results, output_path)` - Write results to xlsx with sheet "results"

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-receipt-parse-export/scripts')
from utils import parse_receipt_text, write_results_to_excel

parsed = parse_receipt_text(ocr_text)
write_results_to_excel(results_list, '/app/workspace/stat_ocr.xlsx')
```

## Total Amount Priority Keywords
1. GRAND TOTAL
2. TOTAL RM, TOTAL: RM
3. TOTAL AMOUNT
4. TOTAL, AMOUNT, TOTAL DUE, AMOUNT DUE, BALANCE DUE, NETT TOTAL, NET TOTAL

## Exclusion Keywords
SUBTOTAL, SUB TOTAL, TAX, GST, SST, DISCOUNT, CHANGE, CASH TENDERED
