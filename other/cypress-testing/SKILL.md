---
name: cypress-testing
description: "Authors and improves Cypress E2E tests - installs Cypress, configures `cypress.config.ts`, authors `cy.*` command chains, refactors existing specs (`cy.wait(ms)` sleeps into assertions, repeated flows into `cy.session` custom commands), and debugs with the time-travel GUI; Cypress Cloud for parallel runs and recording. Use for both greenfield test authoring and improving hand-written specs already in the codebase. For automated refactor of raw Cypress Studio recordings specifically, use a dedicated codegen-review pass."
---

# cypress-testing

## Overview

Per [cy-overview][cy]:

[cy]: https://docs.cypress.io/guides/overview/why-cypress

> "Cypress is described as 'a next generation front end testing
> tool built for the modern web.'"

Differentiators ([cy-overview][cy]):

> - **Time Travel Debugging:** "Cypress takes snapshots as your
>   tests run. Hover over commands in the Command Log to see
>   exactly what happened at each step."
> - **Automatic Waiting:** "Never add waits or sleeps to your
>   tests. Cypress automatically waits for commands and assertions
>   before moving on."
> - **Reliability:** "The testing approach avoids
>   Selenium/WebDriver architecture, resulting in fast, consistent
>   and reliable tests that are flake-free."

## When to use

- The team has invested in Cypress; a migration is unlikely.
- The test author values the time-travel debugger / GUI
  experience.
- Component testing is needed (Cypress supports React / Angular /
  Vue / Svelte component testing).
- Single-browser focus is acceptable (Chromium-first; Firefox /
  Edge supported but secondary).

For cross-browser including WebKit, see
`playwright-testing`.

## How to use

1. Install Cypress and scaffold the project (`npm install --save-dev cypress`, `npx cypress open`).
2. Set `baseUrl`, `specPattern`, and `retries` in `cypress.config.ts`.
3. Add `@testing-library/cypress` so specs select by role / label, not by CSS class.
4. Author each flow as a `describe` / `it` block; lean on auto-waiting assertions instead of `cy.wait(ms)`.
5. Extract repeated auth into a `cy.session`-backed custom command called from `beforeEach`.
6. Run headless in CI (`npx cypress run`); debug failures by replaying commands in the time-travel GUI.
7. For scale, record + parallelize via Cypress Cloud and upload screenshot artifacts on failure (see [references/ci-and-cloud.md](references/ci-and-cloud.md)).

## Step 1 - Install

```bash
npm install --save-dev cypress
npx cypress open   # first run scaffolds the project
```

The interactive setup creates `cypress.config.ts` + `cypress/`
directory.

## Step 2 - Configure

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{ts,tsx}',
    video: true,
    screenshotOnRunFailure: true,
    retries: { runMode: 2, openMode: 0 },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
});
```

## Step 3 - Author E2E tests

```typescript
// cypress/e2e/checkout.cy.ts
describe('Checkout flow', () => {
  beforeEach(() => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.env(['USER_PASSWORD']).then(({ USER_PASSWORD }) => {
      cy.get('[data-testid="password"]').type(USER_PASSWORD, { log: false });
    });
    cy.get('[data-testid="signin-btn"]').click();
    cy.contains('Welcome').should('be.visible');
  });

  it('completes checkout end-to-end', () => {
    cy.visit('/products/BOOK-001');
    cy.contains('button', /add to cart/i).click();
    cy.get('[data-testid="cart-count"]').should('have.text', '1');

    cy.visit('/checkout');
    cy.env(['TEST_CARD_NUMBER']).then(({ TEST_CARD_NUMBER }) => {
      cy.get('[name="card"]').type(TEST_CARD_NUMBER, { log: false });
    });
    cy.contains('button', /place order/i).click();
    cy.contains('Order confirmed', { timeout: 10000 }).should('be.visible');
  });
});
```

Per [cy-overview][cy], assertions auto-wait - no `cy.wait(2000)`
needed.

Never type a password or card number as a literal. Per [cy-env][cyenv],
`cy.env()` (Cypress 15.10+) yields the requested keys, and per
[cy-env-guide][cyenvguide] Cypress strips the `CYPRESS_` prefix, so CI
sets `CYPRESS_USER_PASSWORD` from its secret store. `{ log: false }`
keeps the value out of the Command Log.

[cyenv]: https://docs.cypress.io/api/commands/env
[cyenvguide]: https://docs.cypress.io/app/guides/environment-variables

## Step 4 - Use cypress-testing-library

For accessibility-first selectors:

```bash
npm install --save-dev @testing-library/cypress
```

```typescript
// cypress/support/commands.ts
import '@testing-library/cypress/add-commands';

