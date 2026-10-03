---
name: html-screenshot
description: Generate full-page screenshots of HTML files when browser_vision or the Hermes browser tool times out on local Chrome.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, screenshot, browser, playwright]
---

# html-screenshot

Generate full-page screenshots of HTML files when `browser_vision` or the Hermes browser tool times out on local Chrome.

## When to use

- User asks to render HTML as an image/screenshot
- `browser_vision` or `browser_navigate` + `browser_vision` times out (common on local Chrome/CDP)
- Need full-page capture beyond viewport height (Chrome `--headless --screenshot` caps at viewport)

## Steps

1. Write the HTML to a temp file (e.g. `/tmp/page.html`)

2. Install Playwright if not already available:
   ```bash
   pip install playwright --break-system-packages
   ```

3. Install Chromium browser + system deps:
   ```bash
   python3 -m playwright install --with-deps chromium
   ```

4. Capture full-page screenshot:
   ```python
   /usr/bin/python3 -c "
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page(viewport={'width': 1200, 'height': 2200})
       page.goto('file:///tmp/page.html')
       page.screenshot(path='/tmp/output.png', full_page=True)
       browser.close()
       print('Done')
   "
   ```

   Adjust `height` in viewport if the page is taller — it doesn't need to match the full page, just needs to be large enough for the initial render. `full_page=True` handles the rest.

5. Share with user: `![description](MEDIA:/tmp/output.png)`

## Notes

- Always use `/usr/bin/python3` (system Python) for Playwright since it was installed globally, not in the hermes-agent venv.
- If the page is very tall, increase the viewport height.
- The DBus errors in Chrome headless output are benign and can be suppressed with `2>/dev/null`.
- If Playwright is already installed, skip steps 2–3.
