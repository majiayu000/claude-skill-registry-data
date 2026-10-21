---
name: review
description: Review and self-improvement loop for drawn-by-code. Use it after EVERY render or visible change to a scene, whenever the user gives feedback on a video ("this doesn't read", "faster", "I like X"), and when closing an experiment. Runs the automatic critique on real frames, fixes the scene and turns what was learned into permanent changes to the skills and the engine.
---

# Review: critique, fix and learn

Every test has to leave the repo better than it found it. The loop has two halves: the
**automatic critique** (without the user, before showing them anything) and the **user's
feedback**. Both end the same way: in changes to the scene and, if the lesson
generalizes, in changes to the skills or the engine.

## A · Automatic critique (before showing the user anything)

1. `node engine/review.mjs <scene.js>` → read `review/auto.md` and look at
   `review/sheet.jpg` with the Read tool. Objective warnings (errors, Non-deterministic,
   Cuts off the beat, still stretches) **are always fixed**, or you justify in `review.md`
   why they are intentional.
2. Full-size stills of the key moments:
   `node engine/render.mjs <scene.js> --at 1.2,3.5,5.8` and look at them (out/stills/).
   Look especially at the moments when text is read, the contacts (hands grabbing,
   things colliding) and the last frame.
3. Go through the **general checklist** (below) and the **style checklist** (in its
   skill). Write each flaw as *what you see · at which second · why it fails*.
4. Fix, go back to 1. **At most 3 automatic rounds**; if something doesn't improve in 3,
   raise it with the user as an open question instead of going round in circles.
5. Log the round in `review.md`: `### Round N (auto)`, what you saw, what you changed.

Be harsh: the most common failure of self-critique is approving out of fatigue. If you
hesitate between "it reads" and "it doesn't read", **it doesn't read**.

### General checklist

- **Legibility:** every text stays on screen at least ~0.4 s per short word + 1 s, with
  enough contrast and without covering anything. Nothing important in the outer 5 % (in
  vertical, keep the bottom 250 px and the top 150 free, where social apps put their
  buttons).
- **Clarity:** every shot is understood without sound and without explanation, and what
  happens can be told in one sentence with a verb (if you can only describe the look, the
  action is missing). A single focus of attention at a time; if two things move, one
  leads.
- **Density:** are there at least three layers (moving background, secondary elements,
  protagonist)? Any moment with a single thing moving on an empty background?
- **Motion:** anticipation and settle (nothing starts or stops dead unless on purpose),
  ease curves, nothing still for more than 1 s except the ending, nothing jittering
  unintentionally.
- **Photosensitivity:** no more than 3 flashes per second (abrupt changes in overall
  brightness). `review.mjs` measures them; in psychedelic videos it is mandatory.
- **Rhythm:** cuts on the beat; visual hits (impacts, stamps, appearances) land on the
  beat too.
- **Origin and physics:** everything that emanates (steam, smoke, sparks, liquid, papers
  coming out of a box) is visibly born at its source and not behind or above it. Things
  rest where they should and fall downward. Check it in a still of the instant it
  appears.
- **Continuity:** characters and objects identical across shots and to the approved style
  test; gaze and movement direction consistent across cuts.
- **Composition:** rule of thirds or deliberate symmetry, level horizon unless
  intentional, consistent margins, clear size hierarchy.
- **Accuracy:** nothing promises more than the source (website, brief). Third-party
  brands only as generic icons.
- **Ending:** the last frame holds up as a poster and the final message reads in full.
- **Detail:** crop each element at full resolution (`render.mjs --at` and zoom, or
  `reference.mjs compare --crop`) and hold it to the style's detail bar: separate pieces,
  organic shapes, textures that say what the material is, real hands. «It reads» is not
  enough; «it could be a frame of a finished film» is.
- **The detail gate:** with a reference, `engine/detail.mjs` must PASS before anything is shown (CLAUDE.md → «The detail bar»); without one, crop every element at full resolution. Evident details are never left for the user to find.
- **Hands and brand:** at every contact frame check each hand (right side, right view,
  never through what it holds; style skill → «Detail») and put the logo next to the
  client's SVG at the same size.

### Replicas and studies of a reference (`engine/reference.mjs`)

Work from measurements, never from eyeballing:

1. `sheets` for the shot list; exact cut frames from a per-frame colour probe (cuts land on
   frames, not seconds; seek at `frame/24 − 0.004` or `-ss` may land a frame late).
2. `colors` for every palette; `track --color` for anything that moves (centre, box, area
   per frame): the reference animates on twos, so author **one row per drawing** (1/12 s)
   with position, size, squash and expression, not a smooth curve.
3. Build, then **measure your own render the same way** (render the stretch small, run the
   same probe) to calibrate sizes before comparing by eye.
4. `compare --times … --crop x,y,w,h` per element at full resolution until the side-by-side
   shows the same pieces, shapes, colours, textures and layering. The diff number helps; the
   eyes decide.
5. Big replicas parallelise well: one file per object and one agent per group of objects,
   each with a written brief (why, contract, tools, rules, report). Keep shared files
   (choreography, common kit) with the lead and merge by file.

