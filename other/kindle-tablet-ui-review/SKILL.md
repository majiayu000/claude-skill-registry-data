---
name: kindle-tablet-ui-review
description: Review and improve AetherCode UI for Kindle Fire tablet constraints (7-11 inch displays, touch ergonomics, offline resilience).
---

# Kindle Tablet UI Review

Use this skill when refining the Kindle app UX for real tablet usage.

## Review Checklist
1. Touch targets: at least 48dp-equivalent for primary actions.
2. Readability: minimum body text 14-16px with high contrast.
3. Layout: avoid dense two-column flows on 7-inch devices.
4. Offline mode: clear state indicator when network drops.
5. Latency guard: show loading states for remote model calls.
6. Navigation: keep key controls in thumb-accessible zones in landscape.

## Working Method
1. Compare `src/aethercode/app.html` and `kindle-app/www/index.html`.
2. Patch source UI first (`src/aethercode/app.html`), then regenerate `www` assets:
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE\kindle-app
npm run copy:assets
```
3. Validate on Kindle via ADB install.
4. Emit cross-talk packet with before/after notes and screenshot paths.

## Minimum Evidence
- Updated file paths
- At least one device-targeted test note (7", 8", 10", or 11")
- One clear UX improvement claim tied to a visible change
