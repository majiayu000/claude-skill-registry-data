---
name: wengz-credits-payments
description: Changes Wengz credits, packages, subscriptions, payment proofs, provider wallet, withdrawals, or finance settings. Use when touching credit-logic, subscription/payment routers, free trial, settleCompletedRequest, or admin finance.
---

# Wengz credits, payments, and wallet

## Prerequisites

- Business: `docs/ADVANCED_BUSINESS.md` §§ Commercial model, Provider earnings, Client journey steps 6–9 / 14.
- Technical: `docs/ADVANCED_TECHNICAL.md` (cron release holds, env).

## Client money path

1. **Free trial** — `assignFreeClientSubscription` on client approve (`free-client-subscription.ts`). Once per user (`isFreeTrialUsed`). Silent no-op if free package missing — surface errors if changing that behavior.
2. **Subscribe paid** — `subscription.subscribe` → **inactive** sub; old active plan stays spendable until proof approved.
3. **Proof** — `payment.submitProof` (USD amount = package price; ≤10MB image). Bank / InstaPay only.
4. **Approve** — `payment.approvePayment` (FM/SA): CAS proof, deactivate other actives, activate paid, reset period; **does not** carry leftover credits from old plan.
5. **Reject** — cancel that pending sub only.
6. **Spend** — `checkAndDeductCredits` / revision paid path: `isActive` + `endDate >= now` + package service scope.

## Provider money path

1. Client/staff approve delivered → `settleCompletedRequest` → ledger **HOLD** + wallet held balances.
2. Cron `release-provider-holds` → available after 7 days.
3. Withdraw / dispute → FM/SA review with proof (`provider-wallet.ts`, admin finance).

## Invariants

| Rule                                | Enforcement                                    |
| ----------------------------------- | ---------------------------------------------- |
| No spend on unpaid (inactive) sub   | credit-logic / create-request                  |
| File/voice attributes add 0 credits | attribute-validation                           |
| Settlement ≠ package price          | finance-settings credit USD price              |
| No automatic payout gateway         | manual FM/SA                                   |
| `addCredits` unused                 | do not invent refunds without product decision |

## Checklist

- [ ] Correct procedure: `clientProcedure` vs `financeManagerProcedure`.
- [ ] Invalidate subscription cache when activating/cancelling when helpers exist.
- [ ] Notify client with recipient locale.
- [ ] Update business doc if money rules change.

Related: `.cursor/skills/wengz-domain-workflows/SKILL.md`
