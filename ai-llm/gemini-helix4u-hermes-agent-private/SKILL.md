---
name: gemini
description: Gemini CLI for one-shot prompts, summaries, structured output, and extension-aware calls.
version: 1.0.0
author: local
license: MIT
metadata:
  hermes:
    tags: [Gemini, CLI, Google AI, LLM, One-shot]
---

# gemini

Use Gemini CLI in one-shot mode with a positional prompt.

Core usage
- `gemini "Answer this question..."`
- `gemini --model <name> "Prompt..."`
- `gemini --output-format json "Return JSON"`

Extensions
- List available extensions:
  - `gemini --list-extensions`
- Manage extensions:
  - `gemini extensions <command>`

Auth and safety notes
- If auth is required, run `gemini` once interactively and complete login.
- Prefer one-shot commands for reproducible automation.
- Avoid `--yolo` mode for safety-sensitive workflows.
