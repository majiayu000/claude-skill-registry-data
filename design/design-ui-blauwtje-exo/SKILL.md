---
name: design-ui
description: "Use when a page, component, or visual axis changes (type, color, spacing, motion, copy), including a redesign or a surface called empty, boring, or generic. When a new visual surface does not name its displayed data, settings, or behavior, spec decides those first; design-ui follows for presentation. Not for typo-only fixes or behavior with no visual effect."
argument-hint: <page, component or visual change>
effort: high
---

# Visual Design

Design so the result reads polished, modern and cleanly finished in the chosen mood: every visual choice traceable to that mood, the audience, the page job or the content. The enemy is the unfinished default — stock type, flat ground, loose spacing and missing states. The overcorrection is a costume: a theme, metaphor or prop drawn from the subject, such as a barcode or a ledger, unless the user asks for one.

A full or bounded redesign fails when the rendered result stays materially interchangeable with the baseline. It also fails when supporting regions stay generic while one focal point carries the design. It also fails when a large empty area has no content, grouping, pacing, or staging job. Do not default an open axis — composition, type, chromatic hierarchy, surface treatment, imagery, motion — to absence: restraint on one axis needs a brief-side reason and expression on the others.

Every screen ships the scope `references/composition.md` completes and the motion bar of `references/motion.md`, whatever the mood.

**After a compaction notice**, see `## The run directory` of `references/intake.md`.

## Size the request

Any visual change belongs here, at any file count; an undecided surface goes to `spec` first, added state, persistence, a dependency or a network call to `build`.

- **Page or redesign:** a new page/view/identity; a request changing at least three of composition, palette, type, motion, and content hierarchy; or a report that an existing surface is empty, boring, generic, flat, unfinished, or not distinctive. It takes the one pass below; the existing direction is evidence, not a veto.
- **Sketch, new piece, tweak:** `## Sizes` of `references/phase-build.md`.

## Route

Resolve the surface from the markup and style files in the working-tree diff, then the last touched one; with neither, ask only which surface. Then stop at the first matching rung:

1. **Tweak:** the tweak path.
2. **Handed a direction:** a plan's `Contract:` or a brief's `contract-selected.json` is copied to `$RUN/contract-selected.json` and resumes at the build step, skipping the plan.
3. **Asked to choose:** the user asks to see or choose between looks, or the brief's `## Visual direction` names the user as chooser: the offer in `## Asking` of `references/intake.md`.
4. **Sketch:** the sketch path.
5. **Settled identity:** the evidence `## Settled identity` of `references/intake.md` lists, while neither the user nor the brief lets it be replaced: the plan keeps that identity. A component library in the manifest is not that evidence on its own.
6. **Everything else**, a landing or marketing page included: the scope form in `references/intake.md`, then one direction in the plan from its mood and the nearest sibling surface, no offer.

Only a request from the user opens the picker: a landing page or an open identity does not.

## The one pass

The default for every rung but 1 and 4; it builds in this session, with no agent. The references call steps 1-2 Phase 1-2 and steps 3-7 Phase 3; Phases 4 and 5 are the full run's critique and QA.

1. **Context.** Read `## Context`, `## The build floor`, `## Precedence` and `## Judgment` of `references/phase-detail.md`, once.
2. **Plan.** After one line each stating the scope groups and the mood, write a plan of at most 25 lines in the transcript before any edit, under `references/phase-direction.md`. It names the color roles with hex values, the display and body fonts, the motion thesis, and an ASCII layout at 1440 and 390 wide.
3. **Check the plan.** List each scope group, and each section, content item, tone word and constraint the request names, and mark where the plan carries it. Revise the plan until none is missing, because a page built from a plan that dropped a request item is rebuilt.
4. **Build.** Read `references/phase-build.md` first, then build the whole page here and run its proof.
5. **Capture.** Run `node <skill dir>/scripts/capture.mjs --url <file:// or http:// url> --viewport 390x844 --viewport 1440x900 --full-page --label post-build --out "$RUN/renders"`.
6. **Look.** Read `$RUN/renders/post-build-390x844-fullpage.png` and `$RUN/renders/post-build-1440x900-fullpage.png`, and list each fault against the plan, the request and the build floor.
7. **Fix once.** Repair every listed fault in one pass, then report without a second capture; a fault the pass leaves open is named in the report.

A page that does not render reports the capture as blocked and names what went unchecked.

## On request only

The parts below run only when the user's own words ask for them; a page's size, rung or genre never starts them.

- **Variants or a picker** ("show me options", "let me choose"): rung 3.
- **A survey, parallel builders, a critique or QA** ("run the full process", "critique it"): the full run of `## Full run` in `references/phase-detail.md`, where the `exo:survey-ui` agent writes `$RUN/inventory.md`, `exo:build-ui` builds per surface, `exo:critique-ui` judges and a QA delegate checks.

