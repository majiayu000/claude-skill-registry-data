---
name: trading-execution-safety
description: Use when Ruby/Rails applications place or manage orders through an external execution system — brokers, exchanges, paper and live gateways — covering durable order intent, client order IDs, duplicate order prevention, submission versus acknowledgement versus fill, retry under uncertain outcomes, reconciliation, paper/live separation, and fail-closed risk gates.
license: MIT
---

# Trading Execution Safety

## Purpose

Treat order execution as the boundary where a software defect has direct financial consequences, and engineer it so the worst failures cost an alert rather than a duplicated live order.

A safe execution layer persists a durable intent before any side effect, gives every order a deterministic client-generated identity, distinguishes submission from acknowledgement from fill, retries nothing that might already have executed, reconciles against the broker as the source of truth, and keeps paper and live execution separated by gates that fail closed.

Core flow:

```
decision produces an order intent (durable, identified)
-> risk gates evaluate fail-closed before submission
-> submit exactly once per intent with the client order ID
-> acknowledgement, partial fills, and fills update state through transitions
-> uncertain outcomes are resolved by reconciliation, never by resubmission
-> exits and cancellations follow the same rules
-> divergence from the broker reconciles to the broker
-> every step observable and tested adversarially
```

Compose this skill with:

- rails-state-machine-engineering for the order lifecycle as a guarded machine;
- rails-api-integration for the broker's REST contracts and idempotent requests;
- ruby-financial-data-integrity for money/quantity representation and ledger effects;
- trading-market-data-and-backtesting for data integrity feeding decisions;
- rails-external-stream-ingestion for consuming broker event streams;
- rails-reliability-engineering for circuit breakers and degradation budgets;
- rails-observability for execution telemetry and divergence alerts.

This skill owns execution safety at an external venue. It does not own strategy quality (market data and backtesting own that), general messaging, or generic API advice — those composites already exist.

## Activate when

- placing, modifying, or cancelling orders through a broker, exchange, or gateway;
- implementing paper versus live trading modes and the gates between them;
- designing order intent records, client order IDs, or duplicate order prevention;
- handling acknowledgements, partial fills, rejections, and order state callbacks;
- deciding retry behavior when a submission outcome is uncertain (timeout, disconnect);
- building broker reconciliation for positions, orders, or fills;
- adding risk guards that must prevent unintended live execution;
- reviewing execution-path code for double-execution or runaway-order risks;
- testing execution flows without a live account.

Do not activate for market data pipelines, indicator or strategy research, or backtests — those are data-integrity problems, not execution boundaries. Do not use this skill to build investment advice; it is an engineering safety contract.

## Repository inspection

Inspect:

1. the gateway abstraction: paper and live implementations and their shared/differing contracts;
2. the order intent model: durability, identity, lifecycle states, and audit trail;
3. how client order IDs are generated and whether they are deterministic per intent;
4. the exact broker request/response contracts: submit, amend, cancel, and status;
5. acknowledgment and fill event sources: push streams, polling, or both, and their ordering;
6. retry and timeout behavior on every execution call path, including job retries;
7. position and order state derivation: computed locally, from broker events, or reconciled;
8. the paper/live switch: configuration, flags, defaults, and what fails open;
9. risk guards and their position in the flow relative to submission;
10. what happens on process crash between intent, submission, and confirmation;
11. reconciliation tooling and its schedule, or its absence;
12. tests for duplicate submissions, partial fills, and ambiguous outcomes;
13. credentials and environment targeting for live venues (where they live, how they are scoped).

Do not assume the broker deduplicates, that submit responses imply acceptance, or that polling and streams agree. Verify each guarantee against the venue's documented contract and observed behavior in the sandbox.

## Decision rules

1. Classify the change: order identity and intent; submission and fill handling; retries and uncertain outcomes; paper/live separation and risk gates; or reconciliation and testing. Load the matching reference below before changing that boundary.
2. Persist the intent, with its deterministic client order ID, before any submission call — an intent that exists only in memory cannot be deduplicated, recovered, or audited.
3. Separate the lifecycle states of submitted, acknowledged, partially filled, filled, rejected, and cancelled; they are different facts from different sources at different times.
4. Treat every ambiguous outcome (timeout, connection drop, unknown error) as "probably executed" until reconciliation proves otherwise; never auto-resubmit to "make sure".
5. Fail closed on risk gates: missing data, stale prices, unknown positions, or unhealthy feeds must block submission, not pass with defaults.
6. Derive nothing from paper behavior that is asserted about live behavior; the two share contracts, not risk.

## Critical invariants

- Never submit without a durable, uniquely identified intent recorded first.
- Never regenerate a client order ID on retry; the ID is the intent's identity across all attempts.
- Never resubmit an order whose submission outcome is unknown; reconcile instead.
- Never let a live submission path be reachable by default; live mode must be an explicit, gated, observable switch.
- Never bypass a risk gate for latency, convenience, or a "special case".

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change defines order intents, client order IDs, or duplicate-order prevention | [references/intent-and-identity.md](references/intent-and-identity.md) | Durable intent before side effects; Client order ID generation; Duplicate prevention; Amend and cancel identities | `state-transition-guard` |
| a change submits orders or handles acknowledgements, partial fills, or rejections | [references/submission-and-fills.md](references/submission-and-fills.md) | Submission semantics; Acknowledgement versus fill; Partial fills; Exit requests; Event application | `event-envelope` |
| a change retries submissions, handles uncertain outcomes, or reconciles with the broker | [references/retries-and-reconciliation.md](references/retries-and-reconciliation.md) | Ambiguous outcomes; Retry policy; Broker reconciliation; Divergence handling | `inbox-deduplication` |
| a change touches paper/live separation, risk gates, or execution testing | [references/paper-live-and-testing.md](references/paper-live-and-testing.md) | Paper/live separation; Fail-closed gates; Execution testing; Adversarial cases | `circuit-breaker` |

