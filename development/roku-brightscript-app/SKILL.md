---
name: roku-brightscript-app
description: Build a real Roku channel in BrightScript + SceneGraph and drive it autonomously over the network. Covers the language traps that compile clean and die at runtime, the SceneGraph focus and rendering model, a from-scratch design system (real fonts, a light focus ring, rounded corners, pills, scene-based Detail/Series) because Roku ships almost no design primitives, the ECP control+screenshot harness and its silent failure modes, deep-linking as the test door, and the certification limits that are decisions rather than bugs. Triggers on Roku, BrightScript, SceneGraph, .brs, roSGNode, ECP, RowList, MarkupGrid, Roku channel, sideload, trick play, BIF, Roku Search.
---

# Roku channel in BrightScript + SceneGraph

Written from taking a 27,000-title catalog app to Roku end to end — shell, Home,
Browse, Detail, Series, Channels/EPG, Search, Player — and driving it on real
hardware with no human watching. Roku is not like the other TV runtimes: the
language will betray you at runtime, the framework gives you almost nothing to
design with, and the only way to know anything works is to make the app tell you
over the console. Everything here was paid for on the glass.

If you are only *deciding whether* to build Roku, read
`smart-tv-platform-expansion` §10 first (0% code reuse, the `Video`-node
resilience regression, the economics). This skill is for when the answer is yes.

## 1. BrightScript compiles clean and dies at runtime — the trap list

There is no type checker worth the name. Every item below compiled and shipped
and then failed on the device; treat this as a lint you run in your head.

- **Reserved words cannot be parameters or variables.** `step`, `pos`, `run`,
  `on` are builtins. `sub advance(step)` fails to compile with "Builtin function
  call expected" — and you will write `step` again two ticks after you first fix
  it, so rename to `delta` and move on.
- **No method calls on a function's return value.** `CreateObject("roDateTime").AsSeconds()`
  and `Val(x).ToInt()` compile and die at runtime ("Member function not found" /
  "Builtin function call expected"). Assign to a variable first, or use the
  primitive form: `Int(Val(x))`, not `Val(x).ToInt()`.
- **A bare numeric literal's type is load-bearing.** `1.0` is a 24-bit-mantissa
  Float; `0x100000001b3` silently truncates to 32 bits. FNV-1a and SplitMix
  hashing that must match another platform's need `LongInteger`/explicit widths,
  or the deterministic schedule diverges from web/Android.
- **`str.Replace` (or any match) that matches nothing is a silent no-op.** A
  category line that never landed, a chip value that never changed — all looked
  like "no change" rather than an error. When a transform seems inert, log the
  before and after, do not assume it ran.
- **`Val()` returns a Float primitive**, so `svc.qDecade = Val(x).ToInt()` dies;
  `Int(Val(x))` is the form.
- **A missing `<script>` include is a RUNTIME error, not a build error.** The
  channel launches and the component silently does nothing. There is no linker.
- **`Str()` takes a Float**, so `Str(aString)` is a runtime Type Mismatch that
  halts the component. Route everything printable through one `fmt(v)` helper
  that switches on `type(v)`.
- **A field `init()` has not set yet is `invalid`, and `not invalid` is a Type
  Mismatch.** Write `not (m.flag = true)`, never `not m.flag`, for any flag that
  an observer can read before `init()` runs.
- **`itemContent` (and other observed fields) can arrive before `init()` has
  found its child nodes.** Guard the handler on the nodes existing, and replay the
  stored content at the end of `init()`.
- **Size an array from its definitions list, never a literal count.** A reset
  loop that hard-coded 4 after a fifth filter chip was added caused about 90% of
  Archive Watch 1.0.77's crashes (3.1% crash rate, read from the dashboard's crash
  logs). Read crash logs per version before guessing.
- Keep a project `tools/test_*_includes.py` that parses every `.xml` and asserts
  each referenced `.brs` exists and each `sub`/`function` a component calls is
  defined — the compiler will not.

## 2. SceneGraph: the rendering and node model

- **A `Rectangle` has no bitmap fields.** Reading `bitmapWidth` off one returns
  `Invalid`, and `Invalid > 0` is a Type Mismatch that halts the whole
  component — the symptom is a screen that only ever shows the splash. Guard
  every bitmap read with `HasField("bitmapWidth")`.
- **A gradient built from stacked `Rectangle`s BANDS.** Sixteen 6%-steps at
  ~40px each read as stripes on a panel. Use a single pre-authored vertical PNG
  scrim, `scaleToFill`.
- **`RowList` field names are irregular.** It is `rowSpacings` (plural), not
  `rowSpacing`; a wrong name is silently ignored. Read the component reference,
  do not guess.
- **A `LabelList`/`MarkupGrid`'s focus bitmap draws UNDER the item text** if it
  is opaque. For a custom ring, use a transparent 9-patch and
  `drawFocusFeedbackOnTop = true`, and draw your own ring in the item.
