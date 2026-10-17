---
name: model-card
description: >
  Document a machine learning model in a structured, transparent format for stakeholders, reviewers,
  and future maintainers. Use when the user says "document this model", "write a model card",
  "model documentation", "how should I document my ML model", "bias and fairness report",
  "model transparency", "what does this model do", "model handoff", "production model documentation",
  or needs to communicate what a model does, how it was built, where it works, and where it fails.
---

## Overview

Based on **"Interpretable Machine Learning"** by Christoph Molnar, with structure informed by the Google Model Cards framework (Mitchell et al., 2019). The core principle: a model without documentation is a liability. Interpretability is not a post-hoc courtesy - it is a prerequisite for responsible deployment. A model card makes the model's intended use, performance limits, and failure modes explicit before the model reaches production.

## Workflow

### Step 1: Write the model overview section

```markdown
## Model Overview

**Model name:** [descriptive name, not a variable name]
**Version:** [semantic version, e.g., v1.2.0]
**Model type:** [e.g., XGBoost binary classifier, LSTM time-series forecaster]
**Owner:** [team or individual responsible for this model]
**Last updated:** [date]

**What does this model do?**
[One paragraph. Plain language. No jargon. What input does it take? What output does it produce?
What decision does it support?]

**Primary use case:**
[Specific intended application. Be concrete: "Predicts 30-day churn probability for active
subscribers with > 60 days of account history."]

**Out-of-scope uses:**
[List uses this model was NOT designed for and should not be used for.]
```

### Step 2: Document training data and known limitations

```markdown
## Training Data

**Data source:** [database, pipeline, or dataset name]
**Time range:** [e.g., Jan 2022 - Dec 2023]
**Size:** [rows and columns in the training set]
**Target variable:** [column name and class distribution, e.g., "churned: 8.3% positive"]
**Train / validation / test split:** [e.g., 70/15/15, stratified by target]

**Known data limitations:**
- [e.g., "Users from regions X and Y are underrepresented (< 2% of training data combined)"]
- [e.g., "Labels were collected through a manual review process with 15% inter-annotator disagreement"]
- [e.g., "Training data reflects behavior during a promotional period - may not generalize to steady-state"]
```

### Step 3: Document model performance metrics

Report performance on the held-out test set. Always report more than accuracy.

```markdown
## Performance

**Evaluation dataset:** [held-out test set description]

| Metric    | Value  | Notes                                |
|-----------|--------|--------------------------------------|
| AUC-ROC   | 0.847  | Primary metric                       |
| Precision | 0.71   | At threshold = 0.45                  |
| Recall    | 0.63   | At threshold = 0.45                  |
| F1        | 0.67   |                                      |
| Brier     | 0.082  | Calibration quality (lower = better) |

**Threshold selection rationale:**
[Why was this threshold chosen? What is the cost of false positives vs. false negatives?]

**Baseline comparison:**
[How does this model perform vs. the previous model or a naive baseline?]
```

### Step 4: Document subgroup performance and fairness evaluation

Molnar's emphasis: aggregate performance metrics hide disparate performance across subgroups.

```markdown
## Subgroup Performance

| Subgroup             | AUC   | Precision | Recall | Sample Size |
|----------------------|-------|-----------|--------|-------------|
| All users            | 0.847 | 0.71      | 0.63   | 50,000      |
| Mobile users         | 0.831 | 0.68      | 0.61   | 31,000      |
| Desktop users        | 0.872 | 0.76      | 0.67   | 19,000      |
| Account age < 90d    | 0.762 | 0.54      | 0.58   | 8,200       |
| Account age > 365d   | 0.889 | 0.79      | 0.71   | 22,000      |

**Known performance gaps:**
[Call out any subgroup with substantially lower performance. Document whether this is
acceptable or a known risk to remediate.]
```

### Step 5: Document features, interpretability, and failure modes

```markdown
## Features and Interpretability

**Number of input features:** [N]

**Top features by importance:**
| Feature                  | Importance | Notes                          |
|--------------------------|------------|--------------------------------|
| days_since_last_login    | 0.18       | Strongest predictor            |
| session_count_30d        | 0.14       |                                |
| support_tickets_open     | 0.11       | Proxy for dissatisfaction      |

**Interpretability method:** [SHAP, LIME, permutation importance, or none]
**Explainability at inference time:** [Yes/No - can individual predictions be explained?]

## Known Failure Modes

- **[Failure mode 1]:** [When does the model perform poorly? What data distribution causes it?]
- **[Failure mode 2]:** [e.g., "Model underperforms on accounts with < 30 days of history - cold start problem"]
- **[Failure mode 3]:** [e.g., "Performance degrades on data from promotional periods"]
```

### Step 6: Document deployment context and monitoring plan

```markdown
## Deployment

**Serving environment:** [batch job / real-time API / embedded in product]
**Inference frequency:** [daily batch / per-request / hourly]
**Latency requirement:** [e.g., < 200ms p99]
**Input data pipeline:** [where does inference data come from? what preprocessing is applied?]

## Monitoring and Maintenance

**Data drift monitoring:** [what features are monitored? what triggers a retraining alert?]
**Performance monitoring:** [what metric is tracked in production? what is the degradation threshold?]
**Retraining cadence:** [monthly / on-trigger / manual review]
**Model owner for production issues:** [team or individual]
**Deprecation plan:** [when and how will this model be retired?]
```

## Anti-Patterns

**1. Reporting only overall accuracy**
Bad: "The model is 91% accurate."
Good: Report AUC, precision, recall at the operating threshold, and subgroup breakdowns. 91% overall can mean 60% on the segments that matter most.

**2. Vague intended use statements**
Bad: "This model predicts user behavior."
Good: "This model predicts 30-day voluntary churn for subscribers with > 60 days of account history, using account activity features from the past 90 days."

**3. No out-of-scope section**
Bad: Documenting only what the model does, not what it should not be used for.
Good: Explicitly listing misuse cases. Other teams will reuse your model for purposes you did not intend.

**4. Skipping subgroup performance**
Bad: Publishing aggregate metrics without subgroup analysis.
Good: Always stratify by the subgroups that matter for the use case. If the model supports a decision that affects people, fairness analysis is not optional.

## Quality Checklist

- [ ] Model name, version, type, owner, and last-updated date present
- [ ] Intended use written in plain language with specific scope
- [ ] Out-of-scope uses listed explicitly
- [ ] Training data source, time range, size, and known limitations documented
- [ ] Test set performance reported with AUC, precision, recall, and F1 (not just accuracy)
- [ ] Subgroup performance table included for operationally relevant groups
- [ ] Top features by importance listed with interpretability method named
- [ ] At least 2 known failure modes documented
- [ ] Deployment environment and monitoring plan included