## Reference example

Intent first, identity deterministic, submission exactly once per identity:

```ruby
# app/services/execution/submit_order.rb
module Execution
  class SubmitOrder
    def initialize(gateway:, risk_gate:)
      @gateway = gateway
      @risk_gate = risk_gate
    end

    def call(intent)
      @risk_gate.assert_submittable!(intent)      # fail-closed; raises on any unknown

      ActiveRecord::Base.transaction do
        intent.transition!(:submitted)              # illegal second submission raises here
        ExecutionLog.create!(intent: intent, phase: "submit", client_order_id: intent.client_order_id)
      end

      response = @gateway.place_order(             # after commit: the remote side effect
        client_order_id: intent.client_order_id,  # deterministic: derived from the intent
        symbol: intent.symbol, side: intent.side,
        quantity: intent.quantity, price: intent.limit_price
      )
      intent.transition!(:acknowledged, broker_order_id: response.order_id)
    rescue Gateway::TimeoutError, Gateway::ConnectionError
      intent.transition!(:outcome_unknown)          # reconcile; never resubmit blindly
      Execution::ReconcileIntentJob.perform_later(intent.id)
    end
  end
end
```

The unique index on `client_order_id` plus the `submitted` transition guard makes a double submission impossible; the timeout path preserves the identity for reconciliation instead of gambling on a second order.

## Agent review checklist

- [ ] intent persisted with deterministic client order ID before any remote call
- [ ] unique constraint enforces one submission per identity
- [ ] client order ID stable across retries, replays, and restarts
- [ ] submission, acknowledgement, fill, and rejection states distinguished
- [ ] partial fills accumulate to the executed quantity without double counting
- [ ] exit/cancel requests carry their own identities and confirmations
- [ ] ambiguous outcomes marked unknown and reconciled, never auto-resubmitted
- [ ] retry policy classifies errors into definitely-not-executed versus unknown
- [ ] reconciliation treats the broker as the source of truth for executed quantity and position
- [ ] paper/live separation explicit, gated, and off by default for live
- [ ] risk gates fail closed on unknown data, stale prices, and missing positions
- [ ] execution path observable: every phase logged with identifiers, never with secrets
- [ ] adversarial tests cover duplicate submission, timeout-then-filled, and divergence

## Anti-patterns

- generating a random order ID per attempt;
- resubmitting after a timeout because the response never arrived;
- treating a submit's 200 as a fill;
- deriving positions by summing local events and never reconciling;
- one boolean "live mode" flag readable from anywhere with no gate;
- risk checks that pass when their inputs are missing or stale;
- bypassing the intent table "just for this one manual trade";
- paper mode that differs from live in serialization, validation, or sequencing;
- logging API keys or full credentials in execution logs;
- testing only the happy path with a mocked gateway that always fills.

## Verification

For identity and intent:

`intent created -> ID deterministic -> unique constraint holds -> crash before submit -> exactly one order can ever exist for the intent`

For the fill lifecycle:

`submitted -> acknowledged -> partial fills accumulate -> filled or rejected -> quantities balance`

For uncertain outcomes:

`timeout -> state unknown -> reconciliation query -> correct final state -> no second order`

For gates:

`stale price -> blocked; missing position -> blocked; feed down -> blocked; healthy input -> allowed`

Report the identity discipline, the retry classification, the reconciliation evidence, and the gate test results.

## Source foundation

- FIX protocol dictionary (ClOrdID, OrdStatus, ExecType semantics): https://www.fixtrading.org/standards/
- Rails Active Record Transactions: https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- Idempotency keys in payment/execution APIs (Stripe pattern): https://docs.stripe.com/api/idempotent_requests
- Repository skills: rails-state-machine-engineering, rails-api-integration, ruby-financial-data-integrity, trading-market-data-and-backtesting, rails-external-stream-ingestion, rails-reliability-engineering, rails-observability, rails-test-engineering

## Trading execution safety changes

For order placement, gateway, and execution-path changes:

- persist a durable intent with a deterministic client order ID before any remote submission;
- enforce one submission per identity with a database unique constraint plus a guarded transition;
- distinguish submission, acknowledgement, partial fill, fill, and rejection as separate facts;
- classify every error as definitely-not-executed or unknown, and reconcile the unknown instead of retrying;
- make exits and cancels first-class identified requests with their own confirmations;
- treat the broker as the source of truth and reconcile positions, executed quantities, and order state on a schedule;
- keep paper and live behind one explicit, observable, default-off gate and make them share contracts;
- make risk gates fail closed on stale, missing, or inconsistent inputs, and never bypass them;
- log execution phases with identifiers (intent, client order ID, broker order ID) and never with credentials;
- test duplicates, timeouts, partial fills, out-of-order events, and divergence adversarially with a fake gateway, never a live account.
