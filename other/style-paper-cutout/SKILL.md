---
name: style-paper-cutout
description: Paper-cutout animation style drawn with code (torn edges, marker fill, grain, handwriting), the style of a previous paper-cutout short. Use it when asked for a warm, handmade or character video, or anything "paper/collage/cutout/stop-motion"-like, or when working with styles/paper-cutout/.
---

# Style · Paper cutout

Approved reference: `sandbox/2026-09-24-coffee-first/` (look at `review/sheet.jpg`
before starting).

## Code

- `styles/paper-cutout/paper.js` → `Paper`: `cutout(ctx, poly, color, seed, o)` is the
  base piece (torn white edge + color + marker strokes + pasted-paper shadow).
  Shapes: `roundRect`, `ellipse`, `circleUnion` (clouds, soft silhouettes), `noodle`
  (strips for arms and legs), `bezier`. Strokes: `markerStroke`, `scribble` (illegible
  writing), `marker` (texture). `grainTile` for grain.
- `styles/paper-cutout/kit.js` → `PaperKit.make(env, { font })`: `hand` (text that writes
  itself), `title` (text + underline), `sfxWord` («zap!»), `paperBg`, `glow`, `sheet`,
  `ticket`, `wisp` (a wisp of steam or smoke), `grainPost` and the `COL` palette.
- `styles/paper-cutout/detail.js` → `PaperDetail` (see `styles/paper-cutout/showcase/`):
  shapes `spline`, `cspline` (centripetal: no bulge at corners), `taper` (strip with a
  width per control point: tentacles, stems, tails), `curl` (pose variation of a
  centreline); printed papers `knit`, `rib`, `newsprint`, `wordBars`, `cursive`,
  `sheetMusic`, `mapPaper` (`rings` + `wobblyLine`), `woodGrain`, `strands`; marks
  `markerPath` (a marker line as a chain of strokes, revealable by arc length), `crease`,
  `punch` (a hole with a torn rim); `hand` (open, wave, pinch, fist with thumb and cuff);
  `shade` (returns hex).
- Characters as **puppets**: one function per character that takes `{ t, armL, armR,
  legL, legR, look, blink, … }` and is drawn with the origin **between the feet** (up is
  negative). Arms and legs are `noodle`s through shoulder-elbow-hand.
- If the hand rests on the body, the arm is painted in two passes (all of it behind, and
  from the elbow in front) so it reads as an arm akimbo and not as a mug handle.

## Style rules

- **Nothing boils:** every piece has its fixed seed. The tear and the texture are the
  same in every frame. Life comes from motion (breathing, swaying, blinking), not from
  a jittering outline.
- **Palette:** dark, muted background (aubergine `#3a2146`) with saturated pieces on top
  (orange `#f2643c`, mint `#6cc9a1`, yellow `#e9b949`). Ink `#2a1826`, never pure
  black. Cream `#f4ecda` for text on dark.
- **White edge** on every main piece; backgrounds have no edge.
- **Pasted-paper shadow**, short and offset down-right: the light is always the same
  across the whole piece.
- **Lettering:** Patrick Hand for everything handwritten (labels, notes, onomatopoeia).
  Brand/CTA text in the brand's typeface, never the handwritten font. An orange marker
  underline drawn right after the text.
- **Characters:** heavy-lidded eyes with a sidelong glance, a crooked half-smile; limbs
  one shade darker than the body. No blush unless it's for kids.
- **Camera:** frontal shots like a paper puppet theater; moves are gentle pushes (`cam`
  with `inOut`). Impacts are seen from above or head-on, never in profile against a wall.
- **What changes shape is animated like stop-motion:** steam, smoke, water, flames… are
  fixed cutouts (a sprite with its seed) that shift, rotate, scale and fade out, several
  staggered. Never regenerate, every frame, an outline with a torn edge that deforms: the
  tear is recomputed and boils.
  Whatever comes out of a container is painted **in front**, in the container's
  coordinates, and clipped (`clip`) to «above the surface» ∪ «the surface ellipse»; the
  piece starts hidden under the surface and emerges as it rises. Painting it behind the
  container makes it come out from behind the rim.
