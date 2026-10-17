---
name: react-testing-engineering
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / react-testing-engineering + frontend-e2e instead. Select only to maintain existing work during the deprecation window. Use when testing React components, hooks, async UI, user interactions, accessibility, and integration boundaries.
license: MIT
---

# React Testing Engineering

## Purpose
Test observable UI contracts and state transitions while keeping tests deterministic and independent of implementation details.

## Activate when
- adding or repairing React tests;
- testing hooks, forms, async rendering, or user interaction;
- replacing brittle implementation-coupled tests.

## Repository inspection
Inspect the test runner, DOM environment, Testing Library usage, network mocking, fixtures, fake timers, accessibility tooling, and CI commands.

## Decision rules
- Prefer user-observable assertions.
- Prefer role, name, and label queries for accessible controls.
- Mock stable network or module boundaries only when isolation requires it.
- Do not mock React internals or every child by default.
- Synchronize async work explicitly.
- Test rejection and recovery paths.

## Implementation procedure
1. Identify the user-visible contract.
2. Select the smallest boundary that proves it.
3. Control external dependencies.
4. Exercise realistic interaction.
5. Assert UI and meaningful side effects.
6. Add regression cases for prior failures.

## Anti-patterns / failure modes
- asserting private state;
- class-name selectors for semantic behavior;
- sleeps for async synchronization;
- snapshot-only verification;
- disabling accessibility warnings globally.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`) and run with Vitest + jsdom.

```tsx
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, test, vi } from "vitest";
import { useState } from "react";

function Subscribe({ submit }: { submit: (email: string) => Promise<void> }) {
  const [status, setStatus] = useState<"idle" | "done" | "error">("idle");
  return (
    <form
      onSubmit={async (event) => {
        event.preventDefault();
        const email = new FormData(event.currentTarget).get("email");
        try {
          await submit(String(email));
          setStatus("done");
        } catch {
          setStatus("error");
        }
      }}
    >
      <label>
        Email
        <input name="email" type="email" />
      </label>
      <button type="submit">Subscribe</button>
      {status === "done" && <p role="status">Subscribed</p>}
      {status === "error" && <p role="alert">Could not subscribe</p>}
    </form>
  );
}

// Without Vitest globals, Testing Library cannot register its own cleanup.
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

// Drive the UI the way a user does and assert on what they can perceive;
// the network boundary is a fake passed in, not a mocked module internal.
test("shows confirmation after a successful subscription", async () => {
  const submit = vi.fn().mockResolvedValue(undefined);
  render(<Subscribe submit={submit} />);

  await userEvent.type(screen.getByLabelText("Email"), "sam@example.test");
  await userEvent.click(screen.getByRole("button", { name: "Subscribe" }));

  expect(await screen.findByRole("status")).toHaveProperty("textContent", "Subscribed");
  expect(submit).toHaveBeenCalledWith("sam@example.test");
});

test("reports a failed subscription", async () => {
  render(<Subscribe submit={vi.fn().mockRejectedValue(new Error("503"))} />);
  await userEvent.click(screen.getByRole("button", { name: "Subscribe" }));
  expect(await screen.findByRole("alert")).toBeTruthy();
});
```

## Agent review checklist
- Do assertions describe user-observable behavior?
- Are network/module mocks placed at a stable boundary?
- Are async waits deterministic?
- Are failure and recovery paths covered?

## Verification
Run focused tests, relevant integration tests, typecheck, and lint.

## Source foundation
- React Learn: https://react.dev/learn
- Testing Library: https://testing-library.com/docs/
