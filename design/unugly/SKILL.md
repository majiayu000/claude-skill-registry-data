---
name: unugly
description: "Find what makes AI-built UI look generic, fix it once approved. Use when the user says \"this looks AI-generated\", \"make it less generic\" or \"polish this UI\"."
license: Apache-2.0
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: design
  cover: "0 slop"
---

# Unugly

Make AI-generated UI look intentional. Audit it, propose changes with reasons, wait for a yes,
then write them on the project's own tokens. Work inside the existing project, never around it.

## The rules underneath

1. **No code changes without approval.** Show the reasoning and the diff first. Write only after
   the user says yes.
2. **Load the design context before any proposal.** Without it, every suggestion is generic.
3. **Respect the existing system.** Inherit the palette, spacing scale, type, components and tone.
   Never fight the codebase.
4. **Few, specific findings beat a long list.** Name the element, the problem and the fix.

## Pick the job

| The user asks for | Do |
| --- | --- |
| "What's wrong with this page?" | Audit (step 4) |
| A scored, structured review | Critique (step 5) |
| "Make this bolder / quieter / cleaner…" | Variants with a verb (steps 6 and 7) |
| Better words | Rewrite (step 8) |
| A new section (hero, pricing, features…) | Insert a block (step 9) |
| "Are we on our own system?" | Drift check (step 10) |

Every job ends at the same gate: propose, wait, write, verify (steps 11 and 12).

## Steps

### 1. Load the design context once

Read these at the start and keep them in mind. Don't re-read them for every change.

- **Design doc and tokens:** `DESIGN.md` or similar, the theme file (`@theme` block, Tailwind
  config, CSS variables), the component library in use.
- **Product doc:** audience, voice, banned words, competitors if listed.

If there is no design doc, offer to draft a short one first: tokens read from the code (colours,
type scale, spacing scale, radii), plus audience and voice from the user. If the user declines,
say you're using sensible defaults and carry on.

### 2. Decide the register

- **Brand surface** (landing page, hero, campaign): the design is the product. Committed or
  drenched colour can be right. The reflex-reject list and both slop tests apply in full.
- **Product surface** (app UI, dashboard, settings, tools): the design serves the product.
  Restrained colour is the floor. One type family is often right. A fixed rem scale. Familiar
  beats surprising.

### 3. Look at it

If you can drive a browser, take a screenshot of the page or the element. Otherwise read the
component and ask the user for a screenshot. Judge what renders, not only what the code says.

### 4. Audit

1. Find real, specific issues: gradient slop, off-scale spacing, weak hierarchy, failing contrast,
   mixed radii, crowding, missing states. Use the judgment and anti-pattern lists below.
2. Cite the project's own tokens in each fix, not generic advice.
3. Give each finding a severity: **critical**, **warning** or **suggestion**.
4. Score 0 to 100, where 100 is clean. Be honest: a generic page is a 60, not a 90.
5. If the product doc lists competitors, end with one finding: "1 way to stand out from
   <competitor>", one concrete design choice that answers a weakness in their design.

Report it like this:

```
Score: <N>/100
1. [critical] <element>: <problem>. Fix: <change, on which token>.
2. [warning] …
Stand out from <competitor>: <one choice>   (only if competitors are listed)
Want variants for any of these?
```

### 5. Critique (when asked for a structured review)

Score Nielsen's 10 heuristics from 0 to 4 each (max 40). 0 = severe violation, 1 = major problems,
2 = present but weak, 3 = mostly met, 4 = fully met. If the screen gives no way to judge one, score
it 2 and say so.

| # | Heuristic | Quick check |
| --- | --- | --- |
| 1 | Visibility of system status | Loading, progress, success and error feedback |
| 2 | Match between the system and the real world | Words and icons users know |
| 3 | User control and freedom | Undo, back, cancel, dismiss |
| 4 | Consistency and standards | Same word and colour for the same role |
| 5 | Error prevention | Confirm destructive actions, constrained inputs |
| 6 | Recognition rather than recall | Labels visible without hover, current state shown |
| 7 | Flexibility and efficiency of use | Keyboard, shortcuts, progressive disclosure |
| 8 | Aesthetic and minimalist design | Nothing competes with the main content |
| 9 | Help users recognize, diagnose and recover from errors | Plain-language errors with a next step |
| 10 | Help and documentation | Empty states that guide, contextual help |

