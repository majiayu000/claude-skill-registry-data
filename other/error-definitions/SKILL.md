---
name: error-definitions
category: observability
description: Use before proposing error definitions (propose_error_definitions) - how to read an error group, pick its category and action, write a match that catches one kind of error and nothing else, and when a definition should not be proposed at all
---

# Error definitions

An error definition says what one kind of runtime error means and what happens when it recurs. A person accepts or dismisses each one you propose, so every proposal has to stand on its own: a name a person recognises, a match they can read, a category and action they would have chosen, and a one-sentence rationale.

## Category: what it is

| Category | It is | Usual action |
|---|---|---|
| `bug` | this code does the wrong thing (a nil dereference, an unhandled case, a wrong query) | `task` — one developer task per new group; `incident` if it breaks a core flow |
| `expected` | a designed outcome logged at error level (a cancelled checkout, a webhook for an unknown event, a cache miss logged loudly) | `ignore`, or `none` to keep it visible but labelled |
| `user_error` | input the code rejects correctly (validation, not found, unauthorised, rate limited) | `ignore` unless a sudden rise would mean an attack or a broken client — then `alert` with a threshold |
| `dependency` | a downstream service or API failing (timeouts, 5xx from a provider, a broker disconnect) | `alert` with a threshold: one timeout is noise, fifty in ten minutes is an outage |
| `infrastructure` | the platform itself (out of memory, disk full, DNS, the database refusing connections) | `incident` |

Read the code before you choose: the line that raises it, and what its callers do with it. A `404` the API returns on purpose is `user_error`; a `404` the service gets back from its own storage is a `bug` or a `dependency`.

## Match: one kind of error, nothing else

Every field you set must hold.

- `fingerprint` — exactly one group. Use it when the group is one specific failure and its message would match too much.
- `message_regex` — a family. Anchor on the words that never change (`^payment provider timeout`), escape what is literal (`\(`, `\.`), and never include an id, a timestamp, an amount or a host that varies between occurrences. Test it mentally against two different groups of the family.
- `exception_type` — the class or error type as printed before the first `:`; a bare name (`TimeoutError`) matches its qualified form.
- `endpoint` (`POST /v1/charges`, `/v1/orders/*`) and `status` (`504`) — when the message prints them, to tell the same exception on two routes apart.
- `attributes` — exact `key=value` pairs the message prints (`tenant=acme`), or `source` / `provider`.

A match that also catches unrelated groups is worse than none: an `ignore` hides real failures and an `alert` pages for the wrong thing. When in doubt, narrow it.

## Thresholds

For `alert` and `incident`, set `alert_threshold` from what the group does today: its `count` over a window in `list_error_groups`. A dependency that times out three times an hour normally wants an alert at, say, twenty in ten minutes — not at one. Leave it out and the defaults apply (alert: 10 in an hour; incident: any occurrence).

## Severity

`critical` only when a core flow is down for everyone; `high` when users notice; `medium` for degraded but working; `low` for noise you still want counted.

## Evidence and rationale

`evidence`: the group fingerprints it matches and the `file:line` that raises it. `rationale`: one sentence a person reads in the Errors page before accepting — "Raised in payments/client.go:88 when the provider exceeds 5 s; retried once, so a burst means the provider is down."

## Do not propose

- A group you could not trace to code — say in your reply that it is unexplained instead.
- A definition for a group that already carries one (`definition` is set in `list_error_groups`).
- Anything whose only purpose is to make the inbox look empty. `ignore` is for errors that are genuinely expected, never for defects nobody has fixed yet.
