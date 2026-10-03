---
name: design-review
description: "Evaluate and refine UI the way a senior product designer would, visual hierarchy, spacing and rhythm, typographic scale, legibility, information density, alignment, and restraint, then apply the highest-leverage fixes. Use this skill WHENEVER the user says a UI / page / screen / component feels 'clunky', 'packed', 'cramped', 'busy', 'off', 'amateur', 'cluttered', or 'needs polish'; when they ask to 'improve the design / layout / hierarchy / spacing / legibility', 'make this look designed / professional', 'apply design principles', 'clean this up', 'review the design', or want a 'senior designer' / 'senior product designer' pass; and proactively after building any non-trivial UI, to critique and tighten it before moving on. Grounded in the design canon (Dieter Rams, Edward Tufte, the Gestalt principles, the Vignelli Canon, Nielsen's heuristics) and the Refactoring UI playbook. It respects and extends the project's existing brand / design system first, runs a mandatory system coverage inventory (undesigned groups and unspent brand personality are automatic findings, not just visual excess), reviews the whole surface across all states rather than the recent diff, and documents any missing pattern before building it. When a screen 'lacks personality' it benchmarks named personality-forward references (e.g. PostHog, Duolingo) and designs from them rather than rearranging what exists. Works on existing UI code (improves it in place) or on a screenshot / description. Distinct from a usability/UX audit (this is visual / product-design craft) and from code review (this is design, not correctness)."
---

# Design Review: the senior product designer's eye

Evaluate a screen the way a senior product designer does, then apply the highest-leverage fixes. The
goal is never decoration. It is to make the screen's **one job** unmistakable, through hierarchy,
whitespace, legibility, and restraint. A good pass usually *removes and quiets* more than it adds.

> "Less, but better." (Dieter Rams) · "Above all else show the data." (Edward Tufte)

## The one move: emphasize by de-emphasizing

The single most valuable senior instinct: when the important thing doesn't stand out, **don't pile
on more emphasis; quiet the things competing with it, or remove them.** A UI that feels "clunky",
"packed", or "busy" is almost always *too many equal-weight signals*. The fix is **remove → demote →
quiet**, and only rarely *add*. Emphasis is a fixed budget you allocate, not a property you sprinkle:
if everything is bold, nothing is.

## First, respect the design system

Before touching a single style, find the project's design language and work *inside* it:
- A brand / design-system doc (`brand.md`, `design-system.md`, a Figma/tokens export).
- Design tokens (a Tailwind theme, CSS variables, a spacing/type/color scale).
- Existing components (a `ui/` folder, shared primitives).

Pull type sizes, spacing, color, radii, and shadows from those **defined scales**, never invent a
one-off spacing value, a bespoke grey, or a novel button for a single screen. Per-screen invention is
how design systems rot (Vignelli's *discipline*; Nielsen's *consistency & standards*). **If a needed
pattern genuinely isn't defined, derive it from the system's north-star, write it into the system
first, then build it.** If no system exists, establish the minimal one (a spacing scale, a type
scale, ~2-3 text weights, one accent) before styling screens.

### The system coverage inventory (mandatory, before any lens)

Reading the system for *tokens* is not the same as reading it as a *checklist*. Before diagnosing,
**enumerate every visual group on the screen(s)** — header, each form cluster, each card, each list,
each footer strip — and for each one, **name the system recipe it instantiates**. Two outcomes are
findings, automatically ranked top-3:

- **A group with no recipe** is undesigned UI: either design it into the system first, or it's the
  reason the screen "feels thrown together" (a bare form floating outside the card language is the
  classic case).
- **A declared pattern with zero instances** is unused budget: if the system defines personality
  devices (a mascot, hand-scrawl asides, rotation, illustrations) and the screen has none, the brand
  is silently off. Ask where the personality *should* live on this screen.

This inventory exists because the squint test below only catches **excess** (what stands out that
shouldn't); it is structurally blind to **omission** (what was never designed, dead space, missing
personality). You need both instruments.

## Workflow: diagnose, then apply

### 1. Diagnose, a *prioritized* critique, not nitpicks

**Review the whole surface, never the diff.** Walk the screen the way a visitor does — every state
(empty, partial, full, error), top to bottom — not the way its author does (only the elements recent
work touched). Scoping the critique to what you just built is confirmation bias wearing a design hat;
the stale header nobody has looked at in weeks is exactly where the findings hide.

Start from the job, not the pixels:
1. **Name the ONE job** of the screen in a sentence, and the user's **priority order** for the
   content/actions.
