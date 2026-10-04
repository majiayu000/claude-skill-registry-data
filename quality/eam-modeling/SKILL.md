---
name: eam-modeling
description: Inspect, explain, design, fit, diagnose, compare, validate, and report evidence-accumulation and simulation-based inference analyses. Use for MBNCS26 Days 1-5 material; R/EMC2 WDM, DDM, LBA, RDM, LNR, hierarchical, between-subject, dynamic, reinforcement-learning, stop-signal, continuous-judgment, joint, SEM, fMRI, and causal workflows; BayesFlow NPE/NLE/NRE, PyMC composition, model comparison, DMC/LCA simulators, calibration, and joint behavioral-neural inference; or Superstats time-varying cognitive models.
---

# Evidence-accumulation and SBI modeling

Build reproducible cognitive-model analyses while keeping the scientific claim, data coding, generative model, estimator, and predictive adequacy separate and auditable. Treat MBNCS26 examples as teaching patterns rather than validated defaults for new data.

## Route the request

- **Explain or review course material:** inspect the supplied code, object, output, or named day; do not refit unless asked.
- **Audit data:** map participant, response, RT, stimulus, condition, trial order, reward, neural, and grouping fields before modeling.
- **Likelihood-based EAM:** use R/EMC2 for standard, hierarchical, between-subject, joint, SEM, stop-signal, continuous-judgment, dynamic, or RL analyses when the required likelihood/API exists.
- **General SBI:** choose NPE, NLE, NRE, or classifier-based model comparison from the scientific query and downstream inference needs.
- **Amortized EAM:** use BayesFlow with explicit adapters and set/time-series routing; train on simulations, validate in silico, then infer real data.
- **Superstatistics:** use Superstats when the target includes full time-varying parameter trajectories and transition-process parameters.
- **Causal EAM/SEM:** separate the cognitive measurement model from the causal estimand, confirm identification assumptions, propagate latent uncertainty, and calibrate causal language.
- **Diagnose or compare:** distinguish sampler/training convergence, approximation quality, absolute predictive fit, and relative model preference.

## Load only the needed references

- Read [course-map.md](references/course-map.md) to locate a five-day worked example.
- Read [provenance-and-credits.md](references/provenance-and-credits.md) before using or describing MBNCS26-derived material.
- Read [data-schema.md](references/data-schema.md) for every new dataset.
- Read [model-routing.md](references/model-routing.md) before choosing a likelihood or architecture.
- Read [emc2-compatibility.md](references/emc2-compatibility.md) before writing or running EMC2 code.
- Read [emc2-workflow.md](references/emc2-workflow.md) for standard, hierarchical, group, fitting, prediction, or diagnostic work.
- Read [rl-dynamic-workflow.md](references/rl-dynamic-workflow.md) for trial-varying covariates, kernels, learning, Q-values, or feedback.
- Read [advanced-models.md](references/advanced-models.md) for stop-signal, continuous-judgment, joint, M/EEG, fMRI, or SEM work.
- Read [sbi-estimator-routing.md](references/sbi-estimator-routing.md) for NPE, NLE, NRE, PyMC composition, or neural model comparison.
- Read [day5-sbi-patterns.md](references/day5-sbi-patterns.md) before adapting a Day 5 example.
- Read [baygent-amortized-eam.md](references/baygent-amortized-eam.md) for BayesFlow adapters, simulator banks, offline training, recovery, or calibration.
- Read [superstats-workflow.md](references/superstats-workflow.md) for neural superstatistics and time-varying SBI.
- Read [baygent-bayesian-gates.md](references/baygent-bayesian-gates.md) before any new fit, sensitivity analysis, or model comparison.
- Read [baygent-causal-claims.md](references/baygent-causal-claims.md) for causal, mediation, intervention, counterfactual, or structural claims.
- Read [reporting.md](references/reporting.md) before delivering an analysis or scientific interpretation.

## Execute the workflow

### 1. Preserve, scope, and record provenance

- Treat raw data, supplied fits, simulator code, and course assets as immutable.
- State the scientific question, observables, latent quantities, estimand, candidate models, and available compute.
- Record data, simulator, software, course, repository, commit, license, and modification provenance.
- Apply the course attribution and redistribution boundary when MBNCS26 material is used.

### 2. Check the environment and API

- Run `scripts/check_eam_environment.R` before EMC2 work. Require the dynamic API for Day 4 kernels or RL models.
- Run `scripts/check_sbi_environment.py --profile day5` for the MBNCS26 BayesFlow environment.
- Run `scripts/check_sbi_environment.py --profile superstats` for Superstats.
- Inspect actual function availability and signatures. Do not infer API compatibility from a package version alone.
- Use a project-local R library or Python environment when changing EMC2 branches or deep-learning backends.

