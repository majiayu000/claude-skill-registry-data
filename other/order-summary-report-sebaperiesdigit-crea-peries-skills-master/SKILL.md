---
name: order-summary-report
description: "Use when someone asks to summarize orders data, calculate revenue totals, or list the top selling products from an orders CSV."
argument-hint: [orders.csv]
---

## Purpose

Read an orders CSV file and produce a plain-text summary of total orders, total revenue, and the top 3 best-selling products.

## Inputs

- A file path to `orders.csv` or a similarly structured orders file.
- Expected columns: `order_id`, `order_total`, and a product identifier such as `product_name` or `items`.
- No file writes or external services.

## Steps

1. If a CSV path hasn't already been supplied (via `$ARGUMENTS` or earlier in the conversation), ask via `AskUserQuestion` how to provide it: **Provide a file path** / **Paste the CSV content directly** / **Use the file already referenced earlier in this conversation** (include this option, marked Recommended, only when one genuinely exists). If the file cannot be found, ask directly as free text for the correct path -- a path value has no finite menu.
2. Read the CSV file in read-only mode and validate that it contains the required columns.
3. Parse each row into order data, extracting `order_id`, `order_total`, and product/item names.
4. Skip rows with missing or invalid totals or product information, and track how many rows were skipped and why.
5. Count unique orders and sum `order_total` to calculate total revenue.
6. Tally product sales and identify the top 3 best-selling products, ranked by quantity or order count.
7. Return a clean plain-text summary with:
   - Total orders
   - Total revenue
   - Top 3 products and their sold quantities
   - Any skipped rows or validation issues

## Output

- A ready-to-read summary report in plain text.
- No files created, no data sent externally.

## Guardrails

- Do not modify the CSV file.
- Do not invent missing data.
- Be transparent about skipped or invalid rows.

## Notes

- Clickable-question convention: the Step 1 intake-method choice uses `AskUserQuestion`. The CSV content and any corrected file path stay free text -- genuine data, not a finite menu.
