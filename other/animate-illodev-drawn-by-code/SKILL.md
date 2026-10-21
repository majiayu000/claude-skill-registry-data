---
name: animate
description: Directs the creation of a code-made animation or video in drawn-by-code, from brief to final MP4. Use it whenever the user asks for a video, animation, motion graphics, explainer, product/launch video, reel, intro, animated logo or "a test" of a style; also to resume an experiment in sandbox/. Orchestrates the other skills (engine, review, sound and the chosen style's skill).
---

# Animate: from brief to video

Every video is made **with code** (2D canvas, deterministic, frame by frame) and reviewed
by looking at real frames. Nothing is signed off without being rendered and looked at.

## 0 · Before anything

- `sh engine/setup.sh` if there is no `node_modules/` or `ffmpeg` is missing.
- Read `sandbox/INDEX.md` (what has already been tried) and the relevant style skill.
- Available styles: folders in `styles/` with their skill `.claude/skills/style-*`. If
  the request fits none of them, use the **new-style** skill before going on.

## 1 · Brief (don't animate without one)

`node engine/new.mjs <name> --style <style> --aspect 16:9 --duration <s>` creates
`sandbox/YYYY-MM-DD-<name>/` with `brief.md`, `scene.js` and `review.md`.

Fill in `brief.md` with the user (ask only what you can't infer): what it's for, the idea
in one sentence, literal on-screen text, format, music, what must not happen. If there is
a product or brand, **nothing promises more than its website**: note the source of every
claim.

**The brand's logo is traced, never drawn by eye.** Take the path from the site's SVG
(sample its curves into points, keep its proportions and gaps) and cut that as paper. An
approximated logo is the first thing the client sees: in saas-promo a «cloud with a bar»
drawn by eye was a blob that «no se parece al logo» (see the mark in `private/brand.js`).
The same goes for the **wordmark**: wherever the logo appears with its name (an app's
sidebar, a phone screen), draw the whole lockup from the SVG in the brand colour
(`BRAND.lockup`), never the mark plus the name typed in ink with the brand font: the user
caught a two-colour logo on two renders in a row.

## 2 · Shot-by-shot script

A `Time | Shot | What happens` table in the brief. Rules that have already cost us dearly:

- **Every shot, one action you can tell in a sentence with a verb** ("the marble dyes the
  sea on every beat"), not a look ("a psychedelic jellyfish"). If the sentence is "X
  floats" or "X glows", the action is missing: the style doesn't replace it.
- **Density in layers:** a moving background, secondary elements with their own rhythm
  (on the offbeat, smaller and less saturated) and a protagonist. An empty background or
  a single moving thing reads as poor, especially in psychedelic styles.
- **One evolving visual idea** (the box that empties and the vase that grows) is worth
  more than a list of scenes. Look for the object that changes over the video.
- **Vary the structure** of each block: the same formula repeated gets boring by the
  third use.
- **Cuts on the music beat.** At 120 BPM, multiples of 0.5 s. Declare `bpm` in the scene
  and `review.mjs` will warn about cuts off the beat.
- **Nothing still for more than 1 s** except the ending: visual silence looks like a bug.
- **Dress the set:** an action that reads on an empty background still looks unfinished. Give each place objects from the person's world and period (furniture they sit on, tools, a window, a floor) with their own small motions (a flame, running sand, a swaying lamp). Nobody sits on an invisible chair, and a globe gets its real continents, not blobs.
- **Bodies that move** (physics-history): a full-body rig with IK and fixed bone lengths,
  poses as spline channels (velocity carries through keys), pole points for elbows and knees,
  feet planted between steps (`sandbox/2026-09-25-physics-history/figure.js`). Offsets on the
  torso are in the body's frame, never in screen axes. Cloth that hangs (coat skirts, hair)
  follows gravity, not the limb.
- **Thrown and falling things follow physics:** fall time from g, bounces from restitution, a
  roll with friction. The hand's grab key is placed where the object stops. A throw leaves the
  hand on the release frame, and a camera that follows it keeps the relative motion
  decelerating.
- **Every joke has to read** at normal speed and without explanation.
- **Short climax** (2–3 s). Six seconds of climax is tiring.
- **Stylize from reality:** before drawing a phenomenon or a gesture (steam, smoke, water,
  fire, cloth, a jump, a walk), look at a real reference (photo or video) and note the
  3–4 traits that make it recognizable. The style simplifies those traits, it doesn't
  invent them: otherwise you get the cliché (three-tentacle steam).
- **Several styles in one video** (exquisite corpse): a **through-line** that crosses
  every segment (an object that is always visible and the most saturated thing in the
  shot) and transitions that pass through it (skill **transitions**). Each segment a
  clearly different style, not the same one with other colors. If it can close as a
  loop, close it.
- For long pieces, cross 2–3 different script proposals and keep the best of each before
  animating.

## 3 · Style test (4–7 s)

A single shot, the most representative one, at final quality. This is where the look of
the characters and typography is locked: **what is approved here doesn't change later**
(the main character changed between the style test and the animatic and it had to be
undone). Run the
**review** loop and show it to the user before going on.

## 4 · Animatic

The whole structure with a timecode and shot-name label, unpolished. It is for judging
rhythm and comprehension. Iterate versions (v1, v2…) with **review**; record in
`review.md` what didn't work in each.

## 5 · Final

Polish, audio (skill **sound**), format versions if needed (vertical 9:16 recomposed, not
cropped). Render: `node engine/render.mjs <scene.js> --size 1920`.

**The level of detail is the job.** An animatic look (merged body parts, round hands,
plain ellipses, flat paper) is not a final, however good the timing. Before calling a
piece final, crop every element at full resolution and hold it to the style's detail bar
(paper-cutout: «Detail» in its skill). Budget for it: in a replica the detail pass took
several times longer than the animatic, and it is what the user judges first.

For big pieces, split the detail work: one file per object/prop with a small drawer
contract (`(g, x, y, s, t, part?)`), and give groups of objects to parallel agents with a
written brief; keep choreography and shared kits with the lead.

For a marketing piece, the three ideas that carried saas-promo: **one evolving idea**
(a buried desk that each feature clears), **a set piece that carries a sequence** (a twine of
invoices feeding into a slot gives the block one verb and fills the frame), and **show the
product waiting for the user** when the claim is «you approve» (hover, a button ring
pulsing on the beats, a turning hourglass: three signals read at speed).

A round mechanical object seen at an angle (a lens, a wheel, a tube) is projected from 3D geometry with a camera, never hand-placed ellipses (physics-history scope3d.js). A move from a macro to a wide shot of the same subject is one continuous camera, never a cut between two drawings of it: draw the subject once at full detail (the macro's eye inside the whole head, head-galileo.js), dolly the camera (distance shrinks, focal length fixed, so far layers barely scale and the stars not at all), and put hands on a 3D prop in the prop's own projected frame so they stay on it at every size (hands-galileo.js). To move the camera into a character's point of view, have the character move out of the axis first (he pulls back, astonished), then let the camera take his place. Arms seen from the side are foreshortened: use the seen bone lengths, or the elbow juts out. Hands follow the skill **hands** (reference first, handedness, what each grip shows, one skin, a hand check image approved before any render). The sun, the moon and the sky only keep still under a pure dolly: when the camera pans, tilts or zooms to follow the action, give them a far-layer share of that motion, or they read as pasted onto the screen. A morph between striped objects rolls the camera first so the stripes run the same way; on a riso press a crossfade greys both images, so prefer a match cut on the beat (physics-history). Parallel block agents (physics-history: four figures in parallel, joins intact): give every join as an exact screen state ("the ground plus one amber line, 8 wide, full width at y = 450"), so the cut is a match the lead can check; let a segment call its neighbour's drawing for its first frames; wrap every segment file in an IIFE (they share one global scope); give each agent's dev scene its own folder, or their stills and reviews overwrite each other. One brief for all (see `sandbox/2026-09-24-saas-promo` history),
the approved frames as the bar, on-screen text only through copy keys, shared kits
read-only, the lead merges by file. Ask each for a shot list with times: it is also the cue
sheet for the sound.

## How to organize a large scene

For more than one shot, the scene declares `shots: [[start, end, 'Name'], …]` and `draw`
dispatches with `Motion.shotAt(shots, t)`. One function per shot (`shotX(g, t)`), shared
pieces (characters, props) in functions or in a separate file in the experiment folder,
loaded from `uses`.

## At the end of every work session

1. `review.md` up to date and the `sandbox/INDEX.md` row with status and main lesson.
2. Generalizable lessons moved up to their skill (see **review**).
3. Commit with the experiment and the skills touched. The latest render goes in
   `render/<name>.mp4`, re-encoded small (`ffmpeg -i out/x.mp4 -c:v libx264 -crf 26
   -preset slow -c:a aac -b:a 160k -movflags +faststart render/<name>.mp4`), overwriting
   the previous round's; no third-party footage or audio in it (`-an` when the soundtrack
   is the reference's). Then its strip: `node engine/strip.mjs render/<name>.mp4
   render/strip.jpg --at <the moments that tell it>`; a new experiment gets a paragraph and
   its GIF in the README's gallery (`node engine/gif.mjs render/<name>.mp4 render/<name>.gif
   --clips a-b,c-d`, under ~5 MB), a new style a `styles/<style>/README.md` and
   `strip.jpg` (see any style folder). Full-quality MP4s and frames (`out/`) are not
   committed; the contact sheet (`review/sheet.jpg`) is, it is the visual history.

## Lessons

- 2026-09-25 · physics-history v2 · A likeness at a small scale lives in its signature shapes, exaggerated: young Einstein with neat short hair and a thin moustache read as Tesla; the tousled volume and a bushy moustache pushed bigger (the head's `bold` option) read as Einstein. Crop the head at its on-screen size and ask «who is this?».
- 2026-09-25 · physics-history v2 · A solid box drawn from 3D is filled only on the faces turned to the camera, and only their edges are drawn: one hidden edge on top of an opaque face turns the box into its own inside.
- 2026-09-25 · physics-history v2 · Something inside a container is drawn in layers: the rim's far edges, the contents, the near walls and edges, then whatever rests on the rim (the paws) last. No border may cross the character.
- 2026-09-25 · physics-history v2 · A physics idea is worth more as a picture than as a prop: the user preferred a black hole (spaghettification, a dive to black) to a Sun, and an X-ray scan plus a frame splitting into worlds that collapse into one to a literal wooden crate. Propose the version where the physics *is* the camera move or the edit.
- 2026-09-25 · physics-history v2 · A frame split into N worlds: each cell draws the whole scene with a uniform scale that frames the subject, clipped to the cell (never a non-uniform squash); the collapse shrinks the other cells into the chosen one while it grows to full frame.
- 2026-09-25 · physics-history v2 · An adversarial review by parallel agents (one per pair of scenes, one for the whole film: joins, pacing, sound sync) on the real render found ~50 issues the author had stopped seeing; verify each on its frames, filter, then fix one at a time with the user.
- 2026-09-25 · physics-history v2 · Transitions the user liked were continuous physical ones: the same object carried across (the coil stays still while the lab assembles round it; the ray drawn identically on both sides of the cut and followed by the camera; light entered in pulses). Generic wipes and kaleidoscope irises read as filler.
- 2026-09-25 · physics-history v2 · Anything tied to a prop in a moving camera (a glow on a tube, a ray's origin) is drawn in the prop's own layer, not in screen space, or it slides off the prop as the camera drifts.
- 2026-09-25 · physics-history v2 · A reveal must not answer the question it poses: when worlds collapse, shrink all of them together, never let the survivor grow out first. Show «both at once» literally (one box half alive, half dead) before splitting it.
- 2026-09-27 · pyramid-engraving · Stills approved in the cloud hid what only motion shows: a full-frame filter reads as a dirty lens, cuts through black read as jumps, and camera keys with central-difference tangents overshoot and come back (a zigzag). Render the whole film early, watch it moving, and scan the camera per frame (speed, turn, reversals) before showing it.
- 2026-09-30 · external product promo · A camera «lift» (zoom out and back in) during a travel between stations uses `sin²` of the progress, not `sin`: it must start and end at zero speed, or each travel spikes at both ends.
- 2026-09-30 · external product promo · Isometric world of stations laid out in a zigzag: the station two steps ahead lands straight below on screen and leaks into the close framing behind the titles; space them so it stays out of frame. An icon on an isometric lid (a tick on a button) is drawn in screen space squashed like the lid's ellipse (0.577 vertically), not through the face's transform, which shears it.
- 2026-09-30 · external product promo · With a narrator, derive every time (cuts, props, sound cues) from the voice's alignment through one shared timeline file, never from numbers typed in the scene: the user changed the voice (a slight foreign accent) after four styles were built, and only what read the timeline re-timed itself. Keep the scene's `duration` next to it, since the scene declares it before loading anything.
- 2026-10-14 · external explainer · A recreated product interface paced like a motion promo reads «brusco y rápido»: camera moves of 0.5–0.7 s on a cubic ease (peak speed 3× the average), a cursor crossing in 0.6 s and state changes in 0.2–0.3 s. For an explainer, camera moves of 1.1–1.3 s on a sine ease (peak 1.6×) with a pause to read between gestures, ~1 s cursor travels and 0.4–0.6 s state changes; frame each move so the frame edges fall in the gaps between cards, never across one.
- 2026-10-14 · external explainer · In a voice-led explainer each scene's payoff (the chain that breaks, the date that matters, «accepted») tends to land on the last word of its sentence, and if the camera leaves 0.1–0.4 s later the payoff is on screen for a quarter of a second. Hold it 1–1.5 s before the camera moves: lengthen the voice gap after that sentence (re-assembling cached takes costs nothing) instead of shortening the travels, and stretch the music to match with a pitch-preserving time-stretch (rubberband) when the change is a few per cent. Tie titles to the word they repeat, never ahead of the voice, and keep the haze behind a title until its letters are gone: brand-coloured letters vanish for a few frames over a same-coloured object if both leave together.
