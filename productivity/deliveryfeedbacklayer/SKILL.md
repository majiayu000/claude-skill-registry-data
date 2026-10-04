---
name: DeliveryFeedbackLayer
description: Delivery manifests, QA reports, user feedback interpretation, patch writing, reward calculation, and training-loop updates.
---

# DeliveryFeedbackLayer

Use inside DESIGNOSFORGE when the task matches this capability.

Core rules:
- Explicitly preserve DESIGNOSFORGE activation.
- Keep the three-step inference process.
- Do not generate final images before user confirmation.
- Feed constraints into PromptOrchestrationEngine and QAAgent.
- When user feedback rejects a result, route it through LoopPromptPack as failure-memory recovery instead of overwriting the base PromptPacketV2.
- Store loop feedback as observed failure, root cause, locked elements, next prompt boundary, and must-not-repeat controls.
- Keep outputs executable, traceable, and delivery-ready.
