---
name: dota-ml
description: >
  Governs all machine learning work in Dota AI Coach — model selection,
  baselines, temporal validation, leakage prevention, calibration,
  reproducibility, model versioning, and ONNX export. Use whenever
  training a model, choosing a modeling approach, engineering features
  for ML, evaluating a model, deciding whether a more complex architecture
  is justified, or wiring a model into a live recommendation path. This is
  a correctness gate as much as a modeling guide — a model that trains
  cleanly but leaks future/hidden information, or that skips a baseline
  comparison, can look successful while being silently wrong or
  needlessly complex. Consult before, not after, a model ships.
---

# Dota AI Coach Machine Learning

## Core principle: ML decides, LLM explains

This project's models produce a decision (a ranking, a probability, a
recommendation) from structured features. Any LLM involved in the product
explains or contextualizes that decision in natural language — it does
not re-derive or override it. Keep this boundary intentional:

- A model's output should be a well-defined, structured quantity
  (probability, score, ranked list) that can be evaluated, calibrated,
  and tested independently of any language generation.
- If a task feels like it needs an LLM to "decide" something (e.g. judge
  whether a play was good), that's a signal the actual decision needs a
  proper model with a defined target and evaluation, not a prompt. Route
  it back into this skill's modeling workflow instead of reaching for an
  LLM as a decision-maker.
- This split also keeps evaluation honest — `references/evaluation.md`'s
  metrics only make sense against a structured model output, not against
  free text.

## The critical rule

> A live model may never train using information unavailable to the
> player at the equivalent game timestamp.

This is the ML-specific instance of `dota-fairplay`'s core rule, and it's
the single most consequential thing to get wrong here: a leak here
doesn't just hurt accuracy, it turns the product into something that
functions like a cheat, because the model has effectively learned from
hidden information and will reproduce that advantage at inference time.

- Any feature used by a **live** model must be reachable from
  `LIVE_ALLOWED`/`VISIBLE_SCREEN`/`PUBLIC_PREFLIGHT`-classified data only
  (see `dota-fairplay`), evaluated as of the same in-game timestamp the
  live model will see it at inference time.
- Training on full-match/postgame data (fog-of-war-revealing replay
  data, final outcomes, later-game state) is fine for **offline analysis
  or postgame-only models** — it is never fine for a model that will run
  live. See `references/leakage-and-feature-availability.md` for exactly
  how to test this, because "the feature seems fine" is not sufficient
  verification.
- This rule sits above model architecture choice — a leaking Logistic
  Regression is still a violation; a leak-free Transformer would still be
  premature per the complexity rule below, but at least wouldn't be a
  fairness violation. Fix leakage before worrying about model choice.

## Model complexity: start simple, earn complexity

**Preferred initial approaches**, roughly in order of reach for:
- **Logistic Regression** — establish the simplest possible baseline
  first; if it already captures most of the signal, that's valuable
  information, not a disappointment.
- **LightGBM / XGBoost** — gradient-boosted trees, strong default choice
  once a linear baseline is beaten, and interpretable enough to inspect
  feature importance against `dota-domain` expectations.
- **Ranking models** — for anything that's actually a ranking task (e.g.
  "which item is best right now" among several candidates) rather than a
  single-target regression/classification — use a model built for
  ranking, not a workaround bolted onto a classifier.
- **Bayesian shrinkage** — for small-sample-size estimates (e.g. a
  specific hero/item combo with few observed games), shrink toward a
  reasonable prior rather than trusting a noisy raw estimate; this is
  often more valuable than a fancier model when data is sparse, which is
  common for narrow hero/item/matchup slices.

**Do not introduce Transformers, GNNs, or other complex architectures**
until:
1. a simpler baseline (per the list above) has actually been built and
   evaluated — not just assumed to be insufficient;
2. the complex architecture's expected improvement over that baseline is
   articulated concretely (what signal does it capture that the baseline
   structurally cannot?), not just "it might do better."

A complex model that beats a baseline by a marginal amount, at large
cost to interpretability, training complexity, ONNX-exportability, and
inference cost on the player's local machine, is usually a worse choice
for this project even if its raw metric is slightly higher — see
`references/model-selection.md` for how to weigh this tradeoff
concretely rather than defaulting to "bigger model is better."

## Required before any model is considered done

Every model — baseline or otherwise — needs all of the following. Full
detail and checklists in `references/` (linked per item):

1. **A baseline exists and was actually compared against** — see above
   and `references/model-selection.md`.
2. **Temporal validation** — train/validate/test split by time, not
   randomly; see `references/validation-and-calibration.md`.
3. **Feature availability validated** — every feature confirmed
   reachable at the model's intended inference time, per the critical
   rule above; see `references/leakage-and-feature-availability.md`.
4. **Leakage tests pass** — automated tests, not just a manual read-through;
   see `references/leakage-and-feature-availability.md`.
5. **Calibration checked** — a model outputting a probability should
   actually mean that probability; see `references/validation-and-calibration.md`.
6. **Reproducibility** — a documented run (data version, code version,
   hyperparameters, seed) that produces the same model again; see
   `references/reproducibility-and-versioning.md`.
7. **Model versioning** — every shipped model traceable to the exact
   training run/data/code that produced it; see
   `references/reproducibility-and-versioning.md`.
8. **ONNX export, where appropriate** — for any model intended to run
   live in the desktop app (per `dota-architecture`'s `Ml.Inference`
   layer); see `references/onnx-export.md` for when this applies and
   what to verify after export.

## Where to go next

- **`references/model-selection.md`** — baseline-first workflow, the
  preferred model list in more depth, and how to justify (or reject)
  reaching for a more complex architecture.
- **`references/leakage-and-feature-availability.md`** — the critical
  rule in full, concrete leakage patterns specific to Dota match data,
  and how to test for them.
- **`references/validation-and-calibration.md`** — temporal splits,
  cross-validation adapted for temporal data, and calibration checks/
  fixes.
- **`references/reproducibility-and-versioning.md`** — what "reproducible"
  means concretely here, and the model versioning scheme.
- **`references/onnx-export.md`** — when to export, what changes between
  training-time and inference-time model behavior, and export validation.
- **`references/evaluation.md`** — evaluation guidance: which metrics fit
  which task (classification, ranking, calibration), and how "ML decides,
  LLM explains" shapes what counts as a meaningful evaluation.
- **`references/ml-checklists.md`** — pre-training, pre-ship, and
  live-deployment checklists pulling all of the above together.

## Relationship to other skills

- `dota-fairplay` — the source of the critical rule; consult it directly
  for the full classification system when a feature's legitimacy is
  unclear, not just this skill's summary.
- `dota-data` — the RAW→BRONZE→NORMALIZED→FEATURES→DATASET pipeline this
  skill's models are trained from; dataset-level quality rules
  (deduplication, temporal splits, provenance) live there, model-level
  concerns (baseline-first, calibration, versioning) live here.
- `dota-architecture` — `Training`/`Ml.Inference`/`RecommendationEngines`
  layering; this skill governs modeling practice within those layers, not
  the layering itself.
- `dota-domain` — feature importance and model behavior should make
  strategic sense; a model that weights a feature in a way that
  contradicts basic Dota strategy is worth double-checking, not just
  accepting because the metric improved.
