---
name: typescript
description: >
  Tommy's TypeScript style rules and philosophy: simple explicit code in the style of
  Mario Zechner (badlogic) and Anthony Fu (antfu), few abstractions and little
  indirection, named constants instead of magic numbers, AbortSignal on every I/O,
  fetch or sleep operation, object params instead of 2+ positional args, and type-safe
  errors as values with errore. ALWAYS load this skill before writing, refactoring or
  reviewing TypeScript code.
---

# typescript

Simple code a reader understands top to bottom in one pass. Every failure mode is visible
in the return type. Also load the `errore` skill: it is the error convention.

## Philosophy

Write TypeScript in the style of **Mario Zechner** (badlogic, creator of pi mono) and
**Anthony Fu** (antfu). Simple, explicit, a few but elegant abstractions where they are
really worth it.

- **Few abstractions.** Only when they remove real duplication or complexity. Three similar
  lines beat a premature helper.
- **Little indirection.** Plain functions and objects. No jumping through files, factories,
  registries or class hierarchies to find what a call does.
- **Explicit over clever.** No metaprogramming, proxies, decorators or type gymnastics
  unless the gain is large.
- **Architecture first.** Know each system boundary; put logic at the right layer instead of
  patching around a flaw.
- **Flat control flow.** Early returns, no `else` chains, no nested `if`.
- **Derive, do not cache.** Minimize mutable state; compute from the source of truth.

## No magic numbers

Name every number in an `UPPER_SNAKE_CASE` constant at the top of the file, unit in the
name, numeric separators for large values. Same for repeated literal strings.

```ts
const REQUEST_TIMEOUT_MS = 30_000
const MAX_UPLOAD_BYTES = 10 * 1024 * 1024
const HTTP_NOT_FOUND = 404
```

- No constant needed for `0`, `1`, `-1` index math, `* 2`, `% 2`.
- Shared constants go next to the owning module or in one `constants.ts`, never one file
  per value.

## Object params

Two or more params means one object, so call sites use named arguments. Inline the param
type in the signature; extract a named type only if other code uses it. Defaults go in the
destructuring.

```ts
await copyFile({ from: src, to: dest, overwrite: true, signal })
```

- One positional arg is fine when obvious: `slugify(title)`.
- Callbacks for `.map` and library APIs keep the shape the API requires.

## AbortSignal on every long running action

Any function doing I/O, `fetch`, child processes, `sleep`, polling or long timeouts MUST
take a **required** `signal` in its object args and pass it to every async call inside.
The caller owns the `AbortController`. An optional signal gets forgotten and silently
breaks cancellation in one layer.

```ts
const user = await getUser({ id, signal: controller.signal })
```

**Timeouts:** use `AbortSignal.any` + `AbortSignal.timeout`, never manual `setTimeout` +
`abort()`.

```ts
const res = await fetch(url, {
  signal: AbortSignal.any([signal, AbortSignal.timeout(REQUEST_TIMEOUT_MS)]),
}).catch((e) => new NetworkError({ url, cause: e }))
if (errore.isAbortError(res)) return res
if (res instanceof Error) return res
```

**Loops:** check `signal.aborted` before each expensive step.

```ts
for (const file of files) {
  if (signal.aborted) return new JobAbortedError({ cause: signal.reason })
  const result = await uploadFile({ file, signal })
  if (result instanceof Error) return result
}
```

**Sleep:** never `new Promise((r) => setTimeout(r, ms))`. Use a sleep that stops on abort:

```ts
export function sleep({ ms, signal }: { ms: number; signal: AbortSignal }) {
  return new Promise<SleepAbortedError | void>((resolve) => {
    const onAbort = () => {
      clearTimeout(timer)
      resolve(new SleepAbortedError({ cause: signal.reason })) // extends errore.AbortError
    }
    const timer = setTimeout(() => {
      signal.removeEventListener('abort', onAbort)
      resolve()
    }, ms)
    if (signal.aborted) return onAbort()
    signal.addEventListener('abort', onAbort, { once: true })
  })
}

await sleep({ ms: RETRY_DELAY_MS, signal: controller.signal })
```

## Type-safe errors with errore

Follow the `errore` skill. Errors are known and each function's failure modes are explicit
in its inferred return type, e.g. `Promise<UserNotFoundError | NetworkError | User>`.

- Return errors, never throw expected failures.
- Convert exceptions only at boundaries (`.catch()` async, `errore.try` sync), wrapped in a
  tagged error with `cause`.
- Abort errors extend `errore.AbortError`, detected with `errore.isAbortError`.
- Use `errore.matchError` when callers handle each failure mode differently.
