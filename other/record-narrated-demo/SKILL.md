---
name: record-narrated-demo
description: "Record a narrated walkthrough video of a working Mendix app — the human-facing half of the journey/demo pair. Use when asked to demo, show off, or produce a walkthrough recording, after the app's end-to-end journey already passes."
---

# Record a Narrated Demo

Proving a feature works and showing it off are two different jobs, and one script
cannot do both well. This skill covers the second. It assumes the first is done.

| | Stage 1 — journey | Stage 2 — demo |
|---|---|---|
| Script | `journey-runner.js` | `narrated-walkthrough.js` |
| Job | **asserts** | **explains** |
| Gates the build | yes | no |
| Optimised for | signal — no narration, no reading pauses | a viewer — human pace, on-screen narration |
| Verdict lives here | **yes** | **never** |

Both walk the same persona down the same path. The demo reuses the journey's
shape and its OQL-backed data checks, so what it shows on screen is still true —
but the PASS/FAIL judgment stays in the gating runner. A demo that can fail the
build is a test with worse ergonomics; a test that narrates is a demo that misses
regressions.

## Before recording: the journey must exist and pass

Write `journeys/<Module>.journey.json` first — one persona, one path, with
carried state, not a list of page stops. Its canonical definition is
**`skills/journey-proof.md` in `mxcli-project-toolkit`**; do not re-derive the
protocol here. In outline, each step asserts five independent rungs:

1. **Landing guard** — the step's `ready` widget is visible. Without it every
   later assertion silently runs against the *previous* page.
2. **What the screen says** — `textPresent` / `textAbsent`. The backend can be
   correct and the screen can still lie about it.
3. **Ordered spans** — the right microflows fired, in order, plus `mustNotFire`.
4. **Data effects** — row created, association actually set (not null), pointing
   at the *right* seeded value. Three claims, not one.
5. **Outcome** — one query over the final state. Per-step deltas can each be
   right while the net result is wrong.

Every rung is proved falsifiable by re-running with one broken precondition each
(7 mutants — rungs 3 and 4 make two claims apiece) and requiring the *targeted*
check to fail. A rung nobody could break is `UNPROVEN`, which is a **fault**, not
a pass. Verdicts are `PASS` / `FAIL` / `INVALID` and never collapse into each
other: `INVALID` means the instrument did not run, which is a finding of its own.

**Writing the journey first is what makes the demo cheap.** The persona, the
path, and the definition of success already exist by the time you record.

## Seed the data before you record

The failure this skill is most prone to, and it is not subtle. The first real
ContactBook capture was an empty grid reading `0 to 0 of 0` with a column header
rendering as `colActions` — which reads as **a broken app, not a new one**. The
journey passed; the app was live; the recording was worthless.

Before any take:

- **Populate every list the camera will see**, with plausible values — real names
  and amounts, never `test1` / `asdf` / `aaa`.
- **Caption every column and button the camera will see.** A header showing its
  attribute name is the single clearest tell that nobody looked at the screen.
- **Open on something already interesting.** The first thing on screen should be
  a populated state, not an empty one waiting to be filled.

`mxcli` seeds this itself — see [demo-data](../demo-data/SKILL.md). Seeding is
part of recording, not a nicety before it.

## Recording mechanics

The things that decide whether the video is watchable, and whether it looks like
the rest of the catalogue. Each has a reason; none is a style preference.

### Record at a human pace, not the harness's

A cursor moving at test speed reads as **broken**, not fast. The gating runner is
tuned for signal and should stay that way — slow the demo script down on its own,
and leave reading pauses where a viewer would actually need to read.

Two numbers, both from films that were re-cut for being too fast:

- **Hold every screen for `max(caption read time, screen read time)`, floor 2.5s.**
  Caption read time is roughly `words ÷ 3.5` seconds — which is what `narrate.js`
  computes. Screen read time is how long it takes a viewer to *find the thing that
  changed*, and it is always longer than it feels while authoring. `narrate.js`
  knows only the caption; when the screen is the slower of the two — or when a
  narration line is longer than both — pass the measured duration as `holdMs`.
