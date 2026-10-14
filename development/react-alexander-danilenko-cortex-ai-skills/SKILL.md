---
name: react
description: "Apply these opinionated React conventions when writing React 18+ or 19 components: hooks patterns, Server Components, Suspense boundaries, state management, performance memoization, React 19 features (use, form actions)."
---

# React

House conventions for React 18/19. Apply them to components you are writing or changing — don't refactor untouched files to match unless asked.

## Conventions

- **Server Component by default; `'use client'` only where you need it** — state, effects, event handlers, browser APIs. Push the boundary as far down the tree as it will go: every component above a `'use client'` marker also ships to the browser. Everything crossing that boundary must be serializable — a function, a class instance, or a `Date` inside a prop object fails at runtime, not at build.
- **Read state through the functional updater inside anything that outlives the render** — intervals, subscriptions, debounced callbacks. `setCount(count + 1)` inside a `useEffect(…, [])` captures `count` from the first render forever and silently sets `1` every tick; `setCount(c => c + 1)` always sees current state.
- **Effects are for synchronising with something outside React** — a subscription, a timer, a non-React widget. Data transformation belongs in render, derived values in a plain variable, and event responses in the handler. Most `useEffect` bugs are an effect that should never have existed.
- **Every effect that starts something returns a cleanup** that stops it. Strict mode double-invokes effects in development precisely to make a missing cleanup visible — treat that as the signal it is, not noise.
- **Keys must be stable identity, not position.** An array index as key makes React reuse the wrong DOM node when the list reorders, and the symptom shows up as state attached to the wrong row.
- **Memoise for a measured reason.** `memo`, `useMemo`, and `useCallback` each cost a comparison and add code to read. They earn their place when a child is genuinely expensive or is itself memoised and a new reference would defeat it — not as a default wrapper.
- **State lives at its natural level.** `useState` locally, lifted only as far as the shared ancestor. Reach for Zustand when genuinely global client state exists; TanStack Query for server state, because cache invalidation and refetching are its job and hand-rolling them in effects goes wrong quietly.
- **Error boundaries around anything that can fail independently** — a route, a widget, a third-party embed. Without one, a render error unmounts the whole tree and the user gets a blank page.
- **Suspense boundaries where you want a fallback**, placed so the loading UI matches the layout that will replace it. A boundary at the root turns any pending fetch into a full-page spinner.
- **React 19: `useActionState` and `<form action>` for mutations**, `useOptimistic` for immediate feedback, `use()` to read a promise or context conditionally. `ref` is a normal prop — `forwardRef` is no longer needed. `useFormStatus` only reports on a form _above_ it, so the submit button reading pending state has to be its own component nested inside the `<form>` — calling it in the component that renders the form always returns `pending: false`.
- **`useTransition` when a keystroke triggers expensive work.** Update the input urgently and mark the derived work as a transition, so React can interrupt it; without this, typing into a field that filters a large list feels broken even though nothing is.
- **Semantic HTML first, ARIA only to fill the gap.** A `<button>` brings focus handling, keyboard activation, and role for free; a `<div role="button">` means reimplementing all three correctly.
- **Query tests by role and label, not test IDs.** `getByRole('button', { name: /submit/i })` fails when the control stops being reachable the way a user reaches it — which is the bug you want the test to catch. `getByTestId` passes regardless and is the fallback for elements with no accessible name.
