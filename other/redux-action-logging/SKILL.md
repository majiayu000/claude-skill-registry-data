---
name: core/redux-action-logging
description: >-
  Use when configuring logReduxActions or inspecting dispatch logs, state
  diffs, and reduxAction stream events across Store families. Owns shared
  traceStreams/loggerFactory lifecycle.
type: sub-skill
requires:
  - core
triggers:
  - redux action logging
  - logReduxActions
  - redux dispatch logging
  - action state diff
  - Store loggerFactory
  - Store traceStreams
---
# Redux action logging

Use this skill when an agent needs to diagnose a dispatch by reading the Redux
action logger. This is a construction-time diagnostic for the shared Store
runtime; it is separate from selector tracing and from the browser devtools
inspection API.

## 1. Enable it for a focused reproduction

Pass `logReduxActions: true` in the **third Store constructor argument**. Pass
`undefined` as the middleware argument when no middleware is configured.

```ts
import { Store } from '@themislib/themis/svelte-store';
import { ReactStore } from '@themislib/themis/react-store';
import { StreamingStore } from '@themislib/themis/streaming-store';

const svelteStore = new Store(reducers, undefined, { logReduxActions: true });
const reactStore = new ReactStore(reducers, undefined, { logReduxActions: true });
const streamingStore = new StreamingStore(reducers, undefined, { logReduxActions: true });
```

Use the constructor corresponding to the app's Store family; do not combine
Svelte, React, and Streaming lifecycle patterns in one app. The option is
shared by all three families and is disabled when omitted or set to `false`.

## Store-owned logging streams

The Store exposes a frozen `traceStreams` collection of six read-only Kefir streams:
`selectorDetail`, `selectorSummary`, `selectorCadence`, `sagaMonitor`,
`runtimeError`, and `reduxAction`. The collection exposes no emitters and does not
permit consumers to publish events. Public `StoreTraceStreams` and
`StoreLoggerFactory` types are available from `@themislib/themis/types` and
re-exported by each Store-family entrypoint.

When `logReduxActions: true`, `reduxAction` is produced by pure middleware:
it calls `next(action)` before publishing one shallow-immutable event with the
action, previous/next state references, and `stateChanged`. Errors and return
values from `next` are preserved, and failed dispatches do not publish an event.
The event does not eagerly compute a state diff; default rendering computes it
lazily as described in **Read one action's group** below. Action/state payloads
may contain application data; redact secrets and sensitive values before sharing.

Selector metadata has a separate privacy contract; follow
[Scope and safety rules](../selector-tracing/SKILL.md#scope-and-safety-rules).

## 2. Read one action's group

With no `loggerFactory`, StoreRuntime's default logger prints a one-time `🔧 Redux Logger Active` legend, then renders each
dispatched action with `console.groupCollapsed`. Expand the action group before
interpreting it:

1. Read the action title to identify the dispatch. Primitive payloads, and a
   one-element array containing a primitive, may be included in the title;
   complex payloads are intentionally not rendered in the title.
2. Read the styled `action` record (`%c action`) to see the dispatched action,
   then the styled state record. The CSS/style argument attached to a console
   call controls presentation only; it is not part of the action or state data.
   The blue action label and green state label are visual legend entries, not
   extra fields.
3. A gray `state (no changes)` record contains `{ state: nextState }` and means
   the reducer returned the same state reference. It is a successful no-change
   dispatch, not missing logger output and not proof that the action was
   rejected. The group title is gray and lighter for this case; changed-state
   titles are bold.
4. For a changed state, expand the `state` record and then its `changes`
   property. It is a path-keyed diff: each key is
   a state path and its value contains the previous and next value for that
   path. The diff is lazy, so inspect or expand it in the console only when
   needed rather than assuming the logger eagerly captured a full state
   snapshot.

The title uses `color: inherit; font-weight: 600` for changed state and
`color: #9E9E9E; font-weight: 300` for unchanged state. Record labels use blue
for `action`, green for changed `state`, and gray/lighter styling for `state
(no changes)`; these styles are presentation hints only.

Treat paths and values in `changes` as diagnostic evidence for the current
Store instance. Redact sensitive values before sharing logs. Do not infer
changes from the group title alone.

## 3. Keep logging opt-in and temporary

There is no dev-mode switch, localStorage toggle, global debug-console toggle,
or runtime enable/disable API for action logging. The pure logger middleware and
default action rendering are enabled only when the normalized constructor option
is `true`; omitted and `false` options do not publish action events or enable
action console groups. Other diagnostic streams have independent options.

For default/custom rendering, factory attachment, and cleanup, follow
[Logger factory lifecycle](#logger-factory-lifecycle).

Selector aggregation is independent of action logging. For `summaryEnabled`
and collector allocation/publication, follow
[Aggregate summaries](../selector-tracing/SKILL.md#aggregate-summaries).

To disable logging, omit the option or set `logReduxActions: false` **and
construct a new Store instance**. Changing an options object, calling `init()`
again, or disposing/reusing the existing instance does not reconfigure its
middleware pipeline.

After reproducing the issue, dispose the diagnostic Store through its normal
family lifecycle and remove the temporary `true` option from application code.

## Logger factory lifecycle

With no `loggerFactory`, StoreRuntime attaches its default console logger,
preserving severity and `[themis]` diagnostic prefixes; enabled action logging
uses the legend/groups described in **Read one action's group** above.

Pass a typed `loggerFactory` to replace the default stream-subscriber logger. It
receives only this Store instance's six read-only streams and may return one
disposer; the built-in legend and default subscriber rendering do not attach.
This is **not a global console-silencing or privacy boundary**: with
`traceSelectors.summaryEnabled: true`, the runtime still prints an eligible,
non-empty period aggregate directly, independently of the custom logger. See
[Aggregate summaries](../selector-tracing/SKILL.md#aggregate-summaries).

```ts
import type { StoreLoggerFactory, StoreOptions } from '@themislib/themis/types';

const loggerFactory: StoreLoggerFactory = (streams) => {
  const subscription = streams.runtimeError.observe(reportRuntimeError);
  return () => subscription.unsubscribe();
};

const options: StoreOptions = {
  loggerFactory,
  logReduxActions: true, // events still publish; default action groups do not
  traceSelectors: { summaryEnabled: true, summaryIntervalMs: 1000 },
}; // non-empty selector period aggregates still reach console.info
```

Pass `options` as the third Store constructor argument. `reportRuntimeError` is
your app-owned reporter; redact sensitive data there. Omit `summaryEnabled` or
set it to `false` at construction if these runtime-owned aggregates are unwanted;
redacting in the custom logger does not redact that separate console path. The factory
attaches during initialization; its disposer runs during `store.dispose()` and
before a later successful initialization attaches it again. Dispose custom stream
subscriptions in that callback and retain the Store initializer's disposer for
the end of the owning Store lifetime.

## 4. Common mistakes

- Do not look for a localStorage key or development-mode gate; neither controls
  this option.
- Do not treat CSS style strings as logger payloads.
- Do not call the unchanged-state record a logger failure.
- Do not request a complete before/after state dump when a path in `changes`
  answers the question; expand only the relevant lazy diff entries.
- Do not use `traceSelectors` to enable action logging. Selector tracing has a
  separate contract and option.
- Do not assume a custom logger silences selector aggregates; `summaryEnabled`
  controls that separate runtime-owned output.

## See also

- `../debugging/SKILL.md` — Store inspection and lifecycle boundaries.
- `../selector-tracing/SKILL.md` — selector diagnostics, which are separate
  from Redux dispatch logging.