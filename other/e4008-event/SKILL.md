---
name: e4008-event
description: "Validate the event publish-and-subscribe design of a space simulator against ECSS-E-ST-40-08C clause 5.4.6. Use when the task is declaring an event source with one typed argument, refusing a repeated subscription or an unsubscribe by a sink that never subscribed, holding notification in subscription order, checking an emitted argument against the declared type, keeping an emission out of a simulator state that cannot honour it, isolating one raising sink so the sinks behind it are still notified, and grading the design against the fourteen normative items the clause carries. Trigger: ecss, e-st-40-08c, simulator-event-source, simulator-event-sink, event-subscription-order, event-argument-type-check, duplicate-event-subscription, event-sink-failure-isolation, event-emission-state-guard."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-40-08-simulation-scope, e4008-event, simulator-event-source, simulator-event-sink, event-subscription-order, event-argument-type-check, event-sink-failure-isolation]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Simulation Infrastructure — Event (space-systems/ecss/e4008-event)

Use when the task is the event mechanism of ECSS-E-ST-40-08C clause 5.4.6
-- how a simulator publishes an event, who is allowed to subscribe to it,
what an emission may carry, and what the infrastructure owes the
remaining subscribers when one of them fails. The clause carries fourteen
normative items and a design is graded against all of them.

## Domain quick reference

- An event source is a named publication point with exactly one declared
  argument type drawn from the infrastructure primitive set. A void
  source publishes the fact that something happened and nothing else, so
  handing it a payload is an error and not a convenience.
- Subscription is by sink identity, not by callable. A repeated
  subscription by the same sink is refused rather than folded into one,
  because the alternative makes the delivered notification count depend
  on how many times the model tree was walked during assembly.
- Sink identity has to be canonical before it is compared. Two names that
  differ only by case, hyphen or blank are the same subscriber; letting
  them both in means an unsubscribe removes one of a pair the design
  believed was single.
- Notification order is the subscription order. It is the only order a
  replay can reproduce, so a set-backed or hash-backed subscriber store
  is a reproducibility defect even when every sink is eventually reached.
- Emission is a state-dependent operation. A simulator that has not yet
  built its model tree, or that is already unwinding, has no consistent
  set of sinks to notify; those states refuse the emission instead of
  dropping it silently.
- One sink raising is a sink defect, not an event defect. The emission
  records the failure and carries on down the list, so a single bad
  subscriber cannot quietly starve every subscriber added after it.
- The delivery walks a snapshot of the subscriber list. A sink that
  unsubscribes from inside its own notification changes the next
  emission, never the one in flight.

## Workflow

1. Validate each source name and argument type at declaration; a
   repeated name inside one publisher is refused rather than shadowed.
2. Record a declared subscriber ceiling where the design states one, and
   whether the source has a documented emitter -- a source nothing ever
   raises is dead interface surface.
3. Canonicalise every sink name to its identity token before subscribing,
   and refuse both an exact repeat and an aliased repeat.
4. Refuse an unsubscribe naming a sink the source does not hold; an
   ignored unsubscribe hides a wiring error in the model tree.
5. On emission, resolve the simulator state, reject a state that cannot
   honour a notification, then check the argument against the declared
   type with the void case handled explicitly.
6. Stamp the emission with the next sequence number, notify the snapshot
   in subscription order, and collect the raising sinks separately from
   the delivered ones.
7. Grade the fourteen normative items, separating a violated item from
   one the evidence never exercised, and report coverage alongside the
   verdict so an untested item cannot read as a pass.

## Pitfalls

- Treating a repeated subscription as idempotent. Collapsing it silently
  makes the notification count depend on assembly order, and the defect
  only shows up as a duplicated telemetry sample much later.
- Comparing sink names raw. A subscriber added as one spelling and
  removed as another leaves a stale entry that keeps receiving
  notifications after the model believes it detached.
- Storing subscribers in a set or dictionary keyed by object identity.
  Every sink is still reached, so the tests pass, but two runs of the
  same scenario notify them in different orders and the recorded output
  stops being reproducible.
- Swallowing an exception raised by a sink and stopping the walk. The
  sinks registered after the raising one never learn the event happened,
  and nothing in the run log says so.
- Mutating the subscriber list from inside a notification. The walk then
  skips the sink that moved into the vacated slot, which is the hardest
  class of missed-notification defect to reproduce.
- Reporting an item as satisfied because no evidence contradicted it. An
  item no scenario exercised is not a pass; it is a coverage gap and the
  assessment reports it as its own status.

## Behavior contract (gate 3)

Name and type validation, sink identity canonicalisation, subscription
and unsubscription refusal, ordered snapshot delivery, state-guarded
emission, argument type checking, raising-sink isolation and the
fourteen-item conformance grading are exercised by the gate 3 contract
test: scripts/test_e4008_event.py against scripts/e4008_event_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e4008_event.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
