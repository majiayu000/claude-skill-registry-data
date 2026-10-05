---
name: padosoft-payments-reconciliation
description: >-
  Use this skill when money moves: a checkout or capture, a refund, a chargeback, a payout, a subscription
  renewal, a promotion or loyalty redemption, a usage or token bill. Also when the user reports that totals
  do not add up, that a customer was charged twice, that a refund exceeded the payment, that a payout cannot
  be tied to orders, that a promotion went over its cap, or that a payment request timed out and nobody
  knows whether it went through. It checks the state machine, the arithmetic that has to close, and the
  boundary between what the provider owns and what you own. Do not use it to integrate a specific provider's
  SDK, for PCI scope decisions, or for pricing and tax strategy.
license: MIT
compatibility: >-
  Provider-agnostic. Applies to card processors, wallets, stored value, subscriptions and metered usage; the
  arithmetic rules assume an exact integer type for minor units.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: Money is a ledger that has to balance, not a status field.
  profiles: payments
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: payments, refunds, chargebacks, payouts, settlement, idempotency, subscriptions, ledger, money
---

# Payments and reconciliation

A payment integration that parses correctly can still be **financially impossible**. These are the checks
that make the difference, and they are almost all about a number that has to close or a boundary that has to
stay closed.

**The rule: money is a ledger of immutable events that must balance, not a status field that gets updated.**

---

## 1. The arithmetic has to close

```text
captured − refunds − lost_chargebacks = net
```

Validating an order and a payment *independently* never detects drift between them. The settlement contract
links every refund and every chargeback to the **exact** payment, distinguishes a resolved effect from an
unresolved one, and proves the equation.

And validate the state machine, not just an inequality: `refunded_amount ≤ amount` happily allows a
"partially refunded" status with a zero refund, or a "not refunded" status with a positive one. Compare
successful refund amounts against the cumulative amount observed on the payment.

## 2. The four joins that look done and are not

| Looks like proof | Is not, because |
|---|---|
| A payout total equal to an order amount | equality is not inclusion. Persist the provider's source id at commit, then verify it appears in the payout's constituent ledger |
| A payout linked to a balance transaction | that says which provider records funded it, not which of **your** orders did, nor when the bank settled |
| An open or won dispute | exposure is not a loss. Only resolved-against outcomes are lost chargebacks; keep exposure separate from payout and fee accounting |
| A paid order | not shipped, not subscribed, not renewed. Fulfilment, subscriptions and disputes are separate lifecycles with their own states |

In all four, **reject incomplete pagination** before claiming a join. A partial page silently becomes a
missing record, and a missing record silently becomes a balanced equation.

## 3. A timeout is not a "no"

After a payment or order request times out, the side effect may already exist.

```text
❌  catch → mark not committed → retry
✅  catch → classify UNKNOWN → keep the approval claim → reconcile against authoritative state
```

Mapping every exception to "not committed" and retrying is how a single slow response becomes two charges.

## 4. Validate-and-commit is not atomicity

A promotion snapshot can be valid for two concurrent checkouts and still exceed its cap, because validation
and increment were two steps. Keep redemption idempotency **and** cap enforcement in one ledger transaction,
serialise by code, and expose exhaustion as its own outcome rather than a generic provider error — see
**`padosoft-atomic-invariants`**.

Cart pricing is stale by definition: re-check promotion validity **at commit**, not only when the cart was
priced.

## 5. Where the provider's authority ends

The provider owns payment state. You own carts, inventory, order ownership and the customer relationship. An
adapter maps authoritative provider responses and enforces idempotency; it does **not** become your commerce
layer, and a REST wrapper around it is not evidence of live checkout, webhooks or settlement.

- **Prove effects, not response shapes.** A provider can return a schema-valid order while charging twice or
  overselling. The contract needs a capability preflight and a journey that compares inventory before and
  after, checks the arithmetic invariants, and retries the **same** idempotency key expecting byte-equivalent
  state.
- **Refunds are their own journey**: strictly below the captured amount, same currency, same order identity,
  idempotent on retry.
- **A missing observer is `unsupported`; an inconsistent snapshot is `error`.** Neither is a successful
  checkout.
- **Read-only evidence first.** Reading a provider's state is the safe first boundary; mutating is the one
  that needs the protected environment.
- **Transport policy fails closed before the request leaves**, not after the response comes back.

## 6. Representation, or how the equation breaks without anybody lying

