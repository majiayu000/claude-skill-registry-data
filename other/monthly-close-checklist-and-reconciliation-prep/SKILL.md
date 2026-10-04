---
name: monthly-close-checklist-and-reconciliation-prep
description: "Turns a pasted bank export or transaction list into a monthly-close checklist, categorization draft with disputed flags, and an accountant/investor summary — no SaaS needed. Triggers: 'monthly close checklist', 'reconcile transactions', 'чек-лист месячного закрытия', 'сверь транзакции'."
version: 1.0.0
---

# Monthly Close Checklist and Reconciliation Prep

This skill turns a pasted transaction list or bank export (CSV rows or markdown table) plus a brief business context into three ready-to-use artifacts: a monthly-close checklist, a categorization draft with disputed flags, and an accountant/investor-ready summary — no accounting SaaS or integrations required.

**Input:**
- Transaction list: CSV rows or markdown table (minimum columns: date, counterparty/description, amount)
- Business context: entity type (ИП / ООО / sole-prop), primary currency, brief description of revenue model

**Output:**
- Artifact 1 — Monthly-Close Checklist (locale-adapted)
- Artifact 2 — Categorization Draft with Disputed Flags
- Artifact 3 — Accountant Snapshot + Investor Narrative

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that a transaction list is present in the user's message (CSV rows, markdown table, or plain list with date + counterparty + amount)
   - If no transaction list detected: **stop**. Return bilingual prompt:
     > "Для работы нужен список транзакций — вставьте CSV-строки или таблицу в формате Markdown. / I need a transaction list — paste CSV rows or a Markdown table."

2. Check that at least one parseable data row exists (not just headers or empty rows)
   - If zero data rows found: **stop**. Return in user's language:
     > "Список не содержит транзакций. Убедитесь, что данные включают хотя бы одну строку с датой, контрагентом и суммой. / The list contains no transactions. Include at least one row with date, counterparty, and amount."

3. Note any missing business context (entity type, currency, revenue model)
   - If absent: proceed with generic international defaults; note assumptions in the output preamble

### Step 2: Map Transaction Columns

1. Identify the date column (date-like values or headers: "date", "дата", "datum")
2. Identify the counterparty/description column (free text, merchant names, or descriptions)
3. Identify the amount column (numeric; note whether debit/credit are separate or a single signed column)
4. Identify the direction column (income/expense) if present; otherwise infer from amount sign

**Edge Case — Non-standard column names:**
- Attempt heuristic detection; list the detected column mapping in the output preamble
- Then ask the user to confirm the mapping before proceeding: "Пожалуйста, подтвердите, что колонки определены верно / Please confirm the detected column mapping is correct: [mapping table]. Reply 'yes' to continue or correct any column names."
- Do not generate the three artifacts until the user confirms or corrects the mapping

**Edge Case — Mixed currencies:**
- Process each currency separately
- Flag multi-currency rows in the Disputed section; add note: "FX conversion is out of scope"

### Step 3: Generate Categorization Draft and Flag Disputed Transactions

1. Scan counterparty names and descriptions to group transactions by pattern (recurring SaaS subscriptions, salary payouts, tax transfers, client payments)
2. Propose a draft category label for each group:
   - Income: Revenue/Consulting, Revenue/Product, Other Income
   - Expense: OPEX/Software, OPEX/Payroll, OPEX/Office, Tax, Transfer, Other
3. Mark a transaction as `⚠ DISPUTED` when:
   - Counterparty is ambiguous or matches no clear pattern
   - Amount is unusually large relative to others in the same group
   - Transaction direction cannot be determined from the data
4. Build the categorization table (see Output Format)

### Step 4: Generate Monthly-Close Checklist

1. Start with standard items for all entity types:
   - [ ] Verify bank balance matches internal records
   - [ ] Confirm all transactions are categorized (zero uncategorized rows)
   - [ ] Review and approve all `⚠ DISPUTED` items
   - [ ] Check outstanding receivables (unpaid invoices this month)
   - [ ] Check outstanding payables (bills due)
   - [ ] Confirm payroll is reflected in records
   - [ ] Verify tax payments and withholdings are current

