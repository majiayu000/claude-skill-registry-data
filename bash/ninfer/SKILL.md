---
name: ninfer
description: Use when serving NInfer models. Manages C++/CUDA LLM server.
---

# NInfer Serving & Runtime Operations

NInfer is a native C++/CUDA inference engine optimized for NVIDIA Blackwell (SM120, RTX 50-series) and Ada Lovelace architectures.

## Architecture & Binary Locations
- Source & Workspace: `/mnt/data/backup/ninfer`
- Build binaries: `/mnt/data/backup/ninfer/build/apps/ninfer-serve` and `/mnt/data/backup/ninfer/build/apps/ninfer`
- Models directory: `/mnt/data/models/`
  - Qwen 3.5 9B Uncensored (HauhauCS): `/mnt/data/models/qwen3_5_9b_uncensored.ninfer`
- Startup script: `/mnt/data/backup/ninfer/run_serve_qwen9b_128k.sh`

## Managing ComfyUI VRAM
When VRAM is constrained before launching NInfer:
```bash
# Soft empty cache and model unload on ComfyUI (drops VRAM from ~4.1GB to ~300MB)
curl -s -X POST http://127.0.0.1:8188/interrupt
curl -s -X POST http://127.0.0.1:8188/free -H "Content-Type: application/json" -d '{"unload_models": true, "free_memory": true}'
```

## Optimal 64k Context + Vision Serving Configuration (RTX 5060 Ti 16GB)
For Qwen 3.5 9B with 64k context (65,536 tokens) and Vision enabled (safer VRAM budget alongside ComfyUI):
- `--vision`: Loads 27-layer Vision Transformer allocations and enables multi-modal image/video inputs.
- `--max-context 65536 --kv-capacity 65536`: Trims KV capacity to 64k, reducing runtime reservation by ~640 MB VRAM.
- NVFP4 KV Cache (`--kv-dtype nvfp4`): Cuts KV payload by ~45.5% compared to INT8.
- MTP Speculative Decoding (`--spec mtp --draft-tokens 3 --lm-head-draft`): Delivers 140-155 tok/s decode on consumer hardware (~75% acceptance rate).
- GDN Recurrent State: 24 layers of Gated DeltaNet are bounded O(1) in context length, requiring negligible state memory (~48 MB per slot).

### Launching via Detached Session (tmux)
```bash
tmux new-session -d -s ninfer_serve '/mnt/data/backup/ninfer/run_serve_qwen9b_128k.sh > /mnt/data/backup/ninfer/serve-128k.log 2>&1'
```

### Full CLI Parameters
```bash
/mnt/data/backup/ninfer/build/apps/ninfer-serve /mnt/data/models/qwen3_5_9b_uncensored.ninfer \
    --host 0.0.0.0 \
    --port 8090 \
    --max-context 65536 \
    --kv-capacity 65536 \
    --kv-dtype nvfp4 \
    --spec mtp \
    --draft-tokens 3 \
    --lm-head-draft \
    --vision \
    --max-concurrency 2 \
    --device-state-slots 2 \
    --host-state-slots 4 \
    --host-kv-mib 4096 \
    --preserve-thinking \
    --cors
```

## Verification & API Endpoints
- Health Check: `curl http://127.0.0.1:8090/health`
- List Models: `curl http://127.0.0.1:8090/v1/models`
- Chat Completions: `http://127.0.0.1:8090/v1/chat/completions` (OpenAI format, supports image/video)
- Anthropic Messages: `http://127.0.0.1:8090/v1/messages`
