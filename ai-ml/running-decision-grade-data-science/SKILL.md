---
name: running-decision-grade-data-science
description: Orchestrate an end-to-end data analysis or machine learning project from decision framing through reproducible handoff. Use when a request spans multiple lifecycle stages or an ambiguous modeling request must become a decision-ready result; use narrower audit or experiment-design skills for isolated reviews.
---

# Run Decision-Grade Data Science

Produce work that another person can inspect, challenge, rerun, and use for a real decision. Treat a model score as evidence, not as the deliverable.

## Establish the decision contract

Before choosing methods, make the following explicit:

- decision or action the work will inform;
- entity and row grain;
- target or claim, including the positive condition;
- observation, prediction, and outcome windows;
- population, exclusions, and deployment context;
- success measures, business costs, and minimum useful improvement;
- constraints on data, latency, interpretability, fairness, or operations.

Infer reversible details when evidence supports them. Ask for a decision only when alternatives would materially change the target, evaluation, permitted data, or external impact. Record assumptions rather than repeatedly pausing for routine choices.

For a full gate-by-gate procedure and stopping conditions, read [references/project-gates.md](references/project-gates.md).

## Run the lifecycle

1. **Inventory evidence.** Identify source files, tables, queries, documentation, prior outputs, and ownership. Preserve raw inputs unchanged and create derived artifacts separately with lineage back to the source.
2. **Audit meaning before computation.** Verify schema, units, grain, keys, time semantics, joins, missingness, duplicates, and ground-truth provenance. When installed, use the `auditing-data-and-ground-truth` skill for a dedicated investigation; otherwise perform the checks directly and keep their evidence in this project's record.
3. **Lock evaluation before tuning.** Define deployment-matched splits, metrics, comparison rules, and test-set isolation. When installed, use the `designing-leakage-safe-experiments` skill for nontrivial feature availability, group dependence, or temporal leakage; otherwise document the same boundaries in the evaluation protocol.
4. **Establish a simple baseline.** Start with a transparent heuristic or simple model. Add complexity one change at a time and keep it only when the prespecified evaluation shows a meaningful gain.
5. **Interrogate failures.** Inspect errors by relevant time, source, entity, class, and operating slice. Distinguish data defects, label defects, extraction defects, modeling limits, and evaluation mismatch. Keep negative and failed experiments in the record. For a reproducible regression, use the `diagnosing-ml-failures` skill when installed; otherwise isolate the first divergent layer and retain a competing-hypothesis log before proposing a fix.
6. **Translate evidence into a decision.** Report what is supported, what remains uncertain, where the result is unsafe to generalize, and the recommended action or next test. Before a consequential claim, use the `validating-models-and-claims` skill when installed; otherwise map each falsifiable claim to independent, scope-matched evidence and narrow unsupported wording.
7. **Handoff reproducibly.** Provide exact inputs or snapshots, environment and parameters, runnable commands, artifact locations, and a compact result ledger. Use the `shipping-reproducible-results` skill when installed; otherwise attempt a clean independent run and label the result as reproduced, ready for independent reproduction, replayable with constraints, or archival evidence only. Never imply that an unexecuted path was reproduced.

## Control material choices

Continue autonomously through ordinary, reversible analysis. Obtain approval before changing the target or source of truth, discarding or overwriting original data, adopting a consequential metric tradeoff not already authorized, incurring material cost, or publishing/deploying externally.

Never treat approval as proof. Keep the evidence, rationale, owner, and downstream effect of each material choice.

## Deliver the record

Copy [assets/decision-grade-project-record.md](assets/decision-grade-project-record.md) into the project and adapt it. Keep claims linked to evidence, not merely to code or charts. Clearly label each final claim as supported, conditional, contradicted, or not tested, and track reproduction status separately.
