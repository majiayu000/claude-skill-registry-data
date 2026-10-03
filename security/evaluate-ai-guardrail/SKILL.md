---
name: evaluate-ai-guardrail
description: Evaluate AI security guardrails, moderation layers, prompt-injection detectors, policy engines, classifiers, and rule-based controls with reproducible adversarial and benign datasets. Use when measuring false negatives and false positives, comparing versions or thresholds, diagnosing bypasses and overblocking, validating multilingual or domain slices, setting release gates, or building a regression suite.
---

# Evaluate an AI Guardrail

Measure both attack detection and benign utility under deployment-like conditions. Preserve raw predictions and dataset provenance so every aggregate can be audited.

Read [methodology](references/methodology.md) before selecting metrics, thresholds, slices, or release criteria.

## Safety boundaries

- Define the allowed content classes, handling rules, reviewers, storage, and retention before loading adversarial data.
- Minimize exposure to harmful content and warn human reviewers about relevant categories.
- Remove or replace personal data, credentials, live exploit targets, and operational secrets.
- Run generated or mutating tests in an isolated environment with tools and network side effects disabled.
- Do not publish raw bypasses, sensitive examples, or uniquely identifying records without a disclosure decision.
- Do not train on, tune against, or manually alter the held-out release set.

## Workflow

1. **Define the control decision.** Record protected policy, deployment point, action on detection, risk tolerance, error costs, users, languages, domains, latency and cost limits, and release decision.
2. **Fingerprint the guardrail.** Pin code or service version, model and snapshot, prompt, rules, thresholds, preprocessing, decoding, dependencies, environment, and evaluation date.
3. **Specify labels and taxonomy.** Write operational label definitions, ambiguous and abstain handling, multi-label rules, severity, attack family, benign intent, language, domain, and reviewer guidance before scoring.
4. **Audit the dataset.** Record source, license or authorization, provenance, collection date, transformations, hashes, class and slice counts, deduplication, near-duplicate groups, label review, leakage checks, and split method.
5. **Build paired coverage.** Pair adversarial cases with benign lookalikes that share vocabulary, format, domain, or user goal. Include clean, obfuscated, indirect, multilingual, long-context, and composition cases only when deployment can receive them.
6. **Run reproducibly.** Preserve one record per case with input ID, ground truth, raw output, normalized decision, score, threshold, latency, token or cost use, error, seed or trial, and guardrail fingerprint.
7. **Measure by slice.** Report confusion counts first, then recall or detection rate, false-negative rate, specificity, false-positive rate, precision, F1 when useful, abstention, coverage, latency, and uncertainty. Avoid unsupported percentages for tiny slices.
8. **Inspect errors.** Review representative false negatives, false positives, abstentions, unstable trials, and system errors. Identify mechanism-level clusters without leaking the held-out set into tuning.
9. **Choose and verify.** Compare thresholds or versions against declared error costs and release gates. Confirm selected changes on untouched data and convert failures into a separate regression suite.

## Evidence rules

- Hash the dataset, split manifest, evaluator code, configuration, and raw result file.
- Preserve immutable case IDs and provenance without storing unnecessary sensitive text in the report.
- Keep raw scores and outputs; do not retain only aggregate percentages.
- Record every error, timeout, refusal, and missing prediction.
- Separate development, threshold-selection, held-out release, and regression sets.
- Report sample counts and confusion counts for every metric and slice.
- Distinguish measured results, statistical uncertainty, interpretation, and release recommendation.

## Output contract

Return:

1. Scope, policy, deployment action, error costs, release gates, and limitations.
2. Guardrail and environment fingerprint.
3. Dataset card with provenance, license or authorization, schema, label rules, split, deduplication, leakage review, and slice counts.
4. Reproducibility manifest and raw-result location or hash.
5. Overall and per-slice confusion matrices, metrics, uncertainty, latency, cost, and system errors.
6. Audited false-negative, false-positive, abstention, and instability clusters with redacted examples.
7. Threshold or version recommendation tied to risk tolerance and benign utility.
8. Release decision, residual risk, monitoring plan, and regression suite.

Write each error cluster as: `ID | error type | attack or benign family | slice | count | representative evidence | likely mechanism | impact | confidence | proposed change | validation set | regression IDs`.

## Quality gate

Do not finalize until:

- Dataset provenance, authorization or license, hashes, labels, split, deduplication, and leakage checks are documented.
- Held-out release data remains untouched by prompt, rule, model, or threshold tuning.
- Every percentage includes a denominator and every slice includes raw confusion counts.
- Attack recall and benign false-positive impact are both reported.
- Small or unstable slices are labeled inconclusive instead of overstated.
- All failed requests and missing outputs are accounted for.
- The release decision follows predeclared gates and states residual risk.
- No benchmark result is presented as proof that the protected application is secure.
