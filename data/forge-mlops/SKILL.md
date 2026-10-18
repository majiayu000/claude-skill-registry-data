---
name: forge-mlops
description: "Forge: production ML systems (opt-in Python) — training-to-serving lifecycle: MLOps, model registry, MLflow, drift monitoring, A/B test, canary, rollback."
---

# Forge playbook — Production ML / MLOps

**Do not duplicate ECC skills — defer to:** `systematic-debugging` (pipeline/training failures), `/test-coverage` (data-validation + feature-code tests), `forge-data` (the upstream ETL/feature pipeline), `forge-prediction` (uncertainty labeling + no-auto-bet rules when the model informs a betting/forecast decision). This file is orchestration only.

The unit of value in MLOps is a **reproducible, versioned, monitored model that a human decides to promote** — not a one-off notebook accuracy number. The dangerous failure is a model that looks better offline, silently skews at serving, decays over weeks, or worse, is wired to *act* (spend, send, trade) on its own. A model **informs**; the owner promotes and the owner gates any irreversible action.

## Hard rules
- **Decision note before training.** Before training code, write a one-page decision note: goal, success and guardrail metrics, acceptable vs unacceptable mistakes, baseline, data snapshot, rollback plan.
- **Metric selection by mistake cost.** Choose metrics by the cost of each mistake: precision when false positives are expensive, recall when misses are; include latency and cost; always compare against the current baseline.
- **Reproducible training.** Seeds fixed, dependencies pinned, data + code + config versioned (DVC / MLflow / a manifest), and the run captured so the **same code + same data regenerates the same metric**. An accuracy you can't reproduce is not a result.
- **Model versioning + working rollback.** Every model artifact is immutable and versioned in a registry with its training data/version and metrics attached. There is a **tested** rollback path and a fallback model (or graceful degradation) if the new one fails at serve time.
- **No train/serve skew.** Feature engineering is versioned and identical between training and serving. A data-validation gate at pipeline entry (schema + range checks) rejects bad input before it poisons training or inference.
- **Offline + online evaluation before promotion.** Offline: a proper holdout / time-based backtest with the task-appropriate metric (AUC/PR, MAE/RMSE, calibration) compared **against the incumbent**, not in a vacuum. Online: shadow / canary / A-B — never a hard cutover of a new model onto a critical path.
- **Drift + decay monitoring.** Feature drift, prediction drift, and performance decay are monitored with alerts; retraining triggers are defined (not "we'll notice eventually"). Serving endpoints have health checks, timeouts, and bounded retries.
- **No automatic real-money / irreversible / outward-facing action — ever.** The model produces a prediction/score; it does not auto-spend, auto-trade, auto-send, or auto-execute. **Promotion to production is an explicit owner-gated step** (Forge honesty + irreversible-action rule). No secrets or credentials embedded in pipeline code or model artifacts.

## Team
Lead: `build-boss` (or `integration-boss` when serving wires into external systems). Specialists: **`ml-engineer`** (`.claude/agents/ml-engineer.md`) leads the pipeline / serving / rollout / monitoring work; **`data-scientist`** (`.claude/agents/data-scientist.md`) owns validation scheme, metric choice, offline eval, leakage checks, and honest uncertainty labels; `python-reviewer` (training + serving code); `database-reviewer` (feature store / offline-online feature parity); `silent-failure-hunter` (a metric that silently degraded, a canary that never actually received traffic). Optional advisor: `security-boss` / `security-reviewer` for secrets-in-artifacts + data-access review.

## Skills / commands / MCP
`systematic-debugging` and `/test-coverage` always in scope. **OPT-IN dependency (honest, load-bearing):** production ML **requires a Python environment + the ML stack** (scikit-learn / PyTorch / XGBoost, plus **MLflow** or **DVC** for tracking/versioning). Forge can scaffold the pipeline, write training/eval/serving code, design the eval + drift harness, and review all of it — but *actually training a model, measuring latency, running a canary, or standing up drift monitors requires that Python env and real serving infra, which the owner provides.* Do not claim a trained model, a measured metric, or a live canary that was never run. Use Context7 / vendor docs for framework + MLflow/DVC API behavior. If the model is served behind an API, defer serving-layer wiring to `forge-integration` / `forge-fullstack`. `claude-api` only if an LLM is the model in the loop (for LLM-app/agent evals, see `forge-agent`).

## Fan-out & flow
L3 (a real production ML system is inherently multi-component).
**Parallel:** data-validation gate ∥ feature pipeline ∥ offline-eval harness ∥ drift/monitoring scaffolding (independent once the feature contract + metric are fixed).
**Serial:** data validation → feature engineering (versioned, parity-checked) → reproducible training → offline eval vs incumbent → register + version artifact → shadow/canary online eval → monitored rollout → **owner-gated promotion**. The go-live decision is a human checkpoint, not a pipeline step.

## Domain gates
Training reproducible (seed + pinned deps + versioned data/config regenerate the metric); model versioned in a registry with a tested rollback + fallback; no train/serve skew (feature parity proven); data-validation gate at entry; offline eval compares against the incumbent with the right metric + validation scheme; online eval via shadow/canary before any promotion; feature/prediction drift + performance decay monitored with alerts and defined retrain triggers; serving has health checks/timeouts/bounded retries; **no auto real-money/irreversible action path exists**; no secrets in pipeline code or artifacts.

## Ship-readiness
Reproducible-run evidence (same seed/data → same metric, with the real command output); versioned artifact + a rollback that was actually exercised; offline metric shown **relative to the incumbent** with its validation scheme; a shadow/canary plan (or executed canary result) before promotion; drift + decay monitors defined/live with alert thresholds and a retrain trigger; **promotion is owner-gated and no autonomous real-money/irreversible action is wired**; no secret in any artifact. Advisory checklist — optionally run `codex-reviewer` (Codex) on the training + serving + feature-parity code (recommended for production ML). **State the Python/infra opt-in status honestly:** if the pipeline was scaffolded/reviewed but not trained or served because the env wasn't available, label those checks not-run rather than implying they passed.

## Untrusted-content note
Training data, feature inputs, and inference requests are untrusted at the boundary — validate schema/ranges and reject anomalies before they reach the model. Never let input content trigger an action; the model's output is a score for a human/gated system to act on, not a command.
