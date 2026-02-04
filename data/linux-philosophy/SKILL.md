---
name: linux-philosophy
description: Unix/Linux design principles for CLI tools and system architecture.
---

# Unix/Linux Philosophy

## Core Principles

1. **Do one thing well** - Each program/function should have a single purpose
2. **Compose with others** - Design for pipelines and composition
3. **Text streams** - Use text as universal interface
4. **Small, sharp tools** - Prefer focused tools over monolithic solutions
5. **Fail fast, fail loudly** - Exit on error with clear messages

## Design Guidelines

- Prefer explicit over implicit behavior
- Make default behavior safe; require flags for dangerous operations
- Support stdin/stdout for composition
- Use exit codes meaningfully (0=success, non-zero=error)
- Write to stderr for diagnostics, stdout for output

## Checklist

- [ ] Single responsibility per module/function
- [ ] Composable via standard I/O
- [ ] Clear error messages to stderr
- [ ] Meaningful exit codes
- [ ] No hidden side effects
