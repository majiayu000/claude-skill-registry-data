---
name: local-llm-serving
description: Run local LLMs in production — model/quant choice, serving stacks, VRAM budgets, fallback chains, evaluation.
version: 1
triggers: local llm, run models locally, llama.cpp, model serving, vram, local ai
category: How Milo works
blurb: Run local language models in production — model choice, serving, memory budgets and fallbacks.
archetype: knowledge
example: Help me serve a local model on my own hardware.
---

# Local LLM Serving

Local inference is infrastructure: match the model to the box, serve it safely, and never let it become a single point of failure.

## When to use
- Running llama.cpp / Ollama / GGUF engines on laptop, box, or GPU hosts.
- Choosing models under VRAM/RAM budgets (16GB-class cards, CPU-only fallbacks).
- Building fallback chains that survive one engine going down.

## Method
1. **Workload → budget first**: tasks, context lengths, concurrency → compute + VRAM/RAM budget; remember the KV cache grows with context — leave headroom; quantize deliberately (Q4/Q5/Q8 trade-offs), not by default.
2. **Model selection**: match model size to task (small for routing/summaries, larger for reasoning); check licenses for commercial use before adopting; pin exact versions + checksums (provenance).
3. **Serving stack**: llama.cpp server / Ollama / vLLM-class as fits; run daemonless under systemd (or Windows service) with auto-restart; bind loopback — remote access only via authenticated tunnel.
4. **Performance**: measure tokens/s + time-to-first-token at realistic context; tune offload layers, parallelism; don't overcommit VRAM ("it loads" ≠ "it serves").
5. **Operations**: health endpoint, structured logs, model catalog pinned, disk space monitored for weights; upgrades = backup → swap → verify → rollback path.
6. **Fallback chains**: local primary → local secondary → declared provider; swap models behind a stable API (OpenAI-compatible surface) so apps never change; test each failover deliberately.
7. **Evaluation**: golden task suite per model change (`agent-evaluation`); record quality + speed before promotion; no silent model swaps in production.

## Quality gates
- [ ] VRAM/RAM + context budget documented for each served model.
- [ ] Versions/license pinned and recorded; loopback-only binding verified.
- [ ] Fallback chain tested (fail the primary on purpose).
- [ ] Golden-task evals recorded per model change.

## Red lines
- No unauthenticated exposure of inference ports; no unvetted model licenses; no silent model swaps.

## Related
`agent-infrastructure-ops` · `agent-evaluation` · `non-docker-isolation`.