- **Poster decode size is a per-URL cache, and `loadWidth`/`loadHeight` are
  hints.** If the same URL is drawn large elsewhere, a node asking for a tiny
  decode still gets the big cached bitmap. To force a small decode (e.g. for a
  blur), give the node a *different, genuinely smaller* URL (tmdb `w92`, commons
  `?width=120`, amazon `_SX120`), not just a small `loadWidth`.
- **A node's children are not auto-stacked.** Two bare siblings in one list item
  overlap at the same origin; wrap them in a layout group (`LayoutGroup`, or a
  Group you position by hand). The framework does no flow layout for you.

## 3. Focus is the whole job, and it is invisible

SceneGraph focus is subtle and every mistake is silent. The rules that cost the
most:

- **A `Group` is not focusable.** `setFocus(true)` on a Group whose descendants
  are all `Rectangle`/`Label` silently does nothing — the Scene keeps focus and
  the component's `onKeyEvent` never runs. Put focus on a real focusable
  (`Button`, `LabelList`, `MarkupGrid`, `Poster` with `focusable`), or the whole
  screen is inert while looking perfect in a screenshot.
- **`setFocus(true)` from INSIDE a component while its own descendant holds
  focus is a silent no-op.** A hero's `enterHero` claimed the screen while its
  RowList still had focus, so every following key went to the row; the fix is
  `m.rows.setFocus(false)` *then* `m.top.setFocus(true)`. The parent scene can
  hand a Group focus at launch (which is why launch-time checks pass) but a
  descendant cannot promote itself over a sibling that holds it.
- **A list keeps `itemHasFocus`/`focusPercent = 1` after the LIST loses focus**,
  so a tile stays ringed under a now-focused hero — two rings at once. Gate the
  tile's ring on the *list's* focus (`gridHasFocus`/`rowListHasFocus`), not the
  item's.
- **A zone with no `onKeyEvent` branch is a dead control.** Search filter chips
  were drawn, styled, listed done — and unreachable, because nothing sent a key
  to them. Every focusable zone must appear in the key handler.
- **Writing a field the value it already holds fires no `onChange`.** Setting
  `focusOn = true` when it is already `true` does nothing; a re-entry needs a
  toggle or an `alwaysNotify="true"` field.
- **A hidden screen keeps running.** A rotating hero kept firing (and fetching
  art) under an open Detail because nothing set its `onScreen` gate false —
  the viewer returned to a different film than they left.
- The transport keys (`Rev`/`Fwd`/`Play`) are **only delivered to a screen that
  is playing video** — a "Fast-forward jumps to results" shortcut on a browse
  screen is dead code the moment it is written.

## 4. There is no design system — you build one

Roku ships flat lists, a grey default focus box, square everything, and system
fonts with **no size** (you pass a `Font` node a uri + a size). A stock channel
looks like a database browser. The "does this read like an Android app on a
Roku?" ship gate is real; passing it means authoring, from nothing:

- **Real typography.** Bundle a variable display face + a text face, instance
  the weights you need (fontTools), Latin-subset them (pyftsubset) to stay under
  the package budget, and define exactly six levels (three weights × two sizes).
  A `Font` node per level.
- **A light focus ring with a soft edge, and only ever ONE lit thing.** Build it
  from 9-patch slices (corners + stretched edges), not a rectangle. It must ring
  the ART, not the CELL — and a shared placement helper must offset by the art's
  own `translation`, or the corners land at the parent origin and the art stays
  square (this is the bug that survives "verified" passes because it is off the
  canvas, not wrong on it).
- **Rounded corners** via corner/edge slices; **pills** for buttons (at most
  three, one primary/marquee); **no tinted-box backgrounds** on rows or cards
  (density comes from removing chrome).
- **Detail and Series are SCENES, not forms.** A backdrop fills the top band
  under a vertical gradient, the poster is an inset, copy sits in a column. See
  `ten-foot-detail-design` for the hero/eyebrow/meta rules — they are shared
  with the other TV platforms and were proven on Roku first.
