---
name: ml-deployment
version: 1.0.0
description: Deploy a trained model to serving with versioning, shadow or canary rollout, and a tested rollback path.
author: matrixx0070
tags: [ml, deployment, serving, canary, rollback]
capabilities: []
---

## When to use

Use this to move a validated model artifact into production serving — choosing batch vs online, versioning the artifact, rolling out safely (shadow/canary), and wiring a one-command rollback.

**Not for:** deploying LLM inference endpoints, agents, or prompt chains (see `ai-agent-design`, `ai-cost-latency`). Not for scheduling data/ETL jobs or publishing reports (see `de-data-modeling`, `data-build-dashboard`).

## Method

1. Choose serving mode. Decision point: predictions consumed on a schedule → batch (write to a table); needed per-request in real time → online (REST/gRPC service).
2. Package the artifact with its transform pipeline and a version tag tied to the promoted run from `ml-experiment-tracking`. Pin dependency versions.
3. Guarantee train/serve parity: the exact same feature transforms run at serve time. A feature store or the serialized pipeline enforces this.
4. Contract the I/O: input schema, output schema, and validation that rejects malformed requests before they reach the model.
5. Roll out progressively. Decision point: unsure of live behavior → shadow (score real traffic, serve nothing) first; confident → canary a small % and compare metrics to the incumbent.
6. Keep the previous version deployable and register the model in a registry (staging → production stages).
7. Define and REHEARSE rollback: one command/flag flips traffic back to the last-good version. Test it before you need it.
8. Emit prediction logs and latency metrics from day one to feed `ml-monitoring`.

## Example

Fraud model served online. Package v3 (model + pipeline) behind a FastAPI endpoint, register as `fraud:staging`. Shadow for 48h: p99 latency 34ms, score distribution matches offline. Promote to canary at 5% traffic; canary block-rate within 0.3pp of incumbent and no latency regression. Ramp 5% → 50% → 100% over three days. Rollback tested: `deploy --model fraud:v2` restores the prior version in ~20s.

## Pitfalls

- **Train/serve skew.** Serving reimplements features slightly differently from training. Ship the same pipeline artifact.
- **Big-bang release.** 0→100% with no shadow/canary. Ramp and compare to the incumbent.
- **Untested rollback.** A rollback path that has never been run fails in the incident. Rehearse it.
- **No prediction logging.** You cannot monitor what you did not log. Emit inputs, outputs, and latency from launch.

## Output format

```
# Deployment: <name>
MODE: <batch|online>
ARTIFACT: <model version> + pipeline | run=<id> | deps pinned
PARITY: <feature store | serialized pipeline>
I/O CONTRACT: in=<schema> out=<schema> + request validation
ROLLOUT: shadow <dur> -> canary <%> -> ramp <plan>
REGISTRY: <name:stage>
ROLLBACK: <command> -> <last-good version> (rehearsed: y/n)
LOGGING: predictions + latency -> monitoring
```