Then pass or fail five personas. Pass means they finish the core task without a blocker.

- **Power user:** sensible tab order, shortcuts, dense information reachable.
- **First-timer:** value clear in 5 seconds, no jargon, no dead ends, obvious CTA.
- **Accessibility:** text contrast at least 4.5:1, visible focus, every control labelled, touch
  targets at least 44px.
- **Edge case:** long text wraps or truncates, empty states designed, long names don't break layout.
- **Mobile:** 44px targets, no horizontal scroll at 375px, readable without zoom.

Score: `round(nielsen / 40 * 60 + passes / 5 * 40)`. 80 to 100 excellent, 60 to 79 good, 40 to 59
needs work, under 40 significant issues. Report the score and the top findings in the audit format.

### 6. Variants

Propose 3 variants along **different axes**, never three shades of one idea:

1. **More restrained:** quieter, more space.
2. **Stronger presence:** more contrast, heavier weight.
3. **Different personality:** another colour temperature or spatial rhythm.

If the product doc lists competitors, swap one for "Beat <competitor>": name one weakness in their
design and how this variant answers it, in one or two sentences.

Each variant:

- A label, a one-line rationale, and the change as a short list of properties.
- A focused delta: 3 to 8 CSS properties, not a redesign.
- Every colour, space and radius is a project token, never a new raw value.
- With several elements selected, the same change must read well on all of them.

If you can preview in a browser without touching source (injected styles, devtools), show them
live. Source changes wait for the gate in step 11.

Use the structural path only when CSS can't express the change (layout, new elements, markup):
build the variants side by side behind a temporary switch, and on approval keep the chosen one,
delete the others and the scaffolding, and leave clean source.

### 7. Verbs

When the user names a direction, follow its moves and avoid its "Not" list. Keep the variants
from step 6 inside that direction.

**Bolder** (more confident, not louder)
- Contrast first: the highest-impact change.
- One weight step up (body 400 to 550, headings 600 to 700+). A size step for presence.
- More padding makes an element feel more important.
- Strip borders, shadows and fills that dilute the focus.
- Not: gradient text, shadows as "weight", all-caps body, more colours, bolding everything.

**Quieter** (considered, not invisible)
- Remove borders that carry nothing, shadows that don't mean elevation, fills that are texture.
- Dim secondary text. Drop weights (labels 600 to 450). Transparent card backgrounds.
- Not: illegible contrast, shrinking everything evenly, 40% opacity on controls (reads disabled),
  quieting the primary action.

**Polish** (the finish that reads as care)
- Every space on the project's scale (usually 4px steps). One `11px` breaks the rhythm.
- Shared alignment axes; icon and text centred; baselines line up across columns.
- One radius per tier: controls about 6px, cards 10 to 12px, pills 999px.
- One border colour and one grey family. Shadows from the elevation scale.
- `cursor: pointer` and a visible focus ring on everything interactive.

**Typeset** (the strongest lever)
- At least 3 distinct levels: display, label, body.
- A real ratio (1.25, 1.333 or 1.5), not 1px steps. Two weights, three at most.
- Body 15 to 16px (never under 14px on desktop), measure 55 to 75 characters (`max-width: 65ch`).
- Line height: headings 1.1 to 1.2, body 1.5 to 1.65, captions 1.4.
- Tracking: headings -0.02em, all-caps labels 0.07 to 0.1em, body 0.
- Not: one weight everywhere, more than 3 sizes in a component, unplanned font pairings.

**Colorize** (roles, not more colours)
- Assign roles (text-primary, surface, border, accent) and use tokens, never literal hex.
- Core palette of 3 to 5. One focal accent per surface; opacity steps for secondary uses.
- Semantic states keep their meaning: red destructive, green success, amber warning, blue info.
- Contrast: body text 4.5:1, large text and UI parts 3:1.
- Not: indigo-violet accent, cream backgrounds by default, 8+ colours in one component, gradient text.

**Animate** (motion that explains cause and effect)
- Use it for state changes, things appearing and leaving, and loading.
- Durations: hover and focus 80 to 120ms, menus and modals 150 to 200ms, route changes 200 to
  300ms, loading pulses 1.2 to 2s.
