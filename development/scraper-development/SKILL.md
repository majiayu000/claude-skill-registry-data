---
name: scraper-development
description: Use when building a new scraper provider for the finance-analysis project — guides interactive browser exploration of financial sites via Playwright MCP and generates BrowserScraper/ApiScraper provider code. Triggers on "new scraper", "scrape provider", "add provider", "explore site for scraping".
---

# Scraper Development

Build new scraper providers by exploring live financial websites (read-only) via Playwright MCP, then generating provider code for the existing framework.

## Two Phases

**Phase 1 — Explore:** Control a browser to understand the site's structure, API calls, and data formats.
**Phase 2 — Generate:** Write a `BrowserScraper` or `ApiScraper` subclass using discovered information.

---

## Phase 1: Exploration

### Setup

1. Ask the user for: **provider name**, **site URL**, **what data they need** (transactions, balances, loans, etc.)
2. Navigate to the login page via `browser_navigate`
3. Take a snapshot and tell the user: **"Please log in manually. I will not touch your credentials. Let me know when you're logged in."**
4. Wait for user confirmation before proceeding

### Exploration Loop

Once logged in:
1. Take `browser_snapshot` to understand current page
2. Check `browser_network_requests` to discover API calls the site makes
3. Use `browser_evaluate` to inspect JS variables, tokens, or embedded data
4. Navigate to pages where the target data lives (using SAFE actions only — see Safety Rules below)
5. Document everything: selectors, API endpoints, request/response formats, auth headers, pagination patterns

### Exploration Report

Before moving to Phase 2, present a summary:
- Pages visited and their purpose
- API endpoints discovered (with request/response shapes)
- Authentication mechanism (cookies, tokens, headers)
- Data structure of the target information
- Recommended approach: `BrowserScraper` (page automation) vs `ApiScraper` (direct HTTP)
- Any gaps or unknowns

Get user approval before proceeding to code generation.

---

## SAFETY RULES — READ-ONLY EXPLORATION

<CRITICAL>
You are exploring a LIVE financial account with REAL money. A wrong click could trigger a transfer, close an account, or change settings irreversibly. These rules are non-negotiable.
</CRITICAL>

### NEVER DO (Absolute Prohibitions)

- **Never type or fill credentials** — the user logs in manually, you wait
- **Never fill ANY form field** during exploration — including search boxes. Describe what you want to search and ask the user to type it, or ask permission first
- **Never click action buttons.** Prohibited labels (in ANY language, including Hebrew): delete, remove, cancel, close, transfer, send, pay, approve, confirm, submit, update, save, apply, activate, deactivate, disable, enable, change, modify, edit, reset, unsubscribe, opt-out, upgrade, downgrade, and synonyms thereof
- **Never navigate to settings, preferences, profile, or security pages** — not even to look. These pages often have toggle switches that activate on click
- **Never click "agree", "accept", or "consent"** on any dialog — ask the user
- **Never download executables** (.exe, .msi, .dmg, .pkg, .sh, .bat)
- **Never dismiss or accept unexpected dialogs** — describe them to the user and ask what to do

### ALLOWED (Safe Actions)

- Click navigation links: menu items, sidebar links, tabs, breadcrumbs, pagination arrows/numbers
- Click "view", "show", "details", "expand", "collapse" elements
- Click date range pickers to change the data viewing window
- `browser_snapshot` — always safe
- `browser_network_requests` — always safe
- `browser_evaluate` with read-only JS (no DOM mutations, no fetch/XHR calls)
- `browser_navigate_back` — always safe
- `browser_take_screenshot` — always safe

### ASK FIRST (Uncertain Actions)

If you're not 100% certain an action is safe, **you MUST ask the user before clicking.** Specifically:

- Any button or link not clearly in the NEVER or ALLOWED lists
- Any pop-up, modal, or overlay — describe it and ask
- Any navigation that would leave the current domain
- Download buttons (PDF, CSV, Excel) — these may trigger email notifications or audit logs
- "Export" or "report" buttons — same concern
- Search or filter inputs — describe what you want to type and get approval
- Anything in Hebrew you cannot confidently translate — show the user a screenshot

### RECOVERY (If Something Goes Wrong)

- **Landed on a settings page?** → `browser_navigate_back` immediately, tell the user
- **Unexpected confirmation dialog?** → `browser_handle_dialog` with `accept: false`, tell the user
- **"Are you sure?" prompt?** → Always decline, tell the user
- **Triggered a POST/PUT/DELETE request?** → Stop immediately, alert the user, show the network request details
- **Session expired?** → Stop exploring, ask the user to re-login

### ADDITIONAL SAFETY PROTOCOLS

- **Domain lock:** After login, note the domain. Any click leading to a different domain requires explicit user approval.
- **Network audit:** After ANY click that wasn't pure navigation, immediately run `browser_network_requests` and check for POST/PUT/DELETE/PATCH requests. If you see one that you didn't expect, alert the user immediately.
- **Periodic checkpoints:** Every 5-10 browser interactions, pause and summarize what you've done and found. Ask the user if they want to continue.
- **Screenshot before uncertain clicks:** Before any ASK FIRST action, take a `browser_take_screenshot` so the user can see exactly what you're about to interact with.
- **Hebrew button awareness:** Financial sites in Israel use Hebrew. You MUST interpret Hebrew labels before clicking. If you cannot confidently read a Hebrew label, screenshot it and ask the user. Common dangerous Hebrew words: שלח (send), אשר (approve/confirm), מחק (delete), בטל (cancel), עדכן (update), שמור (save), העבר (transfer).
- **No JavaScript mutations:** When using `browser_evaluate`, only read data. Never use it to call APIs, submit forms, modify the DOM, or trigger events. Allowed: reading `window.*` variables, `document.querySelector().textContent`, `JSON.parse()`. Forbidden: `fetch()`, `XMLHttpRequest`, `.click()`, `.submit()`, `document.createElement()`, any DOM modification.

