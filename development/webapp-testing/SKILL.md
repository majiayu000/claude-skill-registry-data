---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Use when you need to verify a frontend change actually renders/behaves correctly (not just that the code compiles), when debugging a flaky or unknown selector, when a bug report needs reproduction against a running dev server, when you need to inspect what buttons/links/inputs actually exist on a rendered page, or when capturing a screenshot/console log is the fastest way to confirm UI behavior.
source: ~/.agents/skills@2026-07-13
license: Complete terms in LICENSE.txt
---


# Web Application Testing

> **Auth flows:** See the `playwright-auth` skill for login flow contracts, storage state
> persistence, POM vs fixture patterns, and multi-role auth.

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

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

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## NEVER

- **NEVER inspect the DOM before `page.wait_for_load_state('networkidle')` on a dynamic app** —
  client-rendered content isn't there yet; selectors resolved pre-render silently miss elements
  that appear a beat later, and the script "works" against a half-loaded page.
- **NEVER read a bundled script's source before running it with `--help`** — `with_server.py` and
  its siblings are designed to be called as black boxes. Reading the source first burns context
  on server-lifecycle internals you don't need and won't reuse; only fall back to reading source
  after `--help` proves the script genuinely can't do what the task needs.
- **NEVER launch a headed browser for scripted automation** — always `headless=True`. Headed mode
  is for interactive human debugging only; leaving it on silently breaks on a headless CI/sandbox
  box with no display.
- **NEVER let a script exit without `browser.close()` on every path** — an uncaught exception
  before close() leaks the Chromium process. Once a script does more than a single glance-and-exit,
  wrap the automation body in `try/finally` (or a context manager), not a bare linear script.
- **NEVER hand-roll a `sleep(N)` before `page.goto()` to wait for a dev server to come up** —
  `scripts/with_server.py` already solves server-readiness polling; a fixed sleep is a bet on how
  fast the box happens to be that day and fails first under load.
- **NEVER default to `page.wait_for_timeout()` as the wait strategy** — it's a last resort for
  genuinely non-deterministic timing (an animation, a debounce), not a substitute for
  `wait_for_load_state()` / `wait_for_selector()` / waiting on a specific response. A fixed
  timeout that passes locally becomes a flaky coin-flip the moment the machine is under load.
- **NEVER trust selectors read from a dynamic app's initial/static markup** — client-rendered
  content can diverge from what's in the raw HTML. Resolve selectors from the rendered DOM
  (post-`networkidle` screenshot or `page.content()`), never from a source read alone.

## Reference Files

- **examples/** - Examples showing common patterns. Each is a scenario-gated trigger, not a
  bare-filename menu — open the specific file when its scenario matches, skip the rest:
  - `element_discovery.py` - **MANDATORY: read this when you don't yet know the selectors for a
    rendered page** — before writing actions against buttons/links/inputs you haven't inspected,
    or when a prior selector guess came back empty/wrong. Shows how to enumerate all buttons,
    links, and input fields on a live page so you pick selectors from what's actually rendered
    instead of guessing from source.
  - `static_html_automation.py` - **MANDATORY: read this when the target is a static HTML file
    with no dev server** — i.e. the Decision Tree above routed you to "static HTML" branch. Shows
    `file://` URL construction and the fixed 1920x1080 viewport convention for deterministic
    screenshots of local files.
  - `console_logging.py` - **MANDATORY: read this when debugging a runtime JS error, an unexpected
    client-side warning, or any bug report that says "check the console"** — not for routine
    automation runs. Shows the `page.on("console", ...)` handler pattern for capturing and
    persisting console output during a scripted interaction.