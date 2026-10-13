---
name: anthropic
description: Optimization guidelines for Claude 3.5 Sonnet, Claude 3.5 Haiku, and Opus.
---

# Anthropic

Optimization guidelines for Claude 3.5 Sonnet, Claude 3.5 Haiku, and Opus.

## Core Guidelines

- **XML Tag Usage**: Structure contexts, inputs, and thinking loops inside XML blocks (e.g. `<instructions>`, `<thought>`).
- **Chain of Thought**: Leverage Claude's reasoning skills by prompting for step-by-step logic.
- **System Prompts**: Utilize the dedicated system prompt block for behaviors.
