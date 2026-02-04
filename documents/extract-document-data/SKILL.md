---
name: extract-document-data
description: Extract structured JSON data from business document images (invoices, purchase orders, receipts, delivery orders) using Vision API. Use when processing scanned or photographed business documents that need to be digitized into structured data.
---

# TASK: Extract Data from This Document Image

You are analyzing a document image. Extract all visible business document data and return ONLY valid JSON following the schema below.

Extract structured data from business document images (PDF, PNG, JPEG) using Claude's Vision API.

## Overview

This skill performs pure data extraction from document images. It does NOT make classification decisions about whether a document is "sales" or "purchase" for your company - that responsibility belongs to the Database Agent.

**Your Job**: Extract what you SEE on the document
**Database Agent's Job**: Verify issuer, classify document type, save to database

## Quick Start

When given a document image, extract all visible fields and return as JSON:

```json
{
  "extracted_fields": {
    "issuer": "Company name in header",
    "recipient": "Company in 'Bill To' field",
    "document_title": "EXACT header text",
    "document_number": "Invoice/PO number",
    "date": "YYYY-MM-DD",
    "total_amount": 0.00,
    "items": [...],
    "tax_amount": 0.00,
    "grand_total": 0.00
  },
  "document_type_hint": "invoice",
  "confidence": 0.95
}
```

## Complete Output Schema

Return ONLY valid JSON (no markdown, no explanations):

```json
{
  "extracted_fields": {
    "issuer": "Company name at TOP of document or 'From:' field",
    "recipient": "Company in 'Bill To:', 'To:', 'Customer:', or 'Attention:' field",
    "document_title": "EXACT text from header (e.g., 'SALES INVOICE', 'PURCHASE ORDER', 'TAX INVOICE')",
    "document_number": "Document identifier (e.g., INV-2025-0001, PO25100055, DN-001)",
    "date": "Document date in YYYY-MM-DD format",
    "due_date": "Payment due date in YYYY-MM-DD or null if not shown",
    "total_amount": 0.00,
    "currency": "MYR/USD/SGD (default MYR for Malaysian documents)",
    "items": [
      {
        "description": "Product or service name/description",
        "quantity": 0,
        "unit_price": 0.00,
        "total": 0.00
      }
    ],
    "tax_rate": 6.0,
    "tax_amount": 0.00,
    "subtotal": 0.00,
    "grand_total": 0.00,
    "payment_terms": "Net 30/COD/Upon Receipt/null",
    "notes": "Any remarks, terms, or notes shown on document",
    "issuer_address": "Full address of issuer if visible",
    "recipient_address": "Full address of recipient if visible",
    "issuer_contact": "Phone/email of issuer if visible"
  },
  "document_type_hint": "invoice",
  "confidence": 0.95
}
```

## Extraction Rules

### Rule 1: Issuer vs Recipient
- **Issuer**: Company name at the TOP of document, in letterhead, or labeled "From:"
- **Recipient**: Company labeled "Bill To:", "To:", "Customer:", "Attention:", or "Ship To:"

### Rule 2: Document Title - Extract EXACTLY
Extract the EXACT text you see in the document header:
- If it says "TAX INVOICE" → write "TAX INVOICE" (not "invoice")
- If it says "PURCHASE ORDER" → write "PURCHASE ORDER" (not "PO")
- If it says "SALES INVOICE" → write "SALES INVOICE"

### Rule 3: Numbers - No Formatting
Remove all currency symbols and commas:
- "RM 1,299.50" → 1299.50
- "$5,000.00" → 5000.00
- "18,550" → 18550.00

### Rule 4: Dates - Standardize Format
Convert all dates to YYYY-MM-DD:
- "23/10/2025" → "2025-10-23"
- "Oct 23, 2025" → "2025-10-23"
- "23-Oct-2025" → "2025-10-23"

### Rule 5: Missing Fields
Use `null` for any field not found on the document. DO NOT guess or make up values.

### Rule 6: All Line Items
Extract EVERY line item from the document into the items array. Don't skip any.

## Document Type Hints

Based on visual appearance ONLY, provide ONE of these hints:

| Visual Text | Hint Value |
|-------------|------------|
| "INVOICE", "TAX INVOICE", "SALES INVOICE", "BILL" | `invoice` |
| "PURCHASE ORDER", "PO" | `purchase_order` |
| "DEBIT NOTE", "DN" | `debit_note` |
| "CREDIT NOTE", "CN" | `credit_note` |
| "DELIVERY ORDER", "DO", "DELIVERY NOTE" | `delivery_order` |
| "QUOTATION", "QUOTE", "PROPOSAL" | `quotation` |
| "SALES ORDER", "SO" | `sales_order` |
| Unclear or doesn't match above | `other` |

**IMPORTANT**: This is just a visual HINT. The Database Agent will determine the final classification by verifying who the issuer is.

## Confidence Scoring

Rate your extraction quality (0.0 to 1.0):

| Score | Quality |
|-------|---------|
| 0.9-1.0 | Clear, high-quality scan - all text perfectly readable |
| 0.7-0.9 | Good quality - minor OCR challenges but data is clear |
| 0.5-0.7 | Readable but poor scan quality or some handwritten parts |
| 0.0-0.5 | Very poor quality - many fields unclear or unreadable |

**If confidence < 0.7**: Note which specific fields are uncertain in the `notes` field.

## Critical Rules

**DO**:
- Extract what you SEE, not what you think it means
- Return ONLY valid JSON (start with `{`, end with `}`)
- Use null for missing data
- Be precise with numbers (no commas, no currency symbols)
- Extract document_title EXACTLY as shown
- Include ALL line items

**DO NOT**:
- Decide if document is "sales" vs "purchase" for the company
- Add markdown code blocks or explanations
- Guess or make up missing values
- Round numbers or change precision
- Modify the document title text
- Skip line items

## Example Extraction

**Input**: Image of an invoice with header "TAX INVOICE", from "Dell Malaysia Sdn Bhd" to "Carrickc Emart Sdn Bhd", total RM 185,500.00

**Output**:
```json
{
  "extracted_fields": {
    "issuer": "Dell Malaysia Sdn Bhd",
    "recipient": "Carrickc Emart Sdn Bhd",
    "document_title": "TAX INVOICE",
    "document_number": "SI-2025-9999",
    "date": "2025-10-23",
    "due_date": "2025-11-22",
    "total_amount": 175000.00,
    "currency": "MYR",
    "items": [
      {
        "description": "Dell Laptop XPS 15",
        "quantity": 50,
        "unit_price": 3500.00,
        "total": 175000.00
      }
    ],
    "tax_rate": 6.0,
    "tax_amount": 10500.00,
    "subtotal": 175000.00,
    "grand_total": 185500.00,
    "payment_terms": "Net 30",
    "notes": null,
    "issuer_address": "No. 88, Jalan Ampang, 50450 Kuala Lumpur",
    "recipient_address": "No. 123, Jalan Bukit Bintang, 55100 Kuala Lumpur",
    "issuer_contact": "+60 3-2164 8888"
  },
  "document_type_hint": "invoice",
  "confidence": 0.95
}
```

## Response Format

**Start your response with `{`**
**End your response with `}`**
**No markdown code blocks**
**No explanations before or after JSON**

Just the JSON object.