- **Minor units, exact integers.** Floating point and money do not share a representation. Compare in minor
  units with an exact type.
- **One currency per comparison**, and reject duplicate instruments in a split tender.
- **A canonical timezone for every financial timestamp.** A pricing effective date without an explicit
  instant means two deployments attach two different meanings to the same catalog.
- **A ledger, not a counter.** Loyalty points, credits and stored value reconcile from immutable idempotent
  transactions. A mutable balance cannot show a duplicate earn, and cannot stop a negative one.
- **A price change needs a history, not just a new value.** Consumer-facing price display is regulated in
  several markets: showing a discount requires being able to state the prior price over a defined window.
  That is a table of price events with their validity, written at the moment of the change — it cannot be
  reconstructed afterwards from the current value. Keep the pipeline explicit too: the source list, the
  queue of items to recompute, the staged prices that are not live yet, the live ones, and the history.
- **A margin, a markup or any derived commercial figure is computed server-side and is never an input from
  the interface.** It is arithmetic over values the server already holds, and accepting it from a form is
  accepting a number the customer chose.
- **Stored value has a temporal boundary**: *expired* carries an elapsed instant, and *active* must not
  carry an expiry already in the past.

## 7. Metered and usage billing

- **Enforce the budget on both sides of the call.** Charging only after a response permits an over-budget
  dispatch; checking only an estimate loses the authoritative usage. Estimate before, charge the reported
  amount after, and stop further calls when actual spend reaches the limit.
- **Exhaustion at charge time is also a budget event.** If the adapter raises without emitting it, the run
  loses the only durable signal that explains why it stopped.
- **Settle with pricing provenance**: the model or SKU, the authoritative counts, the actual charge and the
  identity of the price catalog. An expired reservation releases the estimate and must not pretend a usage
  event occurred.
- **A digest of the catalog proves reproducibility, not approval.** Sign it and verify against an
  out-of-band trust map before it is allowed to admit spend.

## 8. Cancellation and reversal

An accepted cancellation is not proof that money moved back. Keep *requested*, *accepted* and *rejected* as
distinct states with decision timing, and link an accepted cancellation of a paid order to a compensating
refund or void.

---

## Gotchas

- **Provider status strings are a vocabulary, not a state machine.** Enumerate the ones you accept and
  reject the rest; a new status must not silently take a default branch.
- **The webhook is not the source of truth, and neither is your database alone.** Reconcile.
- **Fixtures prove the equation and the linkage rules. They do not prove settlement** — that needs a live
  reconciliation journey against the provider. See **`padosoft-evidence-boundaries`**.
- **A test identifier built from a timestamp can look like a card number** to a data-protection filter and
  get rejected. Use deterministic semantic ids, and never weaken the redaction to make the fixture pass.
- **An approval that is not bound to the exact amount is not an approval.** Bind it to the customer, the
  cart revision and the total, consume it once, and re-check atomically at the mutation.

## Checklist

- [ ] `captured − refunds − lost_chargebacks = net` proven, with every effect linked to its exact payment
- [ ] Payment state machine validated explicitly, not by inequality
- [ ] Payout inclusion verified through the provider source id, not by amount equality
- [ ] Dispute exposure kept separate from settled loss; only resolved outcomes counted
- [ ] Fulfilment, subscriptions and disputes modelled as separate lifecycles
- [ ] Incomplete pagination rejected before any join is claimed
- [ ] Timeouts classified as unknown and reconciled, never retried blind
- [ ] Redemption idempotency and cap enforcement in one transaction, serialised by code
- [ ] Promotion validity re-checked at commit
- [ ] Minor units with an exact integer type; one currency; no duplicate instruments
- [ ] Financial timestamps canonical
- [ ] Balances derived from an immutable idempotent ledger
- [ ] Usage: budget enforced before **and** after; settlement carries pricing identity
- [ ] Cancellation linked to a compensating reversal

## Final report

```
Flow: <checkout | refund | payout | subscription | usage>
Equation: captured <…> − refunds <…> − lost chargebacks <…> = net <…>  → closes: yes | no
Joins verified: payment↔refund <…> · order↔payout <…> · pagination complete: yes | no
Idempotency: key <…> · scope <…> · retry returns equivalent state: yes | no
Unknown outcomes: <how a timeout is classified and reconciled>
Representation: minor units <type> · currency <…> · timestamps <canonical form>
Provider boundary: <what it owns> | <what we own>
Still unproven: <what needs a live reconciliation journey>
```
