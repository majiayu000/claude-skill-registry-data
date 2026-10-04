---
name: LoRAStyleTrainingLibrary
description: Isolated LoRA style training library for DESIGNOSFORGE, including dataset ingestion, captions, style tokens, train configs, and adapter manifests.
---

# LoRAStyleTrainingLibrary

Use inside DESIGNOSFORGE when the task matches this capability.

Core rules:
- Explicitly preserve DESIGNOSFORGE activation.
- Keep the three-step inference process.
- Do not generate final images before user confirmation.
- Feed constraints into PromptOrchestrationEngine and QAAgent.
- Reserve aesthetic corpus space by design domain and style axis before training; store real case images, reference images, rejected examples, captions, manifests, and quality reviews separately.
- Do not track training images, generated private assets, model weights, or unknown-rights references in git.
- Keep outputs executable, traceable, and delivery-ready.