- Easing: `cubic-bezier(0.2, 0, 0, 1)` or ease-out to enter, ease-in to leave. Never linear.
- Not: page-load showpieces, animated backgrounds, staggered lists unless the list is the feature,
  interactive transitions over 200ms.

**Layout** (structure before styling)
- Related things sit closer than unrelated things. One dominant axis.
- Fewer, wider columns; one column on mobile until there's a reason.
- Snap to the grid. Put the primary CTA in the next eye position after the value line.
- Not: equal grids for unequal content, cards around everything, centred text wider than 75ch,
  same size for different importance.

**Hero** (a brand surface; run both slop tests)
- Headline: `clamp(2.75rem, 5vw, 4.5rem)`, weight 700 to 800, tracking -0.03em, leading 1.05.
  Never above 6rem, never tighter than -0.04em, never gradient-filled or all-caps.
- CTAs: primary opaque at full contrast; secondary ghost at 60 to 70%, same radius. Never two
  identical gradient pills.
- Product preview: neutral 1px border, colourless depth shadow, about 12px radius. No coloured glow.
- Social proof: small, about 50% opacity, greyscale logos as plain items, no card per logo.
- Background: one strategy. Flat dark, or a single-colour glow at 15% opacity or less.
- Not: the big-number metric template, a grid overlay stacked on a gradient and a glow.

**Rewrite:** see step 8.

### 8. Rewrite copy

The words are part of the design. Read the voice from the product doc. If the visible text is cut
off, read the full text in the source first. Change words only: no styling, no structure.

Give 3 alternatives:

- **Direct:** the shortest true sentence. Action plus object. No adjectives.
- **Concrete:** one specific: a number, a time, a named outcome.
- **On-voice:** the product's own register. Dry stays dry, technical stays precise.

By role:

- **Headline:** subject, verb, specific outcome, 4 to 9 words.
- **Subhead:** how the headline happens, in one sentence. Don't restate it.
- **CTA:** action plus object ("Start a project", "See pricing"). Never "Get started", "Learn more",
  "Click here", "Submit".
- **Eyebrow:** at most 2 words, sentence case, only if it adds information. Otherwise delete it.
- **Empty state:** what goes here and the one action that fills it. Not an apology.
- **Error:** what happened, why, what to do next. No blame, no "Oops!".
- **Microcopy:** one fact per line.

Never write:

- Slop words: unleash, unlock, supercharge, turbocharge, seamless, effortless, elevate, empower,
  revolutionize, game-changing, next-level, cutting-edge, blazing fast, "10x your…", "in today's
  fast-paced world", plus everything on the product's banned list.
- Exclamation marks, unless the voice allows them. ALL CAPS for emphasis.
- Benefit soup ("speed, power and flexibility"). Rhetorical-question headlines. "We believe…" on
  product surfaces.

Test: *could this headline sit on any other product's site?* If yes, rewrite it. If two of your
three alternatives could swap between products unnoticed, sharpen the axes. If the existing copy
is already specific and on-voice, say so and offer refinements, not replacements.

**Whole-page copy pass:** list every heading, CTA and paragraph with its file and line. Pick the 10
worst at most (slop words, vague or repeated CTAs, shouting, exclamations, placeholder text). Leave good
copy alone. Rewrite those, then send them through the gate as diffs.

### 9. Insert a block

1. Place it next to the element the user picked, or where it makes most sense.
2. Build it from the project's real components and tokens.
3. Offer variants as in step 6 (structural path).
4. It must look native. Never invent a look that fights the system.

### 10. Drift check

1. List the page's distinct colours, spacings and radii (from the code or the rendered styles).
2. Compare them with the design doc. Mark each off-system value and the nearest token.
3. Offer to fix the worst offenders: replace hard-coded values with tokens, and make sure the app
   actually imports the token file.
4. The design doc is the source of truth. Don't change it to match the drift.
5. A font change means installing the font for real: the import, the weights the system uses, and
   the variable that points at it. Check that it renders.

### 11. The gate: propose, then stop

Work out the exact source change but don't write it. Show it as a unified diff, one per file:

```
<variant or fix name>
Why: <one line>
--- a/<file>
+++ b/<file>
@@ … @@
Write this?
```

Wait for the user's yes. "Cancel" means write nothing and remove any scaffolding.

### 12. Write and verify

