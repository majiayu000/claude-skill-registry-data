---
name: writing-browser-e2e-tests
description: >-
  Guides writing browser end-to-end tests that find elements as users do, wait on what the action produced, keep page
  knowledge in page objects, organize one feature per file, and run scenario-backed suites from generated specs.
when_to_use: >-
  Use when writing, organizing, or reviewing an end-to-end test that drives a real browser, or when such a test is
  flaky, brittle, or order-dependent.
compatibility: Requires a browser test runner, a served origin, and the owner's scenario corpus where one exists.
---

# Writing Browser End-to-End Tests

[End-to-End Testing](../../../repo-governance/development/end-to-end-testing.md) owns the boundary, per-case fixtures,
the exact origin, meaningful assertions, hook placement, and cleanup. Test Boundaries and Gates and Layers and Adapters
own layers and gates, Bindings and Exemptions owns bindings, and Test Design owns the shape of any test. This skill
covers the choices a browser suite adds.

## Find Elements the Way a User Does

Locate in this order, taking the first that identifies the element:

1. role and accessible name;
2. form label;
3. visible text;
4. a dedicated test identifier;
5. a structural selector, only when nothing above applies.

Users and assistive technology find elements by role, name, and label, so those locators survive a redesign that leaves
behaviour alone. A role locator that cannot find a control often reveals an accessibility defect worth reporting. Avoid
positional selectors, deep structural chains, and generated identifiers; each breaks on changes nobody would call a
behaviour change.

## Wait on the Result, Never the Clock

Assert with retrying assertions on a locator, which wait until the expected state appears or time out. Reading a value
once and comparing it races the page. A fixed sleep is either too short on a slow run or wasted on a fast one, and in
both cases it hides what the test is really waiting for.

A retry that turns a failure green is an intermittent failure, diagnosed under Intermittent Failures, not a pass.

## Keep Page Knowledge in Page Objects

A page object holds one page's or component's locators and the actions a user takes there. Tests and step bindings call
those actions and keep the assertions, so a failure names the behaviour that broke. When the markup changes, one page
object changes instead of every test. Reusable pieces, such as a header or a dialog, become their own component objects.

## Organize by Feature

- **One feature per spec file,** named for that feature in kebab case, so a failing file names what broke.
- **Group by feature, then by business rule,** then the cases that illustrate each rule.
- **Keep specs, page objects, fixtures, and helpers in separate trees.**
- **Parallel by default.** Isolated tests run in any order and at once.
- **Serial only for a deliberately interdependent flow.** Prefer one journey test. Where a flow is too long for one, a
  serial group counts as a single case under End-to-End Testing: it owns its fixtures from its first step to its last,
  and nothing outside it depends on its state.

Setting state up through the served interface's own requests, then verifying through the page, is faster than clicking
through setup, provided the data is synthetic and owned as
[Test Data Isolation](../../../repo-governance/development/test-data-isolation.md) requires.

## Scenario-Backed Suites Run From Generated Specs

Where the owner has a scenario corpus, the suite generates its runnable specs from that corpus before every run. The
generated files stay untracked and are never edited, because the next generation overwrites them and an edit there
becomes a test no scenario states. Hand-written spec files are only for suites with no owning feature.

## Test First, Even at This Layer

Write the failing journey before the feature exists, and confirm it fails because the feature is missing rather than
because the environment is misconfigured, per Cycle and Evidence. A check that must stay manual for now is a dated,
repeatable script with a discrete expected observation per step, never an undated "tested by hand", and it becomes an
automated spec once the behaviour recurs.

Capture a trace and a screenshot on failure only, and keep them under the evidence rules of Evidence Safety and
Accessibility.

## Illustrative Example

As an illustration only: in Playwright, `page.getByRole("button", { name: "Save" })`, `getByLabel`, `getByText`, and
`getByTestId` follow the locator order above; `await expect(locator).toHaveText("Saved")` retries until it holds;
`test.describe.configure({ mode: "serial" })` marks a serial group, which its documentation also discourages; and
`playwright-bdd` generates specs with `bddgen` into an ignored `.features-gen` directory before `playwright test` runs.
