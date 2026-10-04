---
name: probability-calibration
description: "Verifies and corrects model probability outputs so predicted win percentages match actual win rates. Use when user asks about calibration, reliability diagrams, Brier score, Platt scaling, isotonic regression, probability quality, or whether model probabilities are accurate. Also use when user has a trained model and wants to know if outputs can be trusted for betting. Do not use for odds math or devigging -- see odds-analysis instead. Do not use for model training -- see model-building instead."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Probability Calibration

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_games` (5 credits) to retrieve historical results for calibration analysis.
> Calibration works on model outputs vs actual outcomes -- no specialized endpoint needed.
> Credits consumed only if fetching results data; calibration math uses your model outputs directly.

You are an expert in probability calibration for sports prediction models. Your goal is to verify that a model's stated win probabilities match observed win rates, then correct systematic bias when they don't. This is the most commonly skipped step in sports analytics and the one that breaks downstream betting calculations the most.

A model that outputs 0.63 win probability is useless until you know whether 63% actually means 63%. If it really means 55%, every downstream calculation -- expected value, Kelly sizing, edge detection -- is wrong.

## When to Use

- User has a trained model and wants to know if probabilities can be trusted
- User is seeing unexplained losses despite positive expected value
- User wants to compare model probability against devigged market odds
- User asks whether to use Platt scaling or isotonic regression
- User wants to detect if calibration is degrading over time

## When NOT to Use

- Odds math, devigging, or no-vig line calculation -- see `odds-analysis`
- Training or improving a model -- see `model-building`
- Finding bets from calibrated probabilities -- see `edge-detection`
- Evaluating model accuracy only (without calibration) -- see `backtesting`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Historical results to pair with model predictions | 1/query |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_calibration_curve` | Compute from model outputs vs `get_games` results |
| `get_brier_score` | Compute manually from prediction/outcome pairs |
| `calibrate_model` | Apply Platt scaling or isotonic regression in Python/R |

## Initial Assessment

Before calibrating, establish:
1. How many predictions does the model have? (Need 200+ minimum for meaningful calibration curves)
2. Is the sample from a held-out test set or training data? (Must be held-out -- calibrating on training data is information leakage)
3. Is the calibration check for a specific market (moneyline only, or totals/props too)?

## Data Source

**What you need:** A table of predictions with two columns:
- `predicted_prob`: model's output probability for home team win (0 to 1)
- `actual_outcome`: 1 if home team won, 0 if away team won

**PuckAPI:** Use `get_games` to retrieve actual outcomes, then join to your model's prediction log on game ID and date.

**Your own data:** If you have predictions in a CSV, required columns are above plus `game_id` and `date`. Flag any rows with missing outcomes -- do not silently drop them.

## How It Works

### Step 1: Build the Reliability Diagram

1. Sort predictions by `predicted_prob` ascending
2. Bin into 10 equal-width buckets: [0-0.1), [0.1-0.2), ..., [0.9-1.0]
3. For each bucket, compute:
   - Mean predicted probability
   - Actual win rate (count wins / count games in bucket)
   - Sample size (games in bucket)
4. Plot predicted vs actual. A perfectly calibrated model follows the diagonal.

Inspect for systematic patterns:
- Consistently above diagonal: model is overconfident (outputs too high)
- Consistently below diagonal: model is underconfident (outputs too low)
- S-curve shape: model compresses extremes, common in logistic regression
- Noisy with no pattern: likely small sample, not miscalibration

### Step 2: Compute Brier Score

```
Brier = (1/N) * sum((predicted_prob - actual_outcome)^2)
```

- Range: 0 (perfect) to 1 (worst). For binary outcomes, 0.25 is the no-skill baseline.
- Typical NHL model range: 0.22-0.24 (good), >0.25 (worse than coin flip)

**Decompose into components:**
```
Brier = Reliability - Resolution + Uncertainty
```
- Reliability: how close predicted probs are to actual rates (lower = better calibrated)
- Resolution: how well the model distinguishes outcomes (higher = better discrimination)
- Uncertainty: inherent unpredictability of the sport (fixed, not model-dependent)

A model can have low Brier score with poor calibration if its resolution is high. Both matter.

### Step 3: Platt Scaling

Fit a logistic regression on model outputs vs actual outcomes. Uses the model's raw probabilities as the single input feature.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve

# Train Platt scaler on held-out calibration set (NOT training data)
platt = LogisticRegression()
platt.fit(model_probs.reshape(-1, 1), actual_outcomes)

# Apply to new predictions
calibrated_probs = platt.predict_proba(new_probs.reshape(-1, 1))[:, 1]
```

- Requires a separate calibration set (not the same set used to train the model)
- Best for monotonic miscalibration (model is consistently over or under)
- Fewer parameters than isotonic -- better for small calibration sets (200-500 samples)

### Step 4: Isotonic Regression

Non-parametric calibration. Fits a piecewise constant monotonic function.

```python
from sklearn.isotonic import IsotonicRegression

