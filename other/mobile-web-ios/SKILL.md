---
name: mobile-web-ios
description: Shipping this game on iOS Safari as an installable PWA — memory ceilings and crash avoidance, frame and draw-call budgets, touch controls, the audio unlock gesture, viewport/safe-area/fullscreen handling, service worker and offline caching, install flow, and on-device testing. Use when working on controls, audio, the PWA shell, or any performance or crash issue on iPhone.
---

# iOS mobile web

iOS Safari is the target, and it is the least forgiving environment we ship to.
Assume everything is tighter than on desktop: memory, thermal headroom, GPU fill rate,
and the patience of a player whose phone is getting hot.

## Memory is the binary constraint

Desktop degrades under memory pressure. iOS Safari kills the tab. There is no warning
and no recovery, so memory is a hard budget rather than a performance concern.

- Watch total **GPU texture memory** above all — it's the usual killer in a 3D web
  game. KTX2/Basis textures stay compressed on the GPU; PNG/JPEG do not, and decode to
  full uncompressed size.
- Cap texture resolution on mobile aggressively and ship a smaller atlas set than
  desktop. Half-resolution textures are almost never noticed on a phone screen.
- The endless city streams continuously, so a small per-chunk leak becomes a crash
  within minutes. The load/unload leak test in `procedural-world` is the defence.
- Test on the **oldest device we support**, not the newest. A crash that only happens
  on an iPhone with less RAM is still a crash for those users.
- Reload-and-play for 10+ minutes before calling a memory change verified. Short
  sessions hide leaks.

## Frame budget

At 60fps the entire frame is 16.6ms — simulation, physics, generation, and render.
Budget explicitly and measure on device:

- Draw calls are the dominant cost on tile-based mobile GPUs. Instance and merge.
  Count them per _object_, then multiply by how many of that object the busiest
  scene will hold — one detailed car at ~44 draws is nothing on its own and 264
  in a six-car chase. Do the multiplication while the object is still the only
  thing on screen; diagnosing a frame-rate problem across six cars and a
  streamed city is a far worse job than making one car cheap.
- Overdraw is the second. Avoid large transparent surfaces, full-screen post-effects,
  and stacked alpha. Post-processing is usually the first thing to cut on mobile.
- Real-time shadows are typically the single most expensive feature — prefer baked or
  blob shadows.
- Thermal throttling means a demo that runs at 60fps for 30 seconds may run at 30fps
  after five minutes. Sustained frame rate is the number that matters; measure it late
  in a session, not at the start.
- Support a quality tier system (texture size, draw distance, effects, shadow on/off)
  chosen by a startup benchmark, with a manual override in settings.

## Touch controls

The car is driven with thumbs on glass. This is a design problem, not a port problem.

- **No virtual joystick for steering.** Choose a scheme deliberately: tilt, steering
  zones (left/right screen halves), or a draggable wheel. Prototype and test on a real
  phone early — this decision shapes the vehicle tuning.