- **Steam and smoke = `kit.wisp`**, translucent tissue paper and not strips of opaque
  paper: it is born very thin, widens as it rises, drifts to one side (all wisps to the
  same side), curls and ends in a point. Few wisps (2–3 sources). Constant-width, opaque,
  vertical strips read as tentacles.
- **Eyes:** open, white + pupil + heavy lid (one shade darker than the face) that never
  lifts all the way. Closed, the lid covers **all** the white and the curved lash goes on
  top; if white shows, it reads «looking down», not «asleep».
- **Forbidden:** soft gradients and pure black.

## Detail (the bar)

The difference between a finished film and an animatic is detail. Every element is worked
until a full-resolution crop of it could pass for the reference (or for a finished film):

- **Every part is its own piece of paper**, cut once, layered in a deliberate order: a dog
  is tail, body, near leg, back spot, haunch, chest patch, three paws, head, collar, tag,
  ear, muzzle, nose, tongue, eye with a catch-light. Decide the layering from whose white
  border is on top, never from where a shape seems to end.
- **Organic shapes are splines** (`PaperDetail.spline`, centripetal where a long segment
  meets a short one), never ellipses or polygons standing in for them. Straight-edged paper
  (cones, bands, tags, pages) stays a torn polygon: a spline makes it bulge.
- **Textures say what the paper is:** knit on sweaters, rib on cuffs, newsprint (columns of
  word bars, headlines, photo blocks), handwriting (`PaperDetail.cursive`: arches, loops,
  dips), sheet music, maps (contour rings, a river, a red dashed route), wood grain.
  Collage props are cut from printed paper.
- **Hands are never circles (or mittens):** every finger is its own tapered piece with a
  round tip, lengths index < middle > ring > pinky, the fingers under others a shade darker,
  knuckle creases, a subtle nail on the backs; the thumb its own piece with the web to the
  index; a ribbed cuff (ribs along the arm) and the sleeve behind. A fist seen from the front
  is four short bars (≈2.5 widths long) side by side, each overlapping the next, the thumb
  across. `PaperDetail.hand(g, x, y, size, rot, pose, o)` does all this: poses open, wave,
  point, fist, pinch/hold, rest, grip; `o.part: 'back' | 'front'` puts a held note, pen or
  mug handle between the fingers and the thumb (`PaperDetail.handAnchor(pose)` says where).
- **Hands the right way round.** Pass `o.side: 'right' | 'left'` (the character's hand; a
  character facing the camera has her right hand on the left of the image), never
  `o.mirror` by habit: the poses are drawn as different hands (back views of a right hand,
  palm-side views of a left hand), and mirroring «the hand on the left» put the thumb on the
  wrong side of every back view: the user saw hands «al revés». Pick the view that matches
  what the camera sees: `palm` (palm to the camera: stop, whoa), `open`/`wave` (back to the
  camera), `pointBack` (POV finger, or pointing away: the back with its nail) vs `point`
  (pointing at the camera), `wrap` round a mug's body (fingers across its front, thumb
  behind, handle turned away; `Laura.wrap` in saas-promo solves the wrist from the mug),
  `edge` (fingers hooked over the top of something held from behind).
- **Hands never pass through things.** Decide the depth of each hand against what it
  touches: behind a pile, draw the hand with the arm (the pile covers it); holding the pile,
  only the fingers come over its edge (`edge`); in front, the whole arm is in front too. An
  arm behind with its hand in front reads as the hand going through the paper.
- **No arm stretched in from the frame's edge.** A straight sleeve from a corner to a prop
  (no elbow, no shoulder) reads as a tube. Frame the elbow, or let the prop move by itself
  (a stamp that comes down on its own: the product does it).
- **Cut small pieces at a big authoring scale** (a hand at palm = 200 units, then scaled):
  `Paper.cutout`'s border, jag, fibres and grain are in absolute units, so cut at a 60-unit
  palm they swamp the fingers. Pick the sprite resolution from `g.getTransform()` and keep
  the white border ≥ ~1.3 output px, so miniatures still show where one finger ends.
- **Paper that moves bends and turns in perspective** (`Motion.quad`); tears follow the
  perforation (square tabs, scraps flying); folds happen step by step with creases.
