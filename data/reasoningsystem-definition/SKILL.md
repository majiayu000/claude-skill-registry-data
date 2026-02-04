---
name: reasoning/system-definition
description: Draft and enforce system-level persona/rules for Ollama SYSTEM blocks. Use to translate role/constraints into Modelfile SYSTEM text.
---

# System Definition

Capabilities
- draft_persona_manifest: convert roles into strict system text.
- inject_operational_constraints: embed rules (e.g., no emojis, JSON-only).
- validate_system_scope: ensure constraints are explicit and bounded.

Dependencies
- tangible-memory (persist persona)
- guardrails-control (optional)

Outputs
- finalized SYSTEM text for Modelfile/system prompt.
