---
name: error-handling
description: "Handle errors explicitly: typed errors, no silent swallowing, no catch-all. Cover failure modes, timeouts, retries with care."
---

# error-handling

Every failure has a type, a boundary where it's translated, and a test. Silence is never handling.

## Activate when

- Designing error flows, reviewing catch blocks, or fixing swallowed/misreported failures.

## Do NOT activate for

- Language syntax (see languages/*); retry topology across services (see distributed/systems).

## Inspection

Find every catch/except, every `unwrap`/bare `except`, every error-to-status mapping, and every retry loop. Classify: typed, swallowed, mistranslated, or retried-blindly.

## Decision rules

- Typed errors at boundaries (thiserror/enums/RFC-7807 types); `anyhow`/context chains inside apps, never across library APIs.
- No silent swallowing: log with context or propagate — `except: pass` and empty catches are defects. Interrupts (`KeyboardInterrupt`, cancellation) are never swallowed.
- Translate once at each trust/layer boundary (infra error → domain error → user-safe message); never leak internals to clients.
- Retries only for idempotent operations with jitter + budgets; timeouts on every call; circuit breaking across repeated failure.

## Procedure

1. Type the error surface per boundary; remove bare catches.
2. Add translation layers with tests per mapping (infra → domain → user).
3. Bound retries/timeouts; prove the worst case terminates.
4. Verify: fault-injection pass (each dependency failing), error-contract tests green, no stack traces or secrets in client responses.

## Failure modes

- Catch-all around business logic; retries amplifying outages; timeouts longer than callers'; user-enumeration via distinct error messages; log-and-continue on corruption paths.

## Escalation

Distributed retries/breakers → distributed/systems; API error contracts → architecture/api-design.

## References

- Related: `../../backend/validation/`, `../../core/debugging/`.