1. Write the approved change at the exact file and line: tokens or utility classes, no leftover
   inline styles, no preview scaffolding.
2. Run the project's lint and typecheck.
3. Look at the changed screen at desktop and phone widths. Check it matches what was approved.
4. Report what changed, in which files, and what you checked.

## Design judgment

Strongest first:

- **Hierarchy:** one clear primary action; reading order set by size, weight, colour, space.
- **Spacing:** the project's scale only (4px grid or the declared scale). No one-off values.
- **Typography:** a real scale with 3+ levels, few weights; size and space carry hierarchy.
- **Restraint:** gradients, shadows, borders and radii are spices. One focal gradient, not ten.
- **Contrast and legibility:** readable text, comfortable measure, left-aligned body copy.
- **Real states:** empty, loading and error, designed.

## The AI tells

Fight these on sight:

- Indigo-to-violet gradients. Gradient-filled text.
- Everything in a card. Border plus heavy shadow on the same element.
- One font size and weight for everything. Off-scale spacing.
- Warm cream backgrounds by default. Coloured left-border stripes.
- Over-rounded buttons, inputs and cards (radius 32px or more).
- Weak CTA hierarchy. Shouting hero type. All-caps eyebrows over every section.
- The generic SaaS hero. Fake charts. Centred long text.
- Missing empty, loading and error states.

## Reflex-reject (training-data defaults)

Don't pick these for new choices. Keep them only where the project already uses them.

- **Fonts:** Inter, Space Grotesk, DM Sans, Plus Jakarta Sans, Outfit, Fraunces, IBM Plex Sans,
  IBM Plex Mono, Space Mono. Look further; a well-tuned system stack with strong weight contrast
  beats them.
- **The cream band:** OKLCH lightness 0.84 to 0.97, chroma under 0.06, hue 40 to 100. It reads as
  sand or parchment whatever the token is called.
- **Saturated lanes:**
  - Synthwave: radial purple glow, grid overlay, violet gradient.
  - Dark-minimal: dark background, white sans headline, a single blue CTA.
  - Ghost card: a thin translucent border plus a wide soft shadow (blur 16px or more). Pick one.
  - Over-rounded: radius 32px or more on cards, sections, inputs.

## The slop tests (every brand-surface proposal)

1. **First order:** could someone guess the palette and layout from the category alone ("SaaS
   tool, so dark background, purple gradient, Inter headline")? Then it failed.
2. **Second order:** could they guess it from the category plus "avoided the first reflex" ("not
   purple, so dark-minimal monochrome")? Then the second reflex won. Rework until neither answer
   is obvious.

Name a reference before committing colour or type, for example "near-black with tight type" or
"one committed colour, restrained everywhere else", ideally a real product the user admires.
Unnamed ambition turns beige.

## Never

- Write to source before the user approves the diff.
- Propose without reading the design context, or invent a look that fights the system.
- Add raw hex, one-off spacing or new radii when a token exists.
- Pick a reflex-reject font, the cream band or a saturated lane for a new choice.
- Change the type scale, radius scale or brand colours without asking: those are brand decisions.
- Rewrite copy that is already specific and on-voice.
- Leave preview scaffolding, inline styles or unused variants in the code.

## Red flags: you're about to ship slop

- "It's just a small tweak, I'll write it directly." Every write goes through the gate.
- "Three variants" that differ by one shade. Use different axes.
- "Score 88" for a page that looks like every other one. A generic page is a 60.
- "Learn more", "Get started", or a slop word in your own rewrite.
- "Looks right in the code." Look at the rendered screen, desktop and phone.

## Credits and licence

Adapted from [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus, Copyright 2025
Paul Bakaus, licensed under the Apache License 2.0. This skill is licensed under the same terms;
the full text is in `LICENSE.txt` next to this file.

Taken from Impeccable: the first- and second-order slop tests, the reflex-reject fonts and
aesthetic lanes, the cream band, the brand and product registers, the Nielsen-and-personas
critique, and the direction verbs (bolder, quieter, polish, typeset, colorize, animate, layout).

Changed by Tony Gorb: rewritten in plain language as one skill; every write goes through a
propose-a-diff-then-wait gate; fixes must use the project's own tokens; added the audit report
format, the combined critique score, the competitor line, the three-way copy rewrite with its
banned-word list, the hero numbers and the drift check.
