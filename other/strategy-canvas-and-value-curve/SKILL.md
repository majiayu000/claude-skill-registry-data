---
name: strategy-canvas-and-value-curve
description: "Structures competitors or alternative solutions on shared industry competitive factors, maps the industry's 'as-is curve,' and finds ways to break away from or differentiate against it — using the Blue Ocean Strategy model and the owner's 360 comparison tool."
---

# Strategy Canvas & Value Curve

## Purpose

Structures competitors or alternative solutions on the same "strategy map"
using shared industry competitive factors, makes the industry's "as-is
curve" visible — the set of conventional, assumed choices that most players
compete on using the same logic — and then systematically looks for ways to
**break, deviate from, or differentiate against** this as-is curve. This is
above all a way of thinking, not a finished analysis: the skill helps you
see your own and competitors' offerings side by side in a single picture,
and ask "why are we competing on exactly these factors, and what would
happen if we didn't?"

## Based on

- Kim, W. C. & Mauborgne, R. (2005), *Blue Ocean Strategy* — the **Strategy
  Canvas** and **Value Curve**: the x-axis lists the industry's competitive
  factors, the y-axis shows the level each player offers on each factor;
  the players' curves reveal the industry's shared "as-is curve" and any
  deviations from it. Complementary tools: the **Four Actions Framework /
  ERRC grid** (Eliminate–Reduce–Raise–Create) for designing a new value
  curve, and the **Six Paths Framework** for finding new dimensions of
  differentiation outside the industry's conventional boundaries.
- The owner's **360 Comparison
  Factors** comparison tool — a concrete, productized scoring template for
  building a value curve: a 0–2 scale (0 = weak/not offered,
  1 = industry mid-level, 2 = strong/distinctive) applied to 10 typical
  comparison factors, see `../../references/360-comparison-template.md`.

## Method

1. **Choose the players to compare.** Your own solution + 3–5 relevant
   competitors or alternative solutions. Also include the "do nothing" /
   status quo option if the customer could genuinely choose it — it often
   reveals the truest as-is curve.
2. **List the industry's competitive factors.** Not just the obvious
   product features, but every dimension on which the customer actually
   compares alternatives: e.g. price, quality, user experience, design,
   variety, setup time, self-service level, integrations/API, delivery
   time, number of features (the 360 model's 10 example factors, see
   `../../references/360-comparison-template.md`). These are a starting
   point, not a fixed list — drop what's irrelevant and add your own
   industry's own factors.
3. **Score every player on every factor.** Use a consistent scale (0–2 in
   the 360 model: 0 = weak/not offered, 1 = industry mid-level/standard,
   2 = strong/clearly distinctive). Score honestly — including your own
   solution — and mark clearly which scores are based on information the
   user provided and which are `[assumption — verify]`. Don't invent
   competitor data from memory.
4. **Draw the strategy map.** The x-axis lists the competitive factors (in
   the order from step 2), the y-axis shows the score. Connect each
   player's scores across the factors into its own curve — the result is a
   visual strategy map showing all players side by side.
5. **Identify the as-is curve.** Points where most players' curves run in
   the same direction at the same level are the industry's assumed,
   taken-for-granted competitive factors and their conventional level —
   this is the starting point of Blue Ocean thinking: industries often
   compete on the same dimensions with the same logic, without anyone
   questioning it.
6. **Apply the ERRC grid to every factor:**
   - **Eliminate:** which of the industry's taken-for-granted factors can
     be eliminated entirely, because they no longer create real value for
     the customer?
   - **Reduce:** which factors can be offered clearly below the industry
     standard without meaningfully hurting customer value?
   - **Raise:** which factors can be raised clearly above the industry
     standard?
   - **Create:** what entirely new factors — that no one in the industry
     yet offers — could be added to the comparison?
7. **Look for new dimensions of differentiation outside the industry**
   (Six Paths inspiration): alternative industries (what the customer would
   use instead), strategic groups within the industry, different roles in
   the buyer chain (who decides, who pays, who uses), complementary
   product/service offerings, functional vs. emotional appeal, and the
   direction of time (where trends are taking the industry).
