---
name: game-testing
description: Write and run tests for this game — headless simulation tests, determinism and replay checks, physics/collision cases, input and timing edge cases, performance budgets, and visual regression. Use when adding tests, when a gameplay bug needs a reproducing case, before pushing a gameplay change, or when a test is flaky and needs diagnosing.
---

# Game testing

Games break in ways ordinary test suites miss: a bug appears only at 144fps, only
after 4000 ticks, only when two inputs land on the same frame. This skill is about
catching those.

## Project specifics

- **Test runner:** Vitest (TypeScript-native, runs the simulation headless in Node).
- **Run all tests:** `npm test`
- **Run one test:** `npm test -- <pattern>`
- **Typecheck / lint:** `npm run typecheck` / `npm run lint`
- **Headless sim entry point:** the simulation module runs with no Babylon scene and
  no renderer. If a test needs a `BABYLON.Scene`, the code under test is in the wrong
  layer — fix the layering rather than the test.
- **Havok in tests:** Havok is a WASM module and loads asynchronously. Initialise it
  once per test run, not per test.
- **Determinism caveat:** Havok is not guaranteed bit-exact across platforms, so
  golden-replay tests assert on _tolerance-bounded_ state, not on exact hashes, for
  anything downstream of physics. Pure-logic state (scores, heat, AI decisions, world
  generation) is hashed exactly. Keep the two clearly separated.

## The core idea: test the simulation, headlessly

Because simulation is separated from presentation (see the `game-dev` skill), the
great majority of gameplay logic is testable as a pure function with no window, no
GPU, and no real time. Tests drive the simulation directly:

```
world = newWorld(seed=1234)
for tick in 0..N:
    world = step(world, FIXED_DT, inputAt(tick))
assert something about world
```

Every test uses a **fixed seed** and a **fixed timestep**. A gameplay test that
depends on wall-clock time or an unseeded RNG is broken, not flaky.

## What to test, in priority order

1. **Determinism.** Run the same seed and input script twice; assert the resulting
   states are byte-identical. This one test protects every other test in the suite —
   when it fails, something ambient (a clock, a hash order, a global RNG) has leaked
   into the simulation.
2. **Replay/golden runs.** Record an input script plus the final state hash for a few
   representative scenarios. These catch unintended behaviour changes across a whole
   system that unit tests scoped to one function will miss. When a golden fails,
   decide deliberately whether the change was intended — and if so, re-record in the
   same commit and say so in the message.
3. **Rules and state machines.** Scoring, damage, win/lose conditions, cooldowns,
   phase transitions, resource economies. Ordinary unit tests, high value, cheap.
4. **Physics and collision.** See the edge-case list below.
5. **Timing and input.** Buffering, coyote windows, simultaneous inputs, held vs.
   tapped, inputs on the exact boundary tick.
6. **Content validation.** Every level/data file loads, validates, and is completable
   or otherwise well-formed. Run this over all content, not a sample.
7. **Performance budgets.** Assert tick time and allocation stay under budget for a
   representative heavy scene.

## Edge cases that actually bite

Write these deliberately; they are the recurring sources of real game bugs.

**Physics / collision**

- Tunnelling: a fast object crossing a thin wall in one tick. Test at the highest
  speed the game can produce, not a typical one.
- Resting contact: an object on a surface must not jitter or slowly sink over
  hundreds of ticks. Run it for 1000+ ticks and assert stability.
- Corner and seam cases: exactly-on-boundary positions, two surfaces meeting, the
  gap between adjacent tiles/colliders.
- Zero and degenerate values: zero-length vectors, zero mass, zero-size colliders,
  entities at exactly the same position.
- Simultaneous collisions: three-body contact in one tick; assert order-independence
  or that the defined order is the one implemented.

**Timing**

- Very small and very large `dt` (frame spikes, alt-tab, breakpoint pauses).
- The accumulator clamp: assert a long stall does not produce a catch-up spiral.
- Long-run drift: 10,000+ ticks — accumulated float error, counters overflowing,
  slow leaks in pools.

