---
name: web-world-models
title: "Web World Models"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.23676
keywords: [world-models, simulation, language-models, web-technologies]
description: "Bridge deterministic web code and generative LLMs via hybrid world models. State and physics defined by TypeScript code, LLMs generate narrative/aesthetics on top. Uses typed interfaces, deterministic hashing, graceful degradation—enabling scalable interactive environments from travel atlases to fictional worlds without databases."
---

## Overview

Web World Models combine structured code for invariant state with LLM-driven narrative generation.

## Core Technique

**Two-Layer Architecture:**

```python
# Physics layer (deterministic code)
class Physics:
    inventories: dict  # Code enforces consistency
    coordinates: XYZ

# Imagination layer (LLM-driven)
class Narrative:
    descriptions = llm.generate(physics_state)
    dialogue = llm.generate(context)
```

## References

- Physics layer as TypeScript code
- Imagination layer for aesthetics
- Deterministic hashing for consistency
