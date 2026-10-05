---
name: prototype
description: Generate N different HTML implementations of a UI feature, preview them, and iterate a few times, a fast "show me the options" loop for exploring what a feature could look like. Default N is 5. Use when the user wants to prototype a UI, explore or compare designs for a feature, says "prototype this", "try a few designs", "explore some options for X", "what could this look like", or hands over a feature with no spec. Marks a quiet pick but does NOT collapse to one winner, research, implement, verify, or open a PR; a chosen direction hands off to the build skill, whose review gates check the result. For editable Paper artboards rather than throwaway HTML, use paper-prototype instead; for whether a state model, business logic, or data shape feels right, use logic-prototype.
---

# Prototype

`prototype` answers one question, **what could this look like?**, with `N`
previewable HTML takes you can click through. It explores and quietly flags a
favourite. It does **not** collapse to one option, research, implement, verify, or
ship. When a direction wins, hand it to the `build` skill, whose pre-build and
post-build reviews check the result; the HTML here is throwaway.

## Inputs

- **Feature** (required): what you're prototyping, however loosely phrased
  ("prototype the autocomplete dropdown", "try a few designs for the empty state").
- **N** (optional, **default 5**): how many implementations to generate. Honour an
  explicit count ("prototype 3 options...") up to a ceiling of 5 — past that,
  variants stop being radically different and start being noise; say so and cap.

If the feature is genuinely unclear, ask one tight question. Otherwise proceed.

## Generate

**Match fidelity to the decision.** When the open question is direction — layout,
hierarchy, density, disclosure — sketch it; low-fi takes settle a direction, and
going hi-fi across the whole set spends the finish `N` times over to answer one
question. Save the finish for a settled direction, or for a question that is
itself about finish. Say which you are doing — sketch fidelity means placeholder
content and fewer states, never invented values: rule 2 holds at every fidelity.

Produce `N` **self-contained, single-file HTML** files (inline CSS/JS, no build
step, openable directly in a browser), each a genuinely *different* implementation
of the feature. Four rules keep the set useful:

1. **Anti-wallpaper guard.** Variants must differ *structurally* (layout,
   hierarchy, interaction model), not be the same thing recoloured. If it helps,
   name the single axis they vary along (density, hierarchy, mood, disclosure) and
   state it, so the comparison means something. Argue for every option: what it
   bets on, and what it gives up. If you cannot write that pair for a variant, it
   is filler — replace it with one you can.
2. **Build from the product's own materials.** Before generating, go and read
   them: whatever file holds the theme (`variables.css`, `theme.*`, a Tailwind
   config, a tokens file), the component package and anything documenting it, the
   icon set, the fonts the product ships, a `CONTEXT.md` if the project keeps one
   (see the `grill-with-docs` skill), and the two or three shipped screens this
   feature would sit beside. Take every number from there: resolve a token to the
   value it renders as, rather than sampling a colour off a screenshot or rounding
   a measurement to whatever looks about right. Type, spacing, corners, elevation
   and control sizing all come from the same place. Prefer components that already
   exist, in the variants and states they already have — these files stand alone,
   so copy them as markup rather than importing them — and make anything new look
   like it belongs beside them. Name in one line what you took ("from the app
   shell: 4px corners, the neutral ramp, 36px inputs"), so the claim can be
   checked. If none of it is reachable, say so and name what you assumed rather
   than rebuilding the product from memory.
3. **Stress-content the previews.** Populate with realistic *and* edge-case content:
   long strings, empty and error states, narrow widths, keyboard focus. The point
   of a real preview is to surface problems a static mockup hides, while you're
   still choosing.
4. **Judge in context, not in a vacuum.** A variant floating on a blank page always
   looks fine. Reproduce the host surface around each option — the real header,
   sidebar, neighbouring content, and density of the page it would live in, built
   from those same values — so the options compete against the app, not against
   whitespace.

### Craft floor

- Icons are inline SVG in one consistent style, matching the weight and fill of the
  product's own set; where there is none, draw them stroke-based at 16, 20 or 24px.
  Emoji and unicode glyphs are not icons.
- At phone width, reserve the system's space and leave it blank — on a device the
  OS paints its own bar and keyboard over yours, so a drawn copy shows up twice.
- At phone width, hit areas start at 44px. On pointer surfaces the control height
  you took from source wins.
- For an icon, image, or component you cannot reach, draw a marked placeholder — it
  beats a bad imitation of the real thing.

## Preview

Emit one small `index.html` gallery that links to (or embeds) all `N` files, so
there is a single surface to look through. Write the `N` files and the gallery to a
gitignored scratch or temp directory, never committed and never left polluting
`git status`. Print the file paths too, so they can be opened directly or with
whatever preview command the project already uses.

State the design question in one visible line at the top of the gallery, next to
the named axis of variation, so the comparison can be checked later — by the
user, or by whoever opens it cold.

Give the gallery a **compare mode**: embed the variants in one frame and cycle
them in place with ←/→ (wrapping around; ignore arrow keys while an input,
textarea, or contenteditable element has focus). Label the frame with the current
variant's key and name (e.g. "3 — Sidebar layout") and reflect it in
`location.hash`, so what's on screen is nameable and a reload lands on the same
variant. Flipping variants in the same viewport position exposes structural
differences that a serial gallery of links hides.

## Quietly mark the recommendation

Form an opinion and surface it **understated**, inside the artefact, never as a
loud prose verdict:

- A small, low-key marker on the favoured variant in the gallery (e.g. a muted
  "Agent's pick" dot/badge) and **one** short line of rationale in small,
  low-contrast text.
- **Do not** add a banner or modal, and **do not** reorder the pick to the front. It
  must be ignorable. The user is the design lead; this is a nudge, not a decision.
- If the user would rather not see it, omit it.

## Iterate

Refine on request; a few passes is normal. The user drives and owns the decision.
Never auto-collapse to the recommended option; only consolidate when the user
chooses one or edits toward it.

Option identities are fixed for the life of the exploration: once a variant is
"3 — Sidebar layout" it keeps that key and that name through every pass.
Renumbering across turns breaks every reference already made to it — in the
gallery, in `location.hash`, and in what the user said last turn.

## Capture on hand-off

When a direction wins, don't bin the exploration. Copy the variant set, the
gallery, and a one-line verdict (which option won and why) to a durable notes or
artefacts location outside the repo — wherever the project keeps design
decisions — and leave a pointer wherever the implementation is tracked. The
losing options and the rationale are the primary source for "why does it look
like this"; the winner alone can't answer that.

## Scope

That's the whole skill. Heavier steps (researching patterns first, implementing the
winner for real, opening a PR with a screenshot) stay **at prompt time** when the
user asks for them, exactly as a person would layer them on. They are deliberately
not baked in. Hand a chosen direction to the `build` skill; its review gates
check the result. The recommendation is the single opinion this
skill expresses, and it expresses it quietly.
