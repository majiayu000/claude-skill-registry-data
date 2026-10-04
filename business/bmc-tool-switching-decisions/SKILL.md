---
name: bmc-tool-switching-decisions
description: "Decides when to move from the BMC to another tool (Value Proposition Canvas, Lean Canvas, Mission Model Canvas, financial modeling, multiple parallel canvases) and assesses the quality of the canvas, hypothesis, and segment using three decision criteria before moving to the testing phase."
---

# BMC Tool Switching Decisions

## Purpose

Helps recognize when the BMC is no longer (or never was) the right tool
for the question at hand, and what to switch to instead. Also includes
three decision criteria that determine when a canvas, hypothesis, or
segment is good enough to move to the next phase.

## Anchored in research

Based on the owner's private research layer (an April 2026 expert
interview)
(`30_domain_packs/bmc/facilitation/tool_switching_logic.md` and three
`08_decision_model/decision_types/*.md` files — all
`status: template`, `source: research_layer`), a synthesis drawing on
Jeffries, Strategyzer, Ash Maurya (Lean Canvas), Blank (Mission Model
Canvas), and van der Linden.

## Method

### A. When to switch tools

1. **Switch to the Value Proposition Canvas (VPC)** when the team can't
   clearly articulate the customer's jobs, pains, and gains for the
   primary segment — the BMC's value proposition block is too small a
   space for this work. Osterwalder's own Value Proposition Design
   (2014) frames the VPC as a zoomed-in tool for exactly this block; in
   many professional practices it's done as prep work BEFORE a BMC
   session, not as an escape route from one.
2. **Switch to the Lean Canvas** when the primary uncertainty is
   problem-solution fit, not business-model fit. Ash Maurya's Lean
   Canvas (*Running Lean*, 2012) replaces: key partners → problem, key
   activities → solution, customer relationships → unfair advantage,
   revenue streams → existing alternatives. Use when: very early stage,
   founder-led, and the question "is this a real problem?" is still
   open.
3. **Switch to the Mission Model Canvas** when the organization doesn't
   run on revenue logic — nonprofit, government, mission-driven.
   Steve Blank and Pete Newell's Mission Model Canvas (2016) replaces:
   customer segments → beneficiaries, revenue streams → funding sources,
   customer relationships → buy-in/support mechanisms.
4. **Switch to financial modeling** when the cost structure or revenue
   streams need numerical precision that sticky notes can't provide. The
   BMC isn't a spreadsheet. Once decisions depend on unit economics,
   margins, or runway, a separate financial model is needed.
5. **Stay in the BMC but split into multiple canvases** when the
   organization has more than one genuinely distinct business model
   (different segments requiring fundamentally different value
   propositions, channels, and cost structures). One canvas produces a
   false average — every distinct model needs its own canvas.

### B. Three decision criteria

6. **Canvas quality decision** — threshold criterion: does the canvas
   pass the Hook Rule (see `../bmc-canvas-diagnostic-reading/SKILL.md`)?
   If a fundamental contradiction exists between the value proposition
   and the cost structure, or between the segments and the revenue
   streams, the canvas isn't ready — fix the contradiction first. If
   consistent, assess: segment specificity, value proposition quality,
   evidence honesty. Outcomes: **proceed to testing** (12+ points on the
   rubric AND no fundamental contradictions), **proceed with a flag**
   (8-11 points, an identified weakness that doesn't block initial
   testing but must be fixed within the first two test cycles), **send
   back for rework** (below 8 points OR a fundamental contradiction).
7. **Hypothesis quality decision** — three requirements: **testable**
   (would the result of an experiment change the team's belief?),
   **precise** (does it include numbers, timeframes, or thresholds —
   "customers would pay more for faster delivery" is NOT precise, "60%
   of current users would pay a 5% premium for same-day delivery" IS),
   **isolated** (does it test exactly one variable — if a hypothesis has
   an "and" in it, it's testing two hypotheses). "Clueless Corner"
   prioritization: plot hypotheses by importance to business success
   (vertical axis) against strength of current evidence (horizontal
   axis) — the upper-left corner (high importance, no evidence) gets
   tested FIRST, not last, because discomfort signals risk.
8. **Segment validity decision** — four criteria: the segment can be
   described through jobs, not just demographics; payer and user are
   distinguished when they differ; the segment is specific enough to
   produce testable hypotheses; the segment isn't defined by the
   founder's own network (the most common hidden invalidity: the segment
   is really "people we already know who've expressed interest" — this
   is a discovery starting point, not a validated segment).

## What this skill does NOT do

- Doesn't do financial modeling itself — it only identifies when it's
  needed and points the way there.
- Doesn't contain the owner's own line between canvas work and financial
  modeling, their own timing for bringing in the VPC, or their own
  experience with the Lean Canvas / Mission Model Canvas — these remain
  open as `[EXPERT INPUT]` sections in the source files.
- Doesn't replace `../bmc-canvas-diagnostic-reading/SKILL.md` for
  assessing a canvas's internal quality — it uses that skill's Hook Rule
  concept as a threshold criterion but doesn't repeat the full
  diagnostics.

## Refinement notes

- When do you bring in the VPC? Do you use it routinely before the BMC,
  or only when the BMC gets stuck?
- Do you use the Lean Canvas? When? Do you switch between them mid
  engagement?
- Have you used the Mission Model Canvas? What adaptations do you make
  for mission-driven clients even when they're using a regular BMC?
- Where's YOUR OWN line between canvas work and financial modeling? Do
  you do both, or hand off?
- When have you used multiple parallel canvases? What triggered the
  split?
- What's your real proceed/return threshold for canvas quality?
- How do you help teams prioritize hypotheses? What's the most common
  mistake in hypothesis prioritization?
- What's your own segment validity test in practice?

## Continue from here

- Previous skill in the same pack:
  `../bmc-canvas-diagnostic-reading/SKILL.md` — the Hook Rule and other
  diagnostic rules this skill's threshold criterion uses.
- Related skill in the same pack:
  `../bmc-innovation-pattern-matching/SKILL.md` — by the time the BMC
  hands off to financial modeling, the pattern choices have already been
  made.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../CLAUDE.md` — this pack's shared guardrails
