---
name: startup-evaluation
description: Use when a startup needs an evidence-weighted health check, investor lens, runway diagnosis, top constraint, or cheapest next validation test.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "one-shot"
  assumes: "The company stage, business type, and at least partial customer or operating evidence can be obtained."
  conflicts_with: "Treating pitch quality, market size, or founder conviction as proof of demand or investment merit."
---

# Startup Evaluation

<skill_contract>
  <input>Company, stage, evaluation decision, customer evidence, traction, economics, team, runway, terms, and risks.</input>
  <output>An evidence-weighted health, venture-suitability, and financing assessment with one top constraint and cheapest test.</output>
  <done>Every score and verdict traces to evidence, fatal risks remain visible, and the next test has owner, threshold, budget, and stop.</done>
  <non_goals>Investment advice by narrative, averaging away fatal risk, or treating market size, conviction, or pitch quality as demand.</non_goals>

Evaluate the company the evidence supports, not the story it tells. Distinguish business health, venture suitability, and financing readiness; they are different decisions.

## Usage Template

Provide: company, stage, startup type, evaluation decision, customer, problem, product, traction, team, economics, runway, round terms, and known risks. Use the rubric in `references/evaluation-rubric.md` when scoring is requested.

## Workflow

<intake>

Classify stage, type (`SME`, innovation-driven, venture-scale, hard-tech, AI-native), lens (founder, diligence, fundraising, pivot), and evidence state. Define the decision and time horizon before calculating a score.

</intake>

<unknowns_gate>

Separate facts, assumptions, self-reported claims, and missing evidence. If the target decision or company identity is unclear, return `NEEDS_INPUT`. Continue with missing metrics only when the output is explicitly provisional and each gap has a probe.

</unknowns_gate>

<execute>

1. Rank demand evidence from belief and interviews through behavior, payment, retention, expansion, and referral.
2. Score eight dimensions using stage-adjusted weights: pain/beachhead, market/timing, value step-change, PMF/traction, business model/economics, team/governance, capital/runway, and moat/risk.
3. For investor work, cross-check 5T: Team, Target Market, Tech/Product, Traction, Terms.
4. For AI-native or hard-tech cases, test what remains defensible as components cheapen and identify physical, regulatory, deployment, or supply-chain bottlenecks. For AI value capture, separate **usage**, **productivity**, **customer ROI**, and **vendor profit**; do not infer durable economics from token volume or revenue growth alone.
5. Separate the spending engine (CapEx, inference, integration, service labor,
   energy, and deployment cost) from the earning engine (retention, expansion,
   pricing power, gross margin, and free cash flow). Test who owns institutional
   learning: workflow exceptions, context, permissions, and feedback write-back.
6. Diagnose runway and whether spend buys evidence for the next milestone.
7. Name the single constraint most likely to invalidate or unlock the company.
8. Specify the cheapest test, threshold, owner, budget, and stop condition.

Do not average away fatal risk. A healthy cash-flow business may still be a poor venture investment; a large market cannot rescue absent demand evidence.

</execute>

<evaluate>

Trace every score and verdict to the evidence ledger. Stress-test the conclusion against churn, paid acquisition dependence, founder conflict, financing timing, platform dependency, falling model prices, rising inference/service cost, and customer ROI that fails to become vendor margin. Calibrate confidence to the weakest decision-critical claim.

</evaluate>

## Failure Protocol

- `NEEDS_INPUT`: the evaluation decision, stage, or company boundary is unclear.
- `INSUFFICIENT_EVIDENCE`: the requested verdict depends on unavailable demand, retention, economics, or terms data.
- `VERIFY_FAILED`: a score lacks evidence or contradicts the ledger; rescore or mark unknown.
- `BUDGET_STOP`: return the provisional constraint and highest-value evidence request.

## Output Contract

Return `status`, `result` (verdict, scorecard, top constraint, fatal risks, and next test), `evidence` (fact/assumption ledger), `unknowns`, and `next_action` with owner and threshold.

## Edge Cases

- Pre-revenue company has no retention data: do not assign traction maturity; score the available behavioral test and make payment/usage the next gate.
- Bootstrapped company has strong cash flow but a small market: rate business health separately from venture-scale suitability.
- AI usage grows while gross margin and customer retention fall: record adoption
  without calling it value capture; test pricing, service labor, and inference
  economics separately.

## Success Metrics

- Stage, type, decision lens, and evidence maturity are explicit.
- Verdict confidence follows observed behavior rather than narrative polish.
- AI-native verdicts distinguish adoption, customer value, and supplier profit.
- One top constraint and one cheap falsifiable test govern the recommendation.

## Quality Gates

- [ ] Facts, assumptions, self-reports, and missing evidence are separated.
- [ ] Score weights fit stage and business type.
- [ ] Fatal risks are not hidden by averages.
- [ ] AI cases separate spending, usage, productivity, customer ROI, and vendor profit.
- [ ] Runway, milestone, test threshold, owner, and stop condition are explicit.

</skill_contract>
