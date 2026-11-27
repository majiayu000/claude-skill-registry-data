---
name: ui-review
description: "Screenshot a web app at phone and desktop size, then design-critic review. Use after any UI change, before the PR."
---

# UI review

**Every UI change** (moved here from `CLAUDE.md`, S11a): the project's `DESIGN.md` first (none: `frontend-design` and `impeccable`, one clear direction; art direction before any screen, `roles/designer.md`, its `## Bar` is what the Tester checks), nothing from `ui-review/SLOP.md`; screenshots at 390px and 1440px, `design-critic` review, fixes, screenshots in the PR. UI text is German first, English second, static files included.

yskills' lasting likes and dislikes are in `TASTE.md` next to this file, the slop patterns that
fail any screen in `SLOP.md`; the critic gets both with the screenshots and the references.

## 1. Run the app

Start the project's dev or preview server in the background (`npm run dev`, `npm run preview`,
`nuxt dev`...) and note its URL. Prefer a production build (`build` + `preview`) when the change
is about performance or final look. Fill pages with realistic data; an empty page hides problems.
- Chrome as root in the cloud container (shader and audio checks) needs a wrapper with `--no-sandbox` (MyPage, 2026-10-04).

## 2. Shoot

```
node <ui-review skill folder>/scripts/shoot.mjs --base http://localhost:3000 --out .shots / /pricing
```

- The phone size runs as a touch device, and each shot waits for one-shot animations to end.
- Each target is saved as `<page>-phone.png` (390x844 @2x) and `<page>-desktop.png` (1440x900).
- `--full` captures the whole scrolling page, `--only phone|desktop` skips one size,
  `--wait 1500` waits longer for animations or WebGL.
- Absolute URLs are shot as-is: that is how you capture a design reference site.
- Console errors are printed; treat each one as a bug unless you know it is expected.
- Playwright is found in the project, then globally; otherwise install it once with
  `npm i -g playwright && npx playwright install chromium`.
- Keep `.shots/` out of git (add it to `.gitignore`).

For a page behind a login, log in with a throwaway local account; never use or print real
credentials.

## 2b. Load once

Every page must load once per visit. A double load slipped past screenshots once (Yland
2026-10-08: a PWA reloaded itself after every deploy, and the server sent "Loading…" before the
real page), so run this on the production build of any app with a service worker or SSR data:

```
node <ui-review skill folder>/scripts/load-once.mjs http://localhost:8787/ 15
```

It visits three times in one profile (first, second, first after a simulated deploy) and fails
on any second page load. Also open the server's HTML (`curl`): it must already hold the page's
data, not a loading placeholder that the browser fills in a second time. A PWA follows
the `toolbox` skill's PWA row (`registerType: 'prompt'`).

## 3. Review

1. Open every PNG yourself first, next to `design/reference/`. Run
   `node <ui-review skill folder>/scripts/design-check.mjs` in the project; fix what it lists. If the PR changes user-facing text, also run
   `node <ui-review skill folder>/scripts/copy-check.mjs design/COPY.md` (`operator/roles/content-designer.md`).
2. Run `.claude/skills/impeccable/scripts/impeccable detect` on the changed source files (a local
   linter for AI-look anti-patterns, no LLM; scan files, not a URL, because URL scans can't start
   Chromium as root in cloud threads) and check the diff against the
   `web-interface-guidelines` skill. Fix what they flag.
3. Run the `design-critic` agent with the screenshot paths, and tell it to return its findings as
   its final text (a report "delivered as a message" can get lost). Fix every **blocking** finding and
   the cheap **polish** ones, then shoot again.
4. Attach the final phone and desktop screenshots to the PR description.

## 4. Record (when yskills should see it run)

- Web flow: set `video: 'on'` (or `recordVideo` on the context) in Playwright; it records headless.
- Anything with its own window (Electron, a game, a native app): run it on the thread's own virtual
  screen and record it with
  `bash <ui-review skill folder>/scripts/desktop.sh .shots/run.webm <command>`.
  Look at a few frames (`ffmpeg -ss 5 -i run.webm -frames:v 1 f.png`), then attach the WebM to the
  PR or thread. WebM only: the cloud Chromium has no H.264.
