---
name: design-qa
description: Rigorous visual QA and polish pass over a component, a page, or a sweep across several. Renders the target in both themes, magnifies the details, judges the craft against a durable rubric and the rendered siblings, fixes the defects, and reports the taste calls. Use when asked to design-QA something, polish a component or page, judge whether something looks good enough, or find visual inconsistencies across components or pages.
icon: frame_inspect
displayDescription: "Renders the target in both themes, magnifies its seams, corners, and states, and lines it up against its nearest rendered siblings. Judges the arrangement against the fundamental principles (proximity, alignment, repetition, contrast, spacing) and the parts against component-scale craft checks, fixes what has one right answer, and reports the taste calls that need a decision."
invoke: ["design QA [Name]","polish the [Name] component","is [Name] good enough","design QA the [category] components"]
---

# design-qa

The taste gate. Find everything a designer who owns the system would notice and send back — especially the things nobody wants to spend time calling out — then fix what has one right answer and surface what doesn't.

This skill judges **rendered pixels**, not source code. Code review can confirm the tokens are right; this pass decides whether the thing is good.

## When invoked

Use this skill when asked to design-QA, polish, or judge something visual — phrases like "design QA [Name]", "polish the [Name] component", "is [Name] good enough", "look at these buttons", "review the [category] components together". It also runs as the mandatory quality gate inside the `new-component` skill (see the last section).

## Scope

Accept any of:

- **A page** → a URL path on the website. Page reviews inherit the `visual-review` skill's viewport matrix — both themes at desktop *and* mobile widths — since an arrangement that only holds at one width isn't holding
- **A sweep** → several components or pages at once ("the form controls", "every page under /foundations"), each judged individually *and* against the others — cross-target inconsistency is the sweep's whole point

If no target is given, default to what this session built or changed. Ask only when genuinely ambiguous.

## Ground rules — why this pass doesn't go stale

- The rubric below is principles, deliberately free of facts about real components. **Facts come fresh each run**: the design system's spec and component list live in its own repo and are read there when needed, and the standard for consistency is siblings **rendered** now — never a remembered lineup or a list written here.
- Judge the render first, the source second. A seam defect lives in pixels; the CSS that caused it comes after the finding, as the fix's address.
- Component names in this skill's examples are fictional by design — a factual claim about a real component inside an example rots silently.

## Evidence

Use the browser/preview tools the harness provides for every step below; never launch a dev server through a raw shell command.

