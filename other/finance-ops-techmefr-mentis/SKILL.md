---
name: finance-ops
description: Use when setting up or reviewing the company's own financial operations (expense approval, invoicing, budgeting). Building a payment or ledger product is business/fintech-compliance.
---

# finance-ops

Business layer (`business/README.md`). Distinct from `business/fintech-compliance`: that block is
engineering invariants for a *product* that moves other people's money (a ledger, a payment flow); this
one is the structural discipline around the company's *own* financial operations — who can approve
what, how invoicing gets chased, how a budget gets tracked. Same honesty posture as the rest of this
layer: not accounting or tax advice.

## When
Setting up or reviewing who can approve an expense or a payment, how invoices/receivables are tracked,
or how spend against a budget is monitored.

## Steps

### 1. Separation of duties: the core control
1. **The person who requests or benefits from a spend never also approves it.** This is the single
   highest-value control against both error and fraud — not because any specific person is suspected,
   but because a control that depends on one person's honesty rather than on a structural check is a
   control that fails exactly when honesty does.
2. **The person who approves a transaction is not the same person who reconciles or reviews it
   afterwards.** Approval and review are two different checks; collapsing them into one person removes
   the second check entirely.
3. **A small team can't fully separate duties, and that's expected — use compensating controls instead
   of pretending the separation exists.** A founder/owner personally reviewing bank and card statements
   monthly, requiring a second signature above a stated amount, or rotating who handles a given process
   periodically all substitute for headcount the team doesn't have. Don't skip the control because the
   textbook version needs more people than exist.
4. **Detection is faster with the control in place than a post-hoc audit relies on**: organisations with
   real separation-of-duties controls catch discrepancies materially faster than those without, which
   directly caps how large a problem gets before it's noticed. *Re-read before relying: the fraud survey
   that would support this figure could not be read on 2026-10-20 (the file exceeded the fetch limit), so
   this sentence is unsourced.*
5. **Separate authority, custody and accounting, and expect limits.** The US federal internal-control
   standard (Green Book, paragraphs 10.12 to 10.14, read 2026-10-20) says management considers splitting
   authority, custody and accounting so no one person controls a whole transaction; where that is not
   practical because of limited staff, it designs alternative controls; and separation reduces but cannot
   remove the risk of managers overriding controls, nor of collusion between two people. Symptom: one
   person who approves, pays and reconciles. Fix: a named alternative control (for example an owner reviewing
   statements, a second signature above an amount), and say that it is weaker than separation. A US federal
   reference, used for the principle only.

### 2. Invoicing and receivables
1. **An invoice has a stated due date and payment terms from the moment it's sent**, not an implicit
   "whenever." Ambiguity here is what turns into a slow-payer problem later. Jurisdiction example only: the
   French business-service page read 2026-10-20 says a French invoice must show the payment due date, the
   early-payment discount terms or a statement that there are none, the late-payment penalty rate, and the
   fixed 40 euro recovery indemnity owed by a professional customer who pays late, with penalties due
   without a reminder; the maximum payment delay was not found on the pages read. Other countries differ:
   ask whoever owns finance.
2. **Overdue receivables are tracked and chased on a schedule**, not noticed when cashflow gets tight.
   A simple aging view (current / 30 / 60 / 90+ days overdue) surfaces the problem while it's still
   small.
3. **A recurring late payer is a decision to make explicitly** (stricter terms, upfront deposit,
   involving someone senior) rather than an accepted pattern nobody has actually decided to accept.

### 3. Budgeting and spend visibility
1. **A budget is a tracked commitment, not a document written once and revisited at year-end.** Spend
   against it reviewed on a cadence (monthly is common) catches an overrun early enough to act on it,
   rather than as a year-end surprise.
2. **Every recurring spend (subscriptions, contracts) has a named owner** who can say why it exists and
   whether it's still needed — an unowned recurring charge is how a company keeps paying for a tool
   nobody uses.
3. **A one-off spend above a stated threshold gets the same "requester ≠ approver" check as routine
   expenses** — a threshold exists precisely so a large exception doesn't slip through because it felt
   too unusual for the normal process to apply.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a stated separation
between who requests/benefits from a spend and who approves it (or a named compensating control where
headcount doesn't allow real separation), an aging view of receivables reviewed on a schedule, and a
named owner per recurring spend with budget tracked against actuals on a cadence.

## Guardrails
- Never let the same person both request/benefit from and approve the same transaction, without an
  explicit compensating control replacing that check.
- Never let an overdue invoice go unchased until cashflow makes it urgent — track on a schedule, not on
  pressure.
- Never leave a recurring subscription/contract with no named owner.
- This block has no dedicated in-house finance/accounting expertise behind it yet: a solid set of
  structural defaults, not proven doctrine, and not accounting or tax advice — a real bookkeeper or
  controller's judgement outranks it without discussion.

## Origin
**Sourcing pass 2026-10-20 (status stays 🟡, nothing was run).** Read for facts, own words: the US federal
internal-control standard (a US government publication; section 10 on segregation of duties; the PDF text was
extracted locally), a French business-service page on invoice mentions, a small-business agency page on
budgeting and receivables, and a COSO page. Confirmed: the separation-of-duties principle (step 1.1 to 1.3)
including the alternative-control case for small teams. Added: the limits of separation (override, collusion)
and the French invoice-mention example. Not found: any source for the faster-detection claim (1.4, now
marked), for aging buckets or for a budget review cadence (the agency page gave only generic tracking
advice and the COSO page did not name the framework components); those stay own guidance. The French payment
delay page returned the wrong content and the commercial-code article could not be opened.

Assembled from public sources, written without internal finance/accounting expertise. Separation of
duties (requester ≠ approver ≠ reviewer, compensating controls for small teams, faster fraud detection
with the control in place): published internal-controls guidance aimed at small businesses and
nonprofits, where the headcount-constrained case is explicitly addressed rather than assumed away.
Invoicing/receivables aging and budget-as-tracked-commitment: general financial-operations practice,
generalised rather than tied to one accounting platform. Stamped 2026-08-11.

Independent verification 2026-10-21: 9 checked, 8 matched, 0 corrected, 1 unverified
