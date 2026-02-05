---
name: instance-resource-design
description: Guide for designing Instance resources in OptAIC. Use when creating DatasetInstance, SignalInstance, ExperimentInstance, ModelInstance, PortfolioOptimizerInstance, or BacktestInstance. Covers definition references, config patterns, composition, flow execution pairing, and scheduling.
---

# Instance Resource Design Patterns

Guide for designing Instance resources that configure and execute Definition plugins.

## When to Use

Apply when:
- Creating configured dataset/signal/model instances
- Designing composition patterns (Pipeline + Store + Accessor)
- Implementing scheduling and freshness tracking
- Pairing Flow Execution Resources with Instances
- Building special cases like BacktestInstance (no definition)

## Core Concept: Configured Usage

Instances reference Definitions and provide runtime configuration:

```
Instance = Configured Usage
├── definition_resource_id    # Which Definition to use
├── definition_version_id     # Pinned version (optional)
├── config_json               # Runtime configuration
├── schedule_json             # Cron/refresh schedule
├── upstream_refs             # Connected upstream resources
└── flow_execution_handles    # Prefect deployments, MLflow experiments
```

## Instance ↔ Flow Pairing

**Critical Concept**: When an Instance is created, Flow Execution Resources are also created.

Flow Execution Resources are static Prefect deployments (or equivalent orchestration handles) that are:
- Created when Instance is created
- Paired 1:1 or 1:N with Instance (some Instances have multiple flows)
- Stored as handles in the Instance extension table
- The "execution capability" vs Runs which are "execution activities"

```
DatasetInstance creation:
├── Create Resource record
├── Create extension table record
├── Create Prefect deployment for refresh flow
└── Store deployment_id in instance.prefect_deployment_id
```

See [references/flow-pairing.md](references/flow-pairing.md).

## Instance Types

| Type | Parent | Definition Ref | Flow Count | Notes |
|------|--------|---------------|------------|-------|
| `DatasetInstance` | Project | PipelineDef + StoreDef + AccessorDef | 1 | refresh_flow |
| `SignalInstance` | Project | Inherits from DatasetInstance | 1 | Promoted dataset |
| `ExperimentInstance` | Project | OpDef/OpMacroDef | 1 | preview_flow |
| `ModelInstance` | Project | MLModuleDef | 3 | train/infer/monitor |
| `PortfolioOptimizerInstance` | Project | PortfolioOptimizerDef | 1 | optimize_flow |
| `BacktestInstance` | Project | None | 1 | Fixed procedure |

## Multi-Flow Instances

Some Instance types have multiple Flow Execution Resources:

```
ModelInstance:
├── training_flow       → TrainingRun activities
├── inference_flow      → InferenceRun activities
└── monitoring_flow     → MonitoringRun activities

Instance Extension Table:
├── prefect_training_deployment_id
├── prefect_inference_deployment_id
├── prefect_monitoring_deployment_id
├── mlflow_experiment_id        (training tracking)
├── mlflow_registered_model_name (after promotion)
└── evidently_project_id        (monitoring dashboard)
```

## Lineage is Flow-to-Flow

Dependencies track flow statuses, not instance relationships:

```
DatasetInstance.refresh_flow
        ↓ depends on
UpstreamDataset.refresh_flow status = READY
```

Lineage checking uses `check_upstream_freshness()` to verify all upstream
flow statuses before executing a downstream flow.

## Status Aggregation

Instance status aggregates from its Flow(s):

```python
# Single-flow Instance (DatasetInstance)
instance.status = flow.status

# Multi-flow Instance (ModelInstance)
instance.status = aggregate([
    training_flow.status,
    inference_flow.status,
    monitoring_flow.status,
])
# Uses min-severity: READY only if ALL flows are READY
```

Definition specifies the `status_aggregation_contract`:
```json
{
    "status_aggregation_contract": {
        "aggregation_method": "min_severity",
        "status_priority": ["ERROR", "STALE", "RUNNING", "READY"]
    }
}
```

## Composition Pattern

DatasetInstance composes multiple definitions:

```
DatasetInstance
├── pipeline_instance_id  → PipelineInstance → PipelineDef
├── store_instance_id     → StoreInstance → StoreDef
└── accessor_instance_id  → AccessorInstance → AccessorDef
```

See [references/composition.md](references/composition.md).

## Config Structure

```python
instance_metadata = {
    "definition_resource_id": "uuid",
    "definition_version_id": "uuid (optional)",

    "config_json": {
        "symbols": ["AAPL", "MSFT", "GOOGL"],
        "start_date": "2020-01-01",
        "lookback_days": 252
    },

    "schedule_json": {
        "type": "cron",
        "expression": "0 6 * * 1-5",
        "timezone": "America/New_York"
    },

    "upstream_refs": [
        {"resource_id": "uuid", "role": "input"},
        {"resource_id": "uuid", "role": "covariance"}
    ]
}
```

## Special Case: BacktestInstance

BacktestInstance has no Definition - the backtest procedure is fixed:

```python
backtest_instance = {
    "type": "BacktestInstance",
    "name": "Q1_2024_Backtest",
    "metadata_json": {
        # No definition_resource_id

        "assets_json": {
            "universe": ["SPY", "QQQ", "IWM"],
            "benchmark": "SPY"
        },

        "signals_json": {
            "primary": "uuid-of-signal-instance",
            "secondary": ["uuid-1", "uuid-2"]
        },

        "date_range_json": {
            "start": "2024-01-01",
            "end": "2024-03-31"
        },

        "config_json": {
            "rebalance_frequency": "daily",
            "transaction_costs": 0.001,
            "slippage_model": "linear"
        }
    }
}
```

## Implementation Checklist

1. [ ] Reference parent Definition via `definition_resource_id`
2. [ ] Pin version if reproducibility needed (`definition_version_id`)
3. [ ] Design `config_json` matching Definition's `parameters_schema`
4. [ ] Track `upstream_refs` for lineage
5. [ ] Add freshness tracking fields if scheduled
6. [ ] Create extension table in `libs/db/models/`
7. [ ] **Create Flow Execution Resources on Instance creation**
   - [ ] Create Prefect deployment(s) for each flow type
   - [ ] Store deployment IDs in extension table
   - [ ] Register with external systems (MLflow, EvidentlyAI)
8. [ ] **Implement status aggregation** if multi-flow Instance
9. [ ] **Set up real-time subscriptions** via Centrifugo

## Reference Files

- [Composition](references/composition.md) - Dataset composition pattern
- [Examples](references/examples.md) - Complete Instance examples
- [Scheduling](references/scheduling.md) - Schedule configuration
- [Flow Pairing](references/flow-pairing.md) - Flow Execution Resource pairing
