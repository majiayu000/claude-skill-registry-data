---
name: record-demo-video
description: Record a narrated video of a feature running in the local dev app, for a PR or a stakeholder. Drives a headless Chrome over the DevTools Protocol so clicks and keystrokes are real, captures frames, and encodes an mp4 with no extra tooling installed. Use when the user asks to "record a video", "make a demo", "show this working", or wants a screen recording of a change.
---

# Record a Demo Video

Produce a short video of a feature working in the running dev app: real page, real LiveView, real
response times. Not a mockup and not a reenactment, because a demo that does not actually exercise the
code is worse than no demo.

Pipeline: **headless Chrome driven over CDP** → **one PNG per frame on a timer** → **mp4 via
AVFoundation**. Everything needed is already on this machine.

## Why CDP and not the Browser pane

The in-app Browser pane (`mcp__Claude_Browser__*`) is fine for *looking* at a page, but it cannot drive
this reliably:

- Its synthetic clicks do not always fire `phx-click`. When the pane is hidden, a click can land as a
  focus with no submit, and `element.click()` / `new Event('input')` from `javascript_tool` races
  LiveView's re-render and silently no-ops.
- **It cannot screenshot at all unless the pane is on screen.** In a session where it is not,
  `computer{action:"screenshot"}` fails with "the Browser pane is not displayed, so the page is not
  compositing frames" and no amount of re-fronting the tab fixes it. Headless Chrome over CDP is
  never subject to this — do not fall back to the pane when it happens, and do not go hunting for a
  way to display it.
- It has no way to write frames to disk, so there is nothing to encode.

It also cannot hold the app's session cookie: the pane sets its own `httpOnly` session cookie on the
first page load, and `document.cookie` from `javascript_tool` cannot overwrite an `httpOnly` cookie,
so every attempt to sign it in by hand lands back on the login page. `record.sh` installs the cookie
through CDP, where that restriction does not apply.

CDP's `Input.dispatchMouseEvent` / `Input.dispatchKeyEvent` produce **trusted** events, so LiveView
reacts exactly as it does for a real user, and `Page.captureScreenshot` gives frames as files.

## What is available (checked, so do not re-litigate)

- **No** ffmpeg, ImageMagick, chromedriver, playwright, or puppeteer. Do not install any: the pipeline
  below needs none of them, and installing tooling on the user's machine needs their say-so.
- **Node** has a global `WebSocket`, so CDP needs zero dependencies.
- **Swift + AVFoundation** (Xcode is installed) encodes PNG frames to H.264 mp4.
- **Chrome** is at `/Applications/Google Chrome.app`. Always launch it with a scratch
  `--user-data-dir`, never the user's real profile.

## Steps

### 1. Get the dev app running and seeded

The dev server must already be up. `record.sh` finds the port the way the app does: `PORT` from the
environment, else the one in this worktree's `.env.worktree`, else 4000 — so **in a worktree it
drives that worktree's app, not whatever is on 4000**. It refuses to record if what answers is not
Spendable. Start the server from the same checkout you are recording, or the video shows code you
did not write.

Seed whatever the demo needs, and **write a reset script** that puts the data back to the starting
state. Recording is iterative: expect three or four takes, and every take must start from the same
place. Prefer a direct `Repo.insert!` / `Repo.update_all` for setup so it is fast and does not run the
side effects the demo is about to show.

Match the requirements' worked example if there is one. A demo whose numbers match what was asked for
is much easier to review against.

### 2. Write the scenario

Copy [scripts/example-scenario.mjs](scripts/example-scenario.mjs) into the scratchpad and rewrite the
steps. It is plain JS against the session returned by
[scripts/driver.mjs](scripts/driver.mjs):

