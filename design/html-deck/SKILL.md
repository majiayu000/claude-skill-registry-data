---
model_tier: inherit
name: html-deck
description: "Build a slide presentation as one HTML file — fixed 1920×1080 canvas letterboxed to any viewport, layout-system-first, type floors. Use for deck, slides, presentation, or pitch requests."
domain: product
personas: []
workspaces:
  - engineering
packs:
  - frontend-design
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# HTML Deck

Build a slide presentation as a single HTML file with fixed-size slides that
letterbox to any viewport. A deck is fixed-canvas media (default 1920×1080,
16:9) — a different medium from responsive UI and from static posters.

## When to use

> **Cross-surface handoff.** A deck often consumes upstream analysis
> (spreadsheet → deck, research → deck). Read the handoff envelope from
> [`surface-agent-contracts`](../../../docs/contracts/surface-agent-contracts.md#cross-surface-handoff-envelope):
> trust `verification_already_done` (don't recompute the source's numbers),
> carry the asset list, and keep source restrictions intact.

- The user asks for a deck, presentation, slides, or a pitch as a web/HTML
  deliverable.

**When NOT to use:** static single-image visual art (poster, PNG/PDF
one-off) → [`canvas-design`](../canvas-design/SKILL.md). Responsive product
UI → [`fe-design`](../fe-design/SKILL.md) + stack executor. Multiple styled
options of one screen → [`design-variations`](../design-variations/SKILL.md).

## Deck fidelity floor

The deck surface's floor (per
[`surface-agent-contracts`](../../../docs/contracts/surface-agent-contracts.md)):

- **Outline before slides.** Draft the slide outline (title + one-line intent
  per slide) before building any slide; when audience or tone is ambiguous, ask
  once. (fixture: `ssac-deck-missing-notes`.)
- **Labels + speaker notes.** Every slide carries a stable label and speaker
  notes, not just on-slide text.
- **Visual rhythm + readable scale.** Consistent spacing/hierarchy across
  slides; never sub-readable text (the type floors below). (fixture:
  `ssac-tiny-slide-text`.)
- **Image/asset provenance.** Real assets via the project path, no invented
  brand evidence ([`design-fidelity`](../../rules/design-fidelity.md) § Asset &
  imagery discipline).
- **Export verification.** Verify the deck exports/renders
  ([`design-artifact-verification`](../../../docs/contracts/design-artifact-verification.md));
  on a host without export capability, say what could not be verified rather
  than claiming a clean export.

## Procedure

1. **Discovery.** Confirm: audience (engineers / executives / customers —
   determines tone and density), aspect ratio (16:9 default), slide count vs
   time budget (~1 slide/minute; most decks land at 8–15), tone, source
   material (PRD/doc — read it before sketching), speaker notes (off unless
   requested), and the brand / design system. No brand →
   [`design-intelligence`](../design-intelligence/SKILL.md) direction first.
   A fully specified ask ("5-slide deck for the all-hands from this PRD")
   skips the question round.
2. **Commit to a layout system before any slide.** 4–6 layout types (cover,
   section header, content, quote/pull-out, comparison two-column, closing/
   CTA); per layout: background, headline size/position, body area, footer
   treatment. 1–2 background colors across the deck (section headers may
   break to a third). Record the system as a comment block at the top of the
   file.
3. **Start from the deck-shell starter** (`templates/deck-shell.html`,
   skill-local): fixed-canvas scaling + letterboxing, keyboard/tap
   navigation, slide counter, `localStorage` slide-index persistence,
   print-to-PDF CSS. Each slide is a direct child `<section>` with a
   1-indexed `data-screen-label` ("01 Title") so the user can reference
   slides by the counter they see.
4. **Build slide-by-slide, reveal early.** Show the file at 1–2 slides —
   don't perfect 15 in private. Per slide: one primary message; **type
   floors on a 1080p canvas: body ≥24px (32px+ preferred), headlines
   60–96px+**; tokens from the active brand/design system (precedence per
   `brand-source-of-truth`, emission per
   [`design-tokens`](../design-tokens/SKILL.md)); honest placeholders for
   missing imagery (striped background + monospace size label — see
   [`fe-design § Craft details`](../fe-design/SKILL.md)); cut filler slides
   ("Why choose us?", "About this deck") and data that doesn't support the
   slide's point.
5. **Speaker notes only when requested** — as a toggleable overlay or
   per-slide `<aside hidden>`, never printed.
6. **Quality gate.** Run `lint_design_slop` over the file; honor the
   outward-artifact hygiene floor (Q13 in
   [`design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md))
   — no workspace paths, skill/tool names, or generator traces in markup or
   comments; final pass → [`design-review`](../design-review/SKILL.md).
   Verify scaling + navigation + persistence once in a browser before
   delivery.

## Output format

1. **One self-contained HTML file** built on the deck-shell: fixed-canvas
   `<section>` slides with 1-indexed `data-screen-label`s, letterbox scaling,
   keyboard/tap navigation, slide counter, `localStorage` persistence,
   print-to-PDF CSS.
2. **Layout-system comment block** at the top of the file naming the 4–6
   layout types and the background-color budget.
3. **Type-floor compliance** — body ≥24px, headlines 60–96px+ on the 1080p
   canvas; deviations only with a stated reason.
4. **Clean slop scan + Q13** — `lint_design_slop` findings resolved or
   DESIGN.md-justified; no system internals in the artifact.

## Do NOT

- Do NOT hand-roll the scaling/navigation — start from the deck-shell
  starter; re-derived viewport math drifts.
- Do NOT use responsive units/breakpoints inside slides — a deck is
  fixed-canvas; the shell scales the whole stage.
- Do NOT drop body text below 24px on a 1080p canvas — projector legibility
  is the floor, not a preference.
- Do NOT pad with filler slides or invented stats — every slide earns its
  place.
- Do NOT introduce per-slide ad-hoc colors/spacing — the layout system from
  step 2 is the budget.
- Do NOT embed system internals (paths, skill/tool names, generator traces)
  in the file — Q13.

## Gotcha

- `localStorage` persistence keys on `location.pathname` — two decks served
  from the same path share a slide index; rename the file per deck or extend
  the key when hosting several decks under one path.
- Print-to-PDF uses the fixed canvas per page: browsers map it onto the
  paper size — set the print dialog to landscape + "fit to page" or the
  slides clip; test one print preview before shipping a PDF.
- Emoji in slide headlines is the CP5 tell exactly as in product UI — the
  deck medium doesn't exempt it.

## See also

- `templates/deck-shell.html` (skill-local) — the canonical shell; copy, don't re-derive.
- [`canvas-design`](../canvas-design/SKILL.md) — static posters/one-frame art (not decks).
- [`design-intelligence`](../design-intelligence/SKILL.md) — direction/palette/type grounding.
- [`design-tokens`](../design-tokens/SKILL.md) / [`brand-to-tokens`](../brand-to-tokens/SKILL.md) — token precedence and emission.
- [`design-review`](../design-review/SKILL.md) — final review gate.
- [`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md) — catalog, CP5, Q13.
