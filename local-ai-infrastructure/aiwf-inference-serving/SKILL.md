---
name: aiwf-inference-serving
description: AIWF inference serving skill for local model runtimes. Use for vLLM, llama.cpp server, Ollama, OpenAI-compatible APIs, model endpoint health, auth and network binding, telemetry, queueing, reload and unload behavior, batching, latency, stability checks, and serving handoff from loader or training work.
---

# AIWF inference serving

Use this skill when a model needs to be served, kept online, tested through an API, or diagnosed as a local runtime service.

## Safety gate

Do not expose a service to the public network, open firewall rules, publish credentials, or start long-running servers unless Shawn explicitly asks. Localhost checks and config review are allowed.

## Workflow

1. Read project guidance, service scripts, launchers, Docker or WSL notes, and current port conventions.
2. Identify the serving runtime:
   - vLLM
   - llama.cpp server
   - Ollama
   - Transformers or Diffusers API worker
   - FastAPI, Gradio, or project-local OpenAI-compatible wrapper
3. Read `references/serving-checklist.md` before changing launch commands or endpoint code.
4. Create a serving plan for non-trivial work:

```powershell
python <this-skill>\scripts\create_serving_plan.py --runtime vllm --model <model-path> --port 8000 --out <plan.json>
```

5. Verify model loading constraints with `aiwf-model-loader` when the server load path depends on dtype, quantization, GGUF metadata, LoRA state, tokenizer, projector, or context length.
6. Verify service contract:
   - bind address and port
   - auth or local-only boundary
   - health endpoint
   - OpenAI-compatible paths when advertised
   - model list endpoint
   - generation endpoint
   - streaming support
   - error shape
7. Verify runtime operations:
   - startup and shutdown
   - reload and unload
   - queueing and concurrency
   - cancellation where supported
   - telemetry freshness
   - log path and crash visibility
8. Verify cheaply first with health probes, `/v1/models`, tiny prompt calls, and log inspection. Run load or latency loops only when Shawn asks.

## Output

Report:

- runtime and model
- exact launch command or config
- endpoint URLs checked
- local-only or auth boundary
- telemetry and queueing status
- smoke command and result
- remaining stability risks

Use `aiwf-ai-evals` for benchmark or before/after promotion gates after the service is reachable.
