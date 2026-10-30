---
name: browser
description: >-
  Browser and device automation: pick the right engine (the host's preview panel
  first, an anti-detect browser over MCP for hard targets, CDP CLI or Playwright
  for test suites), test local web apps, capture full-page screenshots, and drive
  Android over adb (including a mobile signup without the QR wall). One
  contract; the parts under parts/ carry the methods.
---

# browser — automation engines, testing, and Android

> Home branch in Memora: `root/skill/browser`.
>
> Engine order: (1) the host's own preview panel — `HOSTS.md`, verb *Show app*;
> (2) a real anti-detect browser driven over MCP; (3) Playwright or a CDP CLI for
> headless suites and CI. A local dev server is shown, not screenshotted, unless
> the task needs the pixels.

## Choosing a part

| Task | Part |
|---|---|
| Choose the right browser engine for the task | `parts/browser-automation/` |
| Standalone CDP CLI navigation, forms, extraction | `parts/agent-browser/` |
| Anti-detect Camoufox browsing via BrowserMCP (logins, 2FA/TOTP, snapshots) | `parts/browsermcp-automation/` |
| Production Playwright e2e suites, flaky-test repair, CI/CD | `parts/playwright-pro/` |
| Interactive testing and console/network inspection of local web apps | `parts/webapp-testing/` |
| Full-page / tall-page / SPA scroll-container screenshots via CDP | `parts/full-page-screenshot/` |
| Validation-heavy scraping, crawling, PDF/table extraction pipelines | `parts/universal-scraping-architect/` |
| Drive an Android phone via USB (`adb`, UI dump, MIUI toggles, SMS inbox) | `parts/android-adb-automation/` |

## Rules

- Walk `root/skill/browser` in Memora before starting non-trivial automation; record new anti-bot or device findings as nodes.
- Ask the owner when choosing between a logged-in session and a clean anti-detect
  profile, and before any action inside a signed-in account.
- Before any web deploy, show the running dev server in the host's panel.
- A project-specific capture recipe belongs inside that project, not in this
  router.

## Related

`research` (`skills/research/parts/searchmcp-research/` for multi-engine Camoufox research), `reverse-engineering` (`skills/reverse-engineering/parts/browser-extension-reverse/`), `osint` (platform collection).
