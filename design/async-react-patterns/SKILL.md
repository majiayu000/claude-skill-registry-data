---
name: async-react-patterns
description: Guides React 19 async UI state modeling with Actions, useActionState, useTransition, useOptimistic, use, Suspense, Activity, and useEffectEvent. Use when implementing or reviewing React async flows that risk outdated manual data/loading/error state, ad hoc form submission state, useEffect fetching, stale effect callbacks, or hand-rolled optimistic updates. Do not use for async waterfall performance fixes.
---

# Async React Patterns

Use this skill to avoid outdated async React patterns. Do not use it to fix async waterfalls; use `vercel-react-best-practices` for waterfall and performance work. This skill is about choosing the React 19 primitive that owns pending, optimistic, error, and streaming state instead of hand-rolling those states with scattered `useState`/`useEffect` logic.

## Quick Start

1. Classify the async work:
   - read data: render under `Suspense`, resolve with `await` in Server Components or `use(promise)` in Client Components
   - mutate data: model pending/error/settled state as an Action, usually through `<form action>`, `useActionState`, or `startTransition`
   - preserve hidden UI: use `<Activity>` for stateful hidden sections that should pre-render or resume cheaply
   - effect callback with latest props: use `useEffectEvent`, not disabled dependencies
2. Pick the smallest primitive:
   - form submit -> `<form action={action}>`, `useActionState`, `useFormStatus`
   - non-form async update -> `useTransition`
   - instant feedback during mutation/navigation -> `useOptimistic`
   - stable promise from server/framework -> `use(promise)` inside `Suspense`
   - RSC cache lifetime cleanup -> `cacheSignal`
3. Verify UX states: pending indicator, optimistic rollback/settle behavior, error boundary or returned error state, accessibility (`aria-busy`, disabled only when useful).

## Patterns

### Actions For Mutations

- Name async mutation callbacks with `Action` suffix when they are intended to run in a transition or form action.
- Prefer `<form action>`/`useActionState` for form submissions; React handles pending state, error result state, and uncontrolled form reset.
- Use `useFormStatus` inside reusable form controls that need the nearest parent form pending state without prop drilling.
- Use `useTransition` for non-form work such as router/search-param changes, list filtering, tabs, or button-triggered async mutations.
- Keep urgent input updates outside transitions; put expensive or async follow-up work inside the Action.
- If setting state after `await` inside `startTransition`, re-check current React docs. React currently documents wrapping post-`await` state updates in another `startTransition`.

### Optimistic UI

- Call `useOptimistic(value, reducer?)` at component top level.
- Call the optimistic setter only inside an Action, event handler, effect, or callback; never during render.
- Keep reducers pure. Use a reducer when multiple optimistic operations can overlap or when list updates need typed operations.
- Let parents own optimistic state when reusable children cannot derive the final display value. Children may expose `setValueAction`, `submitAction`, or `onChangeAction` props for parent-specific logic.
- Always define the settle path: successful server/router value replaces optimistic value; rejected work rolls back via React or explicit error recovery.

### Reading Async Data

- In Server Components, prefer `async`/`await` when the component can block at that point.
- To avoid blocking a Server Component shell, create/pass a stable promise to a Client Component and resolve it with `use(promise)` under `Suspense`.
- Do not create promises during Client Component render for `use`; promises should come from a Suspense-aware framework/library or from the server.
- Pair `use(promise)` with `Suspense` for loading and an Error Boundary or `promise.catch` fallback for rejection. Do not wrap `use` in `try/catch`.
- Keep data passed from Server to Client serializable.

### Effects And Background UI

- Do not default to `useEffect` + `fetch` for primary data reads. Prefer framework data loading, Server Components, cached promises, or Suspense-compatible libraries.
- Use `useEffectEvent` only for callbacks that are conceptually events fired from an Effect and need latest props/state without resubscribing the Effect.
- Do not put Effect Events in dependency arrays; keep them declared in the same component or Hook as their Effect.
- Use `<Activity mode="hidden">` for UI likely to be revisited or preloaded while hidden; remember hidden Activities unmount effects and defer hidden updates.
- Use `cacheSignal` only in React Server Components to abort/cleanup work tied to `cache()` lifetime.

## Review Checklist

- No manual `isLoading`/`error`/`data` state machine where an Action, `useActionState`, `useFormStatus`, `Suspense`, or Error Boundary should own the state.
- Mutations expose pending, error, optimistic, and settle behavior in one obvious Action path.
- Reusable components accept Action props instead of owning application-specific async side effects.
- Suspense boundaries are close enough to avoid blanking the whole page but high enough to prevent boundary soup.
- Client promises used with `use` are stable, cached, and rejected through Error Boundaries or fallback values.
- Accessibility reflects async state without over-disabling controls.
- Experimental or canary APIs from articles are verified against current React docs before use.

## Sources

- React 19 overview: https://react.dev/blog/2024/12/05/react-19
- React 19.2 overview: https://react.dev/blog/2025/10/01/react-19-2
- `useOptimistic`: https://react.dev/reference/react/useOptimistic
- `useTransition`: https://react.dev/reference/react/useTransition
- `use`: https://react.dev/reference/react/use
- Async shift article: https://blog.logrocket.com/react-19-2-the-async-shift/
- Reusable Actions article: https://certificates.dev/blog/building-reusable-components-with-react-19-actions
