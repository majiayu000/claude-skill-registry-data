---
name: model-building
description: "Trains and validates prediction models for sports game outcomes. Use when user asks about building a prediction model, training a classifier, choosing between logistic regression or XGBoost, model selection, hyperparameter tuning, feature importance, or ensemble methods. Always uses walk-forward methodology -- refuses k-fold. Do not use for feature construction -- see feature-engineering. Do not use for validating probability calibration -- see probability-calibration. Do not use for xG models specifically -- see xg-model-building."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Model Building

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_games` for historical game results (5 credits per query).
> Model training consumes no credits -- credits are spent in data collection and feature engineering upstream.

You are an expert in building sports prediction models. Your goal is to train classifiers that produce honest accuracy estimates on held-out walk-forward test folds. Training accuracy is never reported. Walk-forward test accuracy is the only number that matters.

## When to Use

- User wants to build a model that predicts game outcomes
- User asks which algorithm to use (logistic regression vs random forest vs XGBoost)
- User wants to tune hyperparameters
- User wants to combine multiple models into an ensemble
- User wants to understand which features matter
- User has features ready and wants to train

## When NOT to Use

- Feature construction -- see `feature-engineering`
- Evaluating whether walk-forward methodology is correctly implemented -- see `walk-forward-validation`
- Verifying that predicted probabilities are calibrated -- see `probability-calibration`
- xG (expected goals) models specifically -- see `xg-model-building`
- Finding betting edges from model output -- see `edge-detection`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_games` | Historical results for training data | 5 per season |
| `get_team_stats` | Team stats for feature pipeline | 5 per call |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `train_model` | Train locally using scikit-learn (instructions below) |
| `get_model_accuracy` | Compute from walk-forward predictions manually |
| `get_feature_importance` | Extract from trained model object after fitting |
| `optimize_hyperparameters` | Grid search within walk-forward folds (instructions below) |

## Initial Assessment

Before training, establish:
1. Are features built and audited for leakage? If not, start with `feature-engineering`.
2. How many seasons of historical data are available? (determines fold count)
3. Is the prediction target binary win/loss, or probability, or goal differential?

## How It Works

### Step 1: Start with Logistic Regression

Always start with the simplest model. Logistic regression provides:
- A performance floor to beat
- Interpretable coefficients (which features drive predictions)
- Fast training (iterate quickly)
- A calibration baseline (logistic outputs are well-calibrated by default)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Fit on train only

lr = LogisticRegression(C=1.0, max_iter=1000)
lr.fit(X_train_scaled, y_train)
preds = lr.predict_proba(X_test_scaled)[:, 1]
```

**If logistic regression gets 58% walk-forward accuracy and XGBoost gets 59%, the added complexity is not worth it.** Report logistic regression as the model.

### Step 2: Model Selection Guidance

Progress through this ladder. Move to the next only if walk-forward accuracy improves by at least 1 percentage point.

| Model | When to Use | Key Advantage | Key Risk |
|-------|------------|---------------|----------|
| Logistic Regression | Always start here | Interpretable, calibrated, fast | Linear decision boundary |
| Random Forest | If LR plateau < 60% | Handles non-linearity, robust to outliers | More tuning, less interpretable |
| XGBoost | If RF improves over LR | Highest ceiling on structured data | Overfits on small sports datasets |
| Ensemble (hard vote) | After testing 3+ models | Reduces variance across model types | Complexity; only worthwhile if models are diverse |

### Step 3: Walk-Forward Hyperparameter Tuning

Hyperparameters are tuned using walk-forward folds -- never on the full dataset.

**Correct approach:**
```python
# Tune on inner folds, evaluate on outer test fold
from sklearn.model_selection import TimeSeriesSplit

# Use TimeSeriesSplit within each training fold for HPO
inner_cv = TimeSeriesSplit(n_splits=3)
param_grid = {'n_estimators': [100, 200, 500], 'max_depth': [3, 5, 7], 'learning_rate': [0.05, 0.1, 0.2]}

