---
name: verify-puzzle-game
description: 'Run and verify this repo''s games for real: which of them build and which are single files, how to drive a game in the browser pane, how to bot-play a full run to check balance, and the gates to clear before calling it done. Use when asked to run, start, preview, screenshot, test or verify Payload or Ledger Lane, or to confirm a change actually works rather than only reading right.'
---

# Verifying the games

## Payload builds; everything else is a single file

This used to say there was no build step. That stopped being true when Payload
was ported to React and TypeScript.

```
src/                 Payload's source: pure engine in src/game, views in src/ui
app/index.html       Payload's entry
public/index.html    The Arcade hub
public/ledger.html   Ledger Lane, a routing puzzle, still one self-contained file
public/payload.html  The superseded single-file Payload. Kept only as the
                     reference src/game/__tests__/parity.test.ts diffs against.
                     It is not the game the hub links to. Do not verify against it.
dist/                THE SITE. Built from the above, gitignored. This is what
                     tools/serve.js serves and what Netlify publishes.
```

So:

```bash
npm ci                       # once
npm run build                # public/ + app/ -> dist/
node tools/serve.js          # serves dist/ at http://localhost:8000
```

`npm run dev` gives Vite with hot reload at :5173, but the service worker, the
install prompt and anything reading `public/`'s sibling files need `tools/serve.js`.

**Rebuild before you look.** `dist/` is stale until `npm run build` runs, so a
change you just made to `src/`, or to anything in `public/`, will not be on
screen. This is the single most common way to conclude a fix did not work when
it did.

## Driving a game from the browser pane

Payload needs the server, because it loads hashed bundles and registers a
service worker:

```
mcp__Claude_Browser__navigate → http://localhost:8000/app/
```

Ledger Lane is still one file, so `file://` works for it straight from source:

```
mcp__Claude_Browser__navigate → file:///C:/Users/Gagan/Desktop/puzzle-game/public/ledger.html
```

**The service worker will serve you a stale build.** It caches the app shell, so
after a rebuild you can reload and still see the old code. Clear it first:

```js
const rs = await navigator.serviceWorker.getRegistrations();
await Promise.all(rs.map(r => r.unregister()));
const ks = await caches.keys();
await Promise.all(ks.map(k => caches.delete(k)));
location.reload();
```

Two traps that will waste your time.

Files outside the project folder open as a static snapshot with JavaScript
disabled, and files served from a `data:` URL have `localStorage` disabled, where
reads throw `SecurityError`. So always test from a path inside the repo, and wrap
anything touching `localStorage` in try/catch. Payload's daily records already
are: a storage failure must degrade to a playable run without persistence, never
to a crash. Verify that path rather than assuming it.

The browser pane throttles background timers. When the pane is hidden,
`requestAnimationFrame` never fires at all and `setTimeout` is clamped to about a
second, so any measurement built on either will hang or report nonsense. Front the
tab first, or measure the pure function in Node instead. Three consecutive
attempts to time the placement sweep through a hidden pane produced garbage before
this was written down.

Prefer `javascript_tool` over clicking for anything multi-step: clicks race the
drop animations, and a scripted run gives you exact numbers back. `computer` clicks
also wait for page stability, which an animation prevents, so they time out.

## Bot-play a full run, which is how balance gets checked

Never claim a difficulty is tuned because the numbers look right. Play it.

Drive the React build through accessible names, not class names. They are stable,
they are what a player relies on, and asserting through them checks the
accessibility surface at the same time. Class names are Tailwind output and change
whenever the styling does.

```js
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const btn = (t) => [...document.querySelectorAll('button')]
  .find(b => b.textContent.trim() === t);
const over = () => !!document.querySelector('[role=dialog]');

for (let i = 0; i < 80 && !over(); i++) {
  // Draft: take the highlighted best placement the preview already computed.
  const skip = btn('Skip');
  if (skip) {
    const best = [...document.querySelectorAll('[aria-label^="Row "]')]
      .find(c => /Best placement/.test(c.getAttribute('aria-label')));
    best ? best.click() : skip.click();
    await sleep(150);
    continue;
  }
  const bp = [...document.querySelectorAll('h2')]
    .find(h => h.textContent.includes('blueprint'));
  if (bp) { bp.parentElement.querySelectorAll('button')[0].click(); await sleep(120); continue; }

  const drops = [...document.querySelectorAll('[aria-label^="Drop a marble"]')];
  const pick = drops.find(d => /best column/.test(d.getAttribute('aria-label'))) || drops[2];
  if (pick && !pick.disabled) { pick.click(); await sleep(1100); continue; }
  await sleep(250);
}
const dlg = document.querySelector('[role=dialog]');
dlg.textContent;
```

Two bots, two questions. A lazy bot, skipping every draft and dropping into an
empty column, must lose; if it wins, the quota curve is too soft. A competent bot,
the one above, must win Easy and get close on Hard. Both were used to tune the
current numbers, so keep using both when you touch quotas, drops or part maths.

Bots systematically underuse Prism catcher columns and Spring loops, so they read
a little pessimistically against a thoughtful human. Leave that headroom in.

One gotcha when scripting: match against a specific element rather than
`document.body.innerText`. Searching the whole page for "JAM" once matched the
compendium instead of the jam banner and reported the opposite of the truth.

## Mobile

Games are mobile-first. Test at phone size, and reset when you are done or every later
screenshot is misleading:

```
resize_window → preset "mobile"      # 375x812
resize_window → preset "desktop"     # ALWAYS reset afterwards
```

What to check on mobile: the board sits above the fold, the end-of-run dialog is
fully inside the viewport at `scrollY === 0`, and tap targets are at least 44px.
Assert those rather than eyeballing them:

```js
const grid = [...document.querySelectorAll('.grid.grid-cols-5')].pop().getBoundingClientRect();
({ fits: grid.bottom <= innerHeight, bottom: Math.round(grid.bottom), vh: innerHeight });
```

The board currently ends at 761px of an 812px viewport. Getting all six rows above
the fold took deliberate work, so re-check it after anything that adds vertical
space.

## Gates before you call it done

1. `read_console_messages` with `onlyErrors: true`, and it must be clean. Stale
   service-worker entries show up here as "unknown error occurred when fetching
   the script"; clear the worker before believing them.
2. A full run played to its end screen, in the mode you changed.
3. If you touched daily or seeding: confirm the same day gives identical drafts
   across reloads, and that Easy and Hard differ from each other, since they are
   salted apart.
4. If you touched quotas or part maths: both bot runs, reported with real numbers.
5. `npm test` and `npm run typecheck`.
6. Temp test files deleted, and `git status` clean apart from intended changes.

## Deploying

Merging to `main` builds and publishes on its own; PRs get a Netlify deploy
preview whose URL is worth handing over when a change needs to be felt rather than
described. Nothing needs deploying by hand.

`public/payload.html` is the superseded single-file build, kept only as the
parity reference. Do not edit it to change the game, and do not verify against it.
