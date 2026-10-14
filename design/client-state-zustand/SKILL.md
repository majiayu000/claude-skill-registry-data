---
name: client-state-zustand
description: When to reach for Zustand vs React Context for client-only UI state, and the store slice convention used in this template.
paths: ["src/lib/store.ts", "src/lib/**/*store*"]
---

- Zustand is for state that (a) is read by components that don't share a parent, or
  (b) changes frequently enough that Context would cause wide re-renders — e.g. a dialog's
  open/closed flag read by both the trigger and the dialog itself (`src/lib/store.ts`,
  `useUiStore`).
- Plain `React.useState`/Context is still correct for state genuinely local to one component
  subtree, or for low-frequency global state (theme, locale) where Context's broader re-render
  is not a real cost — do not reach for Zustand by default.
- One store per concern, not one giant app-wide store — `useUiStore` here only owns UI-only
  state (dialog visibility), never server data (that is TanStack Query's job, never
  duplicated into Zustand).
- Select the narrowest slice a component needs (`useUiStore((s) => s.isSubscribeDialogOpen)`),
  never the whole store object — a whole-store selector re-renders on every field change.
- Actions live on the store itself (`openSubscribeDialog`, `closeSubscribeDialog`), not as
  ad-hoc `setState` calls scattered across components — keeps the state's invariants in one
  place.
