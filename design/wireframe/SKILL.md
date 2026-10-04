---
model_tier: inherit
name: wireframe
description: "Explore a flow or layout with 3+ disposable lo-fi greyscale wireframes on a named axis, before any hi-fi work. Use when the user wants to sketch directions or explore structure."
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

# Wireframe

Produce low-fidelity wireframes or storyboards to explore a flow, layout, or
information hierarchy before committing to hi-fi design. Wireframes are
**disposable** — their value is the breadth of options and the decision they
produce, not the fidelity of any one artifact.

## When to use

- The user wants to "explore options", "sketch something out", "see a few
  directions" for a screen, flow, navigation pattern, or hierarchy.
- The design problem is open enough that hi-fi work would be wasted — the
  structure question is not yet settled.

**When NOT to use:** styled, production-viable alternatives on a settled
structure → [`design-variations`](../design-variations/SKILL.md) (hi-fi,
branded, recommendation-bearing). A single refined implementation →
[`fe-design`](../fe-design/SKILL.md) + stack executor.

## Procedure

1. **Confirm the goal.** What is explored (screen / multi-screen flow /
   navigation / hierarchy / interaction model), the imagined user's goal,
   constraints (mobile/desktop, non-negotiable elements), the count
   (3 minimum, 5–6 ceiling), and the **axis of variation**. If the axis is
   open, propose 2–3 (e.g. single-page form vs multi-step wizard vs
   progressive disclosure) and ask which to explore.
2. **Hold the lo-fi conventions** so the output reads as wireframe, not as
   broken hi-fi:
   - greyscale only — black, white, 2–3 grays; no brand color;
   - system sans-serif — no type personality yet;
   - labeled boxes for content areas ("headline", "image", "feature card");
   - striped placeholders with monospace size labels for imagery (the
     honest-placeholder pattern in
     [`fe-design § Craft details`](../fe-design/SKILL.md));
   - short label-style skeleton copy ("Headline goes here / one sentence on
     the value prop") — never Lorem ipsum (per `output-discipline`), never
     final copy.
3. **Sketch ≥3 variations** on the named axis — layout (centered / split /
   grid), information density, flow structure (single page / multi-step /
   progressive disclosure), CTA placement, navigation pattern. Write each
   variation's distinguishing structure down BEFORE sketching it — left
   unspecified, variations converge on near-identical layouts. Order
   by-the-book → off-distribution; at least one genuinely novel bet.
4. **Annotate** — 2–4 numbered callouts per variation naming what is
   interesting and its trade-off ("fastest path, but heavy first
   impression"), placed next to the variation, not in a separate doc.
5. **Capture the decision** after the user picks: chosen variation (or
   hybrid), what attracted them, what they explicitly rejected, new
   constraints surfaced. This capture is the brief for the hi-fi follow-up.
6. **Hand off** — [`design-variations`](../design-variations/SKILL.md) for
   styled options on the chosen structure, or
   [`design-intelligence`](../design-intelligence/SKILL.md) +
   [`fe-design`](../fe-design/SKILL.md) for a single hi-fi direction. In an
   existing codebase the hi-fi step still passes `existing-ui-audit` per the
   `ui-audit-gate` rule.

## Output format

1. **One file** (HTML or annotated markdown/SVG canvas) with ≥3 greyscale
   variations side-by-side — flows as small storyboards (3–5 screens each);
   no brand color, no styled typography, no real imagery.
2. **Per-variation annotations** — 2–4 callouts naming the structural bet and
   its trade-off, inline next to the variation.
3. **Decision-capture block** (after user pick) — chosen direction,
   attractions, explicit rejections, new constraints; framed as the hi-fi
   brief.
4. **No recommendation ranking** — wireframes surface trade-offs; the pick
   belongs to the user (contrast: `design-variations` closes with a
   recommendation).

## Do NOT

- Do NOT apply brand color, brand type, or real imagery — that pulls focus to
  aesthetics before structure is settled.
- Do NOT polish — wireframes are disposable thinking artifacts.
- Do NOT write final copy or Lorem ipsum — label-style skeleton copy only.
- Do NOT let variations converge — write each variation's structure down
  before sketching.
- Do NOT skip decision capture — an exploration round without a recorded
  decision has to be re-litigated in the hi-fi round.
- Do NOT embed system internals (paths, skill/tool names) in the artifact —
  Q13 in [`design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md).

## Gotcha

- This is the one context where rough, hand-drawn-feeling shapes (rectangles,
  lines, simple icons) are acceptable — everything sits at the same low
  fidelity, so nothing reads as a failed asset (the V4/imagery antipatterns
  apply to hi-fi, not here).
- The wireframe file tends to get promoted into hi-fi by incremental edits —
  don't. Start the hi-fi artifact fresh from the decision capture; the
  wireframe's greyscale skeleton hard-codes non-decisions.

## See also

- [`design-variations`](../design-variations/SKILL.md) — hi-fi options on the chosen structure.
- [`design-intelligence`](../design-intelligence/SKILL.md) — grounded direction selection for the hi-fi follow-up.
- [`fe-design`](../fe-design/SKILL.md) — production heuristics + honest-placeholder pattern.
- [`existing-ui-audit`](../existing-ui-audit/SKILL.md) — mandatory pre-step once hi-fi work lands in a codebase.
