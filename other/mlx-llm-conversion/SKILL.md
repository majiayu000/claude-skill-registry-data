---
name: mlx-llm-conversion
description: >
  Convert, run, and validate text-only language models with Apple MLX and mlx-lm. Use this skill when the user asks about LLM chat/completion models, Hugging Face causal language model checkpoints, mlx-lm generation, text-only quantized MLX variants, or uploading an LLM conversion. Do not use it for vision-language, audio/video, embedding, reranker, diffusion, or processor-dependent multimodal models; route those to the relevant MLX skill first.
compatibility: Cross-platform open skill format. Intended for Apple Silicon MLX workflows using mlx-lm and Hugging Face language model repos.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

`mlx-lm` is the default MLX stack for text-only language models. It can load supported Hugging Face LLM architectures, generate/chat locally, convert weights, quantize, fine-tune, and upload converted repos. It is not a general multimodal converter.

## Task

Help an agent run or convert a text-only LLM safely with `mlx-lm`, while preserving tokenizer behavior and validating output before claiming success.

Use this skill after the model repo audit confirms a text-only LLM or an existing `mlx-community` LLM variant.

## Inputs

- Model ID or local path.
- Whether the goal is run-only, convert, quantize, fine-tune, or package.
- Target output path for converted weights.
- Sample prompts and expected behavior.
- Target machine constraints such as RAM and desired speed.

## Workflow

1. **Confirm scope.** Ensure the model is text-only. If files include image/audio/video processors or the task is image-text generation, stop and use the VLM skill.
2. **Prefer existing MLX variants.** Search for a maintained `mlx-community` or author-provided MLX model. Use it if it matches the task and license.
3. **Check current CLI/API.** Install or update `mlx-lm`, then run help in the active environment because CLI options evolve.
4. **Create a baseline.** Run a small deterministic Transformers or known-reference generation when possible. Save prompt, settings, and output.
5. **Convert without quantization first when quality matters.** A full-precision or bf16 conversion gives a cleaner baseline for diagnosing problems.
6. **Preserve non-weight files.** Tokenizer files, chat template, special tokens, and generation config are part of behavior.
7. **Load and generate from the MLX model.** Conversion success is not enough; generation must work.
8. **Quantize only after a baseline passes.** Use the quantization skill for precision choice and quality checks.
9. **Record commands and artifacts.** Save environment versions, exact model IDs, revisions, local paths, prompts, outputs, and errors.

## Command patterns

Verify current help before running:

```bash
python -m pip install -U mlx mlx-lm transformers huggingface_hub
python -m mlx_lm.generate --help
python -m mlx_lm.convert --help
```

Run an existing MLX model:

```bash
python -m mlx_lm.generate \
  --model mlx-community/Qwen3-4B-Instruct-2507-4bit \
  --prompt "Explain MLX unified memory in two sentences."
```

Convert a Hugging Face LLM to a local MLX folder:

```bash
python -m mlx_lm.convert \
  --hf-path Qwen/Qwen3-4B-Instruct-2507 \
  --mlx-path ./models/qwen3-4b-instruct-mlx
```

Quantized conversion pattern:

```bash
python -m mlx_lm.convert \
  --hf-path Qwen/Qwen3-4B-Instruct-2507 \
  --mlx-path ./models/qwen3-4b-instruct-mlx-4bit \
  -q
```

Python API pattern:

```python
from mlx_lm import load, generate

model, tokenizer = load("./models/qwen3-4b-instruct-mlx")
messages = [{"role": "user", "content": "Summarize why tokenizer files matter."}]
prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
text = generate(model, tokenizer, prompt=prompt, verbose=True)
print(text)
```

## Validation

A conversion is acceptable only when these checks pass:

- The MLX model loads without missing/unexpected critical weights.
- A deterministic prompt generates coherent text.
- Tokenizer and chat template produce the expected prompt format.
- Special tokens are preserved and generation stops correctly.
- Output is compared with the baseline for behavior, not exact token equality unless deterministic parity is realistic.
- Quantized output passes the chosen quality checks if quantization was used.
- Run notes include commands, versions, and local paths.

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Unsupported architecture | `mlx-lm` lacks model class | Search current issues/PRs; use existing MLX variant; port only if needed |
| Model loads but output is garbage | Wrong tokenizer/chat template/special tokens or VLM routed as LLM | Inspect tokenizer files and prompt rendering; rerun repo audit |
| Missing or unexpected keys | Architecture mismatch, tied weights, adapter state, sharded index issue | Compare config with base; test unquantized; inspect safetensors index |
| Converted model works but quantized model degrades badly | Precision/group size too aggressive | Use the quantization skill; back off to 8-bit or bf16 |
| Upload rejected or inappropriate | License/gated repo/auth issue | Use packaging skill and confirm license before upload |

## Done condition

Stop when the model can be loaded and tested locally, or when a specific blocker is documented with evidence and a recommended next step. Do not claim success after download or conversion alone.
