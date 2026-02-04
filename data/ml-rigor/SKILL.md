---
name: ml-rigor
description: Enforces baseline comparisons, cross-validation, interpretation, and leakage prevention for ML pipelines
---

# Machine Learning Rigor Patterns

## When to Use

Load this skill when building machine learning models. Every ML pipeline must demonstrate:
- **Baseline comparison**: Beat a dummy model before claiming success
- **Cross-validation**: Report variance, not just a single score
- **Interpretation**: Explain what the model learned
- **Leakage prevention**: Ensure no future information leaks into training

**Quality Gate**: ML findings without baseline comparison or cross-validation are marked as "Exploratory" in reports.

---

## 1. Baseline Requirements

**Every model must be compared to baselines.** A model that can't beat a dummy classifier isn't learning anything useful.

### Always Compare To:
1. **DummyClassifier/DummyRegressor** - The absolute minimum bar
2. **Simple linear model** - LogisticRegression or LinearRegression
3. **Domain heuristic** (if available) - Rule-based approach

### Baseline Code Template

```python
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import cross_val_score
import numpy as np

print("[DECISION] Establishing baselines before training complex models")

# Classification baselines
dummy_clf = DummyClassifier(strategy='most_frequent')
dummy_scores = cross_val_score(dummy_clf, X_train, y_train, cv=5, scoring='accuracy')
print(f"[METRIC:baseline_accuracy] {dummy_scores.mean():.3f} (majority class)")
print(f"[METRIC:baseline_accuracy_std] {dummy_scores.std():.3f}")

# Simple linear baseline
lr = LogisticRegression(max_iter=1000, random_state=42)
lr_scores = cross_val_score(lr, X_train, y_train, cv=5, scoring='accuracy')
print(f"[METRIC:linear_baseline_accuracy] {lr_scores.mean():.3f}")
print(f"[METRIC:linear_baseline_accuracy_std] {lr_scores.std():.3f}")

# For regression tasks
dummy_reg = DummyRegressor(strategy='mean')
dummy_rmse = cross_val_score(dummy_reg, X_train, y_train, cv=5, 
                              scoring='neg_root_mean_squared_error')
print(f"[METRIC:baseline_rmse] {-dummy_rmse.mean():.3f} (mean predictor)")
```

### Improvement Over Baseline with CI

```python
from scipy import stats

# Calculate improvement with confidence interval
model_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
improvement = model_scores.mean() - dummy_scores.mean()

# Bootstrap CI for improvement
n_bootstrap = 1000
improvements = []
for _ in range(n_bootstrap):
    idx = np.random.choice(len(model_scores), len(model_scores), replace=True)
    boot_improvement = model_scores[idx].mean() - dummy_scores[idx].mean()
    improvements.append(boot_improvement)

ci_low, ci_high = np.percentile(improvements, [2.5, 97.5])

print(f"[METRIC:improvement_over_baseline] {improvement:.3f}")
print(f"[STAT:ci] 95% CI [{ci_low:.3f}, {ci_high:.3f}]")
print(f"[STAT:effect_size] Relative improvement: {improvement/dummy_scores.mean()*100:.1f}%")

if ci_low > 0:
    print("[FINDING] Model significantly outperforms baseline")
else:
    print("[LIMITATION] Improvement over baseline not statistically significant")
```

---

## 2. Cross-Validation Requirements

**Never report a single train/test split.** Cross-validation shows how much your score varies.

### Requirements:
- Use **stratified K-fold** for classification (preserves class distribution)
- Report **mean +/- std**, not just mean
- Calculate **confidence interval** for mean performance
- Use **repeated CV** for small datasets

### Cross-Validation Code Template

```python
from sklearn.model_selection import (
    StratifiedKFold, cross_val_score, cross_validate,
    RepeatedStratifiedKFold
)
import numpy as np
from scipy import stats

print("[DECISION] Using 5-fold stratified CV to estimate model performance")

# Stratified K-Fold for classification
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Multiple metrics
scoring = ['accuracy', 'f1_weighted', 'roc_auc']
cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring, 
                            return_train_score=True)

# Report mean +/- std (REQUIRED)
for metric in scoring:
    test_scores = cv_results[f'test_{metric}']
    train_scores = cv_results[f'train_{metric}']
    
    print(f"[METRIC:cv_{metric}_mean] {test_scores.mean():.3f}")
    print(f"[METRIC:cv_{metric}_std] {test_scores.std():.3f}")
    
    # Check for overfitting
    gap = train_scores.mean() - test_scores.mean()
    if gap > 0.1:
        print(f"[LIMITATION] Train-test gap of {gap:.3f} suggests overfitting")
```

