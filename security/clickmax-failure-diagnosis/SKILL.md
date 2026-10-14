---
name: clickmax-failure-diagnosis
description: Use when the seller asks why their sales/transactions are failing or being declined, wants failed payments grouped by reason, or wants the recoverable value and next action per failure reason in Clickmax.
---

## When this applies

Use this skill when the seller wants to understand WHY transactions fail and what to do about it: failures grouped by reason, recoverable value per reason, and the recommended next action.

Not this skill:

- headline KPIs / paginated dashboard browsing / generic loss cohorts -> `clickmax-payments-dashboard-analysis`
- inspecting or refunding a specific transaction -> `clickmax-transaction-operations`
- **accrued platform-fee debt** -> `transactions_debt` (this is money the seller owes the platform, NOT a failed sale; never use it for failure diagnosis)

## Key assumptions

- `transactions_failure_breakdown` already aggregates FAILED transactions into stable `code` buckets with `count`, recoverable `value`, and `isPlatformFault`, sorted by value.
- `code` is a stable category derived from the gateway's free-text reason; `rawReasons` holds the original strings that fell into each bucket.
- `unknown` means the gateway reason did not match a known pattern — lean on `rawReasons` to describe it.
- `value` mirrors the dashboard's failed-value semantics; render it as currency, do not re-scale it against other tools.
- `count`/`value` are per ATTEMPT: one buyer retrying N times counts N → say "tentativas", never "pessoas"; the deduplicated recoverable total is `recovery_recoverable_revenue`, not the sum of this breakdown.

## Thought process

1. If the seller asks "why are my sales failing?" (or similar), call `transactions_failure_breakdown`. It defaults to the last 30 days; pass `from`/`to` only when the seller names a different window, and state the assumed period in the answer.
2. Translate each `code` into user-facing text and a next action (map below); never surface the raw `code`.
3. Rank by recoverable `value`, lead with the biggest lever, and separate "act differently" faults from legitimate bank declines.

## Execute guide

- For the failure diagnosis, use `mcp__plugin_clickmax_clickmax__transactions_failure_breakdown`. Pass `from`/`to` (ISO date-time) only when the seller named a window; pass `projectIds`/`productIds`/`offerIds` only when they narrowed scope.
- To drill into a single failing sale the seller points at, use `mcp__plugin_clickmax_clickmax__sales_get_details` or `mcp__plugin_clickmax_clickmax__transactions_get`; do NOT paginate `mcp__plugin_clickmax_clickmax__dashboard_my_sales` just to re-count failures the breakdown already aggregated. When you do need the failing ROWS, pass `includeAggregations: false`.
- Never call `transactions_debt` here — it returns platform-fee debt, not failures.

### Failure `code` → user text + next action

Translate the tool's `code` into the seller's language (PT example / EN example) and pair it with the action. `isPlatformFault: true` marks a bug on our side (only `integration_error` today).

|`code`|Label (PT / EN)|Next action|
|-|-|-|
|`card_declined`|Cartão recusado pelo banco / Card declined by bank|Ofereça Pix ou boleto; peça outro cartão|
|`insufficient_funds`|Saldo insuficiente / Insufficient funds|Ofereça Pix/boleto ou parcelamento|
|`invalid_cvv`|CVV inválido / Invalid security code|Peça para revisar o código de segurança|
|`expired_card`|Cartão expirado / Expired card|Peça um cartão válido|
|`card_data_error`|Dados do cartão incorretos / Invalid card data|Peça para reconferir número/dados do cartão|
|`auth_3ds`|Falha na autenticação 3DS / 3DS authentication failed|Oriente concluir a verificação do banco (3DS)|
|`fraud_suspected`|Bloqueio antifraude / Blocked by fraud check|Revise o pedido; se legítimo, oriente contato com o banco|
|`integration_error`|Erro de integração / Integration error|É bug nosso — encaminhe ao suporte|
|`unknown`|Motivo não classificado / Unclassified reason|Descreva a partir de `rawReasons`|

## Report

- Open with the period assumed and the total failed count + recoverable value.
- Result is a **diagnostic ranking**. The runtime renders presentation cards: emit a `cx-ranking` (boxed) with one row per failure reason, ordered by recoverable value, each row's `hint` set to the recommended next action.
- **Money color rule (see presentation contract):** a failed sale is recoverable money (retryable / winnable back), not a consummated loss, so **every** reason row is `tone="warning"` (yellow) — the chart is yellow end to end, never red. Differentiate the platform-fault case (`isPlatformFault`) via the `hint`/action text ("é bug, encaminhe ao suporte"), NOT by changing the tone.
- Translate every `code` to user text (map above); never print the raw `code`. Format `value` as currency.
- If the breakdown was computed over a limited window, add a `cx-note` (`variant="info"`) stating the period premise.
- Cap long lists with `+N more`. Treat any recovery follow-up (campaign, message) as opt-in only.

## Warnings

- `transactions_debt` is platform-fee debt, not failed sales — do not mix it in.
- `value` is recoverable money (winnable back via action, but not in the pocket) — so it reads yellow (`warning`) per the money-color rule, not red (that is for consummated losses like refunds/chargebacks); describe it as "recuperável".
- Never expose the raw failure `code`, UUIDs, or raw tool payloads.

## Anti-patterns

- Paginating `dashboard_my_sales` to hand-count failures the breakdown already aggregated (`dashboard_my_sales_aggregations` returns the same counts in one call).
- Coloring failure rows `negative` (red) or leaving them neutral — failures are recoverable, so all rows are `warning` (yellow); red is only for consummated losses.
- Dumping `rawReasons` verbatim instead of synthesizing a labeled reason.

---

Clickmax skill revision: `b8294822a4d6`
