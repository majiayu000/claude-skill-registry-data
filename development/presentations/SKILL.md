---
name: presentations
description: Jon's standing preferences for building and revising presentations he will deliver aloud.
disable-model-invocation: true
---

# Presentations

Standing preferences, set 2026-08-13.

Two ways in.

**New deck** — read Form, Register, and Structure before the first draft;
do not draft and then retrofit the register.

**Applying feedback** — Jon calibrates by example. When he kills a line,
generalize the kill to the pattern before the next pass: he is correcting
a genre, not a sentence. Then re-sweep every slide against the register,
not only the slides he named, and report what you removed so he can
recall any of it.

## Form

- A presentation is a **slide deck Jon talks over**, never a page the
  audience reads. One slide per viewport: click/arrows/space advance,
  slide counter, Home/End, no-JS fallback to stacked sections,
  reduced-motion respected, dual-theme token CSS.
- One headline claim per slide, at most one visual device, at most 3
  support lines. Read each slide aloud and time it: under 20 seconds.
  Overflow means cut or split — never shrink type to fit.
- Type scales with the screen: root font on a height-aware clamp — copy
  `clamp(16px, min(1.2vw + 9px, 2.75vh), 27px)` on `html.deck`, all
  sizes in rem.
- Vary devices — stat tiles, before/after panels, bar charts, hub
  diagrams, cost→cause→stop rows. Three uniform bullets in a row is the
  ceiling; a section's biggest claim renders big, not bulleted.

## Register — the language laws

Every substantive line passes all of these; a line that fails joins one
that passes, or dies. These laws supersede the generic `humanizer` and
`structural-humanizer` passes for deck copy: those optimise for prose
that reads as human — unresolved threads, oblique tangents. A deck
argues to a close: pains mirror payoffs, and the last slide resolves. Do
not run them over slide copy.

1. **Felt stake.** For every claim, point at three things in order: what
   the audience suffers, the quiet cause, the change. If you cannot
   point at all three, the line is a slogan (vibe without mechanism) or
   trivia (mechanism without stake). Both die.
2. **Titles and section leads state one claim in one sentence** with a
   subject that does something. Guardrail: no rhythmic fragment pairs or
   parallel aphorisms anywhere. A metaphor survives only if cashed out
   by its mechanism in the same breath.
3. **Concrete subjects.** Claims are headed by the specific thing, never
   an abstract noun (logic, machinery, structure), and metaphors never
   state what happens. A metaphor may serve as a NAME for one mechanism,
   glossed once with its literal definition, then reused bare ("the
   doorway — the one builder every endpoint passes through").
4. **One anchor per claim** — a name OR a number OR a mechanism, never a
   stack. Too vague: "Logic gets a home." Too technical: "the staging
   code at line 4,000 of the 15,600-line file becomes ProposalService
   with three constructor-declared collaborators." Right: "The staging
   logic becomes its own class, with a name and a short list of what it
   can touch." Big numbers live in tiles and bar charts, not inside
   sentences.
5. **Spoken-aloud test.** Say it the way you'd say it to a colleague
   across a desk. Plain words; gloss jargon once or replace it
   ("swappable connector", not "port"). If a sentence needs a second
   read, rewrite it.
6. **Titles are concrete claims** carrying one anchor — "We waited ~106
   hours on CI last week" — never a topic label, never a
   name-plus-explainer.

## Structure — the narrative laws

Every law below names a beat the deck must contain. Before publishing,
walk the deck once per law and name the slide that satisfies it. A law
with no slide is a missing beat — add it, or say why this deck does
without it.

- **Open with the felt stake** — money and time, measured, framed as
  what it takes from the audience's own lanes — before any solution
  appears.
- **Name the baseline** before describing the fix (what the system IS
  today, bluntly), then derive each pain causally from that shape.
- **Pains and payoffs mirror one-to-one**, same order, visually paired.
- **The idea's heart is an object-level before/after** — things and
  their connections drawn as diagrams (a flat scatter with crossing
  lines → named layers with declared edges), not code. A code sketch may
  follow as the enforcement beat. Every drawn edge must exist; check for
  orphan boxes.
- **Enforcement is a list of mechanical consequences** — what fails and
  where when someone does it wrong — each carrying its felt stake. No
  summary aphorism after the list.
- **Justify structure by deletion**, led by the inventory of machinery
  it removes — stated as gain, never as a defensive rhetorical question.
- **Reassurance is calm** — "The honest scale of this" — and plain: not
  a rewrite, not one big effort, not free; paced, riding planned work.
- **Method sections teach thinking** — how to see a problem's atoms —
  not worksheet steps.
- **Examples**: rotate across the team's actual work lanes, never the
  same domain twice in a row. Decompose something already shipped,
  labeled as a lens — an invented feature reads as a proposal, and
  in-flight pilots' specifics get over-indexed.
- **Close grounded**: the real target shape of in-flight work (file
  tree, one small code moment), canonical doc paths as a footer line.

## Evidence

- Every number carries its date window and denominator; fetch real
  measurements rather than estimating (CI minutes come from the GitHub
  API, not memory).
- State partial wins as partial — "one corner fixed; the rest still
  pays". Insiders read overclaims as shallow, and one overclaim taxes
  every other number on the page.
- Actors are stated as they really are: agents read, write, and trace
  most code; humans brief, review, decide, get paged. Frame scenarios
  accordingly.

## Before publishing

Run these in order; a deck that has not passed all four is not ready.

1. Open the deck in Chrome at 1280×720, then at 1920×1080 — the narrow
   case grows slides taller through line wrap; the wide case tops out
   the font clamp at 27px. Passing at one size does not imply the other.
2. For every slide, measure `getBoundingClientRect().height` (and
   `scrollHeight`) against the viewport height. Centered flex with
   `overflow: hidden` clips silently without ever registering a scroll —
   the measurement is the check, not the eye.
3. Confirm every SVG label box contains its text and nothing overlaps.
4. Run the Structure walk (one named slide per law), lock overflow, and
   republish to the same file path.
