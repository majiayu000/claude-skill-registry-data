---
name: control-ui
description: Drive and inspect a web, IDE, or Electron UI on this computer and verify it with evidence. Use for UI checks, screenshots, accessibility snapshots, performance profiles, visual diffs, or reproducing a UI bug.
disable-model-invocation: true
---

> Names in backticks, such as `drive-app` and `inspect-runtime`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here.

# Control UI

Verify UI behavior with evidence from the running app. `drive-app` says which browser or app-control tool this environment has. This skill says how to use that tool one step at a time, and how to build a temporary harness when the environment has none.

## Use it for

- Reproducing a UI bug that needs real focus, keyboard input, scrolling, resizing, or rendering.
- Checking a visual or accessibility change with screenshots and snapshots.
- Checking a web, IDE, or Electron change on this computer before it ships.
- Capturing console logs, network logs, CPU profiles, traces, or heap snapshots, with `inspect-runtime` when you attach to the process.
- Before and after evidence for a claim (the **principle-prove-it-works** skill).

## Set up

1. Start the app with the repository's documented dev command.
2. Look for a harness the repository already has, such as Playwright or Cypress tests, Storybook, browser scripts, Electron launch scripts, or snapshot tools. Use it first, because it knows the app's startup and markers.
3. Otherwise use the tool `drive-app` resolves to. When nothing resolves, build one of the temporary harnesses below.
4. For a web app, open the local URL. For Electron or another Chromium app, start it with a remote debugging port when it supports one.
5. Pick the page by a stable marker of the app, not by tab order alone.
6. Target elements by accessibility role, label, or a stable `data-*` attribute, not by coordinates.

`<scratch>` below is a folder from `mktemp -d`.

## A temporary web harness

Use the browser tooling the repository or this computer already has. With Playwright, a one-off probe looks like this:

```javascript
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto("http://127.0.0.1:<port>");
await page.getByRole("button", { name: /submit/i }).click();
await page.screenshot({ path: "<scratch>/after.png", fullPage: true });
await browser.close();
```

Do not add Playwright to the project for a probe unless the user asks.

## A temporary CDP harness

For Electron, or a Chromium app started with `--remote-debugging-port=<port>`, connect over the Chrome DevTools Protocol:

```javascript
import { chromium } from "playwright";

const browser = await chromium.connectOverCDP("http://127.0.0.1:<debug-port>");
const pages = browser.contexts().flatMap((context) => context.pages());
let page;
for (const candidate of pages) {
  if (await candidate.locator("<app-root-selector>").count()) {
    page = candidate;
    break;
  }
}

if (!page) {
  console.log(await Promise.all(pages.map(async (p) => ({
    title: await p.title(),
    url: p.url(),
  }))));
  throw new Error("No matching app page found");
}

await page.screenshot({ path: "<scratch>/cdp.png", fullPage: true });
await browser.close();
```

Replace `<app-root-selector>` with a stable marker from this repository, such as the app's root node, a landmark, or a product-specific `data-*` attribute.

## Interaction loop

1. Capture a snapshot or screenshot before acting.
2. Choose a target from the latest page structure.
3. Do exactly one structural action: click, type, press a key, drag, scroll, navigate, or resize.
4. Capture a new snapshot or screenshot.
5. Check that the expected state change happened.
6. Keep the before and after artifacts when the user asked for proof.

## Lower-level protocol work

Use raw protocol calls only when the higher-level browser API cannot do the job. `inspect-runtime` says how to attach here.

- Performance: CPU profiles, traces, paint flashing, the FPS meter, layout shifts.
- Memory: heap snapshots and forced garbage collection for leak investigations.
- Network: request blocking, throttling, disabling the cache, request and response logs.
- Rendering: viewport changes, color scheme emulation, reduced motion, accessibility checks.
- Debugging: console streaming, exception capture, DOM snapshots.

## Picking the page

When several windows or tabs share one debug port:

- Prefer a positive marker for the surface under test, such as an app root selector.
- Add a negative marker to rule out the wrong surface when you need to.
- If no page matches, list the page titles and URLs. Do not guess.

## Rules

- Do not reuse an element reference after a navigation or a change to the page's structure.
- Click by coordinates only right after a new screenshot.
- Keep test data local and disposable.
- Ask the user before you save screenshots or heap snapshots from a workspace with private data.
- Do not copy selectors, ports, or script paths from another repository. Find this repository's own markers.
- Stop dev servers, debug sessions, and temporary browser profiles when you are done.
