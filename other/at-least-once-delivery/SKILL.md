---
name: at-least-once-delivery
description: Use when a program receives units of work another party delivers, and delivers again until they are acknowledged — a queue or stream consumer, a webhook receiver, any handler a broker or a third-party sender calls — or is itself that sender, relaying an effect it recorded with a committed write, as an outbox relay does, in any project whatever its architecture. Owns when a unit is acknowledged and when it is returned, the bounded redelivery and the dead letter an operator reads, a redelivery that changes nothing — identity and values taken from the unit, never the clock or a per-delivery mint — and a third party's signature verified over the raw body before parsing; and on the sending side, what a relay of a recorded effect owes. It binds no broker and writes no file; the consumer or route that applies it is the architecture family's, an older write never replacing a newer one is `persistence`'s, and whether an effect after a write is recorded at all is `exception-catalog`'s. Also when asked whether a consumer needs at-most-once, at-least-once or exactly-once delivery, whether to acknowledge before or after the handler, why a message was lost or applied twice, where a failed message goes, or how to verify a webhook's signature.
---

# At-least-once delivery — a unit delivered until it is acknowledged

The obligations a program owes each **unit another party delivers to it and delivers again until it is
acknowledged** — a broker's message, a record read from a stream, a webhook request from a third party.
They hold in any project, whatever its architecture and whatever delivers the unit. None binds a broker:
the limit and the dead letter are the delivery mechanism's configuration, declared with the deployment,
and the code that receives the unit — a consumer wrapper, a route, an inbound adapter — is written
under the project's own entrypoint skill. Rule 6 is the same guarantee from the other side: a program
relaying an effect it recorded with a committed write is that sender to whoever receives it.

## When to use vs. neighbours

- The consumer process, its wrapper and the HTTP route that apply these rules in a flat-layered service
  → `flat-entrypoint`, in the `pyhouse-flat` plugin; the inbound adapter of a hexagonal service →
  `hex-architecture`, in the `pyhouse-hex` plugin. Both are examples; with neither installed, the
  project's own entrypoint applies them.
- An older write never replacing a newer one for the same key, and deduplication left to the store →
  `persistence` (rules 15–17); rule 4 here only says when that applies to a delivered unit.
- A failure after a committed write — whether its effect is recorded with the write at all, or stopped
  and logged when it fails — and a failure stopped rather than swallowed → `exception-catalog`; the
  record committed in the write's own transaction → `persistence` rule 2. What the relay owes once the
  record exists is rule 6 here.
- Which scope logs a failed unit, and the event it logs → `python-logging`.
- The signing secret, and where it is unwrapped → `python-settings`.
- Testing that a failed unit is returned and that a second delivery changes nothing → the family's
  entrypoint test skill (`flat-test-entrypoint` rules 2 and 6, in the `pyhouse-flat` plugin, is an
  example); in a hexagonal service the redelivered create is `hex-test-application-handler`'s, in the
  `pyhouse-hex` plugin.

## Which guarantee

- **At least once** is what the rules below bind, and what a broker or a webhook sender gives once the
  program acknowledges after the effect (rule 1). Several defaults give less — a task queue
  acknowledging before the task runs, offsets committed on a timer — and rule 1 is what corrects them; a
  transport that never redelivers (a fire-and-forget publish) is at most once whatever the program does,
  and choosing it is the choice below.
- **At most once** — the unit acknowledged on receipt, a crash losing it — is a choice only where losing
  a unit costs nothing (a metric sample, a presence ping), and only made and recorded as that choice. Rules
  1–3 do not bind a unit taken that way, and rules 4 and 5 still do; an early acknowledgement nobody
  chose is rule 1's defect.
- **Exactly once**, where a broker offers it, holds inside that broker — its transactions, a
  deduplication window over what is sent to it — and never reaches a write the program makes elsewhere. An effect applied once
  is at-least-once delivery with rule 3's idempotent effect, so a broker's exactly-once removes no rule
  here.

## Which rules bind — who delivers

| The unit is delivered by… | Rules |
|---|---|
| a broker or a stream — a queue, a log read by offset, a stream read by a consumer group — whether it pushes or the program polls it, on any schedule | 1–4 |
| a third party over HTTP, which signs what it sends | 1, 3, 4, 5 — and rule 2's answer to a failure; the sender's retry schedule and its dead letter are its own |
| a third party over HTTP that signs nothing, on a network that already trusts it | 1, 3, 4 — and rule 2's answer to a failure |
| this program, relaying to another party an effect it recorded with a committed write — an outbox row | 6; a receiver the project owns holds 3 and 4 |

A program **reading a source that keeps no delivery state for it** — a table, an API, a file listing —
is delivered nothing: nothing redelivers to it, and its next run is its retry. A broker or a stream read
by polling is still delivering, and a relay reading its own record of an effect is the sender of rule 6,
not such a reader.

## Rules

