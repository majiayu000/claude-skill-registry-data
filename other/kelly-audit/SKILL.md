---
name: kelly-audit
description: Personal finance anomaly review desk (Busabase App-in-Skill) that imports the three business tables — orders, invoices, payments/receipts (回款) — from CSV/JSON exports, flags anomalies with deterministic rules, and runs a human review queue with auditable decisions. Use when the user invokes $kelly-audit or /kelly-audit, mentions finance audit, order invoice payment reconciliation, 对账, 应收, 回款, 发票异常, receivables aging, overdue receivables, duplicate payments, missing invoices, amount mismatches, or anomaly review.
metadata:
  category: finance
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-audit
    resources:
      - orders
      - invoices
      - payments
      - anomalies
      - import-log
      - settings
    risk: gated-write

---

# Kelly Audit

## Overview

Use this skill as Kelly's finance anomaly review desk for a finance lead, small-business owner, or bookkeeping team. It imports the three business tables — orders, invoices, and payments/receipts (回款) — from local CSV/JSON exports, cross-checks them with deterministic rules plus agent judgment, and surfaces anomalies in a Busabase-backed App-in-Skill review queue. Reading local export files is a genuine external operation a browser cannot perform: `scripts/import_tables.mjs` is the only place a document enters the system, `scripts/run_checks.mjs` re-derives statuses and runs the anomaly rules, and `scripts/execute_decisions.mjs` prints the plan for approved anomalies. The AirApp itself only reads Busabase and writes review decisions; approved items become concrete follow-up actions (chase a receivable, reissue an invoice, flag to the accountant) executed by the agent outside the app.

This is different from kelly-money, which watches Kelly's own provider accounts: kelly-audit audits imported business documents against each other.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, import/check what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered anomaly cards (`Anomaly #1`) and take verdicts in chat.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Audit overview"></td>
    <td width="50%"><img src="assets/screenshots/anomalies.webp" alt="Kelly Audit anomaly queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Finance audit desk with amount at risk, receivable aging bar, anomaly queue preview, and import history.</td>
    <td><strong>Anomaly queue</strong><br>Rule-flagged anomalies with the order-invoice-payment evidence chain and a drafted chasing email for approval.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/invoices.webp" alt="Kelly Audit invoices"></td>
    <td width="50%"><img src="assets/screenshots/orders.webp" alt="Kelly Audit orders"></td>
  </tr>
  <tr>
    <td><strong>Invoices</strong><br>Invoice ledger with due dates, paid amounts, days overdue, and match status.</td>
    <td><strong>Orders</strong><br>Normalized orders with invoice and payment status badges and linked anomaly indicators.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-audit-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Imports are local files only: `scripts/import_tables.mjs` reads CSV/JSON exports the user provides, normalizes them, and writes them to Busabase. It never fetches business documents from remote systems on its own.
- The AirApp reads and writes Busabase records only. It must not send emails, change ERP/bookkeeping records, move money, or mutate remote systems.
- Any outbound follow-up (a receivable-chasing email, a message to the accountant, a billing task) is approval-required through the anomaly queue and executed by the agent OUTSIDE the app via other skills (e.g. kelly-email), with the real result recorded back onto the anomaly. `scripts/execute_decisions.mjs` never performs these operations itself — it only writes an execution marker.
- Treat all order/invoice/payment data as sensitive business data. Never commit local export files, env files, or generated reports.

## Busabase Resources

Six Bases under one application Folder (`kelly-audit`), declared in `content/kelly-audit-app/app/js/config.js` and the generated template sidecars under `content/`:

- `orders`: normalized sales orders imported from CSV/JSON exports.
- `invoices`: normalized invoices and credit notes.
- `payments`: normalized payments / receipts (回款).
- `anomalies`: the review queue — rule-flagged anomalies with severity, evidence, a drafted follow-up, and the human decision + execution marker on the same row.
- `import-log`: append-only history of import runs (files, added/updated counts, row warnings).
- `settings`: one row (`record-id: "config"`) with company profile, tolerance rules, and import column mappings.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/audit-schema.md` for exact field shapes. Links (order → invoice → payment), statuses, receivable aging, and metrics are recomputed client-side from the stored rows on every read (`content/kelly-audit-app/app/js/audit-model.js`'s `deriveSnapshot`/`buildSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last import/checks run.

## First Run And Onboarding

On invocation, check the `orders`/`invoices`/`payments` Bases. If all three are empty, guide setup before importing real tables: ask, turn by turn, company profile (name, contact email, base currency, optional `fx_rates` for mixed-currency books), which export files to import and their column headers, and tolerance rules (`days_to_invoice`, `amount_tolerance_pct`, `aging_buckets` default 30/60/90, `duplicate_window_days`). Write the answers onto the Settings row, then import:

