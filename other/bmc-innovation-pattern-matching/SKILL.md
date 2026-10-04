---
name: bmc-innovation-pattern-matching
description: "Identifies and justifies 3-5 compatible business model innovation patterns (from the public 159-pattern innovation library) for a given business context, using the expert's own four-part innovation taxonomy (Financial/Operative/Value-based/Experience Model Innovations)."
---

# BMC Innovation Pattern Matching

## Purpose

Helps find a genuinely distinctive, non-trivial innovation direction for a
business model — not a generic "add AI and a subscription model"
combination, but a justified selection of 3-5 mutually compatible patterns
from the 159-pattern library, placed within the expert's own four-part
interpretive framework for WHERE business model innovation typically comes
from: finance, operational superiority, the value proposition, or the
customer experience.

## Anchored in

- The owner's consulting expertise in BMC work, from an April 2026 expert
  interview (the owner's research notes,
  `30_domain_packs/bmc/tools/bmc_innovation_patterns.md`, `status: accepted`,
  `confidence: high`). The expert's own quote: "How a business model
  works as a source of business model innovation — how to make business
  model innovations using BMC — this requires clear choices in the canvas,
  followed by the ability to identify innovation patterns."
- The public innovation pattern library's machine-readable set of 159
  patterns, in four groups / 13 sub-models — see
  `../../references/bmc-innovation-pattern-library.md`. The library's
  four-part structure (Financial/Operating/Value/Experience Model) is
  identical to the expert's own taxonomy — these two sources reinforce
  each other rather than conflict.
- The task specification for the recommendation process that came with the
  library — see `../../references/bmc-source-material-notes.md` section 1.

## Method

1. **Gather the business context before browsing patterns.** You need at
   least: the target customer profile (ICP), the solution category, the
   nature of the market (competitive situation, maturity), and a rough
   sense of the cost structure (e.g. high fixed capital vs. variable
   cost). Without these, pattern selection becomes an arbitrary list.
2. **First identify the innovation direction using the expert's four-part
   taxonomy** (`../../references/bmc-innovation-pattern-library.md`
   opening section) — ask: where is THIS business model's distinctive
   value most likely to come from?
   - Finance (cost strategy + revenue model combination)
   - Operational superiority (key activities + key partners combination)
   - Value proposition (value proposition + customer segments relationship)
   - Customer experience (channels + customer relationships combination)
   More than one direction may be relevant, but choose one PRIMARY
   direction before browsing patterns — this prevents the "pick everything
   that sounds good" mistake.
3. **Browse the sub-models of the chosen group** in
   `../../references/bmc-innovation-pattern-library.md` and pick 3-5
   patterns that:
   - are contextually relevant (not just "sound good")
   - are not mutually contradictory (e.g. Cost Leadership vs. Premium
     Pricing in the same model is a contradiction — see step 4)
   - are achievable with the described team size/resources
4. **Check for contradictions explicitly.** The library's own rules
   (see `../../references/bmc-source-material-notes.md`) require avoiding
   contradictory patterns — e.g. cost-leadership and premium-pricing
   patterns in the same recommendation are internally contradictory unless
   the contradiction is explicitly justified (e.g. segmented pricing for
   different customer groups).
5. **Record for each selected pattern:** the `pattern_id` (full path,
   e.g. `financial.cost.ai_as_a_service`), the pattern name, the
   sub-model, and a 2-3 sentence justification of WHY this particular
   pattern fits the given context — not the pattern's generic description
   as-is.
6. **Record `conflicts_avoided`**: which obvious but contradictory
   patterns were deliberately left out, and why.
7. **Record `assumptions`**: what assumptions were made about the
   context, if the context the user provided was incomplete on some
   dimension.
8. **Move the selected patterns onto the canvas** — see
   `../bmc-canvas-clarity-and-iteration/SKILL.md` for the next step
   (building a variant based on the selected patterns).

## Gotchas

- Step 2 requires committing to ONE primary taxonomy direction before
  browsing patterns. Browsing the library first and rationalizing a
  direction afterward is exactly the "pick everything that sounds good"
  failure mode step 2 exists to prevent.
- Step 4's contradiction check (e.g. cost-leadership vs. premium-pricing) is
  only a violation when it's unjustified — segmented pricing for different
  customer groups is a valid exception. Treating the rule as an absolute
  "never combine these two" will wrongly reject legitimate multi-segment
  strategies.
- Step 1's four context inputs (ICP, solution category, market nature, cost
  structure) are prerequisites, not optional color. Selecting patterns
  against an incomplete context without recording it in `assumptions` (step
  7) produces a recommendation that looks justified but can't be traced
  back to what was actually known about the business.
- The library is closed at 159 patterns — per "What this skill does NOT
  do," a context that calls for something the library doesn't cover must be
  named as an explicit gap, not silently mapped onto the nearest existing
  `pattern_id`.
- This skill stops at pattern selection and hands off to
  `../bmc-canvas-clarity-and-iteration/SKILL.md` to actually build a canvas
  variant — treating the `pattern_id` list plus justifications as a
  finished recommendation, without that handoff, skips the step where the
  pattern gets tested against a real canvas.

## What this skill does NOT do

- Doesn't choose a pattern for you as a final decision — it produces a
  justified recommendation of 3-5 patterns, but the final choice of
  business model is always a human decision.
- Doesn't do financial modeling or profitability calculations for the
  chosen pattern — it only identifies and justifies the pattern's fit.
  Numerical validation belongs to later, more precise tools (see
  `bmc_expert_profile.md`'s own scoping of the BMC's role).
  See also `../bmc-tool-switching-decisions/SKILL.md`.
- Doesn't replace `../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  — this skill is narrower and tied to the pattern library, not a general
  AI-opportunity-portfolio prioritization tool.
- Doesn't invent patterns from scratch — it is limited to the 159-pattern
  library. If a context calls for a pattern that isn't in the library,
  name the gap explicitly rather than inventing a new pattern in the
  library's name.

## Continue from here

- Next skill in the same pack:
  `../bmc-canvas-clarity-and-iteration/SKILL.md` — turning the selected
  patterns into a concrete canvas variant, and the variation logic.
- Related skill in the same pack:
  `../bmc-tool-switching-decisions/SKILL.md` — when to move from the BMC
  to a more precise tool to validate a pattern.
- Related skill in another pack:
  `../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
- Related skills in the same pack: `../bmc-tech-level-repositioning/SKILL.md`
  (a repositioning direction not currently in the pattern library, run
  alongside pattern selection) and `../bmc-revenue-quality-scoring/SKILL.md`
  (uses the `financial.rev.*` patterns here for revenue-stream conversion
  ideas).
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-innovation-pattern-library.md` — the full
  159-pattern library, four groups, 13 sub-models
- `../../references/bmc-source-material-notes.md` — source material background
- `../../CLAUDE.md` — this pack's shared guardrails
