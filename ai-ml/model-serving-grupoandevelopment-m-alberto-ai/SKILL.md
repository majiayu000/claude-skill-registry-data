---
name: model-serving
description: Use when deploying a trained model behind an API. Covers FastAPI inference services, loading artifacts safely, request validation, batching, ONNX/quantization for speed, health checks, and monitoring.
---

# Model Serving

## Overview

Serving turns a saved model into a reliable, low-latency API. The concerns shift from accuracy to **latency, throughput, robustness, and observability**. The model artifact and its preprocessing must travel together (use the pipeline from `sklearn-pipelines`).

## When to use

- A validated model needs to be callable by other systems.
- Moving from notebook to production.

## Minimal FastAPI service

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib, numpy as np

app = FastAPI()
model = joblib.load("model.joblib")  # full pipeline: preprocessing + estimator

class Features(BaseModel):
    age: float
    income: float
    country: str
    plan: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(f: Features):
    import pandas as pd
    X = pd.DataFrame([f.model_dump()])
    proba = float(model.predict_proba(X)[0, 1])
    return {"probability": proba, "label": int(proba >= 0.5)}
```

Run: `uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4`.

## Production checklist

- **Load the model once** at startup, not per request.
- **Validate inputs** with Pydantic; return 422 on bad payloads.
- **Health/readiness** endpoints for orchestrators (k8s).
- **Batch** requests where possible to raise throughput.
- **Timeouts + graceful degradation** for downstream calls.
- **Version the model** in the response (`model_version`) for traceability.
- **Pin the artifact's training env** — preprocessing must match training exactly.

## Speed: ONNX + quantization

```python
# Export sklearn/torch model to ONNX, then serve with onnxruntime
import onnxruntime as ort
sess = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
out = sess.run(None, {"input": X.astype(np.float32)})
```

ONNX runtime + dynamic quantization often gives 2-4x CPU speedups. For LLMs, use vLLM/TGI rather than rolling your own.

## Monitoring (don't deploy blind)

- **Operational:** latency p50/p95/p99, error rate, throughput.
- **ML-specific:** input feature drift, prediction distribution shift, and (when labels arrive) live metric decay.
- Alert on drift — a silently degrading model is worse than a down one.

## Pitfalls

- **Training/serving skew** — different preprocessing in prod than training. Ship the pipeline, not just the estimator.
- **Loading the model per request** — kills latency.
- **No input validation** — one bad payload takes down the worker.
- **`pickle`/`joblib` from untrusted sources** — only load artifacts you produced.
- **No monitoring** — you won't notice drift until users do.

## Hand-off

A containerized, monitored endpoint serving the exact pipeline that model-evaluation validated and experiment-tracking registered.