**Input**

- Press and release within a single tick.
- Conflicting inputs (left+right simultaneously) — assert the defined resolution.
- Input arriving on the first and last tick of a window boundary.

**State**

- Entity destroyed while another system still references it this tick.
- Save/load round-trip: serialise mid-run, restore, assert identical continuation.
- Pause/resume: assert no simulation time passes while paused.

## Test structure

- Name tests for the behaviour and condition, not the function:
  `player_keeps_jump_when_pressed_within_coyote_window`, not `test_jump_3`.
- One behaviour per test. A failure name should tell you what broke without reading
  the body.
- Build scenarios with small, named helpers (`worldWith(...)`, `inputScript(...)`),
  not by hand-constructing world state in every test — hand-built fixtures rot and
  hide what the test actually depends on.
- Assert on meaningful state, not on incidental representation.

## Flaky tests

A flaky gameplay test is a real bug until proven otherwise — usually a determinism
leak, an unclamped `dt`, or a test asserting on float equality without a tolerance.
Never retry, skip, quarantine, or loosen a test to make it pass. Find the source of
nondeterminism; the determinism test above usually names it.

Float comparisons use an explicit epsilon appropriate to the magnitude — and if a
test needs a wide epsilon to pass, that is a signal about the simulation, not the test.

## Visual and audio

These are the parts headless tests cannot reach, so bound them narrowly and check
them by running the game:

- Rendering: screenshot/visual regression at fixed seed, fixed tick, fixed resolution
  if the stack supports it. Otherwise, run the game and describe what you observed.
- Audio and haptics: manual. Say plainly in the report that they were checked manually.

Never claim a visual change works without having run it.

### Audio is more machine-checkable than "manual" suggests

Haptics are manual. Audio mostly is not: hang an `AnalyserNode` off the running
graph as an extra output — a node can feed several destinations, so it observes
without altering — and read RMS over a window. That catches the whole class of
failure where every number is right and no sound comes out: a suspended context,
a disconnected node, a voice that was never started. All three look identical
from Node, and all three look identical to a passing unit suite.

Four things learned doing it in #23:

- **Read the bus that answers your own question.** The master is the only place
  the volume settings have been applied, so it is the only honest place to ask
  "is this muted" — but asking "did the engine stop" there gets the music's
  answer too. One tap made that check quietly unfalsifiable for a whole run.
- **RMS over a window, not a single frame.** A single reading can land on a zero
  crossing of a periodic signal and report silence for a voice that is fine.
- **Wait out the reverb tail.** Everything stops the instant a round is
  disposed, but a convolver's return keeps ringing into the same bus for its
  decay. A measurement taken immediately reads a dying tail and calls it a
  running engine.
- **Assert headroom, not just presence.** "The sirens are audible" passed at an
  RMS of 1.7 — four times too loud, well past clipping. A ceiling is the check
  that would have caught it, and it costs one line.

Node counts are the leak check nothing else can do: audio nodes appear in no
counter any other harness samples, and a one-shot pool that never frees is the
same shape as every other leak already found here.

## Test the production build, not just the dev server

A dev server and a production build differ in bundling, module resolution, asset
URLs and tree-shaking. Code that works under one can fail under the other, and
the dev server is the more forgiving of the two — its dependency pre-bundling
pulls in modules that production tree-shaking discards.

Build it, serve the output, and load it in a browser before believing a change
ships. `vite preview` plus a headless browser is enough; assert that no error
reached the page and that the scene actually has geometry in it.

**And treat a start-up that fails silently as a bug in its own right.** A black
screen on someone else's device is the least actionable report there is. Name
the stage being entered, surface anything thrown to the screen rather than only
the console — which nobody can read on a phone — and make sure failures _after_
start-up are visible too: a handler that writes into a loading overlay reports
nothing once that overlay has been removed, which is exactly the window a
render-loop failure lives in.

## A harness that hides its subprocess output has no diagnosis

