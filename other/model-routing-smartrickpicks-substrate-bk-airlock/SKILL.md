---
name: model-routing
description: Intelligent model selection (Opus/Sonnet/Haiku) based on task complexity and chamber
---

# Model Routing

Select the right Claude model for each task based on complexity, chamber, and cost budget. Prevents Opus spend on tasks Haiku can handle and prevents Haiku misroutes on tasks that require deep reasoning.

## Integration

This skill integrates with Airlock's chamber and persona system from `airlock-persona`. Routing decisions are informed by the active chamber (`Discovery / Build / Verify / Ship`) and can be logged to session state via `session-manager.py` for cost tracking.

## Standalone Behavior

- Default to Sonnet for all Build and Verify chamber work where quality and speed are both required
- Route to Haiku for high-frequency, low-complexity operations: classification, extraction, formatting, short-form generation
- Reserve Opus for Discovery chamber deep research, architectural decisions, and any task where the quality gap between Sonnet and Opus is measurable and consequential
- Always state the routing decision and its rationale in the presence line when switching models mid-task
- When cost budget is constrained, prefer Haiku over Sonnet for any task that passes a quality check on a sample output
