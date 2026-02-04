---
name: strict-tool-implementer
version: 0.2.1
description: >-
  Use PROACTIVELY when building multi-step agentic workflows with validated tool parameters.
  Implements Anthropic's strict tool use mode for guaranteed schema compliance.
  Covers tool schema design, multi-tool agent workflows, error handling, testing, and production patterns.
  Not for data extraction or classification tasks (use json-outputs-implementer instead).
---

# Strict Tool Implementer

## Overview

This skill implements Anthropic's strict tool use mode for reliable agentic systems. With `strict: true`, tool input parameters are guaranteed to match your schema—no validation needed in your tool functions.

**What This Skill Provides:**
- Production-ready tool schema design
- Multi-tool workflow patterns
- Agentic system architecture
- Validation and error handling
- Complete agent implementation examples

**Prerequisites:**
- Decision made via `structured-outputs-advisor`
- Model: Claude Sonnet 4.5 or Opus 4.1
- Beta header: `structured-outputs-2025-11-13`

## When to Use This Skill

**Use for:**
- Building multi-step agentic workflows
- Validating function call parameters
- Ensuring type-safe tool execution
- Complex tools with nested properties
- Critical operations requiring guaranteed types

**NOT for:**
- Extracting data from text/images → `json-outputs-implementer`
- Formatting API responses → `json-outputs-implementer`
- Classification tasks → `json-outputs-implementer`

## Response Style

- **Tool-focused**: Design tools with clear, validated schemas
- **Agent-aware**: Consider multi-tool workflows and composition
- **Type-safe**: Guarantee parameter types for downstream functions
- **Production-ready**: Handle errors, retries, and monitoring
- **Example-driven**: Provide complete agent implementations

## Workflow

| Phase | Description | Details |
|-------|-------------|---------|
| 1 | Tool Schema Design | → [workflow/phase-1-schema-design.md](workflow/phase-1-schema-design.md) |
| 2 | Multi-Tool Agent Implementation | → [workflow/phase-2-implementation.md](workflow/phase-2-implementation.md) |
| 3 | Error Handling & Validation | → [workflow/phase-3-error-handling.md](workflow/phase-3-error-handling.md) |
| 4 | Testing Agent Workflows | → [workflow/phase-4-testing.md](workflow/phase-4-testing.md) |
| 5 | Production Agent Patterns | → [workflow/phase-5-production.md](workflow/phase-5-production.md) |

## Quick Reference

### Schema Template

```python
{
    "name": "tool_name",
    "description": "Clear description",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...],
        "additionalProperties": False
    }
}
```

### Supported Schema Features

✅ Basic types, enums, format strings, nested objects/arrays, required fields

❌ Recursive schemas, min/max constraints, string length, complex regex

## Reference Materials

- [Common Agentic Patterns](reference/common-patterns.md)
- [Success Criteria](reference/success-criteria.md)

## Related Skills

- `structured-outputs-advisor` - Choose the right mode
- `json-outputs-implementer` - For data extraction use cases
