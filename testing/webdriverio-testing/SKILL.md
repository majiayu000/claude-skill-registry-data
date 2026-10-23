---
name: webdriverio-testing
description: "Authors WebdriverIO E2E tests - `npm init wdio@latest` scaffolding, services architecture (sauce, browserstack, appium, devtools), reporters (spec, allure, junit), built-in Mocha/Jasmine/Cucumber framework integrations. WebdriverIO sits between Selenium (W3C protocol) and Playwright (modern API) - Selenium-protocol-compatible with rich plugin ecosystem. Use when the team needs WebDriver protocol + service-based device-farm integration."
---

# webdriverio-testing

## Overview

WebdriverIO (wdio) is a JavaScript / TypeScript E2E framework
built on the W3C WebDriver protocol. It differentiates from
Selenium by:

- Modern JS/TS API.
- Service architecture (browserstack, sauce, appium, devtools).
- Built-in framework integrations (Mocha, Jasmine, Cucumber).
- Multi-protocol support (WebDriver classic, WebDriver Bidi,
  Chrome DevTools Protocol).

## When to use

- A JS/TS project wants WebDriver-protocol compatibility (legacy
  systems / device farms).
- Service-based architecture matters (BrowserStack / Sauce Labs
  via wdio services is clean).
- Team already on Mocha or Jasmine; wants Cucumber-style BDD via
  wdio-cucumber-framework.
- Cross-platform via Appium service (mobile + web in one runner).

For pure-modern E2E, Playwright is simpler. For non-WebDriver
architecture, Cypress.

## Step 1 - Scaffold

```bash
npm init wdio@latest
```

Interactive prompts pick:

- Test runner type (E2E for browsers, mobile via appium).
- Framework (Mocha / Jasmine / Cucumber).
- Reporters (spec, allure, junit, etc.).
- Services (browserstack, sauce, appium, devtools, ...).
- Browser(s) to test.

What lands: `wdio.conf.ts` + `tests/specs/*.e2e.ts` +
`package.json` updates.

## Step 2 - Configure

```typescript
// wdio.conf.ts
export const config: WebdriverIO.Config = {
  runner: 'local',
  specs: ['./tests/specs/**/*.e2e.ts'],
  exclude: [],
  maxInstances: 4,
  capabilities: [
    {
      browserName: 'chrome',
      'goog:chromeOptions': { args: ['--headless=new'] },
    },
    {
      browserName: 'firefox',
      'moz:firefoxOptions': { args: ['-headless'] },
    },
  ],
  baseUrl: 'http://localhost:3000',
  services: ['chromedriver', 'geckodriver'],
  framework: 'mocha',
  reporters: ['spec', ['junit', { outputDir: 'reports/junit' }]],
  mochaOpts: { ui: 'bdd', timeout: 30000 },
};
```

`maxInstances: 4` runs 4 specs in parallel.

## Step 3 - Author a test (Mocha)

```typescript
// tests/specs/checkout.e2e.ts
import { browser, $ } from '@wdio/globals';
import { expect } from 'chai';

describe('Checkout flow', () => {
  beforeEach(async () => {
    await browser.url('/login');
    await $('[data-testid=email]').setValue('user@example.com');
    await $('[data-testid=password]').setValue('pwd');
    await $('button[type=submit]').click();
    await expect($('h1=Welcome')).toBeDisplayed();
  });

  it('completes checkout', async () => {
    await browser.url('/products/BOOK-001');
    await $('[data-testid=add-to-cart]').click();
    await expect($('[data-testid=cart-count]')).toHaveText('1');

    await browser.url('/checkout');
    await $('[name=card]').setValue('4242 4242 4242 4242');
    await $('button=Place order').click();
    await expect($('h1=Order confirmed')).toBeDisplayed();
  });
});
```

The `$` selector returns a wdio element (Promise-wrapped); methods
auto-wait. WDIO selectors have shortcuts:

- `$('h1=Welcome')` - text equals
- `$('h1*=Welcome')` - text contains
- `$('[data-testid=foo]')` - CSS selector
- `$('//button[@type="submit"]')` - XPath

## Step 4 - Services

```typescript
services: [
  // Local browser drivers
  'chromedriver',
  'geckodriver',

  // Cloud device farms
  ['browserstack', { user: 'USER', key: 'KEY' }],
  ['sauce', { user: 'USER', key: 'KEY' }],

  // Mobile
  ['appium', { command: 'appium', args: { port: 4723 } }],

  // DevTools (Puppeteer-style fast browser)
  'devtools',
];
```

Services handle setup / teardown; tests connect via the configured
capability.

## Step 5 - Run

```bash
# Run all specs
npx wdio run wdio.conf.ts

# Specific spec
npx wdio run wdio.conf.ts --spec ./tests/specs/checkout.e2e.ts

# Watch mode
npx wdio run wdio.conf.ts --watch
```

## Step 6 - Cucumber framework (BDD)

```typescript
// wdio.conf.ts
framework: 'cucumber',
specs: ['./features/**/*.feature'],
cucumberOpts: {
  require: ['./features/step-definitions/**/*.ts'],
  backtrace: false,
  requireModule: ['ts-node/register'],
  timeout: 60000,
},
```

```gherkin
# features/checkout.feature
Feature: Checkout

  Scenario: Complete a successful checkout
    Given I am logged in as "user@example.com"
    When I add "BOOK-001" to my cart
    And I complete checkout
    Then I see the order confirmation
```

```typescript
// features/step-definitions/checkout.steps.ts
import { Given, When, Then } from '@wdio/cucumber-framework';
import { $ } from '@wdio/globals';

Given(/^I am logged in as "(.+)"$/, async (email) => {
  await browser.url('/login');
  await $('[data-testid=email]').setValue(email);
  await $('[data-testid=password]').setValue('pwd');
  await $('button[type=submit]').click();
});

// ... etc.
```

Pairs with `cucumber-testing` (in the qa-bdd plugin)
conventions for the Gherkin layer.

## Step 7 - CI integration

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npx wdio run wdio.conf.ts
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: wdio-reports
          path: reports/
```

JUnit XML in `reports/junit/` feeds
`junit-xml-analysis` (in the qa-test-reporting plugin).

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Forgetting `await` on commands                                         | Returns a Promise; subsequent steps race.                                 | Always `await` (TS strict mode helps catch). |
| `browser.pause(2000)`                                                   | Flaky; defeats wdio's auto-waits.                                         | Trust assertion auto-waits; explicit waits when needed via `waitFor*`. |
| Massive `wdio.conf.ts`                                                  | Hard to navigate; merge conflicts.                                        | Split into env-specific configs; share via spread. |
| Mixing services that conflict (chromedriver + selenium-standalone)    | Driver conflict.                                                          | Pick one approach. |
| Running mobile + web in same wdio.conf.ts                              | Tightly coupled config; hard to maintain.                                | Separate configs per stack. |

## Limitations

- **Async-await everywhere.** Forgetting an `await` is the #1
  bug source.
- **Service config can be opaque.** Per-service docs vary.
- **Smaller community than Playwright / Cypress.** Stack overflow
  hit rate lower.

## References

- WebdriverIO at `webdriver.io`.
- `playwright-testing`,
  `cypress-testing`,
  `selenium-testing` - alternatives.
- `appium-testing` - wdio's appium service uses Appium underneath.
- `cucumber-testing` - wdio's cucumber framework integration.
