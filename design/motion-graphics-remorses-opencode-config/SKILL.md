---
name: motion-graphics
description: >
  Tommy's taste for motion graphics videos (launch videos, promo videos, product demos, explainers):
  something always moves, long animations with fast easing so a soft tail keeps moving, a camera that
  never stops, eased slide transitions between scenes (out with ease in, in with ease out), pacing
  that is fast but leaves time to read, cuts on the music beat, showing the real product working,
  one hero per beat with big readable type, a beat table before building, and example styles.
  Independent of the renderer (HyperFrames, Remotion, three.js, headless Chrome). ALWAYS load this
  skill before you design, animate, edit or review a motion graphics video, a scene transition, a
  camera move or video pacing.
---

# motion-graphics

**Something is always moving.** A motion graphics video never has a frozen frame: the camera
drifts, arrivals have long soft tails, held text creeps a few pixels. Movement is fast at the start
and slow at the end, and the next movement starts before the last one stops.

```
position
  │        ╭──────────────────────── long tail: still moving, a little
  │      ╭─╯
  │    ╭─╯       one tween: 1.2 s, expo.out
  │   ╭╯         90% of the move happens in the first 0.3 s
  │  ╭╯
  │──╯
  └────────────────────────────────────────────────> time
     ▲ next element starts here, the tail overlaps it
```