1. **A unit is acknowledged only once its effect is committed, and a failed one is returned.** The
   acknowledgement — a message acknowledged, an offset committed, a success status answered — is a
   progress marker and follows the writes it confirms, never precedes them: a delivery mode that
   acknowledges on receipt acknowledges before the effect exists, and a crash between the two loses the
   unit with a record saying it was kept. A unit whose run fails is returned for redelivery — left
   unacknowledged, rejected back, or answered with a failure the sender retries — **never acknowledged
   as done.** Containing the failure, so one unit does not stop the units after it, is logged once by
   the scope that stops it (`python-logging`) and is never swallowing it (`exception-catalog` rule 15):
   a contained failure that acknowledges the unit loses it silently. Where the acknowledgement is an
   offset, which confirms every unit before it, no offset is committed past a failed unit until that
   unit has been dead-lettered (rule 2). Where the mechanism redelivers only when asked — a stream's
   pending entries — the consumer claims them back; otherwise a failed unit stays pending forever and
   never reaches the bound.
2. **Redelivery is bounded, and a unit past the bound goes to a dead letter an operator can read.** A
   unit that fails is neither acknowledged as done nor retried without bound — one that retries forever
   blocks everything behind it. Its delivery count is the mechanism's where it keeps one — a receive
   count, a delivery count, a pending entry's count — or travels with the unit, **never a counter of
   redeliveries held in the process**, which a restart resets and each replica keeps apart. The limit
   and the dead-letter destination are declared with the deployment: in the mechanism's configuration
   where it has a redrive of its own — a queue's redrive policy, a delivery limit with a dead-letter
   exchange — and otherwise in the consumer's settings, the consumer then moving the unit, intact, to
   the dead letter — a dead-letter topic, a second stream — and only then acknowledging it. The dead
   letter's depth is watched rather than discovered. A unit that can never succeed — malformed, or
   refused — goes to the dead letter directly where the mechanism allows, rather than through
   redeliveries it can never pass, and is never acknowledged and dropped. A retry around the work that
   never hands the unit back is the entrypoint's retry, not a redelivery: the count moves only when the
   unit is handed back. Where a third party delivers, its schedule is its own; the program answers a
   failure it may recover from with the response that sender retries on, and a delivery it will never
   accept with one it does not, where the sender distinguishes them.
3. **A redelivery changes nothing.** Because delivery is at least once, the unit's effect is
   idempotent under redelivery — **a second delivery of a unit already applied changes nothing.** The
   identity of what it creates and every value it writes come from the unit, **never the clock or a
   mint per delivery**: an identifier minted on receipt makes each delivery a new record, and a time
   read on receipt makes each one a different write. A unit already applied is acknowledged as done, or
   answered as a success — never failed as a conflict, which sends a unit that succeeded to the dead
   letter. An effect on a system the program does not own is made under a key derived from the unit,
   wherever that system accepts one.
4. **Arrival order is not the record's order.** A returned unit comes back after units delivered
   behind it, and two consumers take units for one key at once, so where units for one key can reach
   the store out of order, the write is the store's to guard — `persistence` rule 16, by an ordering
   stamp the unit carries and every delivery of it repeats. Where the unit carries no stamp, the
   handler writes the source's current state, read when it handles the unit, or the key keeps one
   writer (`persistence` rule 16). Never reordered in the process's memory, and never assumed from the
   order of arrival.
5. **A third party's delivery is verified against the raw body it signed, before the body is parsed.**
   The signature covers the bytes as received; a body parsed and re-serialized first is not those bytes,
   and a body parsed before it is verified has been trusted already. A delivery that fails verification
   is rejected with nothing written and is never retried into success. Where the scheme signs a
   timestamp with the body, a delivery outside the scheme's tolerance is rejected the same way, since a
   valid signature on an old body is a replay.
6. **A relay delivers each recorded effect at least once, under the record's own id, and marks it
   delivered only once the receiver has acknowledged it.** This is the sending side of the same
   guarantee: the effect was recorded with the write it follows (`exception-catalog`), and a record
   marked delivered before the receiver's acknowledgement is lost by a crash between the two, as rule 1's
   early acknowledgement loses a unit. The receiver is whoever the relay hands the effect to — a broker
   confirming the publish, an endpoint answering success — and its acknowledgement is awaited, never
   assumed from a client accepting the send. Every attempt carries the same id, never one minted per
   attempt, as the message's id or as the receiver's idempotency key wherever it accepts one, so a
   receiver idempotent by that id (rule 3, from its side) treats a redelivery as already applied; where
   the receiver accepts no key, a redelivery may repeat the effect, which is the cost of at least once.
   The relay promises no order between records unless it holds back a key's later records behind a
   failed one; a receiver that needs order has rule 4.

## Hard stops

- Writing the consumer wrapper, the HTTP route or the inbound adapter that receives the unit → stop, use
  the family's entrypoint skill (`flat-entrypoint`, in the `pyhouse-flat` plugin; `hex-architecture`, in
  the `pyhouse-hex` plugin), or the project's own entrypoint where neither is installed.
- Publishing or sending a committed write's effect straight after the write, with nothing recorded,
  where losing it costs something → stop, use `exception-catalog`; the effect is recorded atomically
  with the write and relayed under rule 6, or, where the operation is idempotent under redelivery, the
  operation fails whole and its redelivery reruns the effect.
- Applying rules 1–5 to a program reading a source that keeps no delivery state for it — a table, an
  API, a file listing → stop, they do not bind; its next run is the retry. A broker or a stream read by
  polling is not this case, and what the program relays from its own committed write is rule 6's
  whatever it reads.