- **About two events per ten seconds.** A click, then its result. Not a click, a
  scroll, a filter and a result — that is four things a viewer is asked to track
  in the time they can follow one.

And three the finished film is measured against, from the video system's
`TONE-AND-SPEED.md` — a product demonstration is **60–120s**, **55–65% voice
density**, **~135 wpm**. Density is the one worth checking early: it is the tail
budget stated as a ratio, and a walk that fills 80% of its runtime with talking
is not a slow film that needs trimming, it is a fast one wearing a slow pace.

### Give the compositor something to draw during pauses

Playwright's video captures only frames the compositor actually produces. A
genuinely idle screen during a reading pause can collapse to almost no video, so
a 5-second pause plays back in a blink and the narration desyncs. Keep something
continuously animating so idle time is recorded *as* idle time.

`narrate.js` does this with a hairline segment sweeping the caption plate's top
edge, on a loop, for the whole take. It used to be a spinning ring, and the ring
had to go for a reason worth keeping in mind whenever this element is redesigned:
the design language has **no rounded corners**, so a ring can only be a spinning
square. The keep-alive has to be expressible in the system's own vocabulary —
here, 1px structure travelling — rather than bolted on beside it. What it must
not become is per-caption: a hold *between* captions still has to produce frames,
so the animation runs continuously and is never keyed to a reveal.

### Record the same walk at desktop and at a real mobile profile

Same steps, same assertions, **nothing simplified for the smaller screen**. A
pass that trims the small-screen steps would report success on an app nobody can
use on a phone. This is the pass that catches layout failures nothing static
sees — an mxcli-built app recorded at 414×896 completed the whole flow while both
DataGrid2 screens were unreadable: eight columns compressed to eight single
characters, headers degraded to bare sort arrows. The app *functioned* on a phone
and was not *usable* on one, and only the mobile recording showed the difference.

**A narrow viewport is not a mobile profile.** Mendix picks its navigation
profile from the **user agent**, not from the window size, so a take that only
shrinks `viewport` films the *desktop* app in a narrow window — the phone profile
is never routed to, and the pass cannot show the thing it exists to find while
looking entirely plausible. Pass the device through `contextOptions`:

```js
const take = await openTake(browser, {
  size: { width: 430, height: 932 },
  contextOptions: {
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) ' +
               'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
  },
});
```

`viewport` and `recordVideo` are set by `openTake` itself and win over anything
in `contextOptions`, because both are load-bearing for the cut — a device preset
carrying its own `viewport` would silently letterbox every take.

Also worth knowing before you read a mobile take as a layout bug: **a Mendix page
carries its own layout, and the layout names the navigation profile.** The Phone
profile controls the home page and the menu; it does not re-skin the pages a user
reaches afterwards. A phone user routed to a page built on a desktop layout gets
the desktop frame whatever profile routed them there — measured at 430×932, a
232 px rail on a 430 px screen with the row's action laid out 42 px past the
right edge. That is a real defect and the take is right to fail on it, but the
fix is per-page layouts, not a theme tweak.

### `recordVideo` needs a Node script, not `playwright-cli`

`mxcli verify`'s browser checks run bash scripts against a persistent
`playwright-cli` session (see [test-app](../test-app/SKILL.md)). Video is a
**context-creation** option, so the demo script owns its own browser context via
the Playwright library instead. That is a second reason Stage 2 is a separate
script rather than a flag on the gating runner.

Browser and headless-shell setup is [test-app](../test-app/SKILL.md)'s — do not
duplicate it here. Data assertions under the demo use
[verify-with-oql](../verify-with-oql/SKILL.md). Boot the app with
[run-local](../run-local/SKILL.md) (`mxcli run --local`); for a still-image set
rather than a video, `--screenshot` with repeated `--screenshot-url` already does
that without any script.

### The overlay ships with this skill: `narrate.js`

`narrate.js` sits beside this file and is copied into the project along with it.
Require it from the demo script rather than writing another one — the last three
projects each re-derived their own Stage 2 from this page's prose, which is why
no two demos look alike.

