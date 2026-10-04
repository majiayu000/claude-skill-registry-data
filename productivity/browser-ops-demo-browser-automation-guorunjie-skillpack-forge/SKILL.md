---
name: browser-ops-demo-browser-automation
description: Use when running browser automation workflows for browser-ops-demo.
---

# browser-ops-demo-browser-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Browser automation workflows for testing, scraping, and operator tasks.

## Workflow
- Identify the target URL, browser state, and expected user path
- Run the browser flow in a narrow, repeatable scenario
- Inspect visible page state before and after each important action
- Save failure evidence and rerun focused verification

## Commands
- install: `npm install`
- test: `npm test`
- doctor: `npm run doctor`

## Principles
- Prefer deterministic selectors and explicit waits
- Capture screenshots or traces when a browser flow fails
- Avoid storing secrets, cookies, or private page content in generated files
