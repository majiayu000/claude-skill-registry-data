---
name: invoice-manager
description: Create quotes/invoices, track payments, and manage multi-currency billing for freelancers. Models the Client→Invoice→Payment lifecycle from invoiceninja. Free-first, RTL-aware.
personas:
  - FREELANCE
  - FINOPS
triggers:
  - invoice manager
  - invoice
  - فاتورة
  - quotation
  - payment tracking
tech_stack:
  - invoiceninja/invoiceninja

---
[SKILL] invoice-manager
[OBJ] Generate client-ready quotations and invoices, track payment status, and reconcile multi-currency earnings. Model the lifecycle as Client → Invoice → Payment, mirroring invoiceninja's entity graph, so every invoice traces to a client and every payment to an invoice.

[RULES]
1. [REQ] Entity model: always anchor an Invoice to a Client (name, email, currency, locale). A Payment references an Invoice; never record income without a linked invoice.
2. [REQ] Quotation → Invoice: a quotation is a draft offer; on acceptance convert it to an Invoice with line items (description, qty, unit price, tax), due date, and payment terms.
3. [CMD] Context7 IDs: `invoiceninja/invoiceninja` — extract the Client→Invoice→Payment entity model, recurring invoices, and multi-currency handling.
4. [REQ] Multi-currency: support USD, SAR, AED, EGP (Arabic-platform clients). Store the invoice currency; show the USD-equivalent using a configurable rate. Never hardcode a rate — ask or read from config.
5. [REQ] RTL Arabic invoices: when client locale is ar, render dir="rtl", Arabic labels (فاتورة / عميل / المبلغ / تاريخ الاستحقاق), and Arabic or Western numerals per preference.
6. [REQ] Payment tracking: record status (draft/sent/paid/overdue/partial), send reminders for overdue, and reconcile against received payments. Keep a running aging report.
7. [REQ] Free-first: Invoice Ninja (free self-host / free tier) is the default engine; closed billing tools only as parity.
8. [REQ] Storage: persist clients/invoices/payments via `StorageFactory`; never log client PII or payment credentials.

[PROHIBIT]
1. No sending an invoice or marking a payment received without explicit user approval.
2. No fabricating payment records or balances to mask overdue accounts.
3. No storing card/bank credentials or PII outside the approved storage backend.
