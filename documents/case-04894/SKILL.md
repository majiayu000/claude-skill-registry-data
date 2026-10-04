---
name: ca-file-processor
description: >
  Process financial documents for Indian CA firms. Use when any PDF, Excel (.xlsx/.xls), CSV, JPG, or PNG file is received or uploaded — including GST returns, ITR PDFs, scanned invoices, trial balance sheets, bank statements, Form 16, TDS certificates, and audit reports. Automatically detects file type and extracts text, tables, and key fields (GSTIN, invoice number, totals, dates).

  Triggers on: file upload, attachment, "process this file", "read this PDF", "extract from this invoice", "analyse this statement", "what does this document say".
version: 1.0.1
homepage: https://github.com/purvik6062/ca-file-processor
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins:
        - python3
        - tesseract
      env: []
    files:
      - "scripts/*"
---

# CA File Processor

This skill processes the four most common file formats used by Indian CA firms and extracts structured information from them for analysis, summarisation, and answering queries.

## Supported formats

- **PDF** — GST returns, ITR acknowledgements, audit reports, scanned invoices (text-layer and scanned via OCR)
- **Excel (.xlsx / .xls)** — Trial balance, P&L, balance sheets, payroll registers, GST workings
- **CSV** — Bank statement exports (HDFC, ICICI, SBI), GSTR-2B downloads, Tally exports
- **Images (.jpg / .png)** — WhatsApp invoice photos, scanned Form 16, cheque images

## How to use

When a file is attached or uploaded, run the appropriate script:

```
python3 scripts/skill_router.py <file_path>
```

The router auto-detects the file type and calls the correct processor. It returns a structured JSON dict.

## What to do with the output

Once the script returns output, use it to:

1. Answer the user's question about the document
2. Extract specific fields they asked for (GSTIN, totals, dates)
3. Summarise the document in plain language
4. Flag anomalies or missing information
5. Compare figures across multiple documents

## Field extraction — what gets detected automatically

For invoices and PDFs:
- GSTIN (supplier and recipient)
- Invoice number and date
- Total amount / grand total
- PAN number
- Email and phone

For bank statements (CSV):
- Total debits and credits
- Date range of transactions
- Detected bank format

For Excel files:
- Document type (trial balance / P&L / balance sheet / payroll / GST workings / ledger)
- Sheet names and row counts
- Preview of header rows

## OCR notes

- Text-layer PDFs are read directly (fast, accurate)
- Scanned PDFs and images go through Tesseract OCR (English + Hindi)
- Confidence is rated high / medium / low in the output
- Always flag low-confidence results to the user and ask for confirmation on numeric fields

## Trust statement

This skill runs entirely locally on your server. No data is sent to any external service. All processing happens via open-source Python libraries (PyMuPDF, pytesseract, openpyxl, pandas).