1. **Render the real thing.** The `website` configuration in `.claude/launch.json` (theme is `data-theme` on the root element; the `visual-review` skill's step 3 and Key context document how to switch it — verify the attribute actually changed before capturing — and what page chrome to expect).
2. **Capture the matrix.** Every variant and state, in light **and** dark. Then **magnify the details**: zoomed crops of every join, corner, divider, icon seat, and focus ring. Seam defects — a doubled border where two segments meet, a divider a pixel taller than its track, a radius that doesn't flow through a join — are invisible at 1x and glaring at 3x. If the harness offers a zoom or region capture, use it on every joint the component has; if not, scaling the render up (a transform on the story root works) is a fine substitute. One capture-environment trap: after a programmatic theme flip in a hidden browser pane, CSS transitions can freeze mid-flight (paused rendering never advances them), so a token can screenshot at neither theme's value and read as a broken palette. Before judging any colour, let the page settle in a fronted tab or force-finish the page's animations — and when a colour still looks wrong, confirm it with computed styles before writing the finding.
3. **Drive the states for real.** Hover, focus-visible (reached by keyboard, not click), active, disabled, loading, empty, error. Capture each. A state you didn't render is a state you didn't review. On a page review, the layout-mounted chat button's hover-summoned summary panel counts as one of the page's states — summon it and let the reveal settle. The chat panel and its suggestion chips animate on open, close, and reveal (design.md's Site chat pattern owns the choreography): capture after they settle, and read a mid-flight frame — a part-transparent panel, shimmer pills where chips belong — as animation, not defect.
4. **Stress the content.** Longest plausible label, most items, zero items, a narrow container, wrapping text. Use story controls or a scratch story; don't ship the scratch.
5. **Line up the siblings.** Pick the two or three nearest relatives by role — same registry category, or same pattern family (everything pill-shaped, everything with a chevron, every card) — and capture the same crops of them. Consistency findings come from this lineup, not from memory. For a page: one or two established pages of the same type.
6. **Read the source.** The page's own `page.tsx` and `page.module.css`, and the design system's Composition rules (in its repo) if a layout question turns on them — the token rules, and the component or page source. After the visual pass, to name causes and to check behaviour pixels can't show.

## The eye — the design principles

These describe the arrangement, not the parts. The design system already governs the parts — the tokens, radii, type, and their validators decide what a component may be made of. A layout assembled one component at a time will satisfy every token and still be wrong, because these properties only exist between components. Evaluate them after assembly, looking at the whole. They are also the vocabulary findings are written in: "not good enough" only becomes fixable once the violated principle has a name.

### Proximity

Space encodes relationship, and it is read before anything else on the screen. Uniform spacing claims nothing is related to anything. The authoritative rule — and the rhythm ladder that makes it actionable — is the design system's own spec, in its repo. Read the rendered result here. This heading is the name the finding gets.

### Alignment

Every element belongs to a shared structure. Placement is never arbitrary and never local. An element positioned correctly relative to its neighbour but not to the composition is misaligned — and this is the most common failure when building a layout piece by piece.

### Repetition

A treatment used consistently becomes a signal. The same role gets the same treatment throughout, which is what makes deviation legible as emphasis rather than as inconsistency.

### Contrast

Differences must be unmistakable. Anything not the same must be clearly different, since near-sameness reads as error. Attention needs somewhere to land first.

### Spacing

Padding belongs to the component; margin belongs to the layout. The rule itself is the design system's Composition rule 1 (parent owns spacing) — cite it there; the finding to watch for is a component asserting a relationship it cannot see by carrying its own outer margin.

### After assembly

Stop and look at the full composition before finishing:

- What structure do the elements share? If you cannot name it, there is no alignment.
- What does the spacing say about what belongs together? Is that true?
- What does the eye land on first? Is that correct?
- Which treatments repeat, and which are one-offs? Can each one-off be justified?

## The craft checks — the same principles at component scale

Inside and between a component's own parts, judged at magnification, per theme:

**Geometry and joins**

- **Optical beats mathematical.** Icons, chevrons, punctuation, and round shapes carry uneven visual weight, so a mathematically centred glyph often looks off-centre. Judge centring by eye at 3x, never by the box model.
- **Concentric corners.** A nested radius relates to its parent's through the padding between them; equal radii on nested boxes look wrong at the corner. (the design system's spec records its worked example in the Composer geometry.)
- **Joins render once.** Where two segments share an edge — a split control, an attached input-and-button, a segmented anything — the shared border must not double, the group's outer radius must flow through as if it were one shape, and any divider spans exactly the height it should. The two halves must look designed together in *every* state: capture the compound in each state and ask whether the treatment of the inactive half was chosen or inherited.
- **Hairlines are crisp.** 1px lines land on the pixel grid; a soft, blurry border means a half-pixel offset somewhere.

**States as a family**

- **Every state designed, not derived.** A loading state is composed — spinner colour, size, and seat all look chosen — not "opacity plus a spinner". Disabled reads as one coherent treatment, not per-part fading.
- **States don't move geometry.** Hover, focus, and loading never shift layout, resize the control, or reflow the label. Compare each state crop pixel-for-pixel against the resting crop.
- **The family shares logic.** If hover deepens the fill on one variant, it deepens it on all. A state treatment that exists on one component of a pattern family and not its siblings is a Repetition finding, whichever side is right.

**Theme parity**

- Dark is designed, not inverted. For each key crop, put light and dark side by side: fills, strokes, and elevation must make the same statement in both. A treatment that reads as a solid fill in light and dissolves into the background in dark is a Contrast finding.

**System fidelity**

- The right component is used — a page re-implementing an existing library pattern in local CSS is a Repetition finding even when it looks fine today.
- Icons match the type: an icon's stroke weight sits with the font weight beside it; a heavy icon next to light text reads as borrowed from another system.
- The action colour means action, status roles carry status, and visible copy follows `content-design.md`. Token *compliance* has its own skill (`token-audit`); here, judge what the token **choices** look like — a legal token in the wrong role is exactly the kind of thing this pass exists to catch.

## Judging

The bar is a three-second glance from the designer who owns the system. The founding rule of this skill: **the findings nobody wants to spend time writing up are exactly the findings to write up.** "The buttons on the new component are not good enough" is a legitimate trigger; this pass exists to turn that sentence into named, located defects.

Every finding names the principle or craft check it violates, and each is classified:

- **Defect** — objectively wrong against the rubric, the spec, or the sibling lineup: a doubled seam, an off-grid hairline, a state that shifts layout, an inconsistent gap. One right answer. *Fix it.*
- **Polish** — a clearly better version is available, and the change is small and safe: an icon a shade too heavy, padding a step too tight, an abrupt transition where every sibling eases. *Fix it.*
- **Direction** — more than one defensible answer, or it changes the design: this variant shouldn't exist, this layout wants a rethink, this empty state needs different content. *Recommend one option; don't apply.*

## Polish loop

For every defect and polish finding:

1. Fix at the source — component CSS/TSX or the page module. The fix itself obeys all the library's token and motion rules (the `new-component` skill's `ComponentName.css` section is the reference).
2. Re-render and re-capture **the same crops**. Keep the before/after pairs.
3. Re-run the eye over the changed area — fixes cause regressions too.
4. Loop until a full pass yields no new defect or polish findings.

## Report

Lead with the verdict, evidence attached:

```
## Design QA: [target]

**Verdict:** [clean | N findings fixed, M decisions open | sent back — needs direction before polish helps]

### Fixed
- [what was wrong, one sentence] → [what changed] (before/after crops)

### Open decisions
- [the taste call] — recommendation: [one option and why]

### Checked and clean
[One short paragraph: which variants, states, themes, stress cases, and siblings
were actually reviewed — so "clean" has a defined coverage.]
```

Reference the exact element and file, e.g. "the divider in Gadget's split variant sits 1px proud of the fill (Gadget.css:47)" — the component in that example is fictional by design.

## Guardrails

- **Contrast findings:** the `color-contrast` axe rule is deliberately switched off — rule-wide, every pair — by a settled decision, and the comment beside the override in `scripts/validate-website-a11y.mjs` is its authoritative record (the shipped action pairings it discusses clear AA). Read it before raising any contrast finding, and never re-raise the decision itself as a finding without asking Rob first.
- **Page reviews** inherit the false-finding caveats in the `visual-review` skill's Key context — the ambient background's two renderers, the layout-mounted chrome, `desktopOnly` nav — read that section before judging a page screenshot.
- **A clean pass is a valid outcome.** Don't invent findings to justify the run; state what was covered and stop.

## As a gate

When invoked on work in progress rather than as a review, this is a gate, not a report: loop until no defect or polish findings remain, fold any open direction calls into the hand-off summary, and treat "renders correctly" as necessary but nowhere near sufficient. Before registration the build gate is `npm run verify`, which runs the generators and validators before it builds.