# Grid search only on training data -- never on test fold
grid_search = GridSearchCV(XGBClassifier(), param_grid, cv=inner_cv, scoring='neg_log_loss')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

**Do not tune hyperparameters by looking at test fold accuracy.** That is test-set snooping. Tune on training folds only, lock parameters, then evaluate on the held-out test fold.

### Step 4: Ensemble Construction

If three or more models each reach 58%+ walk-forward accuracy independently, ensemble them.

**Hard vote beats probability averaging in practice (PuckCast result: +2pp over averaging):**

```python
# Hard vote: majority of models must agree
def hard_vote(preds_list, threshold=0.5):
    votes = [(p > threshold).astype(int) for p in preds_list]
    majority = np.round(np.mean(votes, axis=0))
    return majority

# Probability averaging (often worse):
def avg_proba(preds_list):
    return np.mean(preds_list, axis=0)
```

**Why hard vote wins:** When models disagree on a game, the market is typically pricing in that uncertainty. Disagreement games are lower-confidence bets. Hard vote automatically skips them (no majority = no prediction). Probability averaging smooths disagreements into a low-confidence probability that the model then bets on anyway.

**Diversity requirement:** Models in an ensemble must use zero shared features. Three models with overlapping features do not reduce variance -- they are correlated noise. PuckCast used three fully separate feature sets across its three base models.

### Step 5: Feature Importance Analysis

After each walk-forward fold, extract feature importance:

```python
# XGBoost / Random Forest
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'feature': features, 'importance': importances})
feature_importance_df.sort_values('importance', ascending=False)

# Logistic Regression (use coefficient magnitude)
coef_df = pd.DataFrame({'feature': features, 'coef': np.abs(lr.coef_[0])})
coef_df.sort_values('coef', ascending=False)
```

Aggregate importance across folds. Features that consistently rank in the bottom 10% across all folds are candidates for removal. Remove them and retest -- if walk-forward accuracy holds or improves, they're gone.

**Warning sign:** If a feature shows very high importance (>30% of total) in isolation, inspect it for leakage. Leaky features dominate importance rankings because they carry perfect information.

### Step 6: Overfitting Detection

Compare training accuracy vs walk-forward test accuracy per fold:

| Gap | Interpretation |
|-----|---------------|
| <2pp | No meaningful overfitting |
| 2-5pp | Moderate overfitting -- consider regularization |
| 5-10pp | Significant overfitting -- prune features, increase regularization |
| >10pp | Severe overfitting -- model is memorizing training data |

**For XGBoost:** Increase `min_child_weight`, decrease `max_depth` (try 3-4), add `subsample=0.8`, add `colsample_bytree=0.8`.
**For Random Forest:** Increase `min_samples_leaf`, decrease `max_features`.
**For Logistic Regression:** Decrease `C` (stronger regularization).

### Step 7: Model Persistence

Save: model object, feature pipeline (scaler, encoders), version metadata.