### Confidence Interval for CV Mean

```python
# CI for cross-validation mean (t-distribution for small n)
def cv_confidence_interval(scores, confidence=0.95):
    n = len(scores)
    mean = scores.mean()
    se = stats.sem(scores)
    h = se * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean - h, mean + h

ci_low, ci_high = cv_confidence_interval(cv_results['test_accuracy'])
print(f"[STAT:ci] 95% CI for accuracy: [{ci_low:.3f}, {ci_high:.3f}]")

# For small datasets, use repeated CV
print("[DECISION] Using repeated CV for more stable estimates")
rcv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
scores = cross_val_score(model, X, y, cv=rcv, scoring='accuracy')
print(f"[METRIC:repeated_cv_mean] {scores.mean():.3f}")
print(f"[METRIC:repeated_cv_std] {scores.std():.3f}")
```

---

## 3. Hyperparameter Tuning

**Avoid overfitting to the validation set.** Report the distribution of scores, not just the best.

### Requirements:
- Use **RandomizedSearchCV** or **Bayesian optimization** (Optuna)
- Report **distribution of scores** across parameter combinations
- Use **nested CV** to get unbiased performance estimate
- Watch for **overfitting to validation set**

### RandomizedSearchCV Template

```python
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from scipy.stats import uniform, randint
import numpy as np

print("[DECISION] Using RandomizedSearchCV with 100 iterations")

# Define parameter distributions (not just lists!)
param_distributions = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

random_search = RandomizedSearchCV(
    model, param_distributions,
    n_iter=100,
    cv=5,
    scoring='accuracy',
    random_state=42,
    return_train_score=True,
    n_jobs=-1
)

random_search.fit(X_train, y_train)

# Report distribution of scores (not just best!)
cv_results = random_search.cv_results_
all_test_scores = cv_results['mean_test_score']
all_train_scores = cv_results['mean_train_score']

print(f"[METRIC:tuning_best_score] {random_search.best_score_:.3f}")
print(f"[METRIC:tuning_score_range] [{all_test_scores.min():.3f}, {all_test_scores.max():.3f}]")
print(f"[METRIC:tuning_score_std] {all_test_scores.std():.3f}")

# Check for overfitting during tuning
best_idx = random_search.best_index_
train_test_gap = all_train_scores[best_idx] - all_test_scores[best_idx]
if train_test_gap > 0.1:
    print(f"[LIMITATION] Best model shows {train_test_gap:.3f} train-test gap")
```

### Nested Cross-Validation (Unbiased Estimate)

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

print("[DECISION] Using nested CV for unbiased performance estimate")

# Outer CV for performance estimation
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Inner CV is handled by RandomizedSearchCV
inner_search = RandomizedSearchCV(
    model, param_distributions,
    n_iter=50,
    cv=3,  # Inner CV
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

# Nested CV scores
nested_scores = cross_val_score(inner_search, X, y, cv=outer_cv, scoring='accuracy')

print(f"[METRIC:nested_cv_mean] {nested_scores.mean():.3f}")
print(f"[METRIC:nested_cv_std] {nested_scores.std():.3f}")
print(f"[STAT:ci] 95% CI [{nested_scores.mean() - 1.96*nested_scores.std()/np.sqrt(5):.3f}, "
      f"{nested_scores.mean() + 1.96*nested_scores.std()/np.sqrt(5):.3f}]")
```

---

## 4. Calibration Requirements

**Probability predictions must be calibrated.** A 70% confidence should be correct 70% of the time.

### Requirements:
- Check **calibration curve** for probability predictions
- Report **Brier score** (lower is better)
- Apply **calibration** if needed (Platt scaling, isotonic regression)

### Calibration Code Template

```python
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
import matplotlib.pyplot as plt

print("[DECISION] Checking probability calibration")

# Get probability predictions
y_prob = model.predict_proba(X_test)[:, 1]

# Brier score (0 = perfect, 1 = worst)
brier = brier_score_loss(y_test, y_prob)
print(f"[METRIC:brier_score] {brier:.4f}")

# Calibration curve
prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)

