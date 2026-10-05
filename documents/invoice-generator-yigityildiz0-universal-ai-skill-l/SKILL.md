---
name: invoice-generator
description: Invoice-creation skill. Use when Codex should generate professional invoices from clients, dates, line items, taxes, and payment terms.
---

# Invoice Generator

Use this skill when the user needs a new invoice or a reusable invoice template.

## Workflow
- Collect all billing fields explicitly.
- Calculate subtotal, tax, discounts, and total clearly.
- Format for PDF, DOCX, or spreadsheet output.

## Deliverables
- A complete invoice draft or template.
- A machine-readable line-item table when useful.

## Guardrails
- Do not invent legal or tax details without marking placeholders.
- Do not alter currency or terms silently.
