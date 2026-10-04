---
name: academic-experiments
description: "Audit, run, or verify experimental evidence for CS/AI/ML papers. Produces Evidence Inventory with evidence_type annotations (newly_run/preexisting_artifact/user_claim) and Protocol Risk assessments. Use when: checking if experiment results are reproducible, auditing existing experiment artifacts, running minimal reproducible commands, evaluating checkpoints without full retraining, documenting protocol risks like data leakage or missing baselines. Triggers on: 复核实验, run experiments, 实验结果, experiment evidence, verify results, 实验验证, evidence inventory, protocol risk, 跑实验, check results, reproduce experiments, 实验审计."
---

# Academic Experiments

将此 skill 视为"实验取证代理"，目标是建立最短且可信的证据链，而不是尽量多跑实验。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines non-negotiable rules, evidence type semantics, failure degradation, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables per mode and claim-readiness classification.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
4. Detect the mode using the manifest's `mode` axis: `experiment-evidence-pass`, `evidence-inventory-only`, or `minimal-reproducible-run`. Align evidence type semantics to `../shared/core/evidence-policy.md`.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `experiment-evidence-pass` | Full audit: inventory + run + record + risk analysis |
| `evidence-inventory-only` | Inventory existing artifacts only, no execution |
| `minimal-reproducible-run` | Execute minimal reproducible command (e.g. eval existing checkpoint) |

## Agent Dispatch

`agents/experiment_agent.md` is dispatched by `academic-paper-writer` orchestrator at Step 4. The agent may run experiments but must not modify project source code or data files, nor write paper prose independently.

## Independent Use

| Input | Mode | Priority | Behavior |
|---|---|---|---|
| `repo_path` + no run mode | experiment-evidence-pass | 2 (path trigger) | Full audit: inventory → env → minimal run → risk |
| `repo_path` + "inspect only" | evidence-inventory-only | 1 (explicit) | Inventory only, no commands |
| `repo_path` + specific command | minimal-reproducible-run | 1 (explicit) | Verify env → execute → record |
| No `repo_path` | — | 3 (no input) | Ask path, or auto-detect entry files |

| Scenario | Recommended |
|---|---|
| Just auditing/reproducing evidence | This skill (standalone) |
| Writing results into paper prose | academic-paper-writer orchestrator |
| Draft results need verification | This skill → academic-reviser |
