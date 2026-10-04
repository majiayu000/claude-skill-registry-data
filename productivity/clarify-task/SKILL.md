---
name: clarify-task
description: Ask clarifying questions before implementing to ensure Python requirements are understood. Use when a task lacks detail, dependencies are unclear, or multiple interpretations are possible.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: planning
  since: "2026-02-25"
---

# Clarify Task

Before implementing any Python work, pause and gather context so the solution matches what’s really needed.

## Steps

1. **Ask focused questions**
   - Data flow, inputs/outputs, and architecture (async vs sync, service vs script)
   - API contracts, dependencies, and integrations
   - Authentication, authorization, and configuration expectations
   - Edge cases, error handling, and rollback requirements
   - UX/CLI expectations if applicable (prompts, flags, logging)

2. **Restate the requirements**
   - Summarize your understanding in plain language
   - Confirm the desired behavior, inputs, and success criteria

3. **Confirm before moving forward**
   - Once you have enough context, ask if you can proceed with planning or implementation
   - If questions remain, repeat steps 1–2 until confident

## Tools

- Use the `AskQuestion` tool to present multiple-choice clarifications when the extra structure helps.
- Keep responses brief and focused; avoid assumptions about unrelated components.