- **Nothing on screen narrates navigation** ("Press OK to play", "Left/Right for
  more") and **no engineering talk** ("121 bytes of 32 KB used") reaches a
  consumer surface. The results are visibly to the right; the viewer does not
  need telling.
- **Broadcast-safe colour**: no channel above 235 (pure white `#FFFFFF` fails
  certification). Use `#EBEBEB` text, `#EB5531` for orange fills.
- **The font has no emoji** — a `⏩` renders as a tofu box on the glass. Icons
  are slices or shapes, never glyphs.
- **Mechanize the ship gate as a source lint** (`tools/roku_design_lint.py`):
  flag system-font-by-name, raw content-type slugs on screen, navigation-
  narrating sentences, flat-plate buttons, the old ring bitmap. Skip comments.
  Keep it at zero findings as a merge gate. A lint has blind spots — it caught
  instruction strings but not a slug inside a longer sentence — so it is a floor,
  not the whole check.

## 5. The ECP harness — and its silent failures

Roku's External Control Protocol is how you drive the device with no human.
It is also full of ways to *look* like it is working while doing nothing.

- **`/keypress/<Key>` key names are a CLOSED set. Roku returns HTTP 200 for a
  name it does not recognise and does nothing.** `keypress/OK` looked like a
  working press for thirty-odd ticks while the app never saw it — every OK
  assertion was vacuous. The key is `Select`. Make the harness refuse unknown
  names rather than trusting the 200.
- **`/launch/dev` restarts the channel; `/input?contentId=…` does not.** Use
  `/input` for deep links between surfaces so you keep app state; `/launch` only
  to cold-start.
- **The telnet console on :8085 REPLAYS its backlog when a client attaches, and
  DROPS on relaunch.** So a reader connected before `/launch` receives the old
  backlog and then EOF, and reads nothing the new run prints — which looks like
  "no trace". Connect the reader ~6s AFTER launch, and mark the line count so
  you distinguish new output from replay.
- **Text entry is `Lit_<url-encoded char>`** per character. On a Compose/on-
  screen key GRID (which is what a designed search screen is), neither `Lit_`
  nor an OS text-inject reaches the field — you must D-pad across the letter
  grid and Select each key. Assert your starting focus cell by its bounds before
  you begin, or the choreography types into the wrong place.
- **A screenshot cannot capture the video plane** — it comes back black while a
  film is genuinely playing. Verify playback by the console trace (state
  transitions, advancing bookmark position), never by the screenshot.
- **`error` on the Video node is STICKY** — it describes the last media session,
  so one broken film makes the next look broken. Clear/ignore it across sessions.
- **The dev installer speaks HTTP DIGEST auth**, not basic, and its "deploy OK"
  can be a parse of a response it did not understand — grep the response for the
  real success marker.

## 6. The iron rule of TV verification

**A harness step that does not reach its target proves nothing.** The two most
expensive mistakes both had this shape: presses that never got to the search
chips reported `[]` and got written up as "unverified"; a control sweep run
against a channel that was not even foregrounded reported every step green.
Before trusting any assertion, confirm the flow reached the thing — by the app's
own console trace (`AW*`-tagged prints) first, screenshots second. Read every
screenshot ADVERSARIALLY: list what is wrong in the PNG before you say anything
is right, and zoom 3× before filing a "border" defect (scanned posters carry
white margins that read as ring bugs). The owner is never the tester; the device
is the oracle and it will only tell you the truth if you make it talk.

## 7. Deep-linking is mandatory, and it is your test door

Certification requires deep links (they feed Roku Search), and they are also the
only deterministic way a harness reaches a surface: `/input?contentId=go:search`,
`go:surprise`, `item:<id>`, `series:<slug>`, plus harness-only doors
(`selftest:bif=<url>`, `selftest:layout`) that print a report or exercise one
path. Build the routing table early; you will lean on it for every check.

## 8. What is a decision, not a bug (write it down)

- **The `Video` node owns networking in firmware.** BrightScript cannot
  intercept, range-request, proxy, or observe it — so byte-range resume and
  storage-node failover **cannot be reproduced**. What remains is redirect
  pinning + a position-stagnation watchdog that re-issues `play` at the last
  position (every recovery is a visible cold re-buffer). Record this as an
  accepted regression, not a TODO.
- **Off-device sign-in is prohibited by certification.** Google's limited-input
  device-code flow IS off-device sign-in, so cross-device sync via Drive/iCloud
  is blocked on Roku by POLICY, not plumbing. Do not build it because a backlog
  note says to — the binding doc and the sourced cert rule win over a NEXT note.
- **Storage is a ~32 KB registry** and `cachefs:` is evictable, so a Library is
  capacity-bounded and downloads are impossible — the same constraint tvOS has.
- **Trick-play thumbnails (BIF) are a cert item for content over 15 min.**
  Measure before pricing: one real BIF is `ffmpeg -skip_frame nokey` streamed
  (no full download), ~21s and ~2.5MB for a feature, and the `Video` node
  renders it natively from `HDBifUrl` with nothing else set. That is a
  cover-job-shaped batch, not a "pipeline programme".

## See also

- `ten-foot-detail-design` — the hero/eyebrow/meta/episode/search patterns,
  proven on Roku and ported to Android TV; platform-agnostic
- `smart-tv-platform-expansion` — the decision to build Roku, the four-runtime
  map, and the cross-store economics
- `native-platform-first` — exhaust the platform's own controls (its transport,
  its trick play) before drawing your own
- `resilient-media-streaming` — the streaming resilience Roku's `Video` node
  cannot reproduce, so you know exactly what you are giving up
- `binding-design-doc-discipline` — a ROKU-DESIGN.md the ship gate cites; a
  NEXT/STATE note never overrides a binding rule
