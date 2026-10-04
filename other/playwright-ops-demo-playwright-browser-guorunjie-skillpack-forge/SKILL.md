---
name: playwright-ops-demo-playwright-browser
description: Use when running playwright browser workflows for playwright-ops-demo.
---

# playwright-ops-demo-playwright-browser

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Playwright browser automation workflows for reliable UI tests, inspections, and scripted operator tasks.

## Workflow
- Identify the target URL, browser project, viewport, and expected user journey
- Run the narrowest Playwright command first, such as npx playwright test path/to/spec --headed
- Inspect page state with screenshots or traces before changing selectors
- Update fixtures, waits, and assertions only after reproducing the failure
- Rerun the focused Playwright test and document any skipped browser coverage

## Commands
- install: `npm install`
- test: `npm test`
- e2e: `npm run e2e`

## Principles
- Use locators that reflect user-visible intent before falling back to brittle selectors
- Capture screenshots, traces, or console output when a browser run fails
- Keep browser state, credentials, and downloaded artifacts out of committed files
- Prefer small reproducible flows over broad end-to-end scripts