If a test spawns a server, a build or an emulator, capture that child's stdout
and stderr and print them when the test fails. The first CI run of the
production smoke test here failed with `preview server never became reachable`
and nothing else — the server's own output was piped into a variable nobody
read. That message names the symptom the harness observed, never the cause the
child already printed.

Three related rules, all learned from the same failure:

- **Let the tool choose the port and tell you which one it chose.** A pinned
  port fails two ways: a stray listener makes the harness give up, or — far
  worse — the stray listener _answers_ the readiness probe and the test happily
  runs against somebody else's server and passes.
- **Watch the child for death, not only the port for silence.** Poll the exit
  event alongside the readiness probe, and re-check it after a probe succeeds. A
  dead server can leave something live-looking behind it.
- **Size timeouts for a cold CI runner, not a warm laptop.** Ten seconds passed
  locally every time and failed in CI on the first run. Waiting longer for a
  server that is coming up costs nothing; giving up early costs a red build with
  no explanation.

Kill the child from a `process.on('exit')` handler, not only on the paths you
remembered — an assertion that throws otherwise orphans it for the life of the
runner.

## Put geometry generation where a test can reach it

Mesh building that lives in the renderer layer cannot be tested headlessly, and
"cannot be tested" here means real bugs ship. The road surface was built in the
engine layer with its segment quads wound the opposite way round from its
junction pads: every segment was backface-culled, and the city rendered as
disconnected squares with no roads between them. No error, no warning, and it
survived several screenshots because the roads were also nearly the same colour
as the ground.

Moving the buffer generation into the pure layer — positions, indices, normals,
colours as plain arrays, with the renderer doing nothing but uploading them —
turned it into a one-line assertion: every triangle's signed area in the ground
plane must have the same sign. It also puts the work where a Worker can run it,
which streaming wants anyway.

Worth testing about generated geometry, all of it headless:

- **Consistent winding**, and no zero-area triangles.
- **Buffer coherence**: normals and colours match the vertex count, no index
  exceeds the vertex count.
- **Position invariants**: a flat surface has every Y equal and every normal up.
- **Budget**: triangles per chunk, asserted, so a spacing change that multiplies
  the cost fails here rather than on a phone.

## A screenshot noise floor does not transfer between scenes

Measuring how much two runs of a capture harness differ _with the code
unchanged_ is the right way to know whether a difference means anything. But the
number is a property of the scene, not of the harness. Post-drive shots differed
by 0.2–0.6 of a channel value when the world was an empty plate; in a city the
same shots differ by 3–6, because a few centimetres of car position now change
which buildings are in frame.

So: re-measure the floor whenever the scene changes materially, and prefer
comparisons on shots that do not depend on a physics run at all. The static
at-rest angles stayed at 0.001 throughout and are what actually settled whether
a far-clip change removed anything visible.

## When something is invisible, make it unmistakable before theorising

Three rounds were lost to "is the geometry missing, mispositioned, culled, or
just too dark?" — each guess spawning another screenshot. The way out is one
override, from the console or the harness:

    material.disableLighting = true;
    material.emissiveColor = new Color3(1, 0.25, 0.25);

Flat bright, no lighting, no shading to interpret. Placement stops being a
judgement call, and the answer arrives in one shot instead of five. Pair it with
a dump of each mesh's world-space bounding box: between them, "not there",
"somewhere else" and "there but unreadable" are three visibly different answers.

Note also which harness mistakes cost time, because they recur: a portrait
viewport tripped the game's own rotate-to-landscape overlay, and pointing the
camera straight down left it gimbal-locked against its up vector and rolled the
view arbitrarily. Frame diagnostic shots obliquely.

## Test the world the game actually has

A pursuit test on bare ground passed comfortably while, in the running game, the
same AI car drove fifty metres and wedged itself against a building. The test
world had no buildings in it, so it could not have found that — and it read as a
green tick on the exact behaviour that was broken.

When a system's whole job is to negotiate the world, the test has to include the
world: stream the collision in, place the obstacles, use the real generator.
Anything less tests a simulation of a simulation.

