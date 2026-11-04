---
name: browser
description: Browse via node .rulesync/scripts/browser.mjs (Lightpanda). App e2e uses Playwright.
---
Zero-config. `node .rulesync/scripts/browser.mjs <verb>`.

Verbs: `nav <url>` · `snap` · `click <ref>` · `fill <ref> <text>` · `scroll [ref|down|up|N]` · `wait [ms]` · `hover <ref>` · `select <ref> <value>` · `shot` · `pdf` · `stop` · `doctor` · `ensure`.

- **snap** = default read (markdown + numbered refs). `click`/`fill` need a prior snap.
- Lightpanda default. The rail swaps to Chromium when `shot`/`pdf`/`trace`, win32, missing Lightpanda, probe-fail once, Chromium-first hosts (figma docs/sheets/slides mail.google earth amazon), or a blocked/empty/client-rendered snap. One swap. Do not stop and say you cannot.
- Session/profile: `.tmp/grunt/browser/`. `stop` reaps; second `stop` ok.
- Windows: Chromium even if Lightpanda exists.
- `doctor`/`ensure` → `node .rulesync/scripts/doctor.mjs` or `grunt doctor`. Engine hints: `node .rulesync/scripts/setup.mjs browser`. Do not read a README unless doctor/setup is missing; then https://github.com/lovrozagar/grunt#prerequisites (not the consumer README).
- No env. No MCP. No raw Playwright. Spec: `.rulesync/reference/browser.md`.
