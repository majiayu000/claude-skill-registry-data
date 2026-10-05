---
name: streaming/selector-lifecycle
description: >-
  Choose StreamingStore selector call/subscription timing and withStore bindings.
  Direct Kefir calls require init() and are invalid after disposal; Store
  construction and teardown belong to streaming/store.
type: sub-skill
requires:
  - streaming
  - streaming/selectors
sources:
  - "@themislib/themis/streaming-store"
  - package-internal streaming selector implementation
  - "@themislib/themis/docs/SELECTORS.md"
triggers:
  - stream selector lifecycle
  - observe selector stream
  - streaming selector before init
  - streaming selector teardown
  - withStore stream
---
# Streaming selector lifecycle

Use this skill to decide when a Streaming selector can be invoked, observed, or bound to an alternate StreamingStore.

Use it only for apps that chose the Streaming Store family. Do not combine these Streaming lifecycle/setup rules with alternate Store or selector lifecycle/setup patterns in the same app.

For construction, initialization, and whole-Store shutdown, read `../store/SKILL.md` — **Lifecycle rules** and **Process bootstrap**. This leaf owns when consumers may call and observe selectors, not how the Store runtime is initialized or disposed.

## Lifecycle map

| Phase/context | Correct action | Why |
| --- | --- | --- |
| Module setup | Define selectors with streamStore.createSelector(...) | Creation stores the selector callback; it does not read stream state yet. |
| Before init() | Avoid direct selector calls | They need the initialized Store-owned Kefir state stream. |
| After init() | Call selectFoo(...args) for a Kefir observable | The Store state stream is available. |
| Tests/composition | Use selectFoo.select(state, ...args) | Pure synchronous selector path, no Store lifecycle needed. |
| Sagas | Use yield* selectFoo.effect(...args) | Keeps named selector ownership and typed-redux-saga style. |
| Explicit StreamingStore binding | Use selectFoo.withStore(streamStore)(...args) | Binds to another initialized StreamingStore. |
| Consumer teardown | Unsubscribe each consumer when its owner ends, before whole-Store shutdown | Consumer ownership is separate from the Store lifetime in ../store/SKILL.md — **Lifecycle rules**. |

## Operational guardrails

- Direct selector calls intentionally throw before `init()` and after `dispose()`; do not hide that error with fallback empty streams.
- A direct selector call returns a Kefir observable. Manage observation/teardown using the consuming app's Kefir subscription pattern.
- Output reuse does not extend the valid invocation window; see `../selectors/SKILL.md` — **Selector caching** for the identity/cache contract.
- `.withStore(...)` accepts another initialized StreamingStore; use it for tests/integration adapters that own their own initialized Store state.
- For non-subscription read forms, use `../selectors/SKILL.md` — **Call forms**. Selector-driven saga subscriptions instead follow `../../core/selector-channels/SKILL.md` — **Do** and **Implementation cues**, including the plain-argument tuple and saga-context state contract.

## Consumer subscription ownership

The process bootstrap in `../store/SKILL.md` — **Process bootstrap** initializes
the Store before starting consumers. Each Kefir consumer retains its own
subscription and stops it before that Store owner shuts down. For example, an
app-owned `startConsumers` function can return the observer's cleanup:

```ts
function startConsumers() {
  const subscription = selectTodoCount().observe(handleTodoCount);
  return () => subscription.unsubscribe();
}
```

Use the same ownership pattern for direct public diagnostic-stream observations;
the logger's own lifecycle remains in `../../core/redux-action-logging/SKILL.md` —
**Logger factory lifecycle** and **Store-owned logging streams**. Do not import internal emitters to subscribe.

## Verification cues

- Examples initialize the `StreamingStore` before direct selector invocation.
- Pre-init or post-dispose behavior is either avoided or explicitly tested as the documented selector state error.
- Streaming guidance instructs agents to initialize the `StreamingStore` before direct observable observation.