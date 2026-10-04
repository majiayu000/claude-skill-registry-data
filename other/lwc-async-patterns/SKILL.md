---
name: lwc-async-patterns
description: "Async/await and Promise patterns in LWC: imperative Apex, loading states, error handling, concurrent wire + imperative, AbortController for in-flight cancellation, Promise.all for parallel calls. NOT for the basic imperative Apex import-and-call pattern or cacheable=true rules — use lwc/lwc-imperative-apex. NOT for @wire provisioning basics — use lwc/wire-service-patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - User Experience
tags:
  - lwc
  - async
  - promise
  - imperative-apex
  - abortcontroller
triggers:
  - "lwc imperative apex async await loading state"
  - "lwc promise.all parallel apex call performance"
  - "lwc abortcontroller cancel inflight fetch on navigate"
  - "lwc unhandled promise rejection swallowed error"
  - "lwc wire + imperative call race condition"
  - "async error lwc toast user feedback"
inputs:
  - Data needs (imperative vs wire)
  - Parallel vs serial requirements
  - Cancellation semantics
outputs:
  - Async handler with try/catch + finally
  - Loading-state management
  - AbortController usage (where applicable)
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-05-19
---

# LWC Async Patterns

Activate when writing asynchronous logic in LWC — imperative Apex calls, fetch to external endpoints, or complex orchestration of multiple data sources. LWC supports `async`/`await` natively; getting loading states, error handling, and cancellation right separates a polished component from a flaky one.

## Before Starting

- **Decide imperative vs wire.** Wire is reactive and caches; imperative runs on demand and surfaces errors/loading cleanly.
- **Identify parallel opportunities.** Multiple independent calls → `Promise.all`.
- **Plan cancellation.** Long-running fetches need `AbortController` to avoid setState-on-unmounted.

## Core Concepts

### Imperative Apex with async/await

```
import getAccounts from '@salesforce/apex/AccountService.getAccounts';

async handleLoad() {
    this.isLoading = true;
    try {
        this.accounts = await getAccounts({ region: this.region });
    } catch (err) {
        this.error = err.body?.message ?? 'Unknown error';
    } finally {
        this.isLoading = false;
    }
}
```

### Parallel calls

```
const [accs, cons, opps] = await Promise.all([
    getAccounts(),
    getContacts(),
    getOpportunities()
]);
```

Fails fast — first rejection aborts. Use `Promise.allSettled` if partial results are acceptable.

### AbortController for cancellation

```
this.controller?.abort();  // cancel prior
this.controller = new AbortController();

try {
    const resp = await fetch(url, { signal: this.controller.signal });
    // process
} catch (e) {
    if (e.name === 'AbortError') return;  // expected cancellation
    throw e;
}
```

### Race-condition guard: stale responses

If the user changes filter while a call is in flight, a late response can overwrite fresh state. Track a request Id:

```
const reqId = ++this.latestReqId;
const data = await getData(...);
if (reqId !== this.latestReqId) return;  // stale
this.data = data;
```

### Loading + error states

```
@track isLoading = false;
@track error;
@track data;
```

Template:

```
<template if:true={isLoading}><lightning-spinner /></template>
<template if:true={error}><c-error-banner message={error} /></template>
<template if:true={data}><!-- content --></template>
```

## Common Patterns

### Pattern: Debounced search with cancellation

```
handleSearch(e) {
    clearTimeout(this.timer);
    this.timer = setTimeout(async () => {
        this.controller?.abort();
        this.controller = new AbortController();
        try {
            this.results = await searchApex({ q: e.target.value });
        } catch (err) {
            if (err.name !== 'AbortError') this.error = err;
        }
    }, 300);
}
```

### Pattern: Retry with exponential backoff

```
async fetchWithRetry(fn, retries = 3, delay = 500) {
    for (let i = 0; i < retries; i++) {
        try { return await fn(); }
        catch (e) {
            if (i === retries - 1) throw e;
            await new Promise(r => setTimeout(r, delay * 2 ** i));
        }
    }
}
```

### Pattern: Dependent chained calls

```
const user = await getUser();
const [orders, tickets] = await Promise.all([
    getOrders(user.id),
    getTickets(user.id)
]);
```

## Decision Guidance

| Situation | Approach |
|---|---|
| Reactive data that updates with context | `@wire` |
| On-demand fetch (button click) | imperative + async/await |
| Multiple independent calls | `Promise.all` |
| Partial-success acceptable | `Promise.allSettled` |
| User can navigate away mid-fetch | `AbortController` |
| User rapidly retypes a query | debounce + cancel prior |

## Recommended Workflow

1. Classify each call as wire or imperative.
2. For imperative, wrap in try/catch with `finally` resetting loading state.
3. For multiple calls, use `Promise.all` when order doesn't matter.
4. Add `AbortController` or request-id guards to prevent stale updates.
5. Surface errors via `ShowToastEvent` (sticky for errors) OR inline banner.
6. Test with slow-network throttling in browser devtools.
7. Ensure unmount path clears pending timers / aborts controllers.

## Review Checklist

- [ ] try/catch wraps every imperative call
- [ ] `finally` resets loading state
- [ ] `Promise.all` used where calls are independent
- [ ] Stale-response guard (AbortController or request id) present for filter/search UIs
- [ ] Unmount path cancels in-flight work
- [ ] Error branch displays meaningful message (not raw Error stringify)
- [ ] No unhandled promise rejections (don't swallow errors silently)

## Salesforce-Specific Gotchas

1. **Imperative Apex errors have shape `{body: {message}}`** — not `.message` directly. Always `err.body?.message`.
2. **LWC does NOT expose a `componentWillUnmount` lifecycle hook.** Use `disconnectedCallback` to abort in-flight work.
3. **`@wire` cannot be cancelled** — if you need cancellation semantics, switch to imperative.
4. **Awaiting inside `connectedCallback` blocks rendering if synchronous.** Prefer dispatching the async work and updating `@track` fields as results arrive.

## Output Artifacts

| Artifact | Description |
|---|---|
| Async handler utility | `try/catch/finally` + loading state template |
| AbortController wrapper | Cancellation helper for fetch/Apex |
| Retry-with-backoff helper | Shared exponential retry |

## Related Skills

- `lwc/lwc-wire-refresh-patterns` — wire vs imperative tradeoffs
- `lwc/lwc-show-toast-patterns` — error feedback
- `apex/apex-http-callout-mocking` — server-side mock tests