8. **Draw the intended new value curve** based on the ERRC decisions and
   compare it to the as-is curve. Test it against Blue Ocean thinking's
   three quality criteria: is the new curve **focused** (not trying to be
   best at everything), **divergent** (clearly different in shape from the
   as-is curve), and does it have a **compelling tagline** (crystallizes
   into one understandable sentence)?
9. **Test feasibility.** Is the new curve genuinely achievable with current
   or acquirable resources, does it produce value innovation (more value in
   some respects, at lower cost in others), and is it differentiated enough
   from competitors' curves to be defensible over time?

## Available scripts

- **`scripts/value_curve.py`** -- once every player is scored on every
  factor (Method step 3), renders the strategy map as an SVG line chart
  (step 4) and computes a factor-by-factor spread analysis that surfaces
  the as-is curve automatically (step 5): factors where players cluster
  within 1 point of each other are flagged as `as_is_curve_candidates`,
  sorted first -- these are the highest-leverage places to run the ERRC
  grid (step 6). Missing scores are reported as errors, not silently
  defaulted, matching this skill's "don't invent competitor data" rule.

  ```bash
  python3 scripts/value_curve.py --example > input.json         # see the input shape
  python3 scripts/value_curve.py input.json --output curve.svg
  ```

  Stdlib only (json, argparse) -- no install needed, no external charting
  library required.

## Gotchas

- Keep the scale consistent across every player. The 360 model's 0-2 scale
  (0 = weak/not offered, 1 = industry mid-level, 2 = strong/distinctive) is
  what `scripts/value_curve.py` assumes by default -- mixing in a 1-5 scale
  for some players, or forgetting to pass a different `scale_max`, produces
  a chart and an as-is-curve analysis that both look precise but compare
  incompatible numbers.
- The "do nothing" / status quo option (Method step 1) is the easiest
  player to skip because it doesn't feel like a real competitor -- but when
  the customer's actual alternative is inaction, leaving it out hides the
  truest as-is curve, not just one extra data point.
- A factor where every player scores 2 (all strong) is still an as-is-curve
  factor -- industry table stakes, not a differentiator -- even though the
  raw numbers look good. As-is-curve detection (step 5, and the script's
  `as_is_curve_candidate` flag) is about low SPREAD across players, not
  about low absolute scores.
- The 360 model's 10 example factors are an explicit starting point, not a
  checklist to fill in mechanically (see "What this skill does NOT do") --
  a canvas that just plugs in the generic factors without dropping the
  irrelevant ones and adding the industry's own looks rigorous but rarely
  surfaces anything the team didn't already know.
- A redesigned value curve has to pass all three Blue Ocean quality tests
  together (focused, divergent, a compelling one-sentence tagline) -- a
  curve built by raising several factors and eliminating none usually fails
  "focused" even when each individual ERRC decision seemed reasonable on
  its own.

## What this skill does NOT do

- Doesn't score competitors for you without user-provided information or a
  clearly marked assumption — competitor data is never generated from
  memory.
- Doesn't guarantee that a new value curve will succeed in the market — the
  tool structures thinking and makes the alternatives visible; the market
  validates the outcome.
- Doesn't replace in-depth structural competitive analysis — see
  `../../../opportunity-recognition/skills/competitive-and-five-forces-mapping/SKILL.md`
  for Porter's Five Forces analysis. The strategy canvas is a complementary,
  visual, differentiation-focused tool, not a substitute for industry or
  financial analysis.
- Doesn't limit comparison factors to the 360 model's 10 examples — they're
  a starting point that should always be customized to the industry.

## Continue from here

- Preceding skills in the same pack: `../layer-based-business-structuring/SKILL.md`,
  `../value-chain-mapping/SKILL.md`, `../category-definition-and-modeling/SKILL.md`
  — once a new value curve has been sketched, these can structure *how* it
  gets implemented (layers, value chain) and *how* it gets positioned
  (category decision).
- Related skill in another pack: `../../../opportunity-recognition/skills/competitive-and-five-forces-mapping/SKILL.md`
  — a structural complement to this visual differentiation tool.
- Related skill in another pack: `../../../opportunity-recognition/skills/opportunity-value-assessment/SKILL.md`
  — the differentiation produced by a new value curve as an input to
  opportunity assessment.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/360-comparison-template.md` — the 360 Comparison
  Factors template (10 example factors, 0–2 scale, usage instructions)
- `../../CLAUDE.md` — the pack's shared guardrails
