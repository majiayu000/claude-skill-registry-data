---
name: databricks
description: Use when running data and ML workloads on Databricks, including the no-cost Free Edition — Databricks Asset Bundles (databricks.yml) for jobs and notebooks, OAuth login with the CLI instead of personal access tokens, serverless compute limits, MLflow tracking and Unity Catalog model registration, and porting a local pipeline. Also use when a job fails only on Databricks, a library version differs from local, or a feature is not available in the free tier.
---

# Databricks

Default: everything deployable defined in an Asset Bundle in git, deploy and run with the Databricks CLI, OAuth user login (no long-lived tokens), serverless jobs, models registered in Unity Catalog, the same code tested locally first.

## Login without tokens

```bash
databricks auth login --host https://<workspace-host> --profile dev
databricks current-user me --profile dev
```

OAuth refreshes automatically; personal access tokens are long-lived secrets that end up in files and logs — avoid them unless a tool cannot do OAuth.

## Asset Bundles

```yaml
# databricks.yml
bundle: { name: model-pipeline }
targets:
  dev: { mode: development, default: true }
resources:
  jobs:
    train:
      name: train
      tasks:
        - task_key: train
          notebook_task: { notebook_path: ./notebooks/train.py }
```

```bash
databricks bundle validate -p dev
databricks bundle deploy  -p dev
databricks bundle run train -p dev
```

`mode: development` prefixes resource names per user and pauses schedules, so experiments do not collide with shared jobs.

## Free Edition constraints (check the current documentation)

- Serverless compute only; no custom clusters.
- Daily usage quotas; long or parallel jobs stop when exceeded.
- Non-commercial use only.
- Limited or no GPU model serving; plan CPU models or batch scoring.
- The managed runtime's Python and library versions may be older than your local environment; pin versions in the notebook (`%pip install` with exact versions) and record differences in a compatibility note.

## MLflow on Databricks

- Tracking works without configuration inside the workspace.
- Register models in Unity Catalog with a three-level name (`catalog.schema.model`) and set an alias (`champion`) — the same promotion rule as locally.
- Use `mlflow.set_registry_uri("databricks-uc")` when registering from code.

## Porting a local pipeline

1. Keep pure functions in a module that both local scripts and notebooks import.
2. Notebooks handle only I/O, configuration and logging.
3. Run the same assertions (metric thresholds, drift detection on a normal and a shifted batch) locally and as a job; compare numbers.

## Verification loop

1. `bundle validate` clean; `bundle deploy` succeeds.
2. `bundle run` finishes; record wall time and metrics.
3. The registered model version exists and the alias points to it.

## Pitfalls

- **Workspace paths vs repo paths:** notebooks deployed by bundles live under a bundle-specific path; use relative imports configured for that layout.
- **`%pip install` restarts Python;** put it in the first cell.
- **Quotas end runs abruptly;** keep jobs small and idempotent so a rerun is safe.
- **Secrets:** use secret scopes, never literals in notebooks (they are saved with outputs).
