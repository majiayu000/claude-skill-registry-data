---
name: error-handling-patterns
description: How to handle errors explicitly and consistently across an app — validate at boundaries, classify operational vs programmer errors, add context while propagating, retry transient failures with backoff, and never swallow. Covers JS/Python/Go/Rust patterns with runnable checks.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Error Handling Patterns

Errors are part of the contract, not an afterthought. A robust system **handles errors where it can act,
propagates them where it can't, and never lets a failure vanish silently**. This skill is the deep
reference: the decisions, the trade-offs, and the anti-patterns. Heavy detail lives in `references/`,
copy-paste material in `examples/`, and a runnable linter for swallowed errors in `scripts/`.

## Mental model

Every error sits on two axes that decide what you do with it:

| Axis | Question | Consequence |
|---|---|---|
| **Operational vs programmer** | Is this an expected runtime condition (network down, bad input) or a bug (null deref, broken invariant)? | Operational → recover/retry/surface. Programmer → fail fast, let it crash, fix the code. |
| **Recoverable vs fatal** | Can the caller do something useful about it here? | Yes → handle locally. No → add context and propagate. |

Classifying wrong is the root cause of most bad error handling: retrying a programmer bug forever, or
crashing the process over a single bad HTTP request. The full taxonomy is in
[`references/error-taxonomy.md`](references/error-taxonomy.md).

## The five rules

1. **Validate at the boundary.** Reject bad input early with a clear, specific message (fail fast). Never
   trust data crossing a trust boundary — HTTP bodies, env vars, file contents, API responses.
2. **Classify the error.** Operational errors are values you handle; programmer errors are bugs you
   surface loudly. Don't `catch` a `TypeError` to "be safe".
3. **Add context as you propagate.** Wrap with *what you were doing* and preserve the original cause and
   stack (`new Error(msg, { cause })` in JS, `fmt.Errorf("...: %w", err)` in Go).
4. **One owner for user-facing messaging.** Translate to a friendly message at the edge (the HTTP layer,
   the UI). Keep full detail in server-side logs only — never leak stack traces to users.
5. **Never swallow.** An empty `catch {}`, a bare `except: pass`, or a `.catch(() => {})` is a defect.
   Run `scripts/lint-empty-catch.mjs` in CI to catch these automatically.

## Adding context without losing the cause

The single most valuable habit: wrap errors with context while chaining the original, so the final log
shows the full causal trail from the low-level failure up to the request that triggered it.

```js
// Node 16.9+ supports the standard `cause` option on Error.
async function placeOrder(userId, cart) {
  try {
    const order = await db.orders.insert({ userId, items: cart.items });
    return order;
  } catch (err) {
    // Wrap: keep the DB error as `cause`, add the business context.
    throw new Error(`failed to place order for user ${userId}`, { cause: err });
  }
}
```

```python
# Python's `raise ... from` preserves the chain (shown as "The above exception
# was the direct cause of the following exception" in the traceback).
def place_order(user_id, cart):
    try:
        return db.orders.insert(user_id=user_id, items=cart.items)
    except DBError as err:
        raise OrderError(f"failed to place order for user {user_id}") from err
```

Language-by-language patterns (try/catch vs `Result`/`Either` vs panics) are in
[`references/language-patterns.md`](references/language-patterns.md).

## Retrying transient failures

Only **operational, transient, idempotent** failures are safe to retry — a 503 or a connection reset,
not a 400 or a `NullPointerException`. Retry with **exponential backoff plus full jitter** to avoid
synchronized retry storms (the "thundering herd"), and always cap attempts and total time.

```js
async function withRetry(fn, { retries = 4, baseMs = 100, isRetryable } = {}) {
  let attempt = 0;
  for (;;) {
    try {
      return await fn();
    } catch (err) {
      attempt++;
      if (attempt > retries || (isRetryable && !isRetryable(err))) throw err;
      const backoff = baseMs * 2 ** (attempt - 1);
      const jittered = Math.random() * backoff; // full jitter
      await new Promise((r) => setTimeout(r, jittered));
    }
  }
}
```

When NOT to retry, circuit breakers, and budgets are covered in
[`references/retry-and-backoff.md`](references/retry-and-backoff.md).

## Common pitfalls (anti-patterns)

- **Swallowing errors** — empty `catch {}`, `except: pass`, `.catch(() => {})`, or `if err != nil {}` in
  Go. The failure disappears and you debug blind. This is the #1 defect; lint for it.
- **Catch-log-rethrow-wrapped duplication** — logging *and* rethrowing at every layer produces the same
  error logged ten times. Log once, at the boundary that owns the response.
- **Catching too broadly** — `except Exception` or `catch (e)` that also eats `KeyboardInterrupt`,
  programmer bugs, or `OutOfMemory`. Catch the narrowest type you can actually handle.
- **Returning a sentinel instead of erroring** — returning `null`/`-1`/`{}` on failure forces every
  caller to remember the magic check; most won't. Prefer throwing or a `Result` type.
- **Leaking internals to users** — returning raw stack traces or SQL errors is both bad UX and a security
  leak (reveals schema, file paths, library versions).
- **Retrying non-idempotent or non-transient operations** — retrying a `POST /charge` on timeout can
  double-charge; retrying a `400` just wastes time. See the retry reference.
- **Losing the original cause** — `throw new Error("save failed")` without `{ cause }` discards the stack
  that tells you *why*.

## When NOT to use / trade-offs

- **Don't catch programmer errors to keep running.** A bug that corrupted state should crash the process
  (let a supervisor like systemd/k8s/PM2 restart it clean) rather than limp along with bad data.
- **Don't add a `Result`/`Either` type to a small script** — the ceremony outweighs the benefit. Plain
  exceptions are fine when there's one boundary and one owner.
- **Don't retry by default.** Retries amplify load during incidents and can mask a real outage; only
  retry classified-transient, idempotent calls, and always with a budget.
- **Defensive `try/catch` everywhere is a smell**, not safety. It scatters handling, hides bugs, and
  makes control flow unreadable. Handle at meaningful boundaries.

## Files in this package

- [`references/error-taxonomy.md`](references/error-taxonomy.md) — operational vs programmer errors, and how the distinction drives recovery
- [`references/retry-and-backoff.md`](references/retry-and-backoff.md) — when to retry, exponential backoff, jitter, circuit breakers, budgets
- [`references/language-patterns.md`](references/language-patterns.md) — try/catch vs `Result`/`Either` vs panics across JS, Python, Go, Rust
- [`examples/express-error-middleware.js`](examples/express-error-middleware.js) — a complete centralized error handler with an `AppError` class
- [`examples/result-pattern.ts`](examples/result-pattern.ts) — a typed `Result<T, E>` with helpers, no exceptions for expected failures
- [`scripts/lint-empty-catch.mjs`](scripts/lint-empty-catch.mjs) — runnable Node linter that flags swallowed errors; supports `--selftest`

Pairs with the `code-reviewer` agent, the `silent-failure-hunter` agent, the `rest-api-design` skill
(for the HTTP error envelope), and the `owasp-top10` skill (for not leaking sensitive data in errors).
