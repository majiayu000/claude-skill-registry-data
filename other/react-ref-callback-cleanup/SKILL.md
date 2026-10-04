---
name: react-ref-callback-cleanup
description: >-
  Use when a React 19 component forwards a ref and also uses it internally — a ref-merge helper, a
  `React.RefCallback` built with useCallback, or an effect that writes the forwarded ref — and a
  consumer's cleanup function returned from `ref={node => () => ...}` never runs on unmount.
---

# React ref callback cleanup propagation

## Profile keys consumed

- `framework.ui`
- `architecture.source_root`
- `architecture.component_prefix`
- `make.test_unit_client`

## Overview

In React 19 a ref callback may return a cleanup function, which React calls when the ref detaches
instead of re-invoking the callback with `null`. A component that installs its own callback over a
forwarded ref becomes the only callback React sees, so the consumer's cleanup runs only if that
component returns it.

## When to use

- Writing or reviewing a component that both forwards a ref and reads it internally (focus
  management, outside-click, measurement).
- A ref-merge helper whose return type is `void` while its parameter is `React.ForwardedRef<T>`.
- A consumer reports that the function returned from its ref callback never fires on unmount.
- Not for: object refs (`useRef` results) — they have no return value and nothing to propagate.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): no — React 18.3 ignores ref returns.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — React 19.2, so any
  forwarded-ref component here is subject to it.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — React
  19.2; two prefixed components under `architecture.source_root` (a background-picker's
  `picker-refs.ts` and a profile-select-card's `menu-focus.ts`, both named per
  `architecture.component_prefix`) expose a `void`-returning `assignTriggerNode` consumed by a
  `React.RefCallback`, which is exactly the shape that swallows a consumer cleanup.

Read the React major from `framework.ui` before applying this: below 19 there is nothing to
propagate.

## Core pattern

The merge helper must hand back whatever the forwarded callback returned, and the ref callback must
return it in turn:

```ts
export function assignTriggerNode(a: TriggerNodeAssignment): (() => void) | void {
  const { forwarded, own, node } = a;
  own.current = node;
  if (typeof forwarded === 'function') {
    return forwarded(node) as (() => void) | void;
  }
  if (forwarded != null) {
    forwarded.current = node;
  }
  return undefined;
}

const triggerRef: React.RefCallback<HTMLButtonElement> = React.useCallback(
  (node) => assignTriggerNode({ forwarded: forwardedRef, own: refs.trigger, node }),
  [forwardedRef, refs]
);
```

Two things break it. An arrow body annotated `: void` discards the return silently, and an object
ref branch must return `undefined` rather than the assignment expression — returning a node is not a
cleanup function and React rejects it.

## Verification

The regression test asserts the consumer's cleanup, not the component's internals, and must fail
against the non-propagating version. Run it through the target mapped by `make.test_unit_client` —
skip with a recorded note when that key maps to `null`:

```ts
const cleanup = jest.fn();
const { unmount } = render(<Card ref={() => cleanup} />);

unmount();
expect(cleanup).toHaveBeenCalledTimes(1);
```

Pin the same behaviour for the object-ref branch (no throw, `.current` reset) so a later refactor
cannot trade one for the other.

## Common mistakes

- Typing the merge helper `: void` — the compiler then accepts the swallowed return.
- Writing the ref callback as a statement body with no `return` — the cleanup is dropped even when
  the helper propagates it correctly.
- Returning the assignment expression from the object-ref branch — that returns the node, which
  React does not accept as a cleanup.
- Asserting the internal ref instead of the consumer's cleanup — such a test passes against both
  implementations and proves nothing.
