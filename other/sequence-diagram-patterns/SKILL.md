---
name: sequence-diagram-patterns
version: "0.1"
description: >
  [STUB - Not implemented] Sequence diagram patterns for documenting system interactions and API flows.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# Sequence Diagram Patterns

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- Authentication/authorization flows
- API request/response sequences
- Microservice communication patterns
- Error handling and retry sequences
- Async message queue patterns
- Database transaction flows

## Example Pattern

```mermaid
sequenceDiagram
    Client->>API: POST /auth
    API->>Database: Validate credentials
    Database-->>API: User found
    API-->>Client: JWT token
```

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