# Plot calibration curve
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot([0, 1], [0, 1], 'k--', label='Perfectly calibrated')
ax.plot(prob_pred, prob_true, 's-', label=f'Model (Brier={brier:.3f})')
ax.set_xlabel('Mean predicted probability')
ax.set_ylabel('Fraction of positives')
ax.set_title('Calibration Curve')
ax.legend()
plt.savefig('figures/calibration_curve.png', dpi=150, bbox_inches='tight')
print("[ARTIFACT:figure] figures/calibration_curve.png")

# Check calibration quality
max_calibration_error = np.max(np.abs(prob_true - prob_pred))
print(f"[METRIC:max_calibration_error] {max_calibration_error:.3f}")

if max_calibration_error > 0.1:
    print("[LIMITATION] Model probabilities are poorly calibrated")
```

### Apply Calibration

```python
print("[DECISION] Applying isotonic calibration to improve probability estimates")

# Calibrate using held-out data
calibrated_model = CalibratedClassifierCV(model, method='isotonic', cv=5)
calibrated_model.fit(X_train, y_train)

# Compare before/after
y_prob_calibrated = calibrated_model.predict_proba(X_test)[:, 1]
brier_calibrated = brier_score_loss(y_test, y_prob_calibrated)

print(f"[METRIC:brier_before_calibration] {brier:.4f}")
print(f"[METRIC:brier_after_calibration] {brier_calibrated:.4f}")
print(f"[METRIC:calibration_improvement] {brier - brier_calibrated:.4f}")
```

---

## 5. Interpretation Requirements

**Explain what the model learned.** Black boxes are not acceptable for important decisions.

### Requirements:
- Compute **permutation importance** or **SHAP values**
- Show at least one **case study** (why this specific prediction?)
- Verify features make **domain sense**

### Permutation Importance Template

```python
from sklearn.inspection import permutation_importance
import pandas as pd

print("[DECISION] Computing permutation importance on test set")

# Permutation importance (more reliable than built-in feature_importances_)
perm_importance = permutation_importance(
    model, X_test, y_test, 
    n_repeats=30, 
    random_state=42,
    n_jobs=-1
)

# Create importance DataFrame
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance_mean': perm_importance.importances_mean,
    'importance_std': perm_importance.importances_std
}).sort_values('importance_mean', ascending=False)

# Report top features
print("[METRIC:top_features]")
for i, row in importance_df.head(5).iterrows():
    print(f"  {row['feature']}: {row['importance_mean']:.4f} (+/- {row['importance_std']:.4f})")

# Check for unexpected features
print("[CHECK:domain_sense] Verify top features align with domain knowledge")
```

### SHAP Values Template

```python
import shap

print("[DECISION] Using SHAP for model interpretation")

# Create explainer
explainer = shap.TreeExplainer(model)  # or shap.KernelExplainer for any model
shap_values = explainer.shap_values(X_test)

# Global importance
shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
plt.savefig('figures/shap_summary.png', dpi=150, bbox_inches='tight')
print("[ARTIFACT:figure] figures/shap_summary.png")

# Mean absolute SHAP values
if isinstance(shap_values, list):  # Multi-class
    shap_importance = np.abs(shap_values[1]).mean(axis=0)
else:
    shap_importance = np.abs(shap_values).mean(axis=0)

top_features = sorted(zip(feature_names, shap_importance), 
                     key=lambda x: x[1], reverse=True)[:5]
print("[METRIC:shap_top_features]")
for feat, imp in top_features:
    print(f"  {feat}: {imp:.4f}")
```

### Case Study (Individual Prediction)

```python
print("[DECISION] Analyzing individual prediction for interpretability")

# Select an interesting case (e.g., high confidence wrong prediction)
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)
mistakes = (y_pred != y_test)
high_conf_mistakes = mistakes & (np.abs(y_pred_proba - 0.5) > 0.4)

if high_conf_mistakes.any():
    case_idx = np.where(high_conf_mistakes)[0][0]
    print(f"[ANALYSIS] Case study: High-confidence mistake (index {case_idx})")
    print(f"  Predicted: {y_pred[case_idx]} (prob={y_pred_proba[case_idx]:.3f})")
    print(f"  Actual: {y_test.iloc[case_idx]}")
    
    # SHAP for this case
    shap.force_plot(explainer.expected_value[1] if isinstance(explainer.expected_value, list) 
                    else explainer.expected_value,
                    shap_values[case_idx] if not isinstance(shap_values, list) 
                    else shap_values[1][case_idx],
                    X_test.iloc[case_idx],
                    matplotlib=True, show=False)
    plt.savefig('figures/case_study_shap.png', dpi=150, bbox_inches='tight')
    print("[ARTIFACT:figure] figures/case_study_shap.png")
    print("[LIMITATION] Model fails on cases with pattern: [describe pattern]")
