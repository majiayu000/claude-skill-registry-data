---
vendored_from: https://github.com/appautomaton/delineate
name: svg-climate-garden
description: >
  Make or change a garden on this project's Garden site (garden/): the plants of one real climate,
  drawn in code as watercolor-and-ink SVG that grows as the page scrolls, by day and by night. Use
  for a new garden or climate, a plant added, redrawn, or refined, a garden's composition changed
  (sides look empty, plants crowd, the sky fills up), seasons or water given to a garden, or a
  plant's look researched, even if the user never says "skill" or names the files.
triggers:
  - svg-climate-garden
  - svg
  - climate
  - garden

---

# Climate garden

Project paths are relative to the repository root; `ref/` files are in this skill's folder. Load a
ref when its step comes up, not before.

## The bar

A garden a visitor can tell from every other by silhouette alone, before color: about twelve real
plants of one climate, drawn as one hand would draw them, growing in as the page scrolls, by day
and by moonlight.

- **Real plants, drawn true.** Every plant exists and is grown in the climate, wild or cultivated.
  How it looks is researched before it is drawn; where it is native is not our question.
- **One hand.** A new plant is drawn in the manner of the plants around it, at the same weight of
  wash and ink, so the garden reads as one sheet.
- **It grows.** The page is a growth, not a picture: limbs extend, then parts unfold where the limb
  has reached. The first scroll must visibly answer.
- **Nothing floats.** Whatever hangs (lichen, a vine, spent flowers, fruit) hangs from a host drawn
  with it. Side plants reach in from beyond the frame; bed plants root below it, so no ground is
  ever drawn. Open land leaves the top to the sky.
- **Judged at garden size.** A detail that reads in a close study can vanish where the plant is
  placed; a flower under about eight pixels is lost.

## How a garden works

- **A plant is a function.** It draws in its own units, base (or hanging point) at the origin,
  from its own seed, into a list of SVG elements wrapped in growth markup. The page drives one
  progress value from 0 to 1; a garden that shows a year maps it onto the calendar.
- **Color is tokens.** A drawing names a species tone or a material, never a color; each has a day
  value and a night value in `garden/src/tokens.css`.
- **Layout is CSS.** Each garden has a stylesheet that places its plants for each tier of screen;
  a solver then slides them apart.
- **`npm run draw` renders every plant** and fails when a part would open before its limb reaches
  it. The page, the gallery, and the solver all read what it writes.

To see what exists, read the code rather than a list: the gardens in
`garden/src/garden/gardens.ts` (the page, the switcher, and the gallery find a garden through it),
the plants in `garden/src/garden/plants.json` (names, the gallery's words, rank, and paint order),
and the drawings in `garden/draw/`, where the registry in `draw.ts` maps each plant to its
function. Most gardens draw in a module named for them; the oldest draw in the shared kit. `garden/climates.md` holds the
mechanisms gardens share (Seasons, Water) and each garden's botanical reference.

## The task

- **A new garden.** Research the roster (`ref/botany.md`) and decide it: about four sides, two or
  three hangers on their hosts where the climate has a canopy (none on open land), five or so in
  the bed. Decide the moment or the year: a climate whose plants change their silhouette through
  the year (wood that goes bare, herbs that die back) earns a year; one whose silhouettes hold
  (evergreens, succulents, cushions) shows its best moment. Record it in `climates.md`. Wire the
  garden in wherever an existing one is wired (see Finding the places, below), its `gardens.ts`
  entry first. Start with the signature plant alone, draw it until it sets the manner
  (`ref/drawing.md`), and show it to the user before the rest. Then draw the rest in one batch,
  judge each, compose (`ref/layout.md`), and verify (`ref/verify.md`).
- **A plant added to a garden.** Research the one plant. Check its silhouette against the garden's
  others before drawing. Read its neighbors' code and draw in their manner, with a close study
  beside the drawing for the gallery. Wire it in wherever a neighbor is wired: its registry entry
  (seed, drawing, close study) and its `plants.json` entry together (`npm run draw` stops on a
  plant listed but not registered), its token in both lights, its place in the layout tiers where
  it earns one, and its rows in `climates.md`.
- **A plant redrawn or refined.** Find it through `plants.json` and its garden's module; read its
  entry in `climates.md`. Judge it in the gallery by day and by night and at garden size before
  and after the change.
- **A garden recomposed.** `ref/layout.md`, then `npm run look` for every tier.
- **Seasons or water.** The mechanisms are in `climates.md`; timing parts on the year is in
  `ref/drawing.md`.

**Finding the places.** Lists of files go stale; the code does not. `git grep -il <key>` for an
existing garden's or plant's key, together with the files named for it, shows every place one is
wired in; a new one goes in each of those places. Prose that counts the gardens (the README,
delineate's page) names no key: search for the count in words.

Every task ends the same way: `npm run check` and `npm run look <key>` (both draw the plants
first), then read the screenshots and tell the user where to look, what changed, and what is
still off.

## Working rules

- The roster, the drawings, and the layout are yours to decide. Decide, build, show; the user
  corrects. Ask only where the choice is theirs (which garden next, a plant they may not want).
- Draw back to front, and build volume from parts: a mass painted behind a shrub reads as a rock.
- Reuse the kit before writing geometry. When a second garden needs a helper that lives in one
  garden's module, move it into a shared module then, named by what it is, not by the plant it
  first served.
- Improve rather than preserve: an earlier drawing is not a specification. When an approach fails,
  delete it; keep only code the drawings use.
- A lesson another garden will need goes, as a rule, into the ref it belongs to (a drawing trap
  into `ref/drawing.md`, a placement into `ref/layout.md`). What only one garden needs lives in its
  code.

## Routing

| Step | Load |
|---|---|
| Researching a roster or a plant, briefing research agents | `ref/botany.md` |
| Drawing a plant, growth markup, tokens, the emblem, a drawing that looks wrong | `ref/drawing.md` |
| Placing plants, tiers of screen, sides, crowding | `ref/layout.md` |
| Running the site, looking at layouts, the build | `ref/verify.md` |
