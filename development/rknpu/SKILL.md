---
name: rknpu
description: >
  RK1 NPU inference pool: 4× rkllama servers using the RK3588S NPU (6 TOPS)
  with Llama-3.1-8B w8a8 model. Covers NPU device mapping (/dev/dri/renderD129),
  Modelfile requirements (FROM + HUGGINGFACE_PATH), Longhorn NVMe storage, and
  LiteLLM least_busy load balancing.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [npu, rk3588s, rkllm, rkllama, litellm, turing-pi]
---

# RK1 NPU Pool Skill

## Stack Overview

| Component | Image | Target Nodes | StorageClass | Model |
|-----------|-------|--------------|--------------|-------|
| NPU Pool Deployments | `ghcr.io/notpunchnox/rkllama:main` | 4× TuringPi 2 RK1 nodes | `longhorn-nvme` (30Gi PVC) | Llama-3.1-8B w8a8 (~8.63 GB on disk) |
| LiteLLM Router | `ghcr.io/berriai/litellm:main-latest` | srv-rk1-nvme-03 | `local-path` | `least_busy` load balancing pool |

---

## Device Mapping (Critical)

The TuringPi 2 RK1 modules (Rockchip RK3588S) expose the 6 TOPS NPU using the DRM interface. The kernel driver maps devices inside `/dev/dri`:

| Device | Driver | Purpose |
|--------|--------|---------|
| `/dev/dri/renderD128` | `rockchip-drm` | Mali GPU (graphics) — **NOT** the NPU |
| `/dev/dri/renderD129` | `RKNPU` | **NPU node** — used by `librkllmrt.so` |

### Configuration Rule
Always mount `/dev/dri` (the whole directory) into the pod and use `privileged: true`. The `librkllmrt.so` runtime version 1.2.3 auto-scans `/dev/dri/` and binds to the correct RKNPU driver at `renderD129` automatically. Do NOT try to mount only `renderD129`.

---

## Modelfile Requirements

`rkllama` uses standard `python-dotenv` under the hood to parse `Modelfile`. Therefore, a standard Ollama-style Modelfile will **fail** to parse unless it is written as standard key-value environment variables.

### The Correct Modelfile Format:
```ini
FROM=Llama-3.1-8B-Instruct_w8a8_g128_rk3588.rkllm
HUGGINGFACE_PATH=meta-llama/Llama-3.1-8B-Instruct
```

- **FROM**: Name of the `.rkllm` binary file inside the model directory `/opt/rkllama/models/llama-3.1-8b-instruct/`.
- **HUGGINGFACE_PATH**: The base repository to load tokenizers from (e.g. `meta-llama/Llama-3.1-8B-Instruct`).

---

## Context Length Limit (Crucial)

The compiled `.rkllm` model has a hard-coded context limit determined at compilation time:
- **Max context limit**: `4096` tokens.

⚠️ **WARNING**: If `num_ctx` is configured higher than `4096` (e.g. `8192` via `RKLLAMA_MODEL_DEFAULT_NUM_CTX` environment variable), the model initialization will fail with:
`E rkllm: max_context[8192] must be less than the model's max_context_limit[4096]`

Always keep `RKLLAMA_MODEL_DEFAULT_NUM_CTX` set to **`4096`** or lower.

---

## Deployment & Verification

### Deploy/Upgrade NPU Pool:
```bash
make ai-npu-pool
```

### End-to-End Verification:
Run the customized verification script to check status, verify the Modelfile, and execute a chat completion test on all 4 NPU nodes:
```bash
./scripts/test-npu-pool.sh
```

### Manual Curl Test inside a Pod:
```bash
kubectl exec -n ai <pod-name> -c rkllm-inference -- \
  curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.1-8b-instruct","messages":[{"role":"user","content":"hola"}],"max_tokens":15}'
```

---

## Troubleshooting

### "missing FROM or HUGGINGFACE_PATH" / "Modelfile not found"
- Verify that `/opt/rkllama/models/llama-3.1-8b-instruct/Modelfile` exists.
- Ensure it contains `=` key-value formats rather than spaces: `FROM=...` and `HUGGINGFACE_PATH=...`.

### "Unexpected Error loading the model"
- Check the pod logs for NPU initialization issues:
  ```bash
  kubectl logs -n ai deployment/rk1-npu-01 -c rkllm-inference --tail=50
  ```
- Look for `E rkllm: max_context[...]` errors or LPDDR4X out-of-memory errors on the physical node.
