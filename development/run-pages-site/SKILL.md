---
name: run-pages-site
description: Launch the pages/ site (Vite dev server or production build) and drive it in a real browser to screenshot it. Use when asked to run, start, preview or screenshot the site, or to check that a change to pages/ actually renders. Covers the two things that fail cold - the required PAGES_RELEASE_INPUT_ROOT env var, and the missing Playwright browser.
---

# Run the pages site

`pages/` is a Vite 7 + React 19 SPA. It reads `gamedata/`, `gamesymbols/` and the
site datasets from the repo root through four custom Vite plugins, so it will not
start without being told where the repo root is.

Two things fail on a cold machine, both with unhelpful errors. Both are handled
below; do not rediscover them.

## 1. `PAGES_RELEASE_INPUT_ROOT` is mandatory

`vite.config.ts` throws outright without it:

```
Error: PAGES_RELEASE_INPUT_ROOT is required for Pages development and builds
```

It must be the **repo root** (the directory holding `gamedata/`), not `pages/`.
Every `dev`, `build` and `preview` invocation needs it. `npm test` does not —
the config skips the check when `VITEST` is set.

```bash
cd /root/CS2_VibeSignatures
PAGES_RELEASE_INPUT_ROOT=$(pwd) npm --prefix pages run dev     # http://localhost:5173/
PAGES_RELEASE_INPUT_ROOT=$(pwd) npm --prefix pages run build   # -> pages/dist
```

Run the dev server in the background and wait for its banner rather than
sleeping a fixed time:

```bash
cd /root/CS2_VibeSignatures/pages
PAGES_RELEASE_INPUT_ROOT=/root/CS2_VibeSignatures nohup npm run dev > /tmp/dev.log 2>&1 &
until grep -q "Local:" /tmp/dev.log; do sleep 2; done
```

Vite is ready in ~160 ms, but the first page load compiles on demand — give a
route 1–2 s after `networkidle` before screenshotting, and ~2.5 s for
`/symbols` and `/game-data`, which fetch and parse the published datasets.

## 2. No browser is installed

`@playwright/test` is a devDependency but `~/.cache/ms-playwright` is empty on a
fresh clone. Install just chromium (~114 MB):

```bash
cd /root/CS2_VibeSignatures/pages && npx playwright install --with-deps chromium
```

Import from **`@playwright/test`**, not `playwright` — the bare package is not
installed, and a script outside `pages/` cannot resolve either. Put the driver
inside `pages/` and delete it afterwards.

## Routes

They are not the directory names. `appViews.ts` explains why: the built site
serves `gamedata/`, `gamesymbols/`, `diagnostics/`, `badge/` and `assets/` at the
root, so a route may not share one of those names.

| View | Path |
|---|---|
| Overview | `/` |
| Find a symbol | `/symbols` |
| Game data | `/game-data` (**not** `/gamedata`) |
| Check my file | `/check` |
| Analysis runs | `/analysis` |
| Live runs | `/runs`, `/runs/:runId` |
| Words | `/words` |

Only the **live** run pages are behind the connection gate (`ApiGate` in
`AppShell.tsx`); without a backend they render "Connect to the local progress
API" instead of content. Everything else, `/analysis` included, reads published
datasets and renders standalone — `/analysis` shows the run that produced the
newest build from `diagnostics/<build>.json`. Verified by loading all seven.

## Driver

```js
// pages/shot.tmp.mjs — delete when done
import { chromium } from '@playwright/test'

const OUT = '/tmp/shots'
const browser = await chromium.launch()
const ctx = await browser.newContext({ viewport: { width: 1440, height: 1024 } })
// Theme is read from localStorage by a pre-paint script in index.html, so it has
// to be set before the document runs, not toggled after load.
await ctx.addInitScript(() => { try { localStorage.setItem('cs2vibe.theme', 'light') } catch {} })
const page = await ctx.newPage()

const errors = []
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()) })
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`))

for (const [path, file, wait] of [['/', 'overview.png', 1200], ['/symbols', 'symbols.png', 2500]]) {
  await page.goto(`http://localhost:5173${path}`, { waitUntil: 'networkidle' })
  await page.waitForTimeout(wait)
  await page.screenshot({ path: `${OUT}/${file}` })
  console.log(file, await page.title(), (await page.locator('body').innerText()).slice(0, 120).replace(/\s+/g, ' '))
}
console.log(errors.length ? 'ERRORS: ' + errors.join(' | ') : 'no console errors')
await browser.close()
```

```bash
cd /root/CS2_VibeSignatures/pages && node ./shot.tmp.mjs
```

**Look at the screenshots.** Printing the body text is a liveness check, not a
verification — it proves React mounted, nothing about how the page looks.

## Shoot both themes

`--accent` and several status colours differ between them, and the light theme is
where contrast breaks: a token that passes on the near-black ground can fail on
white. A light-theme regression is invisible to `npm test`, because the tests
query by role and text and an unreadable colour still matches. Always shoot both.

Theme is `document.documentElement.dataset.theme`, seeded from
`localStorage['cs2vibe.theme']` by the inline script in `index.html`; anything
other than `"light"` resolves to dark.

## Afterwards

```bash
pkill -f '[v]ite'                    # the dev server does not stop on its own
rm -f pages/shot.tmp.mjs            # never commit the driver
```

`pages/dist` is gitignored. Nothing else in this repo runs Vite, so matching on
it is safe — do **not** widen it to a bare `pkill -f node`.

Two traps in the stop command, both of which cost a run:

- **Bracket the pattern, and stop in its own call.** `pkill -f vite` matches the
  shell that is running it, because that shell's own command line contains
  "vite" — it kills itself with exit 144 before the next command runs. `[v]ite`
  matches "vite" but not the literal text `[v]ite`. That only holds while the
  same command line does not also say `vite` elsewhere, so never put the
  `pkill` and an `npx vite ...` start in one Bash call.
- **One dev server per `node_modules`.** To compare against another checkout
  (a `git worktree` of `HEAD`, say), do not symlink its `node_modules` and run
  both servers at once: they share `node_modules/.vite`, each re-optimizes the
  deps under the other, and the page goes blank with
  `504 (Outdated Optimize Dep)` in the console. Run them one after the other,
  each started with `--force`.

## Checks that are not this

- `npm test` (vitest, ~150 tests), `npm run lint` and `tsc -b` need no browser and
  no env var. They pass on markup that renders illegibly, which is the whole
  reason to drive the real thing.
- `npm run verify:gamesymbols` and `npm run verify:gamedata` check the **built**
  `dist/` byte-for-byte against the repo's data; run a build first.
