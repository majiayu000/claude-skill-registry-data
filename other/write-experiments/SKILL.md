---
name: write-experiments
description: Use when drafting, revising, or auditing engineering-paper Experimental Studies, Results, Performance Evaluation, ablation, convergence, sensitivity, robustness, or numerical-analysis sections, especially when evaluation fairness, reproducibility, evidence-to-claim logic, statistical support, training credibility, or paragraph organization is weak.
---

# Write Experiments

## Purpose

Design and write an experimental section as a chain of questions, controlled comparisons, observations, explanations, and bounded conclusions. Every paper claim must map to sufficient evidence, and every figure or table must have a distinct evidentiary role.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. Always read [the reader and terminology contract](references/core/reader-and-terminology-contract.md).
3. Read [the house-style card](references/styles/house-style-card.md) unless the user names another venue or team style. It governs author voice, sentence rhythm, connectives, section and subsection titles, paragraph openers, captions, and equation lead-ins, and it overrides the generic example sentences of this skill where they differ. When drafting or revising, also read Sections 8, 9, and 13 (titles, experiment openers, captions and table forms) of [the full team house style](references/styles/team-house-style.md); read its other sections only when the card's last table names them.
4. Read [the Chinese manuscript adapter](references/languages/zh.md) when the manuscript is written in Chinese.
5. For population-based, Pareto, constrained, or dynamic evolutionary optimization, read [the evolutionary-algorithm route](references/methods/evolutionary-algorithms.md).
6. For value-based, policy-gradient, actor-critic, single-agent, or multi-agent learning, read [the reinforcement-learning route](references/methods/reinforcement-learning.md).
7. Read [the MEC domain pack](references/domains/mec.md) only for MEC or directly adjacent edge-computing systems. It also holds the order-of-magnitude scale table.
8. When several routes apply, read all relevant references and audit each evidence channel separately.
9. Run [the fingerprint script](scripts/style_fingerprint.py) on the draft before delivery when Python is available, with the ranges of the scale statement as `--scale` and the term ledger as `--terms`. `--spine --section exp` prints the paragraph-opening sentences for the center-sentence audit.

## Workflow

### 0. Choose the mode

- Results mode: result artifacts exist; follow Steps 1-7.
- Design mode: no results exist. Write the protocol, not the outcome.
  - Keep the claim-to-experiment ledger with a leading `Hypothesis id` column. Give each claim an id, a falsifying outcome, and the maximum conclusion it could support.
  - Fix the analysis plan before any run: statistical unit, aggregation hierarchy, test and pairing key, the criterion for "stable", and its tolerance.
  - Use protocol wording ("is compared with", "is measured by"). Result verbs and numbers not taken from the configuration are forbidden (shows, outperforms, achieves, demonstrates, validates, is robust).
  - Leave result slots out of the prose and list them as pending in the ledger.
  - Title the section "Experimental Design" or equivalent, not "Results".

### 1. Build the claim-to-experiment ledger

| Paper claim | Experiment question | Controlled comparison | Metric and direction | Artifact | Required evidence | Status |
|---|---|---|---|---|---|---|

Include effectiveness, component contribution, efficiency, scalability, convergence, feasibility, robustness, generalization, and deployment claims. Record the aggregation hierarchy and pairing key for every statistical claim. Remove or bound claims without an adequate experiment.

### 2. Establish the evaluation contract

State environment or dataset, instances and splits, baselines, implementation and hardware, budgets, hyperparameter-selection rules, random seeds, independent runs, uncertainty summaries, statistical tests, stopping criteria, and failure handling. Compare methods under equivalent information, data, compute, or evaluation budgets relevant to the claim.

### 3. Assign each artifact one primary role

Use tables for exact comparisons, figures for trends or distributions, ablations for component causality, sensitivity studies for parameter dependence, and case studies for operating behavior. Avoid duplicating the same evidence across several artifacts without a distinct question.

### 4. Draft by experiment question

Use two linked blocks:

`question -> rationale -> controlled variables -> metrics -> artifact pointer`

`overall answer -> discriminating values or statistics -> trend and exception -> supported mechanism explanation -> bounded conclusion`

Open with the experiment purpose or empirical answer, not “Figure X shows.” Do not narrate every plotted point or repeat the caption.

### 5. Reconcile quantitative claims

For every retained number, record the artifact, panel or row, metric direction, aggregation, denominator, comparison baseline, and run-selection rule. Recompute relative changes. Distinguish percentage change from percentage-point change and mean from best, median, representative, or individual runs.

Use “significant,” “stable,” “robust,” “generalizes,” and causal verbs only when the stated analysis supports those meanings.

Name the run selection in the result sentence when an artifact reports selected runs. When one component of a cost or benefit improves, report the net effect or name the offsetting component. Do not narrate an unmeasured intermediate step as a result, do not write a nonsignificant comparison as support for the proposed design, and call values computed under idealized assumptions reference values, not bounds.

### 6. Apply method-family and domain checks

Evolutionary studies must reconcile evaluation budgets, population and generation settings, independent runs, feasibility failures, reference fronts or points, Pareto metrics, convergence, and statistical comparisons.

Learning studies must separate training, validation, and test roles; reward from physical metrics; hyperparameter and checkpoint selection; seeds and uncertainty; generalization; robustness; and offline training cost from online execution cost.

The domain pack may add physical metrics, scenario controls, feasibility events, and interpretation boundaries. It does not replace the generic fairness and claim gates.

### 7. Run the final audit

Apply the core evidence, fairness, reproducibility, statistics, paragraph, and claim gates, then all selected method and domain gates. Verify that every claim maps to evidence, every artifact has a purpose, all exact values match, exceptions are reported, explanations do not exceed experimental isolation, and conclusions name the tested range.

## Reader gates (check before delivering)

1. Every coined term is defined by function at first use (T); no variable-like names for decisions or objectives.
2. Every definite expression has an antecedent (A); every action has a purpose or a cost (Q).
3. Each proposition has one home (D); each universal or negative claim is tagged and supported (C).
4. Length is inside the declared scale range, or the deviation is recorded (S).
5. Sentence rhythm and connectives are inside the house-style band, or each remaining flag and its reason are listed in the delivery note, not in the manuscript (R).
6. Ledgers and notes stay out of the manuscript (H).

## Output constraints

- Match notation, terminology, tense, labels, and venue style.
- Preserve correct data and configuration; do not manufacture missing results.
- Keep ledgers, term tables, and audit notes out of the manuscript text and appendices unless the user asks for them.
- When drafting, return the complete requested unit or section.
- When auditing, report evidence failures by claim and severity before proposing a replacement experiment map.
- Do not alter the method, system model, bibliography, figures, tables, raw data, or manuscript files outside the authorized scope.

