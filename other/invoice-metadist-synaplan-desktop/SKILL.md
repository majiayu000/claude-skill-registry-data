---
name: invoice
description: Turn a JSON spec into a clean, print-ready HTML invoice with line totals, subtotal, optional tax, and grand total.
---

# invoice

Create a professional, print-ready invoice as one self-contained HTML file
(open it and print to PDF from the browser).

## How to run

1. First write the invoice spec as JSON into the out-box with the `Write` tool
   (e.g. `invoice.json`):

```json
{
  "number": "INV-1001",
  "date": "2026-09-01",
  "from": "Acme GmbH\nBerlin",
  "to": "Client Ltd\nLondon",
  "currency": "EUR",
  "tax_rate": 19,
  "notes": "Payment within 14 days.",
  "items": [
    { "description": "Consulting", "quantity": 3, "price": 150 },
    { "description": "Hosting", "quantity": 1, "price": 40 }
  ]
}
```

2. Then render it:

```
python3 <skill_dir>/run.py <spec.json> <output.html>
```

- `currency` — `EUR`, `USD`, `GBP`, `CHF`, `JPY`, or any symbol/text.
- `tax_rate` — a percentage (e.g. `19`) or a fraction (e.g. `0.19`); omit for none.

Standard library only. After running, tell the user the saved path.
