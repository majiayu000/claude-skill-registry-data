---
name: exasol-distributed-ml
description: "Distributed machine learning, data mining, and iterative HPC with Exasol. Covers end-to-end ML pipelines (DISTRIBUTE BY + SET scripts + BucketFS), per-entity federated training with partial_fit and ctx.reset(), batch inference, map-reduce ensemble training, distributed ensemble and SON algorithm for frequent itemset mining (Apriori, FP-Growth, association rules, market-basket analysis), Lua execute script orchestration for iterative algorithms (k-means, SGD, gradient descent), scikit-learn model training, parallel hyperparameter search, per-entity forecasting, anomaly detection, model lifecycle in BucketFS (pickle/joblib/ONNX versioning), GPU acceleration via CUDA SLCs (PyTorch/TensorFlow/RAPIDS), and ML-specific performance tuning (skew, OOM, multi-pass chunking)."
---

# Exasol Distributed ML and HPC

Trigger when the user mentions: **distributed ML**, **machine learning**, **train model**, **batch inference**, **prediction**, **feature engineering**, **hyperparameter**, **PyTorch**, **TensorFlow**, **scikit-learn**, **RAPIDS**, **GPU model**, **model deployment**, **distributed training**, **ensemble**, **anomaly detection**, **forecasting**, **clustering at scale**, **k-means**, **gradient descent**, **iterative algorithm**, **frequent itemset**, **association rules**, **market basket**, **Apriori**, **FP-Growth**, **data mining**, **SON algorithm**, **partial_fit**, **federated training**, or any pattern where data is trained or scored inside Exasol.

## Routing Algorithm

Choose the narrowest matching route. Load all routes that apply — they are designed to be read together.

### Route 1 — Pipeline architecture, algorithms, and patterns

**Trigger phrases:** `distributed training`, `end-to-end ML`, `feature engineering`, `batch inference`, `ensemble`, `k-means`, `gradient descent`, `frequent itemset`, `association rules`, `market basket`, `Apriori`, `FP-Growth`, `data mining`, `federated training`, `per-entity model`, `anomaly detection`, `forecasting`, `hyperparameter search`, `map-reduce`

→ Load: **[references/distributed-ml-patterns.md](references/distributed-ml-patterns.md)**

### Route 2 — Model storage, versioning, and lifecycle

**Trigger phrases:** `save model`, `ONNX`, `joblib`, `pickle`, `model versioning`, `load model in UDF`, `update model`, `latest.json`, `model registry`, `model path`, `BucketFS model`

→ Load: **[references/model-lifecycle.md](references/model-lifecycle.md)**

### Route 3 — GPU, CUDA, and RAPIDS

**Trigger phrases:** `GPU UDF`, `CUDA SLC`, `PyTorch`, `TensorFlow`, `RAPIDS`, `cuDF`, `cuML`, `GPU acceleration`, `TorchScript`, `GPU cluster`

→ Load: **[references/gpu-acceleration.md](references/gpu-acceleration.md)**

### Route 4 — Performance, tuning, and memory

**Trigger phrases:** `slow UDF`, `OOM`, `out of memory`, `memory_limit`, `data skew in ML`, `profile SET script`, `chunking`, `group size`, `partial_fit convergence`, `ctx.reset`, `multi-pass`, `epoch loop`

→ Load: **[references/ml-performance.md](references/ml-performance.md)**

## Defer to Existing Skills

Do not re-explain these — activate the relevant skill instead:

- **UDF API basics** (ctx.emit, ctx.get_dataframe, SCALAR vs SET syntax, CREATE SCRIPT templates) → **exasol-udfs**
- **SLC build/deploy** (exaslct CLI, flavor selection, Dockerfile customization) → **exasol-udfs** `references/slc-reference.md`
- **Lua execute script orchestration** (query/pquery API, error handling) → **exasol-udfs** `references/lua-execute-scripts.md`
- **BucketFS file operations** (cp/ls/rm via exapump) → **exasol-bucketfs**
- **DISTRIBUTE BY table design and query profiling** → **exasol-database**

## Key Principles

- Prefer `partial_fit` algorithms (SGD, MLP, MiniBatchKMeans) — stream chunks with `ctx.get_dataframe(num_rows=CHUNK_SIZE)`, loop epochs with `ctx.reset()` for convergence
- Avoid `ctx.get_dataframe(num_rows='all')` — it materializes the entire group in memory
- For algorithms without `partial_fit` (RandomForest, GradientBoosting): use the map-reduce ensemble pattern (Section 6 of distributed-ml-patterns.md) rather than loading all data at once
- Load models at module level (outside `run()`), never inside `run()`
- Orchestrate iterative algorithms with Lua execute scripts (`query`) rather than external drivers when possible
- DISTRIBUTE BY on the training/inference key keeps related rows on the same node and eliminates shuffles
