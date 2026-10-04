---
name: coval-calibrate-metric
description: Validate one Coval judge against independent human labels, with grouped development/test separation, class-specific errors and uncertainty. Use for trust claims or calibration; without real labels, prepare review rather than inventing ground truth.
compatibility: Coval CLI or public API; Python 3.10+ for the bundled offline binary calibration calculator.
---

# Calibrate a Coval metric

Measure whether a specific metric version matches a domain expert on its intended
population. Successful metric execution and agreement on prompt-tuning examples
are not independent validation.

## Establish the evidence contract

Confirm organization/workspace, one metric ID, rubric, output type/polarity and
decision. Read the definition and output version IDs. Inspect an existing review
project and completed annotations, or a human-provided labeled export:

```bash
coval --agent metrics get <metric-id>
coval --agent review-projects get <project-id>
coval --agent review-annotations list --filter 'project_id="<project-id>" AND metric_id="<metric-id>" AND completion_status="COMPLETED"' --page-size 100
```

Check success and paginate using the public reviews API when the CLI cannot
prove completeness. Preserve annotation IDs, output/conversation IDs, reviewer,
completion status, label values and rubric provenance. Zero is a valid label;
null is missing. Record whether each source is a simulated or uploaded conversation:
`simulation_output_id` in an annotation can refer to either. Retrieve its original
metrics from the matching `simulated-conversations` or `uploaded-conversations`
CLI collection/public API, not from a guessed collection. Don't silently treat pending, deferred or AI-generated labels
as completed human ground truth.

If human labels are absent, produce a review-ready sample and criteria using
`coval-discover-failures`. Return **not yet calibrated**. Agent-generated labels,
synthetic expected answers and a reviewer-shaped email are not human validation.
Do not create assignments or notify reviewers without the required authorization.

## Separate development from evaluation

Assign related calls to a stable `group_id`: same original conversation,
near-duplicate scenario, caller/customer thread, or resimulations of a case.
Keep each group in only one split, including few-shot examples. Choose a split
appropriate to the available sample; do not force tiny datasets into meaningful-
sounding percentages. Record the IDs before tuning.

- **train**: examples allowed in the judge prompt.
- **dev**: inspect disagreements and refine the prompt.
- **test**: untouched until the candidate is frozen; measure once.

Have a domain expert resolve conflicting human labels against the rubric; do not
overwrite them to match the judge. Multiple reviewers on one conversation are
not independent examples. Low human agreement suggests an unclear criterion.
Keep original labels and adjudication provenance.

For development, propose a candidate metric separately from production defaults.
Fix one observed error pattern at a time. Keep the same frozen metric version
across the evaluated split. Re-scoring existing outputs through `metrics test`
is cheaper than resimulating; it still needs a bounded metric-evaluation budget.
Inspect per-item queue failures and poll each returned `metric_output_ulid`,
not a prior output. Capture version IDs and available runtime model metadata.
If the runtime model cannot be pinned or identified, report that limitation.

## Measure the right errors

For binary pass=1/fail=0:
- **Pass recall (TPR)** = correctly passed / human passes.
- **Failure detection (TNR)** = correctly failed / human failures.
- **False-pass rate** = judge passes / human failures. This often matters most
  for a release gate.

Report the confusion counts, each denominator and uncertainty. Overall agreement
can be useful alongside these, but cannot hide an always-pass judge. If a class
has no examples, its rate is **unknown**, not zero or perfect. Pick thresholds
with the customer based on consequences; there is no universal 90% certification.

The bundled offline calculator accepts a deliberately normalized, auditable
export described in [references/calibration-input.md](references/calibration-input.md):

```bash
python3 scripts/calibration.py --input calibration.json --split dev
python3 scripts/calibration.py --input frozen-test.json --split test
```

It checks grouping, duplicate conversations, label provenance and metric version,
excludes unusable results, and calculates Wilson 95% intervals. It cannot verify
that a file's claimed human labels were actually supplied by a human; inspect
the source records. Do not relabel AI findings to make the validator accept them.

For categorical metrics, retain categories and report a confusion matrix and
per-category error counts. For numerical metrics, predefine tolerance/decision
threshold and report absolute error plus boundary disagreements. The bundled
calculator is binary-only; don't coerce another metric type into it.

## Decide and stop

Inspect development disagreements, never the held-out test during tuning. After
examining final test outcomes, that set is no longer untouched for further
iterations. Use new held-out groups for a later trust claim. Include failed,
skipped and missing score counts so selected successes cannot inflate quality.

Return the metric/version, rubric, label source, split/group manifest, counts,
errors, uncertainty and intended population. Distinguish **development evidence**,
**held-out measurement**, and **insufficient evidence**. A small test can prove
the workflow works without proving the judge reliable.

Do not automatically turn a failure-enriched validation sample into a production
pass rate. Prevalence correction requires representative production sampling,
stable class-conditional error rates and uncertainty from both samples; those
assumptions often do not hold after agent or traffic changes. Report the directly
measured errors first. Revalidate after rubric, model, input or population changes.
