---
name: tutorial-video
description: Produce narrated product tutorial videos automatically — script, OpenAI voice-over, a real recording driven by Playwright (web app, browser-extension popup) or the iOS simulator (mobile app), cursor/tap highlights, captions, ducked music, title and end cards, 1080p mp4. Use when the user wants a tutorial, demo, walkthrough, onboarding or sales video of an app, or wants to re-record one in another language.
---

# Tutorial videos

Script → voice per scene → recording that holds each scene exactly as long as its narration → ffmpeg. No manual editing. Proven on a web portal, a Chrome extension popup and an Expo app.

## Ground rules (ask first, never assume)

- **Real actions only on a test account**, and only after the user says so. Recordings click for real (clock in, confirm, approve). Prefer a stage with mocks (mode B) when the account must stay untouched.
- **Never show credentials.** The user signs in off camera (the driver waits for it). Blur e-mails (overlay does it), pixelate account footers in screenshots. Dev logs may print inputs (passwords): never grep them into the conversation; redact log files.
- **Language = native voice**, not just translated text: OpenAI `gpt-4o-mini-tts` keeps an American accent unless the instruction says so. Working setup (German): voice `marin` + instruction "Sprache: Deutsch. Sprich wie eine deutsche Muttersprachlerin aus Deutschland, klares Hochdeutsch … kein amerikanischer Akzent … Speak German as a native speaker; no American accent." Let the user pick by ear (generate 4–6 voice samples of one sentence, publish them with audio players).
- Look at frames before calling a take done (contact sheet of 6–8 frames at scene midpoints).

## Layout in the project

```
<app>/tutorial/
  script.<lang>.json   title, subtitle, endTitle, endSubtitle, brand {color, logo, logoOnDark}, voice, scenes [{id, chapter, vo}]
  record.mjs           project-specific: what each scene does (copy a template)
  stage.html           mode B/C only (copy a template)
  out/                 git-ignored: vo/, frames/, timeline.json, the mp4
```

Scripts live in this skill (`scripts/`), templates in `templates/` (generic examples: replace selectors, labels and routes). Run scripts from a folder whose `node_modules` has `playwright` (or set `PLAYWRIGHT_FROM`).

## Workflow

1. **Script** (`templates/script.example.json`): 6–10 scenes, one sentence or two each (≈6–12 s spoken). Scene ids drive the recorder's `ACTIONS`. Intro/outro are cards. Write the narration in the target language as a native would; captions show the same text.
2. **Voice**: `node <skill>/scripts/voice.mjs <lang> <tutorial-dir>` → `out/<lang>/vo/*.wav` + `vo.json` (durations). Key: `OPENAI_API_KEY` from env, nearest `.env` upwards, or keychain `openai-api-key`; `VOICE=say` for a free macOS draft. Silence at both ends is trimmed.
3. **Record** (pick the mode):
   - **A · Web app, signed in** — `scripts/driver.mjs <workdir> <sign-in URL> <signed-in path regex>` opens Chrome for Testing headed; the user signs in; then drop command modules into `<workdir>/cmd/` (recon → off-camera reset → `templates/record-web.mjs`, e.g. `export default async (a) => (await import("/abs/path/record-web.mjs")).default(a)`). Crop the headed browser's white right/bottom strip at render: `TUTORIAL_CROP=1896:1066:0:0`. The recorder injects `scripts/overlay.js` (cursor, ripple, ring, chapter, captions, cards; fill `__BRAND__`, `__LOGO__` with inline SVG markup, `__END_TITLE__`, `__END_SUBTITLE__`) and captures with CDP `Page.startScreencast`.
   - **B · Extension popup / UI with mocks** — build a `stage.html` (a browser-window frame at 1920×1080, the real built popup in an `<iframe>` from the same local server, a toolbar icon with badge, captions, cards, cursor) and a `demo-mock.js` loaded before the popup bundle that answers `chrome.*` (storage, runtime.sendMessage, getManifest) and the API (`window.fetch` → canned, stateful answers) and exposes a movable clock (`Date.now` override, `__demo.setNow(iso)`). Record it like mode A (CDP screencast, sync flash) with the *headless shell*. Deterministic and touches no account. Use CSS `zoom` inside the iframe (not a transform) so Playwright's coordinates stay right; highlight inside the iframe with an outline class.
   - **C · iOS app** — `templates/record-sim.mjs`: `simctl io recordVideo` + taps by accessibility label via argent (`describe` / `gesture-tap`). Then `scripts/render-phone.mjs` composes the phone into `templates/stage-phone.html` with chapter + captions beside it and a ring on every tap.
