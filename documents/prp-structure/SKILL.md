---
name: prp-structure
description: Provides the standard structure and format for Prompt-Response-Plan (PRP) documents. Use when creating, formatting, or validating PRP documents for systematic problem-solving workflows.
---

# PRP Structure Skill

This skill defines the standard structure for Prompt-Response-Plan (PRP) documents used in context engineering workflows.

## PRP Document Structure

A well-formed PRP contains three main sections:

### 1. Prompt Section

The initial problem statement or request that initiates the workflow:

```markdown
## Prompt

[Clear, concise description of the problem or task]

### Context
- Background information
- Relevant constraints
- Success criteria
```

### 2. Response Section

Analysis and proposed approach:

```markdown
## Response

### Problem Analysis
- Key challenges identified
- Dependencies and prerequisites
- Risk factors

### Proposed Solution
- High-level approach
- Alternative approaches considered
- Rationale for chosen approach
```

### 3. Plan Section

Detailed execution plan with trackable steps:

```markdown
## Plan

### Implementation Steps

1. [ ] Step 1: [Description]
   - Sub-tasks if needed
   - Expected outcome

2. [ ] Step 2: [Description]
   - Dependencies: Step 1
   - Expected outcome

3. [ ] Step 3: [Description]

### Testing Strategy
- Unit tests
- Integration tests
- Acceptance criteria

### Rollback Plan
- Contingency steps if issues arise
```

## Best Practices

- **Keep prompts focused**: One PRP per distinct problem
- **Be specific in plans**: Each step should be actionable and measurable
- **Track progress**: Use checkboxes to mark completed steps
- **Document assumptions**: Make implicit knowledge explicit
- **Include validation**: Define how success will be measured

## File Naming Convention

```
prp-[description]-[timestamp].md
```

Example: `prp-refactor-auth-module-2025-11-21.md`

## Integration with Agents

This structure works seamlessly with:
- `context-engineering-prp-generator` agent (generates PRPs)
- `context-engineering-executor` agent (executes plans)
- `context-engineering-orchestrator` agent (coordinates workflows)