It asserts nothing and holds no selectors, so it is the same file in every
project:

| | |
|---|---|
| `configure({ zoom, accent, ground, font })` | tokens and the **zoom take.js is using** — see below; call it before anything else |
| `say(page, text, step)` | caption, held for `max(2500, words * 280)` ms — a fixed hold rushes long lines and stalls on short ones. Refuses a caption containing a tofu glyph |
| `point` / `unpoint` | pulsing outline around an element's rect, **drawn** — a real click ring would move the cursor and the page under it. The film's one accent event |
| `clickSlowly` | scroll in, mark, beat, click: a cursor that arrives and clicks in one frame reads as a glitch |
| `typeSlowly` | per-key typing, then commit |
| `bringIntoView` | includes **horizontal** scroll (`inline: 'center'`), for a grid whose action sits past a phone's right edge |
| `checkOverlay(page)` | the design rules that are measurable in the page, as a check that **throws**. Run by `install()`, so it costs nothing to remember |

The sweeping hairline is the compositor fix described above, not decoration and
not a loading indicator — it is what keeps a reading pause from collapsing to no
frames. Removing it silently breaks the pause *and* any audio timed against it.

What stays per-project is the walk itself: the persona, the steps and the
selectors (`narrated-walkthrough.js`). Only the library is shared.

### The overlay is the film's furniture, so it is on the design system

A capture is most of a Type A film's runtime, and the caption plate is the only
thing the film draws over it. Furniture that disagrees with the frames it cuts
against reads as two designs — so the overlay is built to
`video-system/DESIGN-LANGUAGE.md`, not to whatever looked reasonable in a
browser. What that changed, and why each one is a defect rather than a taste:

- **One accent, and it is the pointer.** The plate carries none. Two accented
  things competing is the fastest way a frame stops working, and the accent's
  job here is *where to look*.
- **The plane is flat** — no shadow under the plate, no corner radius on the
  plate or the pointer, no glow. Depth is the hairline at the plate's top edge
  and the value step to the app's ground. The pointer pulses on **opacity**,
  because the old expanding `box-shadow` was a glow.
- **No system font stack.** `'Segoe UI'` and friends do not exist on a clean
  build machine and fall back to DejaVu Sans with nothing saying so, so the
  plate now inherits the **app's own computed body font**. That is also the
  seam-free choice: furniture set in a different face from the UI it wraps is
  the one thing a viewer notices without being able to name it.
- **Ligatures off**, for the reason the whole system has them off: a code
  ligature composes `!=` into one glyph, and on a caption quoting the app that is
  a claim rather than a typographic choice. `say()` refuses `≠ → ✓ ✗` and the
  rest of the tofu set outright — derive the real set from the font's cmap when
  you know the file (`fontTools` recipe in `PRODUCTION.md` §3).
- **The plate fills the caption band**, exactly — the bottom 17% of 1080,
  `y896–1080` — and the safe-area gutter puts its text at `x96`. That band is
  reserved across the whole catalogue, kept clear even in films that carry no
  captions, so a plate that is 96px tall or floated somewhere else is not a
  smaller caption: it is the one film whose bottom edge does not line up.

**Geometry is stated in video pixels and converted with the zoom, and the two
coordinate spaces do not agree.** This is the part worth reading twice, because
it is invisible until the capture is cut against a composed frame. `take.js`
reaches a fixed-width layout with CSS `zoom` on `html`, so a plate declared
`96px` tall lands at `96 × zoom` in the *file*. Measured at zoom 1.6842: the old
96px plate is **162 video px**, not the 184 the band wants — and it is worse than
a wrong number, because everything about it looks right in the browser. So pass
the zoom to `configure()` and let the overlay do the division.

Then measuring it back has the opposite trap, also measured on Chromium 1194:

| under `html{zoom:1.6842}` | reports |
|---|---|
| `getBoundingClientRect()` | **video px** — a 109.25px-tall plate measures 183.98 |
| `getComputedStyle()` | **CSS px** — the same plate reports `109.25px` |