4. **Render**: A/B `TUTORIAL_NAME=x node <skill>/scripts/render-frames.mjs <lang> <dir>`; C `TUTORIAL_NAME=x node <skill>/scripts/render-phone.mjs <lang> <dir>`. Output: H.264 1080p30, AAC, -16 LUFS, pad ducked 16–23 dB under the voice.
5. **Review** a contact sheet, fix, re-take (reset state off camera first), then publish (artifact with `<video>` players for the user; copy mp4 + poster where the product page needs it).

## Gotchas that cost hours

- **Frame size**: full Chrome's new headless crops the screencast to 993 px high — use the *headless shell* (`ms-playwright/chromium_headless_shell-*/…/chrome-headless-shell`) for B; headed Chrome for Testing with `deviceScaleFactor: 1.25` on a 1536×864 viewport gives ~1920×1080 for A (render crops/scales to exactly 1920×1080).
- **Sync**: A/B start with a magenta flash; render finds the first frame after it. C: `recordVideo` writes frames only on screen changes — the file starts at the spawn time (`recStart`) but **ends at the last change**, so never use `stop − duration`.
- **Waiting**: dev servers compile on first visit (5–15 s). Wait for real content (`locator.waitFor`), set `page.setDefaultTimeout(9000)` while recording so a missing element skips instead of freezing 30 s; highlights must never block (`boundingBox({timeout})` in try/catch).
- **Selectors**: sidebars often exist twice (desktop + hidden mobile sheet) → `a[href*="…"]:visible`. Disabled rows (locked weeks) → `:not([disabled])`. Groups may need expanding first. Do a read-only recon module (buttons, dialogs, checkbox states, screenshot) before scripting a scene.
- **Dialogs** in real apps often need extra input (a reason ≥3 chars, a "notices checked" box, times per day). Inspect them off camera; never tick a box you have not read (one take ticked "did not work this day").
- **State between takes**: every real take changes data. Write an off-camera `reset` (end the running shift, confirm, close dialogs) and run it until the start state is back. "Später"/"later" dismissals may not persist across navigation.
- **Overlay**: `addInitScript` accumulates per take — the overlay removes older roots and the newest wins. Logos as `<img>` (path or data:) can be blocked by the app's CSP → inline SVG markup. Hide dev-only UI (TanStack devtools button, Expo tools FAB).
- **Expo dev client FAB** (gear in every screenshot): `xcrun simctl spawn <udid> defaults write <bundle-id> EXDevMenuShowFloatingActionButton -bool NO`, relaunch. Use the installed app's real bundle id (`simctl listapps`).
- **Deep links** on a deep navigation stack lag or do nothing (modal open) → navigate in-app (back, tap rows); it also looks more natural.
- **Login detection** on the simulator: don't guess from pixels (it tapped during the user's password entry); wait for the app's first signed-in request in the Metro log.
- **ffmpeg 8** removed `-filter_complex_script` → `-/filter_complex <file>`. Odd widths break yuv420p → scale/crop to 1920×1080.
- **Lockfiles**: adding tooling to a pnpm workspace can re-resolve shared deps — check `git diff pnpm-lock.yaml | grep '^-[^-]'`.

## Other languages

Copy `script.de.json` → `script.<lang>.json`, translate as a native writer (not word order of the source), set the voice instruction for that language, run voice + render; re-record only when the UI language must change too.
