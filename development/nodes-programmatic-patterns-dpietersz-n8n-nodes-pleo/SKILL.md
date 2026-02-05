---
name: Nodes Programmatic Patterns
description: Build n8n nodes using programmatic style with full control over execution, data handling, and API calls. Use this skill when implementing execute() methods, creating helper functions for API requests, handling pagination with cursor-based logic, implementing loadOptions for dynamic dropdowns, processing binary data, building webhook or polling triggers, or handling complex data transformations. Apply when building trigger nodes, GraphQL integrations, non-HTTP protocols, or any scenario requiring custom execution logic.
---

## When to use this skill:

- When implementing execute() methods with getInputData/getNodeParameter
- When writing helper functions for API requests (apiRequest, apiRequestAllItems)
- When implementing cursor-based or custom pagination logic
- When building loadOptions methods for dynamic dropdown options
- When handling binary data downloads and uploads
- When building webhook triggers with signature validation
- When implementing polling triggers with getWorkflowStaticData
- When processing items in loops with try-catch and continueOnFail
- When creating new objects from input data (never modify input directly)
- When working with this.helpers.httpRequest for API calls
- When handling multiple sequential API calls
- When building GraphQL integrations or non-HTTP protocols
- When needing custom authentication flows beyond declarative routing

# Nodes Programmatic Patterns

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle nodes programmatic patterns.

## Instructions

For details, refer to the information provided in this file:
[nodes programmatic patterns](../../../agent-os/standards/nodes/programmatic-patterns.md)
