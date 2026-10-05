---
name: hyperparameter-optimization
description: "The search algorithm matters far less than the budget and the space you give it,"
---

# Hyperparameter Optimization (Verbose)

## Core Patterns

### Choosing a Search Strategy

The search algorithm matters far less than the budget and the space you give it,
but the choice still costs or saves hours.

| Strategy | Trials to be useful | Parallel | Best when |
|---|---|---|---|
| Grid search | Exponential in dims | Fully | ≤ 2 params, discrete, small |
| Random search | 30–100 | Fully | Default. Unknown space, cheap fits |
| Successive halving | 100–500 configs | Fully | Fits scale with data or epochs |
| TPE / Bayesian | 50–300 | Partly (sequential bias) | Fits cost minutes+, few params |
| Evolutionary (CMA-ES) | 500+ | Fully | Continuous, smooth, large budget |

Grid search is the default people reach for and it is almost always wrong. A grid
of 4 values across 4 parameters is 256 fits, yet it only ever evaluates 4 distinct
learning rates. Random search spends the same 256 fits on 256 distinct learning
rates. Bergstra & Bengio's 2012 result is that this asymmetry is decisive because
real hyperparameter surfaces have **low effective dimensionality** — a handful of
parameters explain nearly all the variance in the score, and which ones they are
differs by dataset. Random search does not need to know which axis matters; it
resolves all of them at once.

The budget arithmetic is worth memorizing. If the top `p` fraction of the space is
"good enough", `n` random trials miss it with probability `(1 - p)^n`. For `p = 0.05`,
`n = 60` gives `0.95^60 ≈ 0.046` — a 95% chance of a hit, independent of how many
dimensions the space has.

### Defining the Search Space

```python
import optuna

def objective(trial: optuna.Trial) -> float:
    params = {
        # log scale: spans orders of magnitude
        "learning_rate":     trial.suggest_float("learning_rate", 1e-3, 3e-1, log=True),
        "reg_lambda":        trial.suggest_float("reg_lambda", 1e-3, 1e2, log=True),
        # linear scale: bounded, roughly uniform effect
        "subsample":         trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree":  trial.suggest_float("colsample_bytree", 0.4, 1.0),
        "max_depth":         trial.suggest_int("max_depth", 3, 12),
        "booster":           trial.suggest_categorical("booster", ["gbtree", "dart"]),
    }
    scores = cross_val_score(make_model(**params), X, y,
                             cv=StratifiedKFold(5, shuffle=True, random_state=0),
                             scoring="neg_log_loss", n_jobs=-1)
    return scores.mean()
```

Two rules do most of the work:

1. **Log-scale anything that spans decades.** Learning rate, `C`, `alpha`,
   `reg_lambda`, `min_child_weight`. Sampling `learning_rate` uniformly on
   `[1e-5, 1e-1]` places 99% of draws above `1e-3` — the small end is never seen.
2. **Widen when the optimum lands on a boundary.** If the best trial chose
   `max_depth = 12` and 12 is your ceiling, the true optimum is outside the range.
   Re-run with the range extended rather than accepting the edge.

Tune few things. For gradient boosting, learning rate, depth, and one
regularization term account for most achievable gain; `n_estimators` should be
handled by early stopping, not searched.

### Nested Cross-Validation and Honest Estimates

This is the pattern most tuning code gets wrong. Selection is itself a fitting
procedure: choosing the best of 200 configs by validation score is fitting 200
models' worth of choices to that validation data. The winner's score is therefore
biased upward — it contains the config's true quality *plus* however much noise
happened to favor it.

```python
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_val_score

inner_cv = KFold(n_splits=5, shuffle=True, random_state=0)
outer_cv = KFold(n_splits=5, shuffle=True, random_state=1)

search = RandomizedSearchCV(model, param_distributions=space,
                            n_iter=40, cv=inner_cv, scoring="neg_log_loss")

# Tuning is re-run inside every outer fold, on that fold's training data only.
generalization = cross_val_score(search, X, y, cv=outer_cv, scoring="neg_log_loss")
print(generalization.mean(), generalization.std())
```

`search.best_score_` is a **selection** score and must never be reported as
performance. `generalization.mean()` is the number that belongs in the writeup.
On a few thousand rows with a wide search the gap is routinely 1–3 points of AUC.

