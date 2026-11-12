---
name: error-handling-conventions
description: Handle errors with cause chains, typed results, one API error envelope, no log-and-throw, and no empty catch. Use when writing or reviewing error handling in TypeScript files.
license: MIT
compatibility: "Claude Code"
---

# Error-handling rules

- Preserve the cause chain: rethrow with `cause`, for example `throw new AppError("...", { cause: err })`, rather than replacing the original error with a bare `throw new Error(msg)`.
- Prefer an explicit result over null-as-failure. A function that can fail returns a typed result or union such as `{ ok: true, data? } | { ok: false, error }`, or throws. Never use untyped `null` or `undefined` as the failure signal.
- Use one API error envelope: `{ error: { code, message, details? } }`. The machine code uses `SCREAMING_SNAKE_CASE`; the message is for humans. Never expose a stack trace to the client.
- Do not log and throw the same error. Either handle and log it, or propagate it. Doing both creates duplicate logs and false alerts.
- Do not use an empty `catch {}`. Swallowing an error requires a one-line comment that explains why it is correct, and it is almost never correct.
- Exceptions are not control flow. An expected missing record is a typed result, not a try/catch around the happy path.
