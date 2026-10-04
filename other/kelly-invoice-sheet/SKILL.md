---
name: kelly-invoice-sheet
description: Extract invoices, receipts, credit notes, statements, PDFs, images, docs, and spreadsheet-like invoice exports into a reviewable table with field confidence, line items, approval decisions, and CSV/JSON export. Use when the user invokes /kelly-invoice-sheet or $kelly-invoice-sheet, asks for "Invoice转表格", invoice OCR, receipt-to-spreadsheet, invoice data extraction, bookkeeping import prep, or a Lido-style Extract Data workflow with a Busabase-backed App-in-Skill UI.
metadata:
  category: finance
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-invoice-sheet
    resources:
      - invoices
      - settings
    risk: local-write

---

# Kelly Invoice Sheet

## Overview

Use this skill to turn invoice files or extracted invoice text into a structured batch that the user can review in a Busabase-backed spreadsheet-style UI. The skill owns extraction, reasoning, validation, and export; the AirApp only reads/writes its own Busabase Bases and records human decisions.

Default interaction mode: App UI. Unless the user explicitly asks for chat-only handling, ensure Busabase resources are provisioned (the AirApp does this lazily on first run), write extracted invoices with `scripts/import_batch.mjs`, and give the actual AirApp URL (or the local preview URL when local preview is explicitly requested).

## App UI Screenshots

<table>
  <tr>
    <td width="33%"><img src="assets/screenshots/overview.webp" alt="Kelly Invoice Sheet spreadsheet extraction desk"></td>
    <td width="33%"><img src="assets/screenshots/detail.webp" alt="Kelly Invoice Sheet invoice detail review"></td>
    <td width="33%"><img src="assets/screenshots/extract-data.webp" alt="Kelly Invoice Sheet Extract Data upload modal"></td>
  </tr>
  <tr>
    <td><strong>Spreadsheet extraction desk</strong><br>Sheet-like invoice table with extracted rows, status filters, confidence flags, and human-attention counts.</td>
    <td><strong>Invoice detail review</strong><br>Editable invoice fields, line items, confidence notes, and approve/request-changes/block controls.</td>
    <td><strong>Extract Data upload</strong><br>Lido-style upload modal with local file, Google Drive, OneDrive, and email source options.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-invoice-sheet-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Workflow

1. Accept invoice source files or source text from the user. Supported workflow inputs include PDFs, images, Word docs, CSV/XLS/XLSX exports, OCR text, email attachments, and pasted invoice text.
2. Extract invoice header fields, line items, totals, currency, dates, vendor identity, bill-to, payment terms, and source snippets. If OCR or document parsing needs another installed skill or tool, use it, then normalize the result into this skill's batch schema.
3. Read `references/invoice-batch-schema.md` before writing a batch file.
4. Write a batch JSON file (an object with an `invoices` array, or a bare array of invoice objects), keeping stable `id` and `ref` values such as `Review #1`.
5. Run `node scripts/import_batch.mjs --file <batch.json> --apply` to validate and write the batch into Busabase's `invoices` Base.
6. Give the user the AirApp URL (or start local preview with `pnpm --dir content/kelly-invoice-sheet-app dev` if explicitly requested).
7. After the user approves rows in the app, run `node scripts/export_decisions.mjs --apply` to export approved invoices to CSV and JSON and mark them `done`.

Use chat-only mode only when the user says "chat only", "no UI", "纯聊天", "不要打开 UI", or similar.

## Boundary

- The AirApp reads and writes its own Busabase Bases only; it never mutates an external system, uploads an invoice file, pays a vendor, emails anyone, or imports into accounting software. Parent decisions (approve/request-changes/block/revise) write straight onto the invoice record through `busabase-sdk`.
- The skill performs extraction, reasoning, and validation, then records the result to Busabase via `scripts/import_batch.mjs`. It never sends invoice files to an external service from the app itself — any external OCR/API use belongs to the skill workflow and should be explicit.
- Export only happens through the trusted `scripts/export_decisions.mjs` after explicit approval in the UI or chat.

## Busabase Resources

Two Bases under one application Folder (`kelly-invoice-sheet`), declared in `content/kelly-invoice-sheet-app/app/js/config.js` and the generated template sidecars under `content/`:

- `invoices`: one row per extracted invoice/receipt/credit note/statement — header fields, field confidence (JSON), line items (JSON array, shares the invoice's own lifecycle), risk/warning flags (JSON arrays), and the reviewer's decision (`decision-action`/`decision-note`/`decided-at`) written directly onto the same row. Written by `scripts/import_batch.mjs` when the agent finishes extracting a batch; status is set directly by a human decision in the app.
- `settings`: sanitized config summary (default currency, extraction preferences, review policy, export preferences — no secrets), one row keyed by `kind`.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/invoice-batch-schema.md` for exact field shapes.

## Workflow Statuses

- `needs_review`: extracted row needs human review.
- `changes_requested`: user asked the agent to revise extraction.
- `approved`: row is ready for export.
- `done`: row has been exported or intentionally completed.
- `blocked`: row cannot proceed without missing information or source correction.

## Extraction Rules

- Preserve source values. Do not invent invoice numbers, dates, tax ids, vendors, totals, or payment instructions.
- Keep original currency. Do not convert currencies unless the user explicitly asks and provides rates.
- Treat money fields as high-risk: totals, tax, amount due, currency, and bank/payment hints should be reviewed when confidence is low.
- Use `field_confidence` and `warnings` for ambiguous OCR, cropped images, handwritten values, missing references, negative totals, credit notes, duplicate invoice numbers, or total/line-item mismatches.
- Mark rows `blocked` if required fields are missing: vendor name, invoice number, invoice date, currency, or total.
- Never send invoice files to external services from the app. Any external OCR/API use belongs to the skill workflow and should be explicit.

## Scripts

- `node scripts/import_batch.mjs --file <batch.json> [--apply]`
  Validates a batch of extracted invoices and upserts each one into Busabase's `invoices` Base (matched by `invoice-id`, so re-running after a correction updates existing rows). Dry run by default.
- `node scripts/export_decisions.mjs [--apply] [--out <dir>]`
  Reads invoices with status `approved` from Busabase, grouped by `batch_id`, and exports each batch to `exports/<batch-id>/invoices.csv`, `line_items.csv`, and `approved_invoices.json`, then marks each exported invoice `done`. Dry run by default.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-invoice-sheet-app dev` only when local preview/debugging is explicitly requested.

## Demo Mode

`?demo=1#/invoices/all` opens the deterministic offline dataset (3 invoices: 2 `needs_review`, 1 `blocked`) for screenshots and review. Demo mode never reads or writes Busabase; demo decisions are read-only.

## Safety Defaults

- Treat invoice data as sensitive. Never commit a local credential file.
- The app only edits its own Busabase records. It does not upload invoices, import into accounting systems, send email, pay vendors, or mutate remote systems.
- Export only after explicit approval in the UI or chat, via `scripts/export_decisions.mjs`.

## Useful Commands

```bash
node skills/kelly-invoice-sheet/scripts/import_batch.mjs --file batch.json --apply
node skills/kelly-invoice-sheet/scripts/export_decisions.mjs --apply
pnpm --dir skills/kelly-invoice-sheet/content/kelly-invoice-sheet-app dev
```