Nested CV costs `outer × inner × n_iter` fits. When that is unaffordable, the
cheap substitute is a three-way split — train, validation, test — where the test
set is opened exactly once, after every decision is frozen. "Once" is literal: if
you look at test, change something, and look again, it is a validation set now and
your honest estimate is gone.

### Early Stopping and Pruning

```python
study = optuna.create_study(
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=0),
    pruner=optuna.pruners.MedianPruner(n_startup_trials=10, n_warmup_steps=5),
)

def objective(trial):
    model = build(trial)
    for epoch in range(100):
        model.partial_fit(X_tr, y_tr)
        score = model.score(X_val, y_val)
        trial.report(score, step=epoch)
        if trial.should_prune():          # worse than median at this step
            raise optuna.TrialPruned()
    return score
```

For estimators without an epoch loop, successive halving budgets on sample count
instead:

```python
from sklearn.experimental import enable_halving_search_cv  # noqa: F401
from sklearn.model_selection import HalvingRandomSearchCV

search = HalvingRandomSearchCV(model, space, factor=3,
                               resource="n_samples", cv=5, random_state=0)
```

`factor=3` keeps the top third each round and triples their budget. The tradeoff
is real: a config that is mediocre on 10% of the data but excellent on all of it
gets killed early. Set `min_resources` high enough that the first rung is
informative.

### Reporting and Reproducibility

Persist the study, not just the winner. `optuna.create_study(storage=...,
study_name=..., load_if_exists=True)` lets a search resume and lets you inspect
the whole surface afterward — `optuna.importance.get_param_importances(study)`
tells you which parameters actually mattered, which is how you shrink the space
for the next round.

Log the seed, the CV splitter, the metric, the library versions, and the number of
trials alongside the score. Without the trial count the score is uninterpretable:
"0.91 AUC" from 5 trials and from 500 trials are different claims about the same
number.

## Common Anti-Patterns

❌ **Reporting `best_score_` as model performance.** It is the maximum over many
noisy estimates and is biased upward by exactly the amount you searched.
✅ Report a nested-CV score, or a held-out test set touched once.

❌ **Tuning by repeatedly checking the test set.** Slow-motion overfitting; the
test set decays into a validation set and nothing is left to measure with.
✅ Freeze test until every decision is final. If you must peek, budget the number
of peeks in advance and treat the estimate as optimistic.

❌ **Uniform sampling of learning rate or regularization strength.**
✅ `log=True` / `loguniform` for anything spanning more than one decade.

❌ **Grid search over five or more parameters.** The budget goes into resolving
axes that do not affect the score.
✅ Random or TPE, then a small grid refinement around the region that won.

❌ **Preprocessing fitted on the full dataset before CV.** A `StandardScaler` or
`SelectKBest` fitted outside the loop leaks validation-fold statistics into
training.
✅ Put every fitted transform inside a `Pipeline` and pass the pipeline to the
search.

❌ **Picking the config with the highest mean and ignoring the spread.** A 0.002
lead with a fold std of 0.02 is a coin flip.
✅ Prefer the simplest config within one standard error of the best.

❌ **Random `KFold` on time-ordered data.** Future rows train the model that
predicts the past.
✅ `TimeSeriesSplit`, and see time-series-preprocessing for the leakage rules.

❌ **Searching `n_estimators` for boosted trees.**
✅ Set it high and use early stopping on a validation fold; search the parameters
that change the model's shape instead.

## Hyperparameter Optimization Checklist

- [ ] Random or Bayesian search chosen over grid for > 2 parameters
- [ ] Scale-sensitive parameters sampled in log space
- [ ] Search ranges wide enough that the winner is not on a boundary
- [ ] All preprocessing inside a `Pipeline`, fitted per fold
- [ ] CV splitter matches the data structure (stratified / grouped / time-ordered)
- [ ] Nested CV or a once-touched test set provides the reported number
- [ ] `best_score_` never reported as generalization performance
- [ ] Trial count, seed, metric, and library versions logged with the result
- [ ] Pruning or successive halving enabled when fits are iterative or expensive
- [ ] Fold standard deviation compared against the margin between top configs
- [ ] Parameter importances reviewed to shrink the space for the next round
- [ ] Final model refit on train+validation with the selected configuration
