---
name: charles-3d-explainers
description: "Make premium, cinematic 3D explainer videos and 3D cutaways timed to a voiceover: dark 3D worlds lit with one warm accent, glowing signal paths, hero numbers that land on the word, labels pinned to parts, a running HUD counter, live app screens on 3D devices, and continuous camera moves with real depth of field and motion blur, rendered with three.js in headless Chrome (bun). Use whenever Charles asks for 3D explainers, 3D motion design, 'how X works' visuals, documentary-style or cinematic 3D, educational 3D animation, 3D b-roll for a voiceover, or 3D cutaways that replace parts of a talking-head video, for a whole reel or for one slot of a video he is editing (charles-claude-editing asks for an asset at a size)."
---

# Goal

Every clause of the voiceover becomes something the viewer SEES happen, on its word, in a world that looks like an
expensive 3D render. Something new lands about every second, yet any paused frame has exactly one thing to look at.
The bar is a premium motion-design studio, never "three.js demo" and never AI slop.

`K` is this skill's `kit/` folder. Use absolute paths and bun (`export PATH=$HOME/.bun/bin:$PATH`), never node.

# What you are making

| Ask | Output |
|---|---|
| **Reel**: a whole voiceover | one 1080x1920 mp4 with the audio and captions, visuals for every second |
| **Slot asset**: charles-claude-editing picks a layout and asks for a visual at a size, with word times and a text area | one mp4 at exactly that size and length, no audio, captions off, text only inside the area it gave you |
| **Cutaways** for a talking-head reel: replace stretches of the face with 3D beats | one project per stretch on the creator's own voice, delivered as clips plus a cut list (section "Cutaways") |
| **Overlay**: an object floating over footage | ask before promising alpha; the kit renders opaque frames |

Slot sizes the editor uses: 1080x1920 new screen, 1080x960 half split, 1080x768 top-40% split, 1280x630 card above
the face, 1280x1550 tall card. Set `size` in project.json. Positions in this file are for 1080x1920: scale them, and
keep text 60 px inside every edge of the slot (the overlay defaults already scale: type and x by W/1080, y by H/1920;
`--audit` checks the 60 px).

# Setup (once per machine)

- `cd K && bun install`. Google Chrome must be installed (render.mjs finds it, or set `CHROME_PATH`).
- `FAL_KEY` in the environment or a `.env` up the tree, for transcription and the AI tools (models, plates, clips).

# Workflow

Walk these steps in order, every time. Never render a final before step 7 passes.

1. **Project.** `bun K/new.mjs <dir> --audio <voice> [--script script.txt] [--from s --to s] [--palette name]`. It cuts
   the audio, gets word timings, and writes `project.json`, `plan.md` (one row per sentence), `shots/` and `assets/`.
   Always pass `--script` when a script exists: it puts the script's exact words, digits and names onto the timings.
   With a script and no audio, ask for the voiceover first. Why: timing comes from the words, so anything built
   before the audio is a guess.
2. **Words.** Read `words.json` against the script: names, numbers as digits, spellings. `captions.replace` changes
   only how a word reads on screen.
3. **Plan** in `plan.md` (format below). Decide, for the whole video: one palette, one running example, the HUD
   quantity if any, the chapters. Then for every beat walk the Shot, Camera and Transition trees, and count events
   against "Pacing". If Charles is around and did not say "just do it", show him the plan before building.
4. **Build** one shot module per camera setup in `shots/`, registered in `project.json` with its start on a word
   onset. Start from the closest snippet in `references/kit.md` or a project in `examples/`. Read `references/look.md`
   before you light anything.
5. **Stills.** `bun K/render.mjs <dir> --stills <t1,t2,...>` at every key word + 0.2 s. Look at each one at phone
   size. render.mjs prints each still's tone (YAVG, YLOW, YHIGH, SATAVG) against look.md's ranges: fix every still it
   flags (give a shot row whose world is not night a `tone` key: space, screen, warm or hot). Fix and re-render until each
   still passes the Review checklist on its own.
