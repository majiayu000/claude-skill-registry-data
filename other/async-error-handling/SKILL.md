---
id: javascript.async-error-handling
name: JavaScript Async Error Handling
description: >
  Reviews and refactors asynchronous JavaScript error handling so Promise-based code avoids swallowed failures, unhandled rejections, unclear fallback behavior, and weak failure contracts.
stack:
  - JavaScript
  - TypeScript
category: javascript
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - async error handling
  - promise errors
  - unhandled promise rejection
  - async await catch
  - retry logic
  - fallback behavior
  - promise chains
  - async loops
compatibility:
  runtime:
    browser: true
    node: true
---

# JavaScript Async Error Handling

## Purpose

Use this skill to review, refactor, or implement safe error handling for asynchronous JavaScript code.

The goal is to prevent swallowed errors, unhandled promise rejections, duplicated catch blocks, unclear control flow, and unsafe fallback behavior.

This skill applies to plain JavaScript, TypeScript, Node.js, browser code, frontend services, API clients, scripts, and test utilities.

## When to Use

Use this skill when the task involves:

- `async` / `await`
- Promises
- `try` / `catch`
- `.then()` / `.catch()` chains
- API request error handling
- retry logic
- fallback values
- error propagation
- unhandled promise rejection warnings
- async code inside loops, callbacks, or event handlers

## When Not to Use

Do not use this skill when:

- the task is only about synchronous validation
- the problem belongs specifically to RxJS Observable error handling
- the task is only about HTTP status mapping in a framework-specific interceptor
- the code already has a domain-level error strategy and the request does not ask to change it
- the change would hide business errors behind generic fallbacks

## Do

Identify every async boundary involved in the requested change:

- public async functions
- event handlers
- API calls
- service methods
- promise chains
- dynamic imports
- file/network operations
- timers
- task queues
- test setup and teardown

Choose one explicit error contract per boundary:

- throw or reject when the caller must handle the failure
- return a typed result object when failure is part of normal flow
- return a fallback only when the fallback is correct and safe
- log and rethrow when the failure must be observable upstream

Prefer `async` / `await` for imperative flows:

```js
async function loadUser(userId) {
  try {
    return await userApi.getUser(userId);
  } catch (error) {
    throw new Error("Unable to load user", { cause: error });
  }
}
```

Never swallow errors silently:

```js
try {
  await saveData(data);
} catch (error) {
  logger.warn("Save failed", error);
  throw error;
}
```

Preserve stack and context when wrapping errors.

Avoid catch-all fallbacks unless empty data is semantically valid.

Handle parallel async flows intentionally:

- `Promise.all` for all-or-nothing work
- `Promise.allSettled` for valid partial success

Avoid floating promises unless intentionally fire-and-forget:

```js
void saveAuditLog(payload).catch((error) => {
  logger.warn("Audit log failed", error);
});
```

Use `for...of` with `await` for sequential async loops and `Promise.all` for parallel loops.

Test failure paths:

- rejected promise
- thrown async error
- fallback branch
- retry exhaustion
- partial success
- error propagation

## Do Not

Avoid empty catch blocks.

Avoid returning fake success from failed async work.

Avoid `forEach` with async callbacks.

Avoid unhandled promise rejections.

Avoid `Promise.allSettled` when fail-fast behavior is required.

Avoid retries without backoff or limits.

Avoid masking authentication or authorization failures as empty data.

## Review Checklist

- [ ] Every Promise is awaited, returned, or explicitly handled.
- [ ] Every catch block either recovers safely or rethrows.
- [ ] Fallback values are semantically valid.
- [ ] User-facing errors are separated from technical errors.
- [ ] Failure paths are tested.
- [ ] No unrelated async refactor was introduced.

## Expected Output

1. Identify async boundaries.
2. Choose a clear error contract.
3. Preserve stack and context.
4. Avoid swallowed or floating failures.
5. Add or update tests for success and failure paths.
