---
name: hands
description: How to draw hands in drawn-by-code, in any style. Use it before drawing, redrawing or reviewing any hand, and whenever a character holds, grips, carries, throws, touches or points at something, or the user complains about a hand. Covers the reference-first workflow, handedness, the grips and what is visible from each side, proportions, one-skin drawing, and the hand check sheet that must pass before any render.
---

# Hands

Hands are where the viewer catches a fake first, and where this repo has failed most often. In
physics-history the hands took rounds 13 to 16b, many of them making things worse, for
three reasons:
- the grip was guessed instead of copied;
- the hand was mirrored (a left hand's geometry on a right arm);
- images were sent without being looked at.

Follow this page every time a hand is on screen.

## The workflow (in this order, every time)

1. **Reference first.** Before drawing any grip, find or ask for a reference of that grip
   seen from the camera's side: a drawing or a photo, or the user's own hand. Write in the
   code comment which reference it follows. Never invent a grip from memory. The user's
   references are the best ones; ask for one as soon as a grip is new.
2. **Decide what is visible from the camera.** Grips hide a lot: a fist round a bar seen
   from the fingers' side shows no thumb at all. Draw only what the reference shows. A thumb
   that "should be there" drawn where it would be hidden is the typical mistake.
3. **Check handedness against a real hand in the same pose, forearm included.** For a right
   hand, with the palm facing N and the fingers pointing F, the thumb is on the side
   F × N; a left hand has it on N × F. The grip follows the forearm's direction and the
   palm's side, not the object. Write the result in a comment, for example: `right hand,
   forearm from below, palm on the far side: index at +a, thumb hidden`.
4. **Draw it on a hand check sheet** (see below) at full size, on its real prop, from the
   scene's camera, before putting it in the scene.
5. **Look at the sheet as a critic** before sending it (see «Looking»). Then show it to the
   user as an image. **No render until the user approves the hands in an image.**
6. **Change only what the user flags.** If they say the thumb is on the wrong side, move
   the thumb and nothing else. Never redesign a grip they already approved.

## What each common grip shows

| Grip | Seen from | Visible | Hidden |
|---|---|---|---|
| Fist round a bar (power grip), fingers towards the camera | the fingers' side | four fingers wrapping the near face, pressed together, their backs to us; a crease per joint; lines between the fingers; tips curling over the far edge; below the bar, the hand's edge down to the wrist | the thumb, on the far side of the bar |
| Fist round a bar, the back of the hand towards the camera | the back of the hand | knuckles' row near one edge, the fingers going over that edge and away, tendons | the fingertips; the thumb except its root at the heel |
| Hand reaching over a bar from the far side | across the bar | fingertips curling over the top and down the near face, with nails | the palm, the thumb, the wrist |
| A figure in profile facing right holding something up with its right hand (camera on its right) | the little finger's side | the hand's edge from the wrist to the knuckle in profile; the little finger nearest, wrapping the object's front; the others stepped behind | the thumb, on the far side of the hand |
| Holding a round object (an apple) | the side | the fingers cupping under it, the thumb on top or on the near side, and more hand than object: a hand is about 2.3 times as long as an apple | the palm behind the object |
| Pinch (small object) | the side | the thumb and index tips meeting, the other fingers curled loosely | the palm |
| Open hand, relaxed | any | fingers slightly curled, the middle the longest, the thumb lower and turned | nothing |

In a power grip the thumb always closes the grip from the opposite side to the fingers.
It never lies along the bar or on top of the fingers' side.

## Proportions (adult, world units ≈ 1.35 mm)

- Palm: 62 wide and 70 from the wrist crease to the knuckles.
- Fingers, as proximal/middle/distal phalanges:
  - index 30/20/16;
  - middle 33/22/17 (the longest finger);
  - ring 31/21/16;
  - little 24/16/14 (it ends at the ring finger's last joint).
- Finger widths: 13 to 16.5.
- Thumb: 20 wide, phalanges 24 and 21, its root at the heel of the palm.
- A woman's hand is smaller: about 0.85 of these sizes (and slimmer fingers).
- The whole hand is about the face's height, from chin to hairline. A hand smaller than
  the object it holds is almost always wrong.

## Drawing

- **One skin.** Every piece of a hand (palm, fingers, thumb, web) is knocked out and inked
  as one union: trace every outline with the same winding, or overlaps punch holes. Shade
  the hand through one clip.
- **One colour for every visible piece.** The thumb, the fingers and the back of the hand are inked with the same skin spec; a darker spec is only for a piece that is really in shadow (behind the object, turned away), never for the thumb by default.
- **No lines across the hand.** The only lines allowed are:
  - the lines between fingers pressed together;
  - one short curved crease per joint, on the finger's middle;
  - a faint outer edge where the hand meets a similar tone.

  Never outline each piece, and never draw a line along the knuckles' row or a vein that
  reads as a border.
- **Form by shade.** Each finger is round: shade at its sides, light down its middle. The
  parts turning away from the light go darker. Knuckles are light bumps, not rings.
- **Nails** only where the reference shows the back of a fingertip.
- **Cuffs sit on the wrist, outside the hand.** A cuff drawn inside the palm or the fingers
  means the wrist point is wrong: fix the point, don't paint over it.
- **In 3D scenes** draw the hand in the prop's projected frame (the affine map of the
  prop's surface at the grip), so it stays on the prop at every camera. Keep the arm's IK
  target on the hand's wrist point.

## The hand check sheet

Every experiment with hands has a dev scene `dev/handcheck/scene.js` (see
`sandbox/2026-09-25-physics-history/dev/handcheck/`). It draws each hand at full size on its
real prop, from the camera the scene uses. Render one still from it, crop each hand at full
resolution side by side, and save the result as `dev/handcheck/hands.png`. Then:

- Crop every hand in its scene too, at the frames where it acts (grab, hold, release),
  in a sheet of crops at 2 to 3× zoom.
- Put the reference beside the hand when there is one.

## Looking

Before sending a hand image, answer these questions in writing (to yourself). If any
answer is no, fix it first.

1. Does it match the reference piece by piece: which fingers show, where the thumb is,
   which way the tips go?
2. Is it the right hand (or the left), as the handedness check says?
3. Is every visible digit whole? Nothing amputated, no stubs, no blobs.
4. Is it one skin, with no holes, no seams, no lines across it and **no border round it**? Check it in the code, not only in the image: a hand function must not stroke the outline of its palm or back (a `line(...)` over the shape's own points). A border keeps coming back when a hand is copied from an older one.
5. Are the proportions right: the thumb against the fingers, the hand against the face
   and against the object?
6. Would someone who has never seen the code say «a hand holding X» at first glance?

Report honestly what still reads badly, and never call a hand fine because it is better
than the last one.