```

---

## 6. Error Analysis

**Understand where and why the model fails.** Aggregate metrics hide important failure modes.

### Requirements:
- **Slice performance** by key segments (demographics, time periods, etc.)
- Analyze **failure modes** (false positives vs false negatives)
- Check for **systematic errors** (biases, subgroup issues)

### Error Analysis Code Template

```python
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np

print("[DECISION] Performing error analysis across segments")

y_pred = model.predict(X_test)

# Overall confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("[METRIC:confusion_matrix]")
print(cm)

# Classification report
print("[ANALYSIS] Classification report:")
print(classification_report(y_test, y_pred, target_names=class_names))
```

### Slice Performance Analysis

```python
print("[DECISION] Analyzing performance by key segments")

# Create test DataFrame with predictions
test_df = X_test.copy()
test_df['y_true'] = y_test.values
test_df['y_pred'] = y_pred

# Define segments to analyze
segments = {
    'age_group': pd.cut(test_df['age'], bins=[0, 30, 50, 100], labels=['young', 'middle', 'senior']),
    'income_tier': pd.qcut(test_df['income'], q=3, labels=['low', 'medium', 'high'])
}

print("[METRIC:slice_performance]")
for segment_name, segment_values in segments.items():
    test_df['segment'] = segment_values
    
    for segment_val in segment_values.unique():
        mask = test_df['segment'] == segment_val
        if mask.sum() > 10:  # Only report if enough samples
            segment_accuracy = (test_df.loc[mask, 'y_true'] == test_df.loc[mask, 'y_pred']).mean()
            print(f"  {segment_name}={segment_val}: accuracy={segment_accuracy:.3f} (n={mask.sum()})")
            
            # Check for underperformance
            if segment_accuracy < overall_accuracy - 0.1:
                print(f"  [LIMITATION] Model underperforms on {segment_name}={segment_val}")
```

### Failure Mode Analysis

```python
print("[DECISION] Analyzing failure modes")

# Separate false positives and false negatives
fp_mask = (y_pred == 1) & (y_test == 0)
fn_mask = (y_pred == 0) & (y_test == 1)

print(f"[METRIC:false_positive_rate] {fp_mask.mean():.3f}")
print(f"[METRIC:false_negative_rate] {fn_mask.mean():.3f}")

# Analyze characteristics of errors
if fp_mask.sum() > 0:
    print("[ANALYSIS] False positive characteristics:")
    fp_data = X_test[fp_mask]
    for col in feature_names[:5]:  # Top features
        print(f"  {col}: mean={fp_data[col].mean():.3f} vs overall={X_test[col].mean():.3f}")

# Check for systematic bias
print("[CHECK:systematic_error] Review if errors correlate with protected attributes")
```

---

## 7. Leakage Checklist

**Data leakage silently destroys model validity.** Check these BEFORE trusting any results.

### Checklist:
- [ ] **Time-based splits** for temporal data (no future information)
- [ ] **No target information** in features (derived features, proxies)
- [ ] **Preprocessing inside CV** loop (no fit on test data)
- [ ] **Group-aware splits** if samples are related (same user, same session)

### Time-Based Split Template

```python
from sklearn.model_selection import TimeSeriesSplit

print("[DECISION] Using time-based split for temporal data")

# Check if data has temporal component
if 'date' in df.columns or 'timestamp' in df.columns:
    print("[CHECK:temporal_leakage] Using TimeSeriesSplit to prevent future information leak")
    
    # Sort by time
    df_sorted = df.sort_values('date')
    
    # Time-based cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    for fold, (train_idx, test_idx) in enumerate(tscv.split(df_sorted)):
        train_max_date = df_sorted.iloc[train_idx]['date'].max()
        test_min_date = df_sorted.iloc[test_idx]['date'].min()
        
        if train_max_date >= test_min_date:
            print(f"[ERROR] Fold {fold}: Data leakage detected!")
        else:
            print(f"[CHECK:fold_{fold}] Train ends {train_max_date}, Test starts {test_min_date} - OK")
else:
    print("[LIMITATION] No temporal column found - using random split")
```

### Target Leakage Detection

```python
print("[CHECK:target_leakage] Checking for target information in features")

