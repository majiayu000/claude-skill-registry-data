---
name: anti-slop-ajonai
description: >
  Build web interfaces that don't read as machine-generated. Use when creating or reworking any
  frontend — landing page, marketing site, app UI, dashboard, component, or artifact — and
  whenever someone says the output looks AI-generated, generic, templated, "like every other
  SaaS site", or asks to make a UI feel designed, premium, distinctive, or hand-built. Also use
  when auditing an existing interface for default-inherited choices. Covers palette construction,
  type pairing, spacing registers, elevation, interaction states, motion, and asset honesty,
  with a runnable static checker.
---

# Anti-Slop (AJONAI)

## The one idea

A tell is not ugliness, and not popularity. **A tell is a choice whose frequency is invariant to
the brief** — the thing that shows up at the same rate whether the page is a mortgage calculator,
a techno label, or a hospice.

That reframes the whole problem. Design is a sequence of decisions. Wherever a brief is silent,
a generator *inherits* a default and a designer *makes a call*. Every tell marks a place where a
decision was skipped. Untouched defaults are damning precisely because a designer would have
touched them.

So the goal is not to avoid a list of banned things. It is that **every visible property be
derivable from this brief and no other.** A page passes when you can point at any value on screen
and say why it is that value here and would be different elsewhere.

### Why ban-lists fail

They work once, then become the next tell. This is documented, not theoretical:

| Was the escape | Became the tell |
|---|---|
| "Don't use pure white, use a warm off-white" | Cream/beige page grounds are now a detector rule |
| "Escape Inter with an editorial serif, set the hero italic" | Oversized italic serif hero is now a detector rule |
| "Add a tracked uppercase eyebrow for editorial hierarchy" | The eyebrow is now the single most-banned element |
| "Stop shipping heavy shadows, use a 1px hairline" | Models did *both* — hairline + wide shadow is now a named defect |

Advice followed uniformly produces uniformity. A rule that says "avoid X" manufactures "everyone
avoided X the same way." Treat every specific value in `references/` as **perishable**, and the
process below as durable.

## Non-negotiable: decide before generating

The only intervention with evidence behind it is front-loading constraints into the **first**
generation. Correcting afterwards measurably underperforms starting from a stronger instruction,
and generic output is the *mode* of the distribution rather than an unlucky draw — so retrying,
regenerating, and raising temperature do not escape it. Only changing the conditioning moves it.

**Before writing any markup, write the decision sheet.** Five axes, because these are exactly the
slots a brief leaves open:

```
SUBJECT     one sentence: what this is, who it's for, its single job
GROUND      the page's world — materials, instruments, vernacular of the subject
PALETTE     4-6 named hex values, each with a role. State the neutral's hue bias.
TYPE        2+ roles (display / text / utility), named faces, and why these
SPACE       two registers: intra-component values and section rhythm — different numbers
SHAPE       one radius value, one elevation policy (tonal step OR shadow, not both)
MOTION      a count of animated moments and a duration band, or "none"
SIGNATURE   the one element this page is remembered by
```

Then **critique the sheet before building**: work through a similar prompt in your head and see
if you arrive somewhere similar. Any line that would be identical for a different subject in the
same category is a line you inherited. Revise it and say what changed.

Read `references/00-decision-sheet.md` for how to fill each line, with worked examples.

## Weight interaction states above appearance

The counterintuitive finding, and the one that most separates this skill from others: when a large
pool of candidate tells was adversarially audited, **motion and interaction states had the highest
survival rate; hero composition and iconography had the lowest.**

A screenshot of a generated page is usually fine. The giveaway is that it is **inert**. Missing
`:active`, no `:focus-visible`, no disabled styling, no loading, empty, or error state, untouched
`::selection` and `caret-color`, a scrollbar nobody looked at.

So: **ship the states that are absent before restyling the states that are present.** Cheapest,
highest-signal work available. See `references/04-states.md`.

## Reference map

Load only what the current task needs.

| File | Load when |
|---|---|
| `references/00-decision-sheet.md` | Always, before generating |
| `references/01-color.md` | Choosing or fixing a palette, gradients, dark mode, contrast |
| `references/02-type.md` | Choosing faces, scale, tracking, leading, measure |
| `references/03-space-surface.md` | Spacing, elevation, radius, borders, dividers |
| `references/04-states.md` | Any interactive element — read this by default |
| `references/05-motion.md` | Any animation or transition |
| `references/06-assets.md` | Icons, imagery, charts, placeholder data |
| `references/07-audit.md` | Reviewing existing UI, or self-checking before shipping |
| `references/08-dated-defaults.md` | The current monoculture. Check the date at the top. |

## The checker

A dependency-free static checker ships with this skill. It reads source, not renders, so it is
honest about its limits.

```bash
node scripts/check.mjs <paths...>          # files or directories
node scripts/check.mjs src/ --json         # machine-readable
node scripts/check.mjs src/ --only=color   # one category
node scripts/check.mjs src/ --strict       # advisory findings count as failures
```

Findings are `error`, `warn`, or `advisory`. Advisory never fails a run without `--strict`,
because those rules have real false-positive rates. Suppress a checked-and-accepted finding with
`/* deliberate-ignore rule-id */` on the line above, or `<!-- deliberate-ignore rule-id -->` in
HTML. A suppression is a decision, which is the point.

## What this skill refuses to do

Other anti-slop rulesets contain real defects. Do not reproduce them:

- **No blanket typeface bans.** Banning Helvetica and Arial outlaws two of the most-studied faces
  in the history of the discipline. The rule is share-and-context: is this face doing the *display*
  work of a page whose brief never asked for it? A system stack for body text is fine.
- **No total em-dash ban.** Prescribing a hyphen where an en dash is correct damages typography to
  evade a classifier. Optimize for the reader, never for the detector.
- **WCAG large text is 24px, or 18.67px bold** (18pt and 14pt at 96dpi). Several published skills
  state 18px, which lets 18–23.99px text pass at 3:1 where AA requires 4.5:1. That is an
  accessibility regression introduced by an anti-slop rule.
- **Don't treat human tells as AI tells.** Off-scale magic numbers, a double space, sub-pixel
  misalignment, a novelty display face — these are evidence *against* machine authorship. A rubric
  that scores them as positives misfires on hand-built amateur sites, which are exactly the pages
  most likely to be falsely accused.
- **Don't claim a single element proves authorship.** Individual properties are weak evidence;
  co-occurrence is strong. When three independent judges rated a large pool of candidate tells,
  under 10% were unanimously high-signal. Say "this reads as inherited," never "this is AI."

## Working rules

1. **Pin the subject first.** If the brief doesn't say what the thing is, decide and state it.
   Distinctive choices come from the subject's own world, not from a style library.
2. **Spend boldness once.** One signature element carries the page; everything around it stays
   quiet. Uniformly-distributed effects read as generated.
3. **Two spacing registers minimum.** One gap value everywhere asserts a flat, equal-weight
   structure the content does not have. Proximity is meaning.
4. **Commit in a direction.** Detectors are built so that pure white passes and a committed warm
   ground passes — only the timid middle fires. Timidity is the actual failure.
5. **Real content, real assets.** Placeholder services and invented companies are the most
   identifiable artifacts in generated work.
6. **Check the brief's own words first.** If the user asked for a purple gradient, build a purple
   gradient and build it well. Their instruction always outranks this skill.
