---
name: playwright-core
description: Conducts rigorous authoring and review of Playwright E2E tests. Enforces accessibility-first locators, web-first assertions, strict isolation, and DAMP architecture. Use when generating, refactoring, or reviewing any Playwright test code.
---

# Playwright Core: Test Architecture and Quality Gates

## Overview

Writing end-to-end tests is easy. Writing end-to-end tests that survive UI refactors and network latency without flaking requires discipline.

Use this skill when you are authoring, reviewing, or refactoring Playwright tests that should behave like a real user journey. It pairs well with `playwright-auth-state` for logged-in flows, `playwright-network-mocking` for external API control, and `playwright-debugging` when a test is already failing.

**The approval standard:** A test is only valid if it tests the application exactly how a human user interacts with it. We do not test implementation details, we do not rely on fixed sleep timers, and we do not share state between tests. If a test fails, it should indicate a true user-facing bug, not a brittle CSS selector or a race condition.

## When to Use

- Before writing new Playwright E2E tests or component tests.
- When reviewing a PR that adds or modifies test coverage.
- When fixing a "flaky" test that passes locally but fails in CI.
- When refactoring existing Page Object Models (POMs) or test fixtures.

## When Not to Use

- When you need authenticated state reuse; use `playwright-auth-state` instead.
- When you need request interception; use `playwright-network-mocking` instead.
- When you are diagnosing a specific failure or flake; use `playwright-debugging` instead.
- When you need CI configuration, fixture scaffolding, or a broader test framework recipe.

## The Five-Axis Test Review

Every Playwright test must be evaluated across these five dimensions before execution:

### 1. Resiliency (Locator Strategy)

Does the test target user intent, or is it coupled to implementation?

- Are we using `getByRole` as the absolute first choice?
- Are we avoiding CSS classes, XPaths, and DOM hierarchy dependencies?
- If the developer changes a `<div>` to a `<span>`, or swaps a CSS framework (e.g., Bootstrap to Tailwind), will the test survive?

### 2. Determinism (Web-First Assertions)

Are we relying on Playwright's actionability engine, or are we manually guessing execution speed?

- Are there any `page.waitForTimeout()` calls? These are strictly forbidden.
- Are we using auto-retrying assertions like `expect(locator).toBeVisible()`?
- Are we properly awaiting asynchronous UI state changes, such as waiting for a loading spinner to detach, before interacting?

### 3. Isolation (Clean Slate)

Can this test run in complete isolation, in any order, and in parallel?

- Does the test rely on data created by a previous test?
- Is state setup and teardown handled cleanly in `test.beforeEach` and `test.afterEach`?
- Are we bypassing the UI for data setup, using API calls to focus purely on the target behavior?

### 4. Readability (DAMP over DRY)

Can another engineer read the test top-to-bottom and understand the business requirement?

- Do the test names describe the behavior and the outcome?
- Is the test DAMP, meaning Descriptive And Meaningful Phrases? Slight repetition in setup is vastly preferred over 10 layers of abstracted, unreadable helper functions.
- Does the test follow the Arrange-Act-Assert (AAA) pattern clearly?

### 5. Intent (Testing Behavior)

Does the test verify what the user cares about?

- Are we asserting internal component state variables, or the visible DOM?
- Are we checking for accessibility text rather than raw HTML nodes?

---

## Structural Remedies

When you identify a structural problem in a test, do not just patch it. Reach for a named restructuring:

- **Replace brittle CSS selectors** with accessible locators (`getByRole`, `getByLabel`).
- **Replace hardcoded sleeps** with `expect().toBeVisible()` or `page.waitForResponse()`.
- **Collapse abstracted helper logic** back into the test block if it hides the core user journey.
- **Extract deeply nested POMs** into flat, feature-specific Page Objects.
- **Split multi-assertion monolith tests** into separate `test()` blocks with a shared `beforeEach`.

---

## Strict Locator Hierarchy

You must follow this exact order of preference when querying the DOM. Fall to the next level only if the previous is impossible.

1. `page.getByRole()` - Always the first choice. Tests accessibility and user intent simultaneously.
2. `page.getByLabel()` - The standard for form inputs.
3. `page.getByPlaceholder()` - Acceptable for inputs without labels.
4. `page.getByText()` - For generic non-interactive text elements.
5. `page.getByTestId()` - The fallback. Use only when semantic querying is impossible, such as dynamic SVG charts.
6. CSS/XPath - Forbidden unless explicitly requested for legacy integration.

When a locator could match more than one element, refine it with semantic filtering instead of switching to position-based selection. Prefer `filter()`, `and()`, or a narrower accessible name over `nth()` or DOM traversal.

---

## Code Standards & Anti-Patterns

### Web-First Assertions

