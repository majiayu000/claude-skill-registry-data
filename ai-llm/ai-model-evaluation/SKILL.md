---
name: ai-model-evaluation
description: Evaluate model outputs using deterministic schemas, fixtures, and regression metrics. Use when the task concerns ai model evaluation.
---
# Structured model evaluation

Use a fixed, versioned dataset of prompts, expected semantic outcomes and edge cases.
Run a schema validator before comparing semantic content. Track exact-match,
field-level accuracy, invalid JSON, refusal/clarification errors, tool-call failures,
latency and estimated cost. Compare candidate vs baseline on identical inputs and
inference settings. Save anonymized failure examples. Separate deterministic
checks from LLM-as-judge assessments. Require source-data authorization before
transmitting accounting or user data to third-party providers.
