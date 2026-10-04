---
name: validating-models-and-claims
description: Validate trained models and analytical claims against their intended decision, independent evidence, and human-reviewed ground truth. Use when reviewing model performance, analysis conclusions, launch claims, or evaluation reports; use failure diagnosis instead when the main task is locating a known defect.
---

# Validating Models and Claims

Decide what the available evidence actually supports. Treat a metric, chart, or successful run as evidence for a bounded claim, not as proof that the full system works.

## Start with the claim

Write each material claim in a falsifiable form before selecting evidence:

- the decision or action the claim will influence;
- the population, unit of analysis, prediction horizon, and operating conditions;
- the comparator and practical improvement threshold;
- the cost of false positives, false negatives, abstention, and delay;
- the evidence that would refute or narrow the claim.

If these are unresolved and materially change the evaluation, surface the choice instead of silently selecting a convenient definition.

## Build an evidence contract

For every claim, map the claim's scope to evidence of equal scope. A component test cannot establish end-to-end readiness; aggregate accuracy cannot establish subgroup safety; retrospective fit cannot establish future performance.

Separate at least these evidence sources when they exist:

1. development evidence used to choose features, thresholds, or models;
2. untouched or independently collected validation evidence;
3. human-reviewed ground truth and its adjudication record;
4. operational evidence produced under the real inference path.

Do not describe reused tuning data as independent validation. Record every contact with the evaluation set, including manual error review that influenced a subsequent model choice.

When label correctness depends on expertise or judgment, preserve the human ground-truth process: reviewer qualifications, instructions, blinding, disagreement rate, adjudication, unresolved cases, and sampling frame. Model agreement with noisy labels is not accuracy against reality.

## Validate in layers

Use the smallest set of checks that covers the actual claim:

- **Semantic validity:** target, timestamps, joins, exclusions, and units mean what the claim assumes.
- **Evaluation integrity:** split boundaries, leakage controls, comparator, threshold selection, and metric implementation are valid.
- **Performance:** report uncertainty and practical effect size, not only a point estimate.
- **Slices and errors:** inspect decision-relevant subgroups, rare cases, temporal drift, missingness patterns, and high-cost errors.
- **Operational fidelity:** when the claim includes deployment or operational behavior, exercise the same preprocessing, feature availability, threshold, and output interpretation used in practice. Otherwise record why this layer is not applicable.
- **Claim calibration:** narrow the final language to what all completed evidence supports.

Predefine acceptance criteria when possible. If criteria are chosen after observing results, label them exploratory.

## Preserve independence

Prefer a validator who did not construct the evaluated artifact. When that is not possible, create procedural independence: freeze the artifact and protocol, record hashes and versions, run the validation from a clean entry point, and keep exceptions visible.

Never overwrite failed or contradictory results. Explain discrepancies or carry them into the decision as unresolved risk.

## Produce a decision record

Use [assets/validation-report.md](assets/validation-report.md) for a reviewable deliverable. Include:

- a claim-to-evidence matrix with status `supported`, `partially supported`, `unsupported`, or `not tested`;
- the provenance and independence of each evidence source;
- uncertainty, slice results, and representative error cases;
- human ground-truth quality and unresolved disagreements;
- limitations, rejected interpretations, and the exact supported wording;
- a decision recommendation with explicit conditions and owner.

For detailed protocol design, human-label review, and scope-matched proof rules, read [references/validation-protocol.md](references/validation-protocol.md).

## Stop conditions

Do not declare validation complete while a material claim lacks scope-matched evidence, evaluation independence is unknown, the ground truth is unreviewed where it matters, or a claimed operational path has not been exercised. Report missing proof or a justified not-applicable layer rather than converting absence of evidence into a pass.
