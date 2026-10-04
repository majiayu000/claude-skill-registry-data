---
name: component-testing
category: testing
description: Use when writing or changing any React component - React Testing Library tests are behavior-focused (byRole first), use user-event, assert on accessible output, one behavior per test, and run in npm test
tech_stack: React
---
# Component Testing (React Testing Library)

## Overview

A component test that queries by `data-testid` or asserts on internal state proves the implementation didn't change, not that the component works for a user. React Testing Library tests must exercise the component the way a user (and a screen reader) does: find things by role/label/text, interact with them, and assert on what actually rendered.

**Core principle:** Test behavior, not implementation. If a refactor that keeps the same user-facing behavior breaks the test, the test is coupled to the wrong thing.

## Rules

- **Query priority: `byRole` first.** Prefer `getByRole` (with `{ name: ... }`) over `byLabelText`/`byText`, and both over `byTestId`. `byTestId` is a last resort for a node with no accessible role or text — reach for it only when nothing else identifies the element, and treat its presence as a smell worth a follow-up (usually a missing label/role, per accessibility-basics).
- **`user-event` over `fireEvent`.** `fireEvent.click` fires one DOM event; `userEvent.click` simulates the real sequence of events a browser produces (focus, pointer, keyboard) and catches bugs `fireEvent` cannot (e.g. a control that only works because it happens to be focused). Always `await userEvent.setup()` / `await user.click(...)`.
- **Assert on accessible, user-visible output.** Check rendered text, roles, `aria-*` state (`aria-expanded`, `aria-invalid`, `aria-disabled`), and focus — not component internals, prop values, or CSS class names.
- **One behavior per test.** A test named for the behavior it proves (`"shows a validation error when the field is left empty"`), not `"renders correctly"`. Multiple assertions are fine as long as they all check the same behavior; a second, unrelated behavior gets its own test.
- **No implementation-detail mocking.** Mock the network/API boundary (MSW or the API client module), never a child component or a hook's internals just to make the test pass — that tests the mock, not the component.
- **Wire it into `npm test`.** New component test files must run under the project's existing `npm test` script (Vitest/Jest) with no extra flags — a suite that only runs when invoked by hand is not part of the pipeline (see ci-cd-pipeline-authoring).
- **TDD still applies** (see tdd-workflow): write the test against the intended behavior first, watch it fail, then implement.

## Worked Example

```tsx
// ❌ implementation-coupled: breaks on any internal refactor, proves nothing
// about what the user sees
test("renders correctly", () => {
  render(<LoginForm />);
  expect(screen.getByTestId("submit-btn")).toBeInTheDocument();
});

// ✅ behavior-focused: fails only when the real user-facing behavior breaks
test("shows a validation error when submitting with an empty email", async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.click(screen.getByRole("button", { name: /sign in/i }));

  expect(screen.getByRole("alert")).toHaveTextContent(/email is required/i);
  expect(screen.getByRole("textbox", { name: /email/i })).toHaveAttribute("aria-invalid", "true");
});
```

The second test finds the button and field the way a user would (by their accessible name), drives them with `user-event`, and asserts on what actually appears — it stays green through any internal rewrite that keeps this behavior.

## Common Mistakes

- Querying by `data-testid` when a role/label query would work — usually a sign the component is missing an accessible name in the first place.
- Using `fireEvent` for anything a real user would do with a mouse or keyboard.
- One giant test asserting the whole component "renders correctly" instead of named tests per behavior.
- Snapshot tests as the only coverage — they fail on any markup change, meaningful or not, and don't document behavior.
- Mocking a child component to isolate the parent, hiding real integration bugs.
- A new `*.test.tsx` file that `npm test` never picks up (wrong glob, wrong location) — decoration, not a gate.

## Red Flags

- `screen.getByTestId(...)` with no comment on why no role/label query worked.
- `fireEvent` anywhere a `user-event` equivalent exists.
- A test file with only snapshot assertions.
- Assertions on a component's props/state instead of its rendered output.
- Test suite green locally but `npm test` in CI never runs the new file.
