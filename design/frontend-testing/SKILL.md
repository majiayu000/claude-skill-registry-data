---
name: frontend-testing
description: "Use when deciding how a frontend feature is to be verified, or when a frontend defect slipped through: which test layer catches which kind of defect (logic, component, accessibility, contract, journey, visual, device, production errors), how end-to-end and visual tests are kept stable, and what runs when."
---

# frontend-testing

Step 6 and step 8 of the pipeline (`WORKFLOW.md`), next to `skills/tdd` (the doctrine and the
`data-test-*` selector convention), `skills/testing-anti-patterns` (what makes a test worthless) and
`skills/qa-exploratory-testing` (the human pass). Those say how to write a test and when. This block says
**which layer is owed for which kind of defect** on a user interface, because a frontend breaks in ways no
single layer sees. It names no framework and no tool, and it sets no coverage figure.

## When
A frontend feature is planned or reviewed and the question is "how will we know it works", a defect is
found in production or in review that the suite should have caught, or a project sets up its test
pipeline for the first time.

## Steps

1. **List the ways this feature can be wrong**, in the user's terms: wrong value shown, wrong state after
   an error, unreachable by keyboard, broken at a size, broken in another browser, looks different, breaks
   when the API changes, slow, fails only on a phone. Each item is a defect class.
2. **Give each defect class to the lowest layer that can catch it.** The table is the default; a class
   owned by no layer is a hole to say out loud.

   | Defect class | Layer that catches it | What it needs |
   |---|---|---|
   | Wrong logic, formatting, derived state | Unit test of the pure function or store | no browser |
   | Component renders the right states from its inputs, emits the right events | Component test (a real browser engine if it depends on layout, focus or scroll; a DOM emulation otherwise) | `data-test-*` selectors, `skills/tdd` |
   | Missing name, invalid ARIA, bad structure, duplicate ids | An accessibility rule engine run inside the component test and again on the journeys | the engine's report, read; it finds a fraction (`skills/accessibility` §2.12) |
   | Keyboard path, focus order, announcements, zoom | A manual pass with keyboard and screen reader on the critical journeys | `skills/qa-exploratory-testing`, `skills/accessibility` |
   | The front end and the API drifting apart | A consumer-driven contract test: the front end records what it relies on, the API's pipeline verifies it | the contract-first spec of `skills/api-design` |
   | A user journey that crosses pages and services | End-to-end test of the few journeys that carry the business | at least two rendering-engine families |
   | Looks wrong, layout moved, theme broken | Visual regression on stable fixtures | pinned fonts, fixed data, frozen clock, animations off |
   | Touch, virtual keyboard, safe areas, low-end performance | A pass on a real device before release | emulation does not reproduce these |
   | Weight, load and interaction cost | A budget check in the pipeline | `skills/webperf` §4.10 |
   | What no test imagined | Browser error reporting in production | release label and source maps (`skills/webperf` §6.5), personal data scrubbed (`business/data-protection`), `skills/observability-instrumentation` |

3. **Write each test at that layer and no higher.** A rule about a price format is a unit test, not a
   journey; a journey that exists to prove the format is the slow, flaky version of a unit test.
4. **Keep end-to-end tests few, about journeys, and deterministic.**
   - A journey is something a user finishes (sign in, buy, export), asserted on its outcome; not every
     branch of every form.
   - Waits are on conditions (an element, a response, a state), never fixed sleeps. Each test creates the
     data it needs and leaves none behind; tests do not depend on order or on each other.
   - Run them on the engine families that matter to the audience (Chromium-based, Gecko-based, WebKit-based
     at least once before release), because layout, form controls, date inputs, focus rules and many newer
     features differ. The project's config lists the engines, and a family left out is recorded as left
     out.
   - Selectors are the `data-test-*` attributes of `skills/tdd`, not CSS classes or visible text that a
     redesign or a translation changes.
   - When the runner is Playwright Test, its locators, waiting, saved sign-in state, network mocking, fixtures,
     retries and traces are in [`references/01-playwright.md`](./references/01-playwright.md) (pinned to 1.63).
5. **Make visual tests stable before trusting them.** A visual test that fails for no reason is deleted
   within a month. Fix the data, freeze the clock and randomness, disable animation, load the exact fonts
   from the repository, and render in the same container image everywhere. Snapshot components in their
   states rather than whole pages. A human reviews each change and approves it deliberately; an automatic
   "update all" turns the layer into a rubber stamp. It complements assertions and never replaces them.
