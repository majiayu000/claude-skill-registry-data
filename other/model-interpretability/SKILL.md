---
name: model-interpretability
description: "\"Make it interpretable\" is four different requests."
---

# Model Interpretability (Verbose)

## Core Patterns

### Pick the Explanation That Answers the Question

"Make it interpretable" is four different requests. Separate them before
choosing a tool.

| Need | Scope | Tool | Cost |
|---|---|---|---|
| What does the model rely on overall? | Global | SHAP beeswarm, PDP | Moderate |
| Why did *this* row get this score? | Local | SHAP waterfall, LIME | Low per row |
| What would change this decision? | Local, actionable | Counterfactuals (DiCE) | Moderate |
| Shape of the response to a feature | Global | PDP + ICE | Low |
| Regulatory adverse-action reason | Local, defensible | Glassbox model coefficients | Built in |
| Which features earn their keep? | Global | Permutation importance | Retrain-free but slow |

The last row belongs to the feature-importance-analysis skill; keep the two
questions distinct — "what did the model use" is not "what would I lose if I
dropped it."

### SHAP in Practice

SHAP assigns each feature a credit for moving the prediction away from a base
value, using Shapley values from cooperative game theory. The additivity
guarantee is what makes it useful: contributions sum exactly to the output.

```python
import shap

explainer = shap.TreeExplainer(model)      # exact for tree ensembles
sv = explainer(X_test)                     # Explanation: .values, .base_values, .data

shap.plots.waterfall(sv[0])                # single prediction, sorted contributions
shap.plots.beeswarm(sv)                    # global: spread and direction per feature
shap.plots.scatter(sv[:, "tenure"])        # learned response shape for one feature
```

Two details that trip people up:

- **Units.** For a binary tree classifier, `TreeExplainer` works in log-odds by
  default, so contributions do not sum to a probability. Convert deliberately or
  present the log-odds honestly.
- **Background data.** Explainers explain relative to a reference distribution.
  `shap.sample(X_train, 100)` or `shap.kmeans` is standard for the
  model-agnostic explainers; changing the background changes every attribution,
  so record which one you used.

Pick the right explainer:

| Model | Explainer | Note |
|---|---|---|
| Tree ensembles (XGBoost, LightGBM, sklearn forests) | `TreeExplainer` | Exact, polynomial time |
| Linear models | `LinearExplainer` | Closed form |
| Neural nets | `DeepExplainer`, `GradientExplainer` | Approximate |
| Anything else | `KernelExplainer` | Model-agnostic, sampled, slow |

Running `KernelExplainer` on a random forest is a common waste: it approximates
by sampling what `TreeExplainer` computes exactly.

### Partial Dependence and ICE

```python
from sklearn.inspection import PartialDependenceDisplay

PartialDependenceDisplay.from_estimator(
    model, X_test,
    features=["tenure", "monthly_charges", ("tenure", "monthly_charges")],
    kind="both",          # ICE curves plus their average (the PDP)
)
```

A PDP is an average over the marginal distribution, and averages hide
heterogeneity. If half the ICE curves slope up and half slope down, the PDP is
flat and reports "no effect" for a feature with a strong, interaction-dependent
effect. Always look at `kind="both"` before believing a flat PDP.

PDPs also extrapolate. Computing dependence on `age=25` while holding
`years_employed=40` fixed evaluates the model on a combination that never
occurs, and the output there is unconstrained fantasy. Accumulated Local Effects
(ALE) avoids this by using conditional rather than marginal distributions and is
the safer default under strong feature correlation.

### The Central Caveat: Model, Not World

An explanation is a description of a function you fit. It carries no causal
claim.

- **Proxies get the credit.** If `number_of_specialist_visits` correlates with
  disease severity, SHAP attributes the prediction to visits. Acting on that —
  reducing visits — changes the prediction and nothing about the patient.
- **Correlated features share credit arbitrarily.** With two near-collinear
  inputs, the fitted model can split the signal between them in many ways that
  are equally good on training loss. Refit with a new seed and the attribution
  can swap. The explanation is stable only to the extent the model is.
- **A wrong model is confidently explained.** SHAP will produce a crisp
  attribution for a model with 0.55 AUC. Validate accuracy first (see
  model-evaluation); interpretation of a bad model is elaborate noise.

If the question is genuinely "what happens if we intervene," you need causal
inference — an experiment, or an identification strategy with stated
assumptions. No post-hoc attribution method substitutes for it.

### Validating an Explanation

```python
# 1. Label-shuffle control: nothing should look important
y_shuffled = rng.permutation(y_train)
control = clone(model).fit(X_train, y_shuffled)
# Any feature with strong attribution here indicates leakage or a pipeline bug

# 2. Stability across seeds
rankings = [top_k_shap(clone(model).set_params(random_state=s).fit(X, y))
            for s in range(5)]
# Disagreement in the top 5 means the ranking is not a finding

# 3. Direct perturbation check
x = X_test.iloc[[0]].copy()
x["tenure"] += 12
model.predict_proba(x)[0, 1] - model.predict_proba(X_test.iloc[[0]])[0, 1]
# Should move in the direction and rough magnitude SHAP claimed
```

### Glassbox Models

When the explanation has to survive a regulator or a clinician, consider making
the model itself the explanation: penalized logistic regression, a scorecard,
a decision list, or an Explainable Boosting Machine (GA2M). These are additive in
shape functions, so the "explanation" is exact by construction rather than a
post-hoc approximation that may disagree with the model. The accuracy gap versus
a tuned gradient-boosting model on tabular data is often 1-2 points of AUC —
frequently a good trade when a wrong-and-unjustifiable decision is the real cost.

## Common Anti-Patterns

❌ **Reading SHAP causally** — "reduce support tickets to reduce churn" when
tickets merely signal dissatisfaction.
✅ Present attribution as model behavior; escalate to experiment or causal
identification before recommending an intervention.

❌ **Explaining before validating.** A crisp explanation of a model that barely
beats the base rate.
✅ Establish predictive performance first, then explain.

❌ **`KernelExplainer` on a tree model.** Slow sampling where an exact
polynomial-time algorithm exists.
✅ `TreeExplainer` for tree ensembles, `LinearExplainer` for linear models.

❌ **A flat PDP read as "no effect"** on a model with strong interactions.
✅ `kind="both"` to expose ICE heterogeneity; ALE when features are correlated.

❌ **Ignoring the background dataset.** Attributions shift with the reference
distribution and the choice goes unrecorded.
✅ Fix, document, and re-use the background sample across runs.

❌ **Shipping the top-10 feature list without a stability check.**
✅ Recompute across seeds and resamples; report only what holds.

❌ **Explanations shown to end users in log-odds** labeled as probability.
✅ State the units, or transform explicitly and accept the loss of additivity.

## Interpretability Checklist

- [ ] Explanation question stated: global vs local, descriptive vs actionable
- [ ] Model accuracy validated before any explanation is produced
- [ ] Explainer matched to model family (`TreeExplainer` for trees, etc.)
- [ ] Background / reference dataset chosen and recorded
- [ ] Output units (log-odds vs probability) stated wherever shown
- [ ] PDPs accompanied by ICE curves; ALE used under correlated features
- [ ] Attribution stability checked across seeds and resamples
- [ ] Label-shuffle control run to catch leakage
- [ ] SHAP claims spot-checked by perturbing inputs directly
- [ ] Causal language avoided unless backed by a causal design
- [ ] Glassbox alternative considered where decisions are contestable
- [ ] Explanations regenerated after retraining, not carried forward stale
