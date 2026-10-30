---
name: ruby-financial-data-integrity
description: Use when Ruby/Rails code represents or computes money, prices, quantities, fees, or PnL — BigDecimal discipline, decimal precision and scale, explicit rounding, atomic balance updates, double-entry ledger invariants, posting idempotency, and reconciliation.
license: MIT
---

# Financial Data Integrity

## Purpose

Treat numeric correctness in financial code as a construction discipline: represent money exactly, state rounding instead of stumbling into it, make balances move only through balancing journal entries, and prove the books balance with invariants instead of hoping.

Financial bugs are quiet: totals drift by cents, balances go negative under concurrency, rounding direction silently favors one side, and the discrepancy surfaces days later in a reconciliation nobody can explain. The discipline is boring on purpose — exact representation, explicit scale, transactional posting, invariant checks.

Core flow:

```
choose exact numeric representation
-> fix precision and scale at the schema boundary
-> make every rounding an explicit, named decision
-> move balances only through balanced journal entries
-> post once per business event (idempotency keys)
-> compute PnL and fees from the posting layer
-> verify invariants continuously
-> reconcile against external sources on a schedule
```

Compose this skill with:

- rails-database-engineering for constraints, transactions, and isolation;
- rails-state-machine-engineering when postings follow durable state transitions;
- trading-execution-safety when the money facts originate at a venue;
- rails-api-integration for external financial API contracts;
- rails-active-record for persistence boundaries;
- rails-observability for invariant-violation alerting.

This skill owns numeric and accounting correctness in application code. It does not own tax jurisdiction rules, regulatory reporting formats, or execution safety — those are separate domains composable with this one.

## Activate when

- representing money, prices, quantities, or balances in Ruby or the database;
- choosing between `BigDecimal`, integer minor units, and `Float`;
- defining decimal columns and migrating their precision/scale;
- writing rounding logic for fees, taxes, allocations, or splits;
- building ledgers, journals, balance updates, or account state;
- posting financial events that must apply exactly once;
- computing PnL, realized/unrealized gains, or weighted averages;
- adding idempotency to payment or ledger writes;
- reconciling internal totals against a bank, broker, or processor;
- testing financial arithmetic and its edge cases.

Do not activate for display formatting of already-exact values, or for analytics on non-financial floats (metrics, durations, counts). Activate whenever a number that represents money or quantity flows through code that must not lie.

## Repository inspection

Inspect:

1. every money/quantity representation: `BigDecimal`, integer minor units, `Float`, `String`, or mixed;
2. schema: decimal columns' `precision` and `scale`, integer columns' bit-width assumptions, and nullability;
3. every rounding site: which rounding mode, applied at which step, and whether it is explicit;
4. currency and unit conventions: currency codes, lot sizes, tick sizes, sign conventions;
5. where balances live and every code path that mutates them;
6. the ledger/journal shape if one exists: entries, postings, transactional grouping, and the balancing check;
7. idempotency: what makes a business event postable exactly once, and where it is enforced;
8. fee and PnL formulas and their inputs' exactness (prices from JSON strings? floats from an API?);
9. serialization boundaries: JSON parsing, query parameters, and CSV/external imports;
10. existing invariants or reconciliation jobs, and what they check;
11. tests covering rounding boundaries, negative balances, and concurrent posts;
12. time handling of financial periods (timezone of the close, day boundaries).

Do not assume JSON numbers arrive exact (they may parse to `Float`), that the database column scale matches the application's expectation, or that upstream systems round the way this code does. Verify representation at every boundary; representation drift is the most common financial defect.

## Decision rules

1. Classify the change: representation and rounding; ledger and balances; quantities, fees, and PnL; or reconciliation and testing. Load the matching reference below before changing that boundary.
2. Choose one exact representation per concept (money as integer minor units or scale-fixed `BigDecimal`; quantities as exact decimals) and convert at the edges — never mix representations inside one computation.
3. Make rounding a named decision with a stated mode (`ROUND_HALF_UP` vs `ROUND_DOWN` for fees), never the default of a formatter or a float accident.
4. Move balances only through journal entries that balance, inside one database transaction, with the event's idempotency key.
5. Verify totals with invariants (`sum(debits) == sum(credits)`, account balance equals its entry sum) and alert, do not log-and-continue, when they break.
6. Reconcile against the external source of truth on a schedule; drift is a bug with a number attached.

## Critical invariants

- Never use `Float` for money or for any value that must survive arithmetic unchanged.
- Never widen or narrow a decimal column's scale without migrating and verifying existing data.
- Never mutate a balance outside a balancing journal transaction.
- Never post a business event twice; the idempotency key is the event's identity, not the attempt's.
- Never let an invariant failure pass silently into the books.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change represents money/quantities, parses financial input, defines decimal columns, or rounds | [references/numeric-representation.md](references/numeric-representation.md) | BigDecimal discipline; Precision and scale; Parsing boundaries; Rounding decisions; Minor units | `idempotent-request` |
| a change builds or alters ledgers, balances, or posting paths | [references/ledger-and-balances.md](references/ledger-and-balances.md) | Double-entry invariants; Posting transactions; Atomic balance updates; Posting idempotency | `state-transition-guard` |
| a change computes fees, quantities, or PnL | [references/fees-quantities-and-pnl.md](references/fees-quantities-and-pnl.md) | Quantity and lot constraints; Fee arithmetic; PnL and weighted averages; Sign conventions | `event-envelope` |
| a change verifies totals, reconciles with external systems, or tests financial arithmetic | [references/reconciliation-and-testing.md](references/reconciliation-and-testing.md) | Invariant checks; External reconciliation; Adversarial numeric tests; Rounding regressions | `message-observability` |

