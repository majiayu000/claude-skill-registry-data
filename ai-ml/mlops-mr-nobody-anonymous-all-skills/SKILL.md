---
name: mlops
description: "Operate models in production: reproducible training, model and data versioning, deployment strategies, rollback and the feedback loop back into training."
type: procedural
category: ai
domain: ai
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - mlops pipeline
  - model versioning deployment
  - shadow deployment model
  - retrain pipeline schedule
  - feature store consistency
aliases:
  - ml-ops
keywords:
  - mlops
  - versioning
  - registry
  - retraining
  - deployment
  - rollback
  - pipeline
mcp_servers:
  - github
  - kubernetes
source: custom
enabled: true
---

# MLOps

## Purpose

Operate models in production: reproducible training, model and data versioning, deployment strategies, rollback and the feedback loop back into training.

## When to Use

- A model exists in a notebook and must run in production reliably.
- Reproducing last month's model is impossible.
- A deployment needs rollback and an audit trail.

## When NOT to Use

- The task is exploratory analysis with no deployment plan.
- A model is a one-off offline batch with no maintenance.
- The organisation has no data pipeline to feed it.

## Capabilities

- Version data, code and model artifacts together.
- Automate training with pinned environments and recorded metrics.
- Deploy with shadow, canary or blue-green and a tested rollback.
- Capture serving inputs for evaluation and retraining.
- Define the retrain trigger: schedule, drift, or performance drop.

## Inputs

- The training data source and how it changes over time.
- Serving constraints: latency, throughput, hardware.
- The business metric the model is supposed to move.

## Workflow

1. Pin the environment and record the random seeds used in training.
2. Version datasets with content hashes and store the manifest with the model.
3. Register the model with its metrics, training data version and evaluation report.
4. Deploy shadow first and compare predictions against production silently.
5. Canary a small share with alerts on both model and business metrics.
6. Close the loop: log serving inputs, label outcomes and schedule retraining.

## Tools

- mlflow
- dvc
- kubernetes
- airflow
- bentoml

## Examples

- `A model without its training data hash cannot be audited or rolled back meaningfully.`
- `Shadow deployment catches a 30% prediction shift that aggregate accuracy hides.`

## Safety

- Never train on production PII without a documented basis and controls.
- Rollback must be exercised; an untested rollback is a hope.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `kubernetes` | stdio | full | high | `KUBECONFIG` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/ai/mlops`). First-party skill, maintained in this repository.

## Notes

- Feature skew between training and serving is the most common silent failure.
- Record the business metric alongside accuracy; they diverge.
- Pairs with: `model-drift-monitoring`, `rag-evaluation`.
