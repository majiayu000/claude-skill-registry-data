---
name: web-app-testing
description: Test a local web application through realistic browser interactions. Use when validating user journeys, forms, navigation, responsive behavior, or UI regressions in a running development app.
---

# Web App Testing

Test behavior from the user's perspective, using the project's existing browser-test stack where possible.

1. Inspect the repository, app start command, existing test framework, routes, fixtures, and current browser-test conventions before adding tooling.
2. Confirm the target is a local or approved test environment. Never point an automated test at production or real customer data without explicit authorization.
3. Choose a small set of critical user journeys and acceptance criteria. Include success, validation, empty, loading, and failure states where relevant.
4. Prefer accessible locators (role, label, text) over brittle CSS selectors or positional assumptions. Use stable test IDs only when semantic selectors are not sufficient.
5. Make tests deterministic with isolated fixtures, controlled network responses, known state, and cleanup. Avoid arbitrary sleeps; wait for observable conditions.
6. Cover keyboard interaction and essential viewport sizes when they are material to the feature. Check console errors and failed requests for relevant regressions.
7. Capture screenshots, traces, or videos only when they help diagnose a failure. Protect credentials, tokens, and personal information in artifacts.
8. Run the focused tests, then the relevant suite. Report exact commands, browser/runtime, pass/fail state, flaky behavior, and scenarios not covered.

Do not change application behavior merely to satisfy a brittle test. Do not claim visual or accessibility certification from a small smoke test. If the browser tooling is unavailable, state that limit and use the strongest safe alternative.
