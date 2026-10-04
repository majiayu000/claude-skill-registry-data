---
name: safe-to-rerun
description: "Use when designing any job, webhook handler, command, startup step, or loop that changes state. Assume it will run twice and that the last run may have died halfway. It has to end up in the same correct state either way, or it needs a dedupe key."
disable-model-invocation: true
kind: principle
---

# Safe to rerun

Anything that can be triggered twice will be. Webhooks redeliver. Jobs restart. Users double-click. Networks retry. Agents get interrupted and pick up again. Design every state-changing operation so running it again is safe.

Every operation that changes state answers two questions. What happens if this runs twice? What happens if the last run crashed halfway through? If the answer to either is "it depends on what got left behind", the operation isn't done.

## If it can't be made safe, dedupe it

Some operations can't be replayed, like charging a card or sending an email. Those need a dedupe key. An idempotency key on the request, a unique constraint on the record, an "already processed" check keyed on the event id. The second run sees the key and does nothing.

## Patterns

- **Converge on startup.** Scan for existing state, clean up stale artifacts, adopt anything still live. Don't assume you're starting from nothing.
- **Compare by content, not by order.** When cleaning up, decide what's stale by what it contains, not by when it was created.
- **Locks that heal themselves.** A lock file records who holds it and whether that process is still alive. A dead holder means a stale lock, and the next run takes it.
- **Failed work respawns clean.** A job that dies gets rescheduled from fresh input, not from whatever half-state it left.
- **Reconcile when you have to.** If an operation can't be made naturally convergent, add a step at the start that looks at what's there and brings it to a known state before doing anything.

## The test

1. Run it twice in a row. Same result?
2. Kill it at every possible point, then run it again. Same result?
3. Does the second run end in the same state as a clean first run would?

Three yeses or a dedupe key. Nothing else ships.