- **Replacement animation, not deformation:** what the reference redraws (waves, tentacles,
  steam, petals opening) is 2–4 cached drawings swapped on twos, never one outline bent per
  frame. Only scale and move a torn piece; never re-tear it.
- **Bands and rings are two strips** (the back half before the body, the front half after).
  Holes are punched (`destination-out`) inside a torn rim.
- **Marker lines are chains of short overlapping strokes** with lighter edges; reveal them
  by arc length with all the random numbers drawn up front, so nothing boils.
- **Lettering is felt-tip:** a thin darker core inside a lighter rim (see `WL.write` with
  `halo` in the what-do-you-love replica), not a bold fill.
- **Sets are full, in depth:** a back layer (textured wall, window with a view, shelves
  full of objects, pinboard), a mid layer (the working surface crowded with the tools of
  the trade, each in pieces) and a front layer (something big at the frame edge). A few
  props spread over a flat colour reads as «five things in an empty space».
- **Every flat surface wears a printed or textured paper** (wallpaper motif, wood grain,
  cork speckle, handwriting): a plain marker field is what reads as «empty». Zones kept free
  for the action stay calm (wallpaper + one quiet object), not bare.
- **Close-ups keep the world around them:** a screen or a document filling the frame
  still shows the room behind (big, a touch dimmed) and life on its edges (sticky notes,
  a sticker); a flat dark field around it reads as a slide.
- **No `destination-out` inside a cached set sprite:** it cuts through everything painted
  before it in that sprite. Paint holes as a dark fill with a torn rim.
