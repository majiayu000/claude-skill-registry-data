---
name: ml-engineering
version: 1.0.0
author: Param
description: Enforces rigorous ML modeling, feature engineering, training, and evaluation standards at principal-engineer level.
applies-to: .py, .ipynb, ML training scripts, feature pipelines, model evaluation, inference services
---

## Intent

This skill transforms every ML task from "code that runs" into "code that can be trusted." It mandates reproducibility by default, forces explicit reasoning at every modeling decision, prevents the most common forms of data leakage and metric gaming, and ensures that every model shipped is accompanied by the infrastructure needed to catch it when it fails. Loading this skill means no ML code leaves the session without a defined objective metric, a baseline comparison, and a monitoring plan.

See also: [`python-excellence/SKILL.md`](../python-excellence/SKILL.md) for all code style, typing, and formatting rules that apply to ML code as well.

---

## 1. Modeling Philosophy

**Always define three things before writing a single line of model code:**
1. The objective metric (what does "better" mean, in a single number?)
2. The baseline (what does a naive model score on that metric?)
3. The failure modes (what does bad model behavior look like, and what are the consequences?)

**Always start with the simplest model that could work.** Logistic regression before gradient boosting. Linear regression before neural networks. Complexity must be justified in a comment with: what simpler model was tried, what its score was, and why the added complexity is worth the cost.

**Every model file must have a module-level docstring describing:**
- What it predicts (the target variable, its type, its range)
- What features it consumes (reference the feature registry)
- What it outputs (probabilities, scores, labels, embeddings — specify)
- Known limitations and failure modes
- The domain context that makes this model valid

**Always prefer interpretability over marginal accuracy gains** unless the domain explicitly requires otherwise. Document the interpretability trade-off in a comment when choosing a black-box model.

---

## 2. Feature Engineering Standards

**Every feature must be registered.** Use a dataclass or Pydantic model as a feature registry entry. At minimum:

```python
@dataclass
class Feature:
    name: str
    dtype: str            # "float32", "int64", "category", etc.
    description: str      # What does this feature represent?
    source: str           # Which table/system/pipeline produces it?
    nullable: bool        # Can this be missing at inference time?
    point_in_time: str    # What timestamp logic governs its availability?
```

Never add a feature without a registry entry. Never use a feature whose `point_in_time` logic is undocumented.

**Leakage prevention is mandatory.** Before finalizing any feature set:
- Assert that no feature uses information that would be unavailable at inference time
- Document the point-in-time join logic explicitly — what timestamp is the cutoff?
- Any feature computed from future data relative to the prediction target must be flagged and removed
- Add a comment above any temporally sensitive feature: `# Point-in-time safe: computed from data available as of event_timestamp`

**Categorical encoding choices must be justified in a comment:**
- Ordinal encoding: only when the categories have a meaningful order
- One-hot encoding: for low-cardinality nominals with no order
- Target encoding: only with proper cross-validation to prevent leakage; document the folds used
- Embedding: for high-cardinality categoricals; document the embedding dimension choice

**Always handle missing values explicitly.** Never use `.fillna(0)` without a comment explaining why zero is semantically correct for that feature. Document the imputation strategy and its assumptions.

---

## 3. Training Loop Requirements

**Every training script must, without exception:**
1. Set a global random seed for Python, NumPy, and the framework (PyTorch, TensorFlow, JAX) at the top
2. Log all hyperparameters to the experiment tracker before training begins
3. Save the best checkpoint by validation metric (not the last epoch)
4. Produce a reproducibility report: git hash, random seed, library versions, data hash, training duration

**Always use early stopping with patience.** Never hard-code epoch counts without a comment justifying the fixed number (e.g., "fixed at 100 epochs: convergence confirmed across 5 runs; see experiment run xyz-123").

**Always split: train / validation / test.** The test set is touched exactly once: at final evaluation before deployment. Any hyperparameter tuning or architecture selection is done on the validation set. Document the split ratios and the splitting strategy.

**Cross-validation strategy must match the data distribution:**
- Time-series data: always use `TimeSeriesSplit` or a custom walk-forward split — never random shuffle
- Grouped data (multiple observations per entity): always use `GroupKFold` to prevent entity leakage across folds
- Stratified data: use `StratifiedKFold` for classification with class imbalance
- Document the chosen strategy and why it matches the data generating process

**Log these metrics at every epoch/iteration to the experiment tracker:**
- Training loss
- Validation loss
- Primary evaluation metric on validation set
- Learning rate (if dynamic)
- Gradient norm (for deep learning)

---

## 4. Evaluation Standards

**Always report multiple metrics. Never report only accuracy.**

For classification problems, always report:
- Precision, Recall, F1-score (per class and macro/weighted)
- AUC-ROC (for binary and one-vs-rest multi-class)
- AUC-PR (especially important for imbalanced datasets)
- Calibration curve (are predicted probabilities reliable?)
- Confusion matrix (mandatory; analyze the most common error types)
- Brier score (for probabilistic predictions)

