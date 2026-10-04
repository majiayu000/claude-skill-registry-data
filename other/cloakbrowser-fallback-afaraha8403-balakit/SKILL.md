---
name: cloakbrowser-fallback
description: >-
  Stealth browser fallback using CloakBrowser (custom-compiled Chromium with
  C++ source-level fingerprint patches). Use when the built-in browser tool or
  Chrome DevTools fails due to bot detection, Cloudflare/Turnstile walls,
  reCAPTCHA, 403/429/"access denied"/"are you human" interstitials, or empty/
  blocked responses. Also use when the user asks for "cloakbrowser", "stealth
  browser", or to bypass a block.
user-invocable: true
disable-model-invocation: true
version: "1.1.0"
author: "Ali Farahat"
tags: ["cloakbrowser", "stealth-browser", "anti-bot-bypass", "playwright", "fallback"]
when_to_use: |
  USE WHEN:
  - The built-in browser returned 403, 429, "Access Denied", "blocked".
  - A Cloudflare, Turnstile, or reCAPTCHA wall blocks content.
  - The response is empty or clearly a bot-detection interstitial.
  - The user explicitly asks for stealth browser or to bypass a block.
  - Normal automation fails to load a page.

  DO NOT USE WHEN:
  - The built-in browser works fine (try it first).
  - The site requires login credentials or image CAPTCHAs (CloakBrowser can't
    solve these).
  - The user wants to bypass paywalls or violate a site's terms of service.
---

# CloakBrowser Fallback

> **Leading words:** stealth browser, fallback, humanize, bot detection,
> Turnstile, headless failover, real Chromium binary.

Stealth Chromium for navigating sites that block ordinary automation. Drop-in
Playwright API, but the browser is a custom-compiled Chromium binary, so
detectors score it as a real human browser.

Already installed on this machine. Both languages share the same stealth binary at `~/.cloakbrowser/`:
- **Python** (global): `pip` package `cloakbrowser`.
- **JS** (self-contained in this skill's `scripts/`): npm `cloakbrowser` + `playwright-core`.

Prefer **Python** by default. Use **JS** when the target codebase/repo is JS/TS or the user asks for it.

## When to reach for this

Use as a **fallback only** — try the built-in browser tool or Chrome DevTools
MCP first. Escalate to CloakBrowser when any of the triggers in the
frontmatter `when_to_use` fire (403/429, Cloudflare/Turnstile/reCAPTCHA walls,
empty/blocked response, explicit user ask).

**Headless failover pattern:** start headless. If a Turnstile **managed**
challenge appears, re-run with `--headed` — it clears with one click after the
page settles. If an image CAPTCHA appears, stop and report to the user —
CloakBrowser does not solve image CAPTCHAs.

## Quick start (one-shot fetch)

Run the helper — it prints final URL, title, and page text, and saves a screenshot.

Python:

```bash
python scripts/cloak_fetch.py "https://protected-site.com"
```

JS (run from this skill's `scripts/` dir so `node_modules` resolves):

```bash
node scripts/cloak_fetch.mjs "https://protected-site.com"
```

Both accept the same flags:
- `--headed` — show the window. Needed for Turnstile **managed** challenges (resolves with a single click).
- `--screenshot path.png` — where to save the screenshot (default: `cloak_shot.png`).
- `--html path.html` — also dump raw HTML.
- `--wait 5000` — extra ms to wait after load for JS challenges to clear.

## Inline usage (when you need custom interaction)

Python (sync API):

```python
from cloakbrowser import launch

browser = launch(headless=True, humanize=True)  # humanize=True → human-like mouse/keyboard
page = browser.new_page()
page.goto("https://protected-site.com", wait_until="domcontentloaded")
page.wait_for_timeout(4000)                       # let JS challenges clear
print(page.title())
page.screenshot(path="cloak_shot.png", full_page=True)
html = page.content()
browser.close()
```

JS (async API):

```javascript
import { launch } from "cloakbrowser";

const browser = await launch({ headless: true, humanize: true });
const page = await browser.newPage();
await page.goto("https://protected-site.com", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(4000);
console.log(await page.title());
await page.screenshot({ path: "cloak_shot.png", fullPage: true });
const html = await page.content();
await browser.close();
```

Everything else is standard Playwright (`click`, `fill`, `locator`, etc.) — same API you already know.

## Decision notes

- **Turnstile non-interactive** → works headless, auto-resolves.
- **Turnstile managed** → use `--headed`; it clears with one click after the
  page settles (the headless-failover pattern from above).
- CloakBrowser does **not** solve image CAPTCHAs and has no built-in proxy
  rotation. If a site demands an image CAPTCHA, report that to the user
  rather than looping.
- Don't use this to defeat paywalls/auth or violate a site's terms — it's for
  reaching content blocked by overzealous bot detection during legitimate work.

## Verifying / maintaining the binary

```bash
python -m cloakbrowser info     # version, path, platform
python -m cloakbrowser install  # download binary if missing (~535 MB, one-time)
python -m cloakbrowser update   # pull a newer stealth Chromium
```

If a run fails with "binary not found", run `python -m cloakbrowser install` first.
