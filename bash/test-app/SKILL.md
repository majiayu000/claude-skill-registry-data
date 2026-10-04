---
name: test-app
description: "Verify a running Mendix app in a browser with Playwright, with OQL for data assertions. Use when asked to test or validate the app end to end, or to confirm that generated pages actually render."
---

# Test App Skill

This skill guides you through verifying a running Mendix application using playwright-cli for browser automation and mxcli oql for data assertions.

## When to Use This Skill

Use this when:
- The user asks to test, verify, or validate a running Mendix app **in the browser**
- The user wants to confirm that generated pages and widgets actually render
- The user asks for end-to-end or integration tests involving the UI
- The user wants to verify that data is persisted correctly after UI interactions
- You have generated MDL that creates pages and want to close the feedback loop

For **microflow logic testing** (business rules, calculations, entity operations — no browser needed), use the `test-microflows` skill and `mxcli test` instead.

## Prerequisites

The devcontainer created by `mxcli init` installs:
- **Node.js** (LTS) — via the base image
- **playwright-cli** — installed globally, pinned to a known-good version (`npm install -g @playwright/cli@0.1.15`; the package's CLI surface shifts between releases, so it is deliberately not `@latest`)
- **Chromium (headless shell)** — installed via `@playwright/cli`'s **bundled** `playwright-core`, into a shared `PLAYWRIGHT_BROWSERS_PATH`, and exposed at the stable path `/usr/local/bin/mx-headless-shell`. The generated `.playwright/cli.config.json` pins `executablePath` to that symlink.
- **Docker-in-Docker** — Mendix + PostgreSQL running via `mxcli docker run`

If the app calls an external REST API, that endpoint is a prerequisite too — a verification run that depends on a live third party is not repeatable. See [mock-rest-apis](../mock-rest-apis/SKILL.md).

The app must be running before verification:

```bash
mxcli docker run -p app.mpr --wait
```

### `run-code` vs `eval` — read this first

`@playwright/cli` has **two** evaluation commands with **different contexts**:

| Command | Runs in | Use for |
|---------|---------|---------|
| `playwright-cli eval "() => ..."` | **browser page** (`document`, `window` exist) | DOM assertions, clicks, filling fields, reading `.mx-name-*` |
| `playwright-cli run-code "..."` | **Node** (Playwright API; `document` is **undefined**) | Playwright-level scripting, not page DOM |

`eval` takes a **function** (`"() => ..."`) and prints its return value under `### Result`. If it returns a Promise, the CLI awaits it. **Do not** use `run-code "document.querySelector(...)"` — it throws `ReferenceError: document is not defined`. Every page assertion below uses `eval`.

### Browser setup gotchas (Linux arm64)

If you are provisioning manually (outside `mxcli init`) or debugging a browser-launch failure, know these:

- `playwright-cli install` **initializes the workspace** — it does *not* install a browser. The browser command is `playwright-cli install-browser`.
- `open --browser` only accepts `chrome | firefox | webkit | msedge` (no `chromium`), and the default is the **chrome channel** — which has **no distribution on Linux arm64**, and neither does msedge. `npx playwright install chrome` fails with `ERROR: not supported on Linux Arm64`.
- The fix is to use the **bundled Chromium** and pin it explicitly. Install via `@playwright/cli`'s own `playwright-core`:
  ```bash
  node "$(npm root -g)/@playwright/cli/node_modules/playwright-core/cli.js" install chromium chromium-headless-shell
  ```
  then point `.playwright/cli.config.json` at the headless-shell binary (headless mode needs the `chromium_headless_shell-*` build, not the full `chromium-*` one):
  ```json
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "headless": true,
      "executablePath": "/usr/local/bin/mx-headless-shell"
    }
  }
  ```
  `mxcli init` does all of this for you (the Dockerfile installs the headless shell and creates the `/usr/local/bin/mx-headless-shell` symlink). This path is the devcontainer symlink; if you run playwright-cli natively outside the container, point `executablePath` at your own install (or drop it and let a working default resolve).

---

## Quick Start

```bash
# open browser session (headless by default)
playwright-cli open http://localhost:8080

# Take a snapshot to see the page structure and element refs
playwright-cli snapshot

# Interact with elements using refs from snapshot
playwright-cli click e12
playwright-cli fill e15 "some text"

# Verify widget presence (page context -> use eval with a function)
playwright-cli eval "() => document.querySelector('.mx-name-dgCustomers') !== null"

# Take a screenshot for visual inspection
playwright-cli screenshot

# close browser when done
playwright-cli close
```

---

## Widget Name Selectors

Mendix renders each widget's `name` property as a CSS class on the DOM element:

```html
<div class="mx-name-submitButton form-group">
```

This maps directly to MDL widget names. When you generate a widget in MDL:

```sql
actionbutton submitButton (caption: 'Submit', action: save changes)
```

The stable CSS selector is `.mx-name-submitButton`. Use this with `eval` for reliable assertions:

```bash
playwright-cli eval "() => document.querySelector('.mx-name-submitButton') !== null"
```

---

## Verification Patterns

### Login (Security Enabled)

The Mendix login page uses standard HTML IDs:

> **Always dispatch an `input` event after setting `.value`.** Mendix (and React)
> inputs track their state from the `input` event, not the raw `.value` property.
> Setting `.value` alone can leave the field "empty" as far as the app is
> concerned, so the login — or any form fill — silently fails. Every field-setting
> `eval` below follows the `set value → dispatchEvent('input')` pattern.

```bash
playwright-cli open http://localhost:8080
playwright-cli snapshot
playwright-cli eval "() => { const el = document.querySelector('#usernameInput'); el.value = 'MxAdmin'; el.dispatchEvent(new Event('input', {bubbles: true})) }"
playwright-cli eval "() => { const el = document.querySelector('#passwordInput'); el.value = 'AdminPassword1!'; el.dispatchEvent(new Event('input', {bubbles: true})) }"
playwright-cli eval "() => document.querySelector('#loginButton').click()"

# wait for home page to load
playwright-cli eval "() => new Promise(r => setTimeout(r, 3000))"
playwright-cli snapshot

# Save auth state for reuse
playwright-cli state-save mendix-auth
```

To reuse saved auth in a later session:
```bash
playwright-cli open http://localhost:8080
playwright-cli state-load mendix-auth
playwright-cli goto http://localhost:8080/p/Customer_Overview
```

**When security is OFF**: Skip login entirely. Navigate directly to `/`.

### Widget Presence Verification

After navigating to a page, verify that all expected widgets are present:

```bash
playwright-cli goto http://localhost:8080/p/Customer_Overview

# check multiple widgets
playwright-cli eval "() => document.querySelector('.mx-name-dgCustomers') !== null"
playwright-cli eval "() => document.querySelector('.mx-name-btnNew') !== null"
playwright-cli eval "() => document.querySelector('.mx-name-btnEdit') !== null"
playwright-cli eval "() => document.querySelector('.mx-name-btnDelete') !== null"
```

### Form Interaction

```bash
playwright-cli goto http://localhost:8080/p/Customer_Edit

# Take snapshot to discover element refs
playwright-cli snapshot

# Fill form fields using .mx-name-* selectors (page context -> eval)
playwright-cli eval "() => { const el = document.querySelector('.mx-name-txtName input'); el.value = 'Test Customer'; el.dispatchEvent(new Event('input', {bubbles: true})) }"
playwright-cli eval "() => { const el = document.querySelector('.mx-name-txtEmail input'); el.value = 'test@example.com'; el.dispatchEvent(new Event('input', {bubbles: true})) }"

# or use fill with snapshot refs (simpler when refs are known)
playwright-cli fill e42 "Test Customer"
playwright-cli fill e45 "test@example.com"

# Click save
playwright-cli eval "() => document.querySelector('.mx-name-btnSave').click()"
```

### Page Navigation (Security OFF)

When security is OFF, direct `/p/PageName` URLs **do not work** — Mendix redirects to the home page. Navigate through your own named widgets instead:

```bash
playwright-cli open http://localhost:8080

# wait for Mendix to load
playwright-cli eval "() => new Promise(r => { const check = () => document.querySelector('.mx-page') ? r() : setTimeout(check, 500); check(); })"

# Click navigation button (from your MDL-defined NavigationMenu snippet)
playwright-cli eval "() => document.querySelector('.mx-name-btnCustomers').click()"

# wait and verify target page
playwright-cli eval "() => new Promise(r => setTimeout(r, 2000))"
playwright-cli eval "() => document.querySelector('.mx-name-dgCustomers') !== null"
```

### Page Navigation (Security ON)

Direct URLs work after login:

```bash
playwright-cli state-load mendix-auth
playwright-cli goto http://localhost:8080/p/Customer_Overview
playwright-cli eval "() => document.querySelector('.mx-name-dgCustomers') !== null"
```

### Data Assertions via OQL

After a UI interaction, verify data persistence using `mxcli oql` (no `pg` package needed):

```bash
# after creating a customer through the UI...
mxcli oql -p app.mpr --json "SELECT Name, Email FROM MyModule.Customer WHERE Name = 'Test Customer'"
```

This returns JSON that you can inspect directly. No npm dependencies required.

---

## CI/CD: Test Scripts

For regression testing in CI/CD, capture playwright-cli commands as shell scripts. These are the same commands used interactively — readable without TypeScript knowledge.

### Script Format

```bash
#!/usr/bin/env bash
# tests/verify-customers.sh
set -euo pipefail

# Setup
playwright-cli open http://localhost:8080
playwright-cli eval "() => { const el = document.querySelector('#usernameInput'); el.value = 'MxAdmin'; el.dispatchEvent(new Event('input', {bubbles: true})) }"
playwright-cli eval "() => { const el = document.querySelector('#passwordInput'); el.value = 'AdminPassword1!'; el.dispatchEvent(new Event('input', {bubbles: true})) }"
playwright-cli eval "() => document.querySelector('#loginButton').click()"
playwright-cli eval "() => new Promise(r => setTimeout(r, 3000))"

# Verify Customer overview
playwright-cli goto http://localhost:8080/p/Customer_Overview
playwright-cli eval "() => { if (!document.querySelector('.mx-name-dgCustomers')) throw new Error('dgCustomers not found') }"
playwright-cli eval "() => { if (!document.querySelector('.mx-name-btnNew')) throw new Error('btnNew not found') }"

# create a customer
playwright-cli eval "() => document.querySelector('.mx-name-btnNew').click()"
playwright-cli eval "() => new Promise(r => setTimeout(r, 2000))"
playwright-cli fill txtName "CI Test Customer"
playwright-cli fill txtEmail "ci@test.com"
playwright-cli eval "() => document.querySelector('.mx-name-btnSave').click()"
playwright-cli eval "() => new Promise(r => setTimeout(r, 2000))"

# Verify data persistence
mxcli oql -p app.mpr --json "SELECT Name FROM MyModule.Customer WHERE Name = 'CI Test Customer'" \
  | grep -q "CI Test Customer"

# Cleanup
playwright-cli close
echo "PASS: verify-customers"
```

### Running Scripts

```bash
# run directly
bash tests/verify-customers.sh

# run all test scripts
for f in tests/verify-*.sh; do bash "$f" || exit 1; done

# via mxcli (auto-detects app port, captures a screenshot on failure)
mxcli playwright verify tests/ -p app.mpr

# in the edit -> rebuild -> re-verify loop, keep the browser warm so the next
# run reuses the live, still-logged-in session instead of cold-launching
# Chromium (reuse re-navigates, so a rebuilt app is loaded fresh)
mxcli playwright verify tests/ -p app.mpr --keep-open
```

> When reusing across runs (`--keep-open`), **drop any trailing
> `playwright-cli close`** from the scripts — a script that closes the session
> tears it down for the next run regardless of `--keep-open`. Omit `--keep-open`
> for CI so the browser is torn down at the end.

### Assertion Pattern

For `set -e` scripts, `eval` a function that throws to trigger a non-zero exit. The throw must use JavaScript's `Error` constructor (capital E):

```bash
# This exits non-zero if widget is missing
playwright-cli eval "() => { if (!document.querySelector('.mx-name-widgetName')) throw new Error('missing widgetName') }"
```

---

## Session Management

playwright-cli maintains browser sessions across commands. The devcontainer sets `PLAYWRIGHT_CLI_SESSION=mendix-app` by default, so every command shares one browser — state, cookies, and login persist between invocations.

### mxcli lifecycle commands (preferred)

`mxcli playwright` wraps the session so you manage it explicitly across turns, with the project's port/browser resolution built in:

```bash
# open or attach to the session (URL: arg, else --base-url, else .docker/.env, else :8080)
mxcli playwright open -p app.mpr

# is a session live, and what page is it on?
mxcli playwright status

# tear down
mxcli playwright close          # current session
mxcli playwright close --all    # every session
```

**Agentic loop pattern** — open once, log in once, then iterate cheaply:

```bash
mxcli playwright open -p app.mpr                 # 1. warm the browser
# ... log in (script or the login snippet above), state-save mendix-auth ...
mxcli playwright verify tests/ -p app.mpr --keep-open   # 2. verify, keep it warm
# ... edit MDL, mxcli exec, mxcli docker run --fresh --wait ...
mxcli playwright verify tests/ -p app.mpr --keep-open   # 3. reuses the warm, logged-in session
mxcli playwright status                          # check it's still up before deciding to reopen
```

`open` and `verify` share the same open-or-reuse behavior: attach to a live same-origin session (re-navigating so a rebuilt app loads fresh), or open a new one.

### Low-level playwright-cli session commands

```bash
playwright-cli list                          # list active sessions
playwright-cli close                         # close current session
playwright-cli close-all                     # close all sessions
playwright-cli -s=test2 open http://localhost:8080   # named session (parallel testing)
```

---

## Debugging

```bash
# Take screenshot
playwright-cli screenshot

# Take screenshot of specific element
playwright-cli screenshot e42

# show console messages
playwright-cli console

# show network requests
playwright-cli network

# Start/stop tracing
playwright-cli tracing-start
# ... do interactions ...
playwright-cli tracing-stop

# Visual monitoring dashboard
playwright-cli show
```

> **Headed mode** (`open --headed`) needs the full Chromium build and a display; the devcontainer ships only the headless shell and has no display, so use screenshots/tracing for visual debugging instead.

---

## Selector Rules

**Use `.mx-name-*` selectors from your own MDL widgets.** These are reliable and predictable because you control the widget names:

```sql
-- MDL: names you define become test hooks
actionbutton btnDrivers (caption: 'Drivers', action: show page Module.Drivers_Overview)
datagrid dgOrders (datasource: database Module.Order) { ... }
```

```bash
# Tests: use .mx-name-* selectors for those names
playwright-cli eval "() => document.querySelector('.mx-name-btnDrivers').click()"
playwright-cli eval "() => document.querySelector('.mx-name-dgOrders') !== null"
```

**Do NOT guess CSS selectors for Mendix built-in layout widgets.** The top navigation bar, sidebar, header, and other platform UI elements have unpredictable class names.

**NavigationList items need `text_` prefix.** The `<li>` container does NOT get an `mx-name-*` class. The inner `<span>` gets `mx-name-text_<itemName>`:

```bash
# use text_ prefix for navigationlist items
playwright-cli eval "() => document.querySelector('.mx-name-text_itemDrivers').click()"
```

**DataGrid2 rows**: Both header and data rows share `role="row"`. Filter with `:has([role="gridcell"])`:

```bash
playwright-cli eval "() => document.querySelector('.mx-name-dgCustomers [role=\"row\"]:has([role=\"gridcell\"])').textContent"
```

---

## Known Gotchas

### Never use `waitForLoadState('networkidle')`
Mendix maintains a permanent long-polling XHR connection. `networkidle` never fires. Use element-based waits via `eval` instead.

### Top navigation clicks intercepted
Clicking top nav items may fail due to `div.mx-placeholder` overlay. Dispatch the event directly (note the capital `Event`):

```bash
playwright-cli eval "() => document.querySelector('.mx-name-navigationTree1-1').dispatchEvent(new Event('click', {bubbles: true}))"
```

### Login page selectors are stable
The Mendix login page (`/login.html`) uses fixed IDs: `#usernameInput`, `#passwordInput`, `#loginButton`. These are stable across Mendix versions.

---

## Feedback Loop Workflow

The key workflow: generate MDL → build → verify → fix → repeat.

```bash
# 1. generate and apply MDL
mxcli exec changes.mdl -p app.mpr

# 2. build and start
mxcli docker run -p app.mpr --fresh --wait

# 3. open browser and verify
playwright-cli open http://localhost:8080
playwright-cli snapshot
# ... verify widgets, fill forms, check data ...

# 4. Fix any issues in MDL, rebuild, re-verify
```

### Interpreting Failures

| Failure Type | What It Means | MDL Fix |
|-------------|---------------|---------|
| `.mx-name-X` not found | Widget X missing from DOM | Check widget nesting, container visibility, BSON structure |
| `ReferenceError: document is not defined` | Used `run-code` for a page assertion | Use `eval "() => ..."` (page context), not `run-code` (Node) |
| `Chromium distribution 'chrome' is not found` | Browser not provisioned / chrome channel on arm64 | See "Browser setup gotchas" — install bundled Chromium + pin `executablePath` |
| Page returns 500 | Runtime error on page load | Check page layout, datasource, parameter bindings |
| Page returns 404 | Page doesn't exist or wrong URL | Verify page qualified name and navigation |
| OQL returns empty | Microflow didn't commit | Check COMMIT statement, error handling in microflow |
| Console error | JavaScript error in widget | Check widget template, pluggable widget config |

---

## Related Skills

- [test-microflows](../test-microflows/SKILL.md) - **MDL microflow tests** (business logic, no browser needed)
- [/run-app](../run-app/SKILL.md) - Build and start the Mendix app in Docker
- [/docker-workflow](../docker-workflow/SKILL.md) - Full Docker workflow reference
- [/demo-data](../demo-data/SKILL.md) - Seed test data into PostgreSQL
- [/create-page](../create-page/SKILL.md) - Page creation patterns (widget names for selectors)
- [/write-microflows](../write-microflows/SKILL.md) - Microflow patterns (data persistence logic)
