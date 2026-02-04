---
name: embedding-engine
description: Embedding backends (InsightFace/PyTorch+ONNXRuntime vs TensorRT). Use when optimizing embedding throughput or debugging drift/fallbacks.
---

# Embedding Engine Skill

Use this skill to optimize embedding performance and debug embedding drift/fallback behavior.

## When to Use

- Embedding pipeline running slowly
- Need to switch between PyTorch and TensorRT
- Debugging embedding drift between backends
- Building/caching TensorRT engines
- Verifying ONNXRuntime/CoreML provider selection (macOS)

## Sub-agents

| Sub-agent | Purpose |
|-----------|---------|
| **PyTorchEmbeddingSubagent** | Reference ArcFace (training/validation) |
| **TensorRTEmbeddingSubagent** | GPU-optimized TRT inference |
| **ONNXEmbeddingSubagent** | Future ONNXRuntime C++ service (planned) |

## Current Backends

- **`pytorch` (default):** ArcFace via the `insightface` Python package (used by `tools/episode_run.py`)
- **`tensorrt` (optional):** TensorRT engine build + inference via `FEATURES/arcface_tensorrt/`

## Key Skills

### Embed faces with the configured backend

Run embedding with the configured backend (same interface as the pipeline).

```python
from tools.episode_run import get_embedding_backend

embedder = get_embedding_backend(
    backend_type="pytorch",  # or "tensorrt"
    device="cpu",
    tensorrt_config="config/pipeline/arcface_tensorrt.yaml",
    allow_cpu_fallback=True,
)
embedder.ensure_ready()
embeddings = embedder.encode(face_crops)  # (N, 512) L2-normalized
```

### Build a TensorRT engine from ONNX

```bash
python -m FEATURES.arcface_tensorrt --mode build --onnx-path models/arcface_r100_v1.onnx
```

### Compare TensorRT vs PyTorch embeddings (parity + speedup)

```bash
python -m FEATURES.arcface_tensorrt --mode compare --n-samples 100
```

This uses `FEATURES/arcface_tensorrt/src/embedding_compare.py` and reports cosine similarity + L2 distance stats.

## Config Reference

**File:** `config/pipeline/embedding.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `embedding.backend` | `pytorch` | Backend: `pytorch` or `tensorrt` |
| `embedding.tensorrt_config` | `config/pipeline/arcface_tensorrt.yaml` | TensorRT config path |
| `validation.max_drift_cosine` | 0.001 | Drift tolerance (behavior depends on runtime) |

**File:** `config/pipeline/arcface_tensorrt.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `arcface_tensorrt.enabled` | false | Sandbox feature flag (engine must exist) |
| `tensorrt.precision` | fp16 | Engine precision |
| `tensorrt.max_batch_size` | 32 | Max batch for engine build |
| `tensorrt.workspace_size_mb` | 1024 | TRT workspace |
| `tensorrt.engine_s3_bucket` | null | Optional engine bucket |

## Engine Storage

TensorRT engines are GPU-architecture specific. Stored in S3:

```
s3://screenalytics-models/engines/
├── arcface_r100-fp16-sm75.plan   # Ampere (RTX 30xx)
├── arcface_r100-fp16-sm80.plan   # A100
├── arcface_r100-fp16-sm86.plan   # Ada (RTX 40xx)
└── arcface_r100-fp16-sm89.plan   # Hopper (H100)
```

**Naming convention:** `{model_name}-{precision}-sm{arch}.plan`

## Common Issues

### "Engine not found" / TensorRT backend won’t load

**Cause:** No engine built for the current GPU / config mismatch

**Fix:** Build locally:
```bash
python -m FEATURES.arcface_tensorrt --mode build --onnx-path models/arcface_r100_v1.onnx
```

### Embedding drift too high

**Cause:** FP16 quantization or TRT optimization changes

**Check:** Run parity compare:
```bash
python -m FEATURES.arcface_tensorrt --mode compare --n-samples 100
```

**Fix:** Use FP32 precision:
```yaml
tensorrt:
  precision: fp32  # default is fp16
```

### TensorRT slower than expected / falling back

**Cause:** Not batching, engine built with suboptimal shapes/precision, or backend fell back

**Check:** Ensure `config/pipeline/embedding.yaml` has `embedding.backend: tensorrt` and re-run with `--mode benchmark`.

**Fix:** Increase batch size, ensure GPU backend:
```yaml
tensorrt:
  opt_batch_size: 32
  max_batch_size: 64
```

### Out of GPU memory

**Cause:** Engine workspace too large

**Check:** `nvidia-smi` during inference

**Fix:** Reduce workspace:
```yaml
tensorrt:
  workspace_size_mb: 512  # default is 1024
```

## Benchmark Reference

| Backend | Batch | Throughput | Latency | VRAM |
|---------|-------|------------|---------|------|
| PyTorch | 32 | ~50 fps | ~640ms | 2GB |
| TensorRT FP16 | 32 | ~250 fps | ~128ms | 1GB |
| TensorRT FP32 | 32 | ~180 fps | ~178ms | 1.5GB |

## Diagnostic Output

```json
{
  "backend": "tensorrt",
  "engine_path": "~/.cache/screenalytics/engines/arcface_r100_v1-sm86.trt",
  "precision": "fp16",
  "batch_size": 32,
  "embedding_dim": 512,
  "throughput_fps": 245.3,
  "latency_ms": 130.5,
  "vram_mb": 1024,
  "validation": {
    "drift_vs_pytorch": 0.9995,
    "regression_test": "passed"
  }
}
```

## Key Files

| File | Purpose |
|------|---------|
| `tools/episode_run.py` | Pipeline embedding backend selection (`get_embedding_backend`) |
| `FEATURES/arcface_tensorrt/src/tensorrt_builder.py` | Engine build/cache + optional S3 |
| `FEATURES/arcface_tensorrt/src/tensorrt_inference.py` | TensorRT inference wrapper |
| `FEATURES/arcface_tensorrt/src/embedding_compare.py` | Parity + speedup compare utilities |
| `config/pipeline/embedding.yaml` | Backend selection + validation knobs |
| `config/pipeline/arcface_tensorrt.yaml` | TensorRT builder/runtime config |
| `FEATURES/arcface_tensorrt/tests/test_tensorrt_embedding.py` | Unit tests (synthetic) |
| `tests/ml/test_arcface_embeddings.py` | ML-gated embedding invariants |

## Related Skills

- [pipeline-insights](../pipeline-insights/SKILL.md) - General pipeline debugging
- [face-alignment](../face-alignment/SKILL.md) - Alignment before embedding