`checkOverlay()` compares the rect raw and multiplies the computed padding, and
it exists because getting that backwards produces a perfectly styled plate in the
wrong place. Its control is one line: build the overlay without telling it the
zoom, and it reports a 310px plate starting at y770.

The same mismatch had already broken `point()`, silently, for as long as anything
has used `zoom`: it read a rect (video px) and assigned it straight to
`style.left` (CSS px, zoomed on the way out), so the highlight landed at
*position × zoom*. Measured at 1.6842, a target at (168, 202) was ringed at
(274, 330) — a ring around the wrong control, or off the screen, in a take that
otherwise looks fine. Anything that reads a rect and writes a style has to divide.

### Spoken narration, if you add it

`recordVideo` writes a **silent** track — voice is not a setting, it is a second
pipeline you build and mux in. It has been produced ad hoc in a session before,
which is the problem: re-improvised each time, it lands on a different voice, a
different pace and different levels, so the demo's sound quality is luck. Pin it.

**The voice is Kokoro `bm_george`, and it is not a per-film decision.** Every
film in the catalogue uses it; a demo that arrives in a different voice breaks
the family harder than any visual difference, because the viewer hears the change
before they can look for it. Pace varies by type, the voice does not.

```python
from kokoro import KPipeline
pipe = KPipeline(lang_code='b')                      # British English
audio = np.concatenate([c.audio.numpy() for c in pipe(line, voice='bm_george', speed=1.0)])
sf.write(f"assets/voice/{n:02d}.wav", audio, 24000)  # Kokoro emits 24 kHz mono
```

Where mxcli is named at all — in a Type A film that is the closing credit only —
**write it phonetically in the script**, `em ex see ell eye`, so the TTS spells
the five letters out instead of trying to pronounce it. On screen it stays
`mxcli`, lowercase. A copy pass will "correct" this back into a word if nobody
says why it is there.

`ffmpeg` and `ffprobe` are not guaranteed present — both were **absent** from a
fresh web container, and `apt-get install ffmpeg` failed there against a stale
package index (404s on superseded `libva`/`mesa` versions) until `apt-get update`
ran first. Check for them before promising audio.

Four things decide whether the result sounds professional. All are measured, not
matters of taste:

1. **Normalize to the catalogue's level, or it clips *and* it stands out.** Raw
   TTS output measured **-17.5 LUFS with a +0.0 dBTP true peak** — at full scale,
   so it crunches audibly the moment it is encoded to AAC for the video. Two-pass
   `loudnorm` (measure with `print_format=json`, then feed the measured values
   back) to **`I=-18.6:TP=-1.5`**, which is where the rest of the films sit; an
   earlier pass here targeted -16 and would have made the demo the loudest thing
   in the catalogue by two and a half LU. Resample to 48 kHz stereo at the same
   time — 24 kHz mono is not what a video container wants.
2. **A bed, not a track.** A product demonstration takes a warm sustained pad,
   low and continuous, no percussion, mastered to **-30 LUFS** (`loudnorm=I=-30:
   TP=-3:LRA=7`) so it sits well under the voice. Duck it to near-silence under
   the beat that pays off.
3. **Verify per line, never by total duration.** TTS has failed two ways that
   both pass a total check: 0 of 12 lines generated (a silent film, exit 0), and
   10 of 12 (a film with two silent beats). Assert each file exists, is longer
   than 0.5s, and matches the duration recorded for it — and that the count
   matches the script's line count. Read each clip's real duration back with
   `ffprobe` rather than trusting any synthesis flag.
4. **Time the video from the audio, not the reverse.** Synthesize first, measure
   each clip, and hold the step for `voice duration + tail` — not the bare voice
   length, which is what every sync tool defaults to and which leaves zero
   reading time. This is also why the keep-alive above is load-bearing rather
   than cosmetic: if an idle pause collapses to almost no frames, a pre-rendered
   voice track drifts against the picture no matter how good the synthesis is.
   Confirm the recorded file's duration matches the script's wall-clock before
   adding audio at all.

