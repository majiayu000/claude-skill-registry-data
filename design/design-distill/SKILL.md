---
name: design-distill
category: design
description: >
  Distill a visual style from reference sites/products the user likes, then
  articulate it into a validated, dual-mode design system and a ready-to-run
  Claude Design ("Create Design System") handoff. Crystallized from the
  agents-dashboard run (checkit on handrovermeulen/Obsidian-Dashboard →
  moodboard → dual-mode tokens → Claude Design brief). It is a COMPOSITION
  skill — it fires existing tools (agent-browser capture, the Obsidian-Dashboard
  moodboard method, P18 format discipline, P11 dogfood validation,
  arcan-glass / ui-ux-pro-max) in sequence; it does not reimplement them.
  Core principle: MEASURED, NOT INFERRED — the palette and type come from
  computed styles extracted via headless browser, never from the model
  guessing at a screenshot. USE WHEN: distill a style, capture references,
  build a moodboard, "I like the look of X / use these as references",
  extract a palette from a site, design tokens from screenshots, create a
  design system from references, dual-mode (dark+light) design system, make a
  Claude Design brief / "run this through Claude Design". NOT FOR: implementing
  a UI from an existing design system (use design-engineering / impeccable /
  ui-ux-pro-max), brand-facing Broomva styling (use arcan-glass), neutral
  artifact research with no design intent (use checkit), or primitive promotion
  (that's a bstack-engine act). Triggers on the phrases above + /design-distill.
---

# design-distill — references → design system → Claude Design

Turn "I like the look of these sites" into a **measured**, dual-mode design
system plus a **diff-ready Claude Design brief** — without ever inventing a
colour or font.

## The one rule

> **Measured, not inferred.** Never describe a reference's palette or type from
> what a screenshot *looks like*. Extract the **computed styles** with a headless
> browser and report the hex/font you measured. The moodboard method's
> *"describe only what you see"* constraint is enforced by measurement, not by
> the model's eye. A palette value with no `getComputedStyle` provenance is a
> bug, not a description.

Corollary (no-ask-back, inherited from checkit): when the user shares references
with a terse directive ("use these", "a mix of those two"), infer the design
intent, state it in one line, and proceed. Surface costly/irreversible forks
(hero device, accent hue, scaffold target) as **ranked next steps with a
recommended default** — proceed on the default for reversible token-level work.

## Pipeline (what `/design-distill <refs>` does)

1. **Ingest + declare intent** — one line: *"Distilling <refs> into a
   <dark|light|dual>-mode design system for <product>."* Name the originating
   method if there is one (e.g. the Obsidian-Dashboard moodboard step).

2. **Capture + MEASURE** (agent-browser) — for each reference, in each available
   mode: screenshot + `eval` a computed-style extractor (bg/surface/text/muted/
   border, button + link colours, h1 font/size/weight, body font). Handle the
   three site classes (see `references/capture-recipe.md`):
   - respects `set media` → capture dark + light directly;
   - manual toggle (ignores media) → click the theme button, re-measure;
   - single-mode (pins theme) → record as a one-mode anchor, don't fake the other.
   **View the screenshots** to catalogue imagery/layout/motion (the part you
   genuinely must see); measure everything quantitative.

3. **Distill** — synthesize the references: find the **shared DNA** and the
   **productive tension** (the axis the user must decide on). Produce the
   moodboard files per the Obsidian-Dashboard method — `Moodboard.md` (per-ref
   catalogue, measured values, confidence tags), `Design-Brief.md`, `Fonts.md`
   (observed faces + self-hostable substitutions). Markdown (P18 substrate).

4. **Articulate dual-mode** (if asked) — map references to ONE warm/neutral
   palette with semantic tokens, dark + light variants. Pick anchors honestly
   (e.g. warm-dark from ref A, warm-light from ref B; reject a ref's own
   off-direction mode). State the mix in one line.

5. **Generate the design system** in-stack (Tailwind v4 + shadcn, arcan-glass
   aligned): `colors_and_type.css` (dual-mode tokens + type scale + radii/
   spacing/motion), `theme.css` (`@theme inline` → utilities), shadcn JSX
   stubs (`ui-kit/*.tsx`, cva variants), and a **self-contained HTML specimen
   that RUNS the palette** (dogfood — the page is the spec), + a README.

6. **Validate by interacting** (P11) — render the specimen via agent-browser,
   screenshot **both** modes, confirm the toggle flips and console is clean.
   A design system you haven't watched render in both modes isn't validated.

7. **Claude Design handoff** — emit the **upload manifest** (curated,
   non-redundant reference images + the 3 moodboard `.md`) and a **self-contained
   paste-ready prompt** (`templates/claude-design-prompt.template.md`) that
   instructs Claude Design to *refine, not diverge* — so its output is a clean
   **diff** against the in-stack version, not a competing direction. Give
   absolute paths; offer a one-drag zip.

8. **Document proactively** (P6) — file/refresh the entity for any reusable
   insight; if the flow recurs, add/update the bstack-engine candidate-ledger
   row. Never ask permission — file, then report.

## Composition map

| Step | Composes |
|---|---|
| Ingest + intent | **checkit** (no-ask-back artifact intake, P17) |
| Capture + measure | **agent-browser** (`set media`, `eval` computed styles, `screenshot`) — recipe in `references/capture-recipe.md` |
| Distill → moodboard | Obsidian-Dashboard **moodboard method** (`handrovermeulen/Obsidian-Dashboard`) |
| Dual-mode tokens | `[[obsidian-as-middle-layer]]` sibling design work; semantic-token discipline |
| Generate system | **arcan-glass** / **ui-ux-pro-max** (Tailwind v4 + shadcn), P18 (md substrate + HTML specimen) |
| Validate | **P11** dogfood (agent-browser render in both modes) |
| Claude Design handoff | this skill's prompt template; P18 Audience |
| Document | **P6** Bookkeeping + `[[measured-style-capture]]` |

## Worked example (canonical instance)

`~/broomva/docs/moodboard/agents-dashboard/` — the agents-dashboard run end to
end: 11 captured refs (paperclip.ing / cofounder.co / linear.app / attio.com),
`moodboard.html`, and `design-system/` (tokens + theme + ui-kit + specimen +
`claude-design-prompt.md`). Read it as the reference output shape.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I can read the palette off the screenshot." | No. The model approximates colour; CSS is exact. Measure with `getComputedStyle` or it's invented. |
| "`set media light` didn't change it — guess the light mode." | The site pins its theme or uses a manual toggle. Click the toggle, or record it as a single-mode anchor. Never fabricate the missing mode. |
| "A markdown spec is enough." | The specimen must RENDER. Dogfood both modes (P11) or it isn't validated. |
| "Just give them the in-stack system, skip Claude Design." | If the user asked to run Claude Design, produce the manifest + diff-ready prompt. Don't substitute your output for the tool they chose. |
| "Ask which accent / hero they want." | Recommend a default, proceed on it (token-level = reversible), surface alternatives as ranked next steps. |
| "Should I file a KG entry?" | Never ask (P6). File the insight, report after. |

## Scope

- **In scope**: any "I like the look of X → give me a design system" request;
  reference-driven moodboards; dual-mode token systems; Claude Design briefs.
- **Out of scope**: building the actual app from the system (hand to
  design-engineering / the scaffold step); brand-facing arcan-glass work;
  neutral research (checkit).

## Validation (skill self-test)

A `/design-distill` run is complete iff: inferred-intent line stated, no
bounce-back on reversible steps · every palette/type value has `getComputedStyle`
provenance (measured, not inferred) · moodboard `.md` produced with confidence
tags · dual-mode tokens with semantic names (if dual-mode asked) · specimen
rendered + screenshotted in **both** modes with a clean console (P11) · Claude
Design manifest + diff-ready prompt emitted with absolute paths · ≥1 insight
filed proactively (P6).

## References

- `references/capture-recipe.md` — the agent-browser measured-capture recipe
  (the load-bearing, reusable mechanism: dual-mode capture + the three site
  classes + the computed-style extractor + dogfood validation).
- `templates/claude-design-prompt.template.md` — parameterized Claude Design
  "Create Design System" prompt (refine-not-diverge).
- `research/entities/pattern/measured-style-capture.md` — the core insight.
- `research/entities/pattern/obsidian-as-middle-layer.md` — origin artifact.
- `research/entities/pattern/bstack-engine.md` — crystallization candidate row.
