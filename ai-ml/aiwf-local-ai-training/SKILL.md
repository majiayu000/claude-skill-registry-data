---
name: aiwf-local-ai-training
description: AIWF local AI training planning and implementation skill. Use for QLoRA, LoRA, fine-tune, adapter training, dataset readiness, VRAM budget, trainer choice, config review, checkpoint and resume plans, export packaging, and post-training validation for LLM, image, video, and multimodal local models.
---

# AIWF local AI training

Use this skill when the hard question is how to train or fine-tune locally. It owns the path from dataset readiness to training plan, checkpoint policy, export, and validation handoff.

## Safety gate

Do not download large models, launch training, reserve GPU time, or overwrite checkpoints unless Shawn explicitly asks. Planning, config review, small file inspection, and dry-run validation are allowed.

## Workflow

1. Read project guidance first: `AGENTS.md`, `PROJECT_SKILLS.md`, training docs, dataset manifests, and existing trainer configs.
2. Classify the run:
   - LLM LoRA or QLoRA.
   - Image LoRA, DreamBooth-style adapter, embedding, or checkpoint fine-tune.
   - Video or multimodal adapter.
   - Dataset preparation only.
3. Read `references/training-readiness.md` before recommending a trainer, hyperparameters, or launch command.
4. Create a training plan when the work is non-trivial:

```powershell
python <this-skill>\scripts\create_training_plan.py --model <model-id-or-path> --method qlora --dataset <dataset-path> --out <plan.json>
```

5. Verify dataset readiness before trainer choice:
   - provenance and license status
   - schema and file format
   - train/validation/test split
   - deduplication and contamination risk
   - token, image, video, or sample count
   - safety and privacy exclusions
6. Build the resource budget:
   - GPU model and VRAM
   - RAM, disk, and cache paths
   - precision and quantization
   - sequence length, image resolution, frame count, batch size, gradient accumulation
   - expected checkpoint size and cadence
7. Choose the trainer only after the dataset and hardware fit. Use source docs for trainer-specific flags. Treat Axolotl, Unsloth, PEFT/Transformers, kohya, EveryDream, Diffusers scripts, and project-local trainers as different contracts.
8. Define checkpoint and resume behavior:
   - non-overwriting output folder
   - save cadence
   - resume source
   - adapter-only versus merged export
   - tokenizer, config, and metadata preservation
9. Define post-training gates:
   - no-GPU config parse
   - tiny dry run only when cheap and requested
   - adapter load smoke through `aiwf-model-loader`
   - eval plan through `aiwf-ai-evals`
   - serving plan through `aiwf-inference-serving` when the model will be hosted

## Output

Report:

- training objective and method
- dataset readiness status
- hardware and VRAM fit
- trainer choice and rejected alternatives
- checkpoint, resume, and export policy
- commands or configs changed
- validation run and remaining blockers

Use `aiwf-agent-mok` when the plan needs source-backed research or findings capture.
