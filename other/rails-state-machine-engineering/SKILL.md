---
name: rails-state-machine-engineering
description: Use when Rails/Ruby models own durable workflow state — orders, payments, approvals, imports, deployments — with explicit state and transition contracts, transition authorization, concurrent transition attempts, duplicate or out-of-order events, and recovery when side effects fail.
license: MIT
---

# Domain State Machine Engineering

## Purpose

Treat durable state transitions as an application contract, not as scattered `if state ==` checks.

A dependable state machine makes states, legal transitions, guards, and terminal states explicit; authorizes and audits every transition; survives concurrent transition attempts; absorbs duplicate, delayed, and out-of-order events; and recovers when a side effect succeeds but local persistence fails (or the reverse).

Core flow:

```
identify states, events, and terminal states
-> write the transition table as code
-> guard and authorize transitions
-> apply transitions atomically with locking
-> absorb duplicate, delayed, and out-of-order events
-> sequence side effects around persistence deliberately
-> audit every transition
-> test allowed, rejected, concurrent, and recovery paths
```

Compose this skill with:

- rails-active-record for persistence lifecycle and transactions;
- rails-database-engineering for locking and constraint enforcement;
- rails-distributed-systems for saga/compensation when state spans services;
- rails-event-driven-messaging when transitions publish or consume events;
- rails-external-stream-ingestion when state changes are driven by an external feed;
- rails-api-integration for remote side-effect boundaries;
- rails-observability for transition telemetry;
- rails-test-engineering for deterministic state tests.

This skill owns durable, application-level state. It does not replace workflow orchestration across services (rails-distributed-systems owns sagas), and a gem like AASM is one implementation choice, not the contract itself.

## Activate when

- a model has workflow states (orders, payments, approvals, imports, deployments, reservations);
- adding, renaming, or splitting states and transitions;
- writing guards, transition callbacks, or state-dependent authorization;
- handling illegal or double transition attempts from concurrent requests;
- processing duplicate, delayed, or out-of-order state-change events;
- recovering when a side effect succeeded but the transaction rolled back (or the reverse);
- adding audit history for state changes;
- migrating existing data into a stricter state machine;
- testing state machines, including rejected transitions and races.

Do not activate for boolean flags on a model that carry no transition semantics, for cache lifecycles (rails-caching owns those), or for job retry states (rails-active-job owns those). Activate when persisted state with legal-transition semantics is the boundary being changed.

## Repository inspection

Inspect:

1. the model(s) holding state: column, type, default, and whether an enum or string is used;
2. every writer of the state column: controllers, jobs, callbacks, service objects, migrations, console scripts;
3. the current transition set: which transitions actually occur in code and in production data;
4. guards and validations already enforced, and where (model, service, database);
5. transition authorization: who may trigger which transition;
6. locking strategy: optimistic locking, `with_lock`, unique indexes on state;
7. event sources that mutate state: HTTP, webhooks, broker messages, external feeds;
8. duplicate delivery behavior of each source, and whether idempotency keys exist;
9. side effects tied to transitions: emails, payments, external calls, publishes;
10. audit trail: history table, paper_trail-style versions, or none;
11. existing tests covering transitions, races, and recovery;
12. production data distribution across states (a state with zero rows is a state nobody reaches).

Do not assume the state machine is what the tests describe. Derive the real transition table from the code that writes state, then reconcile with documentation and tests; where they disagree, the code is the observed implementation and the disagreement is a finding.

## Decision rules

1. Classify the change: transition contract; guards, authorization, and audit; concurrency and event ordering; side effects and recovery; or migration and testing. Load the matching reference below before changing that boundary.
2. Write the transition table before the code that uses it — states, events, legal transitions, terminal states, and the guard for each edge. If the table cannot be written, the domain is not understood yet.
3. Prefer one transition entry point per model (`transition!`/`apply_event`), so guards, locking, audit, and callbacks live in one place instead of scattered assignments.
4. Choose locking by contention: optimistic locking for low-contention workflows, row locks (`with_lock`) where concurrent attempts on the same record are expected.
5. Make illegal transitions loud: a rejected transition is an exception or an explicit failure result, never a silent no-op.
6. Treat every external state-change event as duplicate-capable and potentially out of order until the source proves otherwise.

## Critical invariants

- Never write the state column outside the transition entry point.
- Never transition on stale state: re-read under lock (or use optimistic locking) before deciding.
- A transition and its transactional side effects commit or roll back together; remote side effects are sequenced deliberately around the transaction (intent, then effect, then completion).
- A duplicate event application must leave the machine in the same state with the same effects as a single application.
- Never destroy the audit trail of how a record reached its current state.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change defines states, events, legal transitions, terminal states, guards, transition authorization, or audit history | [references/transition-contracts.md](references/transition-contracts.md) | Transition table; Guards and exit actions; Transition authorization; Audit history | `state-transition-guard` |
| a change handles concurrent transition attempts, duplicate, delayed, or out-of-order events | [references/concurrency-and-events.md](references/concurrency-and-events.md) | Locking strategies; Concurrent attempts; Duplicate and idempotent application; Out-of-order events | `inbox-deduplication` |
| a change sequences side effects around a transition or recovers from partial failure | [references/side-effects-and-recovery.md](references/side-effects-and-recovery.md) | Transactional side effects; Remote side effects and intent; Failure recovery; Reconciliation | `outbox-publication`, `dead-letter-replay` |
| a change tests transitions, races, or recovery, or migrates existing data into the machine | [references/testing-and-migration.md](references/testing-and-migration.md) | Transition test matrix; Race and recovery tests; Data migration into the machine | `state-machine-testing` |

