---
name: prioritize-risks
description: This skill should be used when the user wants to figure out which part of their business model to test first — "what's the riskiest part of my plan?", "where should I start?", "prioritize my assumptions", "which of these business models should I pursue?", "how do I de-risk this?", or "rank my lean canvases". It identifies the assumptions on the Lean Canvas, classifies them as product/customer/market risk, ranks them, and picks the riskiest-first starting point, writing .lean/risks.md. Use it after a canvas exists and before running experiments or interviews. For documenting the model itself, use lean-canvas; for testing an assumption, use customer-interview or run-experiment.
version: 0.1.0
---

# Prioritize risks — where to start

Incorrect prioritization of risk is one of the biggest sources of wasted effort. This skill turns a canvas full of assumptions into a ranked list and a clear "test this first." You work as the **Strategist** guide role (`../../reference/roles.md`); the **Devil's advocate** role is a natural partner for pressure-testing whether the top risk is really the top risk (offer it). Read `references/risk-scoring.md` before ranking.

## When to use

A canvas exists (or several variants do) and the user needs to decide where to start, or which model to pursue. This sits between `lean-canvas` (document) and the testing skills (`customer-interview`, `run-experiment`). If there's no canvas yet, route to `lean-canvas` first.

## Core stance

- **Risk ≠ uncertainty.** Uncertainty is many possibilities; risk is uncertainty where some outcomes mean a real loss. Rank by risk: probability × cost-of-being-wrong, judged roughly — you do not need a statistical model, just an honest relative ordering.
- **Riskiest first, not easiest first.** The trap is making marginal progress on safe assumptions and getting stuck later on the one that mattered. Name the scary one and put it on top.
- **For most products the solution isn't the riskiest part.** Unless you're solving a genuinely hard technical problem, you can probably build it. The bigger risk is building something nobody wants — a market/customer risk.

## Procedure

1. **Load the canvas.** Read `.lean/canvas.md` (and `.lean/PROGRESS.md`). If multiple canvas variants exist, you'll rank the models too (step 5).
2. **Extract the assumptions.** Walk the canvas and list each load-bearing assumption as a falsifiable-ish claim ("parents find sharing media a must-have problem", "we can reach them via daycares", "they'll pay $X/yr"). Mark which are already supported by evidence vs. pure guesses.
3. **Classify each by risk type** (see `references/risk-scoring.md`):
   - **Product risk** — getting the product right.
   - **Customer risk** — building a path to customers.
   - **Market risk** — building a viable business.
4. **Rank.** Order assumptions by risk (impact if wrong × how unproven). State, for the top few, *why* they rank where they do. The riskiest *untested* assumption is your starting point.
5. **If ranking models (multiple canvases),** use the weighting order from `references/risk-scoring.md`: customer pain → ease of reach → price/margin → market size → technical feasibility. Recommend which model to start with and why; note which to shelve.
6. **Get ready to test.** For the top risk, name the cheapest experiment that would attack it (usually problem interviews early on) and the team/setup it needs. Optionally, recommend a quick round of advisor / business-model interviews to calibrate the ranking before committing — ask an advisor "what's the riskiest part of this plan? have you overcome similar risks? how would you test them?" (mind the advisor paradox: advice informs, it doesn't decide — you own the model).
7. **Write `.lean/risks.md`** from `assets/risks-template.md`: the ranked list with type, rationale, and current status (open / testing / retired). Mirror the top 1–3 into `.lean/PROGRESS.md`. Add a dated revision note.
8. **Hand off** to the skill that tests the top risk — `customer-interview` (problem/solution/mvp) for market/customer risk, `run-experiment` for a build-or-channel test.

## Output

`.lean/risks.md` — assumptions classified (product/customer/market), ranked riskiest-first, each with a one-line rationale and a status. A clear "test this first" with the smallest experiment to attack it. If models were compared, a recommended starting model.

## Related

- `lean-canvas` — produces the assumptions you rank here.
- `customer-interview`, `run-experiment` — test the top-ranked risk.
- `lean-roles` — Devil's advocate to pressure-test the ranking; Mentor for a second opinion.
- `references/risk-scoring.md` — risk types and the model-ranking weighting order.
