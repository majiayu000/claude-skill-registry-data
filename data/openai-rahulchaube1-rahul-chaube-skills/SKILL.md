---
name: openai
description: Optimization templates for GPT-4o, GPT-4, and Assistants API.
---

# Openai

Optimization templates for GPT-4o, GPT-4, and Assistants API.

## Core Guidelines

- **Structured Outputs**: Use OpenAI's json_schema response options for rigid database structures.
- **Negative Constraints**: Repeat negative rules in the system prompt to enforce compliance.
- **Context Management**: Clean conversation queues before hitting token limitations.