This skill says **what** the motion should look like. How to build it is in the renderer's skill
(see [Related skills](#related-skills)).

## Preferences

Tommy's rules, learned from feedback on the ghosthand launch videos. Follow them before anything
else, also where a renderer skill says otherwise.

- **Always animating.** Every frame differs from the one before it. Between two actions the
  camera drifts, a background turns slowly, or held text moves a few pixels. This beats the
  HyperFrames rule "a landed title is dead still".
- **Long durations, fast easing.** Use a strong ease-out (expo, quart) over a long duration,
  about 0.8 to 1.2 s for arrivals. The element is readable almost at once, then settles slowly.
  Short tweens with a mild ease feel stiff and stop dead.
- **Every start and stop eases.** Nothing jerks into motion or stops abruptly, not even the
  camera at the end of a long move.
- **The camera is never still.** It eases between framings without stopping at any of them.
  During a hold it keeps drifting slowly in the direction of its next move, with subtle
  handheld movement on top.
- **Slide transitions between scenes.** When the video has scenes, what leaves slides out and speeds up (ease in, short).
  What enters slides in and slows down (ease out, longer). Never slide an element that stays or
  morphs into the next scene: it keeps moving or morphs instead.
- **Fast pacing.** Each text stays only long enough to read it, then the video moves on. Do not
  slow scenes down too much: "faster please" came right after "give time to read".
- **Slow down without stopping.** For reading time, slow the motion of that span. Never freeze it.
- **On the beat.** Every scene lasts a whole number of beats of the music, so every cut lands on
  a beat. Times come from a `BEAT` constant and scene starts, never from magic numbers.
- **Show the product working.** Text types in, counters climb, checks draw, taps ripple where
  the real tap happened. Prefer real recordings, real logos and real UI over drawn stand-ins, and
  only show claims the product really makes true.
- **Drop what looks ugly.** If an element still looks cheap after one redesign (the mascot's
  hand), remove it. No cheap gradients and no cheap intro animations.
- **Vary.** Scenes enter from different sides, layouts get mirrored, no two scenes use the same
  entrance. The same rule as sound: every scene sounds and moves a little differently.

## Easing

Pick the ease from the role of the movement:

| Movement | Ease | Duration |
| --- | --- | --- |
| Element arrives (card, panel, title) | strong ease-out (expo, quart) | 0.6 to 1.2 s |
| Element leaves the scene | ease-in (power3) | 0.3 to 0.4 s, shorter than its entrance |
| Camera move between framings | ease-in-out, or a spline through keys | 0.8 to 1.5 s |
| One long camera fly | one ease-out over the whole path, so the fly decelerates into the last shot | 3 to 4 s |
| Small pop (icon, check, badge) | back-out with a small overshoot | 0.25 to 0.5 s |
| Drift, rotation, scroll, counters | linear or a slow sine | the whole scene |

- **Overshoot only on small things.** Icons and checks may bounce. Panels, text and the camera
  never overshoot.
- **Mirror the ease at a seam.** An ease-in exit followed by an ease-out entrance reads as one
  continuous move.

```
arrive(el, at):  from {offset, scale 0.92, opacity 0} to rest, duration 1.0, expoOut
leave(el, end):  to {offset, opacity 0}, starts at end - 0.38, duration 0.38, power3In
pop(el, at):     from {scale 0.4, opacity 0} to rest, duration 0.3, backOut(2)
```

## Camera

- **Keys, not stops.** Write the camera as a list of keys `(time, focus x, focus y, zoom)` or,
  in 3D, `(time, target, distance, azimuth, elevation)`. Join them with a smooth curve (a monotone
  spline, or ease-in-out per segment) so the camera passes through each key without stopping.
- **Drift toward the next move.** In a hold the camera creeps in the direction it is about to
  go, so the next move grows out of the hold instead of starting from zero.
- **Handheld on top.** A slow sine wobble on position and a tiny rotation, plus a slow push in.
  This is what keeps a held shot alive.
- **Feel filmed.** Motion blur on fast moves, light film grain, a soft glow and a vignette make
  code look shot by a camera. Keep each one subtle.
- **Travel pattern.** Glide to the place, push in on the detail, pull back to travel, dive in
  again. The pull back shows where the next detail is before the camera goes there.
- **Frame what matters.** Push in on the detail the viewer must read (a caption being typed, a
  request arriving). Pull back to show how two things relate (the phone next to the chat). When
  content grows (a bento grid), frame the bounding box of everything shown so far.
- **Lead the action.** The camera starts its move a little (about 0.1 s) before the element it
  goes to lands, so the motion feels motivated.
- **Big moves in 3D.** Flies, orbits and full 360° turns around an object are welcome. Text stays
  in its own column (left) and the camera frames objects to the right of it.

```
camera(t):
  key   = splineThrough(CAM_KEYS, t)          # never stops at a key
  lean  = key.velocityToNextKey * 0.05        # in a hold, creep toward the next move
  drift = (sin(t*0.9)*8, cos(t*0.7)*6), rot = sin(t*0.6)*0.5°
  zoom  = key.zoom * (1 + 0.004*t)            # slow push in
  return key.focus + lean + drift, zoom, rot
```

## Scene transitions

```
scene A  ────────────────[slide out, ease in, 0.38 s]┐
scene B                              [slide in, ease out, 0.65 s]──────────────>
                                     ▲ cut on the beat; B starts before A is gone
the mascot (carries over) ────────────────────────────────────── keeps its own path >
```

- **Directions tell the story.** The chat leaves to the left as the next chat comes in from the
  right. A window lifts up as the dark window rises from below.
- **Carry-overs keep moving.** An element that lives in both scenes (a character, a logo, a card
  that becomes the next screen) continues its path or morphs. It never slides out and back in.
- **Background changes are slow.** A color flood or darkening runs about 1 s under the last
  moves of a scene, so the outro does not pop in.

## Pacing

- **Reading time.** A line the viewer must read stays about 0.5 s plus 0.3 s per word. Give the
  extra time only to the spans with text, and spread it as slower motion, not as a pause.
- **Title cards are quick.** A slow title card looks like the end screen.
- **Speed up recordings.** Real screen recordings play faster: pauses shrink to about 1 s, actions
  play at about 2x so taps stay readable. The payoff (the post going live) plays near normal speed.
- **Fit scenes to beats.** Choose the beat count per scene first, then stretch or squeeze its
  reading spans to fill it.

```
scene.duration = beats * BEAT
extra = scene.duration - naturalDuration
for span in readingSpans: span.duration += extra * span.weight / totalWeight
```

## Building up content

- **Stagger rows.** Items in a row arrive 60 to 160 ms apart, never all at once and never one
  fully after another.
- **Grow, then frame.** A grid or list grows piece by piece, each piece sliding in from the side
  the grid grows to, while the camera pulls back to include it.
- **Link cause and effect.** When one thing drives another (a chat step and the phone), show the
  link: a beam or a pulse that travels from the cause to the effect.
- **Loops have no sound per item.** A scrolling feed or floating hearts is continuous motion. See
  the `sound-effects` skill for which movements get sounds.

## Readability

- **One idea per beat, one hero.** The hero is sharp and bright, everything else dims back.
- **Say each phrase once.** If the voiceover says it, show it on a real object or type it on
  screen, never both, and never repeat it later.
- **No filler text.** Body copy that is not meant to be read (paper, documents, list rows) is soft
  grey lines, not words people try to read.
- **Big type.** Hero words very large, labels never tiny. If it cannot be read on a phone in one
  second, it is too small or there is too much.
- **Less is more.** Leave out decorative clutter (stickers, stamps, extra labels, random shapes)
  that is not part of the story. Prefer design, smooth movement and clarity over more stuff.
- **Land on the word.** Visual moments hit the spoken word or the beat: a circle drawn as the
  word is said, a stamp on the downbeat.

## Textures

Flat CSS colour looks like a web page. A light paper texture and an animated grain make it look
printed and filmed. Ready files live in `textures/` next to this skill; copy them into the
project's `assets/`.

| File | Use | Source |
| --- | --- | --- |
| `paper-fine-offwhite.jpg` | the ground: neutral off-white, fine tooth, 2160 px | [cosmos](https://www.cosmos.so/e/1105763690) |
| `paper-fine-grey.jpg` | a cooler, darker ground or a card back | [cosmos](https://www.cosmos.so/e/576531001) |
| `paper-cold-press.jpg` | paper objects with relief (notes, tickets, cards) | [pinterest](https://www.pinterest.com/pin/1093811828237448272/) |
| `grain-mono.jpg` | grain overlay, even, no vignette | [pinterest](https://www.pinterest.com/pin/1057079343802453490/) |
| `grain-rgb.jpg` | colour grain overlay, for a filmed look | [cosmos](https://www.cosmos.so/e/951654745), by Louis Vogler |

- **Much weaker than you think.** The ground of a polished explainer measured a pixel standard
  deviation of about 1.4; these papers are about 4 to 5. Shift the texture to the ground colour,
  then show its detail at about 30% (`opacity` over a flat fill, or `soft-light`).
- **Grain moves, paper does not.** Paper is fixed to the world and moves with the camera. Grain is
  fixed to the screen and changes every two frames: offset the grain tile by a seeded hash of
  `floor(frame / 2)`, never `Math.random()`. A still grain looks like a dirty screen.
- **Texture the objects too.** Cards, notes and tickets get the paper at the same low strength, so
  the objects look as physical as the ground.
- **Measure it against the reference.** When copying a video, compare the pixel spread of a flat
  patch of ground and of one card in both, and tune the strength until they match.
- **Credit before publishing.** These come from Pinterest and cosmos uploads, not stock sites.
  `grain-rgb.jpg` is an artist's Instagram post: replace it before a public release.
- **Skip vintage overlays.** The video overlays found on Pinterest and cosmos ("film grain
  overlay") are all heavy light leaks, scratches and dust. They do not fit a clean explainer.

```
grainOffset(frame):
  step = floor(frame / 2)
  return (hash(step) % TILE_W, hash(step + 1) % TILE_H)   # seeded, so any frame renders alone
```

## Process

1. **Beat table first.** Before building, write one row per beat and show it to the user; ask
   about anything unclear.

   | Time | Narration or caption | The one hero | On-screen text |
   | --- | --- | --- | --- |
   | 0.0 | "Agents can't use phones" | iPhone, dimmed world | none |

2. **Build, then check your own work** (see [Review](#review)) before the final render.
3. **Match the format exactly:** aspect, resolution, fps, and a length that matches the voiceover
   or music.

## Review

Look at the real render, not the code:

- **A still from every beat:** fix anything cluttered, hard to read or overlapping.
- **Frame sequences of every camera move:** fix any jerk, jump or abrupt stop.
- **Frames at every seam:** just before, at and after each cut. No jumps, no element that pops.
- **Frames inside holds:** two frames 0.5 s apart in a held shot must differ. A frame diff of zero
  means something stopped.
- **Watch it at full speed once** with the music. Check each text is readable and nothing feels slow.
- **Pure function of time.** Every frame is computed from `t` alone, with a seeded random. No clock
  time, no real-time transitions, no randomness, so any frame renders on its own.

## Example styles

Styles used in real videos. Pick one per video; the rules above apply to all of them.

- **Scenes with slide transitions** (ghosthand Grok Bot launch): a mascot intro, a phone mockup
  next to a chat, a bento grid that grows tile by tile, a logo outro. Each scene slides out and the
  next slides in on the beat, with the camera moving inside every scene.
- **One continuous world** (cinematic explainer): the whole video is one camera move over one big
  world (a map, a desk, a board). No cuts and no slide changes; the camera glides, pushes in on
  details, pulls back to travel and dives in again. Real photos and documents drop onto the world
  as physical objects (prints, papers, clippings) where the story happens.
- **3D setup walkthrough** (ghosthand launch, `promo-video/`): toon-shaded models, one ease-out fly
  between objects, orbits and 360° turns, text in a left column.

## Related skills

- `sound-effects`: a soft sound for every movement, a different whoosh per scene, mix levels.
- `hyperframes` (only when the user mentions HyperFrames): render contract and its `motion.md`
  reference. Where it says titles must be dead still, this skill wins.
- `remotion-best-practices`: when the video is built with Remotion.
- `emil-design-eng`: UI animation in apps. Its short UI durations are for interfaces, not video.
- Example code: `grok-launch-video/` (HyperFrames, GSAP, three.js mascot) and `promo-video/`
  (headless Chrome, three.js camera rig) in the ghosthand repo
  (`~/Documents/GitHub/iphone-usb-control`).
