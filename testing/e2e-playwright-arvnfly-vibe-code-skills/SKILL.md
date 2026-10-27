---
name: e2e-playwright
description: "End-to-end browser automation with Playwright, resilient locator strategies, visual regression tests, and network mocking."
---

# End-to-End Browser Testing Protocol

Author robust, non-flaky end-to-end tests that validate real user journeys.

---

## 1. Accessibility-First Locators

Always prioritize user-facing locators over brittle CSS or XPath selectors:
1. page.getByRole('button', { name: 'Submit' })
2. page.getByLabel('Email Address')
3. page.getByText('Account created successfully')
4. Fallback: page.getByTestId('checkout-card')
5. Never use brittle classnames or DOM traversal.

---

## 2. Elimination of Arbitrary Sleep

1. Strictly forbid arbitrary sleeps (e.g. waitForTimeout).
2. Rely exclusively on Playwright auto-waiting assertions:
   await expect(page.getByRole('heading')).toBeVisible();
3. Wait on specific network responses or DOM states rather than arbitrary delays.
