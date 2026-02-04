---
name: writing-use-cases
description: Create structured use case documentation with sequence diagrams for backend systems. Use when documenting API endpoints, service interactions, event flows, or system behaviors. Triggers on requests like "document this use case", "create use case for X endpoint", "write flow documentation", or "explain how X feature works".
---

# Writing Use Cases

Create use case markdown files that document backend flows with mermaid sequence diagrams.

## Discovery Workflow

1. **Identify entry point** - Find the controller/handler for the endpoint
2. **Trace the flow** - Follow method calls, service interactions, external calls
3. **Find events** - Look for message publishing (SNS, Kafka, RabbitMQ, etc.)
4. **Map state transitions** - Identify entity state changes
5. **Note validations** - Document validation rules and constraints

## Output Structure

```markdown
# {Feature Name} Use Case

## Overview
{1-2 sentences: what this use case does and when it's triggered}

## Flow

{mermaid sequence diagram - see references/mermaid-patterns.md}

## Key Points

- **Entry Point:** `{HTTP method} {path}` ([`{ControllerName}`]({relative-path}))
- **Request Model:** [`{DtoName}`]({relative-path})
- **State Transition:** {from} → {to}
- **Event:** `{EventName}` published to {destination}
- **Validation:** {key validation rules}
```

## Output File

- Use the `docs/{use case name}-use-case.md` as output file location (DEFAULT).
- Ask the User, if the default is fine or another location should be used.

## Writing Guidelines

- Keep overview concise (1-2 sentences)
- Use relative links to source files
- Include all actors and systems in the diagram
- Group related operations with `Note over` blocks
- Use `alt/else` for conditional flows
- Document both success and error paths when relevant

## Mermaid Patterns

See [references/mermaid-patterns.md](references/mermaid-patterns.md) for sequence diagram syntax and examples.
