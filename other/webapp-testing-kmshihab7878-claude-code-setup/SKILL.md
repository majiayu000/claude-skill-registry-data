---
name: webapp-testing
description: >
  Toolkit for interacting with and testing local web applications using Playwright. Supports verifying
  frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
  Includes browser automation safety rules: rate limiting, robots.txt compliance, session handling, and PII protection.
risk: medium
tags: [testing, browser]
created: 2026-03-07
updated: 2026-03-17
---

# Web Application Testing

Playwright-based web application testing toolkit with built-in browser automation safety rules.

## How to use

- `/webapp-testing`
  Apply testing patterns and safety rules to browser automation in this conversation.

- `/webapp-testing <script>`
  Review the script against testing best practices and safety rules below.

## When to use

Reference these guidelines when:
- testing local web applications with Playwright
- verifying frontend functionality or debugging UI behavior
- capturing browser screenshots or viewing browser logs
- building web scrapers or data extractors
- automating browser interactions (Playwright, Puppeteer, Selenium)
- fetching content from external websites
- handling extracted data that may contain PII

## When NOT to use

Do NOT apply this skill when:
- the task is about unit testing (use `testing-methodology` skill)
- the task is about API testing without a browser (use `testing-methodology` skill)
- the task is about UI component design (use `baseline-ui` or `frontend-design` skill)

---

## Prefer expect-cli for Adversarial Browser Testing

For validating browser-facing code changes, prefer `expect-cli` over raw Playwright scripts:

```bash
EXPECT_BASE_URL=http://localhost:3000 expect-cli -m "describe what to test adversarially" -y
```

`expect-cli` (from `millionco/expect`) scans your git diff, generates an adversarial test plan, and executes it in a real browser with session recordings. Use it after any frontend change. See the `expect` skill for full documentation.

Fall back to raw Playwright scripts (below) when you need fine-grained control, custom fixtures, or integration with existing test suites.

## Testing Toolkit

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary.

### Decision Tree

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

### Server Management

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

### Automation Script Pattern
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always headless
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS
    # ... your automation logic
    browser.close()
```

### Reconnaissance-Then-Action
1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```
2. **Identify selectors** from inspection results
3. **Execute actions** using discovered selectors

### Common Pitfall
- **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
- **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

### Best Practices
- Use bundled scripts as black boxes — `--help` first, invoke directly
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

### Reference Files
- **examples/element_discovery.py** - Discovering buttons, links, inputs
- **examples/static_html_automation.py** - Using file:// URLs for local HTML
- **examples/console_logging.py** - Capturing console logs

---

## Browser Automation Safety

Rules for safe, ethical browser automation and web data extraction.

### Priority Levels

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Legal and ethical | Critical |
| 2 | Rate limiting | Critical |
| 3 | Session safety | High |
| 4 | Data handling | High |
| 5 | Error resilience | Medium |

### 1. Legal and Ethical (Critical)

- MUST check and respect `robots.txt` before scraping
- MUST respect `Crawl-delay` directives
- MUST check Terms of Service for scraping restrictions
- NEVER scrape login-protected content without authorization
- NEVER circumvent anti-bot measures on sites that prohibit scraping
- MUST set a descriptive User-Agent string identifying your bot
- SHOULD provide a contact email in User-Agent or on a linked page

### 2. Rate Limiting (Critical)

- MUST use minimum 1-second delay between requests to the same domain
- MUST respect `Retry-After` headers; implement exponential backoff
- MUST use concurrent request limits (max 2-3 per domain)
- SHOULD monitor response times; slow down if server is struggling (5xx responses)
- MUST implement circuit breaker: stop after N consecutive failures
- SHOULD use caching to avoid re-fetching unchanged content

### 3. Session Safety (High)

- NEVER store or log authentication cookies from external sites
- MUST clear sessions after use; do not persist browser state unnecessarily
- SHOULD use incognito/private browser contexts for isolation
- MUST rotate proxies only when authorized and necessary
- MUST handle CAPTCHAs gracefully (stop, don't bypass)
- MUST implement timeouts for all network operations

### 4. Data Handling (High)

- MUST identify and redact PII (emails, phone numbers, addresses) before storage
- NEVER store scraped data longer than necessary
- SHOULD log what was accessed but not the full content (for audit)
- MUST sanitize extracted content before processing (prevent injection)
- MUST respect copyright; do not redistribute copyrighted content
- SHOULD store data with access controls; encrypt at rest if sensitive

### 5. Error Resilience (Medium)

- MUST handle network errors, timeouts, and partial page loads gracefully
- MUST implement retry with exponential backoff (max 3 retries)
- SHOULD validate extracted data shape before processing
- SHOULD log errors with context for debugging
- SHOULD use health checks to verify automation is working correctly
- SHOULD set up monitoring for long-running automation tasks

## Cross-references

- **testing-methodology** skill: Test strategy, unit/integration testing
- **baseline-ui** skill: UI constraints, responsive design patterns
- **security-review** skill: Security audit patterns
- **SECURITY_PLAYBOOK.md**: Broader security rules
