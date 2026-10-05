---
name: verify
description: Build, launch, and drive the P3DX dashboard to verify changes at the browser surface.
---

# Verifying p3dx-dashboard changes

Vite + React 19 SPA, no backend. All state lives in localStorage
(`p3dx-dashboard-state-v3` for data, `p3dx-theme` for theme).

## Launch

```bash
npm run dev -- --port 5199 --strictPort   # background it; ready in ~1s
```

`npm run lint` is oxlint; pre-existing warnings in store.jsx / ui.jsx /
AgentDetail.jsx are known noise.

## Drive (headless browser)

No Playwright in project deps. A working install lives in the npx cache —
import it by absolute path with system Chrome:

```js
import { chromium } from '/home/shikhar/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: true });
```

(If that cache hash is gone, re-run `npx playwright --version` and re-glob
`~/.npm/_npx/*/node_modules/playwright`.)

## Flows worth driving

- Sidebar nav: Overview / World Explorer / Directory / Connections /
  Consents / Transactions (text= selectors work).
- Theme toggle: `.theme-toggle` in topbar flips `document.documentElement.dataset.theme`;
  persists to `p3dx-theme`; fresh visitors follow `prefers-color-scheme`
  (set via Playwright context `colorScheme`).
- Demo walkthrough: switch "Acting as" (topbar select), request/approve
  connections, grant consent, execute exchange.
- "Reset demo" uses `confirm()` — auto-accept dialogs in Playwright.
