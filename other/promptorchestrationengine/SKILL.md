---
name: PromptOrchestrationEngine
description: PromptPacket orchestration for model-specific design prompts, reference locks, QA gates, and negative constraints.
---

# PromptOrchestrationEngine

Use inside DESIGNOSFORGE when the task matches this capability.

Core rules:
- Explicitly preserve DESIGNOSFORGE activation.
- Keep the three-step inference process.
- Do not generate final images before user confirmation.
- Feed constraints into PromptOrchestrationEngine and QAAgent.
- For v1.5 PromptPacket work, require aesthetic thesis, composition hierarchy, layout grid/density, exact text rules, anti-fragmentation negative prompt, and QA scores before image generation.
- For LoopPromptPack work, treat loop prompts as a separate companion scheme. Do not replace PromptPacketV2. Use the loop pack only for self-refine iteration, failed-result recovery, branch search, visual-result repair, or seamless video loops.
- Each loop iteration changes one axis only, preserves the stable brief, reports critique axes, revision delta, score, and stop-or-continue state.
- Keep outputs executable, traceable, and delivery-ready.
