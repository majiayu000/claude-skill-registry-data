---
name: aiwf-ai-pipelines
description: Use to audit or build local AI pipeline wiring across model discovery, loader contracts, backend selection, route registration, runtime preflight, generation or inference stages, saved outputs, API exposure, smoke receipts, and source-to-runtime alignment for image, video, audio, LLM, and multimodal workflows.
---

# AIWF AI Pipelines

## Core Rule

Trace the complete route before changing it: source asset, manifest or registry, loader, runtime stages, preflight, API or callback, output persistence, UI state, and smoke receipt. Prefer local code and receipts over feature-list claims.

## Workflow

1. Read project guidance, route registries, pipeline factories, model inventories, tests, logs, readiness matrices, and recent receipts.
2. Run the bundled read-only crawler when it fits:

```powershell
python <this-skill>\scripts\audit_backend.py --root <project-root> --out <audit-dir>
```

3. Classify each route state as `smoked`, `registered`, `metadata-only`, `broken-runtime`, or `blocked-cleanly`.
4. Identify the first broken contract: missing asset, unsupported format, loader mismatch, stage wiring, API shape, cancellation/progress, output path, or stale status documentation.
5. Read `references/model-source-checks.md` before making model-card, paper, fine-tune, or quantization claims.
6. Patch the smallest coherent boundary, then run a no-GPU or tiny probe before any expensive generation.

## Guardrails

- Do not download models, start training, or run VRAM-heavy generation unless Shawn asks.
- Treat Diffusers snapshots, single-file safetensors, GGUF, ONNX, TensorRT plans, adapters, and native upstream runtimes as different contracts.
- Do not choose a quantization preset as a universal default. Match format, backend, hardware, quality target, calibration requirements, and local support through `aiwf-model-loader`.
- Keep source facts separate from local inference. Use official model cards, upstream repositories, papers, and current local artifact receipts.
- Do not advertise a route that only has metadata or clean failure handling as implemented generation.
- Add `aiwf-ui-electrician` when the backend works but client state, progress, cancellation, errors, or outputs do not travel end to end.
- Use `aiwf-debug-agent-swarm` only when independent lanes justify subagents; subagents report findings and do not edit by default.

## Output

Report artifacts and sources reviewed, route state, findings by severity, files changed, checks and results, and remaining asset or runtime gaps.