Related, and the same shape: **a test's premise can be false while the test still
passes.** One here was named "does not stall when no road route exists", with the
target 1.5 km away — where a route very much does exist (32 hops). It exercised
the ordinary path and never once reached the fallback it claimed to check. Assert
the premise (`expect(routeFromTo(...)).toBeNull()`) so the test fails when it
stops being true, rather than quietly testing something else.

## Some failures cannot be caught by a stopwatch

An unbounded search over an infinite graph is a synchronous infinite loop, and no
test runner can interrupt one from the thread it is running on. A timing
assertion never executes; the suite hangs instead of failing, and in a game it
presents as a frozen tab.

So guard it structurally — export the bound and assert it is finite — alongside
the behavioural test. Same rule as a constant that a test derives its own
expectation from: when the failure mode cannot produce a test result, the
assertion has to be on the thing itself.

## Break the test before you trust it

A suite that goes green on its first run has told you nothing yet. Deliberately
break the thing each test is supposed to police, and check it actually fails.
Doing that to the road-network suite — nineteen tests, all green first time —
found three that did not bite:

- **"Every segment appears exactly once" survived an ownership shift by one
  index.** The set stayed one-per-slot; it was simply the wrong set. The fix was
  to compare the chunks' combined output against the authoritative per-index
  functions, rather than checking the output was self-consistent. Self-consistency
  is not correctness.
- **A test that reads its expectation from the constant it is policing proves
  only that arithmetic works.** `expect(|offset| <= spacing * jitterFraction)`
  passes at _any_ jitter, including values that let adjacent roads swap places.
  Assert the invariant on the constant itself (`jitterFraction < 0.5`), separately
  from any behaviour that derives from it.
- **A property that fails only on a coincidence needs several seeds.** Strict
  ordering of road lines held for the default seed even under a tuning that
  permitted inversions. One seed is one sample.

The mutations that _did_ fail cleanly are worth as much: they are the evidence
that the remaining tests are load-bearing. Record which ones you tried.

## The visual inspection pass

**The gameplay camera is the worst possible place to judge the game from.** It shows
one angle, at one distance, framing the thing it is designed to flatter. Whole
classes of defect are invisible from it and obvious from anywhere else. Run this
pass after any change to geometry, materials, scale, or world construction — and
periodically regardless, because these defects accumulate silently.

Suspend the chase camera (`view.setFollowEnabled(false)`, then place `view.camera`
directly) and capture:

| Angle                                 | Catches                                                           |
| ------------------------------------- | ----------------------------------------------------------------- |
| Front, rear, left, right              | Asymmetry, wrong proportions, parts hidden inside other parts     |
| Two 3/4 views                         | How the object actually reads in play                             |
| Ground level                          | Whether the object sits _on_ the ground or floats; contact shadow |
| High and plan view                    | Footprint, track width, layout, alignment                         |
| Close-up                              | Intersecting geometry, z-fighting, texture stretching             |
| **Wide, far back**                    | **World extents, horizon treatment, LOD popping, missing ground** |
| Dynamic: cornering, braking, airborne | Body roll, dive, suspension travel actually reading               |

Composite the results into labelled contact sheets rather than reviewing one image
at a time — defects show up by comparison, and a sheet makes an asymmetry or a
missing shadow obvious at a glance.

### Verify the harness before trusting it

**Check the rig's own orientation convention against a known asymmetry before
believing a single label.** The first version of this harness had azimuth
inverted: every shot labelled "front" was actually the rear. Nothing failed —
the images were real, the names were wrong, and the conclusions drawn from them
would have been confidently backwards.

Use something unambiguous as the reference: headlamps are white and at the front,
the rear plate is yellow. If the shot named `front` shows a yellow plate, the rig
is inverted, not the car.

The same applies to framing on anything moving. A shot aimed and then captured
after a settle delay frames where the subject _was_: at 20 m/s a 200 ms delay is
four metres. Re-aim immediately before capture.

### The bug class this exists to catch

