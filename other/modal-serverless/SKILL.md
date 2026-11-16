---
name: modal-serverless
description: Deploy AI workloads to serverless GPU/CPU with Modal — define @app.function with GPU/memory specs, build custom container images, run batch jobs and web endpoints, schedule cron tasks, and use distributed volumes for model caching.
triggers:
  - "modal"
  - "modal serverless"
  - "modal gpu"
  - "modal function"
  - "modal app"
  - "modal deploy"
  - "modal run"
  - "serverless gpu python"
  - "modal volume"
  - "modal image"
  - "modal web endpoint"
  - "modal cron"
  - "modal batch inference"
do_not_use_for:
  - LLM fine-tuning orchestration — use llamafactory instead
  - Workflow automation — use n8n-automation instead
  - Local model serving — use llama.cpp or vLLM directly instead
see_also:
  - llamafactory
  - litellm
  - vllm-paged-attention
---

# Modal — Serverless GPU Compute

**Source:** modal-labs/modal-client (Apache 2.0) — run Python functions on cloud GPUs

## Why Modal

- **Zero infra**: no Kubernetes, no Docker registry, no instance management
- **Pay-per-use**: billed per second of GPU/CPU time — no idle costs
- **Fast cold start**: images cached, containers warm in ~1-2s
- **Built for AI**: GPU types from T4 to H100, persistent volumes for model weights
- **FastAPI integration**: deploy LLM endpoints in 10 lines

## Install

```bash
pip install modal
modal setup          # authenticate with Modal account
```

## Basic Function

```python
import modal

app = modal.App("my-app")

@app.function(cpu=2, memory=4096)
def add(x: int, y: int) -> int:
    return x + y

@app.local_entrypoint()
def main():
    result = add.remote(3, 4)   # runs on Modal cloud
    print(result)               # 7
```

```bash
modal run my_app.py
```

## GPU Function

```python
import modal

app = modal.App("gpu-app")

# Define custom image with dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("torch", "transformers", "accelerate")
)

@app.function(
    gpu="A10G",           # T4 | A10G | A100 | H100 | L4 | any
    memory=16384,         # MB
    timeout=600,          # seconds
    image=image,
)
def run_inference(prompt: str) -> str:
    import torch
    from transformers import pipeline

    pipe = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct",
        torch_dtype=torch.bfloat16,
        device_map="cuda",
    )
    result = pipe(prompt, max_new_tokens=200)
    return result[0]["generated_text"]

@app.local_entrypoint()
def main():
    output = run_inference.remote("Explain transformer architecture:")
    print(output)
```

## Persistent Volume (Model Caching)

```python
import modal

app = modal.App("cached-model-app")

# Volume persists across runs — store model weights here
model_volume = modal.Volume.from_name("model-weights", create_if_missing=True)

image = (
    modal.Image.debian_slim()
    .pip_install("huggingface-hub", "transformers", "torch")
)

MODEL_DIR = "/models"

@app.function(
    gpu="A10G",
    image=image,
    volumes={MODEL_DIR: model_volume},   # mount volume at /models
    timeout=300,
)
def download_model():
    from huggingface_hub import snapshot_download
    snapshot_download(
        "meta-llama/Llama-3.2-3B-Instruct",
        local_dir=f"{MODEL_DIR}/llama-3.2-3b",
        token="your-hf-token",
    )
    model_volume.commit()   # persist changes

@app.function(
    gpu="A10G",
    image=image,
    volumes={MODEL_DIR: model_volume},
    timeout=300,
)
def generate(prompt: str) -> str:
    import torch
    from transformers import pipeline

    pipe = pipeline(
        "text-generation",
        model=f"{MODEL_DIR}/llama-3.2-3b",
        torch_dtype=torch.bfloat16,
        device_map="cuda",
    )
    return pipe(prompt, max_new_tokens=100)[0]["generated_text"]
```

## Web Endpoint (FastAPI)

```python
import modal
from fastapi import FastAPI

app = modal.App("llm-api")
web_app = FastAPI()

image = modal.Image.debian_slim().pip_install("fastapi", "anthropic")

@app.function(image=image, secrets=[modal.Secret.from_name("anthropic-key")])
@modal.asgi_app()
def fastapi_app():
    import anthropic

    client = anthropic.Anthropic()

    @web_app.post("/generate")
    async def generate(prompt: str):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"response": response.content[0].text}

    return web_app
```

```bash
modal deploy llm_api.py
# Returns: https://your-org--llm-api-fastapi-app.modal.run
```

## Batch Inference (Map)

```python
import modal

app = modal.App("batch-app")
image = modal.Image.debian_slim().pip_install("anthropic")

@app.function(image=image, secrets=[modal.Secret.from_name("anthropic-key")])
def process_item(text: str) -> dict:
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize: {text}"}],
    )
    return {"input": text[:50], "summary": response.content[0].text}

@app.local_entrypoint()
def main():
    texts = ["Long article 1...", "Long article 2...", "Long article 3..."]

    # starmap: parallel execution with progress
    results = list(process_item.map(texts, return_exceptions=True))
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            print(r["summary"])
```

## Scheduled Cron Job

```python
import modal

app = modal.App("cron-app")

@app.function(schedule=modal.Cron("0 9 * * *"))   # daily at 9am UTC
def daily_report():
    import smtplib
    # Generate and send daily report
    print("Generating daily report...")
    send_report()

# Or use Period
@app.function(schedule=modal.Period(hours=6))
def refresh_cache():
    rebuild_vector_index()
```

## Secrets Management

```python
import modal

# Create secret via CLI: modal secret create my-secrets KEY=value
# Or via UI: modal.com/secrets

app = modal.App("secure-app")

@app.function(
    secrets=[
        modal.Secret.from_name("anthropic-key"),
        modal.Secret.from_name("database-creds"),
    ]
)
def secure_function():
    import os
    api_key = os.environ["ANTHROPIC_API_KEY"]   # injected by Modal
    db_url = os.environ["DATABASE_URL"]
```

## Class-based Functions (GPU warm pool)

```python
import modal

app = modal.App("warm-gpu")
image = modal.Image.debian_slim().pip_install("torch", "transformers")

@app.cls(
    gpu="A10G",
    image=image,
    container_idle_timeout=300,   # keep warm for 5 min after last request
)
class ModelService:
    def __init__(self):
        import torch
        from transformers import pipeline
        # Loaded once per container — not per call
        self.pipe = pipeline("text-generation", model="gpt2", device="cuda")

    @modal.method()
    def generate(self, prompt: str) -> str:
        return self.pipe(prompt, max_new_tokens=50)[0]["generated_text"]

@app.local_entrypoint()
def main():
    service = ModelService()
    print(service.generate.remote("Hello"))
```

## Anti-Fake-Pass Checks

- [ ] `@app.function` defines the function; `.remote()` calls it on Modal cloud
- [ ] `modal run` for local entrypoint; `modal deploy` for persistent web endpoint
- [ ] Volume changes must call `volume.commit()` to persist — uncommitted changes lost on container exit
- [ ] `@app.cls` loads model in `__init__` once per container — not once per call like `@app.function`
- [ ] `secrets=[modal.Secret.from_name("...")]` — secret must be created in Modal dashboard first
- [ ] `container_idle_timeout` keeps GPU warm to avoid cold starts — costs money during idle
- [ ] `gpu="any"` picks cheapest available GPU — use specific type (A10G/H100) for guaranteed VRAM