## References

Load a reference only at its row's phase and predicate, never the set up front. `references/phase-detail.md` reads by section; every other reference over 8 KB names its sections in its row and loads by them (`grep -n '^## '`, then `sed -n` to the next heading).

| File | Read it when |
|---|---|
| `references/intake.md` | Before Phase 1: asking, the run directory, symptoms; its `## Settled identity` when Route rungs 1-4 miss. |
| `../route-skills/references/question.md` | Opt-in: Phase 2 on rung 3, before the preview offer. |
| `references/phase-detail.md` | Phase 1: `## Context`, `## The build floor`, `## Precedence`, `## Judgment`; opt-in: `## Full run`, `## The critique dispatch` and `## QA` when the user asks for the full run. |
| `references/phase-direction.md` | Phase 2, before writing the plan. |
| `references/phase-build.md` | Phase 3, before the first edit. |
| `references/visual-direction.md` | Phase 2, every direction decision, whole; Phase 1 `## Design context first` alone when the repository or docs/design/DESIGN.md holds a design system to extract. |
| `references/sketch-tab.md` | Opt-in: Phase 2 on rung 3, after `--check` reports ok and before the offer; elsewhere, before the first visual choice the user asked to see. |
| `references/direction-preview.md` | Opt-in: Phase 2, only when the user asks to see directions whole, before building the picker's comps. |
| `references/composition.md` | Phase 1 `## Inventory before layout`; Phase 2 `## Turn subject evidence into a system`, `## Choose structures from relationships`, `## Write a composition contract`; Phase 3 `## Build density without clutter`, `## Surface obligations`, `## Responsive recomposition`. |
| `references/typography.md` | When choosing or changing type: Phase 2 `## Source by character, not by list` and `## Pairing`; Phase 3 `## Roles`, `## Scale`, `## Micro rules — the craft floor`. |
| `references/controls.md` | Phase 3, before styling a control. |
| `references/implementation.md` | Phase 3, before writing CSS or component code, whole. |
| `references/motion.md` | Phase 3: `## Motion thesis`, `## Job gate` for the bar; before any animation add `## Materials`, `## Timing`, `## Reduced motion`, `## Scroll and view transitions`, and `## Continuity contract` only when the build uses one; add `## Judgment` when the build uses an animation library. |
| `references/interaction-qa.md` | Phase 3 for controls, flows, disclosure, or reachable states; Phase 5 `## Pre-ship interaction sweep` alone. |
| `references/feedback-and-status.md` | Phase 3 when the surface waits on the network, applies a change before its response, or reports status outside the changed region; Phase 5 `## Sweep` alone. |
| `references/visual-critique.md` | Phase 3, the `## Slop tropes` section, before finishing a treatment; opt-in Phase 4 whole, by `exo:critique-ui` only. |
| `references/craft-recipes.md` | Phase 3, before the first CSS of a ground, surface, motion, or type treatment. |
| `references/component-system.md` | Phase 1 `## Adopt before authoring` alone, when the repository ships a component layer; Phase 3 before building a control, field, or surface the design repeats: `## Anatomy`, `## The state row`, `## Scales, not values`, and `## Composite patterns` for a composite. |
| `references/tokens.md` | Phase 2 only: `## Tiers` first, then `## The DTCG format, where a repository uses it` for a token pipeline or DTCG file, `## Naming that survives a rebrand` for a second theme or brand, `## Derive the ramp from contrast` for a ramp generated against target contrast. |
| `references/icons-and-imagery.md` | Phase 3 only when the build draws or extends an icon set, places a raster or chart, or the inventory names imagery. |
| `references/accessibility.md` | Phase 3 only before a composite widget: `## Keyboard contracts` alone; Phase 5 `## Sweep` alone. |
| `references/performance-budget.md` | Phase 3 only when the build adds a hero raster (`## LCP is an art-direction budget`, `## Layout reservation`), an unloaded font (`## Font cost`), or a persistent effect (`## Effect cost`); Phase 5 `## Outcome thresholds` and `## Hard failures` alone. |
| `references/internationalization.md` | Phase 1 when the product ships more than one language, the repository carries translation machinery, or the audience reads a right-to-left or non-Latin script. |

## Judgment

- Explicit brief requirements outrank every design default and tell list.
- A human selection of a rendered variant outranks this skill's own preference.
- Accessibility and complete content/state coverage outrank visual novelty.
- This skill owns visual decisions only.
- When a `spec`, `build`, or `find-cause` stage called it, return control for product decisions, ordering, wiring, persistence, validation, proof, and reporting.
- When no stage called it, execute the visual-only request and report directly.