6. **Place each layer by cost.** Fast layers (static checks, unit, component, accessibility engine) run on
   every push. The slow ones (end-to-end across engines, visual regression, full budget measurement) run
   on merge or on a schedule, with a rule that a failure blocks release. A real-device pass is a release
   step with an owner.
7. **A flaky test is a defect with a deadline.** Quarantine it the first time (skip it visibly, record an
   owner and a date), find the cause (shared data, timing, order, environment), fix or delete. A
   suite people re-run until green proves nothing. This is `skills/testing-anti-patterns` applied to the
   pipeline.
8. **Optionally, measure whether tests assert.** Mutation testing changes the code and checks that a test
   fails; it is slow, so aim it at logic-heavy pure modules, not at components. Coverage is a signal,
   never a target (`skills/testing-anti-patterns`).

## Output / checkpoint
For a feature: the defect classes, the layer owning each, and the tests added at each layer. For a missed
defect: the class it belonged to, why the owning layer did not catch it, and the test now added there. The
checkpoint is the one `skills/tdd` already writes; this block adds no new one.

## Guardrails
- **No tool, framework or threshold is imposed.** A project picks its runner and engines; this block asks
  only that the choice be recorded.
- **A layer that never fails is not a layer.** If the accessibility engine or the visual diff has never
  caught anything, check that it runs and that it can fail.
- **Never test the framework.** Assert what the user sees and what the contract promises.
- **Never replace the manual pass with the tool.** Rule engines and screenshots cannot judge a name, a
  focus order or a layout's meaning.
- A contract test is not an integration test with a mock: the mock drifts, the contract is verified by the
  other side.

## Mechanical checks

```
grep -nE 'axe|a11y|accessib' package.json
grep -rnE 'chromium|firefox|webkit' playwright.config.* wdio.conf.* 2>/dev/null
grep -rnE 'toHaveScreenshot|matchScreenshot|toMatchImageSnapshot' tests
grep -rnE 'Sentry\.init|Bugsnag\.start|datadogRum|window\.onerror' src
grep -rnE 'pact|contract' tests
grep -rnE 'waitForTimeout|sleep\(|cy\.wait\([0-9]' tests
grep -rnE '\.(skip|only)\(' tests
```

- The first confirms an accessibility engine is a dependency and the pipeline file runs it (grep the CI
  config for the same words).
- The second lists the engines in the end-to-end config; the answer is compared with the recorded list.
- Error reporting is initialised with a release identifier (read the call).
- Fixed waits and left-over `only`/`skip` in tests are findings.
- The runner and file names above vary by project; adapt the patterns, keep the intent.

## Origin
The list of verification topics (accessibility in the pipeline, multi-engine runs, visual regression,
real-device passes, consumer contract tests, error monitoring, mutation testing) comes from reading the
public `Front-End-Checklist` repository (README and package metadata declare MIT; no licence file is
present, so only the topics were used, not its sentences), on 2026-10-02. The layer-to-defect table, the
placement by cost and the flaky-test policy are ours, following `skills/tdd` and
`skills/testing-anti-patterns`. Facts about contract testing follow the consumer-driven contract pattern as
documented by its practitioners; the WAI and WCAG pages are the source for what automated checks cannot
see. Deliberately not taken: a coverage percentage, a named test runner or screenshot service, and mock
guidance (already in `skills/testing-anti-patterns`). A separate `e2e-testing` block was not written: the
end-to-end doctrine is `skills/tdd` and the stability rules are step 4 here. Written, not yet run on
real work.

The Playwright reference (`references/01-playwright.md`) is rewritten from the runner's own documentation
(`microsoft/playwright`, `docs/src`, Apache-2.0), read 2026-10-02 at the 1.63 release notes: best practices,
locators, auto-waiting, assertions, authentication, mocking, fixtures, retries, parallelism, timeouts, trace
viewer, snapshots, web server and accessibility testing. No sentence or example is copied. Facts that move,
pinned to 1.63: the default timeouts (test 30 s, assertion 5 s), the trace modes, the locator list. Not read:
component testing, the test-agents pages, the reporter API, and the other language bindings. Refresh with
`skills/source-freshness` on the next minor.