- **Original pieces need a reference too:** with no film to copy, build against the best
  traced piece in the repo (the replica's fist, its interior) or a real photo, and crop
  both side by side before calling it done.
- **Miniatures are redrawn chunkier** (bigger cells, thicker lines, fewer pieces), not just
  scaled down; give drawers a miniature variant.
- Collage towns and printed-paper planes: `sandbox/2026-09-24-what-do-you-love/segments/town.js`
  (houses of sheet music, newsprint, maps; sticky-note windows; a plane of any printed
  paper pinned by three points).
- `styles/paper-cutout/showcase/` renders the detail kit; `sandbox/2026-09-24-what-do-you-love/segments/things/`
  has one fully detailed object per file to copy from (dog, tree, bread, rain, words,
  music, sea, math, stars, octopus, tea, flowers, cat).

## Style checklist

- [ ] Does any outline or texture change between two consecutive frames without the piece moving?
- [ ] Do all main pieces have a white edge and a shadow toward the same side?
- [ ] Is there any soft gradient or pure black?
- [ ] Is brand text in the brand's typeface and handwriting in Patrick Hand?
- [ ] Are the characters identical to their approved version (proportions, colors, face)?
- [ ] Are QR codes, stamps and documents complete and well made, not half-done?
- [ ] Is the grain visible across the whole image, text included?
- [ ] Is anything that changes shape (steam, smoke) made of fixed pieces and not by deforming a torn outline?
- [ ] Crop every element at full resolution: is each part its own piece, with its texture, its highlight and its layering?
- [ ] Any hand drawn as a circle, any shape that is a plain ellipse or polygon where it should be organic?
- [ ] Every hand: the right hand (`side`), the right view (palm / back / POV), and in front of or behind what it touches, never through it? Mugs held round the body, not by a sideways fist?

## Lessons

- 2026-09-23 · paper-short · Several characters in a row jumping at once read as a bug: stagger them or give one of them the lead.
- 2026-09-23 · paper-short · Stamps and impacts are seen from above (the rubber comes down toward the camera), not sideways against a wall.
- 2026-09-23 · paper-short · QR codes, stamps and documents are drawn complete and for real: half-made objects look like a bug.
- 2026-09-23 · paper-short · A visual joke that needs explaining is cut.
- 2026-09-23 · paper-short · A different setting per block; the same book of pages for everything gets repetitive.
- 2026-09-23 · paper-short · Characters always alive: they breathe, sway and blink with `t` even when not acting.
- 2026-09-24 · coffee-first · Steam as a deformed strip without an edge looked flat and off-style; as fixed cutouts that rise and fade, it works (now in Rules).
- 2026-09-24 · coffee-first · A character-object (the cup) reads as a character with just heavy-lidded eyes and a marker mouth: no arms needed for a short shot.
- 2026-09-24 · coffee-first · The user saw «tentacles» where I saw steam: constant-width, opaque, vertical strips. The good recipe is in Rules (`kit.wisp`).
- 2026-09-24 · exquisite-corpse · `markerStroke` sets its own `globalAlpha`: to fade it out, pass the alpha as a parameter, don't set it beforehand.
- 2026-09-24 · what-do-you-love · The old ban on stars and sparkles came from a client brief, not from the style; a paper-cutout reference uses both. Brand rules live in the brief, not here.
- 2026-09-24 · what-do-you-love · The user: «every element has to go to detail». A dog of five ellipses, a ring drawn as one stroke, round hands and polygon shapes read as low effort next to a reference built piece by piece. The bar is now in «Detail».
- 2026-09-24 · what-do-you-love · `PaperDetail.shade` returned hsla and `Paper.marker` only parses hex: every shaded piece became a brown blob. Colour helpers return hex.
- 2026-09-24 · saas-promo · Style test rejected on detail: «las manos parecen muñones» and «5 cosas repartidas en un espacio hueco». Without a reference I stopped at «it reads»; original work is held to the same bar (see «Detail»: full sets, real hands).
- 2026-09-24 · saas-promo · A pile that grows: every landing squashes the item AND the pile under it (two drawings: 1.07/0.88, 0.97/1.04); items landing alone on a still pile look pasted.
- 2026-09-24 · saas-promo · A logo shown big is re-cut at its display scale (its own sprite key per size); scaling up the small cut shows soft, fat torn edges.
- 2026-09-24 · saas-promo · Big flat shapes (a logo cloud, a card) need layered torn volume: a darker under-layer offset down, a lighter top lobe, a highlight edge; one flat fill reads as a sticker.
- 2026-09-24 · saas-promo · An arm holding a mass (a pile, a mug) goes behind it with only the hand in front; a `grip` rotated ±π/2 holds vertical things (a stamp's neck, a mug handle), bend the wrist so the forearm can come from anywhere.
- 2026-09-24 · saas-promo · A phone held in a close-up: an `open` hand turned sideways behind it, only the fingertips curling round the far edge. A `pinch` thumb over the screen reads as a stump.
- 2026-09-24 · saas-promo · Shadows of floating paper need the torn silhouette of the piece (a sprite), never a rectangle: a rectangle reads as a grey box.
- 2026-09-24 · saas-promo · A mug from above with a curved crema arc under a glint reads as a smiley: keep highlights off the lower half of round things seen from above.
- 2026-09-24 · saas-promo · Full-frame boards laid side by side leave gaps where torn edges meet: paint a dark base under them.
- 2026-09-24 · saas-promo · To show a shared cached set «tidied», redraw its base pieces with the same seeds and pull the kept objects from the original sprite through a clip: the seams match exactly.
- 2026-09-24 · saas-promo · An end card that unfolds reads best as three or four fold drawings on twos; its content lands on the beats after it opens (mark, line, button, small print).
- 2026-09-24 · saas-promo · Animatic v1: the user saw «manos que atraviesan cosas», odd perspectives and «coge el café al revés». Root cause: `o.mirror` used as «the hand on the left of the image» while the poses are drawn as different hands. Now `o.side`, new views (palm, pointBack, wrap, edge) and the rules in «Detail».
- 2026-09-24 · readme-cover · A card held from above with 'hold' read as a mitten: the thumb lay flat across the top edge under a big palm. The user's fix: four fingers over the front, the thumb behind (pose 'wrap', thumb = part back), from above, leaving what is printed on the card clear.
- 2026-10-05 · promptaprompt · `kit.hand` placed each letter by measuring the text up to it, and a ligature («fi» in Patrick Hand) shrinks that run: the next letter landed on the one before and «perfil» read «perfl». Letters are now laid out by their own widths (and `textW` sums the same, so underlines end with the text).
