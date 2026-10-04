---
name: modal
description: Serverless GPU cloud for Python with per-second billing on A100/H100/L40S. Use for burst ML training (>13B parameter models, multi-GPU), parallel evaluation runs, scheduled batch jobs that exceed local M4 Mac capacity, or any GPU-bound work that doesn't justify a permanent cluster.
---

# Modal — Serverless GPU Cloud

## When to use this skill

Use when you need to:

- "Train a 13B+ model that won't fit on my M4 Mac GPU"
- "Run a parallel hyperparameter sweep on 8× A100"
- "Process the full multi-nation curriculum corpus at scale"
- "Schedule a recurring GPU job (nightly HTR re-train)"
- "Serve a model on GPU for inference (without a permanent
  instance)"

## Overview

[Modal](https://modal.com/) is a serverless Python cloud
that runs code on on-demand GPUs (A100, H100, L40S, A10G, T4)
with per-second billing. No Kubernetes, no cluster management
— you decorate a function, and it runs in the cloud.

Key features:

- **`@app.function(gpu="H100")`** decorator — run any Python
  function on a remote GPU
- **`@app.webhook()`** decorator — expose a function as an
  HTTP endpoint
- **`@app.asgi()`** / **`@app.wsgi()`** — mount a full ASGI/WSGI
  app (FastAPI, etc.) without writing a server
- **`modal.Volume`** — shared network-attached storage (similar
  to S3)
- **Image caching** — Docker images are built once and cached
  across runs
- **Snapshotting** — pause a long-running function and resume
- **Multi-region** — choose the GPU region (us-east, eu-west,
  ap-south)

## When NOT to use this skill

- The job fits on the local M4 Mac (use the local
  `bunchloch` environment)
- The job is I/O-bound, not GPU-bound (use Dagster + Cloudflare
  Workers instead)
- The job requires 24/7 uptime (Modal cold-starts ~5-15s; use
  a dedicated server)

## Cianfhoghlaim integration (PRESERVED from the docs)

The Cianfhoghlaim burst-training story is:

```
        ┌─────────────────┐
        │  MacBook M4     │  ← daily fine-tuning
        │  (bunchloch)    │     3B-7B models, <2hr jobs
        └────────┬────────┘
                 │ exceeded capacity
                 ▼
        ┌─────────────────┐
        │  Modal H100     │  ← burst training
        │  (serverless)   │     13B+ models, multi-GPU
        └────────┬────────┘
                 │ trained artifacts
                 ▼
        ┌─────────────────┐
        │  Garage S3      │  ← sync via rclone
        │  (cloud)        │
        └────────┬────────┘
                 │ downloaded
                 ▼
        ┌─────────────────┐
        │  llama-swap     │  ← local serving
        │  (bunchloch)    │
        └─────────────────┘
```

The MacBook M4 (bunchloch) handles daily fine-tuning of
3B-7B models (Unsloth + TRL). For 13B+ full-parameter
training or multi-GPU sweeps, the project uses Modal H100
on-demand (~$3/hr). Trained artifacts are synced to Garage S3
via rclone, then downloaded back to `bunchloch` for llama-swap
serving.

The same pattern applies to:

- **HTR / OCR ensemble inference** — Modal L40S for batch
  processing of the multi-nation curriculum corpus
- **Embedding fine-tuning** — Modal A100 for BGE-M3 domain
  adaptation
- **Parallel eval runs** — Modal A10G for parallel RAGAS
  evaluation across 100s of test cases

## Core patterns

### Basic GPU function

```python
import modal

app = modal.App("cianfhoghlaim-htr-finetune")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch", "transformers", "datasets", "peft", "trl")
)


@app.function(gpu="H100", image=image, timeout=7200)
def train_htr(epochs: int = 3) -> str:
    """Fine-tune a HTR model on a 13B parameter base."""
    from transformers import ...
    # ... training code ...
    model.save_pretrained("/mnt/models/cianfhoghlaim-htr-v1")
    return "/mnt/models/cianfhoghlaim-htr-v1"


@app.local_entrypoint()
def main(epochs: int = 3):
    result = train_htr.remote(epochs=epochs)
    print(f"Trained model: {result}")
```

Run: `modal run --detach train.py --epochs 3`

### Volumes (shared storage)

```python
volume = modal.Volume.from_name("cianfhoghlaim-models", create_if_missing=True)


@app.function(gpu="A100", volumes={"/mnt/models": volume}, timeout=3600)
def evaluate(model_id: str, test_set: str) -> dict:
    """Evaluate a model on a test set; results stored in the volume."""
    # ...
    volume.commit()  # persist
    return {"accuracy": 0.94, "loss": 0.08}
```

### Webhook (HTTP endpoint)

```python
@app.function(gpu="L40S", timeout=300)
@app.webhook(method="POST")
def ocr_endpoint(request: dict) -> dict:
    """OCR a PDF via vision model; return extracted text."""
    pdf_bytes = base64.b64decode(request["pdf_base64"])
    # ... call vision LLM ...
    return {"text": extracted_text, "pages": n}
```

### ASGI app (FastAPI / Hono)

```python
fastapi_app = FastAPI()


@fastapi_app.get("/health")
def health():
    return {"status": "ok"}


@app.function(gpu="A10G", timeout=600)
@modal.asgi()
def serve():
    return fastapi_app
```

### Snapshotting (pause + resume)

```python
@app.function(gpu="H100", timeout=86400, snapshot=True)
def long_training():
    """Train for 24 hours; pause + resume across Modal restarts."""
    # ... long training ...
```

### Scheduled job (cron)

```python
@app.function(gpu="A100", schedule=modal.Period(hours=12), timeout=3600)
def nightly_htr_retrain():
    """Re-train HTR model every 12 hours."""
    # ... retrain ...
```

## CLI

```bash
# Run a function locally (or in the cloud if `image=`)
modal run script.py

# Run detached (don't block terminal)
modal run --detach script.py

# Deploy a webhook
modal deploy script.py

# List recent runs
modal run list

# Inspect logs
modal run logs <run-id>

# Volume management
modal volume create cianfhoghlaim-models
modal volume ls cianfhoghlaim-models
```

## Best practices

1. **Use `Image.debian_slim(python_version="3.12")` for fast
   cold starts** — `ubuntu` images are 2-3× larger
2. **Pin dependencies** — `pip_install("torch==2.5.0", ...)` not
   `pip_install("torch")`
3. **Use `Volume` for model artifacts > 100MB** — local disk
   is ephemeral
4. **Snapshot long jobs** — `snapshot=True` lets you pause +
   resume across Modal restarts
5. **Use `--detach` for long jobs** — don't block your terminal
6. **Cache expensive setups** with `@app.enter()` — runs once
   per container, not per function call
7. **Set timeouts aggressively** — `timeout=3600` for an
   hour, not `timeout=86400` by default

## Common pitfalls

- **Cold start latency** — first call to a function can take
  30-60s (image pull + setup). Subsequent calls are fast
- **GPU quota** — Modal has per-account GPU limits; request
  quota increases via the dashboard
- **S3 transfer costs** — for multi-GB model artifacts, sync
  via rclone (cheap) not via Modal (expensive)
- **Snapshots cost money while paused** — pay-per-second
  applies to paused snapshots too
- **Image caching is per-account** — if you have multiple
  Modal accounts, you re-build images for each

## Cross-references

- `.agents/skills/unsloth/SKILL.md` — for local Unsloth +
  TRL fine-tuning (the upstream skill)
- `.agents/skills/dagster/SKILL.md` — for the orchestration
  layer; Modal is invoked from Dagster assets
- `.agents/skills/dlt/SKILL.md` — Modal is the deployment
  target for the `deploy-modal` recipe
- The Cianfhoghlaim `infrastructure/stacks/modal/` stack
  (planned; not yet provisioned)

## Resources

- Modal docs: <https://modal.com/docs>
- Modal examples: <https://github.com/modal-labs/modal-examples>
- Cianfhoghlaim burst-training workflow: see the
  `cianfhoghlaim/agents/meaisinfhoghlaim/ocr/ensemble_gradio.py` for a
  working example
