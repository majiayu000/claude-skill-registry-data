---
name: art-director
description: Give a website a distinctive, coherent design where every component has its own idea - derived from the product's world, not from trends - while staying useful and restrained. Produces a direction (material, palette, type, motion vocabulary) and a per-component plan where each familiar control gets one new physical idea with a clear purpose. Use when starting a site or redesign, when a design feels generic, or when asked to make components unique, beautiful or memorable.
---

# /art-director

Distinctive design is not decoration added at the end. It comes from one question asked of every part of the interface: **what would this be if it were made of the product's world?** A booking site for tide-dependent boat trips can have a date picker whose unavailable days are the ones the tide is wrong for. That's memorable because it's true.

The method below is the one used to build Vitrine: a familiar job, one new idea, a clear purpose, and restraint.

## 1. Find the world

Before any colours, write down the product's world in plain nouns. Ask the user when you don't know.

- **What it's about:** the domain's objects, places, tools and materials (a logistics company: manifests, containers, tides, cranes, routes; a writing school: pens, paper, ink, margins).
- **Who uses it, where and when:** on a phone on a site visit, at a desk at 2 a.m., once a year.
- **What it should feel like, in two words** that aren't "modern" or "clean": "calm authority", "careful warmth", "field notebook".

Then pick **one material or metaphor** for the whole site. Vitrine's is "kept under glass": a museum case. Everything else is derived from it. If you can't say it in three words, you don't have one yet.

## 2. Write the direction

One page, concrete enough that two designers would build the same thing:

- **Ground and ink.** A background and a text colour chosen for the metaphor (paper cream, night plum, harbour blue), plus **one accent** with a named job ("amber means an action").
  Give both a light and a dark theme if the product needs them, and check contrast (`/theme-system` does this).
- **Type.** At most two families plus a mono, each with a reason: a serif for names and headings because the site is editorial; a sans for reading; a mono for dates, numbers and labels.
  Set the scale (for example 12 / 14 / 16 / 20 / 28 / 44 / 72) and the measure (about 60 characters).
- **Motion vocabulary.** Three or four named behaviours, each tied to the metaphor, used everywhere:
  - how things **arrive**
  - how they **respond** to a press
  - how **state changes** show
  - how things **leave**
  Give each a duration and easing (`/motion-director` has the details).
- **Texture.** At most one: grain, paper fibre, halftone, dither, hairline rules. Or none.
- **Words.** Voice in three rules (for example "numbers before adjectives", "name people", "no exclamation marks").

## 3. Give each component one idea

List every component the site needs. For each one, fill in this row:

| Component | Familiar job | The one idea (new physics) | Purpose: what the idea tells the user | Restraint: what you're leaving out |
|---|---|---|---|---|

Rules for the idea column:

- **It must come from the world or the metaphor**, or from something physical: weight, liquid, paper, light, time, distance, wear. Look for real-world objects that do the same job (a fore-edge of a book is a table of contents; a mercury bead is a selection that moves; a ribbon is a bookmark).
- **It must explain something.** The idea is right when removing it loses information: direction, amount, time, state, where something went.
  - A tab indicator that stretches toward its target shows direction and distance.
  - A digit that turns over only where the number changed shows the size of the change.
  - A card that glows on hover shows nothing.
- **One idea per component.** If you need "and also", pick one.
- **Not every component gets a big idea.** A good site has two or three signature pieces and many quiet ones that share the motion vocabulary. Decide which are which, on purpose.

Then check every idea against the anti-gimmick list and cut the ones that match:

- a cursor glow or spotlight
- tilt on hover
- glass or blur as the idea
- gradient backgrounds carrying the design
- magnetic buttons
- text scramble or typewriter
- particles or confetti
- 3D flips
- the same component with a bounce added
- a style borrowed from a famous product

The test: **remove the effect; if nothing meaningful remains, cut it.**

## 4. Make it cohere

Distinct components can still make an incoherent site. Before building, check that:

- every signature idea uses the same material (don't mix liquid, paper and neon)
- every motion uses the shared vocabulary's durations and easings
- the accent colour means the same thing everywhere
- each section of each page has one focal point, and one of the signature pieces appears at most once per screen

## 5. Build and hold the bar

Build signature components first, then the quiet ones.

For each one:

- **Static quality:** screenshot it with motion off. It must be beautiful and readable standing still.
- **Phone:** it must work at 375px wide with touch, not only with a pointer. Rethink the layout if needed (a vertical rail becomes a strip across the top) rather than shrinking it.
- **Keyboard and reduced motion:** every idea needs a keyboard path and a still version that keeps the information (see `/accessibility-pass`).
- **Real content:** real names, numbers and dates, so you judge the design with the words it will actually carry.

Review the result with `/interface-critic`, and cut anything that doesn't pass. Cutting a clever idea that doesn't serve the page is part of the job.

## Output

When asked for a direction, deliver:

1. The world (nouns), the two-word feeling, and the metaphor.
2. The direction page: ground and ink, accent, type, motion vocabulary, texture, words.
3. The component table, with signature pieces marked.
4. The three ideas you considered and cut, and why. This shows the bar.

When asked to build, deliver the components one at a time in the order above, with a screenshot at desktop and phone width for each.
