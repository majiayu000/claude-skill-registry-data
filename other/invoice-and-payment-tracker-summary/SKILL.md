---
name: invoice-and-payment-tracker-summary
description: "Build an invoice aging summary from a pasted invoice list: paid/overdue classification, aging buckets, per-client reconciliation, and needs-action list. No SaaS needed. Triggers: 'invoice aging summary', 'who owes me money', 'aging-сводка по счетам', 'кто из клиентов не заплатил'."
version: 1.0.0
---

# Invoice & Payment Tracker Summary

This skill assembles an invoice aging summary from a pasted list of invoices or payments. It classifies each invoice by payment status, calculates overdue aging, builds a per-client reconciliation cross-section, and generates a prioritised "needs action" list — with no accounting SaaS or integrations required.

**Input:**
- Pasted invoice or payment list (markdown table, CSV, plain text list, or free-form)
- Optional: payment terms (default: net 30), report date, currency label

**Output:**
- Single markdown document with three sections: Aging Summary / Per-Client Reconciliation / Needs Action

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user has pasted a list of invoices or payments.
   - If input is empty or contains only whitespace: stop and respond: "Вставь список счетов (номер, клиент, дата, сумма, статус). / Paste your invoice list (invoice #, client, date, amount, status)."
   - If input looks like a bank statement (contains debit/credit/transaction columns): stop and respond: "Это банковская выгрузка, а не список счетов. Для анализа банковских транзакций используй скилл monthly-close-checklist. / This looks like a bank statement. For transaction analysis, use the monthly-close-checklist skill."
   - If the user asks to write a reminder letter or dunning message: redirect: "Этот скилл составляет сводку, а не письма-напоминания. Для серии напоминаний используй accounts-receivable-followup-writer. / This skill builds a status summary, not reminder messages. For a reminder sequence, use accounts-receivable-followup-writer."