**Presentation extents that have silently diverged from simulation extents.** The
first time this pass ran on this project it found the visible ground was 400 m
across while the collision ground was 4000 m: the car drove off the edge of the
visible world and kept driving on invisible collision. From the chase camera that
is completely undetectable. From a wide shot it is the first thing you see.

The fix is structural, not a corrected constant: the simulation publishes the
extent and the view reads it, so the two cannot drift apart again. Prefer that
shape of fix whenever presentation and simulation describe the same thing twice.

## Screenshot tools race the thing they are photographing

A tool that waits a fixed time after `goto()` and then shoots is measuring from when
navigation _commits_, not from navigation start. Under throttling that offset is
unpredictable, and a transient screen — a splash, a loading bar, a hit flash — is
easily missed. The front-end pass here waited 700 ms for a splash that was up from
340 ms to 1875 ms and still photographed the menu twice, filing one of them as
"splash".

- **Wait on the artefact, not the clock.** Poll for the element or the decoded image,
  then shoot immediately.
- **Report a missed shot.** A screenshot of the wrong screen is worse than no
  screenshot, because it is filed under the right name and looked at later as
  evidence. Print a warning and mark the filename.
- **Measure before theorising.** Two rounds went into guessing why the splash was
  never captured. Instrumenting the page with `setInterval` marks and printing the
  actual milliseconds settled it in one run — and turned a suspected tooling bug into
  a real product bug (the art was losing a priority race, see `art-direction`).
- An init script runs **before `document.documentElement` exists**. A
  `MutationObserver` attached there throws and the whole script is lost silently — the
  symptom is an empty marks object, not an error.

## Waiting for an element that was never hidden

`waitForSelector('#play')` resolves the moment the element is in the document —
not when it is on screen. A menu built behind a splash is in the document from
the first paint, so the wait returned instantly and every screenshot after it
was one stage early: the "menu" shots were the splash, the "loading" shots were
the menu, and the tool had been reviewed from for a week without once
photographing the thing it was named after.

Wait for the state that actually changed. The splash element is *removed* after
its fade, so its absence is the signal; visibility of the target is the second
half, because a splash can also be dismissed into a boot failure and that ought
to be photographed as a boot failure rather than as a mystery.

The general form: **wait on the transition, not on the destination's
existence.** Anything built ahead of time cannot tell you it has been revealed.

## A harness that never exits looks exactly like a hang

Three screenshot tools here finished all their work, printed all their output,
closed the browser — and sat there holding a port until something killed them.
`process.on('exit', () => server.kill())` never ran, because it only fires once
the event loop empties and the spawned server's stdio pipes keep it from
emptying.

Two runs were killed as hangs before anyone read the last line of output, which
said the work was done.

Kill the subprocess explicitly on the last line of the script. And when a tool
appears to hang, read what it has already printed before treating it as stuck —
the difference between "hung at 40%" and "finished and did not exit" is the
whole diagnosis.

## Playwright's waitForFunction takes three arguments

`waitForFunction(fn, options)` is silently wrong. The signature is
`(pageFunction, arg, options)`, so an options object in the second position is
passed to the page as data and the call uses the **default 30 s timeout**. Every
call in this repo had it — six harnesses, timeouts written as 90 s and 120 s,
none of them ever in effect.

It fails only under load, which is when a long timeout was the point. Pass
`null` as the second argument.

## Screens the type checker cannot see

The menu shipped a button reading `1.5:30`, because `90 / 60` is `1.5` and minutes
needed flooring. Nothing in the type checker, the linter or 233 passing tests could
see it; one screenshot could. Any screen whose output is _looked at_ rather than
asserted needs a rendering pass in `tools/`, run at the size it is used at — for this
project, a landscape phone first and a desktop window second.

## A test that only uses an axis-aligned case cannot see a sign

Twice in one sitting, in two unrelated files: a geometry test written with the
car facing +Z, where the term whose sign was wrong is multiplied by `sin(0)`.
The mutation walked straight through both.