For regression problems, always report:
- MAE (mean absolute error — interpretable in target units)
- RMSE (penalizes large errors — sensitive to outliers)
- MAPE (relative error — use only when zero values are impossible)
- R² (proportion of variance explained)
- Residual plots (residuals vs. predicted, residuals vs. each key feature)
- Error distribution (is the error Gaussian? Are there systematic biases?)

For ranking and recommendation problems, always report:
- NDCG@k (normalized discounted cumulative gain at k)
- MRR (mean reciprocal rank)
- Hit Rate@k / Recall@k
- Precision@k
- Coverage and diversity metrics where applicable

**Always compare against a naive baseline.** The baseline must be defined before model training begins:
- Classification: most-frequent class predictor, or random with class proportions
- Regression: mean predictor or median predictor
- Time-series: last-value predictor or seasonal naive
- Ranking: popularity-based ranking

**Error analysis is mandatory for classification tasks.** After generating predictions:
- Identify the top-k most confidently wrong predictions
- Identify systematic patterns in errors (are errors concentrated in a subgroup, time period, or feature range?)
- Document findings in a comment block or evaluation report

---

## 5. Code Patterns to Enforce

**Use dataclasses or Pydantic for all hyperparameter configs. Never pass raw dicts.**

```python
# WRONG
train_model(params={"lr": 0.01, "batch_size": 32, "dropout": 0.3})

# CORRECT
@dataclass
class TrainingConfig:
    learning_rate: float = 0.01
    batch_size: int = 32
    dropout_rate: float = 0.3
    max_epochs: int = 100
    early_stopping_patience: int = 10
    random_seed: int = 42

train_model(config=TrainingConfig())
```

**Always use Pipelines.** Use `sklearn.pipeline.Pipeline` or an equivalent abstraction to chain preprocessing and modeling steps. Never apply transformations outside a pipeline in training code.

**Always save the full pipeline, not just the model.** The serialized artifact must include:
- All preprocessing steps (scalers, encoders, imputers)
- The model itself
- The feature names and expected dtypes
- The training config

```python
# WRONG — scaler is lost, inference will be wrong
joblib.dump(model, "model.pkl")

# CORRECT
pipeline = Pipeline([("scaler", scaler), ("model", model)])
mlflow.sklearn.log_model(pipeline, "model", input_example=X_val[:5])
```

**Use full type hints everywhere.** ML code is notoriously untyped. Every function must have annotated parameters and return types. For NumPy arrays, use `npt.NDArray[np.float32]` style annotations.

---

## 6. Advanced ML Patterns

**Time-series modeling:**
- Always check for stationarity (ADF test or KPSS); document the result
- Handle seasonality explicitly: document period, decomposition strategy, and whether it is additive or multiplicative
- Document the forecasting horizon (how far ahead?), the prediction cadence (how often?), and the retraining frequency
- Never use future observations as features without explicit documentation of the lookahead

**Embeddings:**
- Document the choice of embedding dimension and the reasoning (rule of thumb: 4th root of cardinality, or domain-justified)
- Document the distance metric used in downstream tasks (cosine vs. Euclidean vs. dot product) and why
- Document how embeddings are updated (frozen, fine-tuned, retrained from scratch) and the policy for refreshing them

**Transformer models:**
- Document the attention mask logic explicitly — what tokens are masked, why, and what the padding strategy is
- Document the tokenization scheme and vocabulary size
- Document the maximum sequence length and what happens when inputs exceed it (truncation, chunking)
- Never leave positional encoding implicit — document absolute vs. relative vs. RoPE choice

**Recommendation systems:**
- Document the cold-start handling strategy explicitly: what happens for new users, new items, or both?
- Document the feedback type (explicit ratings vs. implicit clicks) and the assumptions this imposes
- Document the exposure bias and any debiasing strategy applied

**Multi-task learning:**
- Document the task weighting rationale (fixed weights, uncertainty weighting, gradient normalization)
- Log per-task losses separately in the experiment tracker
- Document which tasks share parameters and which have task-specific heads

---

## 7. Anti-Patterns — Always Refuse These

**Never fit a scaler, encoder, or imputer on the full dataset before train/test splitting.** This is data leakage. Always fit on training data only, then transform validation and test data.

```python
# FORBIDDEN — leaks test statistics into training
scaler.fit(X)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# CORRECT
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Never use `.fillna(0)` without a justifying comment.** Zero is semantically meaningful for many features and may introduce bias.

**Never ignore class imbalance.** At minimum, document the class distribution and choose a deliberate strategy: oversampling, undersampling, class weights, or threshold adjustment. Document the chosen strategy and why.

**Never deploy a model without a monitoring plan.** Before any model ships, define:
- Which input features to monitor for drift (PSI, KS test, or equivalent)
- Which output metrics to monitor (predicted distribution, business KPIs)
- What triggers a retraining run (threshold-based, schedule-based, or manual)
- Who owns the retraining decision

**Never use the test set for anything other than final evaluation.** No hyperparameter tuning, no architecture selection, no feature selection based on test set performance. Violation of this rule invalidates all reported results.

**Never report a model's performance without a confidence interval or statistical significance test** when the evaluation set is small enough that variance matters.
