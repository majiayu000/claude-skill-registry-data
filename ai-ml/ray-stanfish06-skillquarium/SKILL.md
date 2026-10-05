---
name: ray
description: Distributed Python compute with Ray — @ray.remote tasks/actors for cluster-scale parallelism, Ray Data for large-batch preprocessing, Ray Train for distributed model training (DDP/FSDP/DeepSpeed), Ray Tune for scalable hyperparameter search, and Ray Serve for model serving. Use when scaling a Python workload (docking screens, million-cell atlas preprocessing, hyperparameter sweeps, multi-GPU training) from a laptop to a multi-node cluster with minimal code changes. Ray Tune can use optuna as a search algorithm; Ray Train wraps pytorch-lightning-style training loops.
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
compatibility: Requires Python 3.10+ (Ray's PyPI metadata requires >=3.10; older 3.9 wheels exist only for Ray <2.10) and ray 2.x (current 2.56.1). Install the extra matching your workload — ray[default] (dashboard+autoscaler), ray[data], ray[train], ray[tune], ray[serve], ray[rllib] — rather than ray[all]. Every node in a cluster must run the same Ray version and a compatible Python minor version; mismatches fail silently or crash workers.
metadata: {"version": "1.0", "skill-author": "community"}
---

# Ray

## Overview

Ray is a distributed runtime for Python: `@ray.remote` turns an ordinary function or class into a task/actor that Ray schedules across all CPUs/GPUs on your laptop or across every node in a cluster, with the same code in both cases. On top of this "Ray Core," Ray ships purpose-built libraries:

- **Ray Data** — distributed, streaming data loading/transform (`ray.data.read_parquet(...).map_batches(...)`), good for ML preprocessing pipelines that don't fit in one machine's memory.
- **Ray Train** — distributed training wrapper (`TorchTrainer`, `ScalingConfig`) for DDP/FSDP/DeepSpeed, with native PyTorch Lightning and Hugging Face `Trainer` integration.
- **Ray Tune** — scalable hyperparameter search with pluggable search algorithms (including Optuna, HyperOpt) and schedulers (ASHA, PBT, Hyperband).
- **Ray Serve** — programmable, autoscaling model serving (`@serve.deployment`), including an LLM-serving path (`ray.serve.llm`).
- **RLlib** — production reinforcement learning at scale.

Ray Core is the substrate all of the above sit on: tasks (stateless remote function calls), actors (stateful remote classes), and objects (immutable values in a shared, cluster-wide object store).

## Installation

```bash
# Recommended for ML workloads
uv pip install -U "ray[data,train,tune,serve]"

# General-purpose distributed Python (dashboard + cluster launcher, no ML libs)
uv pip install -U "ray[default]"

# Minimal core only (no dashboard) — smallest footprint for worker images
uv pip install -U "ray"

# Reinforcement learning
uv pip install -U "ray[rllib]"
```

Check version: `python -c "import ray; print(ray.__version__)"` (targets the 2.5x series; APIs below are stable across recent 2.x releases). Pydantic v1 is deprecated upstream — run `pip install -U pydantic` if you see a Ray-emitted Pydantic v1 warning.

## When to Use

- A single-machine Python loop (embarrassingly parallel or not) needs to scale to many cores or many machines with minimal rewriting.
- You're bottlenecked on CPU-bound preprocessing before GPU training (Ray Data) or need multi-GPU/multi-node training (Ray Train) without hand-rolling `torch.distributed`.
- You want to run a large hyperparameter sweep (Ray Tune) with early stopping/pruning across a cluster instead of a single machine.
- You need to serve a model (or several) with autoscaling and custom Python routing logic (Ray Serve) rather than a static endpoint.

Not a fit for simple thread/process-pool parallelism on one machine where `concurrent.futures` is enough — Ray's cluster machinery adds overhead that isn't worth it for that case.

## Core Concepts: Ray Core

```python
import ray
ray.init()   # starts a local cluster; omit address to run laptop-only,
             # or ray.init(address="auto") / address="ray://head-ip:10001" to join a real cluster

@ray.remote
def process_one(sample_id):
    ...
    return result

# Launch many tasks in parallel; futures return immediately
futures = [process_one.remote(sid) for sid in sample_ids]
results = ray.get(futures)   # blocks until all complete

@ray.remote(num_gpus=1)
class ModelActor:
    def __init__(self, checkpoint_path):
        self.model = load_model(checkpoint_path)

    def predict(self, batch):
        return self.model(batch)

actor = ModelActor.remote("model.pt")
prediction = ray.get(actor.predict.remote(batch))
```

Key rules:
- `.remote()` on a function/actor method returns an `ObjectRef` immediately (non-blocking); `ray.get()` resolves it.
- Large objects passed between tasks are automatically stored in Ray's shared-memory object store and referenced, not copied — pass big arrays/DataFrames as arguments rather than closing over them, for efficiency.
- `num_cpus=`, `num_gpus=`, `resources={"custom": 1}` on `@ray.remote(...)` declare what each task/actor needs; Ray's scheduler places work accordingly.

## Ray Data: Distributed Preprocessing

```python
import ray

ds = ray.data.read_parquet("s3://bucket/variants/")
ds = ds.map_batches(normalize_batch, batch_format="pandas", batch_size="auto")
ds = ds.filter(lambda row: row["qc_pass"])
ds.write_parquet("s3://bucket/variants_clean/")
```

Ray Data streams batches through the cluster rather than materializing the whole dataset in memory, and integrates directly with Ray Train (`Trainer(..., datasets={"train": ds})`) so preprocessing and training share the same cluster.

## Ray Train: Distributed Training

```python
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_loop_per_worker(config):
    model = build_model()
    model = ray.train.torch.prepare_model(model)   # wraps in DDP automatically
    for epoch in range(config["epochs"]):
        train_one_epoch(model, ...)
        ray.train.report({"loss": loss})

trainer = TorchTrainer(
    train_loop_per_worker,
    train_loop_config={"epochs": 10},
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True),
)
result = trainer.fit()
```

If you already have a PyTorch Lightning `Trainer`, use `ray.train.lightning.RayLightningEnvironment`/`RayDDPStrategy` instead of rewriting the loop — Ray Train slots underneath Lightning's `Trainer(strategy=...)`.

## Ray Tune: Hyperparameter Search

```python
from ray import tune
from ray.tune.search.optuna import OptunaSearch

def trainable(config):
    for step in range(config["epochs"]):
        acc = train_step(config["lr"], config["batch_size"])
        tune.report({"accuracy": acc})

tuner = tune.Tuner(
    trainable,
    tune_config=tune.TuneConfig(
        search_alg=OptunaSearch(),      # delegates sampling to Optuna
        metric="accuracy",
        mode="max",
        num_samples=100,
    ),
    param_space={
        "lr": tune.loguniform(1e-4, 1e-1),
        "batch_size": tune.choice([16, 32, 64]),
        "epochs": 10,
    },
)
results = tuner.fit()
best = results.get_best_result()
```

## Ray Serve: Model Serving

```python
from ray import serve

@serve.deployment(num_replicas=2, ray_actor_options={"num_gpus": 1})
class Predictor:
    def __init__(self):
        self.model = load_model()

    async def __call__(self, request):
        payload = await request.json()
        return self.model.predict(payload["inputs"])

serve.run(Predictor.bind(), route_prefix="/predict")
```

Ray Serve autoscales replicas based on request queue depth and supports composing multiple deployments into a pipeline (e.g., a preprocessing deployment feeding a model deployment).

## Running on a Cluster

```bash
ray up cluster.yaml      # provisions a cluster on AWS/GCP/Azure from a declarative config
ray submit cluster.yaml my_script.py
ray dashboard cluster.yaml   # tunnels the Ray dashboard to localhost
ray down cluster.yaml
```

`cluster.yaml` declares provider (aws/gcp/azure/kubernetes), head/worker node types, autoscaling min/max workers, and a `setup_commands` list (e.g., `pip install -r requirements.txt`) run on every node — this is how you keep Python/package versions in sync across the cluster (see pitfalls below). On Kubernetes, use KubeRay instead of `ray up`.

## Common Pitfalls

- **Version skew across nodes.** Ray requires the *same* `ray` version (and generally the same Python minor version) on the driver and every worker; a mismatch causes opaque serialization or RPC errors, not a clear version-check failure. Bake versions into the cluster image or `setup_commands`.
- **Capturing large objects in a closure.** A remote function that closes over a large local variable (instead of receiving it as an argument) gets it re-serialized on every call; pass large data as explicit `.remote()` arguments so Ray can place it in the object store once and reuse the reference.
- **Object store spilling / OOM.** Long `ray.data` pipelines or large actor state can exceed the object store's memory fraction, triggering disk spill (slow) or worker eviction. Watch `ray status` / the dashboard's object store panel, and prefer streaming (`map_batches` with a small `batch_size`) over materializing everything.
- **Forgetting `ray.get()` blocks.** Piling up thousands of unresolved `ObjectRef`s (e.g., a Python list comprehension over `.remote()` calls with no `ray.get` until the very end) can hold references and delay garbage collection; use `ray.wait()` to process results as they complete instead of `ray.get()` on everything at once for very large fan-outs.
- **`ray[all]` bloat.** The docs explicitly discourage `pip install ray[all]`; install only the extras your workload needs to avoid dependency conflicts and slow builds.
- **Actors are stateful — restarts lose state.** If a node dies, Ray can restart an actor (`max_restarts=`), but any in-memory state is gone unless you checkpoint it explicitly (e.g., to the object store or external storage).

## Resources

- Docs: https://docs.ray.io/
- Installation guide: https://docs.ray.io/en/latest/ray-overview/installation.html
- Ray Train: https://docs.ray.io/en/latest/train/train.html
- Ray Tune: https://docs.ray.io/en/latest/tune/index.html
- Ray Serve: https://docs.ray.io/en/latest/serve/index.html
- Source: https://github.com/ray-project/ray
