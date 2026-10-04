---
name: deferred-jsx-props
description: >
  A prop whose markup is built outside a render — pushed onto a queue,
  held in a signal, sent from a promise — is typed `() => JSX.Element`,
  never `JSX.Element`. Applies whenever adding a prop or an API that
  stores markup and draws it later.
---

Solid's compiler wraps a component's dynamic props in memos **when the element is constructed**. Construct it inside a render and those memos get that render's owner and are disposed with it. Construct it in an event handler, a `.then`, or a `setTimeout`, and they have no owner, live for the life of the page, and Solid says so:

> computations created outside a `createRoot` or `render` will never be disposed

## The rule

- Markup passed **parent to child** stays `JSX.Element`. The compiler makes it a getter evaluated inside the parent's render, which has an owner. `title`, `trigger`, `footer`, `aside` across `src/components/styled` are all correct as they are.
- Markup that is **stored and drawn later** is `() => JSX.Element`. The holder calls it where it draws it.

```ts
// Bad — every caller builds this in a handler or a promise
export interface ToastRequest {
  art?: JSX.Element;
}
toast.push({ art: <ItemSprite item={stack.item} size={24} label="" /> });

// Good — built under the card that draws it
export interface ToastRequest {
  art?: () => JSX.Element;
}
toast.push({ art: () => <ItemSprite item={stack.item} size={24} label="" /> });
```

The holder renders it with an explicit call, and tests the value rather than the markup:

```tsx
<Show when={props.toast.art != null}>
  <div class="…">{props.toast.art?.()}</div>
</Show>
```

## How to tell which you have

Ask where the JSX is written. If the answer is "inside another component's JSX", it is a plain prop. If it is "inside a function that runs after something happened", it is a thunk.
