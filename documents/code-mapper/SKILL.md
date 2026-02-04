---
name: code-mapper
description: Create, update, and review code-map and spec documents for features. Use this skill to document code execution flows, trace function calls, and maintain architectural documentation in docs/2-current/.
---

# Code Mapper

Create and maintain code-map and spec documents that accurately reflect the codebase.

## Document Types

| Type | Pattern | Purpose |
|------|---------|---------|
| Code-map | `docs/2-current/map-*.md` | Trace execution flows |
| Spec | `docs/2-current/spec-*.md` | Architecture, schemas, APIs |

## Analysis Process

1. **Identify starting point**: API endpoint, function, command line
2. **Trace execution**: Follow code from entry to completion
3. **Document control flow**: Conditions, branches, exceptions
4. **Create sub-flows**: Tree structure for complex paths
5. **Capture business logic**: Input options, edge cases

## Code-Map Structure

See `references/codemap-guide.md` for complete format.

```markdown
# Feature Name
## Summary
## Major Flow Blocks
## Flow Diagram (Mermaid)
## Component Call Graph
## Starting Trace Block [[↑ Flow Diagram](#flow-diagram)]
## Sub-flow A [[↑ Flow Diagram](#flow-diagram)]
## Helper Functions [[↑ Flow Diagram](#flow-diagram)]
## Configuration and Environment [[↑ Flow Diagram](#flow-diagram)]
## Error Handling Summary [[↑ Flow Diagram](#flow-diagram)]
## Database Schema Integration [[↑ Flow Diagram](#flow-diagram)]
## Business Logic Summary [[↑ Flow Diagram](#flow-diagram)]
## Dependencies [[↑ Flow Diagram](#flow-diagram)]
```

## Spec Documents

For non-execution information:
- Database schemas
- API endpoint definitions
- Data types and models
- Architecture diagrams
- External component integration

Link spec documents from/to related code-map documents.

## Key Requirements

- Use relative file paths with line numbers: `[file.py:123](../../path/file.py#L123)`
- Include `[[↑ Flow Diagram](#flow-diagram)]` on section headers
- Document all inputs, outputs, and error cases
- Link all function references to their sections
- Keep Mermaid diagrams navigable with anchor links
