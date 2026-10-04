---
name: ml-stack-model
description: Choose an ML model or provider when a user asks which checkpoint, router, local model, adapter, tokenizer, or inference backend fits a task; compare revisions, license, context, cost, latency, quality, and training compatibility.
---

# Model and provider choice

Require task family, input/output contract, quality threshold, latency/SLA, hardware, budget, privacy boundary, context length, license constraints, and whether the use is inference or training.

## Workflow

1. Enumerate candidate model IDs with exact revision, tokenizer, architecture, context limits, modality, license, and availability.
2. Check task-family fit and training compatibility: tokenizer, adapter target modules, quantization, sequence length, image processor, and framework support.
3. Compare local OpenAI-compatible prefixes, HF Router/provider routes, and direct local inference without implying that a prefix proves model identity.
4. Record model-ID freshness, provider health, cost and latency assumptions, quality evidence, and fallback behavior.
5. Produce a reproducible model decision record with rejected alternatives and hand it to `ml-stack-training`, `ml-stack-evaluation`, or `ml-stack-deployment`.

## Boundary

Do not download, publish, route paid traffic, or mutate provider settings without approval. Do not infer license permissions from a model card summary. Abstain when revision, license, tokenizer, or quality evidence is missing. Next owner: `ml-stack-training` for fine-tuning, `ml-stack-evaluation` for benchmark confirmation, and `ml-stack-deployment` for serving.

See [model selection](references/model-selection.md), [local models](references/local-models.md), [gateway and cost](references/gateway-and-cost.md), and [revision and license](references/revision-and-license.md).