| call | what it does |
| --- | --- |
| `demo.login({name, value})` / `demo.goto(path)` | authenticate and navigate, before recording starts |
| `demo.startCapture()` | begin the frame timer |
| `demo.step(text, ms)` | set the caption and hold, so there is time to read it |
| `demo.click(jsExpression)` | trusted click at the element's centre (`{at: 'left'}` for a date field) |
| `demo.type(text)` / `demo.typeDate(sel, digits, expected)` | real keystrokes |
| `demo.expect(js, desc)` / `demo.refute(js, desc)` | assert the state the narration claims |
| `demo.finish()` | stop capturing, return the frame count |

Selectors are JS evaluated in the page, so when nothing stable identifies an element, find it by text:
`[...document.querySelectorAll('button')].find(b => b.textContent.includes('Save'))`.

**Assert what you narrate.** Every claim the captions make should have an `expect` / `refute` behind
it, so a bad take fails loudly instead of producing a confident, wrong video.

### 3. Record and encode

```bash
zsh -c '.claude/skills/record-demo-video/scripts/record.sh <scenario.mjs> <output.mp4> [user]'
```

It launches its own Chrome, mints a session cookie, runs the scenario, encodes, and kills Chrome on
exit. `DEMO_FPS` (default 8) and `DEMO_FRAME_DIR` override the defaults.

The frame timer runs at ~120ms, which lands near **8fps**, so encoding at 8 plays back at real speed.
If you change `frameIntervalMs`, change the fps to match or the video will run fast or slow.

### 4. Check the frames before believing the video

Read a few frames with the Read tool: the opening state, each moment a caption makes a claim, and the
final state. They are PNGs, so you can see them directly. This is also how you catch styling bugs the
tests cannot — a form error rendering white and indented instead of red and flush left, an amount
rendering as `1234.5`.

Then confirm the side effects landed in the database. The video shows the UI; only a query proves the
write.

### 5. Deliver it

`SendUserFile` with `display: "render"`, plus a copy somewhere durable like `~/Desktop`.

**Do not commit the mp4** and do not add it to the repo. Keep the video, the frames, and the scenario
in the scratchpad.

## Putting it on the PR

**GitHub cannot attach video through the API.** There is no REST endpoint for issue or PR attachments,
and `gh` cannot upload media. The `github.com/user-attachments/assets/...` URLs that render as an inline
player are minted only by the web upload. Say that plainly instead of trying to work around it — and
never work around it by committing the mp4, pushing it to an orphan branch, or uploading it anywhere
the app owns. Committing it bloats the git object store permanently.

So the video reaches the PR only by hand: **offer it, do not assume it.** Hand the user the absolute
file path, keep the PR in draft until they have dragged it into the GitHub web editor, and let them
paste the resulting `user-attachments` URL back if you need to reference it. If they would rather not,
say in the PR description in one line that a demo was recorded and where it is, and move on.

## Gotchas that cost real time

- **Never type a password, and never drive Google's OAuth screen.** Authenticate with the session
  cookie [scripts/session_cookie.exs](scripts/session_cookie.exs) mints; `record.sh` handles it, and
  the scenario never needs a `login` step of its own. The dev database must already have a user —
  sign in once in a real browser if it does not, or create one through `Accounts` with `mix run`.
- **A demo of a flow that starts outside the app still starts inside the browser.** An OAuth consent
  screen, a callback, an email link: `goto` the URL the outside system would have sent the user to.
  Point any redirect at a real page of the app rather than a port with nothing listening, so the
  video ends on the product instead of Chrome's error page.
- **Date inputs keep segment focus.** Typing a second date into the same field continues in whichever
  segment was last edited, so the digits pile into the year and overflow it (`07/31/275760`). Walk back
  with three `ArrowLeft` presses first. `typeDate` does this and asserts the resulting value.
- **A `<select>` is a change event, not a click.** Set `.value` and dispatch a bubbling `change`, or
  LiveView never sees it.
- **A caption is not app UI.** Style narration as an obvious overlay bar. Never let it be mistaken for
  something the app renders.
- **Screenshots can land mid-navigation.** The capture loop swallows those; do not make it fatal.
- **Kill Chrome when done**, and stop any dev server you started that the user did not ask for.
- Dev data you mutate while recording is the user's real budget. Tell them what state you left behind.