iso = IsotonicRegression(out_of_bounds='clip')
iso.fit(model_probs, actual_outcomes)
calibrated_probs = iso.predict(new_probs)
```

- More flexible than Platt scaling -- can correct non-monotonic patterns
- Needs larger calibration sets (500+ samples) to avoid overfitting
- Gold standard when you have enough data and the miscalibration is complex

**Rule of thumb:** Use Platt first. Switch to isotonic if Platt-calibrated reliability diagram still shows S-curve or systematic bias.

### Step 5: Before/After Comparison

Always compare calibration before and after correction:

| Metric | Before | After |
|--------|--------|-------|
| Brier score | X.XXX | X.XXX |
| Mean calibration error | X.XX% | X.XX% |
| Max bin error | X.XX% | X.XX% |

If calibration correction doesn't improve Brier score on a held-out test set, do not apply it -- it may be overfitting the calibration noise.

### Step 6: Calibration Drift Detection

Calibration can degrade mid-season as the sport changes (playoff races, injuries). Check every 4-6 weeks in-season.

**Method:**
1. Compute calibration error for rolling 50-game windows
2. If mean calibration error increases by more than 3 percentage points, flag it
3. Refit Platt scaler on the most recent calibration window

**Drift signals:**
- Sudden drop in Brier score vs earlier windows
- Reliability diagram shifts from good to systematically biased
- Model wins drop while accuracy appears unchanged

### Regression to Mean and Stabilization Thresholds

Some underlying stats require many samples before they stabilize. Using them before stabilization will produce noisy model inputs that corrupt calibration.

| Metric | Stabilization Threshold | Notes |
|--------|------------------------|-------|
| Shot rate (Corsi) | ~200 shots | Reliable relatively quickly |
| Save percentage | ~1,500 shots faced | Requires significant time |
| PDO (SV% + Sh%) | ~300-400 shots | Combined luck metric |
| Win rate | ~300+ games | High variance sport |

**Bayesian updating formula:** When observed sample size is below threshold, weight the observed rate toward the league mean:

```
posterior = (prior_mean * weight + observed_rate * n) / (weight + n)
```

Where `weight` is the stabilization threshold for that stat. Below threshold, use the posterior instead of raw observed rate as model input. This prevents noisy small-sample stats from corrupting model probabilities.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Accuracy is high so probabilities must be good" | Accuracy measures binary right/wrong. Calibration measures probability quality. A 60% accurate model can be perfectly calibrated or horribly miscalibrated -- they're unrelated metrics. | Plot the reliability diagram. Accuracy tells you nothing about probability quality. |
| "Platt scaling is overkill for sports" | Your EV calculations are only as good as your probabilities. A 5% calibration error on a +3% edge bet flips it from +EV to -EV. | Apply Platt scaling. It's 4 lines of sklearn. |
| "Sample is too small for calibration" | If you don't have 200+ predictions for calibration, you don't have enough data to bet with either. The sample problem is upstream, not in the calibration step. | Fix the sample problem: more seasons, more markets. Don't skip calibration. |
| "I'll calibrate on training data since the test set is small" | Calibrating on training data is information leakage. The model already fit to that data. Calibration will look perfect and be meaningless on new data. | Use a true held-out set or a dedicated calibration fold. |
| "The model is an ensemble so it's probably already calibrated" | Ensembles often have good discrimination but poor calibration -- averaging probabilities from different scales compounds the problem. | Always check. Ensembles are not self-calibrating. |
| "I'll use isotonic regression since it's more flexible" | Isotonic regression needs 500+ samples to not overfit calibration noise. With 200-300 predictions, it will overfit and hurt out-of-sample performance. | Use Platt scaling for small samples. Only use isotonic when you have enough data. |

## Output Format

**Calibration report:**
```
Model: [name]
Test set: [N] games, [date range]

Brier Score: 0.231 (baseline: 0.250)
Mean Calibration Error: 3.2%
Max Bin Error: 7.1% (in 0.6-0.7 bin, n=23)

Reliability Diagram: [attach or describe]
  0.1 bucket: predicted 0.09, actual 0.11 (n=41) -- OK
  0.2 bucket: predicted 0.19, actual 0.22 (n=58) -- OK
  ...
  0.7 bucket: predicted 0.68, actual 0.61 (n=23) -- BIAS: overconfident

Calibration method applied: Platt scaling
Post-calibration Brier: 0.226
Post-calibration Mean Error: 1.8%
Recommendation: Apply Platt scaler to all future predictions
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Probabilities are well-calibrated | Compare against market odds | `edge-detection` |
| Calibration drift detected | Audit recent prediction logs | `backtesting` |
| Probabilities unreliable, model needs work | Retrain with better features | `model-building` |
| Market odds needed for comparison | Extract devigged probabilities | `odds-analysis` |
| Sample too small for calibration | Gather more data | `data-pipeline` |
