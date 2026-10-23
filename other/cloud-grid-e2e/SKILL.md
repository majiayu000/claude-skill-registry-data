---
name: cloud-grid-e2e
description: "Author and run E2E tests on a cloud browser grid - BrowserStack Automate, Sauce Labs, or LambdaTest. All three follow one pattern: username + access-key env vars, a W3C WebDriver hub URL, a vendor options dict inside the capabilities (bstack:options / sauce:options / LT:Options), a local tunnel binary for internal apps, session pass/fail reporting, and a CI matrix throttled to the plan's parallel-session limit. Worked example uses BrowserStack; per-vendor deltas live in references/. Use for cross-browser regression on real devices + browsers beyond the engines bundled on the local machine - distinct from a local matrix runner and from self-hosted Selenium Grid."
---

# cloud-grid-e2e

## Overview

A cloud grid is a hosted farm of real devices + browsers exposed through a
W3C-compliant WebDriver endpoint. Point any WebDriver client (Selenium,
WebdriverIO, Nightwatch) at the vendor's hub URL and the suite runs on
combinations the local machine cannot host: real Safari on iOS, legacy
browser versions, niche Android devices.

The three major vendors are isomorphic - the same suite moves between them
by swapping four things:

| Concern | BrowserStack | Sauce Labs | LambdaTest |
|---|---|---|---|
| Auth env vars | `BROWSERSTACK_USERNAME` + `BROWSERSTACK_ACCESS_KEY` | `SAUCE_USERNAME` + `SAUCE_ACCESS_KEY` | `LT_USERNAME` + `LT_ACCESS_KEY` |
| Hub URL | `https://hub-cloud.browserstack.com/wd/hub` | regional, e.g. `https://ondemand.us-west-1.saucelabs.com:443/wd/hub` | `https://hub.lambdatest.com/wd/hub` |
| Vendor options dict | `bstack:options` | `sauce:options` | `LT:Options` |
| Local tunnel | BrowserStackLocal | Sauce Connect Proxy | LambdaTest Tunnel |