Always use auto-retrying assertions. Never read a value and assert it synchronously.

```typescript
// Bad: synchronous evaluation. Causes race conditions if the element is still rendering.
const isVisible = await page.getByRole('button').isVisible();
expect(isVisible).toBeTruthy();

// Good: Playwright handles the polling and timeout automatically.
await expect(page.getByRole('button', { name: 'Submit' })).toBeVisible();
```

### Actionability Before Interaction

Do not force clicks on unready elements. Let Playwright wait for actionability.

```typescript
// Bad: bypassing actionability checks.
await page.locator('.btn').click({ force: true });

// Good: waiting for the app to be ready.
await page.getByRole('button', { name: 'Submit' }).click();
```

### Provable Assertions (Mutation Check)

An assertion that has never been observed to fail provides no evidence. Both LLM- and
human-authored tests drift toward assertions that pass regardless of the underlying
behavior — sophisticated-looking checks that are, in spirit, no different from
`expect(true).toBeTruthy()`.

Before treating a new assertion as finished, prove it can go red:

- Temporarily invert the expected condition, or break the state the assertion depends
  on — drop or alter the response with `page.route()`, remove a required fixture, or
  comment out the relevant application behavior — run the test once, and confirm it
  fails for the expected reason.
- Revert the break and confirm the test passes again.
- This is a one-time proof done during authoring, not a permanent step. Do not ship a
  test that deliberately breaks its own app.

This matters most for **negative assertions**. `expect(locator).not.toBeVisible()`
passes just as happily when the locator itself is wrong — a typo'd role or name — as it
does when the element is genuinely absent. A negative assertion is only trustworthy once
you've confirmed, at least once, that the same locator resolves correctly when the
element **is** present. Otherwise a broken selector and a correct negative assertion are
indistinguishable.

### The Anti-Rationalization Table

When tempted to take shortcuts to generate code faster, refer to this table:

| Rationalization | The Reality & Required Action |
| --- | --- |
| "I'll use `page.waitForTimeout(3000)` because the transition animation is slow." | REJECTED. Sleep timers guarantee flaky CI suites. Action: Assert the expected end-state, for example `await expect(modal).toBeVisible()`. |
| "Using `.submit-btn-active` (CSS) is faster than looking up the ARIA role." | REJECTED. Implementation details change often. Action: Locate by user intent: `await page.getByRole('button', { name: 'Submit' })`. |
| "I'll combine 5 different user flows into one giant test block so it runs faster." | REJECTED. Tests must be isolated. If it fails on step 4, steps 1-3 provide no value. Action: Break them into separate `test()` blocks. |
| "I'll use `page.evaluate()` to click the element via JavaScript." | REJECTED. Users cannot fire synthetic JS events; they use a mouse. Action: Ensure the element is not obscured and use a standard `.click()`. |
| "The test passes locally, so I don't need to check the trace." | REJECTED. Local execution does not mimic CI resource constraints. Action: Verify with tracing or multiple repeats to ensure determinism. |
| "The test passes, so the assertion must be correct." | REJECTED. A pass alone proves nothing. Action: break the condition once during authoring and confirm the test goes red before trusting it. |
| "I'll assert the element is *not* visible to confirm it was removed." | RISKY. This passes identically whether the element was removed or the locator is simply wrong. Action: confirm the same locator resolves when the element is present, at least once. |

### Red Flags in Code Review

If you see any of the following in existing code, flag them as Required Changes:

- Use of `.locator('.class-name')` instead of semantic queries.
- Use of `nth()` or index-based selection when a semantic locator can disambiguate the target.
- Tests relying on the execution outcome of the test immediately above them.
- Any instance of `waitForTimeout`.
- Complex if/else logic inside a test file. Tests should be linear paths.
- Unhandled promises, such as missing `await` on actions or assertions.
- Testing external dependencies, for example hitting the real Stripe API instead of mocking it.
- Negative assertions (`.not.toBeVisible()`, `.not.toContainText()`, etc.) with no evidence the same locator resolves correctly when the element is present.
- Assertions that read as boilerplate and show no sign of ever having been proven capable of failing.

### Verification & Handoff Checklist

Before concluding your task, output this checklist and verify each point:

- [ ] All locators are user-facing (getByRole, getByLabel, etc.).
- [ ] No hardcoded sleeps or waitForTimeout calls exist.
- [ ] Assertions use `expect().to...` for auto-retrying.
- [ ] The test is strictly isolated and can run in any order.
- [ ] External dependencies are mocked or intercepted.
- [ ] The test reads like a human user journey, not an implementation walkthrough.
- [ ] New assertions have been proven to fail under a deliberate break, then confirmed to pass again.
- [ ] Any negative assertion has been checked against a false-locator false positive.

If any box is unchecked, treat the test as incomplete.
