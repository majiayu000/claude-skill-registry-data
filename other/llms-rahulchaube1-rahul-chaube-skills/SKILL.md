---
name: llms
description: Large Language Model configurations, hyperparameter settings, and integrations.
---

# Llms

Large Language Model configurations, hyperparameter settings, and integrations.

## Core Guidelines

- **Parameter Bounds**: Select temperatures based on task type (e.g., 0.0 for code/logic, 0.7 for creative content).
- **Structured Outputs**: Force models to return JSON or structured schemas when parsing programmatically.
- **Token Budget**: Monitor prompt sizes to prevent truncation or context window exhaustion.
