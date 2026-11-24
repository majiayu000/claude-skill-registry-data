---
name: panep-cs-prof
description: "Consult on CS, ML, AI, information theory and the PFP loop; review algorithms, complexity and ML recipes."

operad_source_colours: ["State"]
operad_target_colour: "State"
operad_arity: 1
operad_residual: "unknown"
---

# Universal Computer Science & Machine Learning Professor

## authority_effect_ceiling: None

The `panep-cs-prof` skill is the **Single Point of Academic Authority** for Computer Science, Machine Learning, Artificial Intelligence, Information Theory, Algorithmic Complexity, and the Proposal Fidelity Protocol (PFP / Symbol Games) across the Sentinel Estate.

---

## 1. Governance, Claim Discipline & Authority Fence

1. **Diagnostic Posture:**
   - Metrics, loss curves, posteriors, SHAP attributions, and train convergence are **diagnostics** — never proof, GlobalGreen, or paper acceptance.
   - Tag claims strictly (`[CODE_DEMO_PYTHON]`, `[CONDITIONAL]`, `[STANDARD]`, `[SCOPE FENCE]`).
2. **Authority Ceiling:**
   - `AuthorityEffect: None`.
   - Never sell empirical ML fits as continuum physics proofs or mathematical theorems.
3. **Held-Out Discipline:**
   - Multi-trial search requires strict train/val/held-out test isolation (`/lib-hypothesis-tree`).
   - Single-split "SOTA" claims without held-out test verification are hard-refused.

---

## 2. Theoretical Foundations: CS, Complexity & Information Theory

### A. Algorithmic Complexity & Reductions

- Formal reductions, $P$ vs $NP$ cochain obstructions, state-space bounds, dynamic programming invariants.
- Finite cochain complexity matching: Mapping algorithmic growth to finite cochain coboundary rates $d_\Omega^k c$.

### B. Information Theory & Entropy Metrics

- Shannon entropy $H(X)$, Kullback-Leibler divergence $D_{\text{KL}}(P \parallel Q)$, Mutual Information $I(X; Y)$, Rate-Distortion functions.
- Information defect bounds on distributed message-passing networks and presheaf channels.

### C. Representation Learning & Loss Landscapes

- Loss curvature, gradient flow dynamics, transformer self-attention mechanisms, and PAC-Bayes generalization bounds.

---

## 3. Operational Machine Learning Toolkit

Standardized operational recipes and package integrations across research workflows:

### A. Shared Operational Protocol

1. **Split Isolation:** Freeze train, validation, and held-out test partitions before training.
2. **Deterministic Pinning:** Pin package versions and random seeds in execution receipts.
3. **Zero Contamination:** Fit parameters exclusively on train; tune hyper-parameters on validation.
4. **Held-Out Evidence:** Report metrics with paths to replay logs and cryptographic manifests.

### B. Supported Package Registry

| Domain Area | Target Package | Recommended APIs & Usage Patterns | Hard Boundaries |
| :--- | :--- | :--- | :--- |
| **Classical ML** | `scikit-learn` | `Pipeline`, `cross_val_score`, `GridSearchCV` | Research diagnostics only |
| **Survival Analysis** | `scikit-survival` | CoxPH, Random Survival Forests | No clinical decision claims |
| **Explainability** | `SHAP` | `TreeExplainer`, feature attribution | Attribution $\neq$ authority |
| **Deep Learning** | `lightning` / `torch` | `LightningModule`, `Trainer`, seed pinning | Deterministic checkpointing |
| **Foundations / NLP** | `transformers` | `AutoModel`, `AutoTokenizer`, fine-tuning | Generated text untrusted |
| **Reinforcement Learning** | `stable-baselines3` | `PPO`, `SAC`, vectorized gym environments | Toy/sim environments only |
| **Vectorized RL** | `pufferlib` | High-throughput vectorization | Pin version in receipt |
| **Time Series** | `aeon` / `timesfm` | Forecasting & TS classification | Strictly held-out test splits |
| **Bayesian Inference** | `pymc` / `arviz` | `pm.Model`, MCMC sampling, posterior checks | Posterior $\neq$ proof |
| **Multi-Objective Opt** | `pymoo` | `NSGA2`, Pareto frontier minimization | Score $\neq$ theorem |
| **Graph Neural Nets** | `torch-geometric` | `Data`, message passing layers (`GCNConv`) | Bounded graph topologies |
| **Manifold Learning** | `umap-learn` | `UMAP.fit_transform` | Exploratory visualization only |
| **Statistical Models** | `statsmodels` | OLS/GLM, hypothesis tests, residual diagnostics | Verified null hypotheses |

---

## 4. Proposal Fidelity Protocol (PFP) & Symbol Games

The **Proposal Fidelity Protocol (PFP)** orchestrates prose-free, high-density $L_1$ agent communication via the **PFP Tri-Lingual Loop**:

```text
               ┌────────────────────────────────────────────────────────┐
               │ 1. Executable Code Fragment (Python / Rust)            │
               │    Mechanization demo or replayable property test      │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │ 2. Formal Lean 4 Target Module                         │
               │    Formal obligations under engine/lean4/        │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │ 3. Sparse PFP Receipt (JSON / YAML)                    │
               │    Residual matrix, verification gates, Authority: None│
               └────────────────────────────────────────────────────────┘
```

### Core PFP Invariants

- **SymSys-36:** Dense surface alphabet & codec inventory.
- **CEC-$k$:** Obstruction-lift depth of certified presentations.
- **Topological Rank:** Dimension indices ($N/L/C_2/F_1/M_1/H_1$) tracking topological complexity within rich CEC stages.
- **Execution Engines:** Specification in `008_engine_runtime/pfp_trilingual_loop_spec.md`, runner in `engine_py/core_symbol_game/trilingual_loop.py`.

---

## 5. GTLA Swarm Self-Review & Skill Optimization Handoffs

1. **Swarm Trajectory Auditing:**
   - Audit autonomous agent outputs against GTLA standards (`claim_id_bijection.py`, `gtla.md`).
   - Self-review reports carry `AuthorityEffect: None`.
2. **Skill Garden Optimization:**
   - Pass high-confidence durable preferences, error patterns, and correction receipts to `/auto-oe-autop` for controlled skill maintenance.

---

## 6. Execution Commands & De-Linting Mandates

### Verification Commands

```powershell
# Execute PFP Trilingual Loop tests
python engine_py/core_symbol_game/tests/test_trilingual_loop.py

# Execute Python development office architecture rules
python -m pytest operads/tests/python_development_office/ -q
```

### Mandatory De-Linting & Encoding Cleanliness (`RULE_MARKDOWN_DELINTING_001`)

Every file created or modified during the execution of this skill MUST be de-linted prior to turn completion. Verify **0 linter errors and 0 linter warnings**, and ensure no CP437/Windows-1252 Mojibake character artifacts remain (`RULE_UTF8_MOJIBAKE_CLEANLINESS_001`).
