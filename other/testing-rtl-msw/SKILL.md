---
name: testing-rtl-msw
description: RTL query conventions and the MSW network-mocking contract used by every unit/component test in this template. test-author loads this skill automatically.
paths: ["tests/unit/**", "src/**/*.test.*", "src/**/*.spec.*"]
---

- Query priority (matches RTL's own recommendation): `getByRole` with an accessible `name`
  first (`screen.getByRole("button", { name: /subscribe/i })`), then `getByLabelText`,
  `getByText`; reach for `data-testid` (`getByTestId`) only when no accessible query exists —
  see `tests/unit/subscribe-dialog.test.tsx` and the one deliberate exception,
  `data-testid="subscriber-count"` on plain display text with no other role.
- Every test that touches a component using `fetch` needs the MSW server running
  (`tests/unit/setup.ts` already wires `beforeAll(() => server.listen(...))`,
  `afterEach(() => server.resetHandlers())`) — you do not set this up per-test file, it's
  global.
- `onUnhandledRequest: "error"` is deliberate and must never be weakened to `"warn"` or
  `"bypass"` in this template: a test that reaches real network is a **failing** test, not a
  passing one with a warning. Add a handler in `src/mocks/handlers.ts` instead.
- Reset any mutable mock state between tests (`resetSubscriberCount()` in
  `tests/unit/setup.ts`'s `afterEach`) — a test must never depend on execution order.
- Wrap components under test with the app's real providers via the shared
  `renderWithProviders` helper (`tests/unit/test-utils.tsx`), not a bespoke wrapper per test
  file — keeps `QueryClient` defaults (`retry: false`) consistent everywhere.
- Prefer `userEvent` (`@testing-library/user-event`) over `fireEvent` for anything a real user
  would do (click, type) — it dispatches the fuller sequence of events real interaction
  produces.
- A test's `it(...)` description should read as a behavior, and a `// covers: EARS-N` comment
  ties it back to `specs/<feature>/spec.md` (SPEC.md §8's testability contract) — `reviewer`
  checks this traceability.
