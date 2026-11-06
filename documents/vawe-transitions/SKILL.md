---
name: vawe-transitions
description: "Plan scene transitions for a motion graphics video made from HTML. Plan the handoff at every cut of a vawe film so the transitions are continuous, varied and chosen, not defaulted: name what carries over, run the idea method (guides/IDEATE.md) with the twelve families as devices, keep a ledger, and set up the execution. Load at stage 5, when you fill the Board's handoff column."
effort: medium
license: Apache-2.0
---

# vawe-transitions: one handoff per cut

Run this skill inside a vawe checkout: `AGENTS.md`, `taste/` and `bin/vawe` live there. With no checkout, get one: `git clone https://github.com/vawe-hq/vawe.git && cd vawe && npm install && bin/vawe-dev doctor`.

A model asked for a transition writes the same few: a crossfade, a whip pan, a slide-up, a scale-in. This skill makes the choice on purpose.
The grammar (the twelve families, when each fits, its cost, moves to copy) is in `taste/craft/transitions.md` "The twelve handoff families": read it first,
it is not repeated here. Seam timing is rule `seam-timing`; the eye at a cut is in the same craft doc. This file is the procedure.

Run it for every cut of the Board's cut table, then write the result in its `handoff (family: object)` column and the ledger table.

## Per cut

1. **What changes, what carries over.** One line: place, state, scale, time, a reveal or a payoff changes. Name the handoff object: the one thing that leaves
   A and starts B, with its screen position, scale, direction and speed on both sides. If nothing carries over, the family is `deliberate cut`
   and you write why (on a beat, for shock, a tonal flip).
2. **Run `guides/IDEATE.md` for the cut.** Write the cut's row in the brief's `## Ideas` table: the meaning, 4 ideas with 4 different devices, a typicality number
   for each, the pick and why. The twelve families below are the device list for a cut: each idea names one family and the object, its anchor, direction and speed.
   The method owns the 4 ideas and the typicality; this file does not repeat it.
3. **Write the pick in the handoff cell.** The chosen idea's family and object go in the Board's `handoff (family: object)` column. A pick that fits any similar film is a default.
4. **Check the ledger** (the Board's second table, filled from the handoff column):
   - no family on two adjacent cuts;
   - no family more than twice per film (a `deliberate cut` is exempt: hard cuts are most seams, rule `hard-cut-default`);
   - the spectacle cut gets the strongest device of the film, and no other cut competes with it (quiet before it);
   - camera direction never reverses across a cut without a reason.
5. **Defaults need a reason.** Plain fade, crossfade, whip pan, slide-up reveal and scale-in each need `because ...` in the handoff cell
   (a dissolve for passing time between calm frames is a reason; "it looks smooth" is not).
6. **Slideshow tells.** Read "Banned (slideshow tells)" in `taste/craft/transitions.md`; none of the ten may describe your plan. `bin/vawe check slideshow <page>` scores the draft.
7. **Surprise question.** Which cut would a viewer predict? Replace it, or write why the plain one is right.
8. **Execution notes**, one line per cut in the motion pass:
   - z-order: the handoff object sits above both beats until the new one covers the frame; the old layer does not pop off first;
   - speed matched at the seam: read `bin/vawe frame <page> --moment <s> --velocity` on both sides, the exit must not decelerate into an entrance that starts from rest;
   - a flood reaches the farthest corner in about 0.35 s and has a reveal point, else it just cuts;
   - the transition is shorter than the beat it joins;
   - sound sits on the handoff frame: a J or L cut, or the effect on the frame the object lands.

## Row format

`| s2 to s3 | type-fill-transition | ... | ... | ... | ... | ... | ... | type-driven: the word "ship" becomes the ground |`

A cut with nothing to carry: `deliberate cut: lands on the downbeat, the tone flips`.

## Check

`bin/vawe check transitions films/<name>/page.html [--mp4 out/<name>-draft.mp4]` and the draft's advice name: a cut with no planned handoff, one family on
adjacent cuts or more than twice, a plain fade with no reason, and a planned handoff that measures as a hard cut. Advice only. The `slideshow` check scores the ten banned tells. Waive in the page:
code `transitions`, with a reason that names a second and a measure.
