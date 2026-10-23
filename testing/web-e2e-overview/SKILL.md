---
name: web-e2e-overview
description: "Teaches web end-to-end testing from first principles: what browser-driven E2E covers and how it differs from unit and integration tests, a decision table for choosing between Playwright, Cypress, Selenium WebDriver, WebdriverIO, Puppeteer, TestCafe and the BrowserStack / Sauce Labs / LambdaTest cloud grids based on files already present in the repo, install and first-run commands for each, and the flakiness traps (fixed sleeps, CSS and XPath selectors, state shared between tests) that sink new suites. Use when a web application has no E2E coverage yet, when picking or replacing an E2E framework, or when a first browser test needs to go green end to end."
---

# web-e2e-overview

## What web E2E testing is

Web end-to-end (E2E) testing drives a real browser the way a user would: a page is
loaded, interactions are performed (clicks, form fills, navigations), and outcomes are
asserted against what the user should see. Per [playwright.dev/docs/intro][pwi]:
"Playwright Test is an end-to-end test framework for modern web apps. It bundles test
runner, assertions, isolation, parallelization and rich tooling." That bundle is what
distinguishes an E2E framework from a bare browser-automation library: a runner, an
assertion library with retry, per-test isolation, and parallelism.

E2E sits above unit and integration tests, not instead of them. Unit tests call a
function; integration tests call a module against a real dependency; E2E boots the
whole stack (browser, app, API, database) and checks a user journey. It is the only
layer that catches "the button is wired to the wrong handler", and the most expensive
layer to own: per [martinfowler.com/articles/practical-test-pyramid][ptp], E2E tests
"are notoriously flaky and often fail for unexpected and unforeseeable reasons"
(browser quirks, timing, animations, popups), so "you should aim to reduce the number
of end-to-end tests to a bare minimum" and spend them on core journeys only: search a
product, add to basket, check out.

Practical starting budget (a convention among practitioners, not a documented
standard): five to fifteen E2E specs covering signup, login, the primary create /
read / update path, checkout or submit, and one permissions case. Everything else
belongs a layer down.

## Choosing a framework

Read the repo first, then the table. Every row is keyed on something you can observe
without asking anyone. Take the **first** row that matches, top to bottom.

```bash
# Run at the repo root before choosing anything.
ls playwright.config.* cypress.config.* wdio.conf.* .testcaferc.* nightwatch.conf.* 2>/dev/null
ls -d cypress e2e tests/e2e 2>/dev/null
grep -iE '"(@playwright/test|cypress|webdriverio|@wdio/cli|puppeteer|testcafe|nightwatch|selenium-webdriver)"' package.json
grep -riE 'selenium-(java|webdriver)|Selenium\.WebDriver' pom.xml build.gradle* requirements.txt *.csproj Gemfile 2>/dev/null
```