- **This game steers with a pad** (#10): the whole left half is the steering surface,
  and steer is the thumb's travel from wherever it first landed, not from a fixed
  centre. A thumb lands where it lands, and a control you have to look at to find is a
  control you cannot use while driving.
  - Tilt was built alongside it and removed when the pad won. It is not free to keep:
    a second scheme is an iOS permission prompt that silently grants nothing until it
    is asked from inside a gesture, a calibration control, a stored preference, and a
    branch in every steering path. Delete the loser; the history keeps it.
  - Do not auto-accelerate. It was the default here and was wrong: a car that drives
    itself from the first frame takes away the first thing a player does, and every
    deliberate lift, coast and feathered corner entry with it. Braking cutting the
    throttle is enough to stop the two fighting.
- Touch targets sized for thumbs and placed in the natural arc of where thumbs rest,
  respecting safe areas. Do not place controls where a thumb must obscure the road.
- Handle multi-touch properly — steering and handbrake will be pressed simultaneously.
  Track pointers by `pointerId`; never assume one active touch.
- `touch-action: none` and prevent default on the canvas to stop scroll, pull-to-refresh,
  double-tap zoom, and text selection. These will otherwise all fire mid-chase.
- Steering input is smoothed and speed-sensitive (see `vehicle-physics`). Raw binary
  touch input mapped straight to steering angle is undriveable.
- Add haptics via the Vibration API where supported, and treat it as absent on iOS
  Safari — plan feedback that doesn't depend on it.

## Audio

- **Audio will not play until a user gesture.** Create/resume the `AudioContext`
  inside a real tap handler — typically the "Play" button — and never before.
- Handle interruptions: calls, the silent switch, backgrounding, and route changes.
  Resume the context on `visibilitychange` when returning to foreground.
- Engine audio is pitch-shifted from a loop keyed on RPM/speed. Budget it as a real
  cost; too many simultaneous sources will hurt.
- Always ship a mute control, and remember it. Many players play silent.

### Built in #23, and what it actually cost

- **The unlock belongs on the first gesture anywhere, not on Play.** Menu music
  needs a context while someone is reading the menu, not as they leave it. One
  capture-phase `pointerdown` on the menu wrapper takes every tap; capture
  matters, because it runs before any handler that might stop propagation and
  the unlock cannot then be lost to a control written without it in mind.
- **`listener.positionX` is undefined on older Safari, not throwing.** Feature
  detect and fall back to `setPosition`/`setOrientation`. The failure mode of
  getting this wrong is a TypeError in the render loop, or — if you guard it —
  every source sitting dead centre with no clue why. Same shape as the WebGPU
  extension trap this project has hit twice.
- **`decodeAudioData` has two shapes.** Modern browsers return a promise; older
  Safari only takes callbacks and returns undefined, so awaiting the return
  value waits forever. Pass both and let whichever exists win; resolving twice
  is a no-op.
- **A limiter on the master is not optional** once the voice count varies. Peaks
  of independent voices add, and they add hardest exactly when the game is at
  its most exciting. Measured here: three sirens at full scale put the effects
  bus at an RMS of 1.7 before anything else was mixed in.
- **Close the context on teardown.** Safari keeps the audio session — and the
  "in use" indicator — alive otherwise.
- **Generating placeholder samples beats shipping them.** No encoder is needed,
  they weigh zero bytes of download budget, and swapping in a real recording is
  a file copy. Generation is `sin()` per partial per sample on the main thread
  at the moment the player taps, so render drones at 22 kHz — `AudioBuffer`
  resamples on playback and a sound with nothing above a few hundred hertz is
  identical for half the cost.

## PWA shell

- Web App Manifest with `display: "fullscreen"` (or `"standalone"`), correct icons
  including maskable, portrait/landscape orientation as designed, and a theme colour.
- iOS needs `apple-touch-icon` and its meta tags in addition to the manifest — the
  manifest alone does not fully drive the iOS install experience.
- Respect `env(safe-area-inset-*)` for notch and home indicator. Controls under the
  home indicator get swallowed.
- Lock to the intended orientation and handle rotation without losing game state.
- Service worker caches the shell and assets for offline play. **Version the cache and
  handle updates explicitly** — a stale service worker serving old WASM against new JS
  is a confusing and very common failure. Never cache-bust by hand; use a build-time
  hash.
- The WASM (Havok) and any large assets need a considered caching strategy — they're
  the bulk of the download.
- Provide an install prompt/hint. iOS gives no automatic banner, so an explicit
  "Add to Home Screen" hint is required if we want installs.

## First paint versus full load

Splitting boot at the first thing the player can *decide* buys the whole download for
free. Here: renderer, quality detection and the ~670 KB Havok WASM depend on no menu
choice and run behind the title screen; world, city and loop are all seeded from the
player's choices and cannot start until Play is pressed. The wait is spent reading the
menu instead of watching black.

- **Memoise the async loader** so awaiting it again after the choice is free.
- **A long synchronous fill loop makes a progress bar lie.** The city fill ran 64
  passes with no repaint; a bar attached to it goes 0 → 100 in a single paint. Yield to
  a frame every few passes.
- **This does not help the bundle budget.** The gate measures every file in `dist/`
  regardless of load order. Deferring a download changes *perceived* load time and no
  number the budget prints. Say which one you mean.

## Encoding images with no image tooling

No sharp, ffmpeg, ImageMagick or cwebp in this environment — but Playwright is
installed, and Chromium is a competent WebP encoder. Load the source in a page, draw
it to a canvas at the target size with `imageSmoothingQuality = 'high'`, and read it
back with `canvas.toDataURL('image/webp', q)`. Commit the outputs rather than
generating them at build time: a build step that needs a browser is a build step that
breaks on someone else's machine.

## A landscape phone is 390 CSS px tall, and that is the whole budget

Every overlay competes for the same corners, and the bottom-right is the worst
contested: it is both the natural home for an instrument cluster and where the
thumb that accelerates lives. The pedals win — a control that is covered is
broken, an instrument that is smaller is not. Desktop-sized HUD elements need a
compact variant for touch rather than a smaller scale factor; drop what cannot
be read at speed instead of shrinking all of it.

The corners, in the order they were claimed here: bottom-right pedals,
bottom-left steering, bottom-centre a status line, top-left and top-right panel
stacks, top-centre a mirror. Nothing else fits, and each new element has to take
space from something rather than find some.

**Percentage-sized children of a content-sized grid track resolve to nothing.**
A `place-content: center` grid sizes its tracks to their content, so an SVG at
`width: 42%` inside one collapses to a dot. It presents as a broken icon rather
than as a layout bug. Size such children in pixels, from the same source the
container's size comes from.

## A ConvolverNode will not resample its buffer

Everywhere else in Web Audio, an `AudioBuffer` at a rate the context does not
use is fine: an `AudioBufferSourceNode` resamples on playback. That makes
rendering generated audio at 22.05 kHz a free saving when nothing in it goes
near 11 kHz — half the `sin()` calls, no audible difference, and on this
platform generation happens on the main thread at the moment a control is
pressed.

`ConvolverNode.buffer` is the exception. Assign a buffer at any other rate and
it throws `NotSupportedError`, synchronously. Inside a render loop that means a
running game replaced by a boot-failure overlay.

Generate impulse responses at `ctx.sampleRate`, and cache them so the cost is
paid once. Nothing else in the graph needs the exception.

## A centred column that scrolls loses its top, permanently

`justify-content: center` on an element that is also `overflow-y: auto` is a
trap, and it only springs on short viewports — which on this platform means the
target device and nothing else.

When the content is shorter than the box it centres, which is what it was asked
for. When the content is taller, it centres *anyway*: the overflow goes both
directions, and `scrollTop` cannot go below zero, so the part above the origin
can never be scrolled to. It is not clipped-looking. It is simply absent, and
the box scrolls smoothly through everything that remains, which is why it reads
as correct.

Here it ate 24 px off the top of a settings column on an 844x390 phone — a
section heading and part of a row of buttons — and the bottom section with it.
Desktop at 800 px tall never overflowed, so every review missed it.

The fix is two elements:

```
outer:  overflow-y: auto            /* scrolls, nothing else */
inner:  display: flex; flex-direction: column;
        justify-content: center; min-height: 100%
```

Short content centres against the full height; tall content grows the inner box
past 100%, starts at the top, and scrolls to the end.

`justify-content: safe center` expresses this in one declaration and is the
right answer where the Safari floor allows it. Check the floor first — the
fallback when it is not understood is the broken behaviour, silently.

**And measure it, because a screenshot will not tell you.** At `scrollTop = 0`,
the first child's top must be at or below the container's top. One number, and
it is the difference between "looks fine" and "the install hint has never once
been reachable on a phone".

## A long press selects the whole screen, and four properties are needed

Holding a control on a phone selected the entire page. `user-select: none` was
already set — on the wrong element, and alone it would not have been enough.

- **`-webkit-user-select` as well as `user-select`.** Safari still needs the
  prefix, and Safari is the only browser with the bug.
- **`-webkit-touch-callout: none`.** The magnifier and the copy/share bubble are
  a *separate mechanism* that survives `user-select: none` entirely.
- **`-webkit-tap-highlight-color: transparent`** for the grey flash on tap.
- **On `html, body`, not on the control.** This is the part that had been got
  wrong: the pedals are deliberately `pointer-events: none` (see below), so a
  thumb on a pedal is really a thumb on the canvas, and the controls container
  is nowhere in that element's ancestry. Putting it on the root also covers the
  HUD and the menu for free.
- Opt text inputs back in with `user-select: text`, or a "copy this link"
  fallback that calls `select()` becomes a dead end.
- Swallow `contextmenu` on the canvas too — that is the same gesture on Android,
  and a right-click mid-corner on desktop.

## Never give an on-screen control pointer-events

Touch input listens on the canvas and resolves what was hit from
`control-layout.ts`. The overlay that *draws* the controls is
`pointer-events: none` so every touch falls through. That is not incidental
styling — it is the mechanism, and it is what keeps the drawn position and the
pressable position from drifting apart.

Anything painted over a control with pointer events enabled silently intercepts
it. Adding `pointer-events: auto` to the pedals — to get a CSS `:active` pressed
state — made the pedal's own child `<path>` the event target, and because the
overlay is a *sibling* of the canvas rather than an ancestor, the event never
reached the listener. All three controls broke at once, and they still lit up on
press: the worst version of the failure, because it looks like the control
worked and the car is broken.

**A pressed state must come from the input layer, not from CSS.** Publish which
controls are held and let the overlay reflect that. The DOM's opinion about what
was touched and the simulation's opinion are the same thing right up until they
are not, and the moment they diverge is exactly the moment you need the readout
to be honest.

The same applies to anything else that lands over the control zones — dev
buttons, debug panels, a toast. If it has pointer events and it overlaps a
control circle, it is a dead control.

## Haptics: iOS has no web API for them

`navigator.vibrate` is a W3C standard that Safari on iOS does not implement, and
has not for years. There is no supported way for a web page to drive the Taptic
Engine.

There is one unsupported way. iOS 17.4 added a `switch` attribute to
`<input type="checkbox">`, and toggling one produces a real haptic tick — so a
hidden switch, clicked, is a haptic. Feature-detect it with
`'switch' in document.createElement('input')` rather than sniffing the user
agent, which would also match iPadOS pretending to be a Mac.

Treat it as a bonus, never a dependency:

- It needs iOS 17.4+, and does nothing when the player has System Haptics off —
  which is correct behaviour and indistinguishable from being broken.
- Apple can close it in any release, and the failure mode is silence.
- It produces one fixed tick. An API that accepts a strength and ignores it on
  this path is lying to a caller who cannot detect it; say so at the call site.

**Fire haptics from the pointer handler, not from the render loop.** Both
mechanisms want to be inside a real user gesture, and a pressed state derived
from simulation state arrives a frame later with the gesture's call stack gone.

**Wrap every call.** Browsers throw from `vibrate()` when the page is hidden or
the feature is policy-blocked. This code runs inside the handler that also
steers, so an exception there takes the steering with it.

Fire one on the first guaranteed gesture of the session — a Play button — so the
player learns on their first press whether their device does haptics at all,
rather than wondering mid-chase. Expose which mechanism resolved: a device with
none is otherwise indistinguishable from an implementation that is broken.

## Making a touch control feel pressed

One element can only scale, and a control that shrinks reads as moving *away*
from the screen rather than being pushed into it. Use two layers: a rim that
holds its position and a face that travels into it, with the rim's inner shadow
deepening at the same time.

**Lighten the fill on press so the shadow has something to darken.** A dark
inset shadow over a dark fill on a night scene is invisible; the first attempt
here changed only the rim, which read as "highlighted" rather than "pushed in".

Make the downstroke fast and the return slow — roughly 45ms against 170ms. A
pedal is pushed and returns under its own spring, and that asymmetry is most of
what separates a mechanical movement from a UI animation. Give controls of
different kinds different motion: a lever that swings where a pedal sinks stops
three circles reading as three identical buttons.

## Audio that plays before a gesture

Autoplay with sound is refused by default everywhere and hardest on iOS, where
`play()` returns a promise that rejects with nothing logged in a production
build. Write it expecting refusal: attempt, and on rejection arm a one-shot
listener for the first gesture.

Scope that fallback to whether playing is *still* correct. A title sting armed
on first gesture and fired ten seconds later is not a late sting, it is a random
noise over whatever is on screen now — poll the caller's state at fire time
rather than assuming the moment survived.

## Testing on device

Desktop Chrome device emulation does **not** reproduce iOS memory limits, thermal
behaviour, touch handling, or Safari's WebGL/WebGPU quirks. It is useful for layout
and nothing else.

- Test on a real iPhone, connected to Safari Web Inspector on a Mac for profiling.
- Verify both the WebGPU path (iOS 26+) and the WebGL2 fallback on an older device.
- Verify installed-PWA mode separately from in-browser — fullscreen, safe areas,
  service worker, and audio all behave differently once installed.
- Never report an iOS performance or crash fix as verified without having run it on
  hardware. Say which device and iOS version.
