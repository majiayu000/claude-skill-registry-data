---
name: run-resource-design
description: Guide for designing Run resources in OptAIC. Use when creating PipelineRun, ExperimentRun, BacktestRun, PortfolioOptimizationRun, TrainingRun, InferenceRun, or MonitoringRun. Covers execution tracking, metrics, output artifacts, and lineage.
---

# Run Resource Design Patterns

Guide for designing Run resources that track execution results and produce versioned outputs.

## When to Use

Apply when:
- Creating execution tracking for pipeline/model/backtest runs
- Designing output artifact storage patterns
- Implementing metrics and status tracking
- Building lineage tracking for reproducibility

## Critical Concept: Runs are Activities of Flows

**Runs are NOT the same as Flow Execution Resources.**

| Concept | Type | Lifecycle | Analogy |
|---------|------|-----------|---------|
| **Flow Execution Resource** | Static | Created with Instance | The "deployment" |
| **Run** | Dynamic | Created each trigger | The "execution" |

```
Flow Execution Resource = Prefect Deployment (static, created once)
Run = Prefect Flow Run (dynamic, created each trigger, many per Flow)

Instance.refresh_flow  ──┬──> PipelineRun (2024-01-01)
                         ├──> PipelineRun (2024-01-02)
                         └──> PipelineRun (2024-01-03)
```

## Core Concept: Execution Record

Runs track execution activities of Flow Execution Resources:

```
Run = Execution Activity
├── parent_instance_id    # Which Instance was executed
├── flow_kind             # Which flow type (refresh, train, infer, monitor)
├── orchestrator_run_id   # Prefect flow run ID
├── status                # pending|running|completed|failed
├── started_at / ended_at # Timing
├── metrics_json          # Computed metrics
├── outputs_ref           # Path to output artifacts
└── input_versions        # Versions of upstream resources used
```

## Run Types

| Type | Parent Instance | Flow Kind | Key Outputs |
|------|----------------|-----------|-------------|
| `PipelineRun` | DatasetInstance | refresh | rows_added, last_date |
| `ExperimentRun` | ExperimentInstance | preview | preview_data, statistics |
| `BacktestRun` | BacktestInstance | backtest | equity_curve, trades, metrics |
| `PortfolioOptimizationRun` | PortfolioOptimizerInstance | optimize | weights, metrics |
| `TrainingRun` | ModelInstance | training | model_artifact, metrics |
| `InferenceRun` | ModelInstance | inference | predictions, confidence |
| `MonitoringRun` | ModelInstance/DatasetInstance | monitoring | drift_metrics, alerts |

## Run Creation via RunExecutionService

Runs are created by triggering a Flow Execution Resource:

```python
# libs/orchestration/run_service.py
async def submit_pipeline_run(
    session: AsyncSession,
    actor: ActorContext,
    dataset_id: UUID,
    mode: str = "incremental",
) -> PipelineRun:
    # 1. Load Instance and get Flow deployment ID
    instance = await session.get(DatasetInstance, dataset_id)
    deployment_id = instance.prefect_deployment_id

    # 2. Check upstream freshness (flow-to-flow lineage)
    report = await lineage_resolver.check_upstream_freshness(
        session, dataset_id, freshness_checker
    )
    if not report.all_ready:
        raise UpstreamNotReadyError(...)

    # 3. Create Run resource record
    run = PipelineRun(
        parent_id=dataset_id,
        flow_kind="refresh",
        status="pending",
    )
    session.add(run)

    # 4. Trigger Prefect deployment
    result = await orchestrator.submit_run(
        run_id=run.id,
        deployment_id=deployment_id,
        parameters={"mode": mode},
    )
    run.orchestrator_run_id = result.orchestrator_run_id

    # 5. Emit activity
    await emit_activity("pipeline_run.started", run.id, {...})

    return run
```

## Status Flow

```
pending → running → completed
                  ↘ failed
                  ↘ cancelled
```

## Run Lifecycle

1. **Submit**: Create Run in `pending`
2. **Start**: Transition to `running`, set `started_at`
3. **Progress**: Update `progress_pct`, emit activities
4. **Complete**: Set `ended_at`, store outputs, transition to `completed`
5. **Fail**: Set error info, transition to `failed`

See [references/lifecycle.md](references/lifecycle.md).

## Output Artifacts

```python
run_outputs = {
    "metrics_json": {
        "sharpe_ratio": 1.85,
        "max_drawdown": -0.12,
        "total_return": 0.15
    },

    "artifacts_ref": {
        "equity_curve": "s3://runs/{run_id}/equity_curve.parquet",
        "trades": "s3://runs/{run_id}/trades.parquet",
        "weights_history": "s3://runs/{run_id}/weights.parquet"
    }
}
```

## Lineage Tracking

Track which versions of upstream resources were used:

```python
input_versions = {
    "signal_instance_id": "uuid",
    "signal_version_id": "version-uuid",
    "price_dataset_version_id": "version-uuid",
    "model_artifact_version": "v1.2.3"
}
```

## Run Completion Updates Flow Status

When a Run completes, it updates the parent Flow's status:

```python
async def _on_run_completed(session: AsyncSession, run: PipelineRun):
    # 1. Update Instance's freshness status
    instance = await session.get(DatasetInstance, run.parent_id)
    instance.freshness_status = "ready"
    instance.last_run_at = run.finished_at

    # 2. Update StatusStore for freshness calculations
    await status_store.mark_run_success(
        resource_id=instance.resource_id,
        last_data_date=run.metrics_json.get("last_data_date"),
        rows_processed=run.metrics_json.get("rows_processed"),
    )

    # 3. Propagate staleness to downstream resources
    affected = await lineage_resolver.propagate_staleness(
        session, instance.resource_id
    )

    # 4. Publish real-time status update
    await centrifugo.publish(
        channel=f"instance:{instance.resource_id}:status",
        data={"status": "ready", "last_run_id": str(run.id)},
    )

    # 5. Emit completion activity
    await emit_activity("pipeline_run.completed", run.id, {
        "metrics": run.metrics_json,
        "affected_downstream": [str(r) for r in affected],
    })
```

## Implementation Checklist

1. [ ] Create extension table with run-specific fields
2. [ ] Include `flow_kind` and `orchestrator_run_id` fields
3. [ ] Implement status transitions with validation
4. [ ] Track timing (started_at, ended_at)
5. [ ] Store metrics in `metrics_json`
6. [ ] Store large outputs externally (`artifacts_ref`)
7. [ ] Track input versions for lineage
8. [ ] Emit activities at lifecycle transitions
9. [ ] **Update Flow status on completion** (via StatusStore)
10. [ ] **Propagate staleness to downstream** (via LineageResolver)
11. [ ] **Publish real-time updates** (via Centrifugo)

## Reference Files

- [Lifecycle](references/lifecycle.md) - Status transitions and activities
- [Examples](references/examples.md) - Complete Run examples
- [Metrics](references/metrics.md) - Standard metrics by run type
