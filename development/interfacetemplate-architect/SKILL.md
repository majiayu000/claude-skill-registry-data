---
name: interface/template-architect
description: Define and validate Ollama Modelfile TEMPLATE blocks (Jinja2 layout), including chat format detection and syntax validation. Use to translate TEMPLATE directives into safe prompt structures.
---

# Template Architect

Capabilities
- detect_chat_format: identify ChatML/Alpaca/Llama3-style formats.
- construct_jinja2_layout: build {{ .System }}, {{ .Prompt }}, {{ .Response }} blocks.
- validate_template_syntax: basic sanity check for braces/variables.

Dependencies
- memory-linker (optional for persona tokens)

Outputs
- validated template string and format metadata.