Everything else is standard W3C capabilities (`browserName`,
`browserVersion`, `platformName`) per [w3.org/TR/webdriver2/](https://www.w3.org/TR/webdriver2/).

Vendor deep detail (full options tables, tunnel setup, REST artifact
retrieval, CI matrix examples):
[references/browserstack.md](references/browserstack.md) ·
[references/sauce-labs.md](references/sauce-labs.md) ·
[references/lambdatest.md](references/lambdatest.md).

Composes with the sibling `browser-matrix-strategy-reference` for
matrix planning.

## When to use

- Cross-browser regression across more breadth than Playwright's bundled
  engines support (real Safari iOS, legacy versions, niche Android devices).
- Tier-1 browser matrix coverage backed by SLA.
- Internal / localhost applications testable from the cloud via the
  vendor's tunnel binary.

For **bundled-engine** matrix (Chromium / Firefox / WebKit on the runner
machine), use `playwright-testing` (references/browser-matrix.md). For a
self-hosted grid (data residency, cost control), use the sibling
`selenium-grid-4-runner`.

Choosing between the vendors: BrowserStack has the broadest real-device
matrix and enterprise procurement; Sauce Labs suits Selenium-grid-centric
parallel CI farms; LambdaTest is the cost-sensitive smaller-scale option.
Full deltas in the per-vendor references.

## How to use (the vendor-generic pattern)

1. Export the vendor's username + access-key env vars from account settings.
2. Point the WebDriver client at the vendor's hub URL.
3. Build W3C capabilities and set the vendor options dict (`bstack:options`
   / `sauce:options` / `LT:Options`) on the Options object **before**
   creating the driver - set at minimum a project/build/session name triple
   so the dashboard groups sessions.
4. Run the suite; report each session's pass / fail back to the vendor
   before `driver.quit()`, so dashboard metrics stay accurate.
5. For localhost / internal targets, start the vendor's tunnel binary and
   flag the session as tunneled.
6. In CI, run the browser matrix as jobs throttled to the plan's
   parallel-session limit.

## Worked example (BrowserStack)

Run one Selenium suite on the grid end to end - build capabilities, create
the remote driver, drive the test, report status, quit. Per
[browserstack.com/docs/automate/selenium](https://www.browserstack.com/docs/automate/selenium):

```python
import os
from selenium import webdriver

options = webdriver.SafariOptions()
options.browser_version = "17"

bstack_options = {
    "os": "OS X",
    "osVersion": "Sonoma",
    "projectName": "my-app",
    "buildName": os.environ.get("BUILD_TAG", "local-run"),
    "sessionName": "Checkout flow on Safari macOS",
    "local": "false",
}

# Vendor caps must be set on Options BEFORE Remote(); driver.capabilities is a
# read-only result dict, so assigning to it afterwards is a no-op ([Selenium options]).
options.set_capability("bstack:options", bstack_options)

driver = webdriver.Remote(
    command_executor=(
        f"https://{os.environ['BROWSERSTACK_USERNAME']}:"
        f"{os.environ['BROWSERSTACK_ACCESS_KEY']}"
        f"@hub-cloud.browserstack.com/wd/hub"
    ),
    options=options,
)

driver.get("https://example.com")
# ... test ...

# mark the session pass / fail so the dashboard metrics are accurate
driver.execute_script(
    'browserstack_executor: {"action": "setSessionStatus", '
    '"arguments": {"status":"passed","reason":"Login redirected as expected"}}'
)
driver.quit()
```

Every non-W3C capability - `os`, `osVersion`, `projectName`, `buildName`,
`sessionName`, `local` - lives inside `bstack:options`; only the standard
fields (`browserName`, `browserVersion`, `platformName`) sit at the top
level ([Selenium options]). Use `"status":"failed","reason":"..."` on
failure.

The same shape on the other vendors: Sauce Labs reports status via
`driver.execute_script("sauce:job-result=passed")` and LambdaTest via
`driver.execute_script("lambda-status=passed")` - see the references.

## Local tunnel (internal / localhost apps)

Each vendor ships a tunnel binary that lets grid sessions reach hosts on
your network. BrowserStack example:

```bash
# Download the BrowserStackLocal binary from browserstack.com
./BrowserStackLocal --key "$BROWSERSTACK_ACCESS_KEY" --daemon start
# Sessions with bstack:options.local = "true" now tunnel
./BrowserStackLocal --key "$BROWSERSTACK_ACCESS_KEY" --daemon stop
```

Sauce Connect (`./sc --tunnel-name ...` + `sauce:options.tunnelName`) and
LambdaTest Tunnel (`./LT --tunnelName ...` + `LT:Options.tunnel: true`) are
in the references. For ephemeral CI: spawn → wait-for-ready with a bounded
timeout → run tests → terminate.

## CI wiring and parallel limits

Run the browser matrix as CI jobs, one combination per job, with the
credentials in secrets and `buildName`/`build` set to the PR identifier:

```yaml
on: pull_request
jobs:
  grid:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser:
          - { name: Chrome, version: latest, os: Windows, osVersion: "11" }
          - { name: Safari, version: "17", os: "OS X", osVersion: Sonoma }
    steps:
      - uses: actions/checkout@v5
      - name: Run cross-browser tests
        env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
          BUILD_TAG: pr-${{ github.event.pull_request.number }}
        run: pytest tests/e2e/ --bstack
```

All three vendors cap concurrent sessions by plan tier; queue overflow
blocks subsequent sessions until earlier ones complete. Throttle the worker
pool (`ThreadPoolExecutor(max_workers=N)` or the CI matrix `max-parallel`
key) to the plan limit, and tier the matrix per
`browser-matrix-strategy-reference` so full runs stay inside it.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Credentials in code | Token leak | Env vars / secret store |
| All tests on every browser combo | Slow + expensive (plan-limited) | Tier the matrix - see `browser-matrix-strategy-reference` |
| Missing build/project name caps | Sessions un-grouped in dashboard | Always set build to the CI run / PR identifier |
| No session-status update | Dashboard pass/fail rate inaccurate | Always report status before quit |
| Tunnel binary not stopped | Stale tunnels accumulate | Always stop the daemon after the run |
| Parallel exceeds plan limit | Sessions queue + timeout | Match worker pool to plan |
| Polling for tunnel-ready without timeout | Suite hangs if the tunnel never connects | Bounded wait + fail |
| Hardcoded vendor URL in tests | Switching grids requires code changes | Env-var-driven hub URL + a small caps abstraction |
| Treating vendors as drop-in interchangeable | Options dicts differ (`bstack:options` vs `sauce:options` vs `LT:Options`) | Isolate vendor caps in one harness module |

## Limitations

- **Cost.** Plan tiers limit parallel sessions; full-matrix runs on every
  PR are expensive - tier the matrix.
- **Setup latency.** Real-device sessions take 5-30s to start; not optimal
  for short feedback loops.
- **Network shape.** Cloud-grid latency is higher than local; some
  timing-sensitive tests behave differently.
- **Device matrices churn.** Vendors add + retire devices; tests pinned to
  specific versions need periodic updates.
- **Internal networks require the tunnel.** Adds setup + tunnel-stability
  concerns.
- **Cypress does not speak WebDriver.** Cloud grids run Cypress via
  vendor-specific runners (or Cypress Cloud), not the hub URL pattern here.

## References

- BrowserStack Automate Selenium docs -
  [browserstack.com/docs/automate/selenium](https://www.browserstack.com/docs/automate/selenium).
- Sauce Labs test config options -
  [docs.saucelabs.com/dev/test-configuration-options](https://docs.saucelabs.com/dev/test-configuration-options/).
- LambdaTest automated web testing -
  [lambdatest.com/support/docs/getting-started-with-lambdatest-automation](https://www.lambdatest.com/support/docs/getting-started-with-lambdatest-automation/).
- W3C WebDriver specification -
  [w3.org/TR/webdriver2/](https://www.w3.org/TR/webdriver2/).
- [Selenium options] - Selenium 4 browser-options classes;
  `set_capability` for vendor-prefixed caps before driver creation.
- Vendor deltas:
  [references/browserstack.md](references/browserstack.md),
  [references/sauce-labs.md](references/sauce-labs.md),
  [references/lambdatest.md](references/lambdatest.md).
- Composes: `browser-matrix-strategy-reference`.
- Sibling: `selenium-grid-4-runner` (self-hosted alternative).

[Selenium options]: https://www.selenium.dev/documentation/webdriver/drivers/options/
