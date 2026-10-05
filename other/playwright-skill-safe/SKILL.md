---
name: playwright-skill-safe
description: Secure and powerful Playwright browser automation for testing websites, checking deploys, taking screenshots, filling forms, validating login flows, responsive QA, deploy QA, accessibility smoke checks, and browser-based verification. Use when Nick asks to test a page, verify a deployment, automate browser interactions, capture screenshots, inspect console errors, check mobile/desktop rendering, or run real Chromium-based browser checks.
---

# Playwright Skill Safe

Use this skill to write and execute **task-specific Playwright scripts** safely.

## Requirements

- Playwright installed
- Chromium installed
- Write scripts only to `/tmp/playwright-test-*.js`

## Hard rules

- Always write scripts to `/tmp/playwright-test-*.js`
- Never write automation scripts into the skill folder or target project
- Always capture **console errors**, **page errors**, and **request failures**
- Always take a screenshot on failure
- Save trace artifacts on success/failure when possible
- Prefer `page.getByRole()`, `page.getByLabel()`, `page.getByPlaceholder()`, and `page.getByText()` over brittle selectors
- Use raw CSS selectors only as a last resort
- Default to **headless Chromium** unless visual debugging is useful
- Never auto-install packages at runtime

## Standard workflow

1. Determine the target URL and exact browser task
2. Choose the right pattern:
   - deploy QA
   - responsive QA
   - form flow
   - login flow
   - visual verification
   - broken request/API smoke
3. Write a purpose-built script to `/tmp/playwright-test-*.js`
4. Run it with:

```bash
node "$SKILL_DIR/scripts/run_playwright_task.js" /tmp/playwright-test-*.js
```

5. Report:
   - PASS / FAIL
   - what was tested
   - screenshots saved
   - traces saved
   - console errors
   - request failures
   - HTTP 4xx/5xx errors
   - accessibility warnings

## Built-in capabilities

- headed or headless mode via exported config
- viewport presets: desktop, laptop, tablet, mobile
- trace capture
- screenshot helpers
- network failure capture
- HTTP error capture
- accessibility smoke checks
- resilient locator helpers
- responsive sweep helper

## Script contract

Generated scripts should export:

```javascript
exports.config = {
  headed: false,
  slowMo: 0,
  // optional Playwright device name
  // device: 'iPhone 13'
};

exports.run = async ({ browser, context, page, result, helpers, chromium }) => {
  // your task here
  result.ok = true;
};
```

## Recommended patterns

### Deploy QA mode
- open URL
- wait for stable load
- capture title
- verify key heading or CTA
- take desktop screenshot
- run basic accessibility smoke

### Responsive QA mode
- run desktop/tablet/mobile sweep
- capture each screenshot
- note obvious layout issues

### Form flow mode
- use label/role/placeholder locators first
- fill realistic data
- submit
- verify success or validation state

### Login flow mode
- navigate to login
- fill credentials if provided
- submit
- verify redirect or authenticated UI

## Files

- Runner: `scripts/run_playwright_task.js`
- Helpers: `scripts/helpers.js`
- Reference examples: `references/examples.md`
- Task templates: `references/templates.md`

Resolve `$SKILL_DIR` to the directory containing this `SKILL.md` before running commands.
