---
name: component-classifier
description: Classify a RAG request into a constrained execution route by calling the frozen Executor Model. Use inside an Agentic workflow before route-specific retrieval or processing.
---

# Classifier Component

Provide the `classifier` capability for an Agentic RAG slot.

## Interface

Input `ClassificationRequest`:

- `query`: original question
- optional `documents`: JSON-compatible candidate documents
- optional `constraints`: routing constraints from the request
- optional `classification_mode`: `retrieval` (default) or `complexity`
- optional `max_tokens`

Output `ClassificationResult`:

- `route`: one of `lexical`, `semantic`, or `hybrid` in `retrieval` mode; one
	of `non-retrieval`, `single-step`, or `multi-step` in `complexity` mode
- `reason`: concise explanation for the selected route
- `confidence`: number between 0 and 1

## Execution

Run `scripts/component.py:run(inputs, context)`. The runtime must provide the frozen `context.call_model(...)`. This Component selects only a constrained route; the Agentic workflow owns the mapping from route to concrete Component slots. Use `complexity` mode for Hybrid Agentic RAG.