// Now in tests:
cy.findByRole('button', { name: /sign in/i }).click();
cy.findByLabelText('Email').type('user@example.com');
```

`findByRole` (from cypress-testing-library) is the Cypress
equivalent of Playwright's `getByRole` - preferred for
accessibility-aware testing.

## Step 5 - Custom commands

```typescript
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.findByLabelText('Email').type(email);
    cy.findByLabelText('Password').type(password, { log: false });
    cy.findByRole('button', { name: /sign in/i }).click();
    cy.url().should('not.include', '/login');
  });
});

// Usage in tests:
beforeEach(() => {
  cy.env(['USER_PASSWORD']).then(({ USER_PASSWORD }) => {
    cy.login('user@example.com', USER_PASSWORD);
  });
});
```

`cy.session(...)` caches the auth state across tests - reuse the
login result, avoid re-running the login flow.

## Step 6 - Run

```bash
# Open the GUI (interactive; great for development)
npx cypress open

# Headless (CI)
npx cypress run

# Single spec
npx cypress run --spec "cypress/e2e/checkout.cy.ts"

# Specific browser
npx cypress run --browser firefox
npx cypress run --browser chrome
```

## Step 7 - Time-travel debugger

Per [cy-overview][cy]: "Hover over commands in the Command Log to
see exactly what happened at each step."

In `cypress open` mode:
1. Run a test.
2. Hover over commands in the left-side log.
3. See the DOM snapshot for each step in the main browser
   pane.
4. Click a command → freeze the state for inspection.

This is Cypress's killer feature - debugging by visually replaying
the test.

## Step 8 - Cypress Cloud + CI

Recording and parallel runs go through Cypress Cloud (paid; OSS
alternative `currents-integration` in the qa-test-reporting plugin),
and the GitHub Actions job wires `cypress-io/github-action` +
screenshot artifacts on failure. Commands and the full workflow YAML:
[references/ci-and-cloud.md](references/ci-and-cloud.md).

## Worked example

A team has a hand-written `checkout.cy.ts` that logs in from scratch
in every test and sleeps `cy.wait(3000)` before asserting the cart
count. It flakes about 1 run in 5 on CI.

1. The login block moves into a `login` custom command wrapped in
   `cy.session(...)`, called from `beforeEach` with the password read
   via `cy.env()` instead of the old literal - the auth flow now runs
   once and is cached.
2. `cy.wait(3000)` is deleted; the check becomes
   `cy.get('[data-testid="cart-count"]').should('have.text', '1')`,
   which auto-retries until the count settles.
3. CSS-class selectors like `cy.get('.signin-btn')` are replaced with
   `cy.findByRole('button', { name: /sign in/i })` via
   cypress-testing-library.
4. `npx cypress run --spec cypress/e2e/checkout.cy.ts` is green 20/20
   locally; the GitHub Actions job records the run to Cypress Cloud.

Result: the flow runs faster (login cached, no fixed sleep) and the
flake disappears because every wait is now assertion-driven.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| `cy.wait(2000)` between actions                                        | Defeats Cypress's auto-wait; flaky.                                       | Trust assertions; chain commands. |
| `cy.get('.button-class')` (CSS class)                                  | Brittle; defeats `findByRole` patterns.                                   | cypress-testing-library + `data-testid` (Steps 3-4). |
| Cross-test state via global variables                                  | Tests order-dependent.                                                    | `cy.session()` for auth; per-test fresh state. |
| Mixing Cypress + plain xUnit assertions                                | Confusing; two assertion styles.                                          | Cypress chains throughout. |
| Running Cypress against production                                     | Cypress can mutate state; pollutes prod data.                            | Local / staging only. |

## Limitations

- **Single-browser-process architecture.** Per [cy-overview][cy]:
  "avoids Selenium/WebDriver architecture" - but this also means
  no native multi-domain testing (workarounds exist).
- **Same-tab restriction.** Originally Cypress only tested
  same-tab; multi-tab support added later but with caveats.
- **No native mobile.** Mobile via emulation only; for native, see
  `appium-testing` (in the qa-mobile plugin).
- **Cypress Cloud is paid.** OSS-budget teams use
  `currents-integration`.

## References

- [cy][cy] - Cypress overview, key features (time-travel,
  automatic waiting, native browser access), three test types
  (E2E, component, accessibility).
- [cyenv][cyenv] - `cy.env()` command: reads env keys, added in 15.10.0.
- [cyenvguide][cyenvguide] - environment variables and secrets guide:
  `CYPRESS_` prefix stripping.
- `playwright-testing`,
  `selenium-testing`,
  `webdriverio-testing` - 
  alternative E2E frameworks.
- `currents-integration` - OSS analytics alternative to Cypress Cloud.