## Reference example

An explicit transition table with a single guarded, locked, audited entry point:

```ruby
# app/models/order.rb
class Order < ApplicationRecord
  TRANSITIONS = {
    "pending"  => { "place"  => "placed",   "cancel" => "cancelled" },
    "placed"   => { "fill"   => "filled",    "cancel" => "cancelled" },
    "filled"   => { "return" => "returned" },
    "cancelled" => {},                        # terminal
    "returned"  => {}                         # terminal
  }.freeze

  def apply_event!(event, actor: nil)
    with_lock do
      target = TRANSITIONS.fetch(state, {})[event] or
        raise IllegalTransition, "#{state} + #{event} is not a legal transition"

      prior = state
      update!(state: target)
      record_transition(from: prior, to: target, event: event, actor: actor)
    end
    OrderMailer.filled(self).deliver_later if event == "fill" # after commit, idempotent
  end
end
```

The table is executable documentation; `apply_event!` is the only door; every transition is audited; illegal events fail loudly instead of silently.

## Agent review checklist

- [ ] states, events, legal transitions, and terminal states written as one table
- [ ] every state writer routed through the single transition entry point
- [ ] guards and preconditions explicit per edge
- [ ] transition authorization decided (who may fire which event)
- [ ] illegal transitions raise or return explicit failure, never no-op silently
- [ ] concurrency strategy chosen and implemented (lock or optimistic check)
- [ ] duplicate event application idempotent, with identity defined
- [ ] out-of-order events detected, buffered, rejected, or reconciled
- [ ] transactional side effects inside the transition transaction
- [ ] remote side effects sequenced with durable intent before execution
- [ ] recovery path exists for effect-succeeded/state-failed and state-succeeded/effect-failed
- [ ] audit history records from, to, event, actor, and time
- [ ] terminal states reachable and final
- [ ] transition test matrix covers allowed, rejected, concurrent, and recovery paths
- [ ] existing data migrated or validated against the new table

## Anti-patterns

- assigning `state` directly from a controller, job, or callback;
- `if state == "x"` ladders scattered across the codebase instead of a table;
- an `enum` plus scattered `update` calls mistaken for a state machine;
- silent no-ops on illegal transitions;
- transitioning on stale reads without a lock or version check;
- performing remote calls inside the state transaction, holding a row lock over the network;
- assuming webhooks, broker messages, or feeds deliver exactly once and in order;
- wiping or rewriting audit history during a state migration;
- state columns that double as display labels, inviting cosmetic renames that break transitions;
- testing only the happy path through the table;
- `rescue => nil` around transitions in background jobs.

## Verification

For the transition contract:

`table exhaustive -> every event x state classified (legal, illegal, unknown) -> terminal states final`

For concurrency:

`two concurrent transitions -> exactly one succeeds -> loser sees explicit failure -> record consistent`

For events:

`duplicate delivery -> same final state and effects -> out-of-order delivery -> detected and handled by policy`

For recovery:

`crash between intent and effect -> recovery completes or reconciles -> audit trail explains the outcome`

Report the transition table, the locking choice, the duplicate/out-of-order policy, side-effect sequencing, and the test matrix evidence.

## Source foundation

- Rails Active Record Transactions: https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- Rails Active Record Locking (optimistic/pessimistic): https://api.rubyonrails.org/classes/ActiveRecord/Locking.html
- Rails Enum: https://api.rubyonrails.org/classes/ActiveRecord/Enum.html
- AASM: https://github.com/aasm/aasm
- Repository skills: rails-active-record, rails-database-engineering, rails-distributed-systems, rails-event-driven-messaging, rails-api-integration, rails-observability, rails-test-engineering

## Domain state machine changes

For durable state, transition, and workflow changes:

- write the transition table (states, events, legal edges, terminal states) before touching writers;
- route every state write through one guarded entry point and never assign the column elsewhere;
- authorize transitions explicitly (actor, role, or system event source) and record it in the audit trail;
- choose locking by measured contention and re-validate state inside the lock;
- make illegal transitions fail loudly and observably;
- treat external state-change events as duplicate-capable and out-of-order by default; deduplicate on durable event identity;
- keep transactional side effects inside the transaction and remote side effects behind durable intent (outbox or intent record) completed after commit;
- define the recovery and reconciliation path for every partial-failure window before shipping it;
- preserve transition history as append-only evidence;
- test the full matrix: allowed, rejected, concurrent, duplicate, out-of-order, and recovery;
- migrate existing data by validating against the new table first, then backfilling with the audit trail intact.
