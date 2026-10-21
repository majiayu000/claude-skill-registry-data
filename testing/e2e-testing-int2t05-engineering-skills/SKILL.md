---
name: e2e-testing
description: Verify critical user journeys in a real browser. Triggers on "playwright", "端到端测试".
---

# End-to-End Testing

## When to use

- Verify critical user journeys in a real browser.

**Not for:** api-testing for direct service checks; frontend-design for UI design.

## Steps

1. Identify journeys, browser tooling, environment, authentication and isolated data.

2. Use semantic locators, outcome assertions and condition-based waits instead of arbitrary sleeps.

3. Exercise real end-to-end integration where required and relevant errors, permissions, responsive and keyboard states.

4. Run and inspect screenshots, console and network evidence; fix causes, clean test state and remove temporary debugging.

## Verify

- Actual browser outcomes are asserted; tests are isolated and screenshots alone do not prove integration.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/playwright-rules.md](references/playwright-rules.md) — consolidated Playwright rules (locators, auth, assertions, forms, organization, reliability)
- [references/a11y-automation.md](references/a11y-automation.md) — axe-core, Lighthouse CI, Storybook a11y addon: automated accessibility testing in CI
