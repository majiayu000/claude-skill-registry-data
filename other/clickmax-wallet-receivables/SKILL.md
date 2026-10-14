---
name: clickmax-wallet-receivables
description: Use when the user asks if they are ready to sell/receive, about the Clickmax wallet ("Carteira"), bank/receiving account approval, balances, "a receber", receivables, statement/extrato, or withdrawals (saques).
---

## When this applies

Use this skill for seller financial readiness and wallet questions: whether the seller can sell and receive, bank/receiving-account approval, available/pending/"a receber"/anticipatable balances, the wallet statement (extrato), and withdrawal (saque) history.

Not this skill:

- sales/subscription KPIs and revenue analysis -> `clickmax-payments-dashboard-analysis`
- refund/transaction mutations -> `clickmax-transaction-operations`

## Key assumptions

- Clickmax processes payments natively; there is NO external gateway (Stripe, PayPal, Mercado Pago, etc.) to configure to receive sales — never suggest one
- "ready to sell and receive" = `sellerStatus: enabled` AND `bankAccountStatus: approved`
- balances and "a receber" come from the wallet statement, not the sales dashboard
- raw bank account numbers, pix keys, ids, and transaction hashes are never surfaced to the user

## Thought process

1. If the user asks whether they can start selling/receiving, read seller status first.
2. If they ask about money in the wallet (saldo, a receber, antecipável, extrato), read the statement.
3. If they ask about cashouts, read withdrawals.

## Execute guide

- For "am I ready to sell/receive" or "are my bank details approved", use `mcp__plugin_clickmax_clickmax__sellers_status` and interpret:
  - `sellerStatus: enabled` + `bankAccountStatus: approved` -> ready to sell and receive
  - `pending` / `pending_correction` -> still under review; explain the `reason` and point to completing or correcting data in the wallet ("Carteira")
  - `reproved` / `blocked` / `disabled` -> blocked; explain the `reason` and the wallet correction step
- For balances and movement history (saldo disponível, a receber, em análise, antecipável, extrato), use `mcp__plugin_clickmax_clickmax__wallet_statement`; use `page`/`perPage` to browse.
- For withdrawal/cashout history (saques), use `mcp__plugin_clickmax_clickmax__wallet_withdraws`.

## Report

- Lead with the direct answer: ready or not, and the single blocker if any.
- Present money as amounts only; never expose bank account numbers, pix keys, ids, or hashes.
- For balances, separate available vs pending ("a receber") vs anticipatable.

## Warnings

- Never recommend or imply an external payment gateway/checkout to receive sales; Clickmax handles checkout and payment natively.
- A pending/reproved status is resolved in the Clickmax wallet/account setup, never by integrating a third party.

## Anti-patterns

- Suggesting Stripe or any external integrator for receiving sales.
- Reading the sales dashboard to answer wallet balance / "a receber" questions.
- Surfacing raw bank account, pix, ids, or transaction hashes.

---

Clickmax skill revision: `b8294822a4d6`
