---
name: freelance-financials
description: Freelance financial planner — tax/VAT, cash flow, emergency fund, retirement from irregular income. Free-first ERPNext.
personas:
  - FREELANCE
  - FINOPS
triggers:
  - freelance financials
  - ضريبة
  - cash flow
  - تدفق نقدي
  - savings
  - تقاعد
  - تخطيط مالي
tech_stack:
  - frappe/erpnext
  - invoiceninja/invoiceninja
  - lago/getlago

---
[SKILL] freelance-financials
[OBJ] Turn irregular freelance income into a stable financial plan — estimate tax/VAT, project cash flow, build an emergency fund, and plan retirement.

[RULES]
1. [REQ] Income smoothing: average last 6-12 months, build a "base salary" drawn monthly from a holding account; surplus = taxes + savings + profit.
2. [REQ] Tax/VAT: estimate obligation by jurisdiction (e.g., US quarterly est. tax; EU/VAT; KSA/ZATCA; UAE corporate tax thresholds). Set aside % per invoice via `invoice-manager`.
3. [CMD] Context7 IDs: `frappe/erpnext` (DocType/accounts, Arabic VAT), `invoiceninja/invoiceninja` (income tracking), `lago/getlago` (recurring/subscription revenue).
4. [REQ] Free-first: ERPNext (GPL, self-host) for books; InvoiceNinja for invoicing; spreadsheets as fallback. Paid (QuickBooks/Xero) only as parity.
5. [REQ] Cash flow projection: 13-week rolling forecast; flag low-balance weeks; tie to `pricing-strategy` targets from `pricing_calculator`.
6. [REQ] Emergency fund: 3-6 months of base expenses in liquid account before aggressive investing.
7. [REQ] Retirement: allocate % of profit to tax-advantaged/personal vehicle; model compounding. Independent of employer plans.
8. [REQ] Arabic/RTL: for MENA, model ZATCA/VAT filings, local pension (Saudi/GOSI optional), SAR accounts; RTL statements per `arabic-freelance`.
9. [REQ] Reserves split (example): 30% tax, 10% emergency, 10% retirement, 50% living/profit. Adjust by jurisdiction.
10. [REQ] Reporting: monthly P&L + quarterly tax preview; feed `marketing-analytics` CAC/LTV for business decisions.

[PROHIBIT]
1. No personal/business fund commingling.
2. No missed statutory tax/VAT deadline.
3. No treating gross revenue as spendable income.
4. No Arabic jurisdiction filing without local compliance review.
