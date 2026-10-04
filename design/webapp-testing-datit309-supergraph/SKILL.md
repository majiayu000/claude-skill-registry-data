---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
mcp: codebase-memory-mcp
---

# /supergraph:webapp-testing

Test and verify local web application UI behavior using Playwright.

Announce: "🌐 /supergraph:webapp-testing — testing web application..."

## When to Use

- Verifying a frontend change works correctly in the browser
- Debugging UI behavior or unexpected rendering
- Capturing screenshots for visual verification
- Checking browser console logs for errors
- After `/supergraph:frontend-design` to confirm feature works end-to-end

## Steps

### 0. Announce
"🌐 /supergraph:webapp-testing — testing [feature/page]..."

### 1. Understand what changed (graph context)

Before writing tests, use graph context to prioritize coverage:
Use `CBM_PROJECT`: call `detect_changes`, `search_graph` for changed routes/pages,
then `trace_path` for inbound/outbound call and data-flow paths. Run validated
`test-gaps`. Empty results are unavailable; use Serena/filesystem evidence.

**Serena (optional):** For changed component symbols:
```
mcp__serena__find_referencing_symbols(symbol=<changed_component>)
```
If a Playwright test fails on a renamed component/route, `find_referencing_symbols` surfaces all import sites. Skip if Serena unavailable.

### 2. Choose approach

```
Is it static HTML?
├─ Yes → Read HTML file directly to identify selectors
│         Then write Playwright script using those selectors
│
└─ No (dynamic webapp) → Is server already running?
    ├─ No → Run: python scripts/with_server.py --help
    │        Then start server + write Playwright script
    │
    └─ Yes → Reconnaissance-then-action:
        1. Navigate and wait for networkidle
        2. Screenshot or inspect DOM
        3. Identify selectors from rendered state
        4. Execute actions with discovered selectors
```

**MCP Playwright option:** If `mcp__plugin_playwright_playwright__*` tools are available, prefer them over writing Python scripts — no script file needed:
```
mcp__plugin_playwright_playwright__browser_navigate(url="http://localhost:3000")
mcp__plugin_playwright_playwright__browser_snapshot()
mcp__plugin_playwright_playwright__browser_click(selector="...")
mcp__plugin_playwright_playwright__browser_take_screenshot()
mcp__plugin_playwright_playwright__browser_console_messages()
```

### 3. Recon before action (dynamic apps)

```python
page.wait_for_load_state('networkidle')  # CRITICAL: wait before inspecting
page.screenshot(path='/tmp/inspect.png', full_page=True)
content = page.content()
page.locator('button').all()
```
Never inspect DOM before `networkidle` on dynamic apps — selectors may not exist yet.

### 4. Execute test actions

Use discovered selectors from step 3. Write targeted Playwright assertions.

### 5. Verify flows covered

After tests pass, re-run:
Re-run `search_graph` then `trace_path(project=CBM_PROJECT, mode="data_flow")`.
All impacted flows tested? Any gaps → add tests.

### 6. Report
```
✅ /supergraph:webapp-testing
- Flows tested: N/M | Console errors: [list/none]
- Screenshots: [paths] | Selectors verified: [list]
- Next: /supergraph:verify → /supergraph:review
```

## Using with_server.py

Helper script `scripts/with_server.py` manages server lifecycle. **Always run `--help` first** — do NOT read the source unless absolutely necessary (large file, pollutes context window).

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_test.py
```

**Multiple servers:**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_test.py
```

**Automation script template** (server managed externally by with_server.py):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL
    # ... test logic
    browser.close()
```

## Reference Examples

If `examples/` directory exists in project:
- `examples/element_discovery.py` — discovering buttons, links, inputs
- `examples/static_html_automation.py` — file:// URLs for local HTML
- `examples/console_logging.py` — capturing console logs

## Rules

- ALWAYS wait for `networkidle` before inspecting DOM on dynamic apps
- NEVER read `scripts/with_server.py` source — use `--help` and invoke as black box
- Prefer MCP Playwright tools (`mcp__plugin_playwright_playwright__*`) over writing Python scripts when available
- Identify selectors from rendered state (recon-first), not from guessing
- Use descriptive selectors: `text=`, `role=`, CSS, or IDs — never positional selectors like `nth-child`
- Always close browser when done in Python scripts
- Re-check `trace_path` after tests pass to confirm full coverage
