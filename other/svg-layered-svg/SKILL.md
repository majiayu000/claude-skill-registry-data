---
vendored_from: https://github.com/appautomaton/delineate
name: svg-layered-svg
description: >
  Turn a raster picture (painting, illustration, portrait, poster) into a layered, animated vector
  SVG drawn in a style: cel color blocks, line engraving, woodcut, or whatever the reference
  speaks, with depth planes that part and move. Works the way a painter does, coarse to fine,
  judging the whole frame by eye at every stage. Use when making a portrait or scene into
  animatable SVG, rendering a picture in a style, adding motion, parallax, or a separation view to
  a layered SVG, or reworking a portrait piece, even if the user never says "skill".
triggers:
  - svg-layered-svg
  - svg
  - layered
  - svg

---

# Layered SVG

Project paths are relative to the repository root; `ref/` files are in this skill's folder. Load a
ref file when its stage comes up, not before.

## The goal

An artwork that carries its reference's character, drawn in a style, with depth that comes apart
and moves. Mimicry, not fidelity, in what is drawn and never in how well. The reference is usually
generated: its details disagree with themselves, and copying them faithfully copies their
accidents. So you choose which details to carry; that choice is the only freedom. The standard
does not move: the finished SVG stands as a work in its own right, examined at 2:1, never an
approximation excused by the word "style".

- **Fixed:** the composition, the light, the depth. Every thing stays where it is, as large as it
  is. Do not restage the picture.
- **Interpreted:** how it is drawn. The style is a grammar (see `ref/grammar.md`): what the marks
  are, how they carry tone, how they hold form. Follow the grammar where the reference breaks it.
- **Dropped:** the generator's accidents (lines that melt into noise, forms that do not hold) and
  detail no one can read at normal size.
- **Never:** a raster inside the SVG. No `<image>`, no `data:` URIs, no slices of the reference.

**Craft** is what makes the freedom safe. Every mark is deliberate: lines begin and end with
intent, joins close, tone rolls where the style rolls, and no seam, hairline, or stray fragment
lies anywhere, between layers least of all. Where you reinterpret, the result is better made than
the reference, never looser. A dropped detail leaves a clean surface, not a hole or a smudge.

## Who decides

You hold the aesthetic judgment. The user steers direction (which picture, which style, what it
should feel like); everything below that is yours: the grammar, the layers, the tools, what to keep
and what to drop. Decide, build, show, and say why. Ask only when the direction itself is unclear.

The harness holds methods that worked once. Use one when it is the cheapest way to the effect you
have decided on; write something new, or work by hand, when it is not. One question tells you
whether a method is serving you: **who decided this edge?** Pixels may feed a field (tone,
direction, depth) that your marks respond to, and you may read positions off the reference by eye.
When pixels decide the shapes in the drawing, that is tracing, and tracing is not drawing: every
shape is drawn, by hand-read data, a model, or a generator of marks.

## Coarse to fine

Work as a painter does: the whole picture at each stage, never one corner finished while the rest
is blank. Each stage ends with a render of the full frame, looked at small and at size beside the
reference. Move on only when the stage holds; a fault in the lay-in is not fixed by detail.

1. **Read.** Look through gridded crops (`node portraits/harness/trace/look.ts grid ...`) and close
   crops where the style shows. Write the piece's notes at the top of its `scene.ts`: the things in
   depth order, the grammar (what to keep, what to reinterpret, what to drop), and where the eye
   goes.
2. **Lay in.** Depth planes and the big masses: horizon, buildings as blocks, the figure's
   silhouette, the large shadows. Author them from what you read, as polygons and curves at the
   precision this stage needs, which is little. Rendered flat, the frame should already read.
   See `ref/representation.md`.
3. **Tone.** The big values of each mass, three or four steps, in the grammar's own marks, across
   the whole frame. Seen small, the picture should now have its light.
4. **Structure.** The lines and edges that hold form: contours, seams, the edges of planes, the
   features of a face. Only those that carry the form; a busy background keeps few.
