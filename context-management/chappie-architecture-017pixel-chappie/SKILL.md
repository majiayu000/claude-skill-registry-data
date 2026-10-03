---
name: chappie-architecture
description: CHAPPiE's brain, memory, and life simulation architecture. Use when modifying core pipelines, brain agents, steering, or global workspace.
---

# CHAPPiE Architecture

## Active request path

```text
API / CLI / Research
  -> web_infrastructure.chappie_runtime.CHAPPiERuntime
  -> TurnPipeline and TurnContext
  -> Brain, Memory, Life, Global Workspace
  -> GenerationGateway -> vLLM and Steering
  -> formatting and persistence
```

`web_infrastructure/backend_wrapper.py` is only a compatibility layer. Keep `create_chappie_backend`, `init_chappie`, `CHAPPiERuntime` and `CHAPPiEBackend` compatible.

Sync and streaming must build the same `TurnContext`, share preparation and finalization, and differ only at the output adapter.

## Boundaries

- Runtime orchestrates; it does not duplicate Memory or Life semantics.
- `brain/global_workspace.py` selects and broadcasts active signals.
- `brain/action_response.py` creates prompt and action context.
- `brain/steering_manager.py` owns VAD, alpha, composite modes and layer profiles.
- `brain/steering_backend.py` performs activation injection.
- `memory/` owns STM, LTM, retrieval, context files, sleep and forgetting.
- `life/` owns homeostasis, goals, habits, attachment, time and development.

There are ten emotions in `config/emotions.py`. The Qwen 3.5 4B profile steers layers 10 through 26.

## Historical v1

The multi-agent `BrainPipeline` is not production. Exact sources are under `Legacy-Code/brain-pipeline-v1/`; `brain/brain_pipeline.py` is a lazy compatibility loader. Historical agents must not be imported by the active runtime. Do not move or archive active steering with those agents.

## Compatibility rules

- Preserve external API, SSE, CLI and persisted-data contracts.
- Do not reorder Intent, Memory, Life, Workspace, generation or finalization without a regression test.
- Treat provider priority, emotion mapping, sleep behavior and storage changes as separate migrations.
- Keep service and payload versions independent from the product version.

## Required checks

```bash
python3 tests/test_runtime_architecture.py
python3 tests/test_local_first_runtime.py
python3 tests/test_life_simulation.py
python3 tests/test_reasoning_layering.py
```
