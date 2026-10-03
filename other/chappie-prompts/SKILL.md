---
name: chappie-prompts
description: CHAPPiE prompt engineering. Use when modifying system prompts, emotion templates, generation budgets, formatting instructions, or life and training prompt context.
---

# CHAPPiE Prompt Engineering

## Source of truth

All active LLM instructions live in `config/prompts.py`. Runtime, Brain, Memory, Life and Training modules import templates and insert data; they do not maintain duplicate prompt prose.

Relevant groups include:

- persona and neutral system prompts
- generation budget and response-plan instructions
- formatter prompts and visible fallback text
- intent, emotion and query-extraction prompts
- memory consolidation and dream prompts
- life-context template
- trainer prompt and start prompt
- historical agent prompts retained only for v1 compatibility

## Runtime assembly

1. persona or neutral system prompt
2. optional prompt-based emotion status outside activation-steered vLLM
3. answer budget and response plan
4. life and Global Workspace suffix
5. keyword and semantic memories
6. chat history

Local vLLM carries emotions primarily through steering. Groq and Ollama can receive prompt-based state in their supported non-web paths.

## Rules

- Keep instructions compact and non-contradictory.
- Never request or expose private chain-of-thought.
- Preserve parser, sanitizer and external output contracts.
- Formatting prompts may only reorganize whitespace and tagged blocks, not rewrite content.
- Keep dynamic values as explicit format variables.
- Distinguish UI copy, logs and parser patterns from real prompts.
- There is no active Cerebras formatter.
- Ten emotions are defined centrally in `config/emotions.py`.

## Tests

```bash
python3 tests/test_chat_ui_formatting.py
python3 tests/test_reasoning_layering.py
python3 tests/test_response_policy.py
python3 tests/test_settings_integrity.py
```
