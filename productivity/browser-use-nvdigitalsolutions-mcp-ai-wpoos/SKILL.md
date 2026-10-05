---
type: Skill
name: browser-use
description: Control a headless browser to navigate URLs, click elements, fill forms, extract content from JavaScript-rendered pages, take screenshots, and automate end-to-end web workflows.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Browser Use

Interact with live web pages using browser automation. Use this skill when you need to:

- Navigate to URLs and interact with dynamic web content
- Fill out forms, click buttons, and follow links programmatically
- Scrape content from JavaScript-rendered pages (SPAs, dashboards)
- Run end-to-end UI tests against local or staging environments
- Research live web pages and synthesize their content
- Take screenshots for visual verification or debugging

## Prerequisites

Install the `browser-use` Python package and Playwright:

```bash
pip install browser-use playwright
playwright install chromium
```

Or use the browser-use CLI skill:

```bash
npx skills add browser-use/claude-skill
```

## Core Patterns

### Navigate and extract

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    page.wait_for_load_state('networkidle')  # Wait for JS
    content = page.content()
    browser.close()
```

### Click and interact

```python
page.locator('button[type="submit"]').click()
page.fill('input[name="email"]', 'user@example.com')
page.select_option('select#country', 'US')
```

### Screenshot for verification

```python
page.screenshot(path='/tmp/screenshot.png', full_page=True)
```

### Handle authentication

```python
page.goto('https://app.example.com/login')
page.fill('#email', 'user@example.com')
page.fill('#password', 'secret')
page.locator('button[type="submit"]').click()
page.wait_for_url('**/dashboard')
```

## Decision Tree

```
Task requires web interaction?
    ├─ Static HTML → Read file directly; skip browser
    └─ Dynamic webapp / live URL
        ├─ Server not running → Start server first
        └─ Server running →
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## End-to-End Test Workflow

```
User: "Verify the signup flow on staging works end-to-end"

Steps:
1. Open https://staging.yourapp.com/signup
2. Fill in test credentials
3. Click "Create account"
4. Wait for redirect to dashboard
5. Screenshot the result
6. Report: success or describe any failures found
```

## Security Rules

- **Never** submit real credentials or payment details in automated tests
- Use test accounts and sandbox environments only
- Confirm with the user before automating any write/purchase action
- Prefer `--dry-run` or review steps when destructive actions are involved

## Common Pitfalls

- ❌ Don't inspect DOM before `wait_for_load_state('networkidle')` on SPAs
- ✅ Always wait for JavaScript to finish before reading dynamic content
- ❌ Don't hardcode selectors that change between deploys
- ✅ Use stable selectors: `text=`, `role=`, data attributes, or IDs

## Tips

- Use `page.pause()` during development to inspect the live browser state
- Use `page.locator('.selector').all()` to discover all matching elements
- Chain `page.wait_for_selector()` before interacting with async-rendered elements
- For multi-page flows, keep one browser context open throughout the session