6. **Draft.** `bun K/render.mjs <dir> --draft --audit`, then `bun K/sheet.mjs <dir>/out/draft.mp4 --every 1 --words
   <dir>` and `bun K/check.mjs <dir>/out/draft.mp4 --project <dir>`. Fix every `hook`, `static`, `dark` and `dangling`
   line, every stale span, lull, flash and unplanned pop (pops on a word you timed are listed as planned),
   and look at 30 fps strips around every cut (`--strip <t> --span 0.8 --fps 30`).
7. **Review** with the checklist at the end, at phone size. Anything that fails goes back to step 4. Note what you
   changed in `plan.md` so the next pass does not undo it. Then render 16-sample stills of every shot you changed
   since its last stills. Last, `bun K/render.mjs <dir> --draft --samples 16 --audit` and check.mjs on it: a 1-sample
   draft has no depth of field, and in a test round three of four finals failed a `static` run, a 2.2 s gap or the
   caption-band audit that their 1-sample drafts had passed.
8. **Final.** `bun K/render.mjs <dir> --audit`, then `check.mjs` on the final and a contact sheet. A final whose audit
   or check.mjs prints a `hook`, `static`, `dark` or text-over-subject line is not done.

# The plan (plan.md)

One row per beat. A beat is one clause of the voiceover, 0.8 to 3 s.

| start-end | words | the visual: what literally happens, on which word | shot type | camera | overlays | link |
|---|---|---|---|---|---|---|

Rules:
- **Literal first.** Every noun, number, place and app the voice names is visible within 0.2 s of its word, and every
  verb of change (slow down, speed up, split, add, "two things") gets its own visible change on its word. Why: the
  eyes confirm what the ears hear; a visual that lags or paraphrases reads as stock footage, and judges count every
  named idea they could not see.
