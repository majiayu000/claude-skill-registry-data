---
name: mlflow
description: Use when tracking machine-learning experiments and managing models with MLflow — a local SQLite backend, logging parameters, metrics and artifacts, the model registry with aliases such as champion, serving a registered model over HTTP, and simple drift checks on incoming data. Also use when runs cannot be compared, the wrong model version is served, or the same pipeline must run both locally and on a managed platform.
---

# MLflow

Default: tracking server backed by SQLite for local work (`sqlite:///mlflow.db`), one experiment per problem, every run logs parameters + metrics + the model, promotion through registry **aliases** (not stages), serving by alias.

## Local setup

```python
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("tabular-classifier")
with mlflow.start_run():
    mlflow.log_params({"model": "logreg", "C": 1.0, "seed": 42})
    model.fit(X_train, y_train)
    mlflow.log_metric("f1", f1_score(y_test, model.predict(X_test)))
    mlflow.sklearn.log_model(model, name="model", registered_model_name="tabular-classifier",
                             input_example=X_train[:5])
```

(Argument names differ slightly between MLflow major versions — check the version you install.)

Browse with `mlflow ui --backend-store-uri sqlite:///mlflow.db`.

## Registry and promotion

- Each `log_model` with a registered name creates a new version.
- Point an alias at the version you trust: `client.set_registered_model_alias("tabular-classifier", "champion", version)`.
- Load and serve by alias (`models:/tabular-classifier@champion`), so promotion is one call and rollback is moving the alias back.
- Decide promotion by a rule written in code (e.g. new F1 ≥ current champion F1 on the same test set).

## Serving

```bash
mlflow models serve -m "models:/tabular-classifier@champion" -p 5001 --env-manager local
curl -s localhost:5001/invocations -H 'Content-Type: application/json' \
  -d '{"dataframe_split": {"columns": [...], "data": [[...]]}}'
```

Log an `input_example` (or a signature) so the server validates input shapes.

## Drift checks

- Store reference statistics of training features (mean, standard deviation, category frequencies).
- For each batch of incoming data compute the same statistics and flag features beyond a threshold (e.g. mean shifted by more than 3 standard errors, or a population stability index above a limit).
- Test the detector with a normal batch (no alert) and a deliberately shifted batch (alert).

## Same pipeline on a managed platform

Keep training code independent of where it runs; only the tracking URI and registry location change (e.g. a Unity Catalog three-level name on Databricks). Run the same tests in both places.

## Verification loop

1. A run appears with parameters, metrics and the model artifact.
2. The alias resolves to the intended version.
3. The served model answers a known input correctly; the drift check fires on the shifted batch only.

## Pitfalls

- **Parallel writers** to one SQLite file can lock; use one writer or a server backend for concurrent jobs.
- **Environment mismatch:** a model logged with one library version may not load with another; log requirements with the model.
- **Stages are deprecated** in favour of aliases and tags in recent versions.
- **Artifacts grow:** set a location with enough space and clean up failed runs.