- **Headings in a test should be 0.4, 1.1, -2.2 — never only 0 and pi/2.** Every
  axis-aligned heading zeroes one of the two components and hides whatever that
  component's sign was doing.
- **State the property, not the coordinates.** "The offset is perpendicular to
  the heading" — a dot product — has no blind spot. "left.x is negative" has one
  at every quarter turn.
- The same applies to a mirrored coordinate conversion: a car facing north with
  a source dead ahead sits *on* the mirror plane, so the bug is invisible there
  and only there. Put the source to one side, at a heading that is not a
  multiple of a right angle.

## Mutation testing catches tests that cannot see their own subject

Twelve mutations were tried across three new systems here. Eight bit
immediately. The four that survived were all the same failure — a test whose
setup made the thing it asserted unreachable:

- **A ceiling test that measured acceleration.** "Boost raises the speed
  ceiling" sampled at 25s, drove 40s more and asserted the car was faster. It
  was still accelerating the whole time, so it passed with the boosted ceiling
  deleted. Prove the quantity has _settled_ — sample twice and require the
  second to match — before asserting something moves it.
- **A baseline that was also the treatment.** "Boost does nothing on an empty
  tank" held boost on both cars, and the control's tank had been quietly
  refilling. A control must differ in exactly one thing.
- **A correlation test against the wrong subject.** A hash-salt check compared
  trap placement against landmarks, which are keyed differently and disagree
  either way. It passed with the salt removed. Assert against the thing the code
  would collide with, not a plausible neighbour.
- **Two guards that could never fire.** `junctionAt` returns an object for every
  index, and the road generator repairs every junction to `minExits`, so both
  "is this a real junction" checks were unreachable. The mutation pass deleted
  each with the suite green. The fix was to delete the guards and assert the
  invariant they were standing in for.

The pattern: when a mutation survives, the bug is usually in the test's _setup_,
not its assertion. Ask what else changed between the two runs being compared.

A later pass over signs, street lamps and the emissive palette ran 17 mutations
and caught 16 first time. The single survivor is the other recurring shape:
**a test that exercises one case of an N-way branch**. `facadeNormal` picks the
nearest of four block edges; the test placed a building against one of them and
checked the sign went there. Deleting the `+Z` branch outright changed nothing
it looked at. A quarter of the city's signs would have faced the wrong way with
the suite green. If the code under test has four arms, the test needs four cases
— parameterise it rather than picking a representative one.

## Assert what is true, not what ought to be

A test written from the module's _intent_ rather than its _behaviour_ fails
honestly and then tempts you to weaken it until it passes, which is worse than
not writing it.

The palette suite started with "every emitter stays 20° from robber red at every
fade toward the haze". That is the rule the design comment implies. Six cases
failed, and measuring showed the premise was wrong: warm amber loses green faster
than red as it mixes into a violet haze, so it rotates _toward_ red, reaching 6°.
The available responses were to drop the threshold until it passed — leaving a
test that asserted nothing — or to find out what actually separates them, which
is that by then the colour is at value 0.36 against robber red's 0.97.

The result is a better test than the one intended: it asserts the brightness
bound on exactly the samples that come near red's hue, and it fails if that set
becomes empty, so it cannot go vacuous. And the module's own claim — that magenta
moves _away_ from red under fog — turned out to be true and is now asserted as a
monotonic property.

**Measure before choosing a threshold.** Three numbers in that file were picked
as round-looking guesses first (35°, 45°, 20°) and every one was wrong against
the real palette. Print the actual distribution, then set the bar against it and
say in the comment that it was measured.

**And write down what is NOT true.** The tempting blanket rule is the one the
next person will add back. A test that documents the exception, with the reason,
is what stops that.

## Driving the game to review a HUD

A HUD driven by simulation state cannot be reviewed from a static page — every
panel is empty until something happens. `tools/hud-inspect.mjs` runs the real
game through `?nomenu`, holds keys through the keyboard source (the same path a
player takes, not writes into the simulation), and shoots at points where
different parts of the readout are live. It prints the simulation state
alongside each shot, so a panel showing the wrong number is separable from a
panel showing the right number for a state you did not intend.

