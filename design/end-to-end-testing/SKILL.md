---
name: end-to-end-testing
description: End-to-end (E2E) testing patterns for user journeys, browser automation, UI state, and production-like environment validation. Use when testing the system as a black box from the user's perspective.
---

# End-to-End Testing

Validate complete user workflows across the entire stack, ensuring that UI components, APIs, and databases work together in a production-like environment.

## When to Activate

- Automate a critical user journey (Signup, Checkout, etc.)
- Resolve flaky browser tests or slow CI cycles
- Implement visual regression or screenshot testing
- Choose a selector strategy (ARIA vs CSS vs Test ID)
- Test cross-browser or mobile responsiveness
- Simulate network failures or latency in the UI
- Verify analytics or external tracking pixels

## Selector Strategy

| Type | Example | Stability | Recommendation |
| --- | --- | --- | --- |
| User-facing (ARIA) | `getByRole("button", { name: "Submit" })` | High | **Primary**: Tests what the user sees |
| Data attribute | `getByTestId("submit-btn")` | Medium | **Secondary**: Use when ARIA is ambiguous |
| CSS Class/ID | `locator(".btn-primary")` | Low | **Avoid**: Highly coupled to styling |

## Execution Strategy

| Concern | Strategy |
| --- | --- |
| Test Data | Use a dedicated setup API or direct DB seed before each run |
| State Isolation | Clean cookies, localStorage, and indexedDB between tests |
| Waiting | Use auto-waiting or "Wait for State" (loading spinner gone) over hard sleeps |

BAD

```ts
// Flaky and coupled to implementation
await page.click('.login-submit');
await page.waitForTimeout(5000);
expect(await page.url()).toContain('/dashboard');
```

GOOD

```ts
// Stable and user-centric
const submitBtn = page.getByRole('button', { name: /log in/i });
await submitBtn.click();
await expect(page).toHaveURL(/\/dashboard/);
await expect(page.getByText(/welcome back/i)).toBeVisible();
```

## Flakiness Prevention

| Risk | Solution |
| --- | --- |
| Animation lag | Disable CSS animations in the test environment |
| Third-party scripts | Block or stub chat widgets, ads, and telemetry |
| Race conditions | Assert state changes (e.g. "button is hidden") before next step |

## Checklist

- [ ] Selectors use ARIA roles or Test IDs (no CSS classes)
- [ ] Tests assertions wait for specific UI state changes (not time)
- [ ] Every test starts from a clean state (cookies, storage, data)
- [ ] Core user journeys (Happy Paths) are covered first
- [ ] Error states and validation messages are verified
- [ ] Network requests are monitored or stubbed to prevent external flake
- [ ] Screen sizes (mobile vs desktop) are explicitly set
- [ ] Heavy animations are disabled to speed up execution
- [ ] Artifacts (trace, video, screenshots) are captured on failure
- [ ] Test data is isolated to prevent parallel run conflicts
- [ ] Parallelism is enabled and tuned for CI resources
- [ ] Senseless "Wait for X seconds" are replaced with "Wait for Locator"

