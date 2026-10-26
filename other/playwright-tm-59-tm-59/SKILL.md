---
name: playwright
description: Use when writing browser end-to-end and smoke tests with Playwright — testing every screen for console errors, screenshots for visual review and README images, mobile viewports, offline mode, WebGL and WASM pages in headless Chromium, audio checks with the Web Audio API, and running browsers without root access. Also use when E2E tests are flaky, too slow for CI, or cannot launch a browser on a minimal Linux machine.
---

# Playwright

Default: `@playwright/test`, Chromium only unless cross-browser matters, a `webServer` entry that starts the app on a fixed port, smoke tests that fail on console errors, run locally (E2E with recording is too heavy for a minutes-limited CI).

## Setup

```ts
// playwright.config.ts
export default defineConfig({
  testDir: "e2e",
  use: { baseURL: "http://localhost:4300", trace: "retain-on-failure" },
  webServer: { command: "npm run preview -- --port 4300 --strictPort", url: "http://localhost:4300" },
  projects: [{ name: "desktop", use: devices["Desktop Chrome"] }, { name: "phone", use: devices["Pixel 7"] }],
});
```

Pick a port no other project uses; a clash makes tests hit the wrong app.

## Smoke test pattern

```ts
test("title screen", async ({ page }) => {
  const errors: string[] = [];
  page.on("console", m => { if (m.type() === "error" || m.type() === "warning") errors.push(m.text()); });
  page.on("pageerror", e => errors.push(e.message));
  await page.goto("/");
  await expect(page.getByRole("button", { name: /start/i })).toBeVisible();
  await page.screenshot({ path: "e2e-out/title.png" });
  expect(errors).toEqual([]);
});
```

- Wait for UI states (`toBeVisible`, `toHaveText`), never fixed sleeps.
- For canvas games, expose a small read-only test hook (e.g. `window.__game.state()`) and wait on it instead of pixels.

## Special cases

- **WebGL/WASM headless:** Chromium falls back to software rendering (SwiftShader); it works but is slow. Treat fps as relative, increase timeouts for first frame.
- **Offline:** `context.setOffline(true)` to test service-worker caching, then back online to check sync.
- **Audio:** you cannot hear in CI, but you can measure: connect an `AnalyserNode` and assert RMS > 0 on each screen that should play sound.
- **Speech synthesis:** headless environments often have no voices; mock the voice list to test fallbacks.
- **Locales:** run key tests with `locale: "ja-JP"` and `"en-US"`.

## Machines without root

`npx playwright install chromium` downloads the browser to the user cache. System libraries may be missing; `install-deps` needs root. Without root, extract the needed packages into a user directory and point `LD_LIBRARY_PATH` at it.

## Verification loop

1. `npx playwright test` passes on desktop and phone projects.
2. Look at the screenshots: tests can pass on a black screen.
3. On failure, open the trace (`npx playwright show-trace`).

## Pitfalls

- **Flaky selectors:** prefer roles and labels over CSS classes and nth-child.
- **Animations** cause screenshot diffs; disable them in test mode or wait for a "settled" flag.
- **Shared state between tests:** use a fresh context per test (the default) and clear storage where needed.
- **Recording video** for every test is slow and large; enable only for marketing captures or on failure.