2. **Run the system coverage inventory** (above): every visual group named to a recipe, every
   declared personality device accounted for. Unmapped groups and unspent personality are findings.
3. **Squint test.** Blur the screen (mentally, or literally zoom out / blur a screenshot). Whatever
   still stands out is what the user sees first. **Does it match the priority order?** If not,
   hierarchy is the #1 fix, before anything else.
4. **The subtraction question:** for each element, *does this serve the one job?* If not: remove,
   then demote to a caption, then (last resort) keep-but-quiet.
5. **Run the lenses** below, plus a quick pass of **Nielsen's 10 heuristics** (see
   `references/critique-and-anti-patterns.md`). Do it in **2-3 passes**, a single pass misses things.

Then deliver the critique **ranked by leverage**: the **1-3 changes that most improve the screen's
ability to do its job** (usually: fix hierarchy, cut clutter, fix contrast), then everything else as
"polish." Tie every note to a principle or the user's goal ("this competes with the primary action",
not "I'd make it blue"). Frame it constructively: *what works · what's hurting · what to try*.

### 2. Apply

Fix the levers **in this order** (later ones depend on earlier ones being right):
**hierarchy → subtract/de-clutter → whitespace & rhythm → legibility → alignment → tokens/consistency.**
Apply the changes to the code, and **explain the why** (name the principle) as you go, so the user
gains the eye, not just a diff. If the input is a screenshot, translate the fixes into code against
the real design system; then re-screenshot and re-run the squint test to verify.

**Beware the timid fix.** When the finding is "this feels flat / without personality / poorly used
space," rearranging the existing elements is not a fix — it's the same screen in a different order.
That class of finding demands **design work from references**: benchmark 2-3 named products whose
personality the brand admires (the system doc usually names a north star — PostHog, Duolingo,
Gumroad, Mailchimp — products that spend real illustration, mascot, and copy budget on their
surfaces), study *how* they fill the equivalent zone, then design the project's own version inside
its system and write the new pattern into the system doc. Restraint (Rams) governs data surfaces;
declared-personality zones (heroes, headers, empty states, celebrations) are where the brand is
*supposed* to spend — quieting them is malpractice in the other direction.

## The lenses (condensed, depth in `references/`)

- **Hierarchy.** One clear primary action; everything else visibly secondary. Encode importance with
  **size + weight + color, not size alone**, a lighter weight or muted color says "secondary" more
  elegantly than shrinking. ~2-3 text colors and ~2-3 weights per surface; never below weight 400 in
  UI. Fold labels into values ("$19/mo", not "Price: $19"). *Emphasize by de-emphasizing.*
- **Whitespace & rhythm.** Start with too much, then remove. Snap **every** gap to one **spacing
  scale** (4/8-based, e.g. `4 8 12 16 24 32 48 64 96`), never arbitrary px. More space *between*
  groups than *within* them (proximity = grouping). "Packed" reads as cheap; deliberate space reads
  as premium.
- **Legibility (hard gates).** Body contrast **≥ 4.5:1** (large text ≥ 3:1); body around **16px**;
  measure **~50-75 characters** per line; body line-height **~1.5**, headings tighter. **Never grey
  text on a colored background**, use a lighter, re-tinted shade of the *background's* hue instead.
- **Alignment.** Fewest strong edges; left-align text and fields to a shared rail; **right-align
  numerics** with tabular figures; optically center irregular shapes (icons/arrows), don't trust math.
- **Data & tables** (Tufte). Maximize data-ink: kill heavy cell borders, gridlines, and decoration.
  Right-align numbers; **emphasize the primary column and demote the rest**; fewer columns (fold
  meta into a caption line); light chips in dense rows; give rows room.
- **Restraint** (Rams / Vignelli). As little design as possible, every element earns its ink. Limit
  typefaces, weights, and accent colors. Prefer durable convention over trend.

## References, read the relevant one when you need depth

- **`references/principles.md`**, the named canon (Rams' Ten Principles, Tufte, the Gestalt laws,
  the Vignelli Canon, Norman, Nielsen's heuristics) with each principle's UI application. Read this
  to *ground and cite* a critique in real design theory.
- **`references/tactics.md`**, the Refactoring UI playbook (Wathan & Schoger): hierarchy, spacing,
  type, color, depth, tables, forms, plus the canonical numbers (scales, measure, contrast, shadows).
  Read this for the concrete *how*.
- **`references/critique-and-anti-patterns.md`**, the structured critique process (heuristic
  evaluation, prioritization) and the senior-flag **anti-patterns** with their de-cluttering fixes
  (the precise "this feels clunky" recipe). Read this when auditing or when a screen feels off but you
  can't name why.
