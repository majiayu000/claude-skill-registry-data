---
name: ml-stack-training
description: Design advanced ML training when a user asks for SFT, DPO, GRPO, reward modeling, LoRA, QLoRA, sentence-transformer, vision, checkpointing, Trackio, or HF persistence; emit an executable specification unless an equivalent runtime operation exists.
---

# Training design

Require dataset contract and revision, model revision, objective, evaluation plan, hardware, memory budget, cost ceiling, environment policy, output location, and approval for any remote or paid action.

## Workflow

1. Select SFT, DPO, GRPO, reward modeling, sentence-transformer, or vision classification/detection/segmentation from the task and evidence.
2. Preflight format, tokenizer/processor, sequence/image limits, labels, adapters, precision, accumulation, and memory.
3. Choose LoRA/QLoRA or full updates; define optimizer, schedule, seeds, evaluation cadence, checkpoint retention, and stop rules.
4. Capture PEP 723/UV or repository-native environment, data/model revisions, hardware, cost, and deterministic settings.
5. Specify Trackio/HF persistence and artifact paths without claiming integration; hand a job specification to `ml-stack-compute` and run comparison through `ml-stack-experiment`.

## Boundary and outputs

Never submit paid/remote jobs, upload data, or publish checkpoints without explicit approval. If no registry operation matches training, return a bounded executable training specification and exact handoff, not a fake submission result. Abstain when formats, licenses, resource limits, or validation are unresolved. Next owner: `ml-stack-compute` for execution planning, `ml-stack-experiment` for isolated comparison, `ml-stack-evaluation` for quality, and `ml-stack-hub` for approved artifact storage.

See [method selection](references/method-selection.md), [SFT/DPO/GRPO](references/sft-dpo-grpo.md), [vision training](references/vision-training.md), [job handoff](references/job-handoff.md), and [checkpointing](references/checkpointing.md).