```bash
node skills/kelly-audit/scripts/import_tables.mjs \
  --orders /path/orders.csv --invoices /path/invoices.csv --payments /path/payments.csv --apply
node skills/kelly-audit/scripts/run_checks.mjs --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-audit-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: audit command desk. Human-attention panel (anomalies needing a decision, high-risk amount at stake, overdue receivables total), KPI cards (orders/invoices/payments imported, matched %, open anomalies, receivable outstanding), a receivable aging buckets bar (inline SVG), and the recent import log.
- `#/orders` and `#/orders/<id>`: normalized orders table — order no, customer, date, amount, currency, invoice status badge, payment status badge, linked anomaly. Detail shows the linked invoice(s) + payment(s) chain with per-link status.
- `#/invoices` and `#/invoices/<id>`: invoices table — invoice no, order ref, customer, issue/due dates, amount, paid amount, days overdue, status. Detail shows matched payments, amount deltas, and notes.
- `#/anomalies` (and `#/anomalies/<id>` deep links): the review queue with workflow states `needs_review`, `changes_requested`, `approved`, `done`, `blocked`. Each anomaly card shows the rule badge, severity, evidence (the exact rows plus the computed delta), the agent-drafted follow-up action (e.g. a receivable-chasing email draft or an internal request), an editable draft plus a `Review note` textarea, decision buttons (approve / request changes / block / dismiss = done), and a stable reference such as `Anomaly #1`. Decisions write directly onto the anomaly record through `busabase-sdk`.
- `#/settings`: sanitized config summary — company profile, tolerance rules, and import column mappings, read live off the Settings Base.

Demo mode:

- `?demo=1` opens a deterministic mock audit desk for documentation and screenshots.
- `?demo=overview`, `?demo=orders`, `?demo=invoices`, `?demo=anomalies`, and `?demo=detail` (an amount-mismatch anomaly with its evidence chain) select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo content itself (customer names such as 明华贸易, anomaly titles, reasons, drafted emails) is meaningfully localized for Chinese screenshots.
- Demo mode never reads or writes Busabase. Decision buttons still work but act on in-memory state only.

UI language: support English and Chinese chrome with `Auto` default (following the browser language) plus an explicit selector persisted locally. Keep imported document numbers and real business data untranslated.

## Import Workflow

1. Detect mode. Default to AirApp-first.
2. Check the `orders`/`invoices`/`payments` Bases. If all three are empty, enter onboarding.
3. Ask which export files to import (orders, invoices, payments — any subset) and confirm the column mapping if the headers changed (stored on the Settings row's `import_*_columns` fields).
4. Run the write path:

```bash
node skills/kelly-audit/scripts/import_tables.mjs \
  --orders /path/orders.csv --invoices /path/invoices.csv --payments /path/payments.csv --apply
```

The script parses CSV (quoted fields included) or JSON arrays, applies the column mapping from Settings, normalizes dates/amounts/currencies, and upserts each row into Busabase by natural key (`order_no` / `invoice_no` / `payment_ref`) so re-imports are idempotent. It appends an entry to the `import-log` Base with per-file added/updated counts and row warnings. Without `--apply` it is a dry run.

5. Surface import warnings (skipped rows, payments referencing unknown invoices) to the user instead of silently dropping them.

## Check Workflow

1. After every import (or on request), run the deterministic rule set:

```bash
node skills/kelly-audit/scripts/run_checks.mjs --apply
```

Rules, driven by the Settings row's tolerances: `missing_invoice` (order without invoice after `days_to_invoice` days), `amount_mismatch` (invoice total vs order amount beyond `amount_tolerance_pct`), `overdue_receivable` (unpaid past due date, with 30/60/90+ aging buckets), `duplicate` (duplicate payment within `duplicate_window_days`, duplicate invoice number), `unmatched_payment` (payment matching no invoice), `irregular_entry` (credit note without an original, negative payments).

2. Anomaly ids are stable (`anom-<rule>-<key>`), so re-runs upsert instead of duplicating; existing statuses, refs, decisions, and executions are preserved; anomalies whose condition cleared are auto-resolved to `done`.
3. The agent may then improve on the deterministic output: sharpen titles/reasons, localize, and refine the drafted follow-up (chasing email, billing request, accountant note) by editing the anomaly's `draft` field directly — keeping ids and evidence intact.
4. Give the user the AirApp URL and send them to `#/anomalies`.

## Decisions And Execution Workflow

1. The user reviews at `#/anomalies`: approve, request changes (with a note), save an edited draft (revise), block, or dismiss. Decisions write directly onto the anomaly record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution_status: "ready_for_agent"` onto each approved anomaly with the concrete operation — `chase_receivable` (with the drafted email handoff), `reissue_invoice`, `flag_to_accountant` — and target document id). No external side effects either way.
3. The agent then performs the approved follow-ups outside the app (send the chasing email via the email skill, open the billing/accountant task) and records the real result on the anomaly (`execution_status: "executed"`, `execution_detail`). Executed anomalies still require the app or a follow-up decision to move to `done` — this script never flips the workflow status itself.

## Safety Defaults

- Treat every outbound message, ERP/bookkeeping mutation, refund, and credit-note change as approval-required via the anomaly queue.
- Use stable ids and natural-key upserts so repeated imports, checks, and executions are idempotent.
- Never expose secrets or full customer datasets through the settings view or logs; it shows column mappings and tolerance rules only.
- If the tables disagree in a way no rule covers, ask the user — do not invent corrections to make the books balance.

## Useful Commands

```bash
node skills/kelly-audit/scripts/import_tables.mjs --orders orders.csv --invoices invoices.csv --payments payments.csv --apply
node skills/kelly-audit/scripts/run_checks.mjs --apply
node skills/kelly-audit/scripts/execute_decisions.mjs
node skills/kelly-audit/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-audit/content/kelly-audit-app dev
```

In normal use, invoke `/kelly-audit`, let the skill import/check what's due, and open the AirApp.
