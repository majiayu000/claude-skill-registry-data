---
name: sota-ml-engineering
description: >-
  State-of-the-art ML engineering / MLOps rules (2026) for BUILDING and
  AUDITING production machine-learning systems — the
  training→serving→monitoring lifecycle of classical/predictive ML. Distinct
  from LLM apps (prompts/RAG/agents → sota-llm-engineering). Covers ML system
  architecture (feature stores, model registry, reproducibility), data &
  features (leakage, train/serve skew, versioning), training & experiment
  tracking, evaluation (ML Test Score, slices, regression gates),
  deployment/serving (canary/shadow, rollback), monitoring & drift (PSI/KS,
  retraining), and ML security & governance (poisoning, model extraction,
  unsafe pickle, MITRE ATLAS, NIST AI RMF, EU AI Act). Trigger keywords -
  MLOps, machine learning, ML pipeline, model training, feature store, model
  registry, experiment tracking, MLflow, model serving, data drift, concept
  drift, train/serve skew, data leakage, model monitoring, retraining, ML Test
  Score, model card, MITRE ATLAS. Use for BOTH building and auditing ML
  systems.
---

# SOTA ML Engineering / MLOps (2026)

Expert rules for building and auditing **production machine-learning systems** —
the lifecycle that turns a model into a reliable, monitored, governed service.
This is **classical/predictive ML** (tabular, ranking, vision, forecasting,
recommendation): training pipelines, feature stores, model registries, serving,
and drift monitoring. It is **not** LLM-application engineering — prompts, RAG,
agents, and LLM evals live in `sota-llm-engineering`; data pipelines/warehouses
live in `sota-data-engineering`. Grounded in Google's
[Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml),
the [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
rubric, and [Hidden Technical Debt in ML Systems](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/).
Every rule states the *why*; every rules file ends with an audit checklist.

## Purpose

Two consumers, one source of truth:

- **BUILD mode** — building ML systems: follow the rules as defaults. The model
  is a small part; the system around it (data, features, serving, monitoring,
  governance) is where production ML succeeds or rots.
- **AUDIT mode** — reviewing an ML system: hunt violations with the audit
  checklists, classify by severity, report in the finding format below.
  Train/serve skew, data leakage, and an unmonitored model in production are
  presumed-serious until disproven.

## BUILD mode

1. Before building, read the rules files relevant to the task (see index). A new
   model service needs `01`, `02`, `04`, `05`, `06`.
2. Apply the **top-10 non-negotiables** (below) unconditionally.
3. Start simple (Rules of ML #1: *don't be afraid to launch a product without
   ML*; then a simple model with a solid pipeline beats a fancy model on a
   broken one). Build the **pipeline, metrics, and monitoring first**; the model
   is iterated inside that frame.
4. Make everything **reproducible and versioned** — data, features, code,
   config, model, environment — so any model in production can be rebuilt and
   explained.
5. Guarantee **training/serving consistency**: the same feature transformations
   at train and inference time (a feature store or shared transform code), or
   you will ship train/serve skew (Rules of ML #29, #31, #32).
6. When you take a shortcut (manual step, un-versioned data, no slice metrics),
   leave a `# NOTE(sota):` and a tracking item — ML technical debt compounds
   silently.

## AUDIT mode

Work each relevant rules file's audit checklist against the system: the
training pipeline, the feature/serving path, the registry, and the monitoring.
The [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
(data / model / infra / monitoring tests) is the backbone rubric — score each
category. Confirm claims against the code and pipeline config, not the diagram.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **CRITICAL** | Silently wrong predictions in production, or exploitable | Data leakage inflating offline metrics, train/serve skew on the prediction path, label leakage, deserializing an untrusted `pickle`/model, no rollback for a bad model |
| **HIGH** | Likely incident or unsafe deployment | No drift/performance monitoring in prod, no validation gate before deploy, non-reproducible model (can't rebuild), unversioned data/features, no slice metrics on a high-stakes model, PII in features without basis |
| **MEDIUM** | Correctness/maintainability hazard / debt | Single aggregate metric only, no baseline, manual deploy steps, feature computed two ways, no experiment tracking, glue-code/pipeline-jungle, undeclared consumers of a model output |
| **LOW** | Debt that will bite later | Unused features kept in infra, no model card, notebook-only training, weak naming/versioning hygiene |
| **INFO** | Style/doc/hygiene | Missing docstrings, dashboard polish, minor config sprawl |

### Finding format

```
[SEVERITY] path:LINE (or pipeline stage) — short title
  Rule: rules/NN-name.md § section
  Evidence: code/config/metric, verbatim
  Impact: one sentence — what predicts wrong / fails / leaks, under what condition
  Fix: concrete change or control
  Effort: trivial | small | medium | large
```

Group by severity, CRITICAL first. End with: counts per severity, an ML Test
Score-style readiness summary (data/model/infra/monitoring), and the three
highest-leverage fixes.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-ml-systems-architecture.md` | Designing/reviewing an ML system: the model-is-small-part principle, training vs serving paths, feature store, model registry, reproducibility, append-only model audit trail and registered checkpoints, trust domains across training/evaluation/serving (tracker auth, purpose-scoped feature namespaces), the Hidden-Technical-Debt anti-patterns (entanglement/CACE, glue code, pipeline jungles, undeclared consumers, feedback loops) |
| `rules/02-data-and-features.md` | Anything touching training data or features: data leakage and label leakage, train/serve skew, feature/data versioning, splits (temporal/group), feature engineering discipline, dropping unused features, PII minimization, signed dataset attestations and stage-to-stage verification, purpose-bound fields and per-row consent codes, training-data admission (labeling roles, auto-label QA, adjudication-window quarantine) |
| `rules/03-training-experimentation.md` | Training and iterating: experiment tracking & reproducibility (seeds, env, data hash), hyperparameter search, distributed training/checkpointing, config management, reproducible runs, starting simple |
| `rules/04-evaluation-validation.md` | Deciding if a model is good enough: offline metrics vs the business objective, baselines, **sliced** evaluation and fairness, the ML Test Score tests, validation gates and regression thresholds before promotion, robustness slice, re-validating quantised/distilled artifacts |
| `rules/05-deployment-serving.md` | Shipping a model: packaging (containers/ONNX), batch vs online vs streaming serving, model registry promotion, canary/shadow/A-B rollout, full-state rollback and isolated runtime caches, latency/throughput, reproducible inference environment, model decommissioning |
| `rules/06-monitoring-drift.md` | Operating a model: data drift (PSI/KS) vs concept drift vs performance decay, label lag, embedding drift for text/images, abrupt vs gradual shift, prediction & feature monitoring, alerting, retraining triggers and cadence, ML-specific observability (cross-ref `sota-observability`) |
| `rules/07-security-governance.md` | ML security & compliance: training-data poisoning, model extraction/inversion/membership inference, adversarial inputs, supply chain (untrusted `pickle`/model artifacts, dataset provenance, OMS model signing verified at admission and load, sandboxed third-party-model workers), backdoor screening and trigger-corpus gate, extraction detection and response, required adversarial robustness, OOD gating at inference, signed per-model ML-BOM, prompt/guardrail drift checks, on-device model signing, credential leaks as data-integrity incidents, DP training and membership-inference tests, inferred special-category attributes, MITRE ATLAS, NIST AI RMF, model cards, EU AI Act obligations |

## Top-10 non-negotiables

1. **No data leakage.** No information from the target or the future or the test
   set enters training features (no fitting scalers/encoders on the full dataset
   before split, no post-outcome features). Leakage inflates offline metrics and
   is CRITICAL — it makes a broken model look great. (`rules/02`, `rules/04`)
2. **No train/serve skew.** The exact feature transformations used in training
   are used at inference — shared code or a feature store, not reimplemented
   twice. Verify with skew checks. (`rules/01`, `rules/02`)
3. **Everything is reproducible and versioned** — data, features, code, config,
   environment, and the model artifact — so any production model can be rebuilt
   and explained. A model you can't reproduce is HIGH. (`rules/01`, `rules/03`)
4. **Pipeline and monitoring before model sophistication.** A simple model on a
   solid, monitored pipeline beats a fancy model on a fragile one
   (Rules of ML). (`rules/01`)
5. **Evaluate on slices and against a baseline, not one aggregate number.**
   Report per-segment metrics and fairness-relevant slices; a model that wins on
   average can fail badly on a subgroup. (`rules/04`)
6. **A validation gate guards promotion.** Automated checks (metric thresholds,
   no regression vs current prod, slice floors, data/schema validation) must
   pass before a model is promoted; deploys are reversible with fast rollback.
   (`rules/04`, `rules/05`)
7. **Production models are monitored for drift and decay.** Data drift (PSI/KS),
   prediction distribution, and — as labels arrive — live performance, with
   alerts and a retraining trigger. An unmonitored model silently rots. (`rules/06`)
8. **Never deserialize an untrusted model/`pickle`.** `pickle`/`joblib`/`torch.load`
   on an untrusted artifact is arbitrary code execution; verify provenance and
   integrity (hashes/signing), prefer safe formats (`safetensors`, ONNX).
   (`rules/07`)
9. **Govern data and the model.** Minimize PII in features and document a lawful
   basis; produce a model card; map risks with MITRE ATLAS / NIST AI RMF; check
   EU AI Act obligations for high-risk use. (`rules/07`)
10. **Kill ML debt deliberately.** Drop unused features, delete dead pipelines,
    untangle glue code, declare consumers of model outputs, and break feedback
    loops — the Hidden-Technical-Debt anti-patterns. (`rules/01`)