```python
import joblib
import json
from datetime import datetime

# Save model
joblib.dump(model, 'model_v1.pkl')
joblib.dump(scaler, 'scaler_v1.pkl')

# Save metadata
metadata = {
    'version': '1.0',
    'trained_date': datetime.today().isoformat(),
    'train_seasons': ['2019-20', '2020-21', '2021-22', '2022-23'],
    'features': features,
    'walk_forward_accuracy': 0.597,
    'walk_forward_log_loss': 0.670,
    'n_walk_forward_folds': 3,
    'baseline_home_win': 0.548,
    'baseline_market': 0.572
}
with open('model_v1_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

Always version models. When you retrain, increment the version. Keep old models -- if new model underperforms, you roll back.

## Data Source

**PuckAPI (default):** Historical game results via `get_games`. Features already computed upstream via `feature-engineering`. Credits consumed upstream, not here.

**Your own data:** If user provides feature matrix CSV:
1. Verify columns: `game_id`, `game_date`, `season`, all feature columns, `home_win` target
2. Verify data is sorted ascending by game_date
3. Verify no NaN values in feature columns (handle upstream)
4. No credits consumed

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Training and validation | 0 | Local computation; credits consumed in data pipeline |
| `get_games` per season (if pulling here) | 5 | Only if not pulled upstream |

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "90% accuracy on training data" | Meaningless. Training accuracy always inflates -- the model has seen this data. | Report walk-forward test accuracy only. Training accuracy is not in the output. |
| "XGBoost always wins on tabular data" | Start with logistic regression baseline. If the gap is <1pp, the complexity isn't worth it. | Ladder up: LR first, RF second, XGBoost third. |
| "More features = better model" | More features = more overfitting risk on small sports datasets (1,000-5,000 games/season). | Use feature importance to prune. Start with 12 features, add only when walk-forward improves. |
| "My model beats Vegas on this season's data" | Over how many games? What's the CLV? One season is ~1,230 games -- significant at 60% but barely. | Minimum 3 walk-forward folds. Report per-fold. Calculate statistical significance. |
| "Probability averaging is the right ensemble method" | PuckCast tested both. Hard vote on diverse models outperformed probability averaging by 2pp. | Hard vote, zero shared features across base models. |
| "I tuned hyperparameters on the test fold to maximize accuracy" | That is test-set snooping. Your reported accuracy will not generalize. | Tune only on training folds. Lock parameters before touching the test fold. |
| "I'll add more data later to fix overfitting" | More data helps, but overfitting from too many features or too deep trees isn't fixed by data volume. | Regularize the model now. Prune features. |
| "k-fold is fine for model comparison" | k-fold leaks future data into training on time series. Use walk-forward for all evaluation. | Walk-forward for model comparison, not just final evaluation. |

## Output Format

Model building produces:

```
Model Training Report
======================
Model: XGBoost (n_estimators=200, max_depth=4, lr=0.1)
Features: 24 (after pruning 8 low-importance features)
Ensemble: No (single model)

Walk-Forward Results (3 folds):
  Fold 1 (test: 2021-22): train_acc=63.1%, test_acc=59.1%, gap=4.0pp (acceptable)
  Fold 2 (test: 2022-23): train_acc=64.2%, test_acc=61.3%, gap=2.9pp (acceptable)
  Fold 3 (test: 2023-24): train_acc=62.8%, test_acc=58.7%, gap=4.1pp (acceptable)

Mean walk-forward test accuracy: 59.7% (std: ±1.1pp)
Mean log loss: 0.670
Mean Brier score: 0.237

Top 5 Features by Importance:
  1. elo_diff: 18.3%
  2. starter_gsaa_ytd (diff): 14.1%
  3. corsi_pct_roll10 (diff): 11.2%
  4. rest_days (home): 8.7%
  5. goal_diff_roll10 (diff): 7.9%

Baselines beaten:
  Home-win-always (54.8%): YES (+4.9pp)
  Market implied (57.2%): YES (+2.5pp)

Model saved: model_v1.pkl + scaler_v1.pkl + model_v1_metadata.json

Next: probability-calibration to verify probability outputs
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Model trained, want to verify probabilities are accurate | Check calibration curve | `probability-calibration` |
| Want to find betting edges from model output | Compare model probabilities vs market | `edge-detection` |
| Want to test betting strategies historically | Simulate bankroll with historical games | `backtesting` |
| Train accuracy >> test accuracy (>5pp gap) | Overfit -- prune features, add regularization | `feature-engineering` + return here |
| Model doesn't beat baselines | More features needed or different architecture | `feature-engineering` + return here |
| Want to build xG model specifically | Different methodology, shot-level data | `xg-model-building` |
| Need to add Elo as a feature | Build Elo ratings first | `elo-engineering` |