2. Add locale-specific items based on entity type:
   - **ИП (Russia/CIS, УСН):**
     - [ ] Обновить КУДиР записями за месяц (колонка «Доходы» для УСН 6%)
     - [ ] Сверить остатки по банку с данными из личного кабинета
     - [ ] Проверить акт сверки с ключевыми контрагентами при наличии дебиторки
     - [ ] Уточнить срок авансового платежа (Q1: 28 апр, Q2: 28 июл, Q3: 28 окт)
   - **ООО (Russia/CIS):**
     - [ ] Проверить подотчётные суммы (авансовые отчёты сотрудников)
     - [ ] Подтвердить корректность записей по НДС (для плательщиков НДС)
   - **Sole-prop / EN default:**
     - [ ] Review mileage log or home-office deduction documentation
     - [ ] Confirm quarterly estimated tax payment is scheduled

3. Append 1–3 custom items derived from the most critical `⚠ DISPUTED` rows in Step 3
   (e.g., "Clarify [date] [counterparty] [amount] before handoff")

### Step 5: Generate Accountant Snapshot

1. Compute totals from the categorized table:
   - Total income by category; total expenses by category; net cash flow (income − expenses)
2. List all `⚠ DISPUTED` items (date, counterparty, amount, reason for flag)
3. List open questions for ambiguous categorization (formulate as clear yes/no or clarification questions)

### Step 6: Generate Investor Narrative

1. Write a 3–5 sentence plain-language narrative covering:
   - Revenue for the month (and MoM trend if prior context was provided)
   - Cash position after expenses
   - 1–2 key risks or open items (e.g., large disputed transaction, delayed receivable)
2. Keep language accessible to a non-accountant reader — no formulas, no accounting jargon
3. One paragraph only

---

## Negative Cases

- **No transaction list provided:** Stop. Return bilingual prompt (Step 1).
- **Zero parseable rows:** Stop. Return bilingual message (Step 1).
- **User requests SaaS integration (1С, QuickBooks, Xero, etc.):** Decline. State: "Этот скил работает только с вставленными данными и не подключается к внешним системам. / This skill works only with pasted data and does not connect to external systems."
- **List >200 rows:** Process all rows for categorization; produce aggregate totals in investor narrative; note total row count in preamble.

---

## Output Format

Single markdown response with three artifact sections plus an optional preamble:

```
> **Assumptions / Допущения:** [column mapping notes, missing-context defaults, currency split if applicable]

---

## Чек-лист месячного закрытия / Monthly-Close Checklist
**Период / Period:** [Month YYYY]
**Тип субъекта / Entity type:** [ИП / ООО / Sole-prop / Unknown]

- [ ] Item 1
- [ ] Item 2

---

## Правила категоризации / Categorization Draft
| Дата / Date | Контрагент / Counterparty | Сумма / Amount | Категория / Category | Статус / Status |
|---|---|---|---|---|
| YYYY-MM-DD | Name | +/- amount [CCY] | Category/Subcategory | ✅ / ⚠ DISPUTED |

> Спорных транзакций / Disputed: [N]. Отметьте их перед передачей бухгалтеру / Review before handoff.

---

## Резюме для бухгалтера / Accountant Snapshot
**Период / Period:** [Month YYYY]
**Доходы / Income:** [total] | **Расходы / Expenses:** [total] | **Нетто / Net:** [net]

**По категориям / By category:**
| Категория / Category | Сумма / Amount |
|---|---|
| Revenue/Consulting | + |

**Спорные позиции / Disputed items:**
- YYYY-MM-DD | [Counterparty] | [Amount] — [reason]

**Открытые вопросы / Open questions:**
1. [Question for accountant]

---

## Резюме для инвестора / Investor Narrative
[3–5 sentence plain-language paragraph: revenue, cash position, 1–2 key risks]
```

**Formatting rules:**
- All four section headers are bilingual (RU / EN) regardless of detected language
- Body text (list items, table cells, narrative) is in the detected user language
- `⚠ DISPUTED` tag is always in English as a universal visual signal
- Net cash flow = total income − total expenses derived from the categorized table