## The take has to be true, not only watchable

`narrate.js` makes a recording watchable. Nothing in it — by design — checks that
what you filmed actually happened, or that the timestamp you cut on points at it.
Four failures, each of which cost a take and each of which *looked like success*:

### The recorder's clock is not the video's clock

It is wrong in **two** ways at once, and fixing only the first is the trap:

- an **offset** — recording starts when the browser context is created, before
  your first navigation has settled;
- a **scale** — the capture drops frames while the page is busy, so the file plays
  back longer than the session it recorded. Measured at **~1.065**.

A constant offset that was right at the start was **four seconds wrong by the
end** — the difference between cutting to the payoff screen and cutting to the one
before it. Three rounds of cuts showed the wrong moment in every beat before this
was found, and each one was plausible in isolation.

So: record both anchors and map linearly, `video_t = A + B × mark_t`. Then
**verify by looking** — one frame from the middle of every clip, tiled into a
contact sheet. Spot-checking two clips is exactly how the wrong offset survived
those three rounds.

### Assert the state the beat is about

A click can be swallowed while the previous action's request is still in flight,
and the result looks fine: a board ended up *full but not solved*, so the payoff
never arrived and the control that depended on it stayed disabled. Check the DOM
for the state the beat is **about** — not that the click returned.

A beat that cannot be asserted is a beat you cannot trust. This is not a verdict
about the app: the demo still never gates the build. It is a check on the
**recording**, and it belongs here for the same reason a camera has a viewfinder.

### Pace to the app, not to the script

Driving entries faster than the runtime committed them made two microflows overlap
and deadlock in Postgres. The `UpdateConflictException` surfaced as a modal dialog
that then swallowed every later click and killed the take. Two defences: never act
faster than a floor found experimentally per app, and detect-and-dismiss the error
dialog so one failure does not cost the session.

Test the dialog guard on **visibility, not presence** — Mendix ships the error
dialog container in the DOM hidden, so a presence test fires on every click.

### `recordVideo.size` pads; it does not scale

A viewport smaller than the video size lands in the top-left corner with grey
around it. For a fixed-width page — which most Mendix layouts are — set the
viewport **to** the video size and apply CSS `zoom`: the page then lays out at the
smaller effective width while Chromium rasterizes at full device resolution.
Sharp and full-frame, where a smaller viewport is soft and letterboxed. A
stylesheet does not survive a navigation, so re-apply it after every `goto`.

### These ship as code: `take.js` and `cut-clips.js`

Both sit beside this file and are copied into the project with it. CommonJS, like
`narrate.js`, and required the same way.

| | |
|---|---|
| `openTake(browser, opts)` | a context with `recordVideo`, both clock anchors, the zoom fix |
| `take.mark(name)` | a beat, timed from the settled first screen |
| `take.click` / `take.type` | paced to `minGap` and guarded against the error dialog |
| `take.assertBeat(name, probe, why)` | records whether the beat held; `finish()` **throws** if one did not |
| `take.finish()` | closes the context, writes `capture/beats.json` with `offset_s` |
| `node cut-clips.js` | cuts the raw take on the linear map, refuses implausible anchors, writes the contact sheet |

`cut-clips.js` reads a project-owned `capture/clips.json` edit list, so the script
is the same everywhere and only the edit is per-film. It **refuses** a clip
shorter than its target unless that clip is explicitly marked `"freeze": true` —
holding a final frame is legitimate on a static screen, never to stretch an
interaction, and every pad is reported.

What stays per-project is the walk and the selectors. Only the machinery is shared.

## What to narrate

Narrate only what a viewer with **no build context** would understand.

Cut:

- anything that reads as *"here's proof the database is right"* — that is Stage 1,
  and to a viewer it is noise about a claim they were not disputing
- anything implying *"this used to be broken"* — the audience did not see the
  before, so it lands as an apology for a bug they never met
- **every word of Mendix vocabulary.** No entity, microflow, page, association,
  domain model, catalog. The test is sharper than a word list: *if the visual
  needs those words to make sense, the visual is wrong.*

