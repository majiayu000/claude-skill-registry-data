---
name: fine-tune
description: |
  Train custom LLM models locally using conversations exported from LibrAgent.
  Use when the user requests to fine-tune a model, train on past chats, export chat datasets,
  or configure custom agent models.
  Triggers on: "fine-tune model", "모델 학습시켜줘", "내 대화 데이터로 학습해줘", "export dataset", "대화 데이터셋 추출".
---

# Fine-Tune

Export conversational data from LibrAgent and fine-tune a local language model (LLM) with it.

This skill automates the data extraction, hardware pre-flight checks, and training orchestration utilizing Llama-Factory.

## Quick Process

1. **Export Dataset** — Call `history__exportDataset` to extract chats in ShareGPT or Alpaca format.
2. **Pre-flight Check** — Validate local CPU/GPU, VRAM, and CUDA environments.
3. **Orchestrate Training** — Execute `train.py` to initiate Llama-Factory CLI.
4. **Deploy Model** — Update assistant configurations to point to the newly fine-tuned local model.

## Workflow

### 1. Export Dataset
Use the history builtin to export data (requires the `history` optional capability):

```json
history__exportDataset({
  "format": "llamaFactory",
  "outputPath": "workspace/datasets/finetune_data.json",
  "filters": {
    "minTurns": 2,
    "excludeErrors": true,
    "excludeShort": true
  }
})
```

To export a subset, call `history__listSessions` or `history__searchHistory` first and pass `sessionIds`.

### 2. Run Pre-flight Check & Train
Execute the helper script to verify resources and launch training:

```bash
python scripts/train.py --data_path workspace/datasets/finetune_data.json --output_dir workspace/models/finetuned_model
```

### 3. Apply Fine-tuned Model
Once training completes, update the Assistant configuration to load the model path (e.g., via llama.cpp, Ollama, or local Hugging Face model settings).

## Guidelines

- **Hardware Safety** — Always run pre-flight checks. If VRAM is less than 12GB, default to LoRA parameter-efficient training with low batch size.
- **Privacy** — Ensure no credentials or API keys exist in the exported dataset before launching training.

## References

- [Hardware guide](references/hardware-guide.md)
- [Llama-Factory setup](references/llama-factory-setup.md)
