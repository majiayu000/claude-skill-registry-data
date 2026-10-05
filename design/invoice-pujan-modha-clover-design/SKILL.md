---
name: invoice
description: |
  Professional invoice with line items, totals, tax, payment details, and
  branding. Use for "invoice", "billing", "receipt", "quote".
triggers:
  - "invoice"
  - "billing"
  - "receipt"
  - "quote"
  - "estimate"
df:
  mode: prototype
  platform: desktop
  scenario: operations
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Invoice Skill

Produce a professional invoice page.

## Layout
- **Letter/A4 sized wrapper** (8.5×11in or A4 via CSS `@page`).
- **Header**: company logo (wordmark), invoice #, date, due date.
- **From / To**: two-column addresses.
- **Line items**: table — description, quantity, rate, amount.
- **Totals**: subtotal, tax, discount, total. Right-aligned.
- **Payment info**: bank details or payment link.
- **Footer**: thank you note, terms.

## Rules
- Numbers in mono, right-aligned, 2 decimal places.
- Total in larger display font.
- Clean borders, subtle shading on header.
- Print-friendly: `@media print` hides any UI chrome.
- `data-df-id` on each line item row.

## Output
Single `index.html`, inline CSS.