### 3. Audit the data and simulator

Run the data audit for CSV, XLSX, RDS, or RData inputs and inspect every generated file. Resolve response coding, RT units, trial order, condition levels, reset boundaries, missingness, truncation/censoring, contamination, exclusions, and sparse cells.

For simulators, test deterministic seed behavior, parameter order, bounds, transforms, units, output shapes, invalid/non-boundary-crossing trials, missing masks, and contamination. Run a small prior-predictive batch before training or fitting.

### 4. Choose a theory-driven model and estimator

- State the process interpretation and observable implications of each free parameter.
- Keep the candidate set small and scientifically motivated.
- Keep data rows, response coding, units, and preprocessing identical across compared models.
- Enforce EAM scale identification and simulator support explicitly.
- Use NPE for repeated direct posterior queries, NLE for learned-likelihood composition, NRE for ratio-based inference, and model comparison only with a declared model set and model prior.
- Route exchangeable trials through a set representation and ordered learning/dynamic trials through a time-series representation.

### 5. Validate priors and identifiability

- Specify EMC2 priors on the sampling scale and inspect mapped natural-scale implications.
- Inspect parameter-path priors and prior push-forwards for dynamic/Superstats models.
- Reject impossible RT, choice, learning, neural, or trajectory simulations.
- Run parameter/model recovery when a design, simulator, transition, summary, or mapping is new.

### 6. Fit or train in stages

- Pilot before a full MCMC fit or large simulation bank.
- On Windows, use EMC2 `cores_for_chains`; keep `cores_per_chain = 1`.
- For BayesFlow, start with offline training and held-out validation; save split seeds, history, checkpoints, package lock, and simulator hash.
- Use online training only as a justified refinement after an offline pass.
- For Superstats, preserve local, hyper, shared, and fixed parameter roles and the time axis.
- Never assign the return value of R `save()` to a fit object.

### 7. Apply diagnostic gates

Do not interpret real-data parameters until the relevant gates pass:

- MCMC stationarity, chain mixing, R-hat, effective sample size, autocorrelation, posterior geometry, and participant-level checks;
- training-history stability without NaN/divergence;
- held-out parameter and model recovery;
- SBC/calibration, coverage, contraction, and estimator/seed disagreement;
- prior and posterior predictive checks for choice, RT, condition effects, learning curves, trajectories, and neural observations;
- comparison with an analytic likelihood, EMC2, HSSM, or another tractable benchmark when available.

Treat convergence, approximation quality, model adequacy, and model comparison as four different questions.

### 8. Report and hand off

Export the data mapping, exclusion ledger, formulas, contrasts, priors, simulator, estimator/training configuration, checkpoints or fits, posterior draws, PPCs, recovery/calibration outputs, sensitivity results, model comparison, provenance, and limitations. Report failed gates as prominently as passed gates.

## Hard guardrails

- Never alter raw data or supplied fits in place.
- Never silently convert RT units, reorder response levels, flatten ordered trials, or collapse conditions.
- Never extrapolate beyond simulator/prior support without redesigning simulations and revalidating.
- Never treat low training loss, convergence, or a winning comparison as evidence of scientific adequacy by itself.
- Never treat participant posterior means as error-free outcomes when joint uncertainty propagation is feasible.
- Never make a causal claim without an identified design, explicit graph/assumptions, and sensitivity/refutation checks.
- Never copy or redistribute MBNCS26 notebooks, slides, recordings, datasets, logos, or checkpoints through this skill.
- Never describe this skill as official or endorsed by MBNCS26 presenters, organizers, software authors, their institutions, or any AI-agent platform vendor.
- Keep unrelated courses and summer schools outside this MBNCS26 skill.

## Bundled tools

- `scripts/check_eam_environment.R` — inspect R, EMC2, stable/dynamic API availability, and Windows parallel constraints.
- `scripts/inspect_eam_data.R` — audit common behavioral data formats without modifying the input.
- `scripts/new_eam_analysis.R` — scaffold a likelihood-based EAM analysis.
- `scripts/check_sbi_environment.py` — inspect BayesFlow, PyMC, HSSM, Superstats, backends, and Python compatibility without heavy imports.
- `scripts/scaffold_sbi_analysis.py` — scaffold NPE/NLE/NRE/model-comparison/Superstats projects with uv metadata.
- `scripts/inspect_bayesflow_training.py` — inspect saved training histories.
- `scripts/check_bayesflow_diagnostics.py` — summarize saved recovery, calibration, and contraction metrics.
