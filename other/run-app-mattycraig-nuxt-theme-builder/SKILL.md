---
name: run-app
description: Build, start, and drive the Nuxt Theme Builder in a real browser (Playwright) to verify a change end to end — editor interactions, iframe preview sync, persistence across reloads, source view. Use when asked to run/start/screenshot the app or to prove a UI or persistence change works beyond unit tests.
argument-hint: "[route or scenario to verify]"
---

# Run and drive the app: $ARGUMENTS

## Start a server

- **Fast iteration**: `pnpm dev` (port 3000). Security headers are disabled in dev, and the source-view map only refreshes on restart.
- **Production-like** (use this to verify SSR, hydration, cookies, CSP):
  ```bash
  NITRO_PRESET=node-server NODE_OPTIONS=--max-old-space-size=8192 pnpm build   # ~5 min
  NITRO_HOST=127.0.0.1 NITRO_PORT=3000 node .output/server/index.mjs          # run in the background
  ```
- Font-provider 403 warnings during the build are expected in network-restricted sandboxes.
- To stop the server, kill it by PID, or with `pkill -f "node .output/server"` in a **separate** command. A `pkill -f` pattern that also appears in its own command line kills the calling shell.

## Drive it

- Existing specs: `pnpm exec playwright test tests/e2e/smoke` (reuses a server already on :3000 locally).
- Ad-hoc checks: write a short script in your scratch dir using `chromium` from `@playwright/test`, and wait for `[data-testid="theme-editor"][data-hydrated="true"]` before interacting.
- In Claude Code on the web, if Playwright's pinned Chromium isn't installed, launch with `executablePath` pointing at the preinstalled build (`/opt/pw-browsers/chromium-*/chrome-linux/chrome`) instead of running `playwright install`.

## Useful checks

- **Theme sync**: on a demo route such as `/components/button`, change a control in the sidebar and assert that a CSS variable inside the preview iframe changes (`frameLocator("iframe")`). Other pages render without the iframe, so check the top document there.
- **Persistence**: `context.cookies()` → `theme` cookie holds `{ config, activePresetName }` (must stay under 4096 bytes); `localStorage["theme-presets"]` holds saved presets. Reload and assert that both survive.
- **Undo after reload**: make a change, then `ControlOrMeta+z` should return to the reloaded theme.
- **Source view** (`/templates/*`): toggle to code, navigate to another template and back, and confirm the code matches the route.
- **Hydration**: collect `page.on("console")` messages and fail on "Hydration" warnings (dev server).

Report what you ran, what you observed (quote values), and clean up the server and any scratch scripts.
