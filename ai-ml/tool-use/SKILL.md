---
name: tool-use
description: Function definition schemas, API sanitization, and execution constraints.
---

# Tool Use

Function definition schemas, API sanitization, and execution constraints.

## Core Guidelines

- **Explicit Schemas**: Define function arguments, types, and descriptions in clean JSON schemas.
- **Input Verification**: Sanitize parameters before running tools (prevent injection/escapes).
- **Graceful Failure**: Handle tool timeouts and errors cleanly without crashing the main loop.
