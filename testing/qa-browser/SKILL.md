---
name: qa-browser
description: Autonomous browser testing with playwright-cli (token-efficient CLI) and Playwright MCP. Use for E2E tests, browser automation, UI testing, visual regression, screenshot capture, and web flows.
triggers:
  - browser testing
  - playwright
  - e2e test
  - ui test
  - browser automation
  - web flow
---

## Role

Browser automation specialist using playwright-cli as the default tool for E2E flows and CI pipelines. Switch to Playwright MCP for exploratory or long-running sessions that need persistent state and deep introspection. CLI is token-efficient; MCP is context-rich.

## Instructions

### When to use this skill vs others

- Use qa-browser for any flow that requires a real browser: form submission, navigation, session management, UI-level assertions.
- Delegate to qa-visual when the primary goal is pixel-diff comparison or accessibility auditing.
- Delegate to qa-api when the flow only involves HTTP requests without browser-rendered UI.

### Response format

Provide a complete sequence of playwright-cli commands as the primary artifact. Include session management (`--session=name`) for multi-step flows. Always end with a screenshot for verification. Provide the npx playwright test command when generating spec files.

### Edge cases

New project: run `playwright-cli codegen` to record the flow interactively, then refine the generated spec.

CI integration: enforce `headless: true` in config, use `--shard=N/M` for parallel execution, store auth state in `./test-output/auth.json`.

Broken selectors: use `npx playwright agent healer tests/failing.spec.ts` — the healer agent patches selectors automatically.

Cross-platform concerns: `playwright-cli` runs on chromium by default; add `--browser=firefox` or `--browser=webkit` for cross-browser coverage.

## Examples

### Example 1

**Input**: Test the login flow — user enters credentials and lands on the dashboard

**Output**:

```bash
playwright-cli --session=e2e open https://app.example.com/login
playwright-cli --session=e2e type "input[name='email']" "qa@test.com"
playwright-cli --session=e2e type "input[name='password']" "secret"
playwright-cli --session=e2e click "button[type='submit']"
playwright-cli --session=e2e assert-visible "text=Dashboard"
playwright-cli --session=e2e assert-url "**/dashboard"
playwright-cli --session=e2e screenshot --full-page
playwright-cli --session=e2e save-storage ./test-output/auth.json
```

### Example 2

**Input**: Generate a Playwright spec for the checkout flow

**Output**:

```bash
# Record interactively
playwright-cli codegen --output tests/checkout.spec.ts https://app.example.com/products

# Or: use the Playwright agent planner
npx playwright agent planner "Test the checkout flow including cart, address, payment, and confirmation"
# → produces specs/checkout-plan.md

npx playwright agent generator specs/checkout-plan.md
# → produces tests/checkout.spec.ts

# Run with HTML report
npx playwright test tests/checkout.spec.ts --reporter=html
```

## Install

```bash
npm install -g @playwright/playwright-cli
npx playwright install chromium
playwright-cli --version
```

## Config (`playwright-cli.json`)

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": { "headless": true }
  },
  "timeouts": {
    "action": 5000,
    "navigation": 30000
  },
  "outputDir": "./test-output"
}
```

## Core Commands

```bash
playwright-cli open https://app.example.com
playwright-cli open https://app.example.com --headed

playwright-cli click "button[data-testid='submit']"
playwright-cli click "text=Submit Order"
playwright-cli type "input[name='email']" "user@test.com"
playwright-cli press Enter
playwright-cli select "select#country" "US"
playwright-cli check "input[type='checkbox']"

playwright-cli assert-visible "text=Welcome back"
playwright-cli assert-url "https://app.example.com/dashboard"
playwright-cli assert-text "h1" "Dashboard"
playwright-cli assert-count ".product-card" 12

playwright-cli screenshot
playwright-cli screenshot --full-page
playwright-cli screenshot --clip 0,0,800,600

playwright-cli --session=myapp open https://app.example.com
playwright-cli --session=myapp type "input" "value"
playwright-cli session-list
playwright-cli session-delete myapp

playwright-cli mock-route "*/api/users" --body '{"users":[]}'
playwright-cli wait-for-response "*/api/data"

playwright-cli save-storage ./auth.json
playwright-cli load-storage ./auth.json

playwright-cli codegen https://app.example.com
playwright-cli codegen --output tests/login.spec.ts https://app.example.com

playwright-cli trace start
playwright-cli trace stop --output trace.zip
npx playwright show-trace trace.zip
```

## Agent Patterns

### Discovery

```bash
playwright-cli open https://app.example.com
playwright-cli snapshot
npx playwright agent planner "Explore the checkout flow and list all test scenarios"
npx playwright agent generator specs/checkout-plan.md
```

### Execution (CI)

```bash
npx playwright test --reporter=json > results.json
npx playwright test --shard=1/3
npx playwright test --shard=2/3
npx playwright test --shard=3/3
```

### Healing broken selectors

```bash
npx playwright agent healer tests/checkout.spec.ts
```

## MCP Alternative

For exploratory or long-running workflows:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless"]
    }
  }
}
```

```bash
PLAYWRIGHT_MCP_SNAPSHOT_MODE=incremental
PLAYWRIGHT_MCP_TIMEOUT_ACTION=5000
PLAYWRIGHT_MCP_TIMEOUT_NAVIGATION=60000
```

## Playwright Agents (v1.56+)

```bash
npx playwright agent planner "Test the user registration flow including validation"
npx playwright agent generator specs/registration-plan.md
npx playwright agent healer tests/registration.spec.ts
```

## Anti-Patterns

- Use `wait-for-response` or `assert-visible` not hardcoded `sleep()`
- Always `headless: true` in CI
- Use isolated sessions per test suite, not one global session
- Prefer `text=`, `role=`, or `data-testid=` selectors over fragile CSS
- Avoid `snapshot` in loops — it dumps the full DOM tree and burns tokens
