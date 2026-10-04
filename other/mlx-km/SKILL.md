---
name: mlx_KM
description: >
  Route Apple Silicon MLX work to the right specialist workflow. Use this whenever the user says MLX, mlx-lm, mlx-vlm, mlx-embeddings, Apple Silicon model conversion, local Mac model inference, quantization, benchmarking, packaging an MLX model, or debugging MLX failures. This is the umbrella entry point: start here when the stack is unclear, then load the focused MLX skill that matches the actual model/task.
targets: [hermes-default, hermes-gpt, claude-hermes]
metadata:
  hermes:
    command_priority: 80
---
# MLX router

Use this as the first stop for Apple Silicon MLX work. Keep it short: its job is to choose the right specialist skill, not to duplicate all MLX procedures.

## Routing

Start with `mlx-model-repo-audit` when the user gives a Hugging Face repo, local model folder, fine-tuned checkpoint, or asks whether a model is MLX-compatible. Auditing first prevents the common mistake of routing multimodal models through text-only LLM tooling.

Use `mlx-llm-conversion` when the model is a text-only causal/chat LLM and the task is conversion, loading, generation, LoRA/QLoRA/fusion, or `mlx-lm` usage.

Use `mlx-vlm-conversion` when the model consumes images, audio, video, PDFs, screenshots, OCR inputs, scientific figures, or any multimodal processor artifacts. VLM behavior depends on processor files and media token handling, not just weights.

Use `mlx-embedding-reranker` when the output is vectors, similarity scores, retrieval ranking, or document/image embedding rather than generated text.

Use `mlx-quantization-quality` when the user asks about bit width, memory savings, speed/quality tradeoffs, mxfp/nvfp modes, group size, or whether a quantized model is good enough.

Use `mlx-local-benchmarking` when a model already runs and the user wants cold-load time, first-token latency, throughput, peak memory, batch behavior, or variant comparisons on the Mac Studio/MacBook.

Use `mlx-troubleshooting-repro` when there is a concrete error, crash, bad output, missing keys, processor mismatch, OOM, package-version issue, or GitHub issue to file.

Use `mlx-hub-packaging` only after validation passes and the user wants a reusable local package, Hugging Face upload, model card, or MLX Community-style repo.

Use `mlx-speculative-decoding` when the user asks about speculative decoding, draft models, DFlash, MTP drafters, faster generation through speculation, or `--draft-model` for `mlx-lm`/`mlx-vlm`. The skill captures runtime support gaps, decision thresholds, drafter selection, and verified per-chip results so the agent doesn't repeat known-bad experiments.

## Default sequence

For an unknown model, use this sequence:

1. Audit the repo/model.
2. Choose LLM, VLM, or embedding/reranker path.
3. Convert or load a baseline first, ideally unquantized when feasible.
4. Quantize only after baseline behavior is known.
5. Benchmark once the model runs.
6. Package or upload only after validation evidence exists.

## References

Read `references/recommended-suite.md` for the full suite map, `references/research-brief.md` for the ecosystem snapshot, and `references/validation-checklists.md` before claiming a conversion is complete.
