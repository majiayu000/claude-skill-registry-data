---
name: error-handling
description: Error boundary placement, Sentry capture conventions, and user-facing vs technical error messaging in this template.
paths: ["src/**/*.tsx", "src/lib/**"]
---

- Route-level error boundaries come from TanStack Router's `errorComponent` on
  `createFileRoute`, not a hand-rolled `componentDidCatch` — one per route that can fail
  independently, so one broken route doesn't blank the whole app.
- TanStack Query mutation/query errors are surfaced through the hook's own `error`/`isError`
  state (see `mutation.onError` in `SubscribeDialog.tsx`), not thrown and caught ad hoc —
  render the message via the same accessible error pattern as `forms-validation`.
- User-facing error copy is always a plain sentence describing what to do next ("Enter a valid
  email address"), never a raw exception message, stack trace, or HTTP status code.
- Sentry (`@sentry/react`) captures the _technical_ detail for developers — initialize it once
  in `src/main.tsx` behind an environment check (only when `SENTRY_DSN` is set, see
  `.env.example`), never let its absence in local dev throw.
- Never swallow an error silently (empty `catch {}`) — at minimum log it via Sentry or
  `console.error` with enough context (which mutation/query, what input) to debug from the
  report alone.
- A network error and a validation error are different things and must render differently:
  validation errors are the user's to fix (inline, next to the field); network/server errors
  are the system's fault (a dismissible banner or dialog-level message, with a retry action
  when the operation is safely retryable).
