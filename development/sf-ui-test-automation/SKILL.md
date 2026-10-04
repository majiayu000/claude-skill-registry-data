---
name: sf-ui-test-automation
description: Build automated Salesforce UI tests - pick the cheapest tier that can catch the bug (Apex unit, LWC Jest, UTAM end-to-end, Agentforce agent tests), scaffold a UTAM plus WebdriverIO project with Salesforce's own page objects, authenticate a test run without committing a credential, and keep the suite deterministic in CI. Use when writing or repairing browser-level tests, not when configuring an org.
---

# Salesforce UI test automation

## When to use

- A regression escaped Apex tests and Jest because it lives in the rendered page.
- A committed end-to-end suite is needed for a flow a user clicks through.
- An existing UI suite is flaky, slow, or authenticates by pasting a password into a config file.
- An Agentforce agent needs behavioural tests.
- Not for configuring an org through a browser - that is `sf-setup-automation`.
- Not for component-level assertions, which belong in `sf-lwc-jest-testing`.

## Pick the tier that can actually catch the bug

A browser test is the most expensive assertion in the codebase. Work up the table, not down.

| Tier | Tool | Catches | Cost |
| --- | --- | --- | --- |
| Apex unit | `sf apex run test` | Server logic, sharing, triggers, governor limits | Seconds, gated by `vf-check apex` |
| LWC unit | `@salesforce/sfdx-lwc-jest` 7.9.0 | Component rendering, wire adapters, DOM events | Seconds, gated by `vf-check jest` |
| End-to-end | UTAM + WebdriverIO | Navigation, Lightning shell, cross-component flows, permissions as a user sees them | Minutes, needs an org |
| Agent behaviour | `sf agent test run` | Agentforce topic and action selection | Minutes, needs an org |
| Exploratory | Playwright MCP browser tools | "What does this page even do" - never committed as a test | Interactive |

If a Jest test can fail on the bug, write the Jest test. Everything below assumes it cannot.

## 1. The UTAM stack, with versions

UTAM is Salesforce's UI Test Automation Model: page objects declared as `.utam.json`, compiled into
JavaScript classes, driven by a runtime that resolves shadow DOM for you.

| Package | Latest | Role |
| --- | --- | --- |
| `@utam/core` | 3.3.0 | Runtime API - `utam.load`, `utam.getCurrentDocument` |
| `wdio-utam-service` | 3.3.0 | WebdriverIO service that wires the runtime into a run |
| `salesforce-pageobjects` | 12.0.0 | "Page objects provided by Salesforce to test Lightning Experience using the UI Test Automation Model" |
| `@salesforce/sfdx-lwc-jest` | 7.9.0 | The tier below; present in the same project |

`salesforce-pageobjects` is the part that makes this viable: the Lightning shell, app navigation and
Flexipage internals are already modelled, so your own page objects only describe your components.
There is no `@utam/cli` package - the compiler is invoked as `utam -c utam.config.js`.

## 2. Project shape

`utam.config.js` - what to compile and where the classes land:

```js
module.exports = {
    pageObjectsFileMask: ['force-app/**/__utam__/**/*.utam.json'],
    pageObjectsOutputDir: 'pageObjects',
    alias: { 'utam-sfdx/': 'utam-js-recipes/', 'utam-*/': 'utam-preview/' },
    lint: { printToConsole: false },
};
```

`wdio.conf.js` - the service, and the Salesforce page objects injected into the runtime:

```js
const { UtamWdioService } = require('wdio-utam-service');

exports.config = {
    specs: ['force-app/test/**/*.spec.js'],
    capabilities: [{ browserName: 'chrome', 'goog:chromeOptions': { args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] } }],
    services: [[UtamWdioService, { implicitTimeout: 0, injectionConfigs: ['salesforce-pageobjects/ui-global-components.config.json'] }]],
    framework: 'jasmine',
    waitforTimeout: 60 * 1000,
};
```

`implicitTimeout: 0` is deliberate: UTAM waits on conditions, and an implicit wait on top of that
turns one slow element into a multi-minute run. Full files and the npm scripts:
[references/utam-project.md](references/utam-project.md).

## 3. Authenticate without a credential in the repo

Salesforce's own recipes get a login URL from the CLI and write it to `.env` - no password anywhere:

```js
const getUrlCmd = 'sf org open -p /lightning -r --json';   // -r is --url-only
const { url } = JSON.parse(stdout).result;                  // frontdoor URL, single use
```

Two rules that follow from what that URL is. `sf org open --url-only` prints "This command will
expose sensitive information that allows for subsequent activity using your current authenticated
session", and the URL is minted single-use through `/services/oauth2/singleaccess`:

- Regenerate it per run. A stored URL is both a credential and, after one navigation, useless.
- `.env` holding it is gitignored, and the value never goes into a log line or a CI artefact.

In CI, run against a scratch org created for the job and deleted with it - see
`sf-scratch-orgs-sandboxes` for the ephemeral-org script.

## 4. Page objects describe structure, specs describe behaviour

A page object is JSON: a root selector, elements typed by the page object that models them, and
composed methods for multi-step interactions.

```json
{
  "root": true,
  "selector": { "css": "body" },
  "elements": [
    { "name": "navigationBar", "type": "salesforce-pageobjects/global/pageObjects/appNav",
      "public": true, "selector": { "css": "one-appnav" } }
  ]
}
```

The spec then reads as navigation plus assertions, with waits expressed as conditions:

```js
await browser.navigateTo(testEnvironment.sfdxLoginUrl);
const domDocument = utam.getCurrentDocument();
await domDocument.waitFor(async () => (await domDocument.getUrl()).includes('Hello'));
const appHomePage = await utam.load(HomePage);
const item = await (await (await appHomePage.getNavigationBar()).getAppNavBar()).getNavItem('Wire');
await item.clickAndWaitForUrl('lightning/n/Wire');
```

No CSS selector for a Lightning internal ever appears in a spec. When Salesforce restyles the shell,
`salesforce-pageobjects` changes and your specs do not.

## 5. Agentforce agent tests

Agent behaviour is tested by definition, not by clicking: `AiEvaluationDefinition` metadata plus the
CLI.

| Command | Does |
| --- | --- |
| `sf agent generate test-spec` | Scaffold the test spec |
| `sf agent test create` | Create the test in the org from the spec |
| `sf agent test run` | Run it |
| `sf agent test resume` | Reattach to a run |
| `sf agent test results` | Fetch results |
| `sf agent test run-eval` | Run an evaluation |

Details of the metadata type live in `sf-agentforce-development`.

## Anti-patterns

| Anti-pattern | Why it hurts | Instead |
| --- | --- | --- |
| Raw CSS selectors for Lightning internals in a spec | Break on every Salesforce release, and shadow DOM makes them unreachable anyway | `salesforce-pageobjects` page objects, own `.utam.json` for own components |
| `browser.pause(5000)` | Passes on a fast org, fails in CI, hides the real condition | `waitFor` on a URL, a text, or a loaded page object |
| Username and password in `wdio.conf.js` or a CI secret used by the browser | A standing credential for a test run | `sf org open -p /lightning -r --json`, regenerated per run |
| Reusing one login URL across specs | Single-use; the second spec lands on a login screen | One URL per run, or per spec if the run logs out |
| A UI test for logic a Jest test can reach | Minutes of CI for a seconds-long assertion | Push the assertion down a tier |
| UI suite in the blocking pre-merge gate | An org outage becomes a merge outage | Nightly or on-demand; `vf-check local` stays offline |
| Asserting on a toast only | Lightning shows a saved-looking page before validation completes | Assert the persisted state, by query or by reload |
| `--disable-web-security` copied into a shared config | Masks real CORS and CSP failures | Keep the recipes' `--no-sandbox --disable-dev-shm-usage --disable-gpu` and nothing more |

## Verification

```bash
npm run build                 # utam -c utam.config.js, then compile the page objects
npx wdio run wdio.conf.js --spec force-app/test/<one>.spec.js
sf apex run test --target-org <alias> --test-level RunLocalTests --code-coverage --result-format human
node "$CLAUDE_PLUGIN_ROOT/scripts/checks/vf-check.mjs" jest --changed
sf agent test run --target-org <alias>        # when the project has agents
```

A UI suite is healthy when the same spec passes twice in a row on a cold org, and its failure output
names a condition that timed out rather than an element that vanished.

## References

- [references/utam-project.md](references/utam-project.md) - dependency table, the recipes' npm
  scripts verbatim, full `wdio.conf.js` and `utam.config.js`, page object grammar, CI layout.
- Sibling skills: `sf-lwc-jest-testing` (the tier below), `sf-apex-testing`,
  `sf-scratch-orgs-sandboxes` (ephemeral org for a run), `sf-agentforce-development`,
  `sf-setup-automation` (a browser for configuration, not for tests).
- UTAM recipes (source of every verbatim config here):
  <https://github.com/salesforce/utam-js-recipes>
- `salesforce-pageobjects` on npm: <https://www.npmjs.com/package/salesforce-pageobjects>
- `sf org open` flags and its security warning:
  <https://github.com/salesforcecli/plugin-org/blob/main/messages/open.md>
- `sf agent test *` commands: <https://github.com/salesforcecli/plugin-agent>