## Reference example

Money as scale-fixed `BigDecimal` with explicit rounding, posted through a balancing journal:

```ruby
# config/initializers/money.rb
MoneyScale = 10              # decimal(20, 10): prices fit, sums fit, scale is fixed
ROUNDING = BigDecimal::ROUND_HALF_UP   # fees round half-up, decided by name, once

class PostingService
  # One event, one posting: the idempotency key is the business event's identity.
  def post(event)
    ActiveRecord::Base.transaction do
      JournalEntry.create!(event_id: event.id) # unique index on event_id
      JournalPosting.create!(
        entry: entry, account: cash_account(event),
        amount: -event.amount, currency: event.currency
      )
      JournalPosting.create!(
        entry: entry, account: revenue_account(event),
        amount: event.amount, currency: event.currency
      )
    end
  rescue ActiveRecord::RecordNotUnique
    :already_posted            # the key held; the event is applied exactly once
  end

  def fee_for(notional, rate)
    (notional * rate).round(2, ROUNDING)   # rounding is a decision, not a default
  end
end
```

Every amount passes through `BigDecimal` at the parse boundary; the column scale and the round mode agree; the entry balances or the transaction dies.

## Agent review checklist

- [ ] one exact representation per concept, converted at edges only
- [ ] no `Float` anywhere in a money or quantity path
- [ ] decimal columns' precision/scale documented and sufficient for sums
- [ ] every rounding site names its mode and its reason
- [ ] balances mutable only through balancing journal transactions
- [ ] posting idempotency enforced by a unique key on the event identity
- [ ] negative balances impossible by constraint or explained by design
- [ ] quantity/lot/tick constraints validated before execution
- [ ] PnL computed from postings with consistent sign conventions
- [ ] invariants checked continuously and failures alert loudly
- [ ] reconciliation against the external source scheduled and evidenced
- [ ] adversarial tests: rounding boundaries, zero, negative, huge, concurrent posts

## Anti-patterns

- `Float` for money ("it's just a display value" — until it is a ledger input);
- parsing JSON prices with `JSON.parse` and landing on `Float`;
- rounding at intermediate steps of a multi-step calculation;
- storing formatted strings as money;
- `update_all balance: balance + x` without a lock or a constraint;
- balances without a journal, mutated by scattered service objects;
- regenerating an idempotency key per retry;
- symmetric rounding applied to a directional cost (fees should round against the earner, decided once);
- verifying totals with `puts` in a rake task instead of an invariant with an alert;
- reconciling by editing the books to match the bank without recording the adjustment;
- mixing currencies in one arithmetic expression;
- `rescue nil` around a posting.

## Verification

For representation:

`parse exact -> compute -> round once at the named decision point -> serialize exact`

For the ledger:

`event -> balancing entry -> both sides commit -> totals unchanged -> idempotent re-post is a no-op`

For concurrency:

`two posts against one account -> both applied exactly once -> balance equals the entry sum`

For reconciliation:

`internal total -> external statement -> difference computed exactly -> adjustment journaled or alert raised`

Report representation choices, rounding decisions, the balancing invariant, the idempotency key definition, and the invariant/reconciliation evidence.

## Source foundation

- Ruby BigDecimal documentation: https://docs.ruby-lang.org/en/master/BigDecimal.html
- Ruby JSON parsing and Float precision: https://docs.ruby-lang.org/en/master/JSON.html
- PostgreSQL numeric type (precision/scale): https://www.postgresql.org/docs/current/datatype-numeric.html
- Rails Active Record migrations: https://guides.rubyonrails.org/active_record_migrations.html
- Repository skills: rails-database-engineering, rails-state-machine-engineering, trading-execution-safety, rails-api-integration, rails-active-record, rails-observability

## Financial data integrity changes

For money, quantity, ledger, and accounting changes:

- fix the exact representation (integer minor units or scale-fixed `BigDecimal`) at every parse and serialization boundary, and keep `Float` out of the path;
- define decimal precision and scale for the largest realistic sum plus headroom, and migrate scale changes with data verification;
- make every rounding an explicit named decision with a mode and a reason, applied once at the boundary that owns it;
- move balances only through journal entries that balance within one database transaction;
- enforce one posting per business event with a unique idempotency key that is the event's identity;
- validate quantity, lot, and tick constraints before they reach execution arithmetic;
- compute fees and PnL from the posting layer with consistent sign conventions and weighted-average rules;
- check the balancing and account-sum invariants continuously, and alert on violation instead of continuing;
- reconcile internal totals against the external source of truth on a schedule and journal every adjustment;
- test adversarially: rounding boundaries, zero and negative values, overflow-scale sums, and concurrent posting races.