Keep it to the persona's own motivation: what they are trying to do, what they
see, and what changed for them. Name them — "Sam", not "the user".

**Unless the product is single-player.** A puzzle, a calculator, a personal tool
has no task-persona, and inventing one is affectation. Write about the thing in
present tense instead.

## Where this stops

This skill owns the **capture**. How a capture is framed, cut and scored into a
finished film is the video system's — `video-system/` in `ako/mxcli-intro-video`,
which defines the product-demonstration type this skill feeds. Read it before a
film, in its own order, and **treat it as normative over this page**: the numbers
here are copied from it and go stale when it moves.

| | |
|---|---|
| `DESIGN-LANGUAGE.md` | palette, type, grid, plane, motion, the closing lockup, the honesty rules — invariant across all three types |
| `TONE-AND-SPEED.md` | everything that varies, as numbers. The comparison table is the working document |
| `types/product-demonstration.md` | the type this skill feeds |
| `PRODUCTION.md` | the hazards, several of which are the ones on this page |

Four boundaries worth keeping:

- The recording is **full-bleed** — no browser chrome, no window frame, no laptop
  mockup. The capture *is* the frame.
- The narration plate stays `narrate.js`'s. **One caption system per film**; a
  HyperFrames caption layered on in the edit reads as two designs. A film may
  also run the capture with no captions at all and carry the narration in voice
  alone (`videos/sudoku-demo` does) — but then the caption band stays *clear*,
  which is the same rule, not an exemption from it.
- **Nothing is animated on top of a capture in the edit** — no drifting scale, no
  Ken Burns, no highlight rings added in post. The app's own transitions carry
  those beats, and `point()` is allowed precisely because it is *in* the capture,
  decided at record time with the app's state in front of you.
- The **closing lockup** is the film's, not the capture's, and it is identical in
  every film in the catalogue. Do not build one into the walk.

### The clock map is a consequence of one long take

`take.js` records a whole walk in one browser context, which is why `cut-clips.js`
has to fit an offset *and* a ~1.065 clock scale before it can trust a mark. The
alternative — **one context per beat** — removes that problem entirely rather than
modelling it: each recording starts at its own zero, and there is nothing to map.
It costs the session, so each beat has to re-enter the app (carry the login as
Playwright `storageState`) and it cannot film a continuous interaction across a
cut. Take it when the walk is genuinely a set of independent scenes; keep the
single take when the continuity is the point.

## Checklist

- [ ] `journeys/<Module>.journey.json` exists and the journey run is `PASS`
- [ ] The positive-control run has shown every rung can go red — no `UNPROVEN`
- [ ] The demo is a **separate script**; no PASS/FAIL verdict lives in it
- [ ] Pace is human, with real reading pauses; the finished film is 60–120s at
      55–65% voice density
- [ ] Something animates during pauses, so idle time survives into the video
- [ ] `configure()` was told the same `zoom` as `openTake`, and `checkOverlay`
      passed — the plate fills the caption band, flat, accent-free, in the app's
      own font
- [ ] Captions carry no glyph outside the shipped fonts (`say()` refuses the
      known set; derive the rest from the font's cmap)
- [ ] Voice is Kokoro `bm_george`, mastered two-pass to `I=-18.6:TP=-1.5`, and
      every line was verified individually — not by total duration
- [ ] Recorded at **both** a desktop viewport and a real mobile device profile
- [ ] The mobile pass runs the same steps, with nothing simplified
- [ ] Narration mentions no database proof and no past bugs
- [ ] No Mendix vocabulary anywhere in the narration
- [ ] Every list the camera sees is populated with plausible data; every column
      and button the camera sees is captioned
- [ ] Every beat that has a payoff is asserted, and the take reported none failed
- [ ] Both clock anchors recorded, and the contact sheet **looked at** — each tile
      shows its own beat
- [ ] Every frozen tail is on a static screen, and reported
- [ ] App was live and the database real — this instrument mocks nothing