## B · User feedback

1. Show them the result: MP4 (`render.mjs`) and the contact sheet. Tell them in one line
   what you fixed on your own and what doubts remain.
2. Record their feedback **verbatim** in `review.md` (`### Round N (user)`), and below
   it your translation into concrete changes.
3. Apply, go back to A.

## C · Distill: from the experiment to the skills

When closing each round with user feedback, and when closing the experiment, ask of each
lesson: **would it help in another video?**

| The lesson is about… | It goes to… |
|---|---|
| this particular video (this text, this brand) | only `review.md` |
| the style (how the paper looks, the palette, the characters) | the `style-*` skill: *Rules*, *Checklist* or *Lessons* |
| a client's or brand's rule (their typeface, banned motifs, claims) | the experiment's `brief.md` only, never a style skill: a style skill must hold for any client |
| narrative, rhythm, script, legibility | `animate/SKILL.md` or the general checklist here |
| a technical bug, something slow, a missing utility | fix it in `engine/` or in the kit and note it in `engine/SKILL.md` |
| something the automatic review could have caught and didn't | extend `engine/review.mjs` |
| sound | `sound/SKILL.md` |

Lesson format: `- YYYY-MM-DD · <experiment> · <rule in the imperative, one line>`.
Write rules, not anecdotes: "Stamps are seen from above, never sideways against a wall",
not "the stamp in round 2 looked weird".

**Skill maintenance:** when a *Lessons* section goes past ~15 entries, consolidate: move
the recurring ones up to *Rules* or the *Checklist*, delete the obsolete ones. A long,
contradictory skill is worse than a short one. If a lesson contradicts a rule, the most
recent one confirmed by the user wins: fix the rule.

Update the experiment's row in `sandbox/INDEX.md` and commit:
`review(<experiment>): round N · <main lesson>`, with the skills touched in the same
commit, so it shows which test produced which change.

## Lessons

<!-- Lessons about the review process itself. -->
- 2026-09-24 · coffee-first · The sheet at 480 px doesn't show facial details (closed eyes that seemed to look down): always look at full-size stills of close-ups.
- 2026-09-24 · coffee-first · When you spot by eye a flaw that `review.mjs` could have measured (a hole at the edge), extend `review.mjs` and test it with a deliberately broken scene before trusting it.
- 2026-09-24 · coffee-first · I judged the steam by its shape and not by its origin, and the user saw it came out from behind the cup. For every element that appears, ask where it comes from (now in the checklist).
- 2026-09-24 · exquisite-corpse · The image-difference «jumps» warning gave false positives on dense patterns and didn't measure what matters: `review.mjs` now counts flashes frame by frame and separates jumps from cuts (tested with a strobing scene).
- 2026-09-24 · exquisite-corpse · In a long piece, first review with `--times` the instants you changed; the full sheet only when closing the round.
- 2026-09-24 · exquisite-corpse · I approved a jellyfish that was only a look: my critique checked style and legibility but not "what happens?". It is now in the checklist (Clarity and Density).
- 2026-09-24 · what-do-you-love · I «compared» a replica at whole-frame size and called it close; the user saw at once that the dog, the girl and the ring had no craft. Crop every element at full resolution, and measure (track/colors/segmentation) instead of guessing positions and sizes.
- 2026-09-29 · external trailer · Show new graphics already cut into the film, in order and at speed: a test reel that grouped the pieces by type (four title cards in a row) was judged as the film («it needs dynamism; scene, title, scene, title»).
- 2026-09-29 · external trailer · A character composited into a photo must respect every layer the photo puts in front of it: masking only a box's front face, while paper hanging over its rim stayed behind the character, read as pasted. Trace the foreground pieces from the photo zoomed 4× and repaint them over the character. And a character standing right against an object it overlaps reads as floating: set it clear of the object and keep its shadow on the ground while it hops.
- 2026-09-29 · external police parody · A highlight on a line of printed text inside a character is invisible when the character's own pose covers that line (hands over the chest). If the story is "the data comes out", make the data leave as its own object (a small card with a flash) and fly it toward the camera, first sideways so it never crosses the face, and away from the corner that holds the logo. Then cut to where it lands.
- 2026-09-29 · external police parody · Two camera flashes 0.4 s apart trip the photosensitivity check (more than 3 brightness changes per second): space paired flashes a second apart instead of dimming them. Before placing characters on new photo backgrounds, render the plates with a labelled grid in scene units and read off table edges and horizons from it; guessing from the source image's pixels puts feet in the air.
- 2026-10-02 · product videos (four styles) · A reviewer who only sees the film found what the author's own checks missed (effects louder than the voice, a final consonant cut, flaps cutting a logo), because the checks measured less than the ear hears: when a check passes and a person disagrees, test the instrument first (band, weighting, silence handling, a transcription that fills in missing letters) before defending the result.
- 2026-10-02 · product videos · Never retry a check in a loop keyed on its exit code when it exits non-zero on a mismatch by design: the loop repeated eighteen paid calls three times. Run it once and read the diff.
