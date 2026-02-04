---
name: model-selection-orchestrator
description: Select the best local Ollama model for a task and emit tuning presets. Use when choosing between reasoning, creative, fast, vision, synthesis, or pre-AGI modes based on available local models.
---

# Model Selection Orchestrator

Choose an Ollama model based on task intent and emit a consistent tuning preset.

## Workflow

1) List local models with `ollama list`.
2) Map the task to a preference list and pick the first available model.
3) Emit a recommended model, a backup, and a tuning preset.
4) Fall back to the fastest available model when none match.

## Scripts

- Run: python skills/tuning/model-selection-orchestrator/scripts/recommend_model.py --task reasoning

## References

- references/presets.json
