---
name: mlx-model-repo-audit
description: >
  Audit Hugging Face or local model repositories before MLX conversion or inference. Use this skill when the user asks whether a model is MLX-compatible, which MLX stack to use, whether an MLX Community variant exists, or how a fine-tuned checkpoint differs from a base model. It covers repo files, config/tokenizer/processor/chat template, adapters, task type, licensing, and conversion risk. Do not use it for actually converting, benchmarking, or troubleshooting after a concrete error unless the repo has not been audited yet.
compatibility: Cross-platform open skill format. Designed for agents working with Apple MLX, Hugging Face model repos, mlx-lm, mlx-vlm, and mlx-embeddings.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

MLX success is usually decided before conversion starts. A model repo may already have an MLX variant, may be loadable by an existing MLX library, may require a straightforward checkpoint conversion, or may need an architecture port. This audit prevents wasted work and prevents using a text-only tool on a vision/audio model.

## Task

Produce an evidence-based model audit and recommend the next MLX action.

Use this skill for:
- Hugging Face model IDs, local model folders, and MLX Community variants.
- Choosing between `mlx-lm`, `mlx-vlm`, `mlx-embeddings`, another MLX package, or upstream porting.
- Comparing a fine-tuned model with its base model before conversion.
- Identifying tokenizer, processor, chat template, generation config, special token, adapter, quantization, and license risks.

Do not perform conversion in this skill. Stop after a clear recommendation, risk list, and next commands for the relevant follow-up skill.

## Required inputs

Ask for missing inputs only if they block the audit:
- Model ID or local path.
- Intended task: chat/completion, image-text generation, audio/video, embedding, reranking, classification, etc.
- Target machine constraints if available: chip, RAM, storage, desired latency.
- Optional base model ID for fine-tunes or adapters.
- Optional sample prompt or media input for later validation.

## Audit workflow

1. **Classify the model task.** Use repo metadata, `config.json`, model card, file names, and pipeline tags. Treat image/audio/video processors as decisive evidence that the model is not a plain LLM.
2. **Search for existing MLX support.** Check the original repo, `mlx-community`, model-card tags such as `mlx`, and any converted variants. Prefer an existing maintained MLX conversion over re-converting.
3. **Choose the MLX stack.**
   - Text-only causal/seq2seq LLM: `mlx-lm`.
   - Vision-language, image-text-to-text, video, audio, omni: `mlx-vlm` or a task-specific MLX repo.
   - Embeddings and rerankers: `mlx-embeddings` when supported.
   - Unknown architecture: inspect current upstream support before porting.
4. **Inspect files that must survive conversion.** Look for `config.json`, `generation_config.json`, tokenizer files, `chat_template.json` or tokenizer chat template, `preprocessor_config.json`, `processor_config.json`, `image_processor_config.json`, `video_processor_config.json`, `feature_extractor_config.json`, adapter files, and safetensors index files.
5. **Compare base and fine-tune.** For fine-tunes, compare architecture fields, tokenizer vocab size, special tokens, processor configs, generation settings, and adapter/merge status. A fine-tune with unchanged architecture is a conversion candidate; changed architecture or custom code raises porting risk.
6. **Identify trust and license constraints.** Note `trust_remote_code`, license, gated/private access, adapter licenses, and whether upload/reuse is allowed.
7. **Decide the next action.** Recommend one of: run existing MLX model, convert with a specific MLX stack, first create a PyTorch baseline, request upstream support, or port architecture.

## Output format

Use this structure:

```markdown
# MLX repo audit: model-id-or-path

## Recommendation
- Stack: mlx-lm, mlx-vlm, mlx-embeddings, existing MLX model, or port needed
- Action: exact next action
- Confidence: high, medium, or low with reason

## Evidence checked
- Model card / repo files:
- Current MLX variants found:
- Base model relationship:
- Required non-weight files:

## Compatibility assessment
| Area | Finding | Risk | Follow-up |
|---|---|---|---|
| Architecture |  |  |  |
| Tokenizer/chat template |  |  |  |
| Processor/media preprocessing |  |  |  |
| Generation config |  |  |  |
| Weights/adapters |  |  |  |
| License/access |  |  |  |

## Next commands to verify
Commands are candidates; verify current CLI help in the active environment before running.

## Stop conditions
Conversion should not start until the stack and baseline validation plan are clear.
```

## Command patterns

Use these as starting points, not as frozen syntax:

```bash
python -m pip install -U mlx mlx-lm mlx-vlm mlx-embeddings huggingface_hub transformers
python -m mlx_lm.generate --help
python -m mlx_lm.convert --help
python -m mlx_vlm.generate --help
python -m mlx_vlm.convert --help
```

Check repository files with the bundled helper when `huggingface_hub` is available:

```bash
python scripts/audit_hf_repo.py XunmeiLiu/VFIG-4B --base Qwen/Qwen3-VL-4B-Instruct
```

For local folders:

```bash
python scripts/audit_hf_repo.py /path/to/local/model --base /path/to/base/model
```

## Boundaries

- Do not claim a model is MLX-compatible just because it is Qwen, Llama, or Transformers-compatible. Confirm the relevant MLX library supports that architecture and task.
- Do not route a VLM through `mlx-lm` unless the user explicitly wants only the language-model subcomponent inspected. VLM processors and media tokens are part of model behavior.
- Do not skip tokenizer or processor inspection. Output differences often come from preprocessing and chat templates rather than weight conversion.
- Do not recommend uploading converted weights until licensing, validation, and model-card notes are complete.

## Examples

**VLM fine-tune**

Input: `XunmeiLiu/VFIG-4B`, base `Qwen/Qwen3-VL-4B-Instruct`, goal scientific figure to SVG.

Good recommendation: “Use `mlx-vlm` as the first conversion path because the model is Qwen3-VL-derived and its task requires image preprocessing. Create a Transformers baseline from the official model card, confirm the generated SVG extraction behavior, then attempt MLX-VLM conversion. Do not use the text-only `transformers-to-mlx` LLM skill except as architecture reference.”

**Text LLM**

Input: `Qwen/Qwen3-4B-Instruct-2507`, goal local chat.

Good recommendation: “Check for an `mlx-community` variant first. If absent, use `mlx-lm` conversion or direct load depending on current support, preserve tokenizer and generation config, then validate with deterministic prompts.”