# Check correlation between features and target
correlations = X_train.corrwith(pd.Series(y_train, index=X_train.index))
high_corr_features = correlations[correlations.abs() > 0.9].index.tolist()

if high_corr_features:
    print(f"[WARNING] Suspiciously high correlations with target:")
    for feat in high_corr_features:
        print(f"  {feat}: r={correlations[feat]:.3f}")
    print("[LIMITATION] Review these features for potential target leakage")
else:
    print("[CHECK:target_leakage] No obvious target leakage detected")

# Check for post-hoc features (created after the outcome)
print("[CHECK:feature_timing] Verify all features are available at prediction time")
```

### Preprocessing Inside CV Template

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

print("[DECISION] Using Pipeline to prevent preprocessing leakage")

# WRONG: Fitting scaler on all data before CV
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)  # LEAKAGE!
# scores = cross_val_score(model, X_scaled, y, cv=5)

# CORRECT: Preprocessing inside pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', model)
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"[METRIC:cv_accuracy_mean] {scores.mean():.3f}")
print(f"[METRIC:cv_accuracy_std] {scores.std():.3f}")
print("[CHECK:preprocessing_leakage] Scaler fit inside CV - no leakage")
```

### Group-Aware Splitting

```python
from sklearn.model_selection import GroupKFold

print("[CHECK:group_leakage] Checking if samples are related")

# If samples belong to groups (e.g., multiple records per user)
if 'user_id' in df.columns:
    print("[DECISION] Using GroupKFold to prevent group leakage")
    
    groups = df['user_id']
    gkf = GroupKFold(n_splits=5)
    
    scores = cross_val_score(model, X, y, cv=gkf, groups=groups, scoring='accuracy')
    print(f"[METRIC:group_cv_accuracy_mean] {scores.mean():.3f}")
    print(f"[METRIC:group_cv_accuracy_std] {scores.std():.3f}")
    print("[CHECK:group_leakage] Same user never in both train and test - OK")
else:
    print("[CHECK:group_leakage] No group column - using standard CV")
```

---

## Complete ML Pipeline Example

Putting it all together:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

print("[OBJECTIVE] Build and validate classification model with full rigor")

# 1. BASELINE
print("\n--- Baseline Comparison ---")
dummy = DummyClassifier(strategy='most_frequent')
dummy_scores = cross_val_score(dummy, X, y, cv=5, scoring='accuracy')
print(f"[METRIC:baseline_accuracy] {dummy_scores.mean():.3f}")

# 2. CROSS-VALIDATION
print("\n--- Cross-Validation ---")
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(random_state=42))
])
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"[METRIC:cv_accuracy_mean] {cv_scores.mean():.3f}")
print(f"[METRIC:cv_accuracy_std] {cv_scores.std():.3f}")

# 3. IMPROVEMENT OVER BASELINE
improvement = cv_scores.mean() - dummy_scores.mean()
print(f"[METRIC:improvement_over_baseline] {improvement:.3f}")
print(f"[STAT:effect_size] Relative improvement: {improvement/dummy_scores.mean()*100:.1f}%")

# 4. INTERPRETATION
print("\n--- Interpretation ---")
# (permutation importance code here)

# 5. FINDING (only after full evidence)
if improvement > 0.05:
    print(f"[FINDING] Random Forest achieves {cv_scores.mean():.3f} accuracy, "
          f"improving {improvement:.3f} over baseline ({improvement/dummy_scores.mean()*100:.1f}% relative)")
    print(f"[SO_WHAT] Model provides actionable predictions for business use case")
else:
    print("[FINDING] Model does not significantly outperform baseline")
    print("[LIMITATION] Consider simpler approach or feature engineering")
```

---

## Quality Gate: Required Evidence

Before any `[FINDING]` in ML, you MUST have:

| Evidence | Marker | Example |
|----------|--------|---------|
| Baseline comparison | `[METRIC:baseline_*]` | `[METRIC:baseline_accuracy] 0.65` |
| CV scores with variance | `[METRIC:cv_*_mean/std]` | `[METRIC:cv_accuracy_mean] 0.85` |
| Improvement quantified | `[METRIC:improvement_*]` | `[METRIC:improvement_over_baseline] 0.20` |
| Effect size | `[STAT:effect_size]` | `[STAT:effect_size] 31% relative improvement` |
| Interpretation | `[METRIC:top_features]` | Top 3 features listed |
| Limitations acknowledged | `[LIMITATION]` | Model constraints documented |

**Missing any of these? Your finding is "Exploratory", not "Verified".**
