---
name: chrome-devtools-browser-automation
description: Automate browser input, navigation, and interaction via Chrome DevTools MCP (Puppeteer-backed). Click, type, fill forms, drag, upload, navigate pages, wait for conditions, emulate devices.
origin: https://github.com/ChromeDevTools/chrome-devtools-mcp (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Chrome DevTools Browser Automation

Drive a live Chrome instance through 16 input + navigation MCP tools backed by Puppeteer.

## When to Use

- Automating form fills, clicks, drags in a running browser
- Multi-step UI flows that need real browser rendering
- Agent-driven E2E test execution without a separate test runner
- Device emulation for responsive testing
- Waiting for network idle / selector / navigation before next step

## Do NOT use for

- Static HTML scraping (use fetch/curl instead — no browser needed)
- Headless screenshot-only tasks (use `chrome-devtools-lcp-debug` or screenshot tool)
- Production traffic interception (use `chrome-devtools-network-inspector`)

## Input Automation Tools (10)

```
browser_click              — click element by selector or coordinates
browser_drag               — drag from source to target coordinates
browser_fill               — fill input/textarea with value (clears first)
browser_handle_dialog      — accept/dismiss alert, confirm, prompt
browser_hover              — hover over element (trigger CSS :hover)
browser_press_key          — press keyboard key (e.g. "Enter", "Tab", "Escape")
browser_type               — type text character-by-character (realistic)
browser_upload_file        — set file input to local file path
browser_select_option      — choose <select> option by value or label
browser_coordinate_click   — click at (x, y) pixel coordinates
```

## Navigation Tools (6)

```
browser_close              — close current page/tab
browser_list_pages         — list all open pages with URL + title
browser_navigate           — navigate to URL, await load
browser_new_page           — open new tab, optionally navigate
browser_select_page        — switch active page by index or URL match
browser_wait_for           — wait for selector / navigation / network idle
```

## Emulation Tools (2)

```
browser_emulate_device     — emulate device (iPhone 14, Pixel 7, etc.)
browser_resize_page        — set viewport to custom W×H
```

## Usage Pattern

```yaml
# Form automation flow
1. browser_navigate: url: "https://app.example.com/login"
2. browser_wait_for: selector: "#email-input"
3. browser_fill: selector: "#email-input", value: "user@example.com"
4. browser_fill: selector: "#password-input", value: "secret"
5. browser_click: selector: "button[type=submit]"
6. browser_wait_for: navigation: true

# Device emulation
1. browser_emulate_device: device: "iPhone 14 Pro"
2. browser_navigate: url: "https://app.example.com"
3. browser_screenshot  # verify mobile layout
```

## Agent Tip: Wait Before Act

Always use `browser_wait_for` after navigation or dynamic renders. Puppeteer's auto-wait covers most cases, but SPA route changes and lazy-loaded components need explicit waits.

```yaml
browser_navigate: url: "https://app.example.com/dashboard"
browser_wait_for: selector: "[data-testid='dashboard-loaded']"
# now safe to interact
```

## Anti-Fake-Pass Checklist

- [ ] `browser_navigate` returns final URL (confirm no redirect loop)
- [ ] `browser_fill` verified by reading back value — not just calling the tool
- [ ] `browser_wait_for` used before any click on dynamic content
- [ ] Device emulation verified with `browser_screenshot` after emulate call
- [ ] Dialog handler registered BEFORE action that triggers dialog