Every layout collision in this HUD was found this way and none was findable any
other way: a dev overlay printing through a panel, a score printed across the
rear-view mirror, a button covering a label.

## A screenshot tool must emulate the device it is reviewing for

`hud-inspect.mjs` shot a landscape-phone viewport but not `hasTouch`, so
`isTouchDevice()` returned false and the on-screen controls were absent from
every screenshot. The only HUD layout ever reviewed was the one nobody plays.

The first shot taken with `hasTouch: true` showed the accelerator pedal
**entirely underneath the speedometer** — both own the bottom-right corner — plus
three more collisions that had shipped unnoticed. Viewport size alone is not the
device. Anything gated on a capability check (touch, pointer type, reduced
motion, DPR) needs that capability set, or the screenshot is of a configuration
that does not exist.

Corollary: when the layout differs by capability, capture both. A change that
fixes the phone can break the desktop and the tool will never say so.

## Some bugs are invisible to every unit test by construction

`tests/touch.test.ts` dispatches synthetic pointer events straight at the
listener. When `pointer-events: auto` on the pedals stopped real touches ever
reaching that listener, all 18 tests still passed — they exercise the one path
that keeps working when the DOM is wrong.

A test that constructs its own input cannot detect that real input never
arrives. When a layer's whole job is _routing_ — DOM hit-testing, event
delegation, focus, z-order — the only test that means anything runs in a browser
and goes through the real path.

The gate added for this asks the narrowest possible question in production:
**at the centre of each control, is the topmost element the one the input layer
listens on?** No game state, no `__drive`, no timing — just `elementFromPoint`
with touch emulated. It fails as:

    SMOKE FAILED: on-screen controls are covered and cannot be pressed:
      pedal throttle -> path

which names the bug and the element that caused it. Prefer a check shaped like
that over one that drives the game and infers a failure from the result: it
cannot flake, and its message is the diagnosis.

## Before pushing a gameplay change

- Full suite green — paste or summarise the actual result, don't assert it from memory.
- Determinism and golden-replay tests specifically green.
- A new test that fails before the change and passes after it, for every bug fix.
- Performance budget test still within budget.

## A render target needs to be read, not photographed

A rear-view mirror is ninety pixels of a mostly black night scene. In a
screenshot, "the target is broken and rendering black" and "it is night behind
the car" are the same image, and a bug that made the strip solid black on one
device survived several review rounds because of it.

Two instruments settle it, and neither is a screenshot of the game:

- **Dump the target at its own resolution.** `rtt.readPixels()` in the page,
  into an `ImageData` and a canvas, back out as base64. Note that `readPixels`
  comes back bottom-up out of GL, so it needs flipping or the strip is upside
  down — which reads as the mirror being broken rather than as a row order.
- **Drive the input far past its shipping value and measure the mean.** To ask
  whether clustered lamps reach the mirror's pass, multiply every lamp's
  intensity by twelve and compare the target's mean brightness before and
  after. It moved 32%, which no screenshot could have established: the decal
  pools painted on the road look like lit road and cover for lighting that is
  not arriving.

The second one had its own trap. `ClusteredLightContainer.addLight` **removes
each light from `scene.lights`**, so the obvious `scene.lights.filter(...)`
found nothing, the probe reported "0 lamps boosted" and a 0.1% change, and that
reads exactly like the answer being no. A probe that finds nothing must say so
loudly enough that its null result is not mistaken for a measurement.

## A fixed sleep before an assertion is a false failure waiting to happen

The production smoke test clicked Play, slept eight seconds, then read the stats
panel. On a loaded machine the city was sometimes not built yet, the panel was
empty, every number parsed as 0, and the harness reported **"scene looks empty:
only 0 draw calls"**.

