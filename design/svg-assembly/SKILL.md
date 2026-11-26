---
vendored_from: https://github.com/appautomaton/delineate
name: svg-assembly
description: >
  Make a web page that a crew of simulated hands builds in front of its reader: column guides pulled
  down, frames dragged out with their size badges, text typed key by key, headlines pulled up to
  size, crayon drawn stroke by stroke, rows of labels typed at once and put right, then a flock that
  follows the reader's pointer. Built on this repository's engine in assembly/hand/. Use when a page
  or a section should assemble itself as it scrolls into view, when adding live "built by agents"
  or "cursors at work" motion to a page, when tuning how the pointers move or look, or when drawing
  crayon art for the hands to draw, even if the user never says "skill".
triggers:
  - svg-assembly
  - svg
  - assembly

---

# Assembly

Project paths are relative to the repository root; `ref/` files are in this skill's folder. Load a
ref file when its stage comes up, not before. `assembly/` is the work this skill came from: its page
(`index.html`, `style.css`, `main.ts`), the sheet another page shows (`show.ts`), its crayon
(`drawings.ts`), and the engine (`hand/`), every module opening with a comment that says what it
does. `assembly/notes.md` keeps what the work taught.

## The bar

The idea came from a video of a page built by a swarm of cursors. That is the floor, not the aim.
There, the cursors glide like machines and build plain boxes; here, the hands move the way people
move a mouse, and what they build is drawn. Three things are held to:

- **Every frame holds as a page.** Mid-build or done, any screenshot is a composed page: the marks
  of the tool (guides, frames, badges, pointers) are part of the picture, never litter on it.
- **Nothing is decoration.** Every guide falls on a real margin, every badge states a real size,
  every blue line marks edges that really align, every pen goes where the wax really goes down.
- **It belongs where it lives.** The page keeps its site's margins, paper, ink and light, by day
  and by night, at every width, and is simply there, drawn, for a reader who asks for less motion.

## First principles

1. **Write the page first; read it backwards.** The page is written whole, laid out as it will
   stand. The crew measures it and takes it apart into the work a design team would do. So the
   page is a real page (selectable, readable, findable), nothing moves while it is built, and a
   change to the page needs no change to the animation.
2. **Move as people move.** Reaching follows Fitts's law: a quick primary movement that lands near,
   more often short than long, then smaller corrections; each movement minimum-jerk, its path
   bowed. Keys fall unevenly, slower at word starts and after punctuation, with now and then a slip
   seen and taken back. Agents may be quicker than people; they keep a person's rhythm.
3. **Speak the tool's grammar.** Guides from the rulers, frames corner to corner, a headline typed
   small and pulled up by its handle, the pointer's shape the tool in hand, a clash shown in red
   and settled. A reader who has used a design tool reads every act without being told.
4. **Craft at every scale.** The pointers are made as paper things are made, judged on a specimen
   sheet at four times size; the crayon is drawn in the repository's own hand
   (`footers/crayon/`). The smallest thing on screen is held to the same standard as the largest.
5. **Small experiments, a long-lived engine.** Try a thing in a study under `assembly/studies/`;
   when it works, it goes into `hand/` for every page. Improve the engine rather than patch a page.

## Who decides

You hold the aesthetic judgment. The user steers what the page says and how it should feel;
everything below that is yours: the layout, the drawings, the pace, the number of hands, what is a
block and what is typed. Decide, build, show it running in Chrome, and say why. Ask only when the
direction itself is unclear.

## The way

1. **Write the page** as it will stand, in its site's tokens, with `data-section` on each section
   and the few `data-build` marks the crew needs. See `ref/page.md`.
2. **Draw its pictures** in crayon, one `<g data-hand>` per hand, back to front. See
   `ref/drawing.md`.
3. **Set the crew**: how many hands, their colours (crayon names, so they follow the light), their
   pace. See `ref/hands.md`.
4. **Run it and watch it** as a reader would, at three widths, by day and by night, and once with
   less motion. See `ref/verify.md`.
5. **To show it inside another page**, put it on a stage (`show.ts`, `hand/space.ts`): the hands then
   work in the stage's own coordinates and move with whatever holds it.

## Judging

The eye judges; numbers only catch drift. Stop the page at random moments and ask of each frame:
does it hold as a page? Is every mark on it true? Then watch it whole, at a reader's pace: does the
crew read as people at work, with a rhythm (a quick hand, a slow one, a pause to look), or as a
machine replaying a script? Judge pointers on `assembly/studies/pointers/` before you judge them on
the page.

## Working rules

- Run `npm run assembly` and open http://localhost:5310/ in Chrome; the page rebuilds and reloads as
  sources change. A change to `drawings.ts` needs the server restarted.
- A hand's click selects, as in a design tool: the page never hears it.
- Measure only after `document.fonts.ready`; the crew reads boxes, and type that has not loaded
  measures wrong.
- When the crew does something odd, measure the real boxes before guessing.
- Before blaming the approach, read `ref/traps.md`.

## Routing

| Need | Load |
|---|---|
| Writing a page for the crew: marks, layout, light, widths, a stage | `ref/page.md` |
| Crayon for hands to draw: groups, the pen's tip, shapes, colour | `ref/drawing.md` |
| The hands: motion, typing, pace, how many, idle, the flock, the pointers | `ref/hands.md` |
| Checking it and showing it | `ref/verify.md` |
| Something looks wrong and the cause is unclear | `ref/traps.md` |