- **One running example** (pacing.md section 6): one concrete thing from the viewer's life, introduced in the hook and
  carried through every beat that can show it (the photo your mom sent, your phone, packet #0847). When one becomes
  many, single one out with a short tag and follow it. It returns at least every 40 s and is on screen in the last
  5 s. Why: continuity turns 40 shots into one story; it is the cheapest retention tool there is.
- **Stay in the world.** Every beat happens in the running example's world: on, in or around the object, in its
  room, on its device, between two of its parts. An empty void (a backdrop, dust and one glowing line) carries at most
  one shot of 4 s or less per reel. A field of tiles, bits, packets or glyphs lies on a floor that recedes to a
  horizon: the camera 20 to 35 degrees above it, the horizon in the headline band, focus on the near rows (`blur`
  0.015 to 0.02), everything outside the active region at 40% emissive; never a wall square to the camera filling
  the frame. A signal (a wave, a pulse, bits) travels between two real objects of the running example, both in frame
  at least once. The world has several places (the room, the device's inside, the street, orbit, the cable under the
  sea): move to a new place or scale at least every 15 s. Why: the reels that lost the most spent a third of their
  runtime on a line in a navy void or a flat wall of tiles, which reads as a screensaver, and one backdrop held for
  35 s read as monotone even when every shot in it was right.
- **Teaching frames.** Plan the clearest frame first for the 2 or 3 beats that carry the mechanism (its verbs:
  flips, crosses, calculates, both on). The parts involved fill 50 to 80% of the width, seen square-on to the change.
  Two states are colour-coded (the accent and the cool secondary), in the world and in the caption highlights. One
  change at a time, held 1.5 s after it lands. A still of it at phone size can be described in 5 words. Every hero
  object shows the 2 or 3 features that make it nameable from a still (a silicon boule: seed, neck, growth ridges; a
  wafer: a bright thin edge). Every number on screen agrees with the others: received minus sent equals the travel
  time shown, an equation's result checks out, a clock never reads later than the time it stamps. Why: in four of
  five test reels the frames the video existed for were its least legible, and a judge does the arithmetic.
- **Payoff.** The last explained idea gets the biggest, clearest image of the reel: the running example, transformed,
  at 40 to 70% of the width. Never a thin line, a 30 px dot or a shape cut off by the frame. When the voiceover ends
  mid-sentence, end on that image held 0.6 s instead of looping.
- **Hook** (pacing.md section 8). Frame 0 is a finished beauty shot: the hero glows from inside or is backlit by a
  warm horizon (`k.backdrop({ horizon: 0.4 })`), its hottest pixels reach 240, it fills 35 to 60% of the width in the
  subject band, the headline and the first caption are up. Never an opaque matte object alone in a dark void, never
  a fade from black. The camera is already moving on frame 0 at 20 to 40 px/s: start the hook's move with
  `ease: 'linear'` or `'outSine'` (an in- or inOut-ease sits still for the first second). Within 0.5 s something also
  visibly changes on the hero (a light sweeping across it, a turn of 5 degrees or more, motes streaming at the
  camera): a 20 to 40 px/s drift alone reads as a still poster at phone size. Something visibly happens
  on the hero by 1.0 s (a glint sweep with a bloom streak, an ignition, a pulse arriving). Between 1.0 and 2.0 s the
  camera dives: a 2- or 3-stage scale journey (into the object, through its surface, to the first thing the voice
  explains), a stage every 0.5 to 0.8 s, joined by 0.4 to 0.6 s `zoom` transitions (copy `examples/hook-dive`).
  check.mjs's `hook` line reads 4 or more. The headline is 2 to 6 words at 110 px or more (one pill, or
  `style: 'cond'`), the rest of the sentence in a `((sub-line))`; it states a paradox or a surprising pairing ("How
  does [[sand]] think?"), never a description of the video, and leaves as the dive starts (1.2 to 2.4 s). The voice
  opens on the concrete object. Why: in blind tests against premium studio reels, every hook that sat still lost;
  four of five studio reels dive between 1 and 2 s.
- **Structure** (pacing.md section 10): cold open 5 to 15 s; the question restated over a quiet establishing shot; then
  chapters of 20 to 40 s, one world or one scale each, each opening on its biggest transition and a new hero number
  or section word; the last 5 to 10 s pull back to the big picture and end on the opening image, so the reel loops.

## Shot tree

Walk the questions in order for each beat; the first yes wins.

```
1. Names a concrete thing ("This is a transistor")?   → HERO REVEAL: the object alone, sharp, lit, slow push or quarter
                                                        orbit; a label on the part it names
2. Gives a number (count, size, speed, time)?          → HERO NUMBER over a scene that SHOWS the quantity (100 billion →
                                                        a field to the horizon; 30 m → a dimension line in the world);
                                                        a number standing in the world is props.extrude (3D type),
                                                        its text set from ft. A size comparison ("fits on your nail")
                                                        holds its number over the comparison image until the sentence
                                                        ends + 0.5 s, across a cut if needed (globals.js)
3. Says something moves, travels, sends, flows?        → SIGNAL PATH: a glowing path draws on, a pulse travels it, nodes
                                                        light as it passes, the camera follows the pulse
                                                        (cam.follow, pulse.place)
4. Changes scale (inside, from space, microscopic)?    → SCALE JOURNEY: one continuous zoom through nested worlds; a
                                                        scale bar (k.ui.scaleBar) steps down an order of magnitude on
                                                        each zoom word (1 mm, 10 µm, 100 nm)
5. Walks through steps of a mechanism?                 → STAGED MECHANISM: one set for all steps; each step lights or
                                                        moves one part; the step name as the hero term
5b. Says calculate, measure, work out, convert, add up? → EQUATION with real inputs, even when the voice never states
                                                        the formula (distance = 299,792 km/s × 0.0667 s); the terms
                                                        land on their words, the result last in the accent, then it
                                                        moves into the world
6. States a relation or formula?                       → EQUATION: terms land on their words, the result last, in the
                                                        accent, while the scene does the same thing (a curve that
                                                        draws on: glow.plot)
7. Compares two things, or before and after?           → TWO STATES: side by side, or one object morphing on the
                                                        contrast word; the two states in the accent and the cool
                                                        secondary, in the world and in the caption highlights
                                                        (captions.highlight [{ match, color }])
8. Mentions an app, screen, site or message?           → DEVICE SCREEN: a phone or laptop with a live HTML screen doing
                                                        exactly that step. A device action (send, tap, swipe, type)
                                                        is always a device screen with the real UI and a thumb
                                                        (props.hand), never a character clip. A screen in shot never
                                                        shows the reel's own title or captions
9. Names a real place or a distance on Earth?          → GLOBE, CITY or PLATE: the globe with an arc, the city from
                                                        above, an AI plate for a specific interior
10. Shows a person doing something (a habit, a feeling, a reaction)?
                                                     → CHARACTER BEAT: a body part at macro scale (an eye blinking,
                                                        a fingertip, a thumb), graded to the world, 1 to 1.5 s
                                                        (K/clip.mjs, references/characters.md), hard cut on the word,
                                                        then an object shot explains it; never a full cartoon figure
                                                        or a clay mannequin; at most one per 15 s
11. States data: a share, a trend, a ranking?          → CHART: props.bars, lineChart or donut grows on the word; a
                                                        count of things → props.stack with one hero tagged; a running
                                                        total in the world → props.scoreboard
12. Abstract: a feeling, a rule, an idea?              → a METAPHOR OBJECT with one explicit mapping (a lock for
                                                        "encrypted") or a DOODLE, in the running example's world;
                                                        never generic particles, never an empty void
13. Otherwise                                          → stay on the running example and change ONE thing on the key word
```

## Camera tree

Numbers from pacing.md section 4. One move per setup. A reel of 60 s or less moves like the fast story reels: the
camera is never near-still for 3 s in a row (check.mjs `static`), a real move (a dive, a follow, an orbit of 30
degrees or more, a whip) comes every 2 to 3 s, and pushes run 5 to 15% of the distance a second. Long explainers
(2 minutes or more) use the numbers in brackets. Why: premium short 3D reels move like story reels, and a slow
camera was the second most-penalised dimension in blind tests.

```
Introducing or explaining one subject?          → push in, 5 to 15% of the distance per second (long: 2 to 6%), for
                                                  1.5 to 4 s
One becomes many, a part shows its whole?       → pull-back reveal, 5 to 20% a second for 1 to 3 s, easing out
Something travels from a sender to a receiver?  → ONE follow shot through both places (cam.follow): it holds its
                                                  screen position while the world streams past at 300 to 600 px/s;
                                                  never cut between the sender and the receiver
Proving a hero object is real 3D?               → quarter orbit, 60 to 90 degrees over 3 to 5 s, with a gentle push
From a detail to the layout?                    → rise to top-down in 1 to 2 s
Orders of magnitude of scale?                   → cam.logZoom over 1 to 3 s; split into two shots joined by a zoom
                                                  transition when a texture would break up close
A number, equation or diagram is being read?    → drift 40 to 80 px/s (long: 20 to 40) for 2 s at most, then move
New angle on the same subject, in a fast run?   → whip (transition tree)
```

Always: ease in and out (except the hook's first move), `drift` 0.4 to 0.6 on every shot so no frame freezes, the
subject's silhouette inside x 200 to 880, y 560 to 1280 and never in the caption band (y 1320 to 1500). Why: a
locked-off camera reads as a slideshow, and a subject behind the caption is unreadable twice over.

Land the move before a hard cut. An eased move (a crane, an orbit, a push to a framing) reaches its end pose by
`k.out - 0.2`, so the last frames only drift. `k.out` is when the shot is last seen: its end, or a cutaway's out point
(`cutOut`) when that comes first. Key a move to `k.dur + 0.3` only when a whip or a zoom follows, which carries it,
or when the next shot keeps moving the same way at least half as fast; in a cutaway the last shot's `k.dur` runs on
into the 0.5 s handle after the out point. A constant slow orbit (a linear ramp) is ambient and may run through the
cut. check.mjs warns when a cut or the out point lands while the camera still travels; it measures the camera alone,
so rings rippling or a popup slamming in at the cut never count. Why: a cut from a drift, or from a move into a move
that continues it, reads as one flow; a cut in the tail of a move that is still landing reads as a shot cut off
before the camera arrived (Charles caught a crane over a carousel cut at a fifth of its top speed into a still frame;
in 8 of 15 test cutaways the last move was keyed to `k.dur + 0.3` and the face came back with the camera at more than
half its top speed).

## Transition tree

From pacing.md section 5. Pick from the story, never for variety.

```
Same world, attention moves to another part?    → no transition: rack focus (0.3 to 0.6 s, cam.rack) or a short pan
The thing travels to the next place?            → follow it in one shot, no transition
Scale changes (into, out of, down to)?          → "in": {"type": "zoom", "dur": 0.5 to 0.7} plus a push in both shots
Light or energy carries the story, or a chapter changes? → "light", dur 0.5, `at: [x, y]` = the light source's
                                                  screen point as fractions (default [0.5, 0.45]); at most once per
                                                  20 s
Pulling back out to the big picture?            → "zoom" with `out: true`
Time passes, or we leave one world for another? → "dip", dur 0.5
The voice draws an analogy?                     → match cut: the same shape at the same pixel in both shots
New angle on the same subject?                  → "whip", dur 0.3 to 0.45
A different place at the same scale?            → "fade" (a defocus blend), dur 0.3
Enumerated steps ("mix it, heat it, cool it")?  → hard cut on each verb's onset
Something shown small (a screen, a bubble) becomes the next scene? → portal: push into it, then "zoom"
```

Shots start on word onsets (`start` = a word's start). The incoming subject appears within about 300 px of where the
outgoing one was. Why: the eye should never have to search after a change. A hard cut between two framings of the
same subject changes its size by 1.5x or more, or its angle by 35 degrees or more; otherwise keep one continuous move
(check.mjs flags a cut that changes too little). Why: a cut that only moves a ring or a label reads as a glitch.
The outgoing shot's labels and numbers leave in the first third of a whip, zoom or light and the incoming ones
arrive in the last third (the kit does this). Never `fade` between two framings of the same subject: the crossfade
double-exposes it (two cables crossing in a V, ghosted spheres); use a whip, a cut matched on the subject's screen
position, or one continuous move. Fade thin glow lines out before a whip (its smear turns a bright line into a
staircase). Never the same transition three times in a row unless the story repeats.

# The look (numbers in references/look.md)

- **Dark world, one warm accent.** The accent belongs to the protagonist of the explanation (the signal, the active
  part, the term being solved) and to the caption pill that names it. A cool secondary (cyan) is for time and the
  system around it, red only for loss or failure. Big areas stay dark and low in chroma. Why: one warm light in a dark
  world IS the premium look; two accents read as a theme park.
- **Saliency agreement.** The subject is the brightest, sharpest, most saturated thing, and the one moving with
  purpose. If any of those points elsewhere, dim it, defocus it or stop it. This is what keeps a fast video calm.
- **Light like a night product shoot.** A soft, dim key from the top-back; a strong cool rim behind the subject (the
  brightest pixels after the emissives); warm light only from story objects, each with a point light that pools on its
  surroundings. When a floor or terrain fills the frame, keep the directional lights dim (look.md section 4 has the
  rig numbers). Why: evenly lit big surfaces are what reads as milky and cheap.
- **Depth of field by shot type.** Object and macro shots: `k.lens = { blur: 0.016 to 0.03, focus: <subject> }`, only
  the subject sharp. World shots (planet, city, sea floor, grid): `blur` 0.006 or less, deep focus, detail everywhere;
  never blur a world shot to hide missing detail. Pull focus over 0.3 to 0.6 s when the caption's subject changes.
  Nothing out of focus passes in front of the in-focus subject (it renders as stepped copies or a hard band): bring
  it in at the focus distance, or rack to it.
- **Materials.** A bevel on every hard edge, at least two roughness levels, micro-detail at three scales on anything
  that fills more than a third of the frame, contact shadows. A product never sits on a seamless colour backdrop: put
  it in a place (a nightstand at night, a desk, a hand).
- **Glow is information.** Emissive lines and pulses mean signal, current, path or data; nothing glows for decoration.
  Lines at intensity 4 to 6, pulse heads 14 to 30.
- **Air.** 10 to 40 visible motes (`fx.dust`), a lighter region behind the subject, dark corners.
- **Scale cues.** When a size is said, put something of known size beside it (a hair, a fingernail, a phone).
- **People are never toys.** Hands use `props.hand` (skin by default), lit dim and cool with a rim; the warm light
  falls only from the story object. No clay figures or cartoon characters next to hard-surface renders. A CG hand in
  close-up read as a mannequin in every test reel that used one: keep a hand under 30% of the frame height, rim-lit, the
  thumb pressing on its word (`hand.press`), or show the phone on a surface with no hand.
- **Glass, crystal and liquid heroes** need something lit behind them (a horizon glow or an inner point light):
  transmission shows only what is behind, so in a dark void glass reads as an opaque pebble. Anything molten uses
  `mat.molten`.
- **Space is never an empty void:** the kit's stars (150 or more visible at phone width), `fx.milkyWay`, blacks at
  6 to 10.
- **A product in a night world** gets `k.look.productLight(k.scene, product)`: white plastic reads mid-grey under the
  night rig without it.

# Type (numbers in references/look.md section 2)

| Band | y (1080x1920) | What |
|---|---|---|
| Top UI | 0 to 200 | nothing |
| Headline | 240 to 660 | title, hero number, HUD, section word |
| Subject | 650 to 1270 | the one focal object |
| Captions | 1320 to 1470 | one line, centred at about y 1432 (`captions.bottom` 450) |
| Bottom | 1540 to 1920 | quiet world only: the platform covers it |

- **Captions** come from the words: the kit breaks them on phrases (never after 'a', 'the', 'of', 'to', 'and' or
  'your'), keeps each up at least 0.7 s and shows the first one from frame 0 (kit defaults are the measured sizes).
  check.mjs's `dangling` line must be empty; its `flicker` line lists only chunks the size caps force: accept them.
  At most one highlight per chunk and about one chunk in four with one: a number with its unit, the mechanism being
  named, or the viewer's own object, in the colour that thing has in the world (`{ match, color }`). Never a filler
  word.
- **Title**: the hook's headline (see Hook): 2 to 6 words at 110 px or more, one emphasis, an optional sub-line, gone
  by 2.4 s.
- **One statement of a number.** While a hero number is up, its words in the caption get no highlight, and the hero's
  sub-label adds meaning ("light in glass") instead of repeating the caption. Why: judges called the same number in
  the caption, the hero and a label clutter.
- **Legibility.** Text that must be read is 40 px or more at the final framing (label sub-lines 34 px), including
  in-world text and the UI on a device screen; nothing under 44 px rides a moving anchor. A device screen in shot
  keeps its own text and controls above y 1300. While a caption is up, the caption band (y 1320 to 1500) shows only
  dark, defocused world: no bright line, edge, screen or text crosses it (`--audit` measures it; `post.captionShade`
  0.3 to 0.5 darkens the band softly when the composition alone cannot).
- **Hero number**: one at a time, lands within 0.2 s of its word (`at: k.word('200,000') - 0.1`), rolls up in 0.25 to
  0.3 s (`count: { dur: 0.3 }`) or grows live with the motion it measures, holds 0.8 to 2.6 s. Always a unit, and a
  sub-label when the unit is not enough. A result is built: inputs land first, the result last, in the accent.
- **HUD**: only for a quantity the story keeps returning to; one corner, never moves; enters when that journey starts,
  never while the title is up; runs in story time (pacing.md section 6 has the code); the voice quotes it once per
  chapter.
- **Labels**: at most two at once, 1 to 3 words, 30 to 150 px from the anchor, never on the subject or in the caption
  band, 1.5 to 4 s each; no leader line unless the anchor is ambiguous.
- **In-world text** (tags, scoreboards, signs) belongs to the scene; set changing text from the frame time `ft`.

# Pacing: fast but not chaotic (numbers in references/pacing.md)

- Plan one event per 0.7 to 1.2 s of voice, each tied to a word. Never 2.0 s without one; never two within 0.25 s.
  An event is a visible change: something enters, transforms or lights, a number or label lands, the camera reveals or
  turns, the shot changes. Captions are not events, and neither are a shimmer, a drift or a glow pulsing in place: a
  hold over 2 s on one subject reads as dead even when check.mjs counts its shimmer.
- About two events in three happen in the world, one in three is type.
- A bigger beat (a transition, a hero number, a scale reveal) every 3 to 5 s. A cut never lands with a number.
- A camera setup lasts 1.5 to 4 s, unless one follow move carries the time with events inside it.
- One change at a time: the camera, the subject and the text take turns. Little text: a caption, at most one hero or
  counter, at most two labels.
- Many angles, one subject: within a stretch, the angles circle the same subject.
- When a beat needs many things (1,500 packets, 600 cables), show the many as a field and make ONE the hero: lit, in
  focus, tagged.

# Cutaways in a talking-head reel

1. Read the edit's transcript and mark stretches whose words describe something you can show: a mechanism, a number,
   an action, a place, an app. Leave the face for opinions, jokes, direct address and the hook line, and keep it on
   screen for at least a third of the runtime. Why: the face carries the connection; the cutaways carry the
   explanation.
2. A stretch lasts 2 to 8 s, with a new framing every 1 to 1.5 s, one subject per framing, literal to the words.
3. One project per stretch on the edit's own voice: `new.mjs --audio <edit's voice track> --from <s> --to <s>
   --cut-out <out point>`, so every `k.word` is right. `--cut-out` writes the out point as project.json `cutOut` in
   project time (on an existing project, set it by hand: the out point minus `--from`); it sets the last shot's
   `k.out`, so its move lands before the face returns, and check.mjs tests the camera there. Captions off (the edit's
   captions run over the clip, so keep y 1300 to 1500 free of key detail); no title. check.mjs's `hook` line is for a
   reel's opening: on a cutaway, ignore it.
4. One palette for every cutaway in a reel. Match the creator's world: a dark studio world for a tech topic.
5. Deliver the clips at the slot size plus a cut list (in and out on the edit's timeline). Cuts land on word onsets,
   and the face returns on a word onset too.
6. Keep his receipts: a screenshot, code or text he quotes stays on screen while he reads it; the 3D takes over after.
   And on the face, a line that names a change over time ("16 years of retention optimization", "it used to...")
   shows the change happening: the old thing whips out and the new one whips in on the words, with a whoosh, never
   the old one alone as a static sticker. Why: the change is the point, and motion is what holds a talking-head beat.

# Building shots (kit rules)

- Shots are pure functions of time: `update(t, ft)` runs many times per frame at slightly different `t` (that is how
  motion blur and depth of field are made). Never accumulate state across calls; use `k.rng(seed)` and
  `k.ramp/keys/pulse`. Set in-world text from `ft`, the frame time, so it reads crisp. A shot that breaks this flickers
  or ghosts.
- Time everything from words: `const t1 = k.word('billion')` (shot-local seconds). Land events on the stressed
  syllable: `t1 - 0.05`. `k.word` prefers an exact match inside the shot and warns when it reaches outside it; nth
  counts from 0; time common words by two-word phrases ('AND gate', 'At zero'). `k.gword(phrase, nth)` searches the
  whole voiceover (shot-local seconds, negative before the shot), for one world built across several rows.
- `t` runs below 0 and past `k.dur` during transitions. Keep the camera moving there.
- Heavy defocus raises a shot's samples automatically; set `k.samples = 64` on a shot if copies still show.
- When the kit lacks something, walk this tree:

```
k.props has it (references/kit.md section 15: phones, laptops, servers, routers, chips, transistors, molecules,
  fiber, globe, moon, satellites, city, ocean, rooms, heads, ears, hands, headphones, speakers, mics, charts, 3D type)?
                                                                → use it
A simple form (box, cylinder, lathe, extrusion)?               → build it: bevels, two roughness levels, micro-detail
A named product the voice keeps returning to (AirPods, a game console) that the kit prop does not make
  recognisable from a still?                                     → the same model.mjs route below: a generic bud on a
                                                                 stick lost a judge's vote
A specific real object with a complex shape (a tooth, an engine)? → bun K/model.mjs (--dry first; about $0.53 and
                                                                 2 to 3 min, cached), then props.model with a kit
                                                                 material (clay, satin, plastic): AI textures have light
                                                                 baked in. Anything with moving parts or a cutaway is
                                                                 built procedurally: a generated mesh cannot move a part
A real place or an interior too costly to model?               → AI plate (references/plates.md, bun K/plate.mjs)
A person doing something?                                      → character beat (references/characters.md)
A real brand, product UI or logo?                              → the real logo or screenshot (k.imagePlane) or a live
                                                                 HTML screen (k.screen), never a generated imitation
```

  A prop worth keeping goes into `kit/engine/props/` for next time, under a name no other props file exports.

# Review checklist (every still and every draft)

1. Pause anywhere: can you say in 3 words what the frame shows, and is it what the voice says right then?
2. Exactly one sharp, bright, purposefully moving subject, its silhouette inside x 200 to 880, y 560 to 1280;
   nothing bright in the caption band while a caption is up.
3. Every named noun and number visible within 0.2 s of its word (sheet.mjs with `--words`).
4. check.mjs: `hook` 4 or more, no `static` run, no `dark` frame, no stale span over 0.6 s, no gap over 2.0 s between
   events, median gap 1.0 s or less, no unplanned flash, pop or jump.
5. Tone inside look.md's ranges for the world (render.mjs prints it for stills).
6. Type: `--audit` reports nothing (it also measures text over bright 3D); at most one highlight per caption, in its
   thing's colour; hero numbers on their words, and no caption pill on a number a hero is showing; two labels at
   most; text that must be read is 40 px or more, on device screens too; every number on screen agrees.
7. Frame 0 is the finished beauty shot with its headline and caption, the camera is moving, the dive starts by
   2.0 s, and the end returns to the opening image (or holds the payoff when the voice ends mid-sentence).
8. 30 fps strips around every cut and transition: no pops, the new subject appears where the eye already was, no
   crossfade double-exposes one subject, and no move is cut off while it is still landing (check.mjs warns).
9. At phone size (390 px wide), does it look like an expensive render, or like a three.js demo? Fix everything that
   fails before calling it done.
10. Every explanation beat is in the running example's world: no void shot over 4 s, no field filling the frame
    square to the camera, and the mechanism and payoff frames pass the 5-word test.

# References

- `references/look.md`: measured palettes, tone ranges, type sizes and positions, light, materials, depth of field,
  what reads as cheap.
- `references/pacing.md`: measured event cadence, shot lengths, camera moves, transitions, the running example, the
  HUD, the hook, whole-video structure.
- `references/kit.md`: every API, the project.json schema, CLI flags, tested snippets and gotchas.
- `references/plates.md`: AI plates turned into 2.5D sets for real interiors and places.
- `references/characters.md`: people doing things, in 1 to 1.5 s beats.
- `examples/`: complete projects to copy from.