That is the worst shape a false failure can take. It is alarming, it is
specific, and it is about the wrong thing — it sends you looking at the renderer
when the answer is that the machine was busy. Two other gates in the same file
had already been fixed for exactly this, and the sleep survived both times
because it was not the line that failed.

Wait for the condition, then sleep only for what genuinely needs settling time:

```js
await page.waitForFunction(() => /draws \d/.test(statsText()), null, { timeout: 90_000 });
await page.waitForTimeout(4000);   // so the sampled fps is of a running game
```

And when the wait times out, say *that* — "the round never drew a frame within
90 s" — rather than letting a downstream assertion invent a diagnosis from a
zero it was handed.

The general rule: **a harness may sleep to let something settle, never to wait
for something to happen.** If a number being read can legitimately not exist
yet, the read is a race, and the failure message will describe the missing
number instead of the race.

## A feature that changes how the game *plays* needs a probe, not a test

Difficulty levels are the clearest case. Unit tests can prove the tiers are
**ordered** — more units, faster driving, longer memory — and ordering is not
difference. Four buttons that produce an identical chase look exactly like four
buttons that work, and nothing in a green suite says otherwise.

So build a *probe*: a headless run of the real simulation, same seeds across
every variant, one fixed input, reporting outcomes rather than asserting them.
Keep it out of `tests/**` — a separate vitest config with its own include is
enough. Two reasons, and both matter:

- It costs minutes, and a suite people skip protects nothing.
- There is no correct answer to assert. What counts as "hard enough" is a
  judgement about how the game should feel, and freezing today's numbers into a
  threshold turns every future tuning pass into a failing test.

The first run of this one reported **zero busts across all four difficulties**,
and chasing that single number found three bugs that no unit test could have
seen, because each was an interaction:

1. Units were dispatched from further away than they could perceive, so they
   drove to a stale belief and the pursuit never started.
2. Pursuers ran red lights only within 130 m of the player — a distance they
   could not reach *because* they were stopping at every red on the way. A
   deadlock between two rules that were each individually sensible.
3. Heat rose only while a unit was within 250 m, so outrunning the one car
   behind you cooled you down and no more were ever sent.

Every one of those is a rule meeting another rule. Unit tests check rules one at
a time; that is what they are for and why they cannot find this class at all.

**Instrument the probe until it explains itself.** "Zero busts" is a symptom.
Adding pursuer mean speed against its own setting turned a guess ("the cruise
cap is too low") into a fact (they average 15-21 m/s against settings of 34-58,
so the cap was never the constraint). Adding distance travelled exposed that all
eight seeds produced the *same* number to the metre — which meant no buildings
were loaded and the player was driving cross-country while the pursuit followed
streets. A probe measuring the wrong world is worse than no probe: it is
confident.

## Interchangeable placeholders hide the bug in what they are placeholders for

Sixteen billboards showed generated lettering: a frame, a name, a tagline, one
of sixteen palettes. Every board in the city was displaying **a different
brand's atlas cell** — the UV rows ran one way and the canvas rows the other, so
rows 0 and 3 swapped. It shipped, and nothing could see it: every board looked
like a plausible billboard, no test could tell which cell it *should* have had,
and the comment on the UV maths asserted the brand shown was correct.

It surfaced the moment one brand got real artwork, because that was the first
time two cells told apart.

The general shape: **procedural placeholder content is often
self-consistent enough to hide the bug in the system that places it.** Anything
generated from the same template — lorem text, numbered colours, "Item 3" — makes
a wrong index look exactly like a right one. When you cannot tell two outputs
apart by looking, you cannot tell a mapping bug from a working one either.

Two defences, and the second is the one that generalises:

- Make at least one item **distinguishable** early, even in a placeholder set —
  one cell that is obviously itself is worth sixteen that are obviously fine.
- When a value is written in one coordinate system and read in another, derive
  both from one source and assert they describe the same thing. Here that is
  `atlasCell`, returning the rectangle in pixels *and* in UVs, with a test that
  they agree. Any comment claiming two representations line up is a claim to
  test, not to believe — this one was wrong and load-bearing for months.

