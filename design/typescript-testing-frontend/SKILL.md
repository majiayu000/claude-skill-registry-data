---
name: typescript-testing-frontend
description: Use when writing or reviewing TypeScript frontend tests — Jest unit/integration tests for React components and hooks built with Chakra UI, React Query, Zustand, and Next.js App Router. Triggers on edits to `*.test.tsx`, React component/hook test files (`.tsx`, not `.ts`) under `**/__tests__/`, custom test render helpers, or mentions of "frontend test", "component test", "hook test", "React test", "UI test".
when_to_use: |
  Use when writing or reviewing TypeScript frontend tests: Jest unit/integration tests for React components and hooks using React Testing Library, with Chakra UI, React Query, Zustand, and Next.js App Router. The key signals are `*.test.tsx` files, component test helpers, or any request to test a React UI, component behavior, or custom hook.

  Not when: the task is writing tests for backend services, controllers, or APIs — use typescript-testing-backend. Not when the task is running or verifying the UI in a real browser (Chrome DevTools, visual/layout/interaction verification) — use browser-testing-with-devtools.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# TypeScript Testing — Frontend

You are operating as a frontend test engineer. Test what the user sees and does — accessibility-first queries, real interactions, no implementation-detail assertions.

Reference stack: Jest 29 with `@swc/jest`, React Testing Library 16, jest-dom matchers, jest-canvas-mock, in `jsdom`. All tests import from a custom render helper (e.g. `@/test-utils/render`) that wraps children in `ChakraProvider` + `QueryClientProvider` (with retries disabled). Tests are co-located in `__tests__/` folders next to source files.

Mock Zustand stores via the selector pattern, services at the module boundary, and Next.js `next/link` / `next/image` / `next/navigation` modules. Prefer accessibility-first queries.

## Universal Rules

1. **Import from your custom render helper** — never directly from `@testing-library/react`.
2. **React Query retries disabled** in test wrappers — prevents flaky async behavior.
3. **Accessibility-first queries** — `getByRole` > `getByText` > `getByLabelText` > `getByTestId`.
4. **`userEvent.setup()` over `fireEvent`** for realistic interactions.
5. **Mock at the module boundary** — services, stores, Next.js modules.
6. **Use `const React = require('react')`** inside `jest.mock()` factories.
7. **`waitFor()` for async**, `act()` for sync state updates — never `sleep()`.
8. **No snapshot tests** — behavioral assertions only.
9. **Never `test.skip()`** — fix or delete.
10. **Every `it()` asserts** at least one observable behavior.
11. **Tests-only default** — unless the user explicitly asked for production work, **change tests only** (no refactors, no public API or prop-surface changes, no new exports). When testability pain appears, capture it under **Refactor opportunities (not in scope)** (see below); do not implement those ideas unless instructed.

## Tests-only default and refactor callouts

When **writing or reviewing** tests, default scope is **tests only**. Unless the user explicitly asks you to refactor production code or change public contracts (props, exports, module APIs), **ship tests only**. Do not rename props, split components, extract hooks, or change runtime behavior as part of test work.

Hard-to-test UI remains a useful design feedback signal — but **feedback belongs in your response, not in silent production edits.** When you notice testability issues, add a final section in your response titled **Refactor opportunities (not in scope)** with short bullets (what you observed, what would help). Omit the section if nothing is worth flagging.

**Examples of when to flag:** untestable or awkward seams (no stable boundary to mock/fake); heavy or nested mocks to assert one behavior; large wrapper/setup cost for a supposedly small unit; missing stable accessible names (roles, labels) so tests depend on `getByTestId` or brittle copy; business logic or I/O bundled in a component or hook so focused assertions are awkward.

Do not implement those refactors in the same turn unless instructed — hand off for follow-up. Record the signal; acting on it is a separate, explicit scope.

## References

- [references/framework-and-setup.md](references/framework-and-setup.md) — Jest/SWC/RTL versions, setup files, test scripts, key dependencies
- [references/structure-and-naming.md](references/structure-and-naming.md) — co-located `__tests__/` layout, file naming patterns
- [references/test-utilities.md](references/test-utilities.md) — custom render wrapper with Chakra + React Query providers
- [references/component-testing.md](references/component-testing.md) — basic component tests, `userEvent` interactions
- [references/hook-testing.md](references/hook-testing.md) — `renderHook` with explicit wrapper, sync + async patterns
- [references/mocking-patterns.md](references/mocking-patterns.md) — Zustand stores, services, Next.js modules, child components, Chakra/window
- [references/queries-and-async.md](references/queries-and-async.md) — query priority, `waitFor` / `act`, jest-dom matcher reference
- [references/coverage-and-policy.md](references/coverage-and-policy.md) — coverage config, no snapshots, test failure triage
