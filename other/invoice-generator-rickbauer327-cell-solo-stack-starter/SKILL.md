---
name: invoice-generator
description: Use when the user needs to create an invoice, bill a client, or turn a time log or list of deliverables into a sendable invoice. Produces a clean HTML invoice (printable to PDF) plus a markdown copy, numbered sequentially, using terms and details from .solo/business.md.
---

# Invoice Generator

Produce an invoice the user can send within a minute. Output is a self-contained HTML file (prints cleanly to PDF from any browser) plus a markdown copy for records.

## Step 1 — Load context
Read `.solo/business.md`. You need: business name/name, payment terms, payment methods, tax notes, currency, hourly/day rate. If missing, ask for only the missing fields — do not run the full setup.

## Step 2 — Invoice number
Look in `invoices/` for existing files named `INV-<number>-*.{html,md}`. Use the highest number + 1. If the folder is empty, ask the user for the starting number (default `INV-0001`). Never reuse a number.

## Step 3 — Line items
Accept any of:
- A time log (from `/time-log` or pasted): group by task/day, multiply hours by rate.
- A list of deliverables with fixed prices.
- A milestone from a proposal/SOW ("50% deposit for X").

Confirm the total with the user before writing if you had to make any assumption (e.g. which rate applies).

Compute: subtotal, tax (only if business.md specifies a rate; otherwise none and say so), total. Due date = issue date + payment terms (default net 14).

## Step 4 — Write the files
Write `invoices/INV-<number>-<client-slug>.html` and `.md`.

HTML requirements: single file, no external assets, system font stack, prints on one A4/Letter page, `@media print` hides nothing important. Layout:

```
<Business name>                                    INVOICE
<address / email / website>                        INV-<number>
                                                   Issued: <date>
Bill to:                                           Due: <date>
<Client name>
<Client contact / address if known>

| Description | Qty | Rate | Amount |
|-------------|-----|------|--------|
| ...         |     |      |        |

                                       Subtotal   <amount>
                                       Tax (<x>%) <amount>   (omit row if none)
                                       TOTAL      <amount>

Payment: <methods from business.md>
Terms: <payment terms>. <Late fee policy if any.>
<Tax/VAT note if any.>
Thank you.
```

Keep it plain. No logos unless the user provides a path; no colors beyond one accent for the total.

Markdown copy: same content as a table, for the user's records and for `/monthly-finance-summary`.

## Step 5 — Hand off
Report: file paths, total, due date. Offer a 3-sentence cover email in the business.md tone ("Invoice attached for <project>, total <amount>, due <date>. Let me know if anything needs adjusting.").

## Do not
- Do not guess tax rates. If business.md is silent, no tax line, and say so.
- Do not reuse or skip invoice numbers.
- Do not put bank account numbers into the file unless they are already in business.md or the user pastes them for this invoice.
