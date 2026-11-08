---
name: observability-record
kind: pattern
rule: observability
description: Pattern of rule observability. Load when a new log line is added in code — the ready-made logger call, choosing the level, the line name, fields as an object, an external service failure and the wait limit. Not for editing the logger itself and the request context — that is rule observability.
---
<!-- rt-kit v0.34.0 · patterns/observability-record.md · 394a56cf9674 · правится надстройкой, не здесь -->

# A new log line

Pattern of the rule `observability`. What must be true — the law
`docs/constitution/observability.md`.

## When to use

- A place appeared in the domain that the owner must learn about: an automatic step did not
  fire, an external service refused, a procedure fell.
- One wants to put a `console.log` — a log line is put instead.

## The domain logger is taken once

```ts
const LOG_CONTEXT: string = 'PageCache';

readonly #log: ScopedLogger;

constructor(logger: AppLoggerService) {
    this.#log = logger.scope(LOG_CONTEXT);
}
```

The context is set once and as a module constant, not as a literal in the call: neighbouring
classes of one domain write under the same source, and the failure selection judges exactly by
it. The request number, the procedure and who is in the system the logger substitutes itself —
there is no need to pass them as fields.

## The line name is constant, everything that changes goes into the fields

```ts
✓ this.#log.warn('cache.refresh.rejected', { url, attempt, status, durationMs });
✗ this.#log.warn(`cache refresh rejected for ${url} after ${attempt} attempts`);
```

The first argument is the line name, not a sentence. By it the lines about the same thing are
gathered together, and by it they collapse into one row of the failure feed. A value substituted
into the name makes every line unique.

The name is written with dots from the general to the particular: `cache.refresh.rejected`,
`mail.owner.skipped`.

The fields are scrubbed automatically. The line name passes scrubbing only on its way to the
failure store — in the output it is printed as is — so substituting values into it is forbidden
for this reason too.

## A lower-level line needs an entry in the selected list

The failure level and everything above it goes to the failure store by itself. A line of a lower
level gets there only if its name stands in the list of selected names. The list is compared by
the start of the name and edited by the same commit as the place that writes this line.

Forgot to append — the line stays only in the container output, and the owner never learns of it.
Nothing checks this.

## The level is chosen by whether something broke

| Level       | When                                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| failure     | the application did not do what it must: a procedure fell, a write to the storage did not go through                    |
| below       | an automatic step did not fire: a translation, a cache refresh, a poll of an external service. Also a failure on input and rights |
| message     | an action that took place and is worth knowing about: the call went through, the mail went out                          |
| detail      | what is needed in an investigation and not needed in production                                                          |

A guest failing a check, a miss in a form and "not found" are the level below failure. The check
fired, the application works.

## An external service failure is written parsed

```ts
} catch (error: unknown) {
    this.#log.error('mail.send.failed', { to: maskEmail(to), error: describeError(error) });
}
```

Parsing the cause puts the class, the text, the code and a trimmed stack in one shape — the same as
the other failures have. Substituting the error into text (`` `failed: ${String(error)}` ``) is
forbidden: that way a foreign text goes into the log whole, together with the guest's address, key
or mail.

Mail is masked at the call site if it comes as a separate value: scrubbing recognises it by field
name, and a name like `to` does not look like mail.

## A failure comes only when the call has a wait limit

```ts
/**
 * Waiting for the rates source. The rate is a reference value and is refreshed once
 * a day: five seconds of waiting with the previous rate in place is better than
 * five minutes of a busy schedule.
 */
const RATES_TIMEOUT_MS: number = 5_000;

const response: Response = await fetch(RATES_URL, { signal: AbortSignal.timeout(RATES_TIMEOUT_MS) });
```

Without a limit the connection to a silent service lives up to the environment default — minutes
— and all that time `catch` does not come: there is nothing to write. The number stands next to
the client with its own reason, because the price of waiting differs per service: a guest inside a
request waits differently from a night schedule.

## Common misses

- **The same line name stands in two places.** Then two different situations read as one. Either
  the names differ, or the place is one.
- **`console.log` instead of a log line.** It has neither a level nor a request number, and it
  does not get into the selection. In production it is a line nobody will see.
- **The level is chosen by how unpleasant it is.** A guest failing a check is unpleasant, but the
  application works meanwhile.
- **The error is put into a field as is, without parsing the cause.** The error object serialises
  into an empty `{}`, and neither the text nor the class is left in the log.
- **An unfilled part of the group key stands as an omission, not as an empty string.** Two
  failures without a procedure and without a work subject must fall into one group; with an
  omission in the key each opens its own, and the feed fills with single rows about the same
  thing.
- **Identical failures that came at once give two groups.** Between "no such group yet" and the
  insert the second one gets through, so the case is handled not by a check before the insert but
  after the insert did not go through.
- **A log line name longer than the key limit is not written at all.** It is assembled by
  substitution and limited by nothing, while the key has a limit: without trimming, a failure
  with a long name is lost silently — no row in the feed, no failure in the logs.
