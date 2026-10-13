---
name: reasoning
description: Logical Chain-of-Thought (CoT) and cognitive planning workflows.
---

# Reasoning

Logical Chain-of-Thought (CoT) and cognitive planning workflows.

## Core Guidelines

- **Chain of Thought**: Document your logic step-by-step using internal thinking nodes before generating output.
- **Hypothesize**: List 2-3 potential causes for a bug before altering any code.
- **Self-Correction**: If a test or build fails, read the log, pinpoint the file/line, and correct it logically. Do not guess.