2. Identify the report date (use today's date if not provided).

### Step 2: Parse Columns and Confirm Mapping

1. Identify columns or fields in the input. Look for: Invoice #, Client Name, Invoice Date, Due Date, Amount, Paid Amount or Status.
2. If column headers are clear and standard: proceed directly to Step 3.
3. If headers are ambiguous, missing, or non-standard (e.g., "Контрагент", "Сумма к оплате", "Дата оплаты"):
   - Present a mapping confirmation:
     > "Я вижу следующие поля: [col1] → Invoice #, [col2] → Client, [col3] → Amount. Верно? / I see these fields: [col1] → Invoice #, [col2] → Client, [col3] → Amount. Correct?"
   - Wait for user confirmation before proceeding. Do not generate output until mapping is confirmed.

**Edge Case — EC5 (Mixed-language input):** If input contains mixed EN and RU (e.g., Russian client names with English amounts), detect the dominant language of headers and use it to determine output language; preserve original values as-is.

### Step 3: Classify Each Invoice

For each invoice, assign one of four statuses:

| Status | Condition |
|--------|-----------|
| **Paid** | Paid amount equals total amount |
| **Partially Paid** | Paid amount > 0 but less than total amount |
| **Overdue** | Due date has passed AND balance > 0 (or paid amount = 0 and due date has passed) |
| **Current** | Due date is in the future AND not yet paid |

**Edge Case — EC1 (No due date):** If due date is absent, calculate as: Invoice Date + 30 days. Add a note: "Due date assumed: invoice date + net 30. Provide due dates for exact calculations."

**Edge Case — EC2 (Partial payment):** Show paid amount, remaining balance, and days since partial payment (calculated as: Report Date − date of last known payment, if available; otherwise omit) in the per-client reconciliation section. Add a "Days Since Payment" column to that client's table only if the input contains a payment date field; if not available, note "(payment date not provided)" next to the balance.

### Step 4: Calculate Aging

1. For each **Overdue** invoice, calculate Days Overdue = Report Date − Due Date (in calendar days).
2. Assign to an aging bucket:

| Bucket | Days Overdue |
|--------|-------------|
| 0–30 days | 1–30 |
| 31–60 days | 31–60 |
| 61–90 days | 61–90 |
| 90+ days | 91 and above |

3. For **Paid**, **Partially Paid**, and **Current** invoices, leave Days Overdue and Bucket as "—".

**Edge Case — EC3 (Multiple currencies):** Process all rows. Group per-client totals by currency. Add note: "Cross-currency totals omitted — currencies cannot be aggregated without an exchange rate."

**Edge Case — EC4 (Large list, 50+ invoices):** Process all invoices. Add an executive summary card at the top of the output: total outstanding, bucket distribution (count and amount per bucket), top 3 overdue clients by balance.

### Step 5: Generate Aging Summary Table

Build a table with all invoices, one row per invoice:

| Column | Source |
|--------|--------|
| Invoice # | From input |
| Client | From input |
| Invoice Date | From input |
| Due Date | From input or calculated (EC1) |
| Amount | From input |
| Paid | From input (0 if not provided) |
| Balance | Amount − Paid |
| Status | Assigned in Step 3 |
| Days Overdue | Calculated in Step 4 (or —) |
| Bucket | Assigned in Step 4 (or —) |

Sort the table: Overdue (90+ first) → Overdue (61–90) → Overdue (31–60) → Overdue (0–30) → Partially Paid → Current → Paid.

### Step 6: Generate Per-Client Reconciliation

For each unique client in the input:
1. Create a subsection: `### [Client Name]`
2. List all invoices for that client in a table (Invoice #, Date, Amount, Paid, Balance, Status).
   - **EC2:** If any invoice for this client is "Partially Paid" and the input includes a payment date field, add a "Days Since Payment" column (Report Date − payment date). If payment date is not in the input, add a note "(payment date not provided)" next to the Partially Paid balance row.
3. Add a **Total outstanding** line at the bottom of each client section.
4. If the client has no outstanding balance (all invoices Paid): include the subsection and note "(All invoices paid)".

### Step 7: Generate Needs Action List

1. Collect all **Overdue** and **Partially Paid** invoices.
2. Sort by priority: highest days overdue first; within the same aging bucket, sort by largest balance first.
3. Output as a numbered list:
   > 1. **[Client] — [Balance] overdue [N] days** (Bucket: [bucket])
4. If no overdue invoices exist: note "✓ No overdue invoices."

### Step 8: Assemble and Output

Combine the three sections into a single markdown document using the Output Format template below. Output language must match the user's input language: English uses English section headers; Russian uses Russian section headers (see Output Format).

---

## Negative Cases

- **Empty or whitespace input:** Stop. Respond with bilingual prompt listing required fields (see Step 1).
- **Bank statement detected:** Stop. Redirect to monthly-close-checklist skill (see Step 1).
- **Request to write reminder letters:** Redirect to accounts-receivable-followup-writer skill (see Step 1).

---

## Output Format

Single markdown document with three sections:

```markdown
# Invoice & Payment Status Summary
**Report Date:** [date]
**Total Invoices:** [N] | **Total Outstanding:** [amount]

> [Executive summary card — only for 50+ invoices: bucket distribution + top 3 overdue clients]
> [Assumption note if due dates were calculated — only if EC1 applied]

---

## Aging Summary

| Invoice # | Client | Invoice Date | Due Date | Amount | Paid | Balance | Status | Days Overdue | Bucket |
|-----------|--------|--------------|----------|--------|------|---------|--------|--------------|--------|
| INV-001 | Acme Corp | 2026-04-01 | 2026-05-01 | $5,000 | $0 | $5,000 | Overdue | 52 | 31–60 days |
| INV-002 | Beta LLC | 2026-05-10 | 2026-06-10 | $2,000 | $2,000 | $0 | Paid | — | — |

---

## Per-Client Reconciliation

### Acme Corp
| Invoice # | Date | Amount | Paid | Balance | Status |
|-----------|------|--------|------|---------|--------|
| INV-001 | 2026-04-01 | $5,000 | $0 | $5,000 | Overdue 52d |

**Total outstanding: $5,000**

---

### Beta LLC
| Invoice # | Date | Amount | Paid | Balance | Status |
|-----------|------|--------|------|---------|--------|
| INV-002 | 2026-05-10 | $2,000 | $2,000 | $0 | Paid |

*(All invoices paid)*

---

## Needs Action

1. **Acme Corp — $5,000 overdue 52 days** (Bucket: 31–60 days)
```

**Russian variant** uses these section headers:
- `# Сводка по счетам и платежам`
- `## Таблица старения задолженности`
- `## Акт сверки по клиентам`
- `## Требует внимания`

Output is copy-paste ready — no meta-commentary between sections. All notes (EC1 assumption, EC3 currency warning) appear in a blockquote at the top, not inline in tables.