5. **Detail.** Only where the eye goes (eyes, hands, the subject's edge, what is nearest) and only
   what reads at normal size. Distant and busy regions mostly stop at stage 3 or 4.
6. **Motion.** Groups for what moves on its own, planes for parallax, plates for what moving
   uncovers. See `ref/motion.md`.
7. **Show.** Open the work for the user. See `ref/verify.md`.

Keep the build able to stop at any stage (a `STAGE` switch, or a build per stage), so you can step
back to the lay-in when something late looks wrong.

## Tools, not steps

- **Segmentation** (Segment Anything, `trace/sam.ts`) finds complex outlines fast, but it cuts the
  picture into the reference's own accidents. Reach for it when an outline is intricate and a hand
  outline would cost more than it is worth (hair against a busy ground), not to begin a piece.
- **Generated marks** (`ref/marks.md`) are how a style made of marks is drawn: a rule lays them,
  and pixels only feed the fields they respond to.
- **Tracing** (`trace/stack.ts`) is the cel grammar's way of making tone into shapes. It is right
  for a region whose style is flat color, and wrong as a way to copy a style that is made of marks.
- **Models and symbols** (`model/`) draw things with a rule (spheres, repeats, falls) as exact
  geometry, fitted to the picture once.
- **Reading by hand** (gridded crops, coordinates authored into the scene) is often the cheapest of
  all: positions, outlines, the line of a lid.

**Busy backgrounds** are where mechanical work fails. An engraver selects: the far city is tone and
a few edges that give its silhouette; the nearer planes earn their windows; the generator's clutter
goes. Decide the hierarchy at the read, keep it at every stage.

## Judging

The eye judges; numbers only catch drift.

- Every stage: the whole frame beside the reference, small (does it read?) and at size (does it
  hold?); then the same crops of both side by side where the eye goes and where planes meet
  (`look.ts crop`).
- Measure only what the grammar makes measurable. Pixel error suits a cel drawing; for a drawing
  of marks, blur both until the marks vanish and compare tone. A line shifted half a period is not
  an error.
- Ask of every crop: does it read as this style, made by a hand that understood the form? Not:
  does it match the pixels?
- At 2:1, judge the craft as a finished print is judged: every mark clean and intended, every
  join closed, nothing left that a careful hand would have tidied. A crop that resembles the
  reference but is sloppily made fails.

## Working rules

- Work on the bench, and open it for the user before the first stroke: `npm run bench`, then
  `http://localhost:5288/?piece=<piece>&panes=<reference>,previous,latest`. Saving a piece's file
  rebuilds it into a new version and every open bench redraws, so the user watches the work as it
  happens and every change is seen beside the version before it. Put what you compare against (an
  original aligned to a plate's frame) in the piece's references folder. Look through the bench
  yourself; a view you hand the user is its address.
- Experiment small: one region or one crop (`ONLY=<regex> OUT=<file>`) before a full build.
- Improve rather than preserve. An earlier output, or an earlier piece, is not a specification.
- Do not over-split (a face is one group) and do not over-draw (a hidden crowd needs no texture).
- When an approach fails, delete it. Keep only code the build uses.
- Chrome only, through `portraits/harness/browser.ts`.
- Before blaming the approach, read `ref/traps.md`.

## Pieces and the harness

A **piece** is one picture made into a drawing and a page, self-contained in
`portraits/pieces/<piece>/`: its scene and notes (`scene.ts`), `build.ts`, its own marks, models
and fitters, `motion.css`, `page.ts` (the page's words), and its outputs (`<piece>.svg`,
`index.html`). Pieces never import from each other; copy and adapt instead.

The **harness** (`portraits/harness/`) is what any picture needs: `trace/` (rasters, color, masks,
regions, plates, the cel grammar, the checks), `model/` (parametric things drawn as exact geometry),
`stage/` (layers as planes, the motion vocabulary, the page). Every module opens with a comment
saying what it does: read the headers of a folder before writing something it may already hold.
Build what a piece needs in the piece
first; move it into the harness only when it is about the medium (a grammar, depth, motion, a
geometric family) and would serve a picture with none of this one's things. Name it by what it is
(a sphere, a hatch), not by the subject it first served (a balloon, a jacket).

## Routing

| Need | Load |
|---|---|
| Reading a style, writing its grammar | `ref/grammar.md` |
| Drawing a style made of marks: lines, hatching, stipple | `ref/marks.md` |
| Layers, groups, and how each thing is drawn | `ref/representation.md` |
| Regions, plates, the cel grammar (tone-stack tracing), inpainting, bleed | `ref/tracing.md` |
| Motion, parallax, separation view, performance | `ref/motion.md` |
| Checking the result and showing it | `ref/verify.md` |
| Something looks wrong and the cause is unclear | `ref/traps.md` |

## Existing pieces

`portraits/pieces/` holds the pieces, each with its notes at the top of its `scene.ts` (one per
layer, where a piece is built in layers) and its scripts in `package.json`. Read them for the machinery: plates, hidden parts, bleed, motion, the
page. The cel pieces were traced region by region, which breaks the rule above, so do not take
their way of working as the method. The wavy-line engraving lays its tone by rule; `ref/marks.md`
says what to take from it.
