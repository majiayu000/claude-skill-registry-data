---
name: mlx-hub-packaging
description: >
  Package, document, and optionally upload successful MLX model conversions for reuse on Hugging Face or local teams. Trigger when the user asks to publish an MLX conversion, write a model card, prepare an MLX Community-style repo, preserve tokenizer or processor files, upload quantized variants, or make conversion notes reproducible. Do not use it before the model has loaded and passed validation with the relevant MLX stack.
compatibility: Cross-platform open skill format. Intended for MLX model repos produced by mlx-lm, mlx-vlm, mlx-embeddings, and Hugging Face Hub workflows.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

A packaged MLX model should let another user reproduce the run without guessing. Packaging is not just weights: tokenizer, processor, generation config, conversion commands, validation evidence, license, and limitations are part of the deliverable.

## Task

Prepare a successful MLX conversion for local reuse or Hugging Face upload, with documentation and validation evidence.

## Preconditions

Use this skill only after:
- The model loads locally with the intended MLX stack.
- At least one task-representative validation run passes.
- Quantization, if used, passes the quality bar.
- License and access constraints are understood.

## Inputs

- Local converted model path.
- Source model ID and revision.
- MLX stack and version used.
- Conversion command and quantization settings.
- Validation prompts/media/queries and outputs.
- Intended repo name or local package destination.
- License and attribution requirements.

## Packaging workflow

1. **Inspect required files.** Check that weights, config, tokenizer files, processor files, chat template, generation config, and README/model card are present as appropriate for the task.
2. **Remove accidental files.** Exclude logs with secrets, caches, raw private prompts, giant benchmark artifacts, and local paths that should not ship.
3. **Write README/model card.** Include source model, MLX stack version, conversion command, quantization settings, usage command, validation evidence, limitations, license, and citations/links.
4. **Add task-specific usage examples.** VLM examples must include media arguments and prompt format. Embedding examples must show vector shape or reranking score usage.
5. **Validate package locally.** Load from the packaged path, not the working conversion directory.
6. **Upload only when appropriate.** Confirm license, gated-source handling, and repo naming. Use CLI/API upload commands after validation.

## Required README sections

```markdown
# Model name MLX

## Source model
- Source:
- Revision:
- License:

## Conversion
- MLX stack:
- Package versions:
- Command:
- Quantization:

## Usage
Runnable command or Python snippet.

## Validation
Prompt/media/query, settings, observed output, and pass criteria.

## Limitations
Known failures, unsupported tasks, quality caveats, hardware caveats.

## Reproducibility notes
Environment, paths, dates, checksums if available.
```

## Command patterns

Validate package contents:

```bash
python scripts/check_mlx_package.py ./models/my-mlx-model --task vlm
```

Upload patterns vary by stack. Confirm help and license before running:

```bash
python -m mlx_lm.convert --help
huggingface-cli upload my-user/my-model-mlx ./models/my-model-mlx
```

Some conversion CLIs can upload directly; prefer explicit local validation before direct upload.

## Package checks by task

| Task | Required beyond weights |
|---|---|
| LLM | tokenizer files, chat template, generation config, config |
| VLM/audio/video | processor and preprocessor/image/audio/video config, tokenizer, chat template, generation config |
| Embedding | tokenizer or processor, pooling/normalization notes, vector dimension |
| Reranker | tokenizer/processor, input pair format, scoring interpretation |

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Packaged folder fails but working folder works | Missing copied processor/tokenizer/config file | Compare file lists; rerun local package check |
| Users reproduce different output | Missing generation settings or chat template difference | Include exact usage and settings; preserve generation config |
| Upload should not be public | Source license/gated model restrictions | Keep local/private; document constraints |
| Model card overclaims quality | Validation too small or failed cases omitted | State scope and limitations honestly |

## Done condition

Stop when a clean package can be loaded from its final location, usage instructions run, validation evidence is documented, and upload/license decisions are explicit.
