---
name: clickmax-transaction-operations
description: Use when the user wants to inspect transactions or sales, read transaction charts, or refund a transaction in Clickmax.
---

## When this applies

Use this skill for seller-side transaction and sale operations: inspect a transaction/sale, chart transaction activity, read sale buyer/UTM details, or refund a transaction.

Not this skill:

- recurring subscriptions -> `clickmax-seller-subscriptions`
- SaaS workspace billing/plans/cards -> payment billing skills

## Key assumptions

- transaction and sale are related but distinct records
- external-sale details are gateway/provider-specific and should not be merged into native transaction semantics without saying so
- status, UTM, and provider fields answer different questions: payment state, attribution, and gateway traceability
- refund is permanent, reasoned, and always targets exactly one transaction; there is no product-scoped or cohort-scoped refund
- refunding a cohort means one confirmed call per transaction, so the count of transactions matters before starting
- debt is current accrued platform-fee debt, not all-time historical accounting
- `id` means a DIFFERENT id-space per tool, and there is no conversion tool between them: on `transactions_get`/`transactions_refund` it is the TRANSACTION id (route `/transactions/{id}`); on `sales_get_details`/`sales_get_buyer`/`sales_get_utms` it is the SALE id (route `/sales/{id}`); on `sales_get_external_details` it is a THIRD, external-sale id (route `/sales/external/{id}`). Never reuse one id across these tools assuming it's the same entity.

## Thought process

1. Distinguish inspection from refund mutation.
2. Identify whether the user needs transaction-level or sale-level detail.
3. Confirm any refund path unless the intent is already explicit and unambiguous.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__transactions_list` to list transactions by cohort. Pass pagination plus the exact filters the user asked for, such as `transactionStatus`, `productIds`, and `transactionPeriod.from/to`.
- For a paid-sales slice, prefer `transactionStatus = ['paid']` and restrict the date window explicitly.
- Use `mcp__plugin_clickmax_clickmax__transactions_get` when the user starts from a transaction id and needs the transaction record itself.
- Inspect one sale with `mcp__plugin_clickmax_clickmax__sales_get_details`, then add `mcp__plugin_clickmax_clickmax__sales_get_buyer` for buyer identity/context and `mcp__plugin_clickmax_clickmax__sales_get_utms` for attribution context.
- Use `mcp__plugin_clickmax_clickmax__sales_get_external_details` when the user needs provider-facing or external sale detail beyond the main sale record.
- Read debt with `mcp__plugin_clickmax_clickmax__transactions_debt` when the user asks about current platform-fee debt.
- Read chart trends with `mcp__plugin_clickmax_clickmax__transactions_chart` when the user asks for transaction volume or movement over time.
- Refund: use `mcp__plugin_clickmax_clickmax__transactions_refund` with the exact transaction id, a valid cancellation reason, and a short description when needed.
- When the user describes a cohort instead of one transaction, resolve it with `mcp__plugin_clickmax_clickmax__transactions_list` first, report how many transactions and how much money it covers, and confirm before refunding any of them.

## Report

- For reads: summarize the commercial answer, not raw accounting internals.
- For refunds: report what was refunded, what else was affected, and any failures/skips.

## Warnings

- Do not confuse seller transaction refunds with SaaS billing changes.
- A refund cannot be undone; a wrong transaction id costs real money.

## Anti-patterns

- Refunding based on fuzzy product matching without confirming the exact transactions.
- Treating sale buyer/UTM helpers as the canonical transaction object.

---

Clickmax skill revision: `b8294822a4d6`
