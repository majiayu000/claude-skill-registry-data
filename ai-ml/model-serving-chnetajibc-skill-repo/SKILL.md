---
name: model-serving
description: "Ship ML models to production: versioning, eval-gated serving, GPU efficiency, monitoring for drift. Use when a model leaves the notebook."
---

# model-serving

No model ships without an eval, a version, and a drift monitor.
## Inspection

Inventory model artifact, eval set, latency/throughput SLOs, GPU budget, and current serving path (or lack of one).

## Decision rules

Version data+code+weights together; eval-gate every promotion; batch where latency allows; optimize only profiled bottlenecks.


## Activate when

- Serving PyTorch/Transformers models (real-time or batch), optimizing GPU inference, or owning ML pipelines.

## Do NOT activate for

- Agent/RAG orchestration without custom models (see ai/agent-architecture).

## Procedure

1. Version: datasets, code, and weights pinned together; experiment tracking per run.
2. Serve: batch where latency allows; real-time via Triton/ONNX/TensorRT only after profiling proves the need; validate inputs, bound outputs.
3. Optimize: measure first (latency, throughput, memory); CUDA/Docker-GPU parity with training env.
4. Evaluate: offline eval set + online shadow/canary; rollback on regression.
5. Monitor: prediction drift, data validation failures, latency SLOs; retrain triggers documented.
6. Verify: eval report, load test at p99, rollback drill.

## Failure modes

Unversioned weights; eval-free promotion; GPU idle while batching would do; drift unmonitored; training-serving skew.

## Escalation

Agent/RAG without custom models → ai/agent-architecture; infra → cloud/*.