---

## Exploration Techniques for SPAs

### sessionStorage / localStorage Mining

Many Israeli financial sites are Angular/React SPAs that cache all API responses in browser storage. This is often **easier and more reliable** than parsing DOM or intercepting network requests.

**How to check:**
```javascript
// During exploration, run via browser_evaluate:
Object.keys(JSON.parse(sessionStorage.getItem('appState') || '{}'))
// Or check all keys:
Object.keys(sessionStorage)
Object.keys(localStorage)
```

**Why this is valuable:**
- Data is pre-structured JSON — no DOM parsing needed
- All API responses are cached, even from pages you haven't visited yet
- Data persists as you navigate between pages within the SPA
- **Caveat:** Detail pages for individual accounts may **overwrite** the same sessionStorage key when you navigate between accounts — extract data before navigating to the next account

### Navigation Timing for SPAs

- Use `wait_until="domcontentloaded"` instead of `networkidle` for Angular/React SPAs — persistent WebSocket/polling connections prevent `networkidle` from ever firing
- After navigation, use `page.wait_for_function()` to wait for specific sessionStorage keys to populate rather than waiting for DOM elements
- The default `load` event is often too slow for SPAs as well

---

## Anti-Bot Detection

### Human-Like Behavior (Required for Most Sites)

Many Israeli financial sites detect bot behavior and block login. The `BrowserScraper` base class provides shared methods — **always use them during login flows:**

- `self._human_delay(min_sec, max_sec)` — random sleep between interactions
- `self._type_like_human(selector, text)` — character-by-character typing with random delays (50-150ms per char)
- `self._human_mouse_move()` — random mouse movement to simulate human presence
- `self._human_scroll()` — random scroll to simulate reading

**Login flow pattern:**
1. Navigate with `domcontentloaded`
2. Mouse move + scroll before interacting (looks like a human scanning the page)
3. Click field, delay, type like human
4. Delay between fields
5. Wait for submit button to become enabled, then submit

### Common Login Pitfalls

- **Timeout budget exhaustion:** If you use `networkidle` for navigation, it may consume 15+ seconds of a 30-second timeout, leaving insufficient time for subsequent element waits. Always use `domcontentloaded` + explicit element waits.
- **Button enabling:** Many sites disable the submit button until all fields are valid. Wait for `aria-disabled` to change or check for `:not([disabled])` state.
- **OTP redirects:** 2FA flows often redirect to a different subdomain (e.g., `login.fnx.co.il`). Wait for URL changes and new selectors.

---

## Phase 2: Code Generation

### Preparation

Before writing code, read these reference files:
- `scraper/base/browser_scraper.py` or `scraper/base/api_scraper.py` (whichever applies)
- `scraper/base/base_scraper.py` (lifecycle and models)
- `scraper/models/credentials.py` (ProviderConfig pattern)
- `scraper/models/transaction.py` (Transaction dataclass)
- `scraper/models/account.py` (AccountResult dataclass — supports optional `metadata` dict)
- 2 existing providers similar to the target (e.g., `hapoalim.py` for BrowserScraper, `onezero.py` for ApiScraper, `hafenix.py` for insurance/SPA scraping)
- `scraper/__init__.py` (factory registration)

### Code to Generate

1. **Provider class** in `scraper/providers/banks/<name>.py`, `scraper/providers/credit_cards/<name>.py`, or `scraper/providers/insurances/<name>.py`:
   - Subclass `BrowserScraper` or `ApiScraper`
   - Implement `login()` (or `get_login_options()` for BrowserScraper) and `fetch_data()`
   - Return `list[AccountResult]` with properly constructed `Transaction` objects
   - For insurance scrapers: populate `AccountResult.metadata` dict with per-account metadata (investment tracks, commissions, etc.) — the backend adapter persists this to the `insurance_accounts` table
   - Follow the exact patterns from reference providers

2. **Register the provider:**
   - Add `ProviderConfig` entry to `PROVIDER_CONFIGS` in `scraper/models/credentials.py`
   - Add factory entry in `scraper/__init__.py`
   - Add export in `scraper/providers/banks/__init__.py`, `credit_cards/__init__.py`, or `insurances/__init__.py`

3. **Test stub** in `tests/backend/unit/test_scraper/` following existing test patterns

### Multi-Account Providers

For providers with multiple internal accounts (e.g., pension + keren hishtalmut under one login):

1. **Discover accounts** from a summary/overview page first
2. **Navigate account-by-account** to each detail page sequentially
3. **Extract before moving on** — SPA storage keys often get overwritten when navigating to the next account
4. Return one `AccountResult` per internal account, each with its own transactions and metadata

### Code Quality

- Type hints on all methods
- NumPy-style docstrings
- Transaction amounts: negative = expense, positive = income (match framework convention)
- Handle pagination if the site paginates results
- Handle date range filtering (scraper receives start/end dates via `ScraperOptions`)
- Proper error handling using `ScrapingResult` error types
- Use human-like behavior methods from `BrowserScraper` base class during login flows