| What you observe | Use | Why |
|---|---|---|
| `playwright.config.ts` / `.js`, or `@playwright/test` in `package.json` | **Playwright** | Already chosen. Add specs, do not add a second runner. |
| `cypress.config.ts` / `.js`, or a `cypress/` directory | **Cypress** | Already chosen. Extend it; a migration is a separate project with its own budget. |
| `wdio.conf.ts` / `.js` | **WebdriverIO** | Already chosen. |
| `.testcaferc.json` / `.testcaferc.js` | **TestCafe** | Already chosen. |
| `nightwatch.conf.*`, or `nightwatch` in `package.json` | **Nightwatch (legacy)** | Keep it running, but plan a migration to Playwright or WebdriverIO rather than growing the suite. |
| `selenium-java`, `selenium-webdriver`, or `Selenium.WebDriver` in a build file | **Selenium WebDriver** | Already chosen, usually with years of page objects behind it. |
| No E2E config anywhere, and the repo has a `package.json` | **Playwright** | Default for greenfield. One install covers Chromium, Firefox and WebKit [[pwi]]. |
| No E2E config, and the team will not add Node (pure Java / C# / Ruby / Python shop) | **Selenium WebDriver** | The only option with first-class bindings in Java, Python, C#, Ruby, JavaScript and Kotlin [[sellib]]. |
| Safari / WebKit coverage is a stated requirement | **Playwright** | Ships WebKit in the default install [[pwi]]. Cypress lists WebKit as experimental and opt-in [[cybr]]. |
| The same suite must also drive a native mobile or Electron app | **WebdriverIO** | Automates web, hybrid and native mobile via Appium, and native desktop such as Electron [[wdiowhy]]. |
| The task is scraping, screenshotting or HTML-to-PDF, with no assertions | **Puppeteer** | A library, not a test framework: "a JavaScript library which provides a high-level API to control Chrome or Firefox" [[ppt]]. No runner, no isolation, no parallelism. |
| A no-WebDriver architecture is a hard constraint and its wait model appeals | **TestCafe** | Runs on Node.js and waits automatically for selectors, actions, assertions, XHR and redirects [[tcwait]]. |
| Real iOS / Android devices, old browser versions, or a large OS matrix are required | **Keep the runner above, add a cloud grid** | See "Real devices and browser matrices" below. This is an execution target, not a framework choice. |

Tie-break when two rows both look true: whatever is already in the repo wins. A second
E2E framework doubles the CI cost, the selector conventions and the flake surface, and
buys coverage you could get by adding one grid config to the framework you have. If the
repo shows **two competing frameworks** (`@playwright/test` AND `cypress` both in
devDependencies), stop and ask which is canonical - do not silently pick one. And never
recommend a framework swap on an existing project without a stated reason: "modernity"
alone burns years of page-object investment for marginal gain.

## First runnable path: Playwright

For the default choice, per [playwright.dev/docs/intro][pwi]:

```bash
# 1. Scaffold: prompts for TS/JS, tests folder, CI workflow, browser binaries.
npm init playwright@latest

# 2. Run the generated example to confirm the install is healthy.
npx playwright test
```

The wizard writes `playwright.config.ts` and `tests/example.spec.ts`, and updates
`package.json` [[pwi]]. `npx playwright test` runs headless and in parallel by default
across Chromium, Firefox and WebKit [[pwi]]. **Success looks like:** every example
spec passes on a clean machine, with no browser window appearing. If it fails here,
the problem is the install, not your app.

Then open `tests/example.spec.ts`, delete it, and write your first real spec in that
shape:

```ts
import { test, expect } from '@playwright/test';

test('user can reach the pricing page', async ({ page }) => {
  await page.goto('https://example.com/');
  await page.getByRole('link', { name: 'Pricing' }).click();
  await expect(page.getByRole('heading', { name: 'Pricing' })).toBeVisible();
});
```

Two things in that snippet are the whole discipline: locators named after what the
user sees, and an `await expect(...)` assertion that retries. Both are covered below.

## First runnable path for the other tools

| Tool | Install | First run |
|---|---|---|
| Cypress | `npm install cypress --save-dev` [[cyins]] | `npx cypress open`, then pick end-to-end or component mode [[cyins]] |
| Selenium (Python) | `pip install selenium` [[sellib]] | run your test file with the project's runner (pytest, JUnit, NUnit) |
| Selenium (Java/Maven) | add the `org.seleniumhq.selenium:selenium-java` dependency to `pom.xml` [[sellib]] | `mvn test` |
| WebdriverIO | `npm init wdio@latest .` [[wdio]] | `npx wdio run ./wdio.conf.js` [[wdio]] |
| Puppeteer | `npm i puppeteer` (downloads a compatible browser) [[ppt]] | `node your-script.js` |
| TestCafe | `npm install -g testcafe` [[tcgs]] | `testcafe chrome getting-started.js` [[tcgs]] |

Selenium drives "a browser natively, as a user would, either locally or on a remote
machine using the Selenium server" [[selwd]], which is why it has no bundled runner:
you bring JUnit, pytest, NUnit or RSpec yourself.

## Real devices and browser matrices

A local runner covers the engines installed on the machine. When the requirement is
real hardware, legacy browser versions, or dozens of OS/browser pairs, point the same
suite at a hosted grid instead of rewriting it.

| Provider | Credentials | Best fit |
|---|---|---|
| BrowserStack Automate | username + access key from the account profile, set in `browserstack.yml` [[bs]] | broadest device matrix - advertises "3000+ real devices and desktop browsers" [[bs]] - and enterprise procurement |
| Sauce Labs | username + access key from User Settings [[sl]] | Selenium-grid-centric parallel CI farms; region-specific hubs, e.g. `https://ondemand.us-west-1.saucelabs.com/wd/hub`, `https://ondemand.eu-central-1.saucelabs.com/wd/hub` [[sl]] |
| LambdaTest | `LT_USERNAME` and `LT_ACCESS_KEY` environment variables [[lt]] | cost-sensitive, smaller scale; grid endpoint and capabilities are generated from the dashboard [[lt]] |

A grid is recommended **in addition to** the chosen framework, never as a substitute.
Two pairing cautions: Cypress runs its own runner, not WebDriver, so it cannot target a
WebDriver hub URL - use Cypress Cloud or the vendor's Cypress-specific runner instead.
And Puppeteer stays Chromium-only no matter what grid sits behind it - for cross-browser
coverage pick Playwright. Setup for all three vendors is in `cloud-grid-e2e`.

Decide the matrix from analytics, not from anxiety. Grid minutes are billed, and a
matrix of twenty combinations turns a two-minute suite into a twenty-minute one.

## The traps that bite first

**1. Fixed sleeps instead of retrying assertions.** This is the single largest source
of flake. A hard-coded pause is either too short (fails on a slow CI box) or too long
(a suite that takes an hour). Cypress states plainly that "waiting for arbitrary time
periods using `cy.wait(Number)` is an anti-pattern" and directs you to "use route
aliases or assertions to guard Cypress from proceeding until an explicit condition is
met" [[cybp]]. Playwright's equivalent: "By using web first assertions Playwright will
wait until the expected condition is met" [[pwbp]], and before every action it runs
actionability checks for visibility, stability, event reception and enabled state
[[pwact]].

```ts
// Wrong: guesses at timing, fails on a slow runner.
await page.waitForTimeout(3000);
expect(await page.locator('.toast').isVisible()).toBe(true);

// Right: retries until the condition holds or the timeout expires.
await expect(page.getByRole('status')).toHaveText('Saved');
```

Corollary: `isVisible()` and friends return a boolean once, immediately, with no
waiting [[pwbp]]. If you find yourself adding a sleep to make one pass, you wanted a
retrying assertion instead.

**2. CSS and XPath selectors instead of role and label locators.** Selectors bound to
class names, `nth-child` positions or generated IDs break on the next CSS refactor
even though nothing a user can perceive has changed. Playwright's guidance is to
"prefer user-facing attributes to XPath or CSS selectors" and reach for
`page.getByRole('button', { name: 'submit' })` [[pwbp]]. Cypress, which has no role
locator by default, instead tells you to "add `data-*` attributes to make it easier to
target elements" and use `[data-cy="submit"]` selectors, "isolated from styling or
behavioral changes" [[cybp]].

Preference order that works in every framework: accessible role plus accessible name,
then label or placeholder text, then visible text, then a dedicated test attribute
(`data-testid` / `data-cy`), and only then CSS. Never XPath positions. The bonus is
real: a test that can only find the button by its role is a test that fails when the
button loses its accessible name.

**3. State shared between tests.** Order-dependent tests pass locally in one order and
fail in CI in another, and they fail catastrophically under parallelism. Playwright:
"Each test should be completely isolated from another test and should run
independently with its own local storage, session storage, data, cookies etc."
[[pwbp]]. Cypress: "Tests should always be able to be run independently from one
another and still pass" [[cybp]]. Both recommend `beforeEach` for setup rather than
letting test N depend on test N-1 [[pwbp]] [[cybp]].

This matters more than it sounds because parallelism is on by default. Playwright runs
tests in worker processes that are "OS processes, running independently", each with
its own browser, and "you can't communicate between the workers" [[pwpar]]. A shared
login, a shared seeded record, or a fixed username will collide the moment two workers
touch it. Create per-test data with a unique suffix, and set up auth state
programmatically rather than by driving the login form in every spec.

**4. Treating E2E as the coverage strategy.** Every validation rule pushed into a
browser test costs a browser boot. When a case can be checked one layer down, check it
one layer down [[ptp]].

## Going deeper

Optional. Each tool above has a dedicated in-depth component if the full set is
installed alongside this one; nothing here depends on them.

| Tool | Deeper reference |
|---|---|
| Playwright | `playwright-testing` |
| Cypress | `cypress-testing` |
| Selenium WebDriver | `selenium-testing` |
| WebdriverIO | `webdriverio-testing` |
| Puppeteer | `playwright-testing` (Puppeteer is a browser-automation library, not a test framework; migrate to Playwright) |
| TestCafe | `playwright-testing` (marginal adoption; not recommended for new projects) |
| BrowserStack / Sauce Labs / LambdaTest | `cloud-grid-e2e` (one pattern, per-vendor references) |

[pwi]: https://playwright.dev/docs/intro
[pwbp]: https://playwright.dev/docs/best-practices
[pwact]: https://playwright.dev/docs/actionability
[pwpar]: https://playwright.dev/docs/test-parallel
[cyins]: https://docs.cypress.io/app/get-started/install-cypress
[cybp]: https://docs.cypress.io/app/core-concepts/best-practices
[cybr]: https://docs.cypress.io/app/references/launching-browsers
[selwd]: https://www.selenium.dev/documentation/webdriver/
[sellib]: https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
[wdio]: https://webdriver.io/docs/gettingstarted/
[wdiowhy]: https://webdriver.io/docs/why-webdriverio/
[ppt]: https://pptr.dev/
[tcgs]: https://testcafe.io/documentation/402635/guides/overview/getting-started
[tcwait]: https://testcafe.io/documentation/402827/guides/advanced-guides/built-in-wait-mechanisms
[bs]: https://www.browserstack.com/docs/automate/selenium/getting-started/nodejs
[sl]: https://docs.saucelabs.com/basics/data-center-endpoints/
[lt]: https://www.lambdatest.com/support/docs/python-with-selenium-running-python-automation-scripts-on-lambdatest-selenium-grid/
[ptp]: https://martinfowler.com/articles/practical-test-pyramid.html
