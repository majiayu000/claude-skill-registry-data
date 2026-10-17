---
name: ml-testing-strategy
category: testing
description: Use when writing tests for data or ML code — what to test at each layer (transforms, schemas, properties, pipeline smoke, model-quality thresholds, determinism and parity), how to build small synthetic fixtures, and what not to test
tech_stack: Python
source: obra/superpowers test-driven-development (MIT) and wshobson/agents data-quality-frameworks testing pyramid (MIT), adapted to data and ML code; Hypothesis and pytest docs cited
---
# ML Testing Strategy

## Overview

Data code is easy to "test" badly: a test that re-runs the pipeline and asserts the metric equals last week's 0.8312 breaks on every library upgrade and catches nothing. Good data tests pin behaviour on tiny, explicit fixtures where you know the right answer by hand, and assert model quality as a threshold on planted signal.

**Core principle:** test your logic, not the library; derive expected values by hand on a fixture small enough to read; assert ranges for anything learned.

## 1. The layers

| Layer | What it proves | Share of tests |
|---|---|---|
| Pure transforms | A cleaning rule, a feature, a metric gives the hand-derived answer | most |
| Schemas / contracts | Bad input is rejected with the right column named | one per rule |
| Properties (Hypothesis) | Invariants hold for many generated inputs | a few, on core transforms |
| Pipeline smoke | Entry point runs end-to-end on a fixture, writes a loadable artifact | one per entrypoint |
| Model quality | Beats the baseline by a margin on planted signal, fixed seed | one or two per model |
| Determinism and parity | Same seed → same output; saved/loaded and served predictions equal training-time ones | one each |
| Warehouse | dbt data and unit tests (sql-analytics-and-dbt) | per model |

## 2. Fixtures: small, synthetic, explicit

Build them in the test or `conftest.py`. Never a production extract (PII, size, drift) and never the network.

```python
def test_order_value_sums_lines_and_ignores_cancelled() -> None:
    lines = pd.DataFrame({
        "order_id": ["o1", "o1", "o2", "o3"],
        "amount": [10.0, 5.0, 7.0, 3.0],
        "status": ["ok", "ok", "cancelled", "ok"],
    })
    expected = pd.Series({"o1": 15.0, "o3": 3.0}, name="order_value")
    expected.index.name = "order_id"

    pd.testing.assert_series_equal(order_value(lines), expected)
```

Every fixture for a transform carries the cases that break data code: a null, a duplicate key, an unseen category, an empty frame, a single row, a boundary timestamp, a timezone-aware value. Each earns its own named test.

For model tests, plant a known signal with a seeded generator:

```python
@pytest.fixture
def churn_fixture() -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(7)
    n = 400
    X = pd.DataFrame({
        "days_since_order": rng.integers(0, 120, n),
        "orders_90d": rng.poisson(3, n),
        "plan": rng.choice(["free", "pro"], n),
    })
    logit = 0.04 * X["days_since_order"] - 0.5 * X["orders_90d"] - 1.0
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int).to_numpy()
    return X, y
```

## 3. Property tests with Hypothesis

Use them for invariants that hold for every input: totals are preserved, no NaN is introduced, outputs stay in range, a cleaning step is idempotent, a row-wise transform keeps the row count.

```python
from hypothesis import given, strategies as st
from hypothesis.extra.pandas import column, data_frames, range_indexes

order_lines = data_frames(
    columns=[
        column("order_id", elements=st.sampled_from(["o1", "o2", "o3"])),
        column("amount", elements=st.floats(0, 1e6)),
        column("status", elements=st.sampled_from(["ok", "cancelled"])),
    ],
    index=range_indexes(max_size=50),
)

@given(order_lines)
def test_order_value_total_equals_sum_of_ok_lines(lines: pd.DataFrame) -> None:
    result = order_value(lines)
    assert result.sum() == pytest.approx(lines.loc[lines["status"] == "ok", "amount"].sum())
    assert (result >= 0).all()
```

Keep CI deterministic with a profile (`settings.register_profile("ci", derandomize=True, deadline=None)`) if the repository has none; follow its profile if it does.

## 4. Model quality as thresholds

```python
def test_model_beats_prevalence_baseline_on_planted_signal(churn_fixture) -> None:
    X, y = churn_fixture
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    score = cross_val_score(build_model(seed=0), X, y, cv=cv, scoring="average_precision").mean()
    assert score > y.mean() + 0.15
```

- The baseline (prevalence for average precision, 0.5 for ROC-AUC, the dummy's error for regression) sits in the assertion, so the test says what "good" means.
- Margins come from running it: wide enough to survive a library upgrade, tight enough that a broken feature or a shuffled column fails it.
- Add the shuffled-label check from leakage-safe-feature-engineering for any model with engineered features.
- Real-data quality gates (the candidate beats the champion on last month) belong in the training pipeline's evaluation step, not in unit tests.

## 5. Smoke, determinism, round-trip and parity

```python
def test_train_writes_a_loadable_model(tmp_path, churn_fixture) -> None:
    X, y = churn_fixture
    path = train(X, y, out_dir=tmp_path, seed=0)
    model = load_model(path)
    assert model.predict_proba(X.head(5)).shape == (5, 2)

def test_training_is_deterministic_for_a_seed(churn_fixture) -> None:
    X, y = churn_fixture
    a = build_model(seed=0).fit(X, y).predict_proba(X)
    b = build_model(seed=0).fit(X, y).predict_proba(X)
    np.testing.assert_array_equal(a, b)
```

Also: saved-then-loaded model predicts exactly what the in-memory one did; the serving endpoint returns what `pipeline.predict_proba` returns for the same fixture row (model-serving-and-monitoring); a PyTorch model overfits one tiny batch (deep-learning-pytorch).

## 6. Comparing numbers

- Floats: `pytest.approx`, `np.testing.assert_allclose(actual, expected, rtol=1e-6)`, `pd.testing.assert_frame_equal(..., check_exact=False, rtol=1e-6)`.
- Frames: compare whole frames with `assert_frame_equal`, not a handful of cells; decide `check_dtype` and `check_like` (column order) deliberately.
- Learned outputs: ranges and relations (`> baseline + margin`, `0 <= p <= 1`), never exact values.

## 7. What not to test

- That scikit-learn's `StandardScaler` scales or pandas' `groupby` groups — test your use of them.
- Exact metric values from a training run.
- Plot styling.
- Anything needing a warehouse, a GPU or the network in the default suite — mark it with the repository's existing marker (or leave it out) and exercise it as in the prompt's "Exercising the change".

## 8. Speed

The default suite runs in seconds: fixtures of tens to a few hundred rows, `n_estimators` and epochs turned down through the same config the code reads, `n_jobs=1` where parallel start-up dominates. A slow suite gets skipped, and a skipped suite catches nothing.

## Common Mistakes

- Expected values computed with the same pandas expression as the code under test.
- One giant test that runs the whole pipeline and asserts it "did not crash".
- A model test with no seed, flaky one run in twenty.
- Fixtures read from a large CSV checked into the repo.
- Tests that pass on an empty frame because nothing was asserted per row.

## Red Flags

- A test asserting `score == 0.8312`.
- A test suite that downloads data.
- A transform with no test that feeds it a null or a duplicate.
- Coverage from a smoke test only — every line ran, nothing was checked.
