---
name: component-critic
description: Critique a generated answer against the question and supplied evidence by calling the frozen Executor Model. Use for answer quality checks after generation.
---

# Critic Component

Provide the `critic` capability for an Agentic RAG slot.

## Interface

Input `CritiqueRequest`:

- `query`: original question
- `documents`: selected evidence documents
- `answer`: generated answer
- optional `max_tokens`

Output `CritiqueResult`:

- `approved`: whether the answer is supported and responsive
- `score`: quality score between 0 and 1
- `feedback`: concise overall critique
- `issues`: list of concrete problems, possibly empty

## Execution

Run `scripts/component.py:run(inputs, context)`. The runtime must provide the frozen `context.call_model(...)`. This Component critiques an answer only; it does not retrieve documents, generate a replacement answer, or select another Skill.