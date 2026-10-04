---
name: browser-automation
description: Use for browser automation (QA, element interaction, screencapture/snapshot, network capture) or to work across the user's logged-in accounts, apps, memory, and browsing history.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before any browser automation action (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/browser-automation.md`

# Browser Automation

Browser automation tools (see `<project-root>/docs/browser-automation.md`) provide agent-driven and REPL-driven browser control for complex tasks across user's logged-in accounts, cookies, websites, SaaS tools, and browsing histories.

## Choose the Surface

- **Browser exec** (autonomous agent): spawns an agent session like a subagent. Use for whole-task delegation across logged-in accounts, apps, memory, browsing history. Poll and give user status updates every ~60 seconds — the user can't see the CLI background.
- **Browser REPL**: persistent ES2023+ JS REPL with Playwright-compatible, low-level browser interaction. Use for direct evidence, downloads, screenshots, exact verification, deterministic UI steps, sensitive logged-in work. Top-level `const`/`let` bindings persist — use fresh variable names.

Both open ephemeral sessions. Use interactive PTY for CLI commands — session deleted when CLI exits. Inspect current CLI usage before running (see `<project-root>/docs/browser-automation.md`).

## REPL Globals

`page` (current Playwright-like `Page`), `tabs`, `listBrowserTabs()`, `attachBrowserTab(targetId)`, `attachActiveBrowserTab()`, `getTabByTargetId(targetId)`, `openTab(url)`, `closeTab(tab)`, `snapshot(page, options?)` → `{ tree, diff }`, `annotatedScreenshot(page)`, `page.screenshot()`, `page.pdf(options?)` (save under `./artifacts/`), `fetch(url)` (cookie-bearing HTTP; same-origin/trusted GET/HEAD only), `fs`, `path`, `Buffer`, `sleep`, `display`, `pwd`. Use `console.log()` to return values.

## Open Browser Tabs

`browser repl` starts neutral — don't assume `page` is the user's current tab. When the user mentions a current/open page or specific tab, inspect first:
```js
const openTabs = await listBrowserTabs();
console.log(openTabs.map((tab) => ({ targetId: tab.targetId, active: tab.active, title: tab.title, url: tab.url })));
```
`attachActiveBrowserTab()` for current/active page, `attachBrowserTab(targetId)` for specific tab. After attaching, read with `snapshot(page, { interactive: true })`. Only `openTab()` when no relevant open tab exists or user explicitly asks.

## Snapshot

ALWAYS use `snapshot()` as the primary way to read a webpage. Returns compact accessibility tree with unique ref IDs (`e12`, `f1e1`). Tree includes page title, URL, child-iframe contents, and off-viewport elements. Options: `interactive`, `showHidden`, `ref` (e.g. `"e31"`), `selector` (CSS, e.g. `[role="dialog"]` — not `"dialog"`).

- Ref IDs are virtual locator IDs, not DOM properties. Safe to pass to `page.locator('e31')`. NEVER mix into CSS selectors.
- Each new snapshot invalidates earlier ref IDs — take a new snapshot after each action. Save as `const s1`, `const s2`, etc.
- Start with `tree`. After an action, ALWAYS print `diff`.
- NEVER guess ref IDs, selectors, page content, or snapshot size. NEVER truncate with `substring()`, `slice()`, `split()`.

**Reading escalation:** `snapshot(page, { interactive: true })` → `snapshot(page)` → wait + snapshot if still changing → `annotatedScreenshot(page)` (bounding boxes with ref IDs) or `page.screenshot()` (raw visual). Avoid `page.content()`/`page.evaluate()` unless you know the exact selector.

## Navigation and Actions

- Use Playwright APIs through `page`. ALWAYS use `openTab()`/`closeTab()` for tab management — NEVER `page.context().newPage()` or `page.close()` (memory leaks).
- NEVER guess URLs (well-known destinations like Google/YouTube excepted). Use locator actions with ref IDs over `page.evaluate()`.
- Pack action + snapshot in one tool call when next step doesn't depend on new state. Split when next action depends on updated refs.
- Treat action as unconfirmed until fresh snapshot shows expected state. If state unexpected, suspect missed/stale/wrong-target action before inferring site-specific requirements.
- When interaction changes page/persisted state, treat result as evidence of what the site accepted. Recheck only on concrete contradiction, stale snapshot, or unchanged state.
- `openTab()` and `click()` already wait for interactivity/DOM stability. NEVER add redundant `sleep()` after navigation/action — use `sleep()` only when snapshot shows page still transitioning.
- No scroll needed — snapshot includes off-screen elements, click scrolls to targets.

## Forms, Autofill, and Login

Prefer available autofill paths for autofillable forms (ID/PW, email, payment, address). If autofill doesn't complete, inspect updated page with fresh snapshot and continue manually. **ASK USER AS LAST RESORT** if you cannot do it or find the information.

## Downloads

`fetch()` only for same-origin or trusted direct-download GET/HEAD URLs on the current page. No mutations, no cross-origin credential forwarding, no unverified page-text URLs.
```js
await fs.mkdir("./artifacts", { recursive: true });
const href1 = new URL(downloadUrl, page.url()).href;
const res1 = await fetch(href1);
if (!res1.ok) throw new Error(`download failed: ${res1.status}`);
await fs.writeFile("./artifacts/download.pdf", Buffer.from(await res1.arrayBuffer()));
```
For download buttons, blob URLs, redirects, or POST-backed downloads, use browser download handling. Verify `download.path()`; use `download.saveAs("./artifacts/name.ext")` only when you need an artifacts copy.
```js
const downloadPromise = page.waitForEvent('download');
await page.locator('button.export').click();
const download = await downloadPromise;
console.log({ filename: download.suggestedFilename(), downloadPath: await download.path(), size: (await fs.stat(await download.path())).size });
```
`fs` cannot browse real `~/Downloads`. After `download.path()`, the file is readable for verification in the current REPL session. In one-shot `browser repl "..."`, verify inside the same command — session closes afterward. After downloading PDFs/documents, extract facts using local document/PDF tools. Report only facts found in the file or confirmed on the page.
