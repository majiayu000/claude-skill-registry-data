---
name: aiwf-model-loader
description: "Model loader architecture and implementation skill for local AI apps, especially AIWF. Use when coding or reviewing model loading, precision and dtype policy, quantization selection, GGUF/safetensors/Diffusers/Transformers/Nunchaku/vLLM/llama.cpp/TensorRT backend choice, LoRA adapter compatibility, VAE/text-encoder precision, model manifests, preflight checks, loader fallback rules, and runtime tests."
---

# Model Loader

Use this skill when the hard question is how a model should be loaded. It sits between backend pipeline audits and UI connector work: `aiwf-ai-pipelines` asks whether a route is wired, `aiwf-model-loader` defines the loader contract, and `aiwf-ui-electrician` checks whether the UI/API exposes runtime state correctly.

## Workflow

1. Identify the model family, local asset layout, and target hardware before editing loader code.
2. Read `references/source-routing.md` for source priority. Use primary sources when model behavior is uncertain.
3. Read the relevant decision reference:
   - `references/precision-quant-policy.md` for dtype, offload, GGUF, bitsandbytes, AWQ/GPTQ/HQQ, FP8, and component precision.
   - `references/lora-compatibility.md` for LoRA, LyCORIS, adapter, trigger-word, and fuse/unload rules.
   - `references/implementation-contract.md` before changing AIWF model manifests, inventories, loaders, or tests.
4. Create or update a loader contract. Start with:

```powershell
python <this-skill>\scripts\new_loader_contract.py --model-id <id-or-path> --family <family> --backend <backend> --format <format> --out <contract.json>
```

5. Implement only after the contract is clear: discovery, validation, precision map, quantization path, LoRA policy, fallback behavior, and tests.
6. Verify cheaply first: config/header parsing, manifest validation, preflight errors, import/construct checks, unit tests, and route-level no-GPU tests. Run real VRAM generation only when the user asks.

## Loader Contract

Every loader decision should be traceable to a contract with these fields:

- `model_id`, `local_path`, `family`, `format`, `architecture`, `source_urls`.
- `asset_layout`: required files, optional files, split components, VAE/text encoder/tokenizer paths, GGUF projector files.
- `backend`: native upstream, Diffusers, Transformers, llama.cpp, vLLM, Nunchaku, TensorRT, ONNX, or external API.
- `precision_policy`: dtype per component, offload rules, prompt-encoding device, VAE dtype, and unsupported dtype reasons.
- `quantization_policy`: quant format, minimum viable quant, preferred quality quant, calibration/imatrix needs, and backend support.
- `lora_policy`: compatible base models, adapter formats, target modules, scale range, trigger words, fuse/unload behavior, and rejection rules.
- `preflight`: checks that can fail cleanly before loading weights.
- `fallbacks`: allowed fallbacks and forbidden silent fallbacks.
- `tests`: no-GPU tests, loader smoke tests, and optional full generation tests.

## Coding Rules

- Do not collapse every model into Diffusers when the original source requires native inference or a custom loader path.
- Do not silently coerce precision. If a component needs FP32/BF16/FP16/INT8/NF4, make that explicit.
- Treat GGUF, safetensors, Diffusers snapshots, Nunchaku artifacts, and adapters as different runtime contracts.
- Keep base weights, VAEs, text encoders, tokenizers, projectors, and LoRAs separate in discovery and validation.
- Prefer clear unsupported-state errors over fake support that fails after model load.
- Preserve user-selected precision only when the backend and component support it.
- Record the reason for `cache`, offload, CPU prompt encoding, or GPU prompt encoding decisions when they affect runtime behavior.

## Related Skills

Use `aiwf-ai-pipelines` for broader route readiness, `aiwf-inference-serving` for server-specific format support, `aiwf-nvidia-cuda-cudnn-sdk` for TensorRT or CUDA implementation details, `aiwf-gpu-runtime-diagnostics` for environment failures, and `aiwf-ui-electrician` for exposing loader state to the UI. Installed external format-specific skills may supplement current official runtime documentation, but this skill must not depend on an unverified external skill name.